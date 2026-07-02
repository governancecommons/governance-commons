# GC-AUDIT PLAY Obligations

Status: active
Authority: DEV-ACCORD.05 and DEV-ACCORD.06

This document defines which GC-AUDIT events must or should follow each PLAY.
"Must" means non-conformance if skipped. "Should" means expected unless explicitly justified.

The PLAY.jsonl record schema itself — field names, types, and conditional rules —
is owned by the DEV-ACCORD.06 amendment (DEV-PLAYBOOK). This document only covers
which GC-AUDIT events accompany a PLAY; it does not redefine schema fields.
The GC-AUDIT implementation that checks the schema is
`governance-commons/gc-audit/tools/validate-playbook.ps1`, registered as
`gc-audit.playbook`. `validate-recent-work.ps1` Level 1 also runs this check
when a target repo has `PLAY.jsonl`; repos that have not initialized PLAY
tracking are reported as skipped instead of being treated as schema failures.
The record schema is `schemas/gc-play-record.schema.json`; structured validator
output uses `schemas/gc-audit-result.schema.json`.

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

Evidence bundle signing is controlled by `security.evidenceBundles` in
`gc-audit/GC-AUDIT-REGISTRY.yaml`. Repos that have not enabled bundle signing
must declare `enabled: false` with a reason. Repos that enable bundle signing
must declare a contained relative `principalStore` with at least one principal
JSON record; private keys must remain outside the repository.

## Trigger-specific obligations

| Trigger condition | Required GC-AUDIT event |
| --- | --- |
| PLAY touches registry files (PASS, projects.yaml, GC-AUDIT-REGISTRY.yaml) | `gc-audit registry` |
| PLAY involves normalization | Re-run `gc-audit validate` after to confirm clean state |
| PLAY is cross-project or cross-repo | `gc-audit zerotrust` recommended; human authorization required in PLAY record |
| PLAY involves a git split (branch, PR chain, worktree, fork) | `gc-audit validate` on both sides; human authorization required per DEV-ACCORD.10 |
| PLAY level is ambiguous or escalated | User authorizes before PLAY is declared; authorization recorded in PLAY.jsonl |
| Any PLAY closes | Run `gc-audit playbook` (`validate-playbook.ps1`) to confirm PLAY.jsonl still conforms to the DEV-PLAYBOOK schema |
| Any commit citing a PASS ID (heading citation or `Pass-ID:` trailer) | `gc-audit pass-citations` (`validate-pass-citations.ps1`) runs automatically via `.pre-commit-config.yaml` at both the `pre-commit` stage (staged diff) and `commit-msg` stage (trailer block) — no manual invocation needed for normal commits |
| Human request implies multiple coherent lanes ("as much as possible", "batch it", "all N", "parallelize", cross-repo work) | Agent proposes a compound PASS and declares a compound PASS brief before execution — see DEV-ACCORD.06 amendment (DEV-ACCORD.11) |
| A compound PASS is closing, a release gate/version changes, or the human explicitly requests it | Run the release/evidence review (`gc-audit release` + zero-trust evidence posture + playbook validation together). Outside these three conditions, per-level obligations above are sufficient — do not run a full release/evidence review after every small RUN or BUNT. |
| A validator/profile fails twice with the same failure class, or the fix would require validator/tooling/topology/policy changes outside the authorized PLAY | Stop, report a validation blocker, and request human authorization for a separate GC-AUDIT/DEV-ACCORD or topology/policy PLAY. Agents must not invent, edit, register, or run new validation scripts as part of product/app closeout. |
| Repo ambiguity is caused by an incorrect Git remote URL | Fix the incorrect remote first with `git remote set-url` after reporting current path, current remote, intended remote, and any duplicate child repo remote. Do not move, delete, detach, reinitialize, or replace `.git` unless the human explicitly authorizes that exact `.git` operation. |

## Validation loop stop / tooling authorization

DEV-ACCORD.06 owns the universal rule: validation failures are evidence, not
automatic authorization to expand scope. Agents may run existing registered
validators, repo test commands, and ordinary inspection commands inside an
authorized PLAY. Agents must not create new validation scripts, edit GC-AUDIT
tooling, register new validators, or introduce new validation profiles unless a
separate human-authorized GC-AUDIT or DEV-ACCORD PLAY names that tooling change.

When validation crosses into repo topology, branch-protection policy, registry
authority, GC-AUDIT internals, or suspected validator defects, the agent must
stop after one narrow remediation attempt and close or mark the PLAY blocked
with the exact command, failure class, last safe commit/state, and proposed next
authorized PLAY.

## Git remote identity correction

DEV-ACCORD.06 also owns the remote-first rule. Nested repos are allowed when the
portfolio design permits them; a parent repo containing child repos is not itself
a defect. If repo ambiguity is caused by the wrong `origin` URL, the conformant
first fix is to update only the incorrect remote URL. Agents must not move,
delete, rename, detach, reinitialize, replace, or regenerate `.git` directories
unless the human explicitly authorizes that exact `.git` operation.

## Compound PASS brief

Required before a compound PASS begins execution, including any file edit. The
human must confirm the brief; presenting it is not authorization. Fields, in
order: `Goal`, `Proposed PASS ID` (primary `.00` + sub-PASS lanes `.01`-`.09`),
`Sub-PASS lanes` (table), `Repos touched`, `Files`, `Validation gates`,
`Commit plan`, `Blockers`. Full field definitions and the compound-PASS trigger
table are declared in the DEV-ACCORD.06 amendment (DEV-ACCORD.11) — this section
is a summary, not the authority.

## Next recommended step classification

Every PLAY closeout's `Next Recommended Step` must be labeled as one of:
`Compound PASS`, `Single PASS`, `DRIVE`, `RUN`, `BUNT`, or `Blocked`. An
unclassified next step is non-conformant (DEV-ACCORD-CI-37).

## PLAY record close requirements

Every PLAY record in `PLAY.jsonl` must carry at close. Field names, types, and
conditional rules are declared in the DEV-ACCORD.06 amendment; this table is a
summary, not the authority.

| Field | Required when |
| --- | --- |
| `status` | Always for records created after the DEV-ACCORD.06 amendment — `open`, `blocked`, or `closed`. Missing status is legacy-tolerated only for pre-amendment records. |
| `preflight` | Always - `complete`, `blocked`, or `not-yet-enforced` for pre-policy plays |
| `dev_docs_check.status` | Always - `updated`, `not-needed`, or `deferred` |
| `dev_docs_check.note` | Required when `not-needed` or `deferred` |
| `touches` | Required when the PLAY is cross-repo or cross-project |
| `commit_ref` | Required when the PLAY produced a commit |
| `timing.read.started_at`, `timing.read.ended_at`, `timing.read.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.plan.started_at`, `timing.plan.ended_at`, `timing.plan.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.execute.started_at`, `timing.execute.ended_at`, `timing.execute.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.verify.started_at`, `timing.verify.ended_at`, `timing.verify.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `timing.close.started_at`, `timing.close.ended_at`, `timing.close.duration_ms` | Always; null timestamps and zero duration are valid for pre-telemetry plays |
| `validation_profile.profile` | Always for records created after the validation_profile amendment (DEV-ACCORD.06, 2026-07-02) — must match PLAY `level`. Missing `validation_profile` is legacy-tolerated only for records predating that amendment. |
| `validation_profile.checks` | Required when `validation_profile` is present — must include the minimum checks for the PLAY level declared in `GC-AUDIT-REGISTRY.yaml` |

`validate-playbook.ps1` displays the five timing buckets for each checked PLAY so
agents can report read, plan, execute, verify, and close telemetry at the end of
the PLAY. `validate-recent-work.ps1` Level 1 surfaces that playbook output when
`PLAY.jsonl` exists, while keeping other successful validator output compact.
Every PLAY closeout must include the playbook validator's telemetry table, the
latest PLAY summary, and the next recommended step. DEV-ACCORD.06 makes this a
universal GC rule for all GC-conformant agents, environments, platforms, adapters,
and runtimes. It is mandatory for agent final responses after a PLAY, not optional
narration.
