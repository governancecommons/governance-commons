PASS DEV-ACCORD.00 — Planning Document Standard (Cluster Header)

[NP-METADATA]
- PASS ID: DEV-ACCORD.00
- Canonical ID: GC:2008
- Name: Planning Document Standard — Cluster Header
- Domain: governance.docs.planning
- Role: CREATE
- Actor: Jess Ervin (GC founder) + Claude (claude-sonnet-4-6)
- Date: 2026-06-27
- time.loc: 2026-06-27T00:00:00Z
- Authority: AL:2 — GC maintainer decision
- Status: ACCEPTED
- Registry: passes/passes.registry.json — GC:2008 entry required (output of this PASS)

---

[PROBLEM]

Planning documents (DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS) are used across every
project in the portfolio. They are not governed by any canonical standard. The result:

Issue 1 — H1 format drift
H1 headers are inconsistent across the portfolio. Examples found before this PASS:
  `# LASSO Development Path`                     (project name first, no doc type prefix)
  `# Governance Commons SDK - Development Path`  (hyphen separator, reversed order)
  `# DEV-PATH - eco.vs`                          (hyphen instead of em dash)
  `# DEV-PATH — eco Development Path`            (correct format — em dash, type-first)
There is no declared rule. Any format containing the project name is "close enough" by
convention, which means every agent must infer the format rather than conform to one.

Issue 2 — H1 collisions
Two files shared the exact same H1:
  c:\dev\DEV-PATH.md
  c:\dev\dxp-org\devx-control-plane\DEV-PATH.md
Both were titled `# DEV-PATH — DevX Control Plane (DCP)`. An agent reading both in one
session had no reliable signal to distinguish them. Discovered and patched manually.

Issue 3 — No validation tooling
There is no validator. Drift is discovered session by session through manual inspection.
The same class of problem has been patched multiple times without a mechanism to prevent it.

Issue 4 — No ONS registration
DEV-PATH, DEV-PLAN, DEV-RELEASE, and DEV-TRACKS are not registered in ONS as named doc
types. Their naming rules are undeclared.

Issue 5 — Inconsistent doc type names
`TRACKS.md` does not follow the `DEV-` prefix convention that DEV-PATH, DEV-PLAN, and
DEV-RELEASE establish. The canonical name is DEV-TRACKS.

Issue 6 — No canonical doc rule
What each doc type owns is understood by convention, not specification. Agents reading
DEV-PATH for current execution state are making errors that no validator can catch because
no authoritative source declares the boundary.

The problem is systemic. Manual patching is the wrong fix. A governing standard is required.

---

[CLUSTER DECLARATION]

DEV-ACCORD is the Planning Document Standard cluster for Governance Commons.

DEV-ACCORD governs:
- The canonical set of planning doc types and their names (all follow the DEV- prefix)
- The H1 naming format and disambiguation rule
- The em dash separator requirement (U+2014, not hyphen)
- The canonical doc rule (what each type exclusively owns)
- The append-only constraint for DEV-PATH
- The validation contract (what validate-planning.ps1 enforces)

DEV-ACCORD does not govern:
- The content of individual projects' planning docs
- PASS identifier format (CANON governs this)
- Identifier naming grammar (ONS governs this)
- Event emission from planning doc updates (GEE profile — future work, DEV-ACCORD.01)
- ONS registration of the doc type names (separate ONS PASS — required next step)

---

[DOC TYPE REGISTRY]

The following doc types are canonical. All follow the `DEV-` prefix convention.
Any project that uses these doc types MUST conform to this standard.
Additional doc types require a DEV-ACCORD amendment.

| Doc Type | Filename | Owns | Required? |
| --- | --- | --- | --- |
| DEV-PATH | DEV-PATH.md | Phase history, design decisions, PASS registry. Append-only. | Required for active/wip |
| DEV-PLAN | DEV-PLAN.md | Current execution state, active milestones, priority work queue | Required for active/wip |
| DEV-RELEASE | DEV-RELEASE.md | Release train, version targets, distribution status | Optional |
| DEV-TRACKS | DEV-TRACKS.md | Parallel workstreams and inter-track dependencies | Optional |

DEV-PATH and DEV-PLAN are required for any project registered in projects.yaml with
status `active` or `wip`. Projects with status `scaffold`, `stable`, or `archive` are
exempt from the required-pair rule but must still conform if the files exist.

Migration note: existing `TRACKS.md` files are legacy. They MUST be renamed `DEV-TRACKS.md`
before the project can claim full DEV-ACCORD conformance. Until renamed, validate-planning.ps1
will report a warning for `TRACKS.md` files found alongside conformant DEV-* files.

---

[H1 NAMING RULE]

Every planning doc MUST open with an H1 of the form:

  # {DOC-TYPE} — {Project-Scope}

Rules:

R1. `{DOC-TYPE}` MUST be exactly one of: DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS.
R2. The separator MUST be the em dash character `—` (U+2014).
    A hyphen `-` (U+002D) is a violation. An en dash `–` (U+2013) is a violation.
R3. `{Project-Scope}` MUST be a non-empty string.
R4. `{Project-Scope}` MUST be unique within the portfolio for its doc type.
    Two DEV-PATH files with the same H1 is an error.
R5. The H1 MUST be the first non-empty line in the file.
    No frontmatter, no blank lines, no other content before it.
R6. When a naming collision would occur, the more specific entity qualifies its scope
    with a parenthetical:
      `# DEV-PATH — DevX Control Plane (DCP)`
      `# DEV-PATH — Portfolio Control Plane (c:\dev root)`

---

[AUTHORITY LEVEL RULE]

Every planning doc SHOULD contain an authority level declaration within the first 15 lines:

  **AUTHORITY LEVEL: AL:{N}**

Where N is 1, 2, or 3 per the portfolio authority model. Omission is a warning, not an
error. Projects without an AL declaration are in conformance debt.

---

[STATUS RULE]

Every planning doc SHOULD contain a status declaration within the first 15 lines:

  **Status:** {value}

Omission is a warning, not an error.

---

[CANONICAL DOC RULE]

Each doc type is the exclusive owner of its declared content scope.

DEV-PATH owns:
- Phase history and phase completion status
- Design decisions and rationale records
- PASS registry entries for the project
This file is the authoritative historical record. Do not read it for current execution state.

DEV-PLAN owns:
- Current execution state
- Active milestone and release targets
- Priority work queue and queued ideas
This file is the authoritative planning authority. Do not read DEV-PATH for current state.

DEV-RELEASE owns:
- Release train state
- Version targets and distribution channels
- Per-version milestone status and blockers

DEV-TRACKS owns:
- Parallel workstream definitions and ownership
- Inter-track dependency declarations
- Track status and sequencing

---

[APPEND-ONLY RULE FOR DEV-PATH]

DEV-PATH files are append-only historical records.

Permitted operations:
- Reading
- Appending a new phase section at the bottom
- Appending a new PASS registry entry
- Modifying the H1 to bring it into DEV-ACCORD conformance (under explicit human instruction)

Forbidden operations:
- Rewriting existing phase content
- Changing recorded design decisions
- Deleting or collapsing entries
- Summarizing existing history

The H1 carve-out exists because the naming rule was not declared before DEV-ACCORD.00.
Bringing an existing file's H1 into conformance corrects a gap, not a historical record.

---

[VALIDATION CONTRACT]

The portfolio validator (`validate-planning.ps1`) enforces this standard.
Running the validator is equivalent to running a DEV-ACCORD conformance check.

ERRORS (exit code 1):
1. H1 is not the first non-empty line
2. H1 doc type is not one of the four registered types
3. H1 separator is not em dash (U+2014)
4. H1 project scope is empty
5. Two or more docs of the same type share the same H1 (collision)

WARNINGS (exit code 0 unless -Strict):
6. AUTHORITY LEVEL not declared within first 15 lines
7. Status not declared within first 15 lines
8. File named TRACKS.md exists (should be DEV-TRACKS.md)

---

[CLUSTER INVARIANTS]

DEV-ACCORD-CI-1 — Em dash is the required separator
The H1 separator MUST be `—` (U+2014). A hyphen or en dash is a violation.
This invariant is machine-checkable. The validator MUST enforce it.

DEV-ACCORD-CI-2 — Doc type is the H1 prefix
The H1 MUST begin with the doc type token. The form `# Project — DEV-PATH` is a violation
regardless of separator correctness. Type-first ordering is non-negotiable.

DEV-ACCORD-CI-3 — No H1 collisions within a doc type
Two files of the same type with the same H1 is a portfolio-level error. The validator
MUST detect and report this as an error, not a warning.

DEV-ACCORD-CI-4 — DEV-PATH is append-only
No automated tool or agent may rewrite existing DEV-PATH content without explicit human
instruction recorded in the session. This invariant cannot be overridden by a project-level
CLAUDE.md, AGENTS.md, or local instruction file.

DEV-ACCORD-CI-5 — All planning doc types use the DEV- prefix
The canonical names are DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS. A file named
TRACKS.md, ROADMAP.md, or any other non-DEV-prefixed name is not a canonical planning
doc under this standard, even if it serves the same purpose.

---

[REASONING — 5 QUESTIONS]

1. Why is this a GC standard rather than a local portfolio convention?
Planning doc structure is the most repeated pattern across all portfolio projects.
If it remains a convention, it continues to drift — as evidenced by repeated manual
patching before this PASS. A GC standard means it is citable by ID in project CLAUDE.md
files, enforceable by a validator with a declared specification, and portable to any
project adopting GC governance.

2. Why is em dash the required separator?
Hyphens appear inside project names (`eco-edge`, `dxp-org`, `devx-control-plane`).
Using a hyphen as the separator in `# DEV-PATH - eco-edge` produces two hyphens with
different syntactic roles — ambiguous and visually noisy. Em dash (U+2014) is not used
in any registered project name, is visually prominent, and is machine-checkable as a
single Unicode codepoint. En dash was also considered and rejected: em dash is the
conventional English editorial separator for title-level distinctions.

3. Why is the doc type the H1 prefix?
When an agent reads multiple DEV-PATH files in one session, the first token in the H1
is the classification signal the agent processes first.
  `# DEV-PATH — Lasso`           → immediately: this is a path doc, it belongs to Lasso.
  `# Lasso Development Path`     → requires reading the full phrase, doc type is buried.
Type-first ordering matches how agents and humans parse structured labels.

4. Why DEV-TRACKS instead of TRACKS?
Every other canonical planning doc type uses the `DEV-` prefix. TRACKS without the prefix
is inconsistent and breaks the naming pattern. An agent scanning for `DEV-*.md` files would
miss `TRACKS.md`. Consistency in prefix is the single biggest aid to automated tooling
and reduces one more class of "why didn't it find it" errors.

5. What prevents DEV-ACCORD from drifting?
DEV-ACCORD-CI-1 and DEV-ACCORD-CI-2 are expressed as a single machine-checkable regex.
The validator is part of the standard's specification — not a separate artifact.
Running `validate-planning.ps1` is the same as running DEV-ACCORD conformance. Any agent
or session that bypasses the validator without recording a reason is violating DEV-ACCORD.

---

[OUTPUTS]
- DEV-ACCORD.00 accepted as the DEV-ACCORD cluster header and governing standard
- Doc type registry declared: DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS (all DEV-prefixed)
- H1 naming rule declared (R1–R6) with em dash invariant
- Canonical doc rule declared (exclusive ownership per type)
- Append-only rule for DEV-PATH declared with permitted operations
- Validation contract declared (5 errors, 3 warnings)
- 5 cluster invariants declared (DEV-ACCORD-CI-1 through DEV-ACCORD-CI-5)
- GC:2008 registry entry created in passes/passes.registry.json
- GC-PASS-0010.00 entry appended to passchangelog.md
- validate-planning.ps1 created at c:\dev root per validation contract

[DELTA SUMMARY]
- Declared DEV-ACCORD cluster: Planning Document Standard for Governance Commons
- Identified 6 systemic gaps: H1 format drift, H1 collision, no validator, no ONS
  registration, inconsistent TRACKS naming, no canonical doc rule
- Declared canonical doc types: DEV-PATH (append-only history), DEV-PLAN (execution state),
  DEV-RELEASE (release train), DEV-TRACKS (workstreams) — all follow DEV- prefix convention
- Declared H1 naming rule: `# {DOC-TYPE} — {Project-Scope}` with type-first ordering,
  em dash separator, unique scope requirement, H1-as-first-line requirement
- Declared disambiguation rule: parenthetical qualifier resolves name collisions
- Declared AL and status as warning-level requirements (conformance debt, not hard errors)
- Declared canonical doc rule: exclusive content ownership per type
- Declared append-only rule for DEV-PATH with H1 conformance carve-out
- Declared validation contract: 5 errors, 3 warnings
- Declared 5 cluster invariants (DEV-ACCORD-CI-1 through DEV-ACCORD-CI-5)

[CONSTRAINT VALIDATION]
- AL:2 authority confirmed: GC maintainer decision; recorded in passchangelog
- Does not govern individual project content: explicitly excluded
- Does not redefine ONS naming grammar: explicitly excluded; ONS registration is future work
- Does not define GEE profile for planning events: explicitly excluded as DEV-ACCORD.01
- Append-only H1 carve-out is scoped and bounded: existing historical content unchanged
- DEV-TRACKS naming change is declared as migration, not immediate forced rename

[REVERSIBILITY]
Reversing DEV-ACCORD.00 requires a GC-level governance PASS that explicitly supersedes
this PASS, documents why the planning doc standard is withdrawn or replaced, and addresses
whether conformant docs retain their H1 format or require migration.
Until such a PASS exists, DEV-ACCORD.00 is the governing standard.

[HANDOFF]
next_action: ONS namespace registration for DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS
  as named planning doc types (separate ONS PASS)
next_after_that: DEV-ACCORD.01 — GEE event profile for planning doc events
  Requires design decision on system_namespace (proposed: portfolio.planning)
  GEE event types: phase_complete | milestone_hit | pass_entry | doc_created | doc_updated
next_tooling: integrate validate-planning.ps1 into CI/pre-commit hook at portfolio level
future: rename all TRACKS.md files to DEV-TRACKS.md across the portfolio (separate task)
