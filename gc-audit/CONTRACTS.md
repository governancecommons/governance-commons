# GC-AUDIT Contracts

Status: active
Authority: DEV-ACCORD.05 and DEV-ACCORD.06

GC-AUDIT contracts are the machine-readable boundary for Cockpit, Marlin, DCP,
and agents. Callers discover active contracts through
`gc-audit/GC-AUDIT-REGISTRY.yaml`.

## Structured Results

Validation tools that support machine output emit `gc-audit.result.v1`.

Schema: `schemas/gc-audit-result.schema.json`

Current active implementation:

| Tool | JSON support |
| --- | --- |
| `gc-audit.playbook` / `validate-playbook.ps1` | `-Json` |

Other validators may continue to emit human output until they explicitly declare
`supportsJson: true` in the registry.

For PLAY closeout, `summary.latest_play`, `summary.next_recommended_step`, and
`telemetry[]` are required output fields. Agents must surface those values in the
final response after every PLAY.

## PLAY Records

PLAY records live in repo-root `PLAY.jsonl`.

Schema: `schemas/gc-play-record.schema.json`

Each closed PLAY must declare a `validation_profile` whose `profile` matches the
PLAY `level`. Minimum required checks are declared in
`security.playValidationProfiles` in the GC-AUDIT registry:

| Level | Required checks |
| --- | --- |
| BUNT | `dev-docs-check` |
| RUN | `dev-docs-check`, `gc-audit.playbook` |
| DRIVE | `dev-docs-update`, `gc-audit.validate`, `gc-audit.zerotrust` |
| PASS | `dev-docs-update`, `gc-audit.validate`, `gc-audit.release`, `evidence-bundle` |

## Normalization Reports

Normalizers must support explicit apply only. Preview is the default.

Schema: `schemas/gc-audit-normalize-report.schema.json`

Every normalizer preview/apply report must include:

| Field | Meaning |
| --- | --- |
| `mode` | `preview` or `apply` |
| `changes[]` | Proposed or applied file changes |
| `changes[].status` | `would-change`, `changed`, `skipped`, `unfixable`, or `already-ok` |
| `before` / `after` | Machine-readable pointer or content summary when available |

## Evidence Principals

Evidence bundle signing is disabled unless `security.evidenceBundles.enabled`
is `true`.

Principal schema: `schemas/gc-evidence-principal.schema.json`
Bundle schema: `schemas/gc-compliance-evidence.schema.json`

When enabled, the configured `principalStore` must be a contained relative path
and contain at least one principal JSON record. Private keys must remain outside
the repository in an OS keystore, HSM, secure enclave, or external KMS.
