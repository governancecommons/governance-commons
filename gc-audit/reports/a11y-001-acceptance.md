# GC-AUDIT-A11Y-001 — v0.1 owner review candidate

The implementation and [six-page pilot](a11y-001-pilot-assessment.md) are ready for review. Full milestone acceptance is **blocked** by the literal AC-01 contract-reuse requirement and existing repository validation failures described below. No merge, deployment, live-site repair, accessibility certification or whole-site conformance is claimed.

## Acceptance matrix

| ID | Status | Evidence and limit |
| --- | --- | --- |
| AC-01 | **PARTIAL / BLOCKED** | Reuses GC-AUDIT directory, native CLI/export/verify pattern, canonical JSON digest semantics, and TARGET-001 target fields. The universal target descriptor is specification-only; the current executable report/evidence schemas are ZTA-specific, and the operation registry accepts PowerShell governance verbs only. This domain-specific report cannot honestly claim reuse of an executable universal target/evidence/report contract. Smallest resolution: owner approves this scoped v0.1 compatibility or separately governs a universal cross-domain contract. |
| AC-02 | PASS | `criteria.json` contains 55 active WCAG 2.2 A/AA criteria with version-pinned W3C URLs and levels; 4.1.1 is excluded. Applicability defaults to undetermined, with no inferred pass. |
| AC-03 | PASS with limits | Explicit CLI authorization, HTTPS origin, six-document allowlist, GET/static resource restriction, public-IP DNS gate and pinned connection, fresh Chromium context, blocked direct proxy/WebSockets/service workers, no inherited cookies, resource/timeout limits. Tests reject private origins, mixed private DNS, out-of-scope documents and loopback fetch. Host OS/browser sandbox strength was not independently audited. |
| AC-04 | PASS | Standalone HTML fixture and Node package work without target-side SDK/Cockpit. |
| AC-05 | PASS | Axe 4.14.0 rule results, node findings, evidence refs, timestamps and manifest. Rule passes do not become criterion passes. |
| AC-06 | PASS | Ten-domain `manual-checklist.md`; all ten remain `needs-manual-review` in the pilot. All 18 draft procedure IDs are preserved and mapped. |
| AC-07 | PASS | Markdown report includes impact, evidence, severity rationale, remediation and reverification for each finding. |
| AC-08 | PASS | JSON and Markdown export, embedded evidence manifest, per-entry SHA-256 and existing GC canonical digest semantics; verification detects tampering. Integrity is not authentication. |
| AC-09 | PASS | Six live public routes assessed; `/components/` 404 replaced by `/ecosystem/`. Two contrast failures and 56 manual-review nodes recorded. |
| AC-10 | PASS | Tests enforce no criterion pass from axe passes, incomplete criterion ledger, mixed private DNS rejection, loopback fetch refusal, output verification and preservation of prior evidence. |
| AC-11 | PASS | No public website or unrelated audit-domain implementation was edited. The 18-procedure draft was copied unchanged for traceability. |
| AC-12 | PASS locally | Fresh temporary package copy installed with `npm ci`; Chromium installed; eight tests passed. Windows was executed locally; the new three-OS CI matrix awaits hosted results. |

## Validation record

- A11Y local and clean-install fixture suites: 8/8 pass on Windows, Node 24.14.1, Chromium 156.0.8078.4.
- Existing ZTA regression suite: 206/206 pass with isolated Python 3.13 dependencies.
- GC-AUDIT operation registry semantic validation: valid, runtime security assurance `UNVERIFIED`.
- GC-AUDIT zero-trust posture: 0 errors, 2 pre-existing warnings about `validate-portfolio-health.ps1`.
- GC-AUDIT Level 1: fails the pre-existing REVIEW-GRAMMAR topology check; other listed checks passed. This was present before A11Y work and is not amended here.
- Existing HCI contract tests: 3 errors in the pre-existing `finding` schema (`properties.allOf` is an array, invalid under JSON Schema Draft 2020-12). HCI schema repair is a separate scope; no HCI result is claimed green.
- Preflight stamp: completed late; the timing gap was disclosed in the working session. It is a process limitation, not evidence for A11Y conformance.
- Exact-head hosted CI and owner review: pending when this candidate was prepared.

## Changed-file inventory

- `gc-audit/a11y/`: pinned package/lockfile, 55-criterion catalog, ten-domain profile, bounded browser CLI, tests, fixtures, manual procedures and independent runbook.
- `gc-audit/specifications/GC-AUDIT-A11Y-001.md`: owner-supplied milestone specification.
- `gc-audit/specifications/GC-A11Y-PROCEDURES-003.md`: byte-preserved prior 18-procedure draft.
- `gc-audit/reports/a11y-001-*`: machine report, detailed accessible Markdown findings, pilot assessment and acceptance record.
- `.github/workflows/gc-audit-a11y.yml`: clean fixture/report verification on three operating systems.
- `gc-audit/README.md`, `DEV-PLAN.md`, `PLAY.jsonl`: discovery and append-only review state.

## OBDD classification

**BLOCKER:** literal AC-01 universal-contract reuse remains unresolved; the inherited Level 1/HCI validation failures and exact-head hosted CI prevent a green repository-wide acceptance claim. **REQUIRED:** owner review of this focused PR, decision on AC-01's scoped compatibility, and manual evaluations before any criterion or release-level assertion. **DEFERRED:** full-site scanning, monitoring, certification, AI remediation, dashboards and broader HCI work.
