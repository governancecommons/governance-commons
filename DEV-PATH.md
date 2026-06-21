# DEV-PATH — Governance Commons Ecosystem Path

**AUTHORITY LEVEL: AL:2**
**Status:** ACTIVE
**Updated:** 2026-06-05

---

## CANONICAL DOC RULE

`DEV-PATH.md` owns: ecosystem phases, authority model, design decision record.
`DEV-PLAN.md` owns: current execution state, release train, compatibility matrix, gap checklist.

Sub-repo planning files (`agent-dossier/ROADMAP.md`, `agent-project-orchestrator/DevPath-v1.0.md`, etc.)
are **AL:1** — they govern their own repos and do not supersede this file.
This file does not contain per-repo task lists. It sets ecosystem structure and phase gates only.

---

## AUTHORITY MODEL

| Level | Scope | Who can change |
| --- | --- | --- |
| AL:3 | Ecosystem charter — inviolable invariants, licensing model, GC naming, **publish timing, public registry releases, tag creation that triggers publish workflows** | Founder only. Recorded as GC-CHARTER entries. |
| AL:2 | This file + DEV-PLAN — compatibility constraints, release milestones, design decisions, **PASS exit criteria, opening/closing PASSes, GC release milestone declarations** | GC project maintainer. Changes require a GC-PASS entry. |
| AL:1 | Individual repo devpaths — implementation, architecture, release cadence within a spec's scope | Spec owner, independently of ecosystem cadence. |

**Boundary rule:** AL:2 sets compatibility constraints and release milestones. It cannot dictate
implementation choices or release cadence inside any AL:1 repo devpath.

**Agent boundary rule:** Agents (human-assisted or autonomous) operating in this ecosystem are
bound by `governance/agent-constraints.yaml` (GC-CONSTRAINT-001). Key restrictions:

- Agents MUST NOT write or modify PASS exit criteria without maintainer sign-off (AL:2)
- Agents MUST NOT open or close a PASS gate without maintainer confirmation (AL:2)
- Agents MUST NOT publish to any public registry or create publish-triggering tags (AL:3)
- Agents MUST NOT record a DevPath/DevPlan decision as final without maintainer sign-off (AL:2)
- Agents proposing AL:2+ changes MUST flag them: `PROPOSED — requires AL:2 sign-off`
- When uncertain whether a change requires AL:2+ approval, agents MUST ask before writing

---

## PRODUCT CONTEXT

Governance Commons is the portable standards layer in a two-layer product stack:

```text
Governance Commons (governancecommons.org)
  Standards, schemas, specs, compliance mappings, audit contracts
  Portable across organizations and portfolios
        │
        ▼
DevX Control Plane (devx-control-plane)
  Registry, dashboard, planning templates, boundary doctrine, agent routing
  The operational layer developers clone and run
```

**GC without DCP** is a standard without an implementation — useful for enterprises and compliance, harder to adopt for solo developers and small teams.
**DCP without GC** is tooling without a standard underneath — useful but not defensible long-term.
**Together** they are a complete AI project governance stack.

### Product Tracks

There are two go-to-market tracks. Both draw from the same underlying stack.

**Starter track** — lightweight, public, adoption-focused. A simple `.governance/` folder structure with compatibility files for AGENTS.md, CLAUDE.md, Cursor rules, and Copilot instructions. Entry point for solo developers and small teams. Validates market demand. Builds brand.

**Full dev track** — the deep technical stack. Agent identity specs, zero-trust protocols, handoff envelopes, NIST/ISO compliance mappings, audit log chains, conformance reporting. Entry point for teams that need governed multi-agent infrastructure and compliance evidence.

The starter track is the doorway. The full dev track is the engine. They share the same brand and domain.

### OSS Core Baseline Freeze

Founder direction recorded 2026-06-09: the PASS-5 Batch 2 specification surface is the
open-source Governance Commons core baseline. From this point until the first public GC
release declaration, baseline work is limited to release polish, website publication,
schema/static asset publication, bug fixes, documentation corrections, compatibility cleanup,
and public release mechanics. New category-defining capability work belongs in PASS-6 as
optional profiles, not in the frozen OSS baseline.

This is a freeze, not a fork. Governance Commons remains the open standard core. Commercial
or paid-tier value should be implemented around optional PASS-6 profiles, hosted services,
developer tooling, evidence automation, managed registries, audit replay, policy packs, and
control-plane UX. Forking is deferred unless a future licensing, IP, or operational boundary
requires it.

---

## THREE DESIGN DECISIONS

Source 102 identified three decisions that determine whether multi-repo ecosystem architecture
works in practice. Answers are binding at AL:2. Full rationale in `DEV-PLAN.md`.

**DDR-1 — Version conflict handling.**
Specs declare `BREAKING:` + `breaking_consumers:` in their CHANGELOG when a breaking change
is proposed. The ecosystem DEV-PLAN records a coordinated update item. Downstream specs enter
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

**DDR-6 — Timestamp requirement.**
All governance artifacts — PASS records, handoff envelopes, telemetry events, registry entries,
governance documents, and agent-produced scaffolding or implementation outputs — MUST carry a
machine-readable timestamp at the point of creation or emission. No governance artifact is
audit-complete without a timestamp. Timestamps MUST use ISO 8601 / RFC3339 UTC
(`YYYY-MM-DDTHH:MM:SSZ`). This is an AL:2 requirement effective 2026-06-06. The requirement is
implemented across five layers, each scoped to the PASS where it becomes enforceable.

**Canonical field naming (per ONS separator semantics):**

- Document level: `time.loc:` (colon-qualified key, human-readable metadata block)
- Schema level: `*_at` suffix — `created_at`, `emitted_at`, `accepted_at`, `authored_at`
- Telemetry level: `timestamp` (existing field in telemetry_trace_schema) + `time_loc` key in APO telemetry.emit() calls

**Five-layer implementation scope:**

| Layer | Artifact / system | Required field(s) | PASS | Gap / item |
| --- | --- | --- | --- | --- |
| L1 | DEV-PLAN, DEV-PATH, registry files, ONS CHANGELOG entries | `time.loc:` header field | PASS-0 — done | Convention |
| L2 | agent-dossier handoff envelopes; telemetry lifecycle events | `emitted_at` (REQUIRED), `accepted_at` (OPTIONAL); event types: `pass_written`, `scaffold_started`, `scaffold_completed`, `implementation_started`, `implementation_completed`, `doc_written`, `registry_updated` | PASS-1 | GC-1-A-TL-01, GC-1-A-TL-02 |
| L3 | observability-contract.yaml gc.agent.* event schema | `time_loc` required field on every gc.agent.* event | PASS-4 | GC-3-E-01 (existing) |
| L4 | agent-project-orchestrator telemetry.emit() | `time_loc` required key in every emit call; runtime validation rejects emission without it | PASS-2 | GC-1-D-TL-01 |
| L5 | GC release milestone review gate | All specs in the milestone declare timestamp conformance at their declared profile level | PASS-0 — this DDR | AL:2 rule |

**DDR-7 — OSS baseline freeze, version boundary, and fork posture.**
The PASS-5 Batch 2 surface is the frozen OSS core baseline for the first public Governance
Commons release. PASS-5 completion work may prepare and publish that baseline, but MUST NOT
add new baseline scope. Versioning should happen at the GC release-manifest boundary soon;
forking should not happen now. PASS-6 is the proper home for optional category-defining
profiles and commercial-capability implementation paths.

---

## ECOSYSTEM PHASES

Each phase maps to one or more PASSes in `DEV-PLAN.md`. Phase exit criteria must all be met
before the next phase begins. Per-repo implementation work happens inside each repo's own devpath.

---

### PASS-0 — Ecosystem Planning Baseline

**Goal:** Governance Commons has root planning infrastructure, authority model, and machine-readable
project registry. The five design decisions are answered and binding.

**Exit criteria:**

- DEV-PATH.md, DEV-PLAN.md, TRACKS.md, projects.yaml, tools/gc-status.ps1 all exist and are current
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
- Agent Dossier: handoff envelope `emitted_at` field (REQUIRED) and `accepted_at` field (OPTIONAL) defined in spec and schema — Layer 2 timestamp requirement (DDR-6)
- Agent Dossier: telemetry_trace_schema extended with lifecycle event types: `pass_written`, `scaffold_started`, `scaffold_completed`, `implementation_started`, `implementation_completed`, `doc_written`, `registry_updated` — Layer 2 timestamp requirement (DDR-6)
- Agent Matrix: formal SLA/SLO schema; MCP alignment stub; multi-provider SKU fields
- APO: DevPath + Tracks reflect actual implementation state; level-2 escalation reachable; runtime-contract.yaml compiles deterministically
- All specs: valid and invalid test vectors exist for all schemas

**Status:** ✅ COMPLETE — gate review passed 2026-06-07 (GC-PASS-0002.00). All eight exit criteria met. Minor note: agent-matrix lacks invalid test vectors — deferred to PASS-3 tooling work, not blocking.

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
- APO runtime: `time_loc` is a required key in every `telemetry.emit()` call; runtime rejects emission without it — Layer 4 timestamp requirement (DDR-6, gap GC-1-D-TL-01)

**Status:** ✅ COMPLETE — gate review passed 2026-06-07 (GC-PASS-0012.00). All 8 exit criteria met.

---

### PASS-3 — Tooling, SDKs, and Packaging

**Goal:** Adoption does not require cloning repos and running scripts manually.
Validator packages are installable. CI integration is one file copy away.

**Exit criteria:**

- governance-commons-py package builds clean (sdist + wheel), passes twine check, publish workflow in place
- governance-commons-js package builds clean (ESM + CJS + types), passes npm pack, publish workflow in place
- TypeScript reference implementation for ONS exists (prerequisite for VS Code extension)
- GitHub Actions validate-dossier.yml workflow template exists and is usable by adopters
- Conformance report format defined (machine-readable pass/fail with spec version and rule IDs)
- CLI wrappers with stable command names for Python and TypeScript validators

Note: actual registry publish (PyPI + npm) is a PASS-5 exit criterion, not PASS-3.

**Status:** ✅ COMPLETE — gate review passed 2026-06-08 (GC-PASS-0013.00). All 6 exit criteria met.

---

### PASS-4 — Observability and Evidence

**Goal:** Governance events produce standard telemetry. Compliance evidence is machine-readable,
signed, and exportable to external audit systems.

**Exit criteria:**

- observability-contract.yaml defines gc.agent.* OTEL semantic conventions (span names for task start/handoff/escalation/completion, metric names, log body schema)
- observability-contract.yaml: all gc.agent.* events carry mandatory `time_loc` field; canonical lifecycle event types (`gc.agent.pass.written`, `gc.agent.scaffold.started`, `gc.agent.scaffold.completed`, `gc.agent.implementation.started`, `gc.agent.implementation.completed`, `gc.agent.doc.written`, `gc.agent.registry.updated`) are defined with required fields — Layer 3 timestamp requirement (DDR-6, gap GC-3-E-01)
- Agent lifecycle events have a canonical structured event schema
- Tamper-evident audit log hash chaining spec defined
- Signed compliance evidence export format defined
- NIST AI RMF, EU AI Act, ISO 42001 control mappings produce machine-readable evidence artifacts
- Anomaly detection event categories defined

**Status:** ✅ COMPLETE — gate review passed 2026-06-08 (GC-PASS-0015.00). All 7 exit criteria met. Note: EU AI Act coverage satisfied via `control_frameworks` reference in `schemas/gc-compliance-evidence.schema.json` (GC-4-E-04); standalone mapping deferred to PASS-5 or later.

---

### PASS-5 — Public Release Train

**Goal:** Governance Commons ships as a coherent versioned ecosystem without collapsing
child repo autonomy. Release consumers can see exactly which spec versions are included.
Each child repo can still patch independently.

**Exit criteria:**

- governance-commons-py published to PyPI (moved from PASS-3)
- governance-commons-js published to npm (moved from PASS-3)
- Release train manifest format defined and used for GC v1.2.0 declaration
- GitHub org (governancecommons) created; all spec repos transferred or mirrored
- governancecommons.org live with ecosystem and per-standard pages
- GitHub Releases exist for all included spec versions
- RFC/proposal process documented and publicly accessible
- ADOPTERS.md and conformance badge criteria defined
- All included spec versions have release notes and migration notes

**Status:** 🔵 OPEN — PASS-4 gate review GC-PASS-0015.00 cleared on 2026-06-08

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
| --- | --- | --- | --- |
| GC-PASS-0001.00 | Ecosystem planning infrastructure declared — PASS-0 bootstrap | 2026-06-05 | 🔄 |
| GC-PASS-0002.00 | PASS-1 gate review — all 8 exit criteria passed; PASS-2 open | 2026-06-07 | ✅ |
| GC-PASS-0012.00 | PASS-2 gate review — all 8 exit criteria met; PASS-3 open | 2026-06-07 | ✅ |
| GC-PASS-0013.00 | PASS-3 gate review — all 6 exit criteria met; PASS-4 open | 2026-06-08 | ✅ |
| GC-PASS-0014.00 | GC-CONSTRAINT-001 — agent authority constraints registered; DEV-PATH authority model strengthened | 2026-06-08 | ✅ |
| GC-PASS-0015.00 | PASS-4 gate review — all 7 exit criteria met; PASS-5 open | 2026-06-08 | ✅ |

---

*This file sets ecosystem structure and phase gates. Per-repo task execution lives in each repo's own devpath.*

---

## INDUSTRY GAP ANALYSIS — Governance Commons

**Framework:** 12-question gap analysis (c:\dev\docs\gap-analysis-framework.md v1.1)
**Applied:** 2026-06-16
**Scope:** Governance Commons as an AI agent governance standards ecosystem
**Gap states:** `open` | `spec-complete` | `release-complete` | `runtime-complete`

A gap is not closed until: (1) mechanism exists, (2) it is tested, (3) it is observable, (4) it is discoverable.

---

| Q | Area | Priority | Gap | Status | Suggested Action |
| --- | --- | --- | --- | --- | --- |
| Q1 | Regulatory | High | EU AI Act (Aug 2, 2026) not a release gate; GDPR data subject rights not modeled; CO ADMT 2027 not addressed | open | Add jurisdiction profiles to PASS-6: EU AI Act, GDPR, CO ADMT 2027, CA/NY transparency |
| Q2 | Standards | High | SLSA provenance and SBOM open; ISO 42001 + NIST AI RMF + SOC 2 mapped but not published as release artifacts | spec-complete | Finish SLSA provenance, SBOM, release attestations for all published packages |
| Q3 | De Facto | Medium | MCP/A2A/CloudEvents specified and tested; no external adoption proof running against real tooling | spec-complete | Publish examples running against real MCP/CloudEvents tooling, not just schemas |
| Q4 | Best Practice | Medium | Strong schemas/test vectors; no live reference verifier service for signed evidence and audit chains | spec-complete | Build reference verifier service for signed evidence, conformance, audit chains |
| Q5 | Security | High | STRIDE, zero-trust, JWS/Ed25519, revocation defined; PKI key discovery and federated trust immature | spec-complete | Define key discovery, revocation propagation, trust-anchor registry |
| Q6 | Ops | Medium | Governance of operations exists; no public runbooks for validator failure, compromised key, revoked agent | open | Add runbooks for validator failure, compromised key, revoked agent, broken evidence chain |
| Q7 | DevEx | High | SDK exists locally; PyPI/npm publish and first-user install path still open | open | Finish PyPI/npm publish and 5-minute governed-agent example (PASS-5 Batch 4) |
| Q8 | Interop | Medium | Good protocol coverage; no "works with your stack" proof for LangChain, AutoGen, OIDC, GitHub Actions | open | Add GitHub Actions, Prometheus/Grafana, OIDC, LangChain/AutoGen examples |
| Q9 | Process | Medium | RFC and conformance exist; no steering/WG structure established; no named community roles | open | Define community governance roles (Maintainer, Contributor, RFC sponsor) before enterprise adoption claims — these are stewardship roles for the spec community, not product runtime roles; GC has no runtime surface. Required for PASS-5. |
| Q10 | Docs | Medium | Improved; nested spec repos confuse newcomers; no ecosystem map | open | Add ecosystem map and "which repo do I need?" guide |
| Q11 | Testing | Medium | ONS/matrix/SDK have tests; cross-spec conformance suite not packaged | open | Create `gc-conformance-suite` with fixtures across dossier, matrix, ONS, APO |
| Q12 | Ahead | High | Best-positioned repo for category-defining work — constitutional governance, federated trust, temporal authority, audit replay | open | Prioritize constitutional governance layer and audit replay as first PASS-6 optional profiles |

### Doc Vault / DVP additions (2026-06-16)

| Q | Area | Priority | Gap | Status |
| --- | --- | --- | --- | --- |
| Q1 | Regulatory | Medium | ISO 15489, ARMA GARP aligned but no jurisdiction-specific retention law mapping (IRS 7-year, SOX, HIPAA) | open |
| Q2 | Standards | Medium | doc-vault standards-map.md covers alignment; no formal conformance schema for doc vault profile | open |
| Q3 | De Facto | Medium | No integration with OneDrive, Google Drive, Dropbox — where actual business docs live | open |
| Q7 | DevEx | High | DVP installer does not exist yet; adoption requires manual setup | open |
| Q12 | Ahead | High | `.governance/` as machine-readable business constitution — no product owns this space yet | open |

*Do not add per-repo task tables here — update the relevant repo's planning docs instead.*
