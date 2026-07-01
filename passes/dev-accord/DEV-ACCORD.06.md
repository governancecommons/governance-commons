# DEV-ACCORD.06 — Change Playbook

**PASS ID:** DEV-ACCORD.06
**Canonical ID:** GC:2014
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-30T00:00:00Z
**Depends on:** GC:2010 (DEV-ACCORD.02), GC:2013 (DEV-ACCORD.05)
**Supersedes:** Commit trailer spec introduced in DEV-ACCORD.05 (GC:2013) — DEV-ACCORD.06 now owns the full trailer schema.

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
