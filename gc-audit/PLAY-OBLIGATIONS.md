# GC-AUDIT PLAY Obligations

Status: active
Authority: DEV-ACCORD.05 and DEV-ACCORD.06

This document defines which GC-AUDIT events must or should follow each PLAY.
"Must" means non-conformance if skipped. "Should" means expected unless explicitly justified.

## Before the PLAY starts

| Event | Obligation |
| --- | --- |
| `gc-audit preflight` | Must run before any PLAY is declared. Agent posts a valid `PREFLIGHT: complete` or `PREFLIGHT: blocked` stamp. |

## After the PLAY closes (by execution level)

| Execution level | Required GC-AUDIT events | Recommended GC-AUDIT events |
| --- | --- | --- |
| BUNT | DEV-DOCS check (explicit update or `not-needed` with reason) | None |
| RUN | DEV-DOCS check | `gc-audit validate` |
| DRIVE | DEV-DOCS update (required, not optional); `gc-audit validate` | `gc-audit registry` if registry files changed |
| PASS | DEV-DOCS update; `gc-audit validate`; evidence bundle | `gc-audit release` if release-facing; `gc-audit registry` if PASS or registry changed |

## Trigger-specific obligations

| Trigger condition | Required GC-AUDIT event |
| --- | --- |
| PLAY touches registry files (PASS, projects.yaml, GC-AUDIT-REGISTRY.yaml) | `gc-audit registry` |
| PLAY involves normalization | Re-run `gc-audit validate` after to confirm clean state |
| PLAY is cross-project or cross-repo | `gc-audit zerotrust` recommended; human authorization required in PLAY record |
| PLAY involves a git split (branch, PR chain, worktree, fork) | `gc-audit validate` on both sides; human authorization required per DEV-ACCORD.10 |
| PLAY level is ambiguous or escalated | User authorizes before PLAY is declared; authorization recorded in PLAY.jsonl |

## PLAY record close requirements

Every PLAY record in `PLAY.jsonl` must carry at close:

| Field | Required when |
| --- | --- |
| `preflight` | Always - `complete`, `blocked`, or `not-yet-enforced` for pre-policy plays |
| `dev_docs_check.status` | Always - `updated`, `not-needed`, or `deferred` |
| `dev_docs_check.note` | Required when `not-needed` or `deferred` |
| `commit_ref` | Required when the PLAY produced a commit |
| `timing.read.started_at`, `timing.read.ended_at`, `timing.read.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.plan.started_at`, `timing.plan.ended_at`, `timing.plan.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.execute.started_at`, `timing.execute.ended_at`, `timing.execute.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.verify.started_at`, `timing.verify.ended_at`, `timing.verify.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.close.started_at`, `timing.close.ended_at`, `timing.close.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
