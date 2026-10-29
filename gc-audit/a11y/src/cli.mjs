#!/usr/bin/env node
import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { assess, verify } from './core.mjs';

function argsOf(argv) {
  const [command, ...rest] = argv;
  const options = {};
  for (let i = 0; i < rest.length; i += 2) {
    if (!rest[i]?.startsWith('--') || !rest[i + 1] || rest[i + 1].startsWith('--')) throw new Error(`missing value for ${rest[i] || 'option'}`);
    options[rest[i].slice(2)] = rest[i + 1];
  }
  return { command, options };
}
const safe = value => String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('|', '\\|').replaceAll('\r', ' ').replaceAll('\n', ' ');

export function markdown(report) {
  const lines = [
    '# GC-AUDIT A11Y assessment', '',
    `Target: ${safe(report.target.origin)}`,
    `Observed: ${safe(report.started_at)} to ${safe(report.completed_at)}`,
    `Scope: ${report.scope.sampled_pages.length} sampled page(s); WCAG 2.2 A/AA; ${safe(report.environment.browser)}; axe ${safe(report.environment.axe)}.`, '',
    '**This is a bounded automated assessment, not a WCAG conformance claim.** Manual keyboard, visual, responsive, and screen-reader review remains open.', '',
    '## Findings', ''
  ];
  if (!report.findings.length) lines.push('No automated violations were reported in this sample. This does not establish criterion passes.', '');
  for (const f of report.findings) lines.push(
    `### ${safe(f.id)} — ${safe(f.status)}`, '',
    `- URL: ${safe(f.url)}`, `- Element/state: ${safe(f.component)}`,
    `- WCAG: ${f.criterion_refs.length ? f.criterion_refs.map(c => `[${safe(c.id)} (${safe(c.level)})](${c.url})`).join(', ') : 'Advisory; no criterion asserted'}`,
    `- Observed: ${safe(f.observed)}`, `- Impact: ${safe(f.impact)}`,
    `- Severity: ${safe(f.severity)} — ${safe(f.severity_rationale)}`,
    `- Evidence: ${f.evidence_refs.map(safe).join(', ')}`,
    `- Remediation: ${safe(f.remediation)}`, `- Reverify: ${safe(f.verification)}`,
    `- Limitation: ${f.limitations.map(safe).join('; ')}`, ''
  );
  lines.push('## Criterion coverage', '',
    `${report.criterion_ledger.length} WCAG 2.2 A/AA criteria recorded; ${report.criterion_ledger.filter(c => c.outcome === 'verified-failure').length} with automated failure evidence; no criterion was inferred to pass.`, '',
    '## Manual review', '',
    ...report.manual_review.map(row => `- ${safe(row.domain_id)}: ${safe(row.status)} (${row.draft_procedures.map(safe).join(', ')})`), '',
    '## Provenance and limits', '',
    `- Report digest: ${safe(report.report_digest)}`,
    `- Evidence manifest digest: ${safe(report.evidence_manifest.digest)}`,
    `- Profile digest: ${safe(report.profile.digest)}`,
    `- Catalog digest: ${safe(report.catalog.digest)}`,
    ...report.limitations.map(safe).map(s => `- ${s}`), ''
  );
  return lines.join('\n');
}

async function main() {
  const { command, options } = argsOf(process.argv.slice(2));
  if (command === 'verify') {
    const report = JSON.parse(await readFile(options.report, 'utf8'));
    verify(report);
    console.log(JSON.stringify({ status: 'VALID_INTEGRITY_ONLY', digest: report.report_digest }));
    return;
  }
  if (command !== 'assess' || !options.output) throw new Error('usage: assess --origin HTTPS_ORIGIN --paths /,/about/ --authorize-read-only yes --output NEW_DIRECTORY [--prior OLD_REPORT]; or verify --report REPORT');
  const fixtureHtml = options.fixture ? await readFile(options.fixture, 'utf8') : undefined;
  if (fixtureHtml === undefined && options['authorize-read-only'] !== 'yes') throw new Error('explicit read-only website authorization required');
  if (fixtureHtml === undefined && (!options.origin || !options.paths)) throw new Error('origin and bounded page paths required');
  const prior = options.prior ? JSON.parse(await readFile(options.prior, 'utf8')) : undefined;
  if (prior) verify(prior);
  const output = path.resolve(options.output);
  if (await stat(output).then(() => true, () => false)) throw new Error('output directory already exists; preserve prior evidence');
  const report = await assess({ origin: options.origin, paths: options.paths?.split(','), fixtureHtml, targetId: options['target-id'] || 'external-website' });
  if (prior) {
    report.reverification_of = prior.report_digest;
    const { digest } = await import('./core.mjs');
    report.report_digest = digest(Object.fromEntries(Object.entries(report).filter(([key]) => key !== 'report_digest')));
  }
  verify(report);
  await mkdir(output, { recursive: false });
  await writeFile(path.join(output, 'report.json'), `${JSON.stringify(report, null, 2)}\n`, { flag: 'wx' });
  await writeFile(path.join(output, 'report.md'), markdown(report), { flag: 'wx' });
  console.log(JSON.stringify({ status: 'BOUNDED_ASSESSMENT', report: path.join(output, 'report.json'), digest: report.report_digest, findings: report.findings.length }));
}

main().catch(error => { console.error(JSON.stringify({ status: 'EVALUATION_ERROR', reason: error.message })); process.exitCode = 2; });
