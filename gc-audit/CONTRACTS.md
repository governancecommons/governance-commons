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
final response after every PLAY. DEV-ACCORD.06 declares this as universal GC
behavior for every GC-conformant agent, environment, platform, adapter, and
runtime.

`summary.next_recommended_step` must be classified as `Compound PASS`,
`Single PASS`, `DRIVE`, `RUN`, `BUNT`, or `Blocked` (DEV-ACCORD-CI-37, added by
the DEV-ACCORD.06 amendment declaring DEV-ACCORD.11). When a human request
implies multiple coherent lanes of work, callers should expect agents to
propose a compound PASS and present a compound PASS brief before any file edit
— see `gc-audit/PLAY-OBLIGATIONS.md` for the summary and DEV-ACCORD.06 for the
authoritative rule.

## PLAY Records

PLAY records live in repo-root `PLAY.jsonl`.

Schema: `schemas/gc-play-record.schema.json`

Each closed PLAY created after the validation_profile amendment (DEV-ACCORD.06,
2026-07-02) must declare a `validation_profile` whose `profile` matches the PLAY
`level`; records predating that amendment without `validation_profile` are
legacy-tolerated (a warning, not a validation failure). Minimum required checks
are declared in `security.playValidationProfiles` in the GC-AUDIT registry:

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

## Trusted evidence authentication v1

The versioned host-authority, evidence-envelope, and verification-result schemas
are in `schemas/evidence/`. `tools/trusted_evidence.py` verifies Ed25519 signatures
using host-configured public roots and reuses the ZTA canonical JSON encoding.
The host supplies the expected target, revision, environment, catalog, objective,
controls, scopes, time, and a durable replay ledger outside the target repository.
Neither the target nor the signed package may select the host's trust roots.

`AUTHENTICATED` means that the package matched the configured root and delegated
producer, scope, freshness, and replay checks. The result expressly reports
`CONFIGURED_ROOT_ONLY` and leaves the ZTA control `UNVERIFIED`: the verifier
cannot establish the provenance of the host process or its root configuration.
The evaluator retains authority over control decisions. The synthetic example
and reproducibility command are documented in
`specifications/GC-AUDIT-EVIDENCE-001.md`.

## Local host adapter v1

`schemas/evidence/gc-audit.local-host-config.v1.schema.json` defines the
host-owned public roots, policy/catalog pins, exact target context and
revocations. `gc-audit.local-host-receipt.v1.schema.json` defines the
digest-checked result and provenance. The adapter accepts only an
envelopes-only package from the collector. Deployment supplies the host
directory and an independent configuration digest pin; the package cannot
replace either. The adapter checks local filesystem permissions and a
persistent SQLite ledger before invoking the original verifier. See
`specifications/GC-AUDIT-EVIDENCE-002.md` for the role and deployment limits.
