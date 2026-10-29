import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile, mkdtemp, rm } from 'node:fs/promises';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { fileURLToPath } from 'node:url';
import { assess, verify, validateScope, allowedRequest, publicIPv4, resolvePublicIPv4, criterionLedger, criterionRefs, normalizeAxe } from '../src/core.mjs';
const run = promisify(execFile);

test('scope rejects unapproved navigation, methods, and unsafe origins', () => {
  const scope = validateScope('https://governancecommons.org', ['/', '/about/']);
  assert.throws(() => allowedRequest('https://governancecommons.org/admin', scope, 'document'));
  assert.throws(() => allowedRequest('https://127.0.0.1/private', scope));
  assert.throws(() => allowedRequest('file:///etc/passwd', scope));
  assert.throws(() => allowedRequest('https://governancecommons.org/', scope, 'resource', 'POST'));
  assert.throws(() => validateScope('http://governancecommons.org', ['/']));
  assert.throws(() => validateScope('https://127.0.0.1', ['/']));
  assert.throws(() => validateScope('https://governancecommons.org', ['/../admin']));
  assert.equal(publicIPv4('127.0.0.1'), false);
  assert.equal(publicIPv4('10.0.0.1'), false);
  assert.equal(publicIPv4('169.254.169.254'), false);
  assert.equal(publicIPv4('192.168.1.1'), false);
  assert.equal(publicIPv4('172.31.1.1'), false);
  assert.equal(publicIPv4('8.8.8.8'), true);
});

test('all WCAG 2.2 A/AA criteria begin unresolved and 4.1.1 is absent', () => {
  const rows = criterionLedger([]);
  assert.equal(rows.length, 55);
  assert.equal(rows.some(row => row.id === '4.1.1'), false);
  assert.equal(rows.some(row => row.outcome === 'verified-pass'), false);
  assert.deepEqual(criterionRefs(['wcag111', 'wcag411', 'wcag22aa']), ['1.1.1']);
});

test('ten domains map valid criteria and preserve all eighteen draft procedure IDs', async () => {
  const profile = JSON.parse(await readFile(new URL('../profile.json', import.meta.url), 'utf8'));
  const catalog = JSON.parse(await readFile(new URL('../criteria.json', import.meta.url), 'utf8'));
  const ids = new Set(catalog.criteria.map(row => row.id));
  assert.equal(profile.domains.length, 10);
  assert.equal(new Set(profile.domains.map(row => row.id)).size, 10);
  for (const domain of profile.domains) for (const id of domain.criteria) assert.ok(ids.has(id), `${domain.id}: ${id}`);
  const procedures = new Set(profile.domains.flatMap(row => row.draft_procedures));
  for (let n = 1; n <= 18; n++) assert.ok(procedures.has(`GC-A11Y-${String(n).padStart(2, '0')}`));
  for (const criterion of catalog.criteria) {
    assert.ok(['A', 'AA'].includes(criterion.level));
    assert.match(criterion.url, /^https:\/\/www\.w3\.org\/TR\/2024\/REC-WCAG22-20241212\/#/);
  }
});

test('DNS with any private answer is refused before a connection', async () => {
  const mixed = async () => [{ address: '8.8.8.8' }, { address: '127.0.0.1' }];
  await assert.rejects(resolvePublicIPv4('example.org', mixed));
  assert.equal(await resolvePublicIPv4('example.org', async () => [{ address: '8.8.8.8' }]), '8.8.8.8');
});

test('automated rule pass never implies criterion pass', () => {
  const findings = normalizeAxe('https://example.org/', { violations: [], incomplete: [], passes: [{ id: 'image-alt', tags: ['wcag111'] }] }, '2026-10-28T00:00:00Z');
  assert.equal(findings.length, 0);
  assert.notEqual(criterionLedger(findings).find(row => row.id === '1.1.1').outcome, 'verified-pass');
});

test('inaccessible independent fixture produces evidence and remediation can be rescanned', async () => {
  const bad = await readFile(new URL('../fixtures/inaccessible.html', import.meta.url), 'utf8');
  const good = await readFile(new URL('../fixtures/remediated.html', import.meta.url), 'utf8');
  const first = await assess({ fixtureHtml: bad, targetId: 'fixture' });
  verify(first);
  assert.ok(first.findings.some(row => row.status === 'verified-failure'));
  assert.ok(first.scope.sampled_pages[0].rule_results.some(row => row.status === 'verified-pass'));
  assert.ok(first.scope.sampled_pages[0].rule_results.some(row => row.status === 'not-applicable'));
  assert.ok(first.findings.some(row => row.remediation && row.verification && row.evidence_refs.length));
  assert.ok(first.criterion_ledger.every(row => row.outcome !== 'verified-pass'));
  assert.equal(first.scope.full_conformance_claim, false);
  const second = await assess({ fixtureHtml: good, targetId: 'fixture' });
  verify(second);
  assert.ok(second.findings.length < first.findings.length);
  assert.ok(second.manual_review.every(row => row.status === 'needs-manual-review'));
  const tampered = structuredClone(first);
  tampered.findings[0].observed = 'changed';
  assert.throws(() => verify(tampered));
});

test('browser fixture cannot fetch a loopback resource', async () => {
  let hits = 0;
  const server = http.createServer((_request, response) => { hits++; response.end('secret'); });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try {
    const port = server.address().port;
    const report = await assess({ fixtureHtml: `<!doctype html><html lang="en"><title>Isolation</title><body><main><h1>Test</h1><img src="http://127.0.0.1:${port}/secret.png"></main></body></html>` });
    assert.equal(hits, 0);
    assert.ok(report.network.blocked.some(item => item.url.includes('127.0.0.1')));
  } finally { await new Promise(resolve => server.close(resolve)); }
});

test('CLI exports both reports and links reverification without rewriting prior evidence', async () => {
  const root = await mkdtemp(path.join(os.tmpdir(), 'gc-a11y-test-'));
  try {
    const firstDir = path.join(root, 'first');
    const secondDir = path.join(root, 'second');
    const cli = fileURLToPath(new URL('../src/cli.mjs', import.meta.url));
    const bad = fileURLToPath(new URL('../fixtures/inaccessible.html', import.meta.url));
    const good = fileURLToPath(new URL('../fixtures/remediated.html', import.meta.url));
    await run(process.execPath, [cli, 'assess', '--fixture', bad, '--output', firstDir]);
    const priorBytes = await readFile(path.join(firstDir, 'report.json'));
    await run(process.execPath, [cli, 'assess', '--fixture', good, '--prior', path.join(firstDir, 'report.json'), '--output', secondDir]);
    assert.deepEqual(await readFile(path.join(firstDir, 'report.json')), priorBytes);
    const first = JSON.parse(priorBytes);
    const second = JSON.parse(await readFile(path.join(secondDir, 'report.json'), 'utf8'));
    assert.equal(second.reverification_of, first.report_digest);
    verify(second);
    assert.match(await readFile(path.join(secondDir, 'report.md'), 'utf8'), /Criterion coverage/);
  } finally { await rm(root, { recursive: true, force: true }); }
});
