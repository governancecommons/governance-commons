# GC-AUDIT-TARGET-003 — Portal application ZTA behavioral pilot

Status: local synthetic application test. No production, deployment, or operational security assurance.

## Target and method

The requested path `C:\dev\governance-commons-portal` did not exist. The portfolio registry identifies the clean checkout at `C:\dev\governance-commons\governance-commons-portal`, Git revision `f6a5759ced4ee73f9b15f1dc02d98493ddf255c8` (`main`). Its remote `main` matched that revision. The pinned local Observatory Core checkout was `cd6f7dc79346dd129a2ea69828d0c1f8c72ac62e` and was used only for the separate Portal regression suite.

The fixed GC-AUDIT probe started the Portal's actual Node HTTP server bound to `127.0.0.1` with a disposable `LOCALAPPDATA`, synthetic OAuth configuration values, and synthetic membership/session rows. It made no OAuth callback or external release request. The editorial checks used `EditorialStore` and in-memory SQLite. The probe deleted its disposable directory on exit. No production Portal SQLite database, key, or GitHub credential was read or modified. The Portal and Core Git trees remained clean.

## Observed behavior

| Local assertion | Observed result | Relevant ZTA objectives, not control verdicts |
| --- | --- | --- |
| Anonymous dashboard and import requests | HTTP 401, HTTP 401 | ZTA-01.02, 02.01, 06.01 |
| Synthetic owner dashboard request | HTTP 200 | ZTA-01.02, 02.01 |
| Disabled member and revoked session | HTTP 401, HTTP 401 | ZTA-01.02, 02.01, 02.02, 10.01 |
| Import without CSRF and with wrong origin | HTTP 403, HTTP 403 | ZTA-05.01, 06.01 |
| Authenticated reviewer import with valid CSRF | HTTP 403 | ZTA-02.01, 10.01 |
| Author attempts to review own draft | Denied by `EditorialStore` | ZTA-02.01, 10.01 |
| Reviewer attempts to approve same revision | Denied by `EditorialStore` | ZTA-02.01, 10.01 |
| Distinct owner approves reviewed revision | Approved by `EditorialStore` | ZTA-02.01 |

These 11 assertions verify only the listed local behaviors. The ZTA catalog's control objectives demand broader coverage and independently authenticated host evidence. The deterministic evaluator therefore reports **24 UNVERIFIED, 0 PASS, 0 FAIL**, with release eligibility **BLOCKED**. No HTTP status or store result was promoted into a control PASS or trusted negative observation.

## Evidence and reproducibility

- [Machine-readable report](portal-application-zta-pilot.json): `gc-audit.repository-report.v1` with `gc-audit.application-pilot.v1` local observations, exact target revision, Git blob inventory, catalog/profile, evaluator result, source references, limitations and digests.
- Report digest: `sha256:5407e1f09a368a5d31043422c7b343d88e20b14e27b128bfd2be96f1a648313c`.
- Catalog digest: `sha256:d76f4de7a0221d58b3a79e5541840b44767c68d79971615b2bf920cd0a63756e`.
- Target manifest digest: `sha256:25ecaf2b02cd9acd53f19c649eeed2dd66af450accbc624c79cb9993383ddd9e`.
- The JSON names the exact Portal source blob IDs and hashes the fixed probe source and observation set. `verify` reopens the export, recomputes report, manifest, catalog and evaluator digests, checks the local probe source, and optionally checks the exact target revision and tracked Git tree. Digests are integrity metadata, not signatures or authenticated producer authority.

With Node.js 22+ and the Python dependencies in `gc-audit/README.md`, run from the Governance Commons checkout:

```text
python gc-audit/tools/portal_behavioral_assessment.py assess --target C:\dev\governance-commons\governance-commons-portal --authorize-local-test --output <outside-Portal>/portal-application-zta-pilot.json
python gc-audit/tools/portal_behavioral_assessment.py verify --report <outside-Portal>/portal-application-zta-pilot.json --target C:\dev\governance-commons\governance-commons-portal
```

The Portal regression suite passed **264/265 tests, 1 skip, 0 failures** after setting `OBSERVATORY_CORE_CHECKOUT` to the exact pinned local checkout and `LOCALAPPDATA` to a disposable directory. A first unconfigured run failed five Core-dependent tests because the required checkout variable was absent; no code changed to suppress them. The GC ZTA suite passed **181 tests** locally. Hosted CI for this PR is reported separately after exact-head execution.

## Limits and OBDD disposition

Production GitHub OAuth, production identity and membership lifecycle, deployment configuration, network and provider boundaries, complete control applicability, live audit provenance, and independent host authority were not tested. The fixed probe checks selected request and store paths only. The evaluator uses the existing `zta.library.v1` pilot profile; no service-profile policy or control PASS route was invented. Publication HTTP routes remain disabled.

**BLOCKER:** host-owned authority, control-specific proof and deployment observations before any ZTA control PASS or operational assurance. **REQUIRED:** owner review of this bounded PR and exact-head hosted CI. **DEFERRED:** new profile policy, production OAuth/deployment testing, public publication, GUI, AI and Cockpit integration. No release, merge or activation is implied.
