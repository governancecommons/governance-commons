# DEV-ACCORD.03 — Agent Onboarding Protocol

**PASS ID:** DEV-ACCORD.03
**Canonical ID:** GC:2011
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-28T00:00:00Z
**Depends on:** GC:2008 (DEV-ACCORD.00), GC:2010 (DEV-ACCORD.02)
**Partially superseded by:** GC:2016 (DEV-ACCORD.08) — planning doc visibility table and private doc rule replaced
**Amended by:** GC-PASS-0022.00 (2026-08-19) — added Capability Contract package to reading order and router

---

## Summary

The canonical onboarding protocol for any agent operating in this portfolio.
Agent-agnostic. Any GC-conformant agent reads this file before starting work.
Agent-specific bootstrap files are adapters that point here and contain no
portfolio governance. Bootstrap-file conformance is governed by
DEV-ACCORD.04.

---

## Reading order

The full agent-trail for governed project work is:

1. `PROTECTED.md` — files that cannot be touched without explicit instruction
2. `DEV-CONTROL-PLANE.md` — portfolio boundary doctrine
3. `docs/REVIEW-GRAMMAR.md` — command vocabulary: normalize, validate, verify, trace, adversarial audit, meta-audit, close-the-loop, de-stale
4. `governance-commons/passes/dev-accord/DEV-ACCORD.02.md` — execution model: PASS, RUN, Evidence Bundle
5. `governance-commons/passes/dev-accord/DEV-ACCORD.06.md` — Change Playbook: BUNT/RUN/DRIVE/PASS classes, DEV-DOCS obligations, commit trailers
6. `governance-commons/passes/dev-accord/DEV-ACCORD.10.md` — Git split authorization: no new branch, PR chain, worktree, or fork without explicit human approval
7. `projects.yaml` — project registry and canonical plan pointers
8. `dev-docs/_root/contracts/README.md` — Capability Contract package: shared vocabulary for what a project provides/consumes/prohibits for another. Read before declaring, naming, or extending any cross-project capability, and before writing or editing any project's `DEV-CAPABILITIES.md`.
9. The specific project's `DEV-PATH.md` and `DEV-PLAN.md`

**Read when coordinating with other agents:**
`governance-commons/agent-matrix/agent-matrix.yaml` — agent roles, capabilities, routing, trust levels. Only needed when more than one agent is working on the same project in the same session.

### Bootstrap router

The reading order above defines the full agent-trail. Agents may use the router
below to avoid expanding every reference before low-risk work. If the task
escalates, read the additional authority before editing further.

| Task shape | Read now | Defer unless needed |
| --- | --- | --- |
| Read-only answer, orientation, or file lookup | `PROTECTED.md`, `DEV-CONTROL-PLANE.md`, relevant `REVIEW-GRAMMAR` verb | Project `DEV-PATH.md` / `DEV-PLAN.md`, Change Playbook details |
| BUNT: typo, formatting, comment-only, no state change | `PROTECTED.md`, `DEV-CONTROL-PLANE.md`, `DEV-ACCORD.06` BUNT obligations | Project planning docs, PASS/RUN evidence details |
| RUN: bounded single-repo work | Full reading order through `projects.yaml`; project `DEV-PLAN.md` when the change affects project state | Agent Matrix, evidence-bundle details unless significant |
| DRIVE or PASS-trigger work | Full reading order, relevant PASS authority, project `DEV-PATH.md` and `DEV-PLAN.md` | Nothing material; escalate before editing if authority is unclear |
| Client/repo cleanup with no GC standard change | `PROTECTED.md`, `DEV-CONTROL-PLANE.md`, relevant local instructions, `DEV-ACCORD.06` level check | Full GC taxonomy unless the cleanup touches DEV-DOCS, release truth, or protected files |
| Multi-agent or cross-repo work | Full reading order plus `agent-matrix.yaml` | None |
| Naming/declaring what a project provides, consumes, or prohibits for another project | `dev-docs/_root/contracts/README.md` (Capability Contract package) | Full reading order unless the change also touches PASS/governance authority |

The router does not override `PROTECTED.md`, DEV-ACCORD.06 escalation rules, or
DEV-ACCORD.10 git split authorization. A direct edit to a GC standard remains a
PASS-trigger change.

---

## Agent-Trail

**Agent-trail** is the named reading chain that orients any GC-conformant agent from session start to project-specific context. The shorthand form used in instructions and governance docs:

```text
AGENTS.md → DEV-ACCORD.03 → REVIEW-GRAMMAR → local guidance
```

Expanded to the full reading sequence:

| Step | File | What it provides |
| --- | --- | --- |
| Entry | `AGENTS.md` / `CLAUDE.md` | Runtime bootstrap; routes to DEV-ACCORD.03 and nowhere else |
| Protocol | `DEV-ACCORD.03` (this file) | Reading order, portfolio rules, ecosystem map |
| Rules | `PROTECTED.md` | Files that cannot be touched; append-only constraints |
| Doctrine | `DEV-CONTROL-PLANE.md` | Portfolio boundary doctrine: what belongs where |
| Vocabulary | `docs/REVIEW-GRAMMAR.md` | Working command language for the session |
| Execution model | `DEV-ACCORD.02.md` | PASS, RUN, and Evidence Bundle definitions |
| Change Playbook | `DEV-ACCORD.06.md` | BUNT/RUN/DRIVE/PASS change classes, escalation rules, commit trailers |
| Git split rule | `DEV-ACCORD.10.md` | Current-branch publish default; branches/PR chains/worktrees/forks require human authorization |
| Registry | `projects.yaml` | Project index and canonical plan pointers |
| Capability vocabulary | `dev-docs/_root/contracts/README.md` | Shared cross-project capability grammar; read before naming/declaring what a project can do for another |
| Local context | `DEV-PATH.md` + `DEV-PLAN.md` | Project-specific decisions, current phase, active work |

**Properties:**

- The trail is sequential. Each step depends on the prior steps being read.
- The entry step is runtime-specific (`CLAUDE.md` for Claude Code; `AGENTS.md` for other GC-conformant agents). The rest are universal.
- The vocabulary step (`REVIEW-GRAMMAR.md`) makes single-word session commands — normalize, validate, adversarial audit, de-stale — unambiguous without explanation in every session.
- The local context step is project-scoped. It varies per project but always follows the DEV-PATH / DEV-PLAN shape defined in this portfolio.

An agent that reads all steps is oriented. One that skips any step risks violating portfolio rules, misreading a command verb, or acting without understanding the project's current state.

The term **agent-trail** may be used in any governance doc, instruction file, or session note to refer to this chain without spelling it out in full.

---

## Agent bootstrap files

Bootstrap file requirements are defined by DEV-ACCORD.04. This portfolio uses
the following bootstrap files:

| Agent | Bootstrap file | How it reads | Status |
| --- | --- | --- | --- |
| Claude Code | `CLAUDE.md` | platform adapter; Claude Code auto-reads this file | active |
| GC-conformant agents | `AGENTS.md` | normative GC bootstrap; auto-read depends on runtime or adapter | active |

`AGENTS.md` is the cross-agent standard for GC-conformant agents. DEV-ACCORD
does not claim every vendor runtime auto-discovers `AGENTS.md`; it defines what
GC-conformant agents and adapters must read before acting.

---

## Portfolio rules

**Do not rewrite.** Append to planning docs. Do not restructure them.

**Do not rename files.** If a rename seems necessary, ask first.

**Do not delete feature ideas or queued work.** Append to `DEV-PLAN.md`
under `## QUEUED IDEAS`.

**Do not bulk-edit multiple planning docs** without surfacing changes for
approval first.

**Ask before touching** any file marked AL:1 beyond the permitted operations
in `PROTECTED.md`.

---

## What this portfolio is

`C:\dev` is a portfolio control plane — not a monorepo or single project.
Each subdirectory is an independent project with its own planning docs. See
`DEV-CONTROL-PLANE.md` for the boundary doctrine.

---

## Ecosystem overview

| Folder | What it is |
| --- | --- |
| `governance-commons/` | Portable GC standards — CANON, ONS, DEV-ACCORD, Agent Dossier, Agent Matrix |
| `dxp-org/` | DevXToolkit — developer experience tools portfolio |
| `eco/`, `eco-edge/`, `eos/` | Eco ecosystem — AI governance platform |
| `arche/`, `cockpit/`, `elan/` | Other active projects |
| `docs/` | Portfolio-level research, source corpus, planning templates |
| `governed-event/` | Governed Event Envelope (GEE) v0.1 + API-E Workflow Provenance Ontology |
| `time-loc/` | Canonical temporal-spatial primitive (time.loc v1.2) — dependency of governed-event |
| `lasso/` | Multi-agent orchestration platform (concept/design stage) |
| `niji/` | Color palette generator — successor to CPM15 |
| `kinjuu/` | Future app — financial/budget/deadline tracking |
| `dxp-init/` | Marlin — universal package manager and installer family. Four lanes: `marlin` (package manager — apps on machines) · `marlin-dxp` (installs and conforms repo(s) to GC and DXP standards) · `marlin-dcp` (workspace/org manager — DCP lifecycle, repo registry, portfolio sync) · marlin-ux (Cockpit GUI panels for all lanes). Migrating to `marlin/` repo. |
| `bax/` | BAX — governed NCAA tournament structural-evaluation and prediction system (BAX-CORE MACRO/MESO/MICRO factors, BAX-EDGE matchup/bracket layer). Onboarded into GC governance 2026-08-18; see `bax/DEV-PATH.md`. |

---

## Planning doc visibility

DEV-ACCORD.08 (GC:2016) replaces the original planning-doc visibility table and
private doc rule from this PASS. Use DEV-ACCORD.08 as the authority for:

- DEV-DOCS private-by-default handling
- public-safe bootstrap stubs
- required public distribution `.gitignore` block
- `MARKET.md` and `DIST.md` private-repo-only handling

`DEV-RELEASE.md` remains the authority for software release gates. `DIST.md`
commercial milestones must reference `DEV-RELEASE.md` rather than duplicate
version targets.

No new strategy doc types may be introduced without a DEV-ACCORD update.

## Strategy doc schemas

### MARKET.md schema

Every `MARKET.md` must contain these sections in order:

```text
# {Product} — Marketing Strategy
[Owner / Classification / Updated header]

## Positioning
One sentence + the gap the product fills.

## Target Audiences
### Primary — {label}
### Secondary — {label}
### Tertiary — {label}  (omit if none)

## Differentiators
Table: Dimension | {Product} | Competitor… | Competitor…

## Channels
### Phase 1 — {label}
### Phase 2 — {label}
### Phase 3 — {label}  (omit if none)

## Messaging by {Tier|Lane|Audience}
Short copy per tier or product lane.

## Key Narratives
Bullet list — 3–5 narratives, one sentence each.
```

Sections may not be removed or reordered. Additional sections may be appended after Key Narratives.

### DIST.md schema

Every `DIST.md` must contain these sections in order:

```text
# {Product} — Distribution & Monetization Plan
[Owner / Classification / Updated header]

## Distribution Tiers
### Tier 1 — Community ({licence}, free)
### Tier 2 — {name} (paid)
### Tier 3 — {name} (paid)  (omit if none)

## Revenue Streams
### Near-term
### Mid-term
### Long-term

## Open-Source Strategy
Why {licence choice}. CLA policy.

## {Product-specific section}  (optional)
e.g. "Marlin as Distribution for the Product Family"

## Commercial Milestones
Pointer: "Software release gates live in DEV-RELEASE.md in the {product} repo."
Table: commercial-only milestones (first inquiry, first deal, first SLA…).
```

Sections may not be removed or reordered. The Commercial Milestones section must always include the DEV-RELEASE.md pointer before the table. Additional sections may be appended after Commercial Milestones.

---

## Files changed

Doctrine-only PASS. No implementation files created beyond the agent
bootstrap files listed above.

---

## Constraints introduced

- All portfolio governance and reading order lives in this file, not in any
  agent-specific bootstrap file.
- Agent bootstrap files must conform to DEV-ACCORD.04.
- Any future agent runtime added to this portfolio must either read `AGENTS.md`
  directly or provide an adapter file that points to `AGENTS.md` or this
  document before its first session.
