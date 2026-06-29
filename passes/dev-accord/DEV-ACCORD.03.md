# DEV-ACCORD.03 — Agent Onboarding Protocol

**PASS ID:** DEV-ACCORD.03
**Canonical ID:** GC:2011
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-28T00:00:00Z
**Depends on:** GC:2008 (DEV-ACCORD.00), GC:2010 (DEV-ACCORD.02)

---

## Summary

The canonical onboarding protocol for any agent operating in this portfolio.
Agent-agnostic. Claude, Codex, Copilot, and any future agent all read this
file before starting work. Agent-specific bootstrap files (CLAUDE.md,
CODEX.md, COPILOT.md) are thin wrappers that point here and contain nothing
else. All governance lives here.

---

## Reading order

Before taking any action on any project:

1. `PROTECTED.md` — files that cannot be touched without explicit instruction
2. `DEV-CONTROL-PLANE.md` — portfolio boundary doctrine
3. `docs/REVIEW-GRAMMAR.md` — command vocabulary: normalize, validate, verify, trace, adversarial audit, meta-audit, close-the-loop, de-stale
4. `governance-commons/passes/dev-accord/DEV-ACCORD.02.md` — execution model: PASS, RUN, Evidence Bundle
5. `governance-commons/agent-matrix/agent-matrix.yaml` — multi-agent governance: agent roles, capabilities, routing, trust levels
6. `projects.yaml` — project registry and canonical plan pointers
7. The specific project's `DEV-PATH.md` and `DEV-PLAN.md`

---

## Agent bootstrap files

Each agent reads its own thin bootstrap file at the portfolio root. That file
contains one instruction: read this document. Nothing else belongs in it.

| Agent | Bootstrap file | Status |
| --- | --- | --- |
| Claude Code | `CLAUDE.md` | active |
| Codex | `CODEX.md` | not yet created |
| Copilot | `COPILOT.md` | not yet created |

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
| `dxp-init/` | Developer onboarding wizard — five-minute governance bootstrap |

---

## Planning doc roles

| Doc | Owns |
| --- | --- |
| `DEV-PATH.md` | Phase history, design decisions, PASS registry — append-only |
| `DEV-PLAN.md` | Current execution state, active milestones, priority work queue |
| `DEV-TRACKS.md` | Parallel workstreams and dependencies |
| `passchangelog.md` | Ecosystem-level governance decisions — append-only |

---

## Files changed

Doctrine-only PASS. No implementation files created beyond the agent
bootstrap files listed above.

---

## Constraints introduced

- All portfolio governance and reading order lives in this file, not in any
  agent-specific bootstrap file.
- Agent bootstrap files (CLAUDE.md, CODEX.md, COPILOT.md) must contain only
  a pointer to this document. No governance content belongs in them.
- Any future agent added to this portfolio must have a bootstrap file created
  and registered in the table above before its first session.
