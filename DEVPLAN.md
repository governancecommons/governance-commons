# DEVPLAN — Governance Commons Execution Plan

**AUTHORITY LEVEL: AL:2**
**Status:** ACTIVE — canonical execution and release planning source
**time.loc:** 2026-06-05T00:00:00Z
**Canonical pair:** `DEVPATH.md` + `DEVPLAN.md`

---

## CANONICAL DOC RULE

There are exactly two root planning documents for Governance Commons:

1. `DEVPATH.md` — history and governance path. Owns phase/PASS registry, design decision record, authority model, agent onboarding.
2. `DEVPLAN.md` — current execution plan. Owns active priorities, release train status, compatibility matrix, and gap closure tracking.

All other devpath/devplan files under this directory are non-canonical unless they explicitly redirect here.
Sub-repo planning files (e.g., `agent-dossier/ROADMAP.md`) are AL:1 and do not supersede this file.

---

## CURRENT EXECUTION POSITION

**Active PASS:** PASS-0 (Ecosystem Planning Baseline)
**Primary active tracks:** Track C (ONS) + Track D (project-orchestrator-agent) — P0 fixes first
**Secondary active track:** Track A (agent-dossier) — P0/P1 gap closure
**Next milestone:** PASS-1 (Spec Correctness and Validation)

**Recently completed:**

- Source 97–102 gap analysis series read and synthesized
- Three source_102 design decisions answered in DEVPATH.md
- Ecosystem planning infrastructure created (DEVPATH, DEVPLAN, TRACKS, projects.yaml, tools/gc-status.ps1)

**Immediate next tasks (in priority order):**

1. ~~GC-1-C-01 — Fix stale ons.yaml header~~ ✅ DONE (PASS-2026-0005)
2. ~~GC-1-C-02 — Fix ons-conformance.schema.json divergence~~ ✅ DONE (PASS-2026-0006)
3. ~~GC-1-D-02 — CHANGELOG missing Python rewrite entry~~ ✅ DONE
4. ~~GC-1-D-01 — Fix unreachable level-2 escalation + stale Tracks docs~~ ✅ DONE
5. ~~GC-1-A-01 through GC-1-A-06 — agent-dossier P0 fixes~~ ✅ DONE (agent-dossier PASS-2026-0025)

---

## CHARTER AND PROCESS

The operating model gaps Codex flagged as the real missing pieces. These govern how Governance
Commons works as a standards ecosystem, not just a collection of specs.

**Maintainer.** Jess Ervin (jj-ervin) is the founding maintainer. AL:2 decisions (compatibility
constraints, release milestones, design decisions) require a GC-PASS entry. AL:3 decisions
(charter changes, licensing model, inviolable invariants) require founder sign-off.

**How standards change.** Changes within a spec's own scope follow that spec's devpath at AL:1 —
no ecosystem approval needed. Changes that affect cross-spec compatibility (breaking changes,
new inter-spec contracts, shared schema evolution) require a coordinated update item recorded
in this file's COMPATIBILITY MATRIX section before they are merged.

**How breaking changes are coordinated.** Any spec proposing a breaking change that affects a
peer spec declares `BREAKING:` in its CHANGELOG and lists `breaking_consumers:` naming each
affected spec. This file records the coordinated update. Affected specs enter compat-hold on
the dependent work. The GC release milestone that includes the breaking change is blocked until
all listed consumers confirm compatibility.

**RFC process (target: PASS-5).** Public-facing changes to Governance Commons standards will
eventually go through a numbered RFC process. Format: `RFC-NNNN-<slug>.md` filed in a public
`rfcs/` directory. Acceptance requires: problem statement, proposal, alternatives considered,
and a two-week comment window before merge. This process does not exist yet — it is a PASS-5
exit criterion.

**What conformance means.** A project conforms to a Governance Commons standard when:
it satisfies all `MUST` requirements in the spec for its declared conformance profile
(advisory / standard / strict), and its conformance declaration passes the validator for that
spec version. Conformance is self-declared until a certification program exists (PASS-5).

**What a release includes.** A GC release is a named manifest that pins the minimum compatible
version of each included spec. It is not a monorepo tag. Each spec can still patch independently
after a GC release is declared. The release manifest format is a PASS-5 exit criterion.

**What evidence proves governance happened.** An audit-ready governance record must include:
a machine-readable compliance evidence export (signed, structured), a PASS audit trail with
timestamps, handoff envelopes for all agent-to-agent task transfers, and a telemetry trace
mapping task start through completion. This is the PASS-4 exit criterion.

**Steering committee / WG structure.** Not established yet. Required before enterprise procurement
claims. Record here when roles are assigned.

---

## THREE DESIGN DECISIONS — Answers

These are binding decisions at AL:2. Full rationale is in `DEVPATH.md` under Design Decision Record.

**DDR-1 — Version Conflict Handling:**
Breaking changes declare `BREAKING:` + `breaking_consumers:` in CHANGELOG. Ecosystem DEVPLAN records a coordinated update item. Downstream specs enter compat-hold. GC release milestone is blocked until all named consumers are resolved. Machine-readable artifact: `compat:` field in `projects.yaml`.

**DDR-2 — Release Train Mechanics:**
Each spec ships on its own cadence. GC milestones are informational pinning contracts — they name minimum compatible versions, not CI gates. `GC v1.2.0 = agent-dossier >=1.1.0 + agent-matrix >=1.3.0 + ONS >=1.2.0`. Adopters pin to the GC milestone, not to individual spec heads.

**DDR-3 — Authority Model:**
AL:3 = ecosystem charter (founder). AL:2 = this file (GC maintainer). AL:1 = individual repo devpaths (spec owners). Ecosystem devplan sets compatibility constraints and milestones only — cannot dictate implementation within a repo's AL:1 scope.

---

## RELEASE TRAIN STATUS

| GC Release | Status | Requires |
|------------|--------|---------|
| GC v1.0.0 | Implied (current) | Current published versions of each spec |
| GC v1.2.0 | Planned (M2) | agent-dossier >=1.1.0 + agent-matrix >=1.3.0 + ONS >=1.2.0 + POA >=1.1.0 |
| GC v1.3.0 | Planned (M3) | agent-dossier >=1.2.0 + agent-matrix >=1.4.0 + ONS >=1.3.0 |
| GC v2.0.0 | Planned (M4) | Major version — breaking changes allowed |

---

## COMPATIBILITY MATRIX

Current cross-repo version constraints. Updated when breaking changes are declared.

| Spec | Current version | Depends on | Constraint | Status |
|------|----------------|------------|------------|--------|
| agent-dossier | 1.0.x | ONS | ONS naming grammar for PASS IDs | No open conflicts |
| agent-matrix | 1.x | agent-dossier | dossier schema for capability profiles | No open conflicts |
| ONS | 1.2.0 | — | No upstream deps | No open conflicts |
| project-orchestrator-agent | 1.x | agent-dossier, agent-matrix | runtime-contract.yaml schema | No open conflicts |
| agent-team-protocol | 0.1.0 | agent-matrix >=1.4.0, agent-dossier >=1.0.0 | fleet governance consumes per-agent primitives | No open conflicts |

No current `compat-hold` items.

---

## GAP ANALYSIS CHECKLIST

Cross-reference from sources 97–101 to DEVPATH PASS assignments.
Status: **O** = open · **C** = closed · **WF** = won't-fix · **H** = compat-hold

### Source 97 — agent-dossier runtime gaps

| Gap | Description | Priority | PASS | Status |
|-----|-------------|----------|------|--------|
| 97-G1 | No package.json (js-yaml undeclared) | P0 | PASS-1 / GC-1-A-01 | C |
| 97-G2 | No .gitignore | P0 | PASS-1 / GC-1-A-02 | C |
| 97-G3 | JSON Schema validation declared but never wired | P0 | PASS-1 / GC-1-A-03 | C |
| 97-G4 | task-queue.json hand-written (must be compiled artifact) | P0 | PASS-1 / GC-1-A-04 | C |
| 97-G5 | No environment abstraction (paths/IDs/timeouts are literals) | P0 | PASS-1 / GC-1-A-05 | C |
| 97-G6 | Hardcoded Windows paths in source comments | P0 | PASS-1 / GC-1-A-06 | C |
| 97-G7 | Custom telemetry (not OpenTelemetry) | P1 | PASS-4 / GC-1-A-07 | O |
| 97-G8 | PASS-YYYY-NNNN ID format not validated or generated | P1 | PASS-1 / GC-1-A-08 | O |
| 97-G9 | Handoff envelope defined in spec, never emitted in code | P1 | PASS-1 / GC-1-A-09 | O |
| 97-G10 | Orchestrator monolith (no module split) | P2 | PASS-3 / GC-2-A-01 | O |
| 97-G11 | Agents hardcoded via require() (no plugin interface) | P2 | PASS-3 / GC-2-A-02 | O |
| 97-G12 | No Dockerfile or cloud deployment targets | P2 | PASS-3 | O |
| 97-G13 | No installable SDK (no main field, no CLI) | P2 | PASS-3 / GC-2-A-04 | O |
| 97-G14 | No feature flags, no tenant isolation | P3 | PASS-6 | O |
| 97-G15 | No SLSA build provenance | P3 | PASS-5 | O |

### Source 98 — agent-matrix strategic gaps

| Gap | Description | Priority | PASS | Status |
|-----|-------------|----------|------|--------|
| 98-G1 | No MCP server/client model | Critical | PASS-2 / GC-1-B-03 | C |
| 98-G2 | No A2A protocol binding | Critical | PASS-2 / GC-3-B-02 | C |
| 98-G3 | No CloudEvents envelope binding | Critical | PASS-2 / GC-3-B-03 | C |
| 98-G4 | No compliance framework mapping (NIST AI RMF, EU AI Act) | Critical | PASS-1 / GC-1-B-05 | C |
| 98-G5 | SKU model Anthropic-only, no multi-provider routing | Critical | PASS-1 / GC-1-B-04 | C |
| 98-G6 | No matrix overlays/fragments (monolithic YAML) | High | PASS-1 / GC-2-B-01 | C |
| 98-G7 | No named profiles (minimal, data-engineering) | High | PASS-1 / GC-2-B-02 | C |
| 98-G8 | No matrix inheritance (extends: with override semantics) | High | PASS-1 / GC-2-B-03 | C |
| 98-G9 | No runtime agent discovery or registry | High | PASS-2 / GC-3-B-01 | O |
| 98-G10 | No cryptographic agent identity | High | PASS-2 / GC-3-A-02 | O |
| 98-G11 | No formal SLO/SLI definitions per profile | High | PASS-1 / GC-1-B-01 | C |
| 98-G12 | No checkpoint format schema | Medium | PASS-1 / GC-1-B-02 | C |
| 98-G13 | No streaming output schema | Medium | PASS-2 / GC-3-B-04 | O |
| 98-G14 | No prompt injection defense spec | Medium | PASS-2 / GC-3-B-05 | O |
| 98-G15 | No named workflow pattern library | Medium | PASS-1 / GC-2-B-05 | O |
| 98-G16 | No multi-orchestrator topology spec | Medium | PASS-6 / GC-4-B-02 | O |

### Source 99 — project-orchestrator-agent runtime gaps

| Gap | Description | Priority | PASS | Status |
|-----|-------------|----------|------|--------|
| 99-G1 | DevPath + Tracks stale (PASS-1/2/3 marked PENDING, code exists) | P0 | PASS-0 / GC-1-D-01 | C |
| 99-G2 | CHANGELOG missing Python rewrite entry (PASS-2026-0002) | P0 | PASS-0 / GC-1-D-02 | C |
| 99-G3 | Level-2 escalation (operator_clarification) unreachable in escalation.py:27-31 | P0 | PASS-1 / GC-1-D-03 | C |
| 99-G4 | Agents never call telemetry.emit() (all traces from dispatcher only) | P1 | PASS-4 / GC-1-D-04 | O |
| 99-G5 | runtime-contract.yaml non-deterministic (timestamp in trace_id) | P1 | PASS-1 / GC-1-D-05 | O |
| 99-G6 | models/task.py unused; raw dicts used instead | P1 | PASS-1 / GC-1-D-06 | O |
| 99-G7 | governance/multi-agent.yaml never read at runtime | P3 | PASS-2 | O |
| 99-G8 | Handoff envelopes not implemented (level-1 escalation logs warning, no envelope) | P2 | PASS-1 / GC-1-D-07 | O |
| 99-G9 | Zero test coverage for agents and orchestrator | P2 | PASS-1 / GC-1-D-08 | O |
| 99-G10 | Per-agent resource budgets not enforced (time_limit, tool_call_limit unused) | P3 | PASS-2 | O |

### Source 100 — ONS v1.2.0 gaps

| Gap | Description | Priority | PASS | Status |
|-----|-------------|----------|------|--------|
| 100-S1 | Stale header comment (v1.1.0/2026-06-03 vs body v1.2.0/2026-06-04) | Low | PASS-1 / GC-1-C-01 | C |
| 100-S2 | No casing rule for colon (qualification) domain | Medium | PASS-1 / GC-1-C-03 | O |
| 100-S3 | No cluster registration protocol or registry | High | PASS-1 / GC-1-C-05 | O |
| 100-S4 | ons-conformance.schema.json diverges from ons.yaml | High | PASS-1 / GC-1-C-02 | C |
| 100-S5 | No rule soft-deprecation mechanism | Medium | PASS-1 | O |
| 100-S6 | No RFC 2119 normative language | High | PASS-1 / GC-1-C-04 | C |
| 100-T1 | FAST rules in catalog but no validator implements them | — | PASS-1 | O |
| 100-T2 | No pytest suite for tools/validate.py | — | PASS-1 / GC-1-C-07 | O |
| 100-T3 | No rules.json export for LSP/linter authors | — | PASS-1 / GC-1-C-06 | O |
| 100-T4 | VALIDATOR_VERSION hardcoded 1.0.0 | — | PASS-3 | O |
| 100-A1 | RFC 2119 normative language (table stakes for citation) | Table stakes | PASS-1 / GC-1-C-04 | C |
| 100-A2 | Conformance test suite with test vectors | Medium | PASS-3 / GC-2-C-01 | O |
| 100-A3 | TypeScript reference implementation | High | PASS-3 / GC-2-C-02 | O |
| 100-A4 | pip install + npm package | Low-medium | PASS-3 | O |
| 100-N1 | LSP implementation (highest-leverage long-term move) | High effort | PASS-6 / GC-4-C-01 | O |
| 100-N2 | Global cluster registry as governed service | Low-medium | PASS-1 / GC-1-C-05 | O |
| 100-N3 | Machine-readable governance record schema | Medium | PASS-1 / GC-2-C-04 | O |

### Source 101 — Governance Commons capstone gaps

| Gap | Description | Priority | PASS | Status |
|-----|-------------|----------|------|--------|
| 101-G1a | A2A binding is surface mention only | Critical | PASS-2 / GC-3-B-02 | O |
| 101-G1b | MCP not a first-class governance primitive | Critical | PASS-2 / GC-1-B-03 | O |
| 101-G1c | No transport binding (HTTP/2 SSE, WebSocket, gRPC, Kafka) | Critical | PASS-2 | O |
| 101-G2a | No cryptographic integrity (handoffs can be replayed/forged) | Critical | PASS-2 / GC-3-A-01 | O |
| 101-G2b | Agent identity is string-only (no cryptographic binding) | Critical | PASS-2 / GC-3-A-02 | O |
| 101-G2c | No zero-trust establishment/verification/revocation spec | Critical | PASS-2 | O |
| 101-G3a | OTel listed in alignment but not specified (no span names, metric names) | High | PASS-4 / GC-3-E-01 | O |
| 101-G3b | No structured agent lifecycle event schema | High | PASS-4 | O |
| 101-G4a | NIST AI RMF surface mapping only, no control evidence generation | High | PASS-4 / GC-3-E-02 | O |
| 101-G4b | ISO 42001 missing entirely | High | PASS-4 / GC-3-E-03 | O |
| 101-G4c | SOC 2 Type II not addressed | High | PASS-4 | O |
| 101-G5 | Python-only (TypeScript, Go, Rust adopters have no path) | High | PASS-3 | O |
| 101-G6a | No RFC/proposal process | Medium | PASS-5 / GC-3-G-02 | O |
| 101-G6b | No conformance certification mechanism | Medium | PASS-5 / GC-3-G-03 | O |
| 101-G7a | No dossier revocation/expiry model | Medium | PASS-1 / GC-1-A-10 | O |
| 101-G7b | No versioned capability claims for audit replay | Medium | PASS-4 | O |
| 101-AC1 | Constitutional governance layer (constitution.yaml) | Ahead-of-curve | PASS-6 / GC-4-A-01 | O |
| 101-AC2 | Federated Agent Trust Network | Ahead-of-curve | PASS-6 / GC-4-B-01 | O |
| 101-AC3 | Temporal authority windows | Ahead-of-curve | PASS-6 / GC-4-A-02 | O |

---

## NEAR-TERM QUEUED WORK

Work registered but not yet active. Execute after active PASS-0 priorities clear.

| ID | Task | Track | PASS | Blocks |
|----|------|-------|------|--------|
| GC-1-A-07 | OpenTelemetry adapter for agent-dossier | A | PASS-4 | PASS-4 observability |
| GC-1-B-03 | Multi-provider SKU routing test vectors (agent-matrix) | B | PASS-1 | GC v1.2.0 milestone |
| GC-2-C-02 | TypeScript reference implementation for ONS | C | PASS-3 | VS Code extension path |
| GC-1-F-01 | agent-team-protocol: fleet-escalation + team-lifecycle schemas (ATP-1-01, ATP-1-02) | F | PASS-1 | GC v1.2.0 fleet governance |
| GC-1-F-02 | agent-team-protocol: pytest test vectors for all 5 sections (ATP-1-03–05) | F | PASS-1 | GC v1.2.0 fleet governance |
| GC-2-E-01 | governance-commons-py to PyPI | E | PASS-3 | zero-friction adoption |
| GC-2-E-02 | governance-commons-js to npm | E | PASS-3 | zero-friction adoption |
| GC-3-E-01 | observability-contract.yaml (gc.agent.* OTEL conventions) | E | PASS-4 | compliance evidence |

---

*This document is the single authority for Governance Commons execution planning.*
*Do not create alternate execution plan documents — update this one.*
