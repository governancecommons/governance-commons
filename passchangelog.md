# PASSCHANGELOG — Governance Commons

Ecosystem-level governance decisions for the Governance Commons ecosystem.
For per-spec implementation changes, see each spec's own `passchangelog.md` and `CHANGELOG.md`.

Format: GC-PASS-YYYY-NNNN (year, 4-digit sequence). Newest first.

---

## GC-PASS-2026-0003 — 2026-06-07

**pass_id**: GC-PASS-2026-0003
**change_type**: governance
**authority_level**: AL:2
**summary**: Published `docs/observability-contract.yaml` — the ecosystem-level OpenTelemetry
semantic conventions for all `gc.agent.*` instrumentation. Defines required span attributes
(`gc.agent.id`, `gc.agent.class`, `gc.agent.dossier_version`, `gc.agent.event_type`,
`gc.trace_id`, `gc.event_id`, `gc.time_loc`, `gc.severity`, `gc.summary`), OTel severity number
mapping (debug→1/TRACE, info→9/INFO, warning→13/WARN, error→17/ERROR, critical→21/FATAL), log
record field conventions, metric conventions, and 7 compliance rules (obs-1 through obs-7).
Enforces DDR-6 L3: `gc.time_loc` is required on every `gc.agent.*` event; consumers MUST reject
events without it. Closes GC-3-E-01.
**status**: ACCEPTED
**affected_specs**: agent-dossier, agent-project-orchestrator, governance-commons

---

## GC-PASS-2026-0002 — 2026-06-05

**pass_id**: GC-PASS-2026-0002
**change_type**: governance
**authority_level**: AL:2
**summary**: Established unified per-repo planning structure across all four core spec repos. Each spec (agent-dossier, agent-matrix, ons, agent-project-orchestrator) now has DEVPATH.md, DEVPLAN.md, TRACKS.md, and passchangelog.md under AL:1 authority. Stale planning files in agent-project-orchestrator (DevPath-v1.0.md, DevPlan-v1.0.md, Tracks.md) replaced with canonical-format equivalents. ROADMAP.md in agent-dossier retired; deferred items carried forward in agent-dossier DEVPLAN.md.
**status**: ACCEPTED
**affected_specs**: agent-dossier, agent-matrix, ons, agent-project-orchestrator

---

## GC-PASS-2026-0001 — 2026-06-05

**pass_id**: GC-PASS-2026-0001
**change_type**: governance
**authority_level**: AL:2
**summary**: Governance Commons ecosystem planning infrastructure declared. DEVPATH.md (ecosystem phases, authority model, design decisions DDR-1 through DDR-5), DEVPLAN.md (execution plan, gap analysis checklist, charter and process), TRACKS.md (portfolio overview, dependency map), projects.yaml (machine-readable project registry with compat: fields), tools/gc-status.ps1 (status dashboard), docs/ (charter, architecture, rfc, conformance), and tools/ directory structure established at governance-commons root. PASS-0 bootstrap phase initiated. Five design decisions from source_102 answered and recorded as binding AL:2 decisions.
**status**: ACCEPTED
**affected_specs**: governance-commons

---

<!-- New entries go above this line, newest first -->
