# DEV-RELEASE — governance-commons

**AUTHORITY LEVEL: AL:2**
**Status:** Active — PASS-5 (Public Release Train)  
Created: 2026-06-09  
Authority: Owned by this repo. Sequencing and cross-repo dependencies defer to [`docs/DEV-RELEASE.md`](../docs/DEV-RELEASE.md).  
Relationship to DEV-PLAN: `DEV-PLAN.md` owns execution (tasks, PASSes, gap closure). This file owns release contracts — what ships externally, under what conditions, and what each release unlocks downstream.

---

## Current State Summary

**Active PASS:** PASS-5 (Public Release Train) — opened 2026-06-08  
**OSS baseline:** FROZEN as of PASS-5 Batch 2. No new baseline scope until public release is declared.  
**PASS-6 scope:** Optional category-defining profiles (constitutional governance, federated trust, temporal authority). May begin from frozen baseline in parallel with release mechanics.  
**Planned public release:** GC v1.2.0 (open question: rename to v1.0.0 for public clarity — maintainer decision required before Batch 4)

### What Is Already Spec-Complete (not open gaps)

All of the following are complete at spec/schema/test-vector level. The gap is publication and runtime enforcement:

| Area | Artifact | Status |
| --- | --- | --- |
| Handoff signing | JWS/Ed25519 signature block, `handoff-envelope-signature.schema.json` | spec-complete |
| Cryptographic agent identity | DID-compatible `identity_block.crypto_identity` | spec-complete |
| Zero-trust spec | `governance/zero-trust.yaml` (establishment, rotation, revocation) | spec-complete |
| STRIDE threat model | `governance/threat-model.md` — all 6 categories with mitigations | spec-complete |
| A2A binding | agent-matrix full 5/5 depth; 25 tests pass | spec-complete |
| CloudEvents binding | 5 event schemas; delivery/causality/idempotency/trace-context; 43 tests pass | spec-complete |
| MCP governance primitive | agent-matrix MCP tool scopes + server/client model | spec-complete |
| Streaming output schema | SSE/chunk envelope, sequence, backpressure | spec-complete |
| Prompt injection defense | Attack taxonomy, detection hook contract, rejection rules, test vectors | spec-complete |
| OTel semantic conventions | `docs/observability-contract.yaml` v1.0.0 — `gc.agent.*` span definitions, 12 rules | spec-complete |
| Structured event schema | `schemas/gc-agent-event.schema.json` — full lifecycle + security events | spec-complete |
| Tamper-evident audit log | SHA-256 hash chaining spec in observability-contract.yaml | spec-complete |
| Signed compliance evidence | `schemas/gc-compliance-evidence.schema.json` v1.0.0 — JWS EdDSA, control_frameworks | spec-complete |
| ISO 42001 mapping | `governance/iso-42001-mapping.yaml` v1.0.0 — Sections 4–10 + Annex A | spec-complete |
| NIST AI RMF mapping | `governance/nist-ai-rmf-mapping.yaml` v1.0.0 — all 4 functions, 22 subcategories | spec-complete |
| SOC 2 Type II mapping | `governance/soc2-mapping.yaml` v1.0.0 — CC1–CC9, A1.1–A1.3, C1.1–C1.2 | spec-complete |
| Transport binding | `governance/transport-binding.yaml` v1.0.0 — HTTP/2 SSE, WebSocket, gRPC, Kafka | spec-complete |
| Runtime agent registry | agent-matrix `agent_registry` cluster advertisement + discovery protocol | spec-complete |
| Agent revocation/expiry | `identity_block` revocation fields + dossier invalidation rules | spec-complete |
| Versioned capability claims | `identity_block.capability_claims[].declared_at` for audit replay | spec-complete |
| RFC process | `rfcs/RFC-PROCESS.md` + `rfcs/RFC-0000-template.md` | spec-complete |
| Conformance badge criteria | `docs/conformance/badge-criteria.md` — advisory/standard/strict per spec | spec-complete |
| Release train manifest | `schemas/gc-release-manifest.schema.json`; `releases/gc-v1.2.0.yaml` declared | spec-complete |
| PyPI publish workflow | `.github/workflows/publish-py.yml` — OIDC trusted publisher, triggered on `sdk-v*` tags | spec-complete |
| npm publish workflow | `.github/workflows/publish-js.yml` — npm provenance, triggered on `sdk-v*` tags | spec-complete |
| GitHub Actions CI template | `docs/templates/validate-dossier.yml` — adopter CI workflow | spec-complete |
| GitHub org | `governancecommons` org — all 11 repos transferred | spec-complete |
| Matrix overlays/profiles | Overlay fragments, named profiles (minimal, data-engineering), inheritance | spec-complete |
| Named workflow patterns | fan-out, pipeline, saga, critic-loop — versioned, reusable profiles | spec-complete |
| ONS v1.3.0 | RFC 2119 normative language, cluster registration, FAST rules, TypeScript impl | spec-complete |

---

## Release v1.2.0 — Public Release (GC v1.2.0 or v1.0.0)

**Status:** In progress — PASS-5 Batch 3/4 remaining  
**PASS:** PASS-5 (Public Release Train)  
**Open question:** Rename to v1.0.0 for public clarity? Maintainer decision required before Batch 4.  
**Blocker:** none structural — Osprey Strategic Holdings LLC has been live since 2026-06-15; the LLC-filing gate below is resolved.
**Current publication state (2026-10-06):** Public Python `governance-commons` is 0.2.0; public npm `governance-commons` is 0.1.1. Current SDK source is coordinated 0.2.0 and contains newer functionality than the published Python wheel. npm publication history has matching provenance attestations; the current workflow uses Trusted Publishing, so the old NPM_TOKEN setup note is superseded. Current publisher-account configuration is not independently asserted. A coordinated source release and clean published-artifact proof remain separate work.

### What ships

- Python `governance-commons` published to PyPI (GC-5-F-02)
- npm `governance-commons` published to npm (GC-5-F-03)
- GitHub Releases: agent-dossier v1.1.0, APO v1.1.0; release notes for all four v1.2.0 specs (GC-5-G-02)
- `gc-v1.2.0.yaml` status advanced from `planned` to `ready`; `pinned_version` populated for all four specs (GC-5-F-04)
- governancecommons.org live — per-standard pages, validator packages, conformance badge instructions (GC-5-G-03)
- OSS baseline freeze notice on website (GC-5-G-04)

### Spec pins (per release-train DDR-2)

```text
GC v1.2.0 = agent-dossier >=1.1.0 + agent-matrix >=1.3.0 + ONS >=1.2.0 + APO >=1.1.0
```

### Gap closures

- **Q2 Standards:** PyPI/npm with OIDC provenance (partial SLSA), signed releases — closes the `release-complete` gap on all spec-complete standards items
- **Q7 DevEx:** `pip install governance-commons` / `npm install governance-commons` — stranger install path open
- **Q9 Process:** RFC process and conformance badge publicly accessible on governancecommons.org
- **Q10 Docs:** governancecommons.org as the public entry point; "which repo do I need?" resolved by the site

### Admission criteria (all must be true before v1.2.0 ships)

- [x] LLC filing complete (unblocks GitHub Releases and PyPI/npm) — Osprey Strategic Holdings LLC live since 2026-06-15
- [ ] `gc-validate --spec ons` passes cleanly in CI on a fresh clone
- [ ] `gc-validate --spec dossier` passes cleanly in CI on a fresh clone
- [x] Python package `governance-commons` has published successfully via Trusted Publishing — public PyPI 0.2.0 and upload provenance verified 2026-10-06; this does not publish newer source changes
- [x] npm package `governance-commons` has a public published artifact with registry attestations — public version 0.1.1 verified 2026-10-06; coordinated SDK 0.2.0 publication remains open
- [ ] PyPI and npm packages install and run `gc-validate` on a clean machine (stranger test)
- [ ] governancecommons.org live with install instructions
- [x] Release-train notes are drafted in `releases/gc-v1.2.0-notes.md` and the four pinned spec releases are recorded in DEV-PLAN — verified 2026-10-06
- [ ] Versioning question resolved (v1.2.0 vs v1.0.0 public label)
- [x] `releases/gc-v1.2.0.yaml` status: `ready`; all four spec pins populated and compatibility holds empty — artifact verified 2026-10-06

### Downstream unlocks (what this release enables)

- eco and eco-edge can declare governance-commons as a versioned dependency
- eco-edge proof path can reference `gc-conformance-suite` by package version
- dxp-org installer can provision GC artifacts from PyPI/npm (not a repo clone)
- Adopters can self-declare conformance and appear in ADOPTERS.md

---

## Release v1.3.0 — Runtime Proof and Ecosystem Interop

**Status:** Planned — begins after v1.2.0 ships  
**PASS:** PASS-5 remainder + PASS-6 prep

### v1.3.0 Deliverables

- `gc-conformance-suite` packaged — fixtures across agent-dossier, agent-matrix, ONS, APO (for eco-edge proof path)
- Working examples against real MCP/CloudEvents tooling (not just schemas)
- Reference verifier service for signed evidence and audit chains
- GitHub Actions, Prometheus/Grafana, OIDC, LangChain/AutoGen/CrewAI integration examples
- PKI / key discovery / revocation propagation spec
- Operational runbooks: validator failure, compromised key, revoked agent, broken evidence chain
- Steering / WG structure established (prerequisite for enterprise procurement claims)

### Remaining open gaps (from DEV-PLAN gap checklist)

| Gap | ID | Priority | Notes |
| --- | --- | --- | --- |
| SLSA build provenance | 97-G15 | P3 | PASS-5; workflows exist; needs provenance attestation added |
| TypeScript + Go SDKs | 101-G5 | High | PASS-3; TypeScript ONS impl done; full SDK parity open |
| Orchestrator module split | 97-G10 | P2 | PASS-3; APO monolith not yet split |
| Plugin interface (no hardcoded require) | 97-G11 | P2 | PASS-3 |
| Machine-readable governance record schema | 100-N3 | Medium | PASS-4; partially addressed by GC-4-E-04 |
| Conformance certification mechanism (beyond self-declare) | 101-G6b | Medium | PASS-5; badge criteria exist; verifier registry needed |
| Global cluster registry as governed service | 100-N2 | Low-medium | PASS-5 |
| Multi-orchestrator topology spec | 98-G16 | Medium | PASS-6 |
| VALIDATOR_VERSION hardcoded | 100-T4 | Low | PASS-3 |

### Gap closures targeted

- **Q2 Standards:** SLSA Level 1+ provenance on all published packages
- **Q3 De Facto:** Working examples against real MCP/CloudEvents tooling
- **Q4 Best Practice:** Reference verifier service; PKI/key discovery/revocation
- **Q5 Security:** Revocation propagation and trust-anchor registry
- **Q6 Ops:** Operational runbooks for failure modes
- **Q8 Interop:** Integration examples for common stacks
- **Q9 Process:** Steering/WG established; conformance certification beyond self-declare
- **Q11 Testing:** `gc-conformance-suite` as a packaged, installable test artifact

### v1.3.0 Admission criteria

- [ ] `gc-conformance-suite` installable from PyPI/npm and runnable against any adopter repo
- [ ] Stranger can declare conformance end-to-end without asking anyone
- [ ] At least one working example against real MCP tooling (not schema only)
- [ ] Operational runbooks published on governancecommons.org
- [ ] Steering/WG structure declared in DEV-PLAN.md and visible on website

---

## Release v2.0.0 — Category Definition (PASS-6)

**Status:** Planned — scope open; begins from frozen OSS baseline after v1.2.0 ships  
**PASS:** PASS-6 (Category-Defining Profile)

### What ships (PASS-6 optional profiles)

- **Constitutional governance layer** (`constitution.yaml`) — inviolable rules cryptographically committed at project inception, above matrix and dossier. Maps to Constitutional AI research. No existing governance framework has this. (101-AC1 / GC-4-A-01)
- **Federated Agent Trust Network** — inter-org trust between agent matrices without sharing internal policy; SAML-federation analogy for agent capability claims. (101-AC2 / GC-4-B-01)
- **Temporal authority windows** — `authority_window` with absolute start/end, renewable intervals, quorum-required renewal for high-trust agents. (101-AC3 / GC-4-A-02)
- **Human-Agent Teaming Protocol** — formal spec for human principals entering/exiting agentic loops; decision authority tokens; escalation SLAs
- **LSP implementation for ONS** — no naming standard has ever shipped a Language Server Protocol; real-time validation in editors (100-N1 / GC-4-C-01)
- **Multi-orchestrator topology spec** (98-G16 / GC-4-B-02)

### Q12 picks

- **Constitutional governance layer** — the recommended category-defining feature for governance-commons v2.0.0
- **Federated trust network** and **temporal authority** as paired PASS-6 profiles

### v2.0.0 Admission criteria

- [ ] OSS baseline v1.2.0 is released and stable (no new baseline scope before this)
- [ ] Each v2.0.0 feature ships as an optional PASS-6 profile (not a baseline requirement)
- [ ] RFC filed and accepted (per RFC-PROCESS.md) for each normative change
- [ ] No fork; versioned at the GC release-manifest boundary (DDR-7)

---

## Cross-Repo Dependencies (outgoing)

| What ships | Version | Unlocks |
| --- | --- | --- |
| PyPI + npm packages | v1.2.0 | eco/eco-edge: declare GC as versioned dependency |
| gc-conformance-suite packaged | v1.3.0 | eco-edge: conformance reporting in proof path |
| Operational runbooks | v1.3.0 | eco-edge: can reference GC operational model |
| Steering/WG established | v1.3.0 | eco: can make enterprise procurement claims citing GC |
| SLSA provenance | v1.3.0 | eco: full standards compliance claim (Q2) |

---

## Gap Closure Verification

See [`docs/DEV-RELEASE.md`](../docs/DEV-RELEASE.md) for the shared four-condition verification principle.

`spec-complete` ≠ `release-complete`. The distinction that matters for this repo:  
Every item in the spec-complete table above is confirmed — the work is real. The gap is making it publicly installable, observable, and discoverable.

---

## Related Documents

- [`DEV-PLAN.md`](DEV-PLAN.md) — canonical execution plan; owns PASS state, tasks, gap closure tracking
- [`DEV-PATH.md`](DEV-PATH.md) — governance history, design decisions, authority model
- [`DEV-TRACKS.md`](DEV-TRACKS.md) — portfolio overview and track status
- [`docs/DEV-RELEASE.md`](../docs/DEV-RELEASE.md) — portfolio master, priority order, dependency graph
- [`docs/gap-analysis-framework.md`](../docs/gap-analysis-framework.md) — 12-question gap framework
- [`docs/sessions/2026-06-09-combined-synthesis.md`](../docs/sessions/2026-06-09-combined-synthesis.md) — synthesis source

## Release truth reconciliation — 2026-10-06

This file is the canonical GC release contract, selected by `C:\dev\projects.yaml` and the portfolio master `C:\dev\docs\DEV-RELEASE.md`. `dev-docs/governance-commons/DEV-RELEASE.md` is a retained historical copy; its obsolete LLC blocker and extra unchecked item do not create a second independent release obligation. It has not been overwritten or removed.

The four checkboxes above are repaired historical completion records, not a declaration that the current SDK source has shipped. Public package names are `governance-commons` in both registries, replacing the older descriptive `-py`/`-js` labels. PyPI latest is 0.2.0 (published August 19); npm latest is 0.1.1. SDK source metadata is coordinated 0.2.0, but the public registries are not coordinated at that version. Published Python 0.2.0 predates the current source; do not infer feature parity from matching version strings or attempt to overwrite that existing release.

Remaining release work: verify the exact release candidate in fresh-clone CI, test the actually published artifacts from a clean environment, restore/verify the website over valid HTTPS, resolve the ecosystem public version-label decision, and authorize an appropriately versioned coordinated SDK release. The current successful SDK cross-platform workflow is source/build proof, not evidence that current source was published. No release, version bump, tag, deployment or publication was performed by this reconciliation.

Website HTTPS verification failed in this environment. Earlier site-launch records are retained; current public availability/install instructions remain unverified, so that gate stays open.
