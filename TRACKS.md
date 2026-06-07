# TRACKS — Governance Commons Portfolio Overview

**Last updated:** 2026-06-07T00:00:00Z
**Authority:** Master spec/project portfolio view. For PASS governance history see `DEVPATH.md`; for active execution priorities see `DEVPLAN.md`.

---

## Portfolio Status

| Track | Repo | Goal | Status | Next Milestone |
|-------|------|------|--------|----------------|
| [Alpha](agent-dossier/) | agent-dossier | Per-agent identity, authority, handoff, telemetry, audit contract | 🔵 Active — P0 gaps closed | GC-1-A: P1 gap closure |
| [Bravo](agent-matrix/) | agent-matrix | Multi-agent capability, routing, trust, safety, coordination | 🔵 Active — SKU/MCP/SLA gaps open | GC-1-B: SLA schema + MCP stub |
| [Charlie](ons/) | ons | Naming grammar, namespace identity, validation rule IDs | 🟢 Stable — v1.3.0 shipped | GC-1-C-08/09: FAST rules + soft-deprecation |
| [Delta](agent-project-orchestrator/) | agent-project-orchestrator | Runtime execution contract — task graph, dispatch, handoff, audit | 🟢 Stable — PASS-2 runtime governance + budgets enforced | PASS-2 backlog clear |
| [Echo](governance-commons-sdk/) | governance-commons-sdk | SDK layer — Python/TypeScript validators, CLI, CI templates | 🟡 Release prep — v0.1.0 scaffolded | GC-2-E: PyPI + npm publish |
| [Foxtrot](governance-commons-www/) | governance-commons-www | Public web presence for Governance Commons | 🔵 Active | Org creation + domain live |
| [Foxtrot](agent-dossier-www/) | agent-dossier-www | Public web presence for Agent Dossier spec | 🔵 Active | — |
| [Foxtrot](governance-commons-vscode/) | governance-commons-vscode | VS Code extension for Governance Commons standards | 🔵 Active | ONS TypeScript impl needed |
| [Golf](projects.yaml) | ecosystem infrastructure | GitHub org, domain, npm org, PyPI namespace, conformance program | 🔴 Deferred | Start when PASS-2 is in flight |

**Status key:** 🟢 Shipped · 🟡 Release prep · 🔵 Active dev · 🔴 Not started / planning

**Naming note:** NATO call signs are display titles for the canonical track letters only: A/Alpha through G/Golf. They do not rename task namespaces or imply a separate planning taxonomy.

---

## Track Detail

### Track Alpha — agent-dossier

**Scope:** Per-agent identity, authority, handoff, telemetry, and audit contract spec.
**Current version:** 1.0.x
**PASS:** PASS-1 (Spec Correctness)
**Open P0 gaps:** 0 (GC-1-A-01 through GC-1-A-06 closed in PASS-2026-0025)
**Open P1 gaps:** 3 (OTel adapter, PASS ID enforcement, handoff envelope emission)
**Key links:** `agent-dossier/ROADMAP.md`, `agent-dossier/CHANGELOG.md`

### Track Bravo — agent-matrix

**Scope:** Multi-agent capability, routing, trust, safety, and coordination model spec.
**Current version:** 1.x
**PASS:** PASS-1 (Spec Correctness)
**Open Critical gaps:** 4 (MCP, A2A, CloudEvents, compliance mapping)
**Open High gaps:** 6 (SKU multi-provider, matrix composition, agent registry, identity, SLA, SLO)
**Key links:** `agent-matrix/CHANGELOG.md`, `agent-matrix/agent-matrix.yaml`

### Track Charlie — ONS

**Scope:** Ontic Namespace Structure — naming grammar, namespace identity, collision rules, validation IDs.
**Current version:** 1.3.0
**PASS:** PASS-1 (Spec Correctness) — P0 fixes closed
**Open P0 gaps:** 0
**Open High gaps:** 0 (cluster registration protocol closed — registry/clusters.yaml created, PASS-2026-0009)
**Key links:** `ons/ons.yaml`, `ons/CHANGELOG.md`

### Track Delta — agent-project-orchestrator

**Scope:** Runtime execution contract for project-level orchestrators.
**Current version:** 1.0.x (renamed to agent-project-orchestrator; PASS-1 P0 closure complete)
**PASS:** PASS-1 (runtime correctness) — P1 batch closed
**Open P0 gaps:** 0
**Open P1/P2 runtime gaps:** 0
**Key links:** `agent-project-orchestrator/DEVPATH.md`, `agent-project-orchestrator/DEVPLAN.md`, `agent-project-orchestrator/TRACKS.md`

### Track Echo — governance-commons-sdk (SDK)

**Scope:** Code-level implementation — Python/TypeScript/Go validators, CLI tooling, CI templates.
**Current version:** 0.1.0 scaffold
**PASS:** PASS-3 (Tooling, SDKs, Packaging)
**Key deliverables:** governance-commons-py (PyPI), governance-commons-js (npm), GitHub Actions templates
**Key links:** `governance-commons-sdk/`

### Track Foxtrot — Web Presence

**Scope:** All public-facing sites and extensions.
**Repos:** governance-commons-www, agent-dossier-www, governance-commons-vscode
**Current state:** Sites active; governancecommons.org not yet live; org not yet created
**Blocked by:** GitHub org creation (GC-2-G-01)
**Key links:** `governance-commons-www/`, `agent-dossier-www/`

### Track Golf — Ecosystem Infrastructure

**Scope:** GitHub org, domain, npm org, PyPI namespace, conformance program.
**Current state:** All deferred — no org, no domain, no package accounts
**PASS:** PASS-5 (Public Release Train) — start infrastructure when PASS-2 is in flight
**Key milestones:** GitHub org, governancecommons.org live, PyPI/npm namespace claim

---

## Dependency Map

```text
Track Alpha (agent-dossier)
  └── GC-1-A: P0 gap closure ──► GC v1.2.0 milestone
        └── GC-2-A: capability profiles / installable SDK

Track Bravo (agent-matrix)
  └── GC-1-B: SLA schema + MCP stub ──► GC v1.2.0 milestone
        └── GC-2-B: matrix composition + workflow patterns
              └── GC-3-B: A2A binding + registry + identity

Track Charlie (ONS)
  └── GC-1-C: P0 fixes + RFC 2119 ──► ONS v1.2.0 published
        └── GC-2-C: TypeScript impl + conformance tests
              └── GC-4-C: LSP implementation

Track Delta (agent-project-orchestrator)
  └── GC-1-D: P0/P1 runtime correctness + overlay roster + runtime governance + resource budgets closed

Track Echo (SDK layer)
  └── PASS-3 ──► governance-commons-py (PyPI) + governance-commons-js (npm)
                └── GitHub Actions templates

Track Foxtrot (web presence)
  └── Track Golf org creation ──► governancecommons.org live
                               └── GitHub Releases for all specs

Track Golf (infrastructure)
  └── GitHub org ──► Track Charlie ONS v1.2.0 GitHub Release
                  └── Track Foxtrot site deployment
```

---

## Cross-Track Notes

- **Track Charlie (ONS) is stable at v1.3.0.** Remaining PASS-1 work: GC-1-C-08 (FAST rule enforcement) and GC-1-C-09 (rule soft-deprecation).
- **Track Delta (agent-project-orchestrator) P1 runtime correctness, overlay roster support, multi-agent governance runtime loading, and resource-budget enforcement are closed.**
- **Track Echo (SDK) is in release prep.** Python and TypeScript package scaffolds exist locally; PyPI/npm publication is still pending.
- **agent-team-protocol has its PASS-1 schema/test batch closed.** It is tracked as a project/work area in `projects.yaml`, not as a portfolio track call sign.
- **Track Foxtrot and Track Golf are coupled.** Web presence work is blocked on org creation. Do not invest in Track Foxtrot beyond maintenance until the GitHub org exists.
- **CNCF/W3C analogy (source 102):** These ecosystems have formal charters, WG structures, RFC processes, and IP agreements. Governance Commons currently has none of these. Track Golf owns all of them. They are prerequisites for any enterprise conformance claims.
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
