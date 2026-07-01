# DEV-ACCORD.05 — DEV-DOCS Suite and GC-AUDIT Declaration

**PASS ID:** DEV-ACCORD.05
**Canonical ID:** GC:2013
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-30T00:00:00Z
**Depends on:** GC:2008 (DEV-ACCORD.00), GC:2011 (DEV-ACCORD.03)

---

## Summary

This PASS does two things:

1. Names the suite of canonical planning doc types defined in DEV-ACCORD.00 as **DEV-DOCS**.
2. Declares **GC-AUDIT** as the portfolio-wide validation, normalization, and audit toolchain — distinct from DEV-DOCS (what gets checked) and from Marlin (which installs, not audits).

It also declares REVIEW-GRAMMAR as a GC standard component, promotes the DEV-DOCS maintenance gate rule, and specifies the GC-AUDIT invocation interface so Marlin and other tools can delegate to it without owning it.

---

## Vocabulary Table

Four terms. No overlap.

| Term | Owns |
| --- | --- |
| DEV-DOCS | Per-project dev-control documents: DEV-PATH, DEV-PLAN, DEV-TRACKS, DEV-RELEASE |
| DEV-ACCORD | The GC standard and rulebook that governs DEV-DOCS |
| GC-AUDIT | Portfolio-wide validation, normalization, stale-reference detection, adversarial review, trace, and close-the-loop toolchain |
| Marlin | Install/adoption wizard; may invoke GC-AUDIT post-install but does not own audit logic |

These terms are mutually exclusive in ownership. No term absorbs another's responsibility.

---

## DEV-DOCS Suite Declaration

**DEV-DOCS** is the collective name for the four canonical planning doc types declared in DEV-ACCORD.00:

| Doc | Owns |
| --- | --- |
| DEV-PATH | Phase history, design decisions, PASS registry. Append-only. |
| DEV-PLAN | Current execution state, active milestones, priority work queue |
| DEV-TRACKS | Parallel workstreams and inter-track dependencies |
| DEV-RELEASE | Release train state, version targets, distribution channels |

DEV-DOCS are the documents every active project uses to stay oriented.
DEV-ACCORD is the standard that governs their structure, naming, and ownership rules.
A project's DEV-DOCS may cite DEV-ACCORD, but DEV-ACCORD lives in `governance-commons/` and is not a DEV-DOCS member.

DOCS.md (doc authority map) is a companion file, not a DEV-DOCS member. It maps which doc type owns which content area and may appear alongside DEV-DOCS in a project but is not governed by the DEV-DOCS maintenance gate below.

---

## GC-AUDIT Declaration

**GC-AUDIT** is the portfolio-wide toolchain for:

- Validating DEV-DOCS and planning doc conformance
- Normalizing stale, drifted, or inconsistent doc content
- Detecting and removing stale references
- Running adversarial, meta, authority, and registry audits
- Assessing release readiness
- Tracing work from origin to evidence

GC-AUDIT is runnable against any portfolio project: GC, DCP, DXP, eco, niji, Cockpit, or any future project.

### REVIEW-GRAMMAR as canonical verb registry

`docs/REVIEW-GRAMMAR.md` is declared the canonical verb registry for GC-AUDIT operations under this PASS. Its command verbs — normalize, validate, verify, adversarial audit, meta-audit, trace, authority audit, registry audit, close the loop, de-stale — are the standard GC-AUDIT operation names. REVIEW-GRAMMAR.md is promoted from a portfolio working grammar to a GC standard component.

GC-AUDIT implementations must use REVIEW-GRAMMAR verb names. REVIEW-GRAMMAR.md must not duplicate verb definitions; extensions require an amendment to this PASS.

### Existing validators declared as GC-AUDIT implementations

The machine-readable GC-AUDIT registry lives at:

```text
governance-commons/gc-audit/GC-AUDIT-REGISTRY.yaml
```

Cockpit, Marlin, DCP, and agent tooling must use that registry to discover
available audit/status/repair/planning operations. A command surface may present
friendly menus, but it must not invent unregistered operations or execute scripts
outside the allowlisted registry.

Authoritative implementations live under `governance-commons/gc-audit/tools/`.
Portfolio-root `.ps1` files are compatibility adapters only and must delegate to
the authoritative GC-AUDIT tools.

The following scripts are hereby declared GC-AUDIT implementations:

| Script | GC-AUDIT operation |
| --- | --- |
| `governance-commons/gc-audit/tools/validate-planning.ps1` | validate DEV-DOCS conformance (DEV-ACCORD.00 rules) |
| `governance-commons/gc-audit/tools/validate-bootstrap.ps1` | validate agent bootstrap conformance (DEV-ACCORD.04 rules) |
| `governance-commons/gc-audit/tools/validate-pointers.ps1` | registry audit — projects.yaml pointer truth |
| `governance-commons/gc-audit/tools/validate-review-grammar.ps1` | validate REVIEW-GRAMMAR adoption |
| `governance-commons/gc-audit/tools/validate-debt.ps1` | validate open debt markers (TODO/FIXME/TBD) |
| `governance-commons/gc-audit/tools/validate-recent-work.ps1` | adversarial audit, release readiness, and de-stale detection |
| `governance-commons/gc-audit/tools/dev-report.ps1` | meta-audit planning report |

These scripts are GC-AUDIT. They are not Marlin features.

### GC-AUDIT invocation interface

The standard invocation surface for GC-AUDIT is:

```text
dcp audit validate   [-Project <name>]
dcp audit normalize  [-Project <name>]
dcp audit de-stale   [-Project <name>]
dcp audit release    [-Project <name>]
```

Or via Marlin delegation (Marlin calls GC-AUDIT, does not reimplement it):

```text
marlin audit validate
marlin audit de-stale
```

A GC-AUDIT invocation that reimplements validator logic instead of calling the declared GC-AUDIT scripts is a violation of this standard.
An invocation that executes a script not listed in the GC-AUDIT registry is also non-conformant.

---

## DEV-DOCS Maintenance Gate

Any commit or push that includes a meaningful change to code, releases, packaging, dependencies, architecture, or milestones MUST either:

1. Update the relevant DEV-DOCS, or
2. Record an explicit exemption using the commit trailer:

```text
Dev-Docs: not-needed
Reason: <one line — why no doc update is required>
```

Meaningful changes include: formula additions, schema changes, new exports, release version bumps, dependency changes, architecture decisions, milestone completions, new modules. They do not include: typo fixes, comment changes, test-only changes that do not alter behavior.

### Commit trailer

Commits with DEV-DOCS updates carry:

```text
Dev-Docs: updated
```

Commits exempted carry:

```text
Dev-Docs: not-needed
Reason: <reason>
```

Commits that modify meaningful files and carry neither trailer are non-conformant. This is a warning at pre-commit and an error at pre-push.

### Enforcement layers

| Layer | Trigger | What it checks |
| --- | --- | --- |
| Pre-commit hook | Every commit | Trailer present if meaningful files changed |
| Pre-push hook | Every push | GC-AUDIT validate + pointer check; de-stale warning if stale refs detected |
| Agent rule | End of any session with code changes | Agent declares `Dev-Docs: updated` or `Dev-Docs: not-needed` with reason |
| CI | PR / push to main | Full GC-AUDIT validate run |

The pre-commit hook must not block commits on files it cannot classify as meaningful. When uncertain, it warns — it does not block.

---

## Stale Reference Rule

Stale references are one of the primary drift sources across this portfolio. De-stale is not an occasional cleanup — it is a regular GC-AUDIT operation.

De-stale runs:

- As part of any `dcp audit normalize` pass
- As part of pre-push GC-AUDIT validation (warning level)
- As part of release readiness checks (error level if stale refs in DEV-DOCS)

De-stale detects:

- Retired or renamed doc file references
- Old launch commands, install paths, or entrypoints
- Old version claims in docs after a version bump
- Old "not started" or "planned" markers after commits prove completion
- Stale roadmap or milestone language
- References to archived projects as if active

---

## Marlin and GC-AUDIT Relationship

Marlin is an install wizard. Its responsibilities: install, configure, bootstrap, smoke-test, emit evidence. It does not own audit logic.

Marlin MAY invoke GC-AUDIT post-install as evidence collection:

```text
marlin install niji
  → creates venv
  → pip install -e .
  → runs smoke tests
  → calls: dcp audit validate -Project niji   (GC-AUDIT, not Marlin logic)
  → emits evidence bundle
```

The `marlin audit <verb>` surface is a thin delegation layer only. All logic executes inside GC-AUDIT scripts. Marlin must not duplicate validator implementations.
Marlin audit runners must fail closed when a verb is registered without an active allowlisted implementation.

---

## Cluster Invariants

**DEV-ACCORD-CI-9 — DEV-DOCS is the canonical suite name**
The four planning doc types (DEV-PATH, DEV-PLAN, DEV-TRACKS, DEV-RELEASE) are collectively called DEV-DOCS. This name is portfolio-wide and agent-readable. Any doc referring to "the planning docs" or "development docs" without using DEV-DOCS is using informal language.

**DEV-ACCORD-CI-10 — GC-AUDIT owns validation; Marlin owns install**
Validation, normalization, de-stale, adversarial audit, and release readiness are GC-AUDIT operations. Marlin delegates to GC-AUDIT. No Marlin command may reimplement GC-AUDIT logic.

**DEV-ACCORD-CI-11 — DEV-DOCS maintenance gate is mandatory**
Any commit with meaningful changes must carry `Dev-Docs: updated` or `Dev-Docs: not-needed` with reason. This is enforced at pre-commit (warning) and pre-push (error). The gate cannot be waived by a project-level instruction file.

**DEV-ACCORD-CI-12 — REVIEW-GRAMMAR.md is the GC-AUDIT verb registry**
All GC-AUDIT operation names derive from REVIEW-GRAMMAR.md. No GC-AUDIT implementation may introduce operation names that conflict with or bypass the registered verbs.

---

## Outputs

- DEV-DOCS declared as the suite name for DEV-PATH, DEV-PLAN, DEV-TRACKS, DEV-RELEASE
- GC-AUDIT declared as the portfolio-wide validation and audit toolchain
- Four-term vocabulary table established: DEV-DOCS / DEV-ACCORD / GC-AUDIT / Marlin
- REVIEW-GRAMMAR.md promoted to GC standard component; declared canonical verb registry for GC-AUDIT
- Existing validators (validate-planning, validate-bootstrap, validate-pointers, validate-debt) declared as GC-AUDIT implementations
- GC-AUDIT registry path declared: `governance-commons/gc-audit/GC-AUDIT-REGISTRY.yaml`
- GC-AUDIT invocation interface specified: `dcp audit <verb>`
- DEV-DOCS maintenance gate declared with commit trailer format and enforcement layers
- Stale reference rule declared with de-stale triggers and detection scope
- Marlin delegation pattern specified: invoke GC-AUDIT, do not reimplement it
- 4 new cluster invariants: DEV-ACCORD-CI-9 through DEV-ACCORD-CI-12

---

## Constraints Introduced

- DEV-DOCS is now the required term for the planning doc suite. Informal references must migrate over time.
- GC-AUDIT is the required term for the validation/audit toolchain. No other tool or agent may claim ownership of audit logic.
- Marlin may not reimplement GC-AUDIT operations.
- Marlin and Cockpit must discover GC-AUDIT menu/actions from the GC-AUDIT registry and fail closed for unimplemented verbs.
- Commits with meaningful changes require the `Dev-Docs:` trailer — enforced at pre-push.
- REVIEW-GRAMMAR verb names are the standard for all GC-AUDIT implementations.

---

## Amendment — 2026-06-30

The commit trailer spec introduced in the DEV-DOCS Maintenance Gate section of this PASS
(`Dev-Docs: updated | not-needed` + `Reason:`) has been superseded by DEV-ACCORD.06
(GC:2014), which declares the unified commit trailer schema for the portfolio. DEV-ACCORD.06
governs all trailer fields. This PASS remains authoritative for the DEV-DOCS suite
declaration, GC-AUDIT declaration, maintenance gate rule, and stale reference rule.

---

## Reversibility

Reversing this PASS requires a future DEV-ACCORD PASS that supersedes DEV-ACCORD.05, renames or dissolves the suite terms, and provides migration guidance for all adopters. Until such a PASS exists, the four-term vocabulary and maintenance gate are binding.
