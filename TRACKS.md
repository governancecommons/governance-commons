# TRACKS — Governance Commons Portfolio Overview

**Last updated:** 2026-06-05T00:00:00Z
**Authority:** Master spec/project portfolio view. For PASS governance history see `DEVPATH.md`; for active execution priorities see `DEVPLAN.md`.

---

## Portfolio Status

| Track | Repo | Goal | Status | Next Milestone |
|-------|------|------|--------|----------------|
| [A](agent-dossier/) | agent-dossier | Per-agent identity, authority, handoff, telemetry, audit contract | 🔵 Active — P0 gaps closed | GC-1-A: P1 gap closure |
| [B](agent-matrix/) | agent-matrix | Multi-agent capability, routing, trust, safety, coordination | 🔵 Active — SKU/MCP/SLA gaps open | GC-1-B: SLA schema + MCP stub |
| [C](ons/) | ons | Naming grammar, namespace identity, validation rule IDs | 🟡 v1.2.0 pending publish | GC-1-C: stale header + schema fix |
| [D](project-orchestrator-agent/) | project-orchestrator-agent | Runtime execution contract — task graph, dispatch, handoff, audit | 🔵 Active — stale docs + P0 bugs | GC-1-D: stale docs + escalation fix |
| [E](governance-commons-code/) | governance-commons-code | SDK layer — Python/TypeScript validators, CLI, CI templates | 🔴 Not started | GC-2-E: PyPI + npm publish |
| [F](governance-commons-www/) | governance-commons-www | Public web presence for Governance Commons | 🔵 Active | Org creation + domain live |
| [F](agent-dossier-www/) | agent-dossier-www | Public web presence for Agent Dossier spec | 🔵 Active | — |
| [F](agent-dossier-vscode/) | agent-dossier-vscode | VS Code extension for Agent Dossier | 🔵 Active | ONS TypeScript impl needed |

**Status key:** 🟢 Shipped · 🟡 Release prep · 🔵 Active dev · 🔴 Not started / planning

---

## Track Detail

### Track A — agent-dossier

**Scope:** Per-agent identity, authority, handoff, telemetry, and audit contract spec.
**Current version:** 1.0.x
**PASS:** PASS-1 (Spec Correctness)
**Open P0 gaps:** 0 (GC-1-A-01 through GC-1-A-06 closed in PASS-2026-0025)
**Open P1 gaps:** 3 (OTel adapter, PASS ID enforcement, handoff envelope emission)
**Key links:** `agent-dossier/ROADMAP.md`, `agent-dossier/CHANGELOG.md`

### Track B — agent-matrix

**Scope:** Multi-agent capability, routing, trust, safety, and coordination model spec.
**Current version:** 1.x
**PASS:** PASS-1 (Spec Correctness)
**Open Critical gaps:** 4 (MCP, A2A, CloudEvents, compliance mapping)
**Open High gaps:** 6 (SKU multi-provider, matrix composition, agent registry, identity, SLA, SLO)
**Key links:** `agent-matrix/CHANGELOG.md`, `agent-matrix/agent-matrix.yaml`

### Track C — ONS

**Scope:** Ontic Namespace Structure — naming grammar, namespace identity, collision rules, validation IDs.
**Current version:** 1.2.0 (local tag — NOT yet pushed; blocked on org creation)
**PASS:** PASS-1 (Spec Correctness) — P0 fixes first
**Open P0 gaps:** 2 (stale header, conformance schema divergence)
**Open High gaps:** 2 (cluster registration protocol, RFC 2119 normative language)
**Key links:** `ons/ons.yaml`, `ons/CHANGELOG.md`

### Track D — project-orchestrator-agent

**Scope:** Runtime execution contract for project-level orchestrators.
**Current version:** Python rewrite (PASS-2026-0002) — docs still reflect old state
**PASS:** PASS-0 immediate + PASS-1
**Open P0 gaps:** 3 (stale DevPath/Tracks, missing CHANGELOG entry, unreachable level-2 escalation)
**Open P1 gaps:** 3 (agent telemetry, deterministic compilation, models/task.py unused)
**Key links:** `project-orchestrator-agent/DevPath-v1.0.md`, `project-orchestrator-agent/Tracks.md`

### Track E — governance-commons-code (SDK)

**Scope:** Code-level implementation — Python/TypeScript/Go validators, CLI tooling, CI templates.
**Current version:** Not started
**PASS:** PASS-3 (Tooling, SDKs, Packaging)
**Key deliverables:** governance-commons-py (PyPI), governance-commons-js (npm), GitHub Actions templates
**Key links:** `governance-commons-code/` (empty)

### Track F — Web Presence

**Scope:** All public-facing sites and extensions.
**Repos:** governance-commons-www, agent-dossier-www, agent-dossier-vscode
**Current state:** Sites active; governancecommons.org not yet live; org not yet created
**Blocked by:** GitHub org creation (GC-2-G-01)
**Key links:** `governance-commons-www/`, `agent-dossier-www/`

### Track G — Ecosystem Infrastructure

**Scope:** GitHub org, domain, npm org, PyPI namespace, conformance program.
**Current state:** All deferred — no org, no domain, no package accounts
**PASS:** PASS-5 (Public Release Train) — start infrastructure when PASS-2 is in flight
**Key milestones:** GitHub org, governancecommons.org live, PyPI/npm namespace claim

---

## Dependency Map

```text
Track A (agent-dossier)
  └── GC-1-A: P0 gap closure ──► GC v1.2.0 milestone
        └── GC-2-A: capability profiles / installable SDK

Track B (agent-matrix)
  └── GC-1-B: SLA schema + MCP stub ──► GC v1.2.0 milestone
        └── GC-2-B: matrix composition + workflow patterns
              └── GC-3-B: A2A binding + registry + identity

Track C (ONS)
  └── GC-1-C: P0 fixes + RFC 2119 ──► ONS v1.2.0 published
        └── GC-2-C: TypeScript impl + conformance tests
              └── GC-4-C: LSP implementation

Track D (project-orchestrator-agent)
  └── GC-1-D: stale docs + P0 bugs ──► PASS-1 clean
        └── GC-1-D-07/08: handoff envelopes + integration tests

Track E (SDK layer)
  └── PASS-3 ──► governance-commons-py (PyPI) + governance-commons-js (npm)
                └── GitHub Actions templates

Track F (web presence)
  └── Track G org creation ──► governancecommons.org live
                             └── GitHub Releases for all specs

Track G (infrastructure)
  └── GitHub org ──► Track C ONS v1.2.0 GitHub Release
                  └── Track F site deployment
```

---

## Cross-Track Notes

- **Track C (ONS) is the first to publish.** ONS v1.2.0 exists locally; it just needs P0 fixes and a GitHub org to push to.
- **Track D (project-orchestrator-agent) has the most urgent P0 bugs.** The level-2 escalation bug (escalation.py:27-31) is a code correctness issue affecting the governance contract — fix before any other Track D work.
- **Track E (SDK) is a multiplier.** Nothing in Track E is a prerequisite for PASS-1 work, but it unblocks every adoption path for PASS-3+. Identify a starting point (Python validator CLI) and begin scaffolding in parallel with PASS-1.
- **Track F and Track G are coupled.** Web presence work is blocked on org creation. Do not invest in Track F beyond maintenance until the GitHub org exists.
- **CNCF/W3C analogy (source 102):** These ecosystems have formal charters, WG structures, RFC processes, and IP agreements. Governance Commons currently has none of these. Track G owns all of them. They are prerequisites for any enterprise conformance claims.
- **hbl and osprey are NOT listed here.** They are aspirational peer ecosystems. They will appear in TRACKS.md only when real repos exist.

---

## Quick Links

| Resource | Purpose |
|----------|---------|
| `DEVPATH.md` | Ecosystem governance path — PASS registry, design decisions, authority model |
| `DEVPLAN.md` | Current execution plan — active priorities, gap checklist, release train |
| `projects.yaml` | Machine-readable project registry — groups, paths, compat constraints |
| `tools/gc-status.ps1` | Git status dashboard for all sub-repos |
| `docs/charter.md` | AL:3 ecosystem invariants — licensing, naming, founding maintainer |
| `docs/architecture/` | Ecosystem architecture diagrams |
| `docs/rfc/` | RFC proposals (active at PASS-5) |
| `docs/conformance/` | Conformance criteria for GC adopters |
