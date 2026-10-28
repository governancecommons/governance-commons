# GC-AUDIT-PRODUCT-001 Gate 1: portal-kit repository assessment

Status: repository-only pilot; no operational security assurance or release authorization.

## Scope and verified facts

The explicitly selected target was `C:\dev\portal-kit`, identifier `portal-kit`, at Git revision `a61f1ee5ab58f92cebe93e4da0e2d9ae4905afcb` on branch `pk-03-contracts`. Its working tree was clean before and after the assessment. The selected profile was `zta.library.v1`. The bundled draft catalog contains 24 controls. The CLI resolved the Git root, read `HEAD`, checked worktree cleanliness, and inventoried 40 tracked Git blobs with `git ls-tree -r HEAD`. These are verified repository facts. They do not establish any ZTA control.

The existing ZTA evaluator returned **24 UNVERIFIED**, **0 PASS**, **0 FAIL**, and `release_eligibility: BLOCKED`. No independently authenticated behavioral, deployment, host-authority, or negative-observation proof was supplied. In particular, repository descriptions and source files are not treated as trusted producer evidence. Each control's reason and required control objective appear in the JSON report's `result.control_results` and `catalog.controls`. The appropriate next action is to obtain independently authenticated, revision-bound control proof before seeking a control PASS.

## Provenance and integrity

- Machine report: `portal-kit-gate1.json`, schema `gc-audit.repository-report.v1`.
- Catalog source: `gc-audit/catalogs/gc-audit.zta-controls.v1.draft.json`.
- Catalog digest: `sha256:d76f4de7a0221d58b3a79e5541840b44767c68d79971615b2bf920cd0a63756e`.
- Manifest digest: `sha256:9109598a8e9c33d640c0d8fe75193a9fb8c40f73ec5a800093376904049543ab`.
- Report digest: `sha256:f5f3b1442bcc3bf2143d7340904721c4f4a94b96353788a5c356bc79c46ae352`.
- Methods: local Git metadata and tracked-blob inventory; deterministic `zta_evaluator.evaluate` with no control evidence or caller-supplied trust roots.

Reproduce from the Governance Commons repository root with the documented dependencies installed:

```text
python gc-audit/tools/zta_cli.py assess --target C:\dev\portal-kit --target-id portal-kit --profile zta.library.v1 --authorize-local-read --output <outside-target>/portal-kit-gate1.json
python gc-audit/tools/zta_cli.py verify --report <outside-target>/portal-kit-gate1.json --target C:\dev\portal-kit
```

For a portable reopen, omit `--target` from `verify`. Supplying the local target also compares its current exact revision and blob manifest. Assessment does not invoke Cockpit, an AI provider, target code, or network commands. Python dependency installation is a separate setup step and may use the network. The report digest provides integrity checking against a known digest, not authentication. Tracked source inventory omits untracked, ignored, external, and submodule content; production configuration and live behavior were not observed. A repository scan cannot certify complete Zero Trust assurance.

## GC-P01–GC-P14 acceptance at this Gate 1 review

| ID | Status | Evidence or remaining gate |
| --- | --- | --- |
| GC-P01 | BLOCKED | Documented native command works locally; independent clean-environment new-user install was not demonstrated. |
| GC-P02 | PASS | Explicit local target selection and exact revision; no portal-kit edits. |
| GC-P03 | PASS | Read-only Git operations; target status clean before and after; no implicit network call in CLI. |
| GC-P04 | PASS | Existing evaluator positive, negative, adversarial and precedence suite plus CLI regression checks pass locally. |
| GC-P05 | NOT TESTED | No independent pilot user comprehension test. |
| GC-P06 | PASS | Control reasons, catalog objectives and a bounded next action in the exported report. |
| GC-P07 | PASS | Export reopened; report, manifest, catalog and evaluator result checked, with optional exact-target comparison. |
| GC-P08 | PASS | CLI accepts no caller trust roots or roles; forged PASS with recomputed outer digest is rejected. |
| GC-P09 | PASS | Local run needs neither Cockpit nor an AI service; install dependencies before offline operation. |
| GC-P10 | DEFERRED | Optional AI integration belongs to a later gate. |
| GC-P11 | NOT TESTED | Hosted Windows/Linux/macOS results pending PR CI. |
| GC-P12 | PASS | Actual external portal-kit revision assessed and exported; no control assurance claimed. |
| GC-P13 | DEFERRED | UI and accessibility work belong to a later gate. |
| GC-P14 | DEFERRED | Consequential actions and agent approval flows are outside this read-only CLI. |

## OBDD classification

**BLOCKER:** independent host-owned authority and control-specific runtime proof for any trusted ZTA PASS or operational assurance claim. **REQUIRED:** exact-head hosted compatibility CI and owner review of this Gate 1 PR. **DEFERRED:** GUI, AI adviser, Cockpit adapter, scanner integration, deployment, release, and broader assurance work. This report records a product pilot, not closure of the parent charter or approval of a release.
