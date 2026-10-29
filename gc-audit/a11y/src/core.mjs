import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import dns from 'node:dns/promises';
import https from 'node:https';
import net from 'node:net';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const PROFILE = JSON.parse(await readFile(path.join(ROOT, 'profile.json'), 'utf8'));
const CATALOG = JSON.parse(await readFile(path.join(ROOT, 'criteria.json'), 'utf8'));
const BY_ID = new Map(CATALOG.criteria.map(c => [c.id, c]));
const MAX_PAGES = 6;
const MAX_REQUEST = 5 * 1024 * 1024;
const MAX_TOTAL = 40 * 1024 * 1024;
function withTimeout(promise, ms, message) {
  let timer;
  return Promise.race([promise, new Promise((_resolve, reject) => { timer = setTimeout(() => reject(new Error(message)), ms); })])
    .finally(() => clearTimeout(timer));
}

export function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (value !== null && typeof value === 'object') return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonical(value[k])}`).join(',')}}`;
  return JSON.stringify(value);
}
export const digest = value => `sha256:${createHash('sha256').update(canonical(value)).digest('hex')}`;
const hash = value => createHash('sha256').update(value).digest('hex');

export function validateScope(origin, paths) {
  const base = new URL(origin);
  if (base.protocol !== 'https:' || base.username || base.password || base.search || base.hash || base.pathname !== '/' || base.port) throw new Error('target origin must be a bare HTTPS origin');
  if (net.isIP(base.hostname) || base.hostname === 'localhost' || !base.hostname.includes('.')) throw new Error('target origin must be a public DNS name');
  if (!Array.isArray(paths) || !paths.length || paths.length > MAX_PAGES || new Set(paths).size !== paths.length) throw new Error('one to six unique page paths required');
  for (const p of paths) {
    if (typeof p !== 'string' || !p.startsWith('/') || p.startsWith('//') || p.includes('\\') || p.includes('?') || p.includes('#') || new URL(p, base).pathname !== p) throw new Error('invalid allowlisted page path');
  }
  return { origin: base.origin, paths };
}

export function publicIPv4(ip) {
  if (net.isIP(ip) !== 4) return false;
  const a = ip.split('.').map(Number);
  return !(a[0] === 0 || a[0] === 10 || a[0] === 127 || a[0] >= 224 ||
    (a[0] === 100 && a[1] >= 64 && a[1] <= 127) ||
    (a[0] === 169 && a[1] === 254) || (a[0] === 172 && a[1] >= 16 && a[1] <= 31) ||
    (a[0] === 192 && a[1] === 168) || (a[0] === 192 && a[1] === 0) ||
    (a[0] === 192 && a[1] === 0 && a[2] === 2) ||
    (a[0] === 198 && (a[1] === 18 || a[1] === 19 || a[1] === 51)) ||
    (a[0] === 203 && a[1] === 0 && a[2] === 113));
}

export function allowedRequest(raw, scope, kind = 'resource', method = 'GET') {
  const u = new URL(raw);
  if (u.origin !== scope.origin || u.username || u.password || !['GET', 'HEAD'].includes(method)) throw new Error('request outside authorized origin or read-only methods');
  if (kind === 'document' && !scope.paths.includes(u.pathname)) throw new Error('document outside bounded URL allowlist');
  if (kind !== 'document' && (!['stylesheet', 'script', 'image', 'font', 'media'].includes(kind) ||
      !/\.(?:css|js|mjs|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|otf|mp4|webm|avif)$/i.test(u.pathname)))
    throw new Error('non-static or active subresource blocked');
  return u;
}

export async function resolvePublicIPv4(hostname, resolver = dns.lookup) {
  const answers = await resolver(hostname, { family: 4, all: true, verbatim: true });
  if (!Array.isArray(answers) || !answers.length || answers.some(a => !publicIPv4(a.address))) throw new Error('DNS resolved to unsafe address');
  return answers[0].address;
}

async function safeFetch(raw, scope, kind, state, redirects = 0) {
  const u = allowedRequest(raw, scope, kind);
  if (redirects > 3) throw new Error('redirect limit exceeded');
  const ip = await resolvePublicIPv4(u.hostname);
  return await new Promise((resolve, reject) => {
    const request = https.request(u, {
      method: 'GET', timeout: 10000, servername: u.hostname,
      lookup: (_host, options, cb) => options.all ? cb(null, [{ address: ip, family: 4 }]) : cb(null, ip, 4),
      headers: { 'user-agent': 'GC-AUDIT-A11Y/0.1 read-only assessment', accept: '*/*' }
    }, response => {
      if (response.statusCode >= 300 && response.statusCode < 400) {
        response.resume();
        if (!response.headers.location) return reject(new Error('redirect without location'));
        const next = new URL(response.headers.location, u).href;
        safeFetch(next, scope, kind, state, redirects + 1).then(resolve, reject);
        return;
      }
      const chunks = []; let size = 0;
      response.on('data', chunk => {
        size += chunk.length; state.bytes += chunk.length;
        if (size > MAX_REQUEST || state.bytes > MAX_TOTAL) response.destroy(new Error('response budget exceeded'));
        else chunks.push(chunk);
      });
      response.on('error', reject);
      response.on('end', () => resolve({ status: response.statusCode, contentType: response.headers['content-type'] || 'application/octet-stream', body: Buffer.concat(chunks), finalUrl: u.href, ip }));
    });
    request.on('timeout', () => request.destroy(new Error('navigation timeout')));
    request.on('error', reject);
    request.end();
  });
}

export function criterionRefs(tags) {
  const refs = new Set();
  for (const tag of tags || []) {
    const match = /^wcag([1-4])([1-9])([1-9])$/.exec(tag);
    if (match) {
      const id = `${match[1]}.${match[2]}.${match[3]}`;
      if (BY_ID.has(id)) refs.add(id);
    }
  }
  return [...refs].sort();
}

export function normalizeAxe(url, axe, observedAt) {
  const findings = [];
  for (const [bucket, status] of [['violations', 'verified-failure'], ['incomplete', 'needs-manual-review']]) {
    for (const rule of axe[bucket] || []) for (const node of rule.nodes || []) {
      const target = (node.target || []).join(' ').slice(0, 500);
      const refs = criterionRefs(rule.tags);
      const id = `A11Y-${hash(`${url}|${rule.id}|${target}`).slice(0, 16)}`;
      findings.push({ id, kind: refs.length ? 'normative-rule' : 'advisory', status: refs.length ? status : 'observation',
        url, component: target || '(document)', criterion_refs: refs.map(ref => ({ id: ref, level: BY_ID.get(ref).level, url: BY_ID.get(ref).url })),
        procedure: `axe-core:${String(rule.id).slice(0, 100)}`, method: 'automated', observed_at: observedAt,
        observed: String(node.failureSummary || rule.help || '').slice(0, 1200),
        impact: String(rule.help || 'Potential barrier requiring human review.'),
        severity: ({ critical: 'Critical', serious: 'High', moderate: 'Medium', minor: 'Low' })[rule.impact] || 'Medium',
        severity_rationale: `axe impact ${rule.impact || 'unknown'}; human task impact requires review`,
        remediation: String(rule.help || 'Review the element against the referenced criterion.'),
        verification: `Repair ${target || 'the affected element'}; rerun axe rule ${rule.id} and review the criterion manually.`,
        evidence_refs: [`axe:${id}`], limitations: ['Automated rule result does not establish complete success-criterion coverage.'] });
    }
  }
  return findings;
}

export function criterionLedger(findings) {
  return CATALOG.criteria.map(c => {
    const matching = findings.filter(f => f.criterion_refs.some(r => r.id === c.id));
    return { id: c.id, level: c.level, url: c.url, domains: c.domains,
      applicability: 'undetermined', outcome: matching.some(f => f.status === 'verified-failure') ? 'verified-failure' :
        matching.length || c.domains.length ? 'needs-manual-review' : 'not-tested',
      evidence_refs: matching.flatMap(f => f.evidence_refs),
      limitation: 'Criterion-level applicability and complete coverage require human evaluation.' };
  });
}

export async function assess({ origin, paths, fixtureHtml, targetId = 'external-website' }) {
  const scope = fixtureHtml === undefined ? validateScope(origin, paths) : { origin: 'fixture://local', paths: ['/fixture'] };
  const started = new Date().toISOString();
  const state = { bytes: 0, blocked: [], requests: [], active: 0 };
  const browserEnv = Object.fromEntries(['PATH', 'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP', 'HOME', 'USERPROFILE', 'LANG', 'LC_ALL']
    .filter(key => process.env[key] !== undefined).map(key => [key, process.env[key]]));
  const browser = await chromium.launch({ headless: true, env: browserEnv, proxy: { server: 'http://127.0.0.1:9' },
    args: ['--disable-quic', '--force-webrtc-ip-handling-policy=disable_non_proxied_udp'] });
  const pages = []; const findings = []; const evidence = [];
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, serviceWorkers: 'block', acceptDownloads: false,
      permissions: [], javaScriptEnabled: true });
    await context.routeWebSocket('**/*', ws => { state.blocked.push({ url: ws.url(), reason: 'websocket prohibited' }); ws.close(); });
    await context.route('**/*', async route => {
      const request = route.request();
      const kind = request.resourceType();
      try {
        allowedRequest(request.url(), scope, kind, request.method());
        if (state.active >= 4) throw new Error('concurrency bound exceeded');
        state.active++;
        try {
          const result = await safeFetch(request.url(), scope, kind, state);
          state.requests.push({ url: request.url(), status: result.status, resolved_ip: result.ip, bytes: result.body.length });
          await route.fulfill({ status: result.status, contentType: result.contentType, body: result.body });
        } finally { state.active--; }
      } catch (error) {
        state.blocked.push({ url: request.url(), reason: String(error.message).slice(0, 200) });
        if (process.env.GC_A11Y_DEBUG === '1') console.error(JSON.stringify(state.blocked.at(-1)));
        await route.abort('blockedbyclient').catch(() => {});
      }
    });
    for (const pagePath of scope.paths) {
      const page = await context.newPage();
      page.on('popup', popup => { void popup.close(); });
      page.setDefaultTimeout(12000);
      const url = fixtureHtml === undefined ? `${scope.origin}${pagePath}` : 'fixture://local/fixture';
      let response;
      if (fixtureHtml === undefined) response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 12000 });
      else await page.setContent(fixtureHtml, { waitUntil: 'domcontentloaded' });
      if (fixtureHtml === undefined && (!response || response.status() >= 400)) throw new Error(`page unavailable: ${url}`);
      if (fixtureHtml === undefined && page.url() !== url) throw new Error(`page navigated outside exact sample URL: ${page.url()}`);
      const observedAt = new Date().toISOString();
      const axe = await withTimeout(new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']).analyze(), 20000, 'axe analysis timeout');
      if (fixtureHtml === undefined && page.url() !== url) throw new Error(`page navigated during assessment: ${page.url()}`);
      const ruleResults = Object.entries({ violations: 'verified-failure', incomplete: 'inconclusive', passes: 'verified-pass', inapplicable: 'not-applicable' })
        .flatMap(([bucket, status]) => axe[bucket].map(rule => ({ rule_id: rule.id, status,
          criterion_refs: criterionRefs(rule.tags), node_count: rule.nodes.length })));
      const rows = normalizeAxe(url, axe, observedAt);
      findings.push(...rows);
      for (const row of rows) evidence.push({ id: row.evidence_refs[0], type: 'axe-rule-result', capture_method: 'axe-core in isolated Chromium',
        captured_at: observedAt, url, rule: row.procedure, selector: row.component, result: row.status,
        observed: row.observed, impact: row.impact,
        sha256: digest({ url, rule: row.procedure, selector: row.component, result: row.status, observed: row.observed, impact: row.impact }) });
      const structure = await page.evaluate(() => ({
        headings: [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(el => ({ level: Number(el.tagName[1]), text: (el.textContent || '').trim().slice(0, 120) })),
        landmarks: [...document.querySelectorAll('main,nav,header,footer,aside')].map(el => el.tagName.toLowerCase()),
        images: document.images.length, forms: document.forms.length,
        horizontal_overflow: document.documentElement.scrollWidth > innerWidth
      }));
      await page.setViewportSize({ width: 320, height: 800 });
      const reflow = await page.evaluate(() => ({ viewport_width: innerWidth, content_width: document.documentElement.scrollWidth,
        horizontal_overflow: document.documentElement.scrollWidth > innerWidth }));
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.addStyleTag({ content: 'html { font-size: 200% !important; }' });
      const textResize = await page.evaluate(() => ({ method: 'root-font-size override at 200%; approximation, not browser text-only zoom',
        viewport_width: innerWidth, content_width: document.documentElement.scrollWidth,
        horizontal_overflow: document.documentElement.scrollWidth > innerWidth }));
      pages.push({ url, status: response?.status() || 200, title: (await page.title()).slice(0, 200),
        viewport: { width: 1280, height: 800 }, axe: { violations: axe.violations.length, incomplete: axe.incomplete.length,
          passes: axe.passes.length, inapplicable: axe.inapplicable.length }, rule_results: ruleResults,
        structure, reflow, text_resize: textResize, observed_at: observedAt });
      await page.close();
    }
    await context.close();
  } finally { await browser.close(); }
  const ledger = criterionLedger(findings);
  const report = { schema: 'gc-audit.a11y-report.v0.1', version: '0.1.0', target: { id: targetId, type: fixtureHtml === undefined ? 'public-website' : 'fixture', origin: scope.origin,
    authorized_paths: scope.paths, authorization: fixtureHtml === undefined ? 'explicit CLI operator grant' : 'local test fixture' },
    scope: { sampled_pages: pages, methodology: PROFILE.methodology, standard: PROFILE.standard, full_conformance_claim: false },
    profile: { id: PROFILE.id, version: PROFILE.version, digest: digest(PROFILE) }, catalog: { source: CATALOG.source, digest: digest(CATALOG), criterion_count: CATALOG.criteria.length },
    environment: { browser: `Chromium ${browser.version()}`, playwright: (await readFile(path.join(ROOT, 'node_modules/playwright/package.json'), 'utf8').then(JSON.parse)).version,
      axe: (await readFile(path.join(ROOT, 'node_modules/axe-core/package.json'), 'utf8').then(JSON.parse)).version, viewport: '1280x800 CSS px',
      isolation: 'new browser context; no credentials; HTTP GET via validated public-IP fetch; blocked browser direct proxy; WebSocket disabled' },
    started_at: started, completed_at: new Date().toISOString(), findings, criterion_ledger: ledger,
    manual_review: PROFILE.domains.map(d => ({ domain_id: d.id, status: 'needs-manual-review', draft_procedures: d.draft_procedures })),
    evidence_manifest: { method: 'canonical JSON SHA-256; integrity only, not authentication', entries: evidence, digest: digest(evidence) },
    network: { requests: state.requests, blocked: state.blocked, total_bytes: state.bytes },
    limitations: ['Automated rules cover only parts of WCAG criteria; no full conformance claim.',
      'No human keyboard, visual, responsive, or screen-reader review was performed by this command. Reflow and text resize geometry is observational only.',
      'The report digest detects changes but does not authenticate the assessor or target.',
      'The remote browser blocks direct proxy traffic; the host process itself requires a trusted execution environment.'] };
  report.report_digest = digest(report);
  return report;
}

export function verify(report) {
  if (report?.schema !== 'gc-audit.a11y-report.v0.1' || report.scope?.full_conformance_claim !== false ||
      report.catalog?.digest !== digest(CATALOG) || report.profile?.digest !== digest(PROFILE) ||
      report.evidence_manifest?.digest !== digest(report.evidence_manifest.entries) ||
      report.report_digest !== digest(Object.fromEntries(Object.entries(report).filter(([key]) => key !== 'report_digest')))) throw new Error('invalid or changed A11Y report');
  if (canonical(report.criterion_ledger) !== canonical(criterionLedger(report.findings))) throw new Error('invalid criterion ledger');
  const evidenceById = new Map(report.evidence_manifest.entries.map(row => [row.id, row]));
  if (evidenceById.size !== report.evidence_manifest.entries.length) throw new Error('duplicate evidence IDs');
  for (const row of report.evidence_manifest.entries) {
    const body = { url: row.url, rule: row.rule, selector: row.selector, result: row.result, observed: row.observed, impact: row.impact };
    if (row.sha256 !== digest(body)) throw new Error('invalid evidence entry');
  }
  for (const finding of report.findings) {
    if (!['verified-failure', 'observation', 'needs-manual-review'].includes(finding.status) ||
        finding.evidence_refs.some(id => !evidenceById.has(id)) ||
        finding.criterion_refs.some(ref => !BY_ID.has(ref.id) || ref.level !== BY_ID.get(ref.id).level || ref.url !== BY_ID.get(ref.id).url))
      throw new Error('invalid finding or evidence reference');
  }
  return true;
}
