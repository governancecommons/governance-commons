# DEV-ACCORD.06 — Change Playbook

**PASS ID:** DEV-ACCORD.06
**Canonical ID:** GC:2014
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-30T00:00:00Z
**Depends on:** GC:2010 (DEV-ACCORD.02), GC:2013 (DEV-ACCORD.05)
**Supersedes:** Commit trailer spec introduced in DEV-ACCORD.05 (GC:2013) — DEV-ACCORD.06 now owns the full trailer schema.
**Amended:** 2026-07-01 — declares DEV-PLAYBOOK and the PLAY.jsonl lifecycle/schema; adds universal PLAY closeout output rule (see Amendment sections below)

---

## Summary

The Change Playbook defines four execution levels — BUNT, RUN, DRIVE, PASS — that define
the significance and required governance of any unit of work in the portfolio. Each level
determines required DEV-DOCS updates, validation, evidence, and commit trailer fields.

These are execution levels, not planning structure. DEV-ACCORD.02 owns Phase, Wave,
Track, PASS, Sub-PASS, RUN, Evidence Bundle, Work Item, Gate, and Release as the
planning/execution vocabulary. This playbook owns BUNT, RUN, DRIVE, and PASS as
the execution-level vocabulary. Commit trailers record the execution level; they
do not define it.

This PASS also declares the unified commit trailer schema, absorbing the `Dev-Docs:`
field introduced in DEV-ACCORD.05. All trailer fields are owned here. Future fields
require a DEV-ACCORD amendment, not a new independent PASS.

---

## The Four Change Playbook Execution Levels

| Execution level | What it is | Typical examples |
| --- | --- | --- |
| BUNT | Tiny tactical change — no behavioral effect | Typo, comment, formatting, whitespace |
| RUN | Normal bounded work — local, contained impact | Bug fix, small feature, local doc correction |
| DRIVE | Meaningful milestone movement — visible or release-affecting | Version bump, new scheme, packaging, dependency change, public API surface, DEV-DOCS state change |
| PASS | Governed contract — planned, multi-step, or cross-cutting | Multi-agent work, standard changes, cross-project changes, release-defining decisions |

BUNT, RUN, and DRIVE are execution levels for the work being performed. PASS is
the highest Change Playbook execution level and also refers to the governance
contract that wraps one or more execution events. Commit trailers record the
execution level for audit; the level itself is not limited to commits. This extends DEV-ACCORD.02 without replacing
Phase, Wave, Track, or any other planning unit.

---

## Per-Class Obligations

### BUNT

- **DEV-DOCS:** Not required unless the change alters project truth (see Escalation Rules).
- **Validation:** None required. Existing tests should still pass.
- **Evidence:** Commit only.
- **Trailer minimum:** `Change-Level: BUNT` + `Dev-Docs: not-needed` + `Reason:`

### RUN

- **DEV-DOCS:** Required if the change alters project state, feature completeness, or
  any fact a future agent would need to read from DEV-DOCS to understand the project.
  Not required for purely internal refactors with no behavioral or state change.
- **Validation:** Tests must pass. GC-AUDIT not required but permitted.
- **Evidence:** Commit only for most RUNs. Evidence bundle optional for significant RUNs.
- **Trailer minimum:** `Change-Level: RUN` + `Dev-Docs: updated` or `Dev-Docs: not-needed` + `Reason:`

### DRIVE

- **DEV-DOCS:** Required. The relevant DEV-DOCS section must be updated before or in the
  same commit. Which section depends on the change:
  - Version / release state → DEV-RELEASE + DEV-PLAN
  - Architecture decision → DEV-PATH
  - Workstream or dependency change → DEV-TRACKS
  - Active milestone completion → DEV-PLAN
- **Validation:** GC-AUDIT validate must run. De-stale check recommended.
- **Evidence:** Validation output recorded in commit trailer. Evidence bundle for DRIVE
  changes that close a milestone or alter a release gate.
- **Trailer minimum:** `Change-Level: DRIVE` + `Dev-Docs: updated` + `Validation:`

### PASS

- **DEV-DOCS:** Required. The PASS record itself is the primary artifact; DEV-DOCS must
  reflect the PASS outcome.
- **Validation:** Full GC-AUDIT suite. De-stale required before closing.
- **Evidence:** Evidence bundle required for significant PASSes.
- **Trailer minimum:** `Change-Level: PASS` + `Dev-Docs: updated` + `Validation:` + `Pass-ID:`

---

## Escalation Rules

A change MUST escalate to the higher class if any of the following is true:

| Trigger | Minimum class |
| --- | --- |
| Touches version number, release gate, or ship status | DRIVE |
| Touches public API surface, schema, or export format | DRIVE |
| Touches install path, entrypoint, or packaging | DRIVE |
| Closes or opens a milestone | DRIVE |
| Adds or removes a declared dependency | DRIVE |
| Requires coordination between more than one agent | PASS |
| Changes a GC standard, governance rule, or authority document | PASS |
| Affects more than one project in the portfolio | PASS at minimum |

**Escalation is not optional.** Work recorded as BUNT that touches release truth
has the wrong execution level. The pre-push hook treats a BUNT or RUN trailer on
a DRIVE-trigger file as a warning; agents must not suppress it.

**Highest execution level wins.** When a single commit contains work at multiple
levels, the commit records the highest execution level present. A commit with a
typo fix and a version bump is a DRIVE, not a BUNT.

---

## Unified Commit Trailer Schema

All commits in this portfolio use the following trailer schema. Fields are written at
the end of the commit message body, separated from the body by a blank line.

```
Change-Level: BUNT | RUN | DRIVE | PASS
Dev-Docs: updated | not-needed
Reason: <required when Dev-Docs is not-needed — one line>
Validation: <what ran — omit for BUNT; required for DRIVE and PASS>
Pass-ID: <PASS ID — required when Change-Level is PASS>
```

**Field rules:**

- `Change-Level` is required on every commit.
- `Dev-Docs` is required on every commit.
- `Reason` is required when `Dev-Docs: not-needed`. Omitting it is equivalent to
  not writing the trailer at all.
- `Validation` is required for DRIVE and PASS. For RUN it is optional but encouraged.
  For BUNT it is omitted.
- `Pass-ID` is required when `Change-Level: PASS`. Omitted otherwise.

**Minimal trailers by class:**

BUNT — no behavioral change, no doc update needed:
```
Change-Level: BUNT
Dev-Docs: not-needed
Reason: comment-only fix
```

RUN — behavioral fix, no state change in DEV-DOCS:
```
Change-Level: RUN
Dev-Docs: not-needed
Reason: internal refactor, no feature or state change
```

RUN — with DEV-DOCS update:
```
Change-Level: RUN
Dev-Docs: updated
```

DRIVE — version bump and DEV-DOCS updated:
```
Change-Level: DRIVE
Dev-Docs: updated
Validation: pytest, validate-planning
```

PASS — governance change:
```
Change-Level: PASS
Dev-Docs: updated
Validation: pytest, validate-planning, validate-pointers, validate-bootstrap
Pass-ID: DEV-ACCORD.06
```

---

## Enforcement

| Layer | What it checks |
| --- | --- |
| Pre-commit hook | `Change-Level` and `Dev-Docs` fields present; `Reason` present when `not-needed`; warns if DRIVE-trigger files changed but class is BUNT or RUN |
| Pre-push hook | Validates DRIVE/PASS trailers include `Validation`; runs GC-AUDIT validate; warns on stale refs |
| Agent rule | Agent determines execution level before committing; declares level in trailer; does not suppress escalation warnings |
| CI | Full trailer schema validation on PR/push to main |

The pre-commit hook must not block on uncertainty. When it cannot determine
whether a file triggers DRIVE obligations, it warns and defers to the agent.

### Git topology boundary

This playbook governs change level, DEV-DOCS obligations, validation, evidence,
and commit trailers. It does not authorize agents to create branches, PR chains,
worktrees, forks, or alternate publish paths.

DEV-ACCORD.10 governs git split authorization. A DRIVE or PASS-level change may
justify recommending a split, but it does not permit performing one without
explicit human approval.

---

## Cluster Invariants

**DEV-ACCORD-CI-13 — Four execution levels, no gaps**
Every change is a BUNT, RUN, DRIVE, or PASS. No change may lack an execution
level. Omitting `Change-Level` from a commit trailer is a non-conformant commit.

**DEV-ACCORD-CI-14 — Highest execution level wins**
When a commit contains work at multiple levels, the commit records the highest execution level.
No commit may be downgraded by splitting off the DRIVE-trigger change into a separate
commit solely to avoid the DRIVE obligations.

**DEV-ACCORD-CI-15 — Escalation is not optional**
A BUNT or RUN on a DRIVE-trigger file is the wrong execution level. Agents must escalate.
Suppressions require explicit human instruction recorded in the session.

**DEV-ACCORD-CI-16 — Trailer schema is owned here**
The commit trailer schema is defined in this PASS and extended only by a future
DEV-ACCORD amendment. No other PASS, project instruction file, or agent may introduce
trailer fields that conflict with or bypass this schema.

---

## Outputs

- Change Playbook declared: BUNT, RUN, DRIVE, PASS as the four portfolio execution levels
- Per-class obligations defined: DEV-DOCS, validation, evidence
- Escalation rules declared with explicit trigger table
- Highest-class-wins rule declared
- Unified commit trailer schema declared — absorbs `Dev-Docs:` field from DEV-ACCORD.05
- Trailer field rules and minimal examples per class provided
- Enforcement layers specified: pre-commit, pre-push, agent rule, CI
- 4 new cluster invariants: DEV-ACCORD-CI-13 through DEV-ACCORD-CI-16

---

## Amendment to DEV-ACCORD.05

DEV-ACCORD.05 (GC:2013) introduced the `Dev-Docs:` commit trailer field in isolation.
That field is now part of the unified trailer schema declared here. DEV-ACCORD.05
remains authoritative for the DEV-DOCS suite declaration, GC-AUDIT declaration, and
maintenance gate rule. The trailer spec section of DEV-ACCORD.05 is superseded by
this PASS. When the two conflict on trailer format, DEV-ACCORD.06 governs.

---

## Amendment — 2026-07-01 — DEV-PLAYBOOK and PLAY.jsonl Lifecycle

### 1. DEV-PLAYBOOK term declared

**DEV-PLAYBOOK** is hereby declared the canonical term for the combined system this
PASS owns: the four Change Playbook execution levels (BUNT, RUN, DRIVE, PASS) plus
the PLAY declaration and lifecycle model defined below. DEV-PLAYBOOK does not replace
or rename this PASS; it names what this PASS governs so agents and adopters have one
word for "the execution-level and PLAY-tracking system," distinct from DEV-DOCS
(the planning doc suite) and GC-AUDIT (the validation toolchain).

### 2. PLAY definition and lifecycle

A **PLAY** is an agent-declared unit of work mapped to exactly one Change Playbook
execution level. Every PLAY is recorded as one line in an append-only `PLAY.jsonl`
file at the portfolio or repository root — never rewritten, only appended.

A PLAY has exactly one of three lifecycle states, held in its `status` field:

| Status | Meaning |
| --- | --- |
| `open` | Declared and in progress. Timing categories may still be incomplete. |
| `blocked` | Halted pending human authorization or an unresolved dependency. |
| `closed` | Complete. DEV-DOCS check recorded. `commit_ref` present if a commit was produced. |

Agents propose and declare the PLAY before work starts. Users authorize ambiguous,
escalated, cross-project, or PASS-level PLAYs. Every PLAY closes with a DEV-DOCS
check — either an update or an explicit `not-needed`/`deferred` note explaining why.

### 3. PLAY.jsonl record schema

Every PLAY.jsonl line is one JSON object. Required and conditional fields:

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `play_id` | string | Always | Unique across all records in the file. |
| `repo` | string | Always | Repo the PLAY primarily targets. |
| `level` | enum: `BUNT`\|`RUN`\|`DRIVE`\|`PASS` | Always | The Change Playbook execution level declared for this PLAY. |
| `status` | enum: `open`\|`blocked`\|`closed` | Always for records created after this amendment | Records predating this amendment without `status` are legacy-tolerated. |
| `declared_at` | ISO 8601 timestamp | Always | When the PLAY was declared. |
| `time_loc` | string (time.loc format) | Required when time.loc is initialized in the repo | Omitted when time.loc is not initialized. |
| `declared_by` | string | Optional | Agent or human identity that declared the PLAY. |
| `authorized_by` | enum: `agent`\|`human` | Always | Who authorized this PLAY. |
| `authorization_note` | string | Required when `authorized_by` is `human` | Empty or absent when `authorized_by` is `agent`. |
| `scope` | string | Always | One-line description of the work. |
| `touches` | array of strings | Required when the PLAY is cross-repo or cross-project | Lists every repo touched. |
| `timing.read` / `timing.plan` / `timing.execute` / `timing.verify` / `timing.close` | object: `{started_at, ended_at, duration_ms}` | Always | All five timing categories present; `null` timestamps and zero duration are valid for pre-telemetry PLAYs. |
| `dev_docs_check.status` | enum: `updated`\|`not-needed`\|`deferred` | Always | Mirrors the DEV-DOCS obligations declared per execution level above. |
| `dev_docs_check.note` | string | Required when `dev_docs_check.status` is `not-needed` or `deferred` | Explains why no update was made. |
| `commit_ref` | string | Required when the PLAY produced a commit | Omitted for read-only or investigation-only PLAYs. |
| `preflight` | enum: `complete`\|`blocked`\|`not-yet-enforced` | Always | `not-yet-enforced` is valid only for PLAYs that predate AGENT-PREFLIGHT.md enforcement. |

The GC-AUDIT implementation of this schema is
`governance-commons/gc-audit/tools/validate-playbook.ps1`, registered as
`gc-audit.playbook` in `GC-AUDIT-REGISTRY.yaml`. Per-level GC-AUDIT event
obligations that follow a PLAY are declared in
`governance-commons/gc-audit/PLAY-OBLIGATIONS.md`, not duplicated here.

### 4. Cluster invariant additions

**DEV-ACCORD-CI-30 — PLAY.jsonl is the canonical PLAY record store**
`PLAY.jsonl` is append-only at the portfolio or repository root. The PLAY.jsonl
schema fields declared in this amendment are owned by this PASS. No other document
may redefine them without a DEV-ACCORD amendment.

**DEV-ACCORD-CI-31 — Every PLAY declares a status**
Every PLAY record created after this amendment must declare `status` as `open`,
`blocked`, or `closed`. A record missing `status` is legacy-tolerated only when it
predates this amendment.

**DEV-ACCORD-CI-32 — DEV-PLAYBOOK subsumes execution levels and PLAY lifecycle**
DEV-PLAYBOOK is the umbrella term for the four execution levels declared earlier in
this PASS and the PLAY declaration/lifecycle model declared in this amendment. No
other PASS or project instruction file may introduce a competing PLAY schema.

### Outputs of this amendment

- DEV-PLAYBOOK declared as the umbrella term for execution levels + PLAY lifecycle
- PLAY lifecycle states declared: `open`, `blocked`, `closed`
- Full PLAY.jsonl record schema declared with required/conditional field rules
- GC-AUDIT implementation and obligations doc cross-referenced, not duplicated
- 3 new cluster invariants: DEV-ACCORD-CI-30 through DEV-ACCORD-CI-32

---

## Amendment — 2026-07-01 — Universal PLAY Closeout Output

### 1. Universal scope

Every GC-conformant agent, runtime, adapter, host, environment, and platform MUST
produce the universal PLAY closeout output after every PLAY. This rule is not
specific to Codex, Claude, Copilot, Cockpit, Marlin, DCP, Windows, PowerShell, or
any other local implementation.

If an environment cannot run `validate-playbook.ps1`, it MUST produce an equivalent
closeout from the PLAY record using the same required sections and fields. Human
readable text, JSON, UI panels, and API responses are all acceptable surfaces only
if they carry the same required content.

### 2. Required closeout sections

Every PLAY final response or closeout artifact MUST include, in this order:

| Section | Required content |
| --- | --- |
| PLAY telemetry | The five timing buckets: `read`, `plan`, `execute`, `verify`, `close`, plus total duration. |
| Latest PLAY summary | `play_id`, repo, level, status, scope, DEV-DOCS result, commit reference when produced, and validation checks. |
| Next recommended step | One concrete next logical step, or the next required authorization/blocker if work cannot continue. |

These sections are required even when the PLAY is a BUNT, read-only SCREEN/READ
style investigation, blocked PLAY, or no-code documentation PLAY. If exact timing
is unavailable, the agent records zero or null timing according to the PLAY schema
and still displays the table.

### 3. Tooling contract

`gc-audit.playbook` is the reference implementation for this rule. Its human
output and `gc-audit.result.v1` JSON output carry the required closeout sections.
Other tools may render the sections differently, but they may not omit them or
rename them in a way that prevents callers from finding them.

### 4. Cluster invariant additions

**DEV-ACCORD-CI-33 — PLAY closeout output is universal**
Every GC-conformant agent, environment, platform, adapter, and runtime must output
the PLAY telemetry table, latest PLAY summary, and next recommended step after
every PLAY.

**DEV-ACCORD-CI-34 — Closeout output is platform-neutral**
The required PLAY closeout content may be emitted as text, JSON, UI, or API data,
but it must contain the same required fields. A platform limitation is not a valid
reason to omit the closeout.

**DEV-ACCORD-CI-35 — Next-step recommendation is mandatory**
Every PLAY closeout must include one concrete next recommended logical step or a
specific blocker/authorization requirement. Ending a PLAY with validation status
alone is non-conformant.

### Outputs of this amendment

- Universal PLAY closeout output rule declared for all GC-conformant agents and runtimes
- Required closeout sections declared: telemetry, latest PLAY summary, next recommended step
- Platform-neutral rendering rule declared for text, JSON, UI, and API surfaces
- 3 new cluster invariants: DEV-ACCORD-CI-33 through DEV-ACCORD-CI-35

---

## Amendment — 2026-07-01 — Compound-PASS-Default and Next-Step Classification (DEV-ACCORD.11)

### 1. Batch-language default: propose a compound PASS

When a human request implies more than one coherent unit of work in one go, the
agent's default proposal is a **compound PASS** (`CLUSTER.NN.10`, `.20`, … per the
DEV-ACCORD.02 numbering), not a chain of separate single PASSes. The compound PASS
names the parallel batch at the PASS level; its sub-PASSes (`.01`–`.09`) are the
lanes. This amendment does not redefine compound/sub-PASS numbering — that is owned
by DEV-ACCORD.02 (GC:2010) — it declares *when to reach for it by default*.

The following request phrasings are **compound-PASS triggers** unless the human
contradicts them or the work genuinely reduces to a single lane:

| Trigger phrasing (or equivalent intent) | Default proposal |
| --- | --- |
| "as much as possible", "do the most you can" | Compound PASS |
| "batch it", "group these", "all together" | Compound PASS |
| "all N", "all of them", "the whole list" | Compound PASS |
| "parallelize this", "run these in parallel" | Compound PASS |
| "go for all", "next pass do everything" | Compound PASS |
| Work that spans more than one repo or project | Compound PASS (escalation table: PASS minimum) |
| A single, narrow, one-lane change | Single PASS / DRIVE / RUN / BUNT as the level fits |

Defaulting to a compound PASS does **not** lower any obligation. Each sub-PASS
still carries its own Done-when, DEV-DOCS check, validation, and commit trailer.
The compound wrapper plans and validates the lanes as one coherent contract — it
does not skip per-lane governance or collapse validation.

### 2. Compound PASS brief — required pre-execution artifact

Before executing a compound PASS, the agent declares a **compound PASS brief**
with these fields, in order:

```text
Goal:              one sentence — what the compound PASS accomplishes
Proposed PASS ID:  CLUSTER.NN (primary .00) with sub-PASS lanes .01-.09
Sub-PASS lanes:    table — lane ID | scope
Repos touched:     list
Files:             list, grouped by repo when cross-repo
Validation gates:  what runs, mapped to the highest execution level present
Commit plan:       branch/current-branch per DEV-ACCORD.10, trailer fields
Blockers:          open judgment calls or missing authorization, named explicitly
```

This brief is the shared surface the human authorizes against. It replaces
ad-hoc "I'll do a few things" planning for multi-lane work. A compound PASS
must not begin execution — including file edits — before the human confirms
the brief. Presenting the brief is not authorization; explicit confirmation is.

### 3. Next recommended step must be classified

The mandatory "Next recommended step" closeout section (DEV-ACCORD-CI-35) must
classify the recommendation as exactly one of:

- `Next Recommended Step: Compound PASS — <name>` — several lanes can move together.
- `Next Recommended Step: Single PASS — <name>` — the next thing is one governed slice.
- `Next Recommended Step: DRIVE | RUN | BUNT — <name>` — the next thing is a single
  execution-level change below PASS.
- `Next Recommended Step: Blocked — <authorization or dependency required>` — work
  cannot continue until a human resolves it.

A bare next-step sentence with no PASS/level label is non-conformant. When the
current PLAY was itself opened from batch-language, the closeout should scope the
largest coherent compound PASS that can be validated, committed, and pushed
cleanly in the next pass.

### 4. Release/evidence-review threshold

A release/evidence review (`gc-audit release` + zero-trust evidence posture +
playbook validation together) is required only when one of the following is true:

- A compound PASS is closing.
- The change touches a release gate, version number, or ship status (the DRIVE
  escalation trigger for release truth).
- The human explicitly requests it.

Outside those three conditions, the per-level GC-AUDIT obligations in
`gc-audit/PLAY-OBLIGATIONS.md` already apply and are sufficient — running a full
release/evidence review after every small RUN or BUNT is not required and should
not be treated as the default closeout ritual.

### 5. Cluster invariant additions

**DEV-ACCORD-CI-36 — Batch-language defaults to a compound PASS**
When a human request implies multiple coherent lanes of work — including the
trigger phrasings tabled above and any cross-repo work — the agent's default
proposal is a compound PASS, unless the human contradicts it or the work reduces
to a single lane. Proposing a chain of separate single PASSes for clearly
batchable work is non-conformant planning.

**DEV-ACCORD-CI-37 — Next recommended step is classified**
Every PLAY closeout's next recommended step must be labeled as a Compound PASS, a
Single PASS, a sub-PASS execution level (DRIVE / RUN / BUNT), or a specific
blocker. An unclassified next step is non-conformant.

**DEV-ACCORD-CI-38 — Compound PASS brief precedes execution**
A compound PASS must not begin execution, including file edits, before the human
confirms the compound PASS brief declared in this amendment. Presenting the brief
is not itself authorization.

### Outputs of this amendment

- Compound PASS declared as the default proposal for batch-language and cross-repo requests
- Compound-PASS trigger table declared
- Compound PASS brief format declared as the required pre-execution, human-confirmed artifact
- Next-recommended-step classification declared, refining DEV-ACCORD-CI-35
- Release/evidence-review threshold declared: compound-PASS close, release-gate change, or explicit request only
- 3 new cluster invariants: DEV-ACCORD-CI-36 through DEV-ACCORD-CI-38

---

## Amendment — 2026-07-02 — validation_profile Schema Field and Legacy Tolerance

### 1. Gap this amendment closes

A prior DRIVE (governance-commons `gc-play-2026-07-01-005`, GC-AUDIT caller-contract
closure) added a hard-required `validation_profile` field to
`schemas/gc-play-record.schema.json` and to the PLAY.jsonl validation logic in
`validate-playbook.ps1`, without adding it to the PLAY.jsonl record schema table in
this PASS (section 3 of the 2026-07-01 DEV-PLAYBOOK amendment above) and without any
legacy-tolerance carve-out. This put `validate-playbook.ps1` in direct conflict with
DEV-ACCORD-CI-30 and DEV-ACCORD-CI-32 — a validator enforced an undeclared schema
field as a hard failure, and every PLAY record predating the field's introduction
(including the portfolio-root `PLAY.jsonl` bootstrap record) failed validation with
exit code 1 instead of being legacy-tolerated the way `status` was. This amendment
declares the field retroactively and applies the same legacy-tolerance treatment
already established for `status`.

### 2. `validation_profile` added to the PLAY.jsonl record schema

| Field | Type | Required | Rule |
| --- | --- | --- | --- |
| `validation_profile.profile` | enum: `BUNT`\|`RUN`\|`DRIVE`\|`PASS` | Always for records created after this amendment | Must match the record's `level`. Records predating this amendment without `validation_profile` are legacy-tolerated. |
| `validation_profile.checks` | array of strings | Always when `validation_profile` is present | Must include the minimum checks for the PLAY level declared in `security.playValidationProfiles` in `GC-AUDIT-REGISTRY.yaml`. |

This is a clarifying addition to the schema table declared in section 3 of the
2026-07-01 DEV-PLAYBOOK amendment, not a replacement of it. `validation_profile` was
already summarized in `gc-audit/PLAY-OBLIGATIONS.md` and `gc-audit/CONTRACTS.md`;
this amendment is the DEV-ACCORD-owning declaration those documents pointed to but
that did not yet exist.

### 3. Legacy tolerance

A PLAY record missing `validation_profile` is legacy-tolerated exactly like a record
missing `status`: `validate-playbook.ps1` reports it as a warning, not an error, and
does not fail the run. `-Strict` mode treats this warning as a failure, consistent
with how `-Strict` already treats a missing `status`. When `validation_profile` is
present, its internal shape (`profile` matching `level`, non-empty `checks`, and the
per-level minimum checks) is still enforced as a hard error — legacy tolerance covers
absence only, not malformed presence.

### 4. Cluster invariant additions

**DEV-ACCORD-CI-39 — `validation_profile` is a declared PLAY.jsonl schema field**
`validation_profile.profile` and `validation_profile.checks` are PLAY.jsonl schema
fields owned by DEV-ACCORD.06, declared by this amendment. A validator enforcing a
PLAY.jsonl field as a hard error without a corresponding DEV-ACCORD.06 declaration is
non-conformant with DEV-ACCORD-CI-30 and DEV-ACCORD-CI-32.

**DEV-ACCORD-CI-40 — New required PLAY.jsonl fields default to legacy-tolerated**
When a future DEV-ACCORD.06 amendment adds a new required PLAY.jsonl field, the
default treatment for records predating that amendment is a legacy-tolerated
warning, not a hard failure, unless the amendment explicitly states otherwise. This
prevents the `validation_profile` gap — an undocumented hard-required field breaking
every pre-existing PLAY record — from recurring with future schema additions.

### Outputs of this amendment

- `validation_profile.profile` and `validation_profile.checks` formally added to the PLAY.jsonl record schema table, closing the CI-30/CI-32 conflict
- Legacy tolerance for missing `validation_profile` declared, matching the existing `status` treatment
- `validate-playbook.ps1` updated: missing `validation_profile` is now a warning, not a hard error; malformed `validation_profile` remains a hard error
- 2 new cluster invariants: DEV-ACCORD-CI-39 and DEV-ACCORD-CI-40 (the latter is a standing rule for all future PLAY.jsonl schema amendments)
