# GC-AUDIT A11Y 0.1.0

This is a bounded, read-only website assessment profile. It uses WCAG 2.2 A/AA as the normative criterion catalog and WCAG-EM 2.0 to describe sampling and reporting. Automated axe results are rule results; a passing rule never closes a success criterion or establishes WCAG conformance.

## Integration inventory

| Existing GC-AUDIT surface | Reuse and boundary |
| --- | --- |
| `gc-audit/GC-AUDIT-REGISTRY.yaml` | Existing allowlisted PowerShell governance operations. It has no general website adapter/profile invocation. A11Y uses the same `gc-audit/` product directory and a native CLI, as the ZTA pilot does, without changing the frozen operation verb contract. |
| `GC-AUDIT-TARGET-001` | Website target identity, authorized public-observation surface, scope, forbidden methods, provenance and limitations are represented in the A11Y report. The universal target descriptor remains a specification, not an executable schema. |
| `zta_cli.py` / `zta_evaluator.py` | Reuses the report/export/verify pattern and canonical sorted-key JSON SHA-256 digest semantics. ZTA schemas and evaluator decisions are not reused for WCAG outcomes. |
| `trusted_evidence.py` / local host | Signed evidence is ZTA-control-specific and requires host-owned roots; this public website pilot emits integrity digests only, with no authenticated assurance claim. |
| `gc-audit.hci` contracts | HCI findings remain separate. No HCI outcome is converted into a WCAG failure. |
| `GC-A11Y-PROCEDURES-003` | The existing unmerged 18-procedure draft is preserved unchanged in `gc-audit/specifications/`; the ten domains map to its identifiers in `profile.json`. It remains a draft, not executed manual evidence. |

The six-page limit, exact HTTPS origin, document URL allowlist, GET-only transport, public IPv4 resolution, no inherited cookies, fresh Chromium context, blocked WebSockets and service workers, blocked direct browser proxy, and request budgets define the remote collection boundary. Static same-origin assets are allowed. A site that requires authenticated state, private networking, cross-origin resources, active form submission, or uncapped downloads is outside this profile.

## Install and invoke

Node.js 22+ and a fresh package directory are sufficient; the target website needs no SDK, Cockpit adapter, or instrumentation.

```text
cd gc-audit/a11y
npm ci
npx playwright install chromium
npm test
node src/cli.mjs assess --origin https://governancecommons.org --paths /,/ecosystem/,/about/,/observatory/,/conformance/,/release/ --authorize-read-only yes --target-id governancecommons.org --output ./new-assessment-directory
node src/cli.mjs verify --report ./new-assessment-directory/report.json
```

The output directory must not already exist. An assessment writes `report.json` and accessible Markdown `report.md`. `--prior OLD_REPORT` links a later run to the previous digest without overwriting evidence. For an offline fixture, use `--fixture fixtures/inaccessible.html --output NEW_DIRECTORY`; rerun on `fixtures/remediated.html` for reverification.

`verify` checks file integrity, catalog/profile digests, the evidence manifest, and the criterion ledger shape. As in the existing ZTA pilot, a digest does not authenticate the assessor, target, network, or reviewer's identity. Keep the expected digest from an independent channel when comparing reports.

## Domain and draft-procedure mapping

`profile.json` is the machine-readable map. All eighteen `GC-A11Y-01` through `GC-A11Y-18` identifiers appear at least once. The ten A11Y domains group those procedures; they do not replace or renumber them. The draft also covers dialogs, media, authentication, pointer input, motion, language and complete processes beyond the representative criteria in the ten-domain milestone. Those topics remain in the full 55-criterion ledger and the manual review plan; this v0.1 browser command does not claim they were checked. The draft's `PASS/FAIL/INCONCLUSIVE` procedure results are not silently translated into this milestone's seven finding states.

## Review limits

Read [manual-checklist.md](manual-checklist.md) before any human review. Per-page `rule_results` may be `verified-pass`, `verified-failure`, `inconclusive`, or `not-applicable` for an individual axe rule. The CLI records all ten domains as `needs-manual-review`; the full criterion ledger records observed automated failures, unresolved mapped criteria, and `not-tested` criteria. A rule-level pass is never a criterion-level pass. `4.1.1` is excluded as obsolete. Reports are a sampled observation package, not a whole-site or complete-process evaluation.
