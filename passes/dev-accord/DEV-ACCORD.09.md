# DEV-ACCORD.09 — Script and Tooling Placement Rule

**PASS ID:** DEV-ACCORD.09
**Canonical ID:** GC:2017
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-07-01T00:00:00Z
**Depends on:** GC:2011 (DEV-ACCORD.03), GC:2014 (DEV-ACCORD.06)
**Amends:** DEV-CONTROL-PLANE.md — adds script/tooling placement rows to boundary table

---

## Summary

Agents repeatedly placed portfolio-level scripts (validators, auditors, setup
enforcement, boundary checks) inside individual project repos instead of the
portfolio control plane. This PASS declares the placement rule for all scripts
and tooling files and gives agents a mandatory decision gate to run before
creating any script anywhere in the portfolio.

---

## The problem this solves

When an agent is asked to add a validator or setup script, the default instinct
is to place it next to the thing it validates — e.g., `niji/setup.ps1` for the
niji venv, `eco/setup.ps1` for the eco venv, `marlin/scripts/check-install.ps1`
for the Marlin acceptance check. This scatters portfolio-level enforcement across
individual repos, which:

- Makes the enforcement invisible to the portfolio operator
- Requires knowing which repo to look in for each check
- Defeats the purpose of the DCP as a single operational surface
- Creates drift when repos are cloned without the surrounding portfolio context

The correct result in the incident that prompted this PASS: all three scripts
collapsed into one — `c:\dev\validate-env-boundaries.ps1` — because all three
enforced portfolio-wide boundary rules, not project-specific behavior.

---

## Placement decision gate

Before creating any script, tool, automation, or validation file, an agent MUST
answer the following question:

> **Does this script enforce a rule, check a condition, or perform an operation
> that spans more than one project, or that the portfolio operator needs to run
> from a single central location?**

| Answer | Placement |
| --- | --- |
| Yes — enforces a portfolio rule or crosses project boundaries | `C:\dev` (DCP root) |
| Yes — the rule is portable across portfolios or organizations | `governance-commons/` |
| No — operates only on this project's own build/test/runtime artifacts | that project's repo |

If the answer is ambiguous, default to `C:\dev`. It is always easier to move a
script into a project repo later than to discover it was scattered there when it
should have been central.

---

## Canonical placement table

Extends the boundary table in DEV-CONTROL-PLANE.md:

| Script / tool type | Canonical location | Must NOT go in |
| --- | --- | --- |
| Portfolio validators (`validate-*.ps1`) | `C:\dev` | individual project repos |
| Portfolio audit tools | `C:\dev` or `governance-commons/gc-audit/tools/` | individual project repos |
| Sync scripts (`sync-*.ps1`) | `C:\dev` | individual project repos |
| Environment boundary checks | `C:\dev` | individual project repos |
| Setup enforcement (venv, PATH, install checks) | `C:\dev` | individual project repos |
| Portable GC standards and tooling | `governance-commons/` | `C:\dev` or project repos |
| Project build scripts | that project's repo | `C:\dev` |
| Project test runners | that project's repo | `C:\dev` |
| Project-specific CI config | that project's repo | `C:\dev` |

---

## What "project-specific" means

A script is project-specific if and only if:

1. It only reads or modifies files inside that project's own directory.
2. It has no meaning outside the context of that single project.
3. Removing it from that project would not affect any other project or the
   portfolio operator's ability to run the portfolio.

If a script checks a rule that applies to multiple projects (even if it was
written while working on just one), it is portfolio-level and belongs in `C:\dev`.

---

## Anti-patterns to reject

The following are non-conformant placements that agents must refuse to make:

- `{project}/setup.ps1` that creates a venv or configures an environment boundary
  → belongs in `C:\dev\validate-env-boundaries.ps1` or a DCP setup script
- `{project}/scripts/check-install.ps1` that validates a portfolio-wide install contract
  → belongs in `C:\dev\validate-env-boundaries.ps1`
- `{project}/validate-*.ps1` that checks a rule defined in GC or DEV-ACCORD
  → belongs in `C:\dev` or `governance-commons/gc-audit/tools/`
- Duplicate validators: one in `C:\dev` and one inside a project repo checking the same thing
  → consolidate into `C:\dev`; the project repo may reference it but must not own it

---

## Cluster Invariants

**DEV-ACCORD-CI-22 — Portfolio-level scripts belong in DCP, not project repos**
Any script that enforces a portfolio-wide rule, checks a cross-project condition,
or is intended to be run by the portfolio operator must live in `C:\dev`. Placing
such a script inside an individual project repo is non-conformant regardless of
which project prompted its creation.

**DEV-ACCORD-CI-23 — Agents must run the placement decision gate before creating scripts**
Before creating any script or tooling file, an agent must explicitly apply the
placement decision gate defined in this PASS. Skipping the gate and defaulting to
the project currently in focus is non-conformant.

**DEV-ACCORD-CI-24 — Ambiguous placement defaults to DCP**
When the correct placement of a script is unclear, the default is `C:\dev`. Moving
a script from DCP into a project repo is a deliberate, reviewable decision. The
reverse — discovering a portfolio-level script scattered in a project repo — is an
incident.

---

## Outputs

- Placement decision gate defined — mandatory before any script creation
- Canonical placement table declared and extends DEV-CONTROL-PLANE.md boundary table
- Anti-pattern list declared — agents must refuse these placements
- Three new cluster invariants: DEV-ACCORD-CI-22 through DEV-ACCORD-CI-24
