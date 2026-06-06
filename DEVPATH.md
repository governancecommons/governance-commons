# DEVPATH — Governance Commons Ecosystem Path

**AUTHORITY LEVEL: AL:2**
**Status:** ACTIVE
**Updated:** 2026-06-05

---

## CANONICAL DOC RULE

`DEVPATH.md` owns: ecosystem phases, authority model, design decision record.
`DEVPLAN.md` owns: current execution state, release train, compatibility matrix, gap checklist.

Sub-repo planning files (`agent-dossier/ROADMAP.md`, `agent-project-orchestrator/DevPath-v1.0.md`, etc.)
are **AL:1** — they govern their own repos and do not supersede this file.
This file does not contain per-repo task lists. It sets ecosystem structure and phase gates only.

---

## AUTHORITY MODEL

| Level | Scope | Who can change |
|-------|-------|----------------|
| AL:3 | Ecosystem charter — inviolable invariants, licensing model, GC naming | Founder only. Recorded as GC-CHARTER entries. |
| AL:2 | This file + DEVPLAN — compatibility constraints, release milestones, design decisions | GC project maintainer. Changes require a GC-PASS entry. |
| AL:1 | Individual repo devpaths — implementation, architecture, release cadence within a spec's scope | Spec owner, independently of ecosystem cadence. |

**Boundary rule:** AL:2 sets compatibility constraints and release milestones. It cannot dictate
implementation choices or release cadence inside any AL:1 repo devpath.

---

## THREE DESIGN DECISIONS

Source 102 identified three decisions that determine whether multi-repo ecosystem architecture
works in practice. Answers are binding at AL:2. Full rationale in `DEVPLAN.md`.

**DDR-1 — Version conflict handling.**
Specs declare `BREAKING:` + `breaking_consumers:` in their CHANGELOG when a breaking change
is proposed. The ecosystem DEVPLAN records a coordinated update item. Downstream specs enter
compat-hold. The next GC release milestone is blocked until all named consumers resolve.
Machine-readable contract: `compat:` field in `projects.yaml`.

**DDR-2 — Release train mechanics.**
Each spec ships on its own cadence with no shared devpath. GC release milestones (e.g., GC v1.2.0)
are informational pinning contracts that name the minimum compatible version of each spec.
They do not gate any spec's CI. Adopters who need a stable multi-spec combination pin to a GC
milestone. The milestone is declared `READY` only after all named versions are published and the
compatibility matrix shows no open compat-hold items.

**DDR-3 — Authority model.**
Answered in the table above. Key boundary: AL:2 cannot reach into AL:1 scope.

**DDR-4 — Aspirational peer ecosystems.**
hbl and osprey are not real repos yet. They MUST NOT appear in architecture diagrams as
established peers until they exist. They are recorded as `status: planned` in `projects.yaml` only.

**DDR-5 — Inter-repo reference mechanism.**
Repos reference each other by git tag pin or semver range declared in `compat:` fields.
Prose references in specs use schema URIs. No repo inherits from another — reference only.

---

## ECOSYSTEM PHASES

Each phase maps to one or more PASSes in `DEVPLAN.md`. Phase exit criteria must all be met
before the next phase begins. Per-repo implementation work happens inside each repo's own devpath.

---

### PASS-0 — Ecosystem Planning Baseline

**Goal:** Governance Commons has root planning infrastructure, authority model, and machine-readable
project registry. The five design decisions are answered and binding.

**Exit criteria:**

- DEVPATH.md, DEVPLAN.md, TRACKS.md, projects.yaml, tools/gc-status.ps1 all exist and are current
- Three source_102 design decisions answered and recorded (DDR-1 through DDR-5)
- tools/gc-status.ps1 runs against all sub-repos without errors
- All sub-repos listed in projects.yaml with correct group, status, and compat fields

**Status:** 🔄 In progress

---

### PASS-1 — Spec Correctness and Validation

**Goal:** All four specs meet a minimum public quality bar. Schemas validate their own examples.
Normative language is unambiguous. Stale documentation corrected. No spec contradicts its own schema.

**Exit criteria:**

- ONS: RFC 2119 normative language throughout; stale header fixed; conformance schema aligned
- ONS: cluster registration protocol defined and registry file exists
- Agent Dossier: package metadata present; JSON Schema validation wired into tooling; PASS ID enforced
- Agent Matrix: formal SLA/SLO schema; MCP alignment stub; multi-provider SKU fields
- APO: DevPath + Tracks reflect actual implementation state; level-2 escalation reachable; runtime-contract.yaml compiles deterministically
- All specs: valid and invalid test vectors exist for all schemas

**Status:** ⬜ Not started — begins after PASS-0 exits

---

### PASS-2 — Protocol, Security, and Identity Baseline

**Goal:** Move from document-level governance to protocol-aware, zero-trust governance.
Handoff envelopes are cryptographically signed. Agent identity has a cryptographic binding.
Major interoperability protocols (A2A, MCP, CloudEvents) have explicit governance positions.

**Exit criteria:**

- Handoff envelope signature schema defined (JWS/Ed25519)
- Agent identity binding spec defined (public key or DID-compatible reference)
- A2A binding: task lifecycle states, streaming, push notifications, auth headers documented
- MCP governance: tool scopes, trust levels, resource URI rules defined
- CloudEvents binding spec for lifecycle and audit events defined
- STRIDE-style threat model for multi-agent systems published
- Trust establishment, rotation, and revocation rules defined

**Status:** ⬜ Not started

---

### PASS-3 — Tooling, SDKs, and Packaging

**Goal:** Adoption does not require cloning repos and running scripts manually.
Validator packages are installable. CI integration is one file copy away.

**Exit criteria:**

- governance-commons-py published to PyPI
- governance-commons-js published to npm
- TypeScript reference implementation for ONS exists (prerequisite for VS Code extension)
- GitHub Actions validate-dossier.yml workflow template published
- Conformance report format defined (machine-readable pass/fail with spec version and rule IDs)
- CLI wrappers with stable command names for Python and TypeScript validators

**Status:** ⬜ Not started

---

### PASS-4 — Observability and Evidence

**Goal:** Governance events produce standard telemetry. Compliance evidence is machine-readable,
signed, and exportable to external audit systems.

**Exit criteria:**

- observability-contract.yaml defines gc.agent.* OTEL semantic conventions (span names for task start/handoff/escalation/completion, metric names, log body schema)
- Agent lifecycle events have a canonical structured event schema
- Tamper-evident audit log hash chaining spec defined
- Signed compliance evidence export format defined
- NIST AI RMF, EU AI Act, ISO 42001 control mappings produce machine-readable evidence artifacts
- Anomaly detection event categories defined

**Status:** ⬜ Not started

---

### PASS-5 — Public Release Train

**Goal:** Governance Commons ships as a coherent versioned ecosystem without collapsing
child repo autonomy. Release consumers can see exactly which spec versions are included.
Each child repo can still patch independently.

**Exit criteria:**

- Release train manifest format defined and used for GC v1.2.0 declaration
- GitHub org (governancecommons) created; all spec repos transferred or mirrored
- governancecommons.org live with ecosystem and per-standard pages
- GitHub Releases exist for all included spec versions
- RFC/proposal process documented and publicly accessible
- ADOPTERS.md and conformance badge criteria defined
- All included spec versions have release notes and migration notes

**Status:** ⬜ Not started

---

### PASS-6 — Category-Defining Profile

**Goal:** Ahead-of-curve features shipped as optional, versioned, testable profiles.
Baseline adopters are not forced into experimental features. Governance Commons has
demonstrable technical leadership beyond table-stakes compliance.

**Exit criteria (select three of the following to advance):**

- Federated Agent Trust Network protocol proposal published
- Constitutional governance layer (constitution.yaml) spec published
- Temporal authority window schema defined and validated
- Budget governance spec (cost-overrun → escalation) defined
- Governance diff and audit replay format defined
- Edge/offline governance profile defined
- ONS LSP prototype path documented

**Status:** ⬜ Not started

---

## GC-PASS REGISTRY

| GC-PASS | Description | Date | Status |
|---------|-------------|------|--------|
| GC-PASS-2026-0001 | Ecosystem planning infrastructure declared — PASS-0 bootstrap | 2026-06-05 | 🔄 |

---

*This file sets ecosystem structure and phase gates. Per-repo task execution lives in each repo's own devpath.*
*Do not add per-repo task tables here — update the relevant repo's planning docs instead.*
