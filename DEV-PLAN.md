# DEV-PLAN — Governance Commons Execution Plan

**AUTHORITY LEVEL: AL:2**
**Status:** ACTIVE — canonical execution and release planning source
**time.loc:** 2026-06-09T00:00:00Z
**Canonical pair:** `DEV-PATH.md` + `DEV-PLAN.md`

---

## CANONICAL DOC RULE

There are exactly two root planning documents for Governance Commons:

1. `DEV-PATH.md` — history and governance path. Owns phase/PASS registry, design decision record, authority model, agent onboarding.
2. `DEV-PLAN.md` — current execution plan. Owns active priorities, release train status, compatibility matrix, and gap closure tracking.

All other devpath/devplan files under this directory are non-canonical unless they explicitly redirect here.
Sub-repo planning files (e.g., `agent-dossier/ROADMAP.md`) are AL:1 and do not supersede this file.

---

## CURRENT EXECUTION POSITION

**Current state (reconciled 2026-09-30):** PASS-5's original release/site checklist is substantially superseded by the live v1.2.0 baseline and the RFC-0001 public-boundary transition. A7 and Phase B cross-spec reconciliation are CLOSED.
**Active governance decision:** RFC-0001 — Governance Commons Public Boundary Model (**accepted 2026-10-01** by Jesse Ervin, documented maintainer).
**GC v1.2.0:** release-train manifest is PLANNED with explicit Dossier/Matrix compatibility and historical review-provenance holds (readiness withdrawn 2026-10-07). Original pins and readiness timestamp are retained. Python package publication is complete; npm publication remains a separately verified release gate.
**Next execution objective:** implement A-1–A-5 → verify G-1–G-5 → activate the public boundary. RFC-0001 acceptance is CLOSED. Do not reopen A7/Phase B unless a concrete defect is found.
**Strategic checkpoint:** Before opening a new broad GC capability track, validate whether GC should remain a standalone agent-governance standards umbrella versus narrowing to a differentiated interoperability/evidence layer or contributing mature artifacts to an existing ecosystem.
**OSS baseline:** FROZEN. New category-defining capability is not automatically authorized merely because PASS-6 exists.
**Product path:** standards + reference tooling + publication infrastructure; adoption must be earned by a small, independently useful entry point rather than assumed from the umbrella.


### RFC-0001 ACCEPTANCE — 2026-10-01

- **RFC:** RFC-0001 — Governance Commons Public Boundary Model
- **Decision:** ACCEPTED
- **Maintainer:** Jesse Ervin — documented Governance Commons maintainer
- **Review mode:** Maintainer review under `rfcs/RFC-PROCESS.md`
- **Review record:** `rfcs/RFC-0001-maintainer-review.md` and Section 8 of the RFC
- **Effect:** A-1 through A-5 implementation is authorized.
- **Activation:** NOT YET ACTIVE. G-1 through G-5 remain the public-boundary activation gate.
- **Compat-hold:** REQUIRED under DDR-1 until the named consumers confirm compatibility.
- **Review finding:** No unresolved substantive objection was identified. External ecosystem claims were refreshed against primary sources before acceptance.


## SEPTEMBER 2026 CURRENT-STATE RECONCILIATION

**Reconciliation date:** 2026-09-30  
**Authority:** live GitHub state, release manifest, release/site commits, RFC-0001, and completed A7/Phase B commits.

### Closed
- **A7 — delegation lifecycle / revocation evidence:** CLOSED. Registry implementation and verification runs passed.
- **Phase B — ecosystem/cross-spec reconciliation:** CLOSED. Final reconciliation landed 2026-09-17.
- **GC v1.2.0 baseline publication:** website baseline/freeze notice published 2026-09-17.
- **GC v1.2.0 release manifest:** READY with all four pinned components compatible and no compat-hold items.
- **Registry SDK publication workflow:** npm publication was moved to trusted publishing; the resulting workflow runs are green. Actual package publication remains a separate observable gate and must not be inferred from CI success.

### Reclassified / stale planning corrected
- Old PASS-5 wording that treated the website as not live is stale; the live site baseline was published 2026-09-17.
- Old PASS-5 wording that treated the npm gate as permanently blocked on NPM_TOKEN is stale; the workflow was changed to npm trusted publishing on 2026-09-18.
- The old “PASS-5 close-out → v1.2.0 declaration → PASS-6” sequence is no longer the controlling next-step chain. RFC-0001 is now the active governance decision.

### Remaining actual gates
1. **RFC-0001 acceptance decision** — human governance decision.
2. **A-1 through A-5 implementation** — only after acceptance.
3. **G-1 through G-5 activation gate** — verify canonical schemas, licensing, ONS version identity, public website family, and Agent Matrix compatibility.
4. **Independent adoption evidence** — not a release gate, but the strategic gate for deciding whether GC should expand as a standalone ecosystem.
5. **Package/public distribution verification** — verify npm artifact publication independently of workflow success.

### Strategic note
The original PASS-6 document-vault/profile direction remains a product exploration, not an automatic continuation of the GC standards roadmap. It should not be expanded into another large implementation program until there is a clear adoption wedge and evidence that the work is differentiated from existing agent-governance efforts.

**Recently completed:**

- DEV-ACCORD.11 — Compound PASS Operating Rhythm Hardening (2026-07-01, GC-PASS-0018.00): DEV-ACCORD.06 amended with a compound-PASS-default trigger table, a required compound PASS brief that must be human-confirmed before any file edit, next-recommended-step classification (Compound PASS / Single PASS / DRIVE / RUN / BUNT / Blocked), and a release/evidence-review threshold (compound-PASS close, release-gate change, or explicit request only). CI-36 through CI-38 added. `PLAY-OBLIGATIONS.md` and `CONTRACTS.md` updated.
- DEV-PLAYBOOK amendment (2026-07-01, DEV-ACCORD.06): PLAY.jsonl schema locked (status, declared_at, time_loc, authorized_by, authorization_note, scope, touches, 5 timing categories, dev_docs_check, commit_ref, preflight); CI-30 through CI-32 declared; `validate-playbook.ps1` and provider-based `validate-format.ps1` registered in GC-AUDIT-REGISTRY.yaml and wired into `validate-recent-work.ps1` Level 1; Level 1 runs playbook validation when PLAY.jsonl exists and skips cleanly when absent; `gc-audit/PLAY-OBLIGATIONS.md` updated to point to the amendment as schema authority.
- GC-AUDIT caller contract closure (2026-07-01): PLAY records now have `schemas/gc-play-record.schema.json`; `validate-playbook.ps1 -Json` emits `gc-audit.result.v1`; per-level `validation_profile` checks are enforced for BUNT/RUN/DRIVE/PASS; normalization reports have `schemas/gc-audit-normalize-report.schema.json`; evidence principals have `schemas/gc-evidence-principal.schema.json`; `gc-audit/CONTRACTS.md` added for Cockpit/Marlin/DCP callers.
- Universal PLAY closeout rule (2026-07-01, DEV-ACCORD.06): all GC-conformant agents/environments/platforms must include PLAY telemetry, latest PLAY summary, and next recommended step after every PLAY; CI-33 through CI-35 added.
- OSS core baseline freeze decision recorded (2026-06-09): PASS-5 Batch 2 is the frozen open-source baseline for the first public GC release; no new baseline scope before release close-out; PASS-6 owns optional category-defining profiles and commercial-capability paths; forking deferred.
- PASS-4 gate review passed (2026-06-08, GC-PASS-0015.00): all 7 exit criteria met; PASS-5 open. EU AI Act coverage satisfied via `control_frameworks` reference in `schemas/gc-compliance-evidence.schema.json`.
- GC-3-E-03 closed (2026-06-08): `governance/iso-42001-mapping.yaml` v1.0.0 — ISO/IEC 42001:2023 AIMS full mapping; Sections 4–10 + Annex A controls A.2–A.10; coverage levels (full/partial/planned/out_of_scope); all GC artifacts cross-referenced per clause
- GC-3-E-02 closed (2026-06-08): `governance/nist-ai-rmf-mapping.yaml` v1.0.0 — NIST AI RMF 1.0 full mapping; all four functions (GOVERN, MAP, MEASURE, MANAGE); 22 subcategory outcomes mapped to GC artifacts; coverage levels and gap notes included
- GC-4-E-02 closed (2026-06-08): tamper-evident audit log hash chaining — `audit_log_chain` section in `docs/observability-contract.yaml` (SHA-256 canonical serialization spec, verification algorithm, 5 compliance rules chain-1 through chain-5); `gc_chain_id`, `gc_chain_seq`, `gc_prev_event_hash` fields added to `schemas/gc-agent-event.schema.json`
- GC-4-E-03 closed (2026-06-08): security and anomaly detection event categories — `security_events` section in `docs/observability-contract.yaml` (5 new spans: gc.agent.anomaly.detected, policy.violation, constraint.breach, auth.failure, chain.integrity_failure; 5 compliance rules sec-1 through sec-5); 5 new `gc_event_type` enum values and security-specific fields added to `schemas/gc-agent-event.schema.json`
- GC-4-E-04 closed (2026-06-08): signed compliance evidence export — `schemas/gc-compliance-evidence.schema.json` v1.0.0 — bundle_id, evidence_period, control_frameworks (NIST-AI-RMF/ISO-42001/SOC2/EU-AI-Act), events array, bundle_hash (SHA-256 canonical), JWS EdDSA signature block; chain_verified flag; allOf conditional for chain integrity requirement
- GC-3-E-01 closed (2026-06-08): observability-contract.yaml v1.0.0 — 7 canonical lifecycle span definitions with required fields, structured event schema (schemas/gc-agent-event.schema.json), 12 compliance rules, DDR-6 Layer 3 enforcement; JSON Schema validates correctly
- GC-CONSTRAINT-001 registered (2026-06-08, GC-PASS-0014.00): agent authority constraints — prohibited actions (AC-001 through AC-007), proposal protocol, and remediation rules; DEV-PATH authority model strengthened with agent boundary rule
- PASS-3 gate review passed (2026-06-08, GC-PASS-0013.00): all 6 exit criteria met; PASS-4 open
- PASS-2 gate review passed (2026-06-07, GC-PASS-0012.00): all 8 exit criteria met; PASS-3 open
- PASS-2 Batch 4 closed (2026-06-07, PASS-2026-0011): GC-3-B-04 (streaming output SECTION 15B, 33 tests), GC-3-B-05 (prompt injection defense SECTION 16B, 37 tests); 70/70 pass
- PASS-2 Batch 3 closed (2026-06-07, PASS-2026-0010): GC-3-B-02 (A2A 5/5), GC-3-B-03 (CloudEvents 5/5, 5 event schemas, 68 tests)
- PASS-2 Batch 2 closed (2026-06-07, GC-PASS-0005.00): GC-3-A-03 (zero-trust spec — establishment, rotation, revocation)
- PASS-2 Batch 1 closed (2026-06-07, GC-PASS-0004.00): GC-3-A-01 (handoff JWS/Ed25519 signature), GC-3-A-02 (DID-compatible crypto_identity), GC-3-B-06 (STRIDE threat model)
- Source 97–102 gap analysis series read and synthesized
- Three source_102 design decisions answered in DEV-PATH.md (DDR-1 through DDR-5)
- Ecosystem planning infrastructure created (DEV-PATH, DEV-PLAN, TRACKS, projects.yaml, tools/gc-status.ps1)
- agent-project-orchestrator renamed from project-orchestrator-agent and pushed to governancecommons/agent-project-orchestrator
- Track Alpha, Charlie, and Delta P0 gap closure reconciled across source gap checklist and project registry
- GC-1-D-04 through GC-1-D-08: APO P1 runtime correctness batch (telemetry, typed tasks, handoff envelopes, tests)
- GC-1-D-10 / GC-1-D-11: APO PASS-2 runtime governance loading + per-agent resource budget enforcement
- GC-1-C-05: ONS cluster registration protocol defined (PASS-2026-0008) + registry/clusters.yaml created (PASS-2026-0009)
- DDR-6: AL:2 timestamp requirement established; 5-layer implementation scope written into DEV-PLAN, DEV-PATH, agent-dossier spec, and handoff-envelope schema

**PASS-1 completed tasks (all closed):**

All 19 PASS-1 immediate tasks closed. See CHANGELOG entries PASS-2026-0004 through PASS-2026-0014 across agent-dossier, agent-matrix, ONS, APO, and ATP repos.

---

**PASS-2 immediate next tasks (Batch 1 — parallel):** ✅ CLOSED 2026-06-07 (GC-PASS-0004.00)

1. ~~GC-3-A-01~~ — agent-dossier: handoff envelope JWS/Ed25519 signature schema — DONE: `signature_block` in spec + `handoff-envelope-signature.schema.json` + `handoff-envelope.schema.json` updated + valid/invalid examples
2. ~~GC-3-A-02~~ — agent-dossier: agent identity DID-compatible binding — DONE: `identity_block.crypto_identity` (did / public_key) in spec + `agent-dossier-instance.schema.json` updated + examples
3. ~~GC-3-B-06~~ — governance-commons root: STRIDE threat model — DONE: `governance/threat-model.md` covering all 6 STRIDE categories with mitigations; cross-references multi-agent.yaml T-001–T-006

**PASS-2 Batch 2:** ✅ CLOSED 2026-06-07 (GC-PASS-0005.00)

1. ~~GC-3-A-03~~ — governance-commons root: zero-trust spec — DONE: `governance/zero-trust.yaml` — establishment (4-phase), rotation (7-step + dual-sign transition), revocation (6-step, 5 triggers), key material rules, conformance profiles, residual risks

**PASS-2 Batch 3 (parallel):** ✅ CLOSED 2026-06-07 (PASS-2026-0010 in agent-matrix)

1. ~~GC-3-B-02~~ — A2A binding 5/5 — DONE: task_payload, capability_negotiation (6-step), peer_trust_anchor (5-step + gcdossierref), resource_uri_scheme (4 patterns), error_retry_semantics (3 classes, 10 codes, retry_policy), sla_timeout_enforcement; 25 tests pass
2. ~~GC-3-B-03~~ — CloudEvents binding 5/5 — DONE: delivery_semantics (at-least-once), ordering_causality (gcparentid, gcsequence, no-cycle), trace_context (W3C traceparent, strict-profile), idempotency (86400s dedup, trace_id:event_id key); 5 event schemas in schemas/events/; 43 event tests pass

**PASS-2 Batch 4 (parallel) — CLOSED 2026-06-07 (PASS-2026-0011):**

1. GC-3-B-05 — agent-matrix: prompt injection defense spec — attack taxonomy (direct, indirect, jailbreak), detection hook contract, rejection rules, audit obligations; feeds into STRIDE model — **C**
2. GC-3-B-04 — agent-matrix: streaming output schema — SSE/chunk envelope, sequence numbering, terminal chunk marker, backpressure signal — **C**

---

**PASS-3 Batch 1 (parallel) — CLOSED 2026-06-07:**

1. GC-2-C-01 — governance-commons root: conformance report format — machine-readable pass/fail document (JSON/YAML) carrying spec name, spec version, rule IDs evaluated, per-rule result (pass/fail/skip), and overall conformance level; used as the output contract for both Python and TypeScript validators — **C**
2. GC-2-A-04 — governance-commons-py + governance-commons-js: CLI wrappers — stable command names (`gc-validate`, `gc-report`) with `--spec`, `--profile`, `--output` flags; output conforms to GC-2-C-01 report format; entry points wired into package.json and pyproject.toml — **C**

**PASS-3 Batch 2 (parallel) — CLOSED 2026-06-07:**

1. GC-2-E-01 — governance-commons-py: PyPI publish infrastructure — `python -m build` produces sdist + wheel; `twine check` passes; OIDC trusted publisher workflow at `.github/workflows/publish-py.yml`; triggered on `sdk-v*` tags — **C**
2. GC-2-E-02 — governance-commons-js: npm publish infrastructure — `npm run build` produces ESM + CJS + types dist; `npm pack --dry-run` passes; npm provenance workflow at `.github/workflows/publish-js.yml`; triggered on `sdk-v*` tags — **C**
3. GC-CI-01 — governance-commons root: `validate-dossier.yml` GitHub Actions template for adopters — `docs/templates/validate-dossier.yml`; runs `gc-validate --spec ons`, uploads ConformanceReport artifact, includes commented agent-dossier stub — **C**

---

**PASS-5 Batch 1 (parallel) — immediate next tasks:**

1. ~~GC-5-F-01~~ — Release train manifest format — DONE: `schemas/gc-release-manifest.schema.json` v1.0.0 (status lifecycle planned→ready→deprecated; pinning contract with compat-hold enforcement); `releases/gc-v1.2.0.yaml` declared (status advanced to `ready` 2026-06-17, ahead of registry publish + GC-5-G-02 — see GC-5-F-04 below) — **C**
2. ~~GC-5-G-01~~ — GitHub org (governancecommons) — DONE: org exists; all 11 repos transferred (agent-dossier, agent-matrix, ons, agent-project-orchestrator, agent-team-protocol, governance-commons, governance-commons-registry, agent-roster, agent-dossier-www, governance-commons-www, governance-commons-vscode) — **C** _(governance-commons-sdk renamed to governance-commons-registry 2026-07-11)_
3. ~~GC-5-H-01~~ — RFC process — DONE: `rfcs/RFC-PROCESS.md` (lifecycle, numbering, required sections, proportional review, acceptance/rejection rules) + `rfcs/RFC-0000-template.md` (all required sections pre-scaffolded). Fixed two-week delay replaced by explicit maintainer correction on 2026-08-29; no universal minimum now applies. — **C**
4. ~~GC-5-H-02~~ — `ADOPTERS.md` + conformance badge criteria — DONE: `ADOPTERS.md` (self-declaration format, adopter table, profile summary); `docs/conformance/badge-criteria.md` (per-spec criteria for advisory/standard/strict, shields.io badge patterns, declaration process) — **C**

**PASS-5 Batch 2 — Spec completion (prerequisite for end-game; parallel within batch):**

These deferred gaps MUST be closed before the end-game publish sequence. They complete the
spec surface required for a credible v1.0 public release.

1. ~~101-G1c~~ — Transport binding spec: HTTP/2 SSE, WebSocket, gRPC, and Kafka governance positions; delivery guarantees, backpressure, and session lifecycle rules per transport — DONE: `governance/transport-binding.yaml` v1.0.0 — **C**
2. ~~101-G4c~~ — SOC 2 Type II mapping: machine-readable control mapping for Trust Services Criteria (Security, Availability, Confidentiality); coverage levels and GC artifact cross-references — DONE: `governance/soc2-mapping.yaml` v1.0.0 — Security Common Criteria (CC1–CC9), Availability (A1.1–A1.3), Confidentiality (C1.1–C1.2), coverage levels and GC artifact cross-references — **C**
3. ~~98-G9~~ — Runtime agent discovery registry: ONS cluster-based agent advertisement and discovery protocol; requires ONS cluster infra (GC-1-C-05 ✅) — DONE: agent-matrix `agent_registry` cluster_advertisement + discovery_protocol; `schemas/sections/agent-registry.schema.json`; tests — **C**
4. ~~97-G7~~ — OTel migration in APO: replace custom telemetry with OpenTelemetry SDK calls; `time_loc` key maps to OTel span attribute; existing `telemetry.emit()` interface preserved as thin wrapper — DONE: APO `orchestrator/telemetry.py` uses OpenTelemetry SDK spans and preserves JSON audit log — **C**
5. ~~98-G15~~ — Named workflow pattern library: canonical workflow patterns (fan-out, pipeline, saga, critic-loop, etc.) defined as named, versioned, reusable profiles in agent-matrix — DONE: agent-matrix `workflow_patterns` + `schemas/sections/workflow-patterns.schema.json`; tests — **C**
6. ~~101-G7b~~ — Versioned capability claims for audit replay: agent capability declarations carry a `declared_at` version stamp so audit replays can reconstruct the capability state at the time of any task — DONE: `agent-dossier/agent-dossier.yaml` v1.4.0 `identity_block.capability_claims[]`; `agent-dossier/schemas/agent-dossier-instance.schema.json` validates required `declared_at`; valid and invalid fixtures added — **C**

**PASS-5 Batch 3 (parallel — after Batch 2):**

1. ~~GC-5-G-02~~ — GitHub Releases: create tagged releases for agent-dossier v1.1.0 and APO v1.1.0; release notes for all four v1.2.0 specs — DONE: GitHub Releases with substantive release notes exist for all four v1.2.0-pinned specs — agent-dossier v1.1.0 (published 2026-06-18), agent-matrix v1.4.0 (published 2026-06-09), ons v1.2.0 + v1.3.0 (published 2026-06-09), agent-project-orchestrator v1.1.0 (published 2026-06-18). This row had gone stale against the actual GitHub state (never updated after the releases were cut); verified live via `gh release list`/`gh release view` 2026-08-10 — **C**
2. ~~GC-5-G-03~~ — governancecommons.org: live ecosystem landing page with per-standard pages; links to spec repos, validator packages, and conformance badge instructions — **C** _(v1.2.0 baseline/freeze publication landed 2026-09-17; prior 2026-08-10 “not live” note is superseded)_
3. ~~GC-5-G-04~~ — OSS baseline freeze notice: document the frozen OSS core scope on governancecommons.org and in release notes; clarify that PASS-6 profiles are optional extensions, not baseline requirements — **C** _(bound to v1.2.0 release notes/site publication on 2026-09-17)_

**PASS-5 Batch 4 — End-game publish (final; gated on Batch 2 complete; LLC filing gate resolved 2026-06-15):**

1. ~~GC-5-F-02~~ — governance-commons-py: publish to PyPI via OIDC trusted publisher workflow — DONE 2026-08-16: `governance-commons` v0.1.1 live at pypi.org/project/governance-commons/. (v0.1.0 published first via a GitHub-UI-added workflow before README/metadata fixes landed, so its page is frozen with stale placeholder text; v0.1.1 carries the real README and correct project URLs and is what the project page now shows.) — **C**
2. GC-5-F-03 — governance-commons-js: publish to npm via trusted publishing workflow — **O / verification pending**. The old NPM_TOKEN blocker is obsolete; workflow was migrated to npm trusted publishing on 2026-09-18. Verify the actual public package artifact separately.
3. ~~GC-5-F-04~~ — advance `releases/gc-v1.2.0.yaml` status from `planned` to `ready`; populate `pinned_version` for all four specs — DONE: `status: ready` since 2026-06-17; all four specs (agent-dossier, agent-matrix, ons, agent-project-orchestrator) have `pinned_version` populated and `compat_status: ok`; `compat_hold_items: []`. This DEV-PLAN.md row had gone stale against the artifact (caught by the ECOSYSTEM-BOUNDARY.00 cross-repo audit, `c:\dev\docs\ecosystem-roadmap.md` Phase 1). Python 0.2.0 is published; npm 0.2.0 remains unpublished after the workflow moved to Trusted Publishing/OIDC, so package publication proof remains open but is not a manifest-readiness blocker. — **C**

> **Release strategy note (updated 2026-06-09):** PASS-5 Batch 2 completion freezes the OSS baseline. PASS-6 dev work may begin from that frozen baseline and does NOT wait for the end-game publish sequence. The public launch and PASS-6 development run in parallel. Open question: whether the first public release is labeled GC v1.2.0 or renamed GC v1.0.0 for public clarity — requires maintainer decision before Batch 4. No fork is planned at this point; versioning happens at the GC release-manifest boundary.

---

## PASS-6 — Optional Profiles & Document Vault Expansion

**Status:** OPEN — GC-PASS-0006.00 (2026-06-16)
**time.loc:** 2026-06-15T00:00:00Z
**Seed:** gc.profile.doc-vault v0.1.0 committed 2026-06-15 (674ac0f)

PASS-6 owns optional category-defining profiles and the document vault capability track.
The OSS core baseline is frozen. Everything in this section extends it without modifying it.

### Background

On 2026-06-15, while setting up Osprey LLC's business document repository,
`gc.profile.doc-vault` was developed and committed. This became the first GC profile for
non-code repositories. The session revealed a broader product opportunity: governed document
repositories are a more accessible adoption wedge than multi-agent governance for most users.

Key insight: "My files are a mess" is easier to understand than "multi-agent governance framework."
The doc vault profile targets founders, solo operators, LLCs, studios, and consultants —
people who need structure but not enterprise DMS software.

### What was built in the seed session (2026-06-15)

- `profiles/doc-vault/` — 21 files: profile.yml, controls.yml, lifecycle.yml, metadata.schema.yml,
  standards-map.md, retention-schedule.template.yml, access-matrix.template.yml,
  archive-rules.md, ai-access-boundaries.md, 7 templates, Osprey example
- Extended lifecycle states beyond the original spec: `issued`, `confirmation`, `received`
  for external records (government-issued docs, filing receipts, third-party received docs)
- `.governance/` adoption pattern: profile.yml + ons.yml + retention.yml + agents.yml
- `agents.yml` — agent briefing file: quick reference, folder map, rules, current state,
  suggested prompts — the file that makes any LLM immediately context-aware without setup

### PASS-6 Planned Scope (PROPOSED)

#### Track I — Additional profiles

Each profile follows the same structure as doc-vault: profile.yml, controls.yml, lifecycle.yml,
metadata.schema.yml, standards-map.md, templates/, examples/.

| id | name | purpose |
| --- | --- | --- |
| gc.profile.doc-vault | Doc Vault | ✅ DONE — governed document repositories |
| gc.profile.code-repo | Code Repo | Software project governance (README, CONTRIBUTING, AGENTS.md, release rules) |
| gc.profile.doc-control | Document Control | Policies, SOPs, board docs, approval matrices, signature rules |
| gc.profile.audit-gap | Audit & Gap Analysis | required_documents.yml, gap_register.yml, risk_flags.yml — feeds DCP scanner |
| gc.profile.agent-vault | Agent Integration | agents.yml, context_manifest.yml, prompts.md — AI-readable repo context |
| gc.profile.review-grammar | Review Grammar | DRAFT — portable vocabulary for normalize, validate, verify, trace, adversarial audit, meta-audit, authority audit, registry audit, and closure states; profile lives in `profiles/review-grammar/` and is sourced from `C:\dev\docs\REVIEW-GRAMMAR.md` |

Note: gc.profile.code-repo overlaps with existing agent-dossier/agent-matrix work. Reconcile
before building to avoid duplication. gc.profile.agent-vault may become a sub-component of
all profiles rather than a standalone profile.
gc.profile.review-grammar is a draft portable profile. It MUST NOT be treated as a
release-pinned GC standard until accepted by a future GC PASS or RFC.

#### Track II — Business type templates

Pre-filled profile templates by entity type. Lower adoption barrier — user picks a type,
gets a ready-to-use .governance/ folder and folder scaffold.

Target types:

- Wyoming single-member LLC (Osprey pattern — already exists as example)
- Multi-entity holding company
- Creative studio / content creator
- Solo consultant / freelancer
- Real estate holding
- Nonprofit / foundation
- SaaS startup
- Family office

#### Track III — agents.yml as standard profile component

Every profile should ship with an `agents.yml` template. This is the file that makes GC
adoption immediately useful to AI-assisted workflows. Standard fields:

- briefing (plain English repo summary)
- quick_reference (naming, status values, folder map)
- rules_for_agents
- sensitive_fields_never_share
- current_state (what's done, what's pending, known gaps)
- suggested_prompts (copy-paste prompts for common tasks)

#### Track IV — DCP integration surface (PROPOSED, not designed)

The audit/gap analysis capability (scan folder, detect missing docs, suggest renames,
produce cleanup report) belongs in DCP, not in GC profiles. GC defines what good looks like.
DCP checks whether the repo actually follows the rules.

DCP integration points to define:

- DCP reads `.governance/profile.yml` to know which profile to validate against
- DCP reads `.governance/agents.yml` for current state baseline
- DCP writes gap_register.yml and risk_flags.yml back into .governance/
- DCP produces a cleanup report per gc.profile.audit-gap controls

This is future scope. Do not implement validator code in GC profiles.

#### Track V — Adoption UX (tooling concern, not GC concern)

The following are product/tooling ideas that belong in DCP or a separate CLI tool, not in GC:

- Installer wizard ("which profile do you want?")
- Folder scaffold generator from plain-language questions (no YAML required)
- Audit button ("scan this folder and show what's missing")
- Preview changes before applying
- Export install report
- Auto-generate agent-ready prompts from profile

### Track VI — DVP (Doc Vault Plane)

**DVP** is the named control plane for business document repositories.
It is a separate product from DCP and targets a different audience.

```text
DCP   DevX Control Plane     code repos        developer audience
DVP   Doc Vault Plane        business docs     founder / operator audience
```

Both sit on top of GC. Both read GC profiles. Completely separate tools, same underlying standard.

**What DVP owns:**

- Business vault installer (folder scaffold + .governance/ generation from plain questions)
- Business type templates (Holding Company, Creative Studio, Solo Consultant, etc.)
- Audit scanner: reads .governance/profile.yml, scans folder, reports gaps and misfiles
- Cleanup report generator
- agents.yml refresh (keeps current_state accurate as the vault evolves)
- MCP config generator ("Connect to Claude Desktop" button)
- Agent context prompt generator ("Copy Agent Context")
- Dry-run / preview mode before applying changes
- Windows + OneDrive-aware path handling

**What DVP does NOT own:**

- Profile definitions (those are GC)
- Naming grammar (that is ONS)
- Code repo governance (that is DCP)
- Accredited audits or compliance certification

**Build order (PROPOSED):**

1. PowerShell/Python CLI — validates concept, works on Windows today
2. Simple local web UI — accessible to non-developers
3. Desktop app (Tauri or Electron) — only after adoption proves demand

**DVP reads:**

- `GC profiles/` — to know what a governed vault should look like
- `.governance/profile.yml` — to know which profile the vault declares
- `.governance/agents.yml` — to know current state and update it after scans

**DVP writes:**

- `.governance/` folder and all config files (on install)
- `agents.yml current_state` (on scan)
- `gap_register.yml` (on audit)
- Cleanup report (on audit)
- MCP config snippet (on connect)

### Standards alignment note

gc.profile.doc-vault is aligned with ISO 15489, ISO 9001 Clause 7.5, NIST CSF 2.0,
ARMA GARP, and SOC 2 readiness concepts. It does NOT make an adopter compliant, certified,
or audit-ready. Language throughout uses "aligned with," "informed by," "supports readiness for."
This distinction must be preserved across all PASS-6 profiles.

### What is intentionally out of scope for PASS-6

- Validator code in GC profiles (belongs in DCP)
- DCP modification
- Certification claims
- ISO compliance certification
- Enterprise DMS features

---

## PASS-7 — Adoption & Compliance Infrastructure

**Status:** PROPOSED — requires AL:2 sign-off before opening
**time.loc:** 2026-06-15T00:00:00Z
**Depends on:** PASS-6 profiles and .governance/ adoption pattern

PASS-7 is the compliance readiness and adoption infrastructure track. Where PASS-6 defines
what good looks like, PASS-7 provides the scaffolding for organizations to actually demonstrate
they are following the rules over time — building toward real audit readiness, not just alignment.

The four things that separate "aligned with ISO" from "ISO compliant" are:

1. Formal audit by an accredited body
2. Documented evidence over time
3. Trained personnel following processes consistently
4. A corrective action system

GC cannot perform the audit or train the people. But it can provide the structure for
accumulating evidence, recording training, and tracking corrective actions — so that when
an auditor arrives, the evidence exists and is organized.

### Track I — Compliance Evidence Accumulation

GC already has `schemas/gc-compliance-evidence.schema.json` (PASS-4, GC-4-E-04) for
AI agent audit evidence. PASS-7 extends this pattern to document repository governance.

Deliverables:

- `gc.profile.compliance-evidence` — evidence bundle schema for doc vault governance
- Templates for recording evidence of controls being followed over time
- Evidence log: date, control, actor, action taken, outcome, artifact reference
- Linkage from `.governance/` controls to evidence log entries
- Supports: ISO 15489, ISO 9001 Cl. 7.5, NIST CSF 2.0, ARMA GARP, SOC 2

### Track II — Corrective Action System

A corrective action system (CAS) tracks when a control was violated, what was done to fix it,
and whether the fix was verified. This is required for ISO 9001 Clause 10.2 and SOC 2 CC4.

Deliverables:

- `corrective-action-register.template.yml` — log of identified nonconformances
- `corrective-action-record.template.md` — formal CAR document per issue
- Required fields: date identified, control violated, root cause, corrective action taken,
  verification date, closed by
- Integration point: DCP gap scanner writes findings → CAR template → evidence log

### Track III — Training & Awareness Records

Trained personnel following processes consistently is a real ISO requirement. GC can provide
the structure for recording that training occurred.

Deliverables:

- `training-record.template.md` — who was trained, on what policy, when, verified by
- `awareness-log.template.md` — log of policy acknowledgments (e.g., "I have read OH-GOV-DOC-001")
- Applies to: document lifecycle policy, AI access boundaries, sensitive data handling, access control

### Track IV — Audit Readiness Package

When an auditor arrives (ISO, SOC 2, or otherwise), they need a package. GC can define
what that package contains and provide templates to assemble it.

Deliverables:

- `gc.profile.audit-readiness` — profile for assembling an audit evidence package
- `audit-readiness-checklist.template.md` — control-by-control checklist with evidence pointers
- `audit-scope.template.yml` — defines what is in scope for a given audit engagement
- `audit-index.template.md` — table of contents for the evidence package
- Integrates with: compliance evidence log, corrective action register, training records

### Track V — Accredited Audit Path (out of GC scope — recorded for clarity)

GC cannot and will not provide accredited audits. This is explicitly out of scope.
The path to actual certification requires:

- Engaging an accredited certification body (ISO) or qualified auditor (SOC 2)
- Accumulating evidence over a defined period (SOC 2 Type II requires minimum 6 months)
- Resolving all open corrective actions before the audit window closes
- Maintaining the certified state through surveillance audits (ISO) or annual reviews (SOC 2)

GC's role ends at providing the structure. The organization and its advisors do the rest.

### Standards note for PASS-7

All PASS-7 deliverables carry the same language discipline as PASS-6:
"supports readiness for," "provides structure for," "informed by."
No PASS-7 artifact claims compliance, certification, or legal sufficiency.

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

**RFC process (PASS-5 history; amended 2026-08-29).** The initial target called for numbered
`RFC-NNNN-<slug>.md` files and a fixed two-week comment window. The numbered public process now
exists at `rfcs/RFC-PROCESS.md`. On 2026-08-29 the founder and AL:2 maintainer replaced the
fixed delay with proportional review: documented maintainer review is always required, while
a timed public-comment period is required only when known external participants are materially
affected or proposal risk warrants it. The correction and its bootstrap rationale are recorded
in the process document and GC-PASS-0025.00.

**What conformance means.** A declaration names a Governance Commons specification, version,
subject, profile, and evidence. Where a published validator explicitly supports that target, the
declaration records its result. Otherwise the evidence is manual or provisional. Governance
Commons does not operate a certification program, and conformance is never claimed for the
umbrella itself.

**What a release includes.** A GC release is a named manifest that pins the minimum compatible
version of each included spec. It is not a monorepo tag. Each spec can still patch independently
after a GC release is declared. The release manifest format is a PASS-5 exit criterion.

**What the OSS baseline freeze means.** The PASS-5 Batch 2 surface is the public OSS core
baseline. Until the first public release declaration, baseline work is restricted to release
mechanics, website publication, schema/static asset publication, bug fixes, documentation
corrections, release notes, compatibility cleanup, and conformance/public process polish.
New ahead-of-industry capabilities move to PASS-6 as optional, versioned profiles.

**What paid-tier work may include.** Paid or commercial value should sit around PASS-6 profile
implementation and operations: VS Code extension pro features, managed registry/trust network,
audit replay UI, governance diff UI, policy packs, team dashboards, hosted control plane,
conformance evidence automation, and enterprise templates. The OSS standards remain the core.

**What evidence proves governance happened.** An audit-ready governance record must include:
a machine-readable compliance evidence export (signed, structured), a PASS audit trail with
timestamps, handoff envelopes for all agent-to-agent task transfers, and a telemetry trace
mapping task start through completion. This is the PASS-4 exit criterion.

**Steering committee / WG structure.** Not established yet. Required before enterprise procurement
claims. Record here when roles are assigned.

**Timestamp requirement (AL:2 — effective 2026-06-06).** All governance artifacts produced by
agents or humans MUST carry a machine-readable timestamp at the point of creation or emission.
Artifacts without a timestamp MUST be treated as incomplete governance records and MUST NOT
be accepted as audit evidence. This requirement is implemented across five layers — each scoped
to the PASS where it becomes enforceable:

| Layer | Scope | Enforcement point | PASS |
| --- | --- | --- | --- |
| L1 | `time.loc:` field in DEV-PLAN/DEV-PATH/registry headers | Convention — current | PASS-0 (done) |
| L2 | `emitted_at` (REQUIRED) + `accepted_at` (OPTIONAL) in handoff envelopes; `pass_written`, `scaffold_started`, `scaffold_completed`, `implementation_started`, `implementation_completed`, `doc_written` event types in agent-dossier telemetry_trace_schema | agent-dossier spec + schema | PASS-1 |
| L3 | `gc.agent.*` structured event schema with mandatory `time_loc` field in `observability-contract.yaml` | observability-contract.yaml (GC-3-E-01) | PASS-4 |
| L4 | `time_loc` required key in every `telemetry.emit()` call in agent-project-orchestrator | Runtime enforcement in APO | PASS-2 |
| L5 | This AL:2 rule — binding cross-spec requirement enforced at GC release milestone review | DEV-PLAN gating | PASS-0 (this entry) |

The canonical field name is `time.loc` at the document level (colon-qualified key per ONS separator
semantics) and `*_at` at the schema level (`created_at`, `emitted_at`, `accepted_at`). Both forms
MUST use ISO 8601 / RFC3339 UTC format (`YYYY-MM-DDTHH:MM:SSZ`). See DEV-PATH DDR-6 for rationale.

---

## THREE DESIGN DECISIONS — Answers

These are binding decisions at AL:2. Full rationale is in `DEV-PATH.md` under Design Decision Record.

**DDR-1 — Version Conflict Handling:**
Breaking changes declare `BREAKING:` + `breaking_consumers:` in CHANGELOG. Ecosystem DEV-PLAN records a coordinated update item. Downstream specs enter compat-hold. GC release milestone is blocked until all named consumers are resolved. Machine-readable artifact: `compat:` field in `projects.yaml`.

**DDR-2 — Release Train Mechanics:**
Each spec ships on its own cadence. GC milestones are informational pinning contracts — they name minimum compatible versions, not CI gates. `GC v1.2.0 = agent-dossier >=1.1.0 + agent-matrix >=1.3.0 + ONS >=1.2.0`. Adopters pin to the GC milestone, not to individual spec heads.

**DDR-3 — Authority Model:**
AL:3 = ecosystem charter (founder). AL:2 = this file (GC maintainer). AL:1 = individual repo devpaths (spec owners). Ecosystem devplan sets compatibility constraints and milestones only — cannot dictate implementation within a repo's AL:1 scope.

**DDR-7 — OSS Baseline Freeze / Fork Posture:**
PASS-5 Batch 2 is the frozen OSS core baseline. New baseline scope is closed until the first
public release is declared. PASS-6 owns optional category-defining profiles and commercial
capability paths. Do not fork now; defer any fork decision until a concrete licensing, IP, or
operational boundary requires it.

**DDR-8 — GC Portability Posture (resolved 2026-06-17):**
GC core (schemas, YAML specs, markdown) is fully portable — no OS dependency, just files. ONS
naming grammar is portable; platform-specific restrictions (Windows reserved names, forbidden
characters) are addressed by ONS-PC-01/02/03 in PASS-6, not by changing the core grammar. DCP
scripts (PowerShell 7) run on Windows, Linux, and macOS; not on Android/iOS, but that is a
tooling concern, not a GC/ONS concern — GC itself is readable from any platform. No separate
portability tracking item needed; ONS-PC items cover the one real gap (platform naming safety).

---

## RELEASE TRAIN STATUS

| GC Release | Status | Requires |
| --- | --- | --- |
| GC v1.0.0 | Implied (current) | Current published versions of each spec |
| GC v1.2.0 | Ready (M2) since 2026-06-17 — manifest `status: ready` (`releases/gc-v1.2.0.yaml`); Python 0.2.0 is published, while npm 0.2.0 publication remains open under Trusted Publishing/OIDC | agent-dossier >=1.1.0 + agent-matrix >=1.3.0 + ONS >=1.2.0 + APO >=1.1.0 |
| GC v1.3.0 | Planned (M3) | agent-dossier >=1.2.0 + agent-matrix >=1.4.0 + ONS >=1.3.0 |
| GC v2.0.0 | Planned (M4) | Major version — breaking changes allowed |

---

## COMPATIBILITY MATRIX

Current cross-repo version constraints. Updated when breaking changes are declared.

| Spec | Current version | Depends on | Constraint | Status |
| --- | --- | --- | --- | --- |
| agent-dossier | 1.0.x | ONS | ONS naming grammar for PASS IDs | No open conflicts |
| agent-matrix | 1.x | agent-dossier | dossier schema for capability profiles | No open conflicts |
| ONS | 1.2.0 | — | No upstream deps | No open conflicts |
| agent-project-orchestrator | 1.x | agent-dossier, agent-matrix | runtime-contract.yaml schema | No open conflicts |
| agent-team-protocol | 0.1.0 | agent-matrix >=1.4.0, agent-dossier >=1.0.0 | fleet governance consumes per-agent primitives | No open conflicts |

No current `compat-hold` items.

---

## GAP ANALYSIS CHECKLIST

Cross-reference from sources 97–101 to DEV-PATH PASS assignments.
Status: **O** = open · **C** = closed · **WF** = won't-fix · **H** = compat-hold

### Source 97 — agent-dossier runtime gaps

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| 97-G1 | No package.json (js-yaml undeclared) | P0 | PASS-1 / GC-1-A-01 | C |
| 97-G2 | No .gitignore | P0 | PASS-1 / GC-1-A-02 | C |
| 97-G3 | JSON Schema validation declared but never wired | P0 | PASS-1 / GC-1-A-03 | C |
| 97-G4 | task-queue.json hand-written (must be compiled artifact) | P0 | PASS-1 / GC-1-A-04 | C |
| 97-G5 | No environment abstraction (paths/IDs/timeouts are literals) | P0 | PASS-1 / GC-1-A-05 | C |
| 97-G6 | Hardcoded Windows paths in source comments | P0 | PASS-1 / GC-1-A-06 | C |
| 97-G7 | Custom telemetry (not OpenTelemetry) | P1 | PASS-4 / GC-1-A-07 | C |
| 97-G8 | PASS-YYYY-NNNN ID format not validated or generated | P1 | PASS-1 / GC-1-A-08 | C |
| 97-G9 | Handoff envelope defined in spec, never emitted in code | P1 | PASS-1 / GC-1-A-09 | C |
| 97-G10 | Orchestrator monolith (no module split) | P2 | PASS-3 / GC-2-A-01 | O |
| 97-G11 | Agents hardcoded via require() (no plugin interface) | P2 | PASS-3 / GC-2-A-02 | O |
| 97-G12 | No Dockerfile or cloud deployment targets | P2 | PASS-3 | O |
| 97-G13 | No installable SDK (no main field, no CLI) | P2 | PASS-3 / GC-2-A-04 | O |
| 97-G14 | No feature flags, no tenant isolation | P3 | PASS-6 | O |
| 97-G15 | No SLSA build provenance | P3 | PASS-5 | O |

### Source 98 — agent-matrix strategic gaps

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| 98-G1 | No MCP server/client model | Critical | PASS-2 / GC-1-B-03 | C |
| 98-G2 | No A2A protocol binding | Critical | PASS-2 / GC-3-B-02 | C (stub) |
| 98-G3 | No CloudEvents envelope binding | Critical | PASS-2 / GC-3-B-03 | C (stub) |
| 98-G4 | No compliance framework mapping (NIST AI RMF, EU AI Act) | Critical | PASS-1 / GC-1-B-05 | C |
| 98-G5 | SKU model Anthropic-only, no multi-provider routing | Critical | PASS-1 / GC-1-B-04 | C |
| 98-G6 | No matrix overlays/fragments (monolithic YAML) | High | PASS-1 / GC-2-B-01 | C |
| 98-G7 | No named profiles (minimal, data-engineering) | High | PASS-1 / GC-2-B-02 | C |
| 98-G8 | No matrix inheritance (extends: with override semantics) | High | PASS-1 / GC-2-B-03 | C |
| 98-G9 | No runtime agent discovery or registry | High | PASS-2 / GC-3-B-01 | C |
| 98-G10 | No cryptographic agent identity | High | PASS-2 / GC-3-A-02 | C |
| 98-G11 | No formal SLO/SLI definitions per profile | High | PASS-1 / GC-1-B-01 | C |
| 98-G12 | No checkpoint format schema | Medium | PASS-1 / GC-1-B-02 | C |
| 98-G13 | No streaming output schema | Medium | PASS-2 / GC-3-B-04 | C |
| 98-G14 | No prompt injection defense spec | Medium | PASS-2 / GC-3-B-05 | C |
| 98-G15 | No named workflow pattern library | Medium | PASS-1 / GC-2-B-05 | C |
| 98-G16 | No multi-orchestrator topology spec | Medium | PASS-6 / GC-4-B-02 | O |

### Source 99 — agent-project-orchestrator runtime gaps

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| 99-G1 | DevPath + Tracks stale (PASS-1/2/3 marked PENDING, code exists) | P0 | PASS-0 / GC-1-D-01 | C |
| 99-G2 | CHANGELOG missing Python rewrite entry (PASS-2026-0002) | P0 | PASS-0 / GC-1-D-02 | C |
| 99-G3 | Level-2 escalation (operator_clarification) unreachable in escalation.py:27-31 | P0 | PASS-1 / GC-1-D-03 | C |
| 99-G4 | Agents never call telemetry.emit() (all traces from dispatcher only) | P1 | PASS-4 / GC-1-D-04 | C |
| 99-G5 | runtime-contract.yaml non-deterministic (timestamp in trace_id) | P1 | PASS-1 / GC-1-D-05 | C |
| 99-G6 | models/task.py unused; raw dicts used instead | P1 | PASS-1 / GC-1-D-06 | C |
| 99-G7 | governance/multi-agent.yaml never read at runtime | P3 | PASS-2 / GC-1-D-10 | C |
| 99-G8 | Handoff envelopes not implemented (level-1 escalation logs warning, no envelope) | P2 | PASS-1 / GC-1-D-07 | C |
| 99-G9 | Zero test coverage for agents and orchestrator | P2 | PASS-1 / GC-1-D-08 | C |
| 99-G10 | Per-agent resource budgets not enforced (time_limit, tool_call_limit unused) | P3 | PASS-2 / GC-1-D-11 | C |

### Source 100 — ONS v1.2.0 gaps

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| 100-S1 | Stale header comment (v1.1.0/2026-06-03 vs body v1.2.0/2026-06-04) | Low | PASS-1 / GC-1-C-01 | C |
| 100-S2 | No casing rule for colon (qualification) domain | Medium | PASS-1 / GC-1-C-03 | C |
| 100-S3 | No cluster registration protocol or registry | High | PASS-1 / GC-1-C-05 | C |
| 100-S4 | ons-conformance.schema.json diverges from ons.yaml | High | PASS-1 / GC-1-C-02 | C |
| 100-S5 | No rule soft-deprecation mechanism | Medium | PASS-1 / GC-1-C-09 | C |
| 100-S6 | No RFC 2119 normative language | High | PASS-1 / GC-1-C-04 | C |
| 100-T1 | FAST rules in catalog but no validator implements them | — | PASS-1 / GC-1-C-08 | C |
| 100-T2 | No pytest suite for tools/validate.py | — | PASS-1 / GC-1-C-07 | C |
| 100-T3 | No rules.json export for LSP/linter authors | — | PASS-1 / GC-1-C-06 | C |
| 100-T4 | VALIDATOR_VERSION hardcoded 1.0.0 | — | PASS-3 | O |
| 100-A1 | RFC 2119 normative language (table stakes for citation) | Table stakes | PASS-1 / GC-1-C-04 | C |
| 100-A2 | Conformance test suite with test vectors | Medium | PASS-3 / GC-2-C-01 | C |
| 100-A3 | TypeScript reference implementation | High | PASS-3 / GC-2-C-02 | C |
| 100-A4 | pip install + npm package | Low-medium | PASS-3 | C |
| 100-N1 | LSP implementation (highest-leverage long-term move) | High effort | PASS-6 / GC-4-C-01 | O |
| 100-N2 | Global cluster registry as governed service | Low-medium | PASS-5 | O |
| 100-N3 | Machine-readable governance record schema | Medium | PASS-4 / GC-4-E-01 | O |

### Source 101 — Governance Commons capstone gaps

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| 101-G1a | A2A binding is surface mention only — stub exists, 5/5 depth required | Critical | PASS-2 / GC-3-B-02 | C |
| 101-G1b | MCP not a first-class governance primitive | Critical | PASS-2 / GC-1-B-03 | C |
| 101-G1c | No transport binding (HTTP/2 SSE, WebSocket, gRPC, Kafka) | Critical | PASS-4 / GC-4-B-03 | C |
| 101-G2a | No cryptographic integrity (handoffs can be replayed/forged) | Critical | PASS-2 / GC-3-A-01 | C |
| 101-G2b | Agent identity is string-only (no cryptographic binding) | Critical | PASS-2 / GC-3-A-02 | C |
| 101-G2c | No zero-trust establishment/verification/revocation spec | Critical | PASS-2 / GC-3-A-03 | C |
| 101-G3a | OTel listed in alignment but not specified (no span names, metric names) | High | PASS-4 / GC-3-E-01 | C (v1.0.0) |
| 101-G3b | No structured agent lifecycle event schema | High | PASS-4 / GC-3-E-01 | C |
| 101-G4a | NIST AI RMF surface mapping only, no control evidence generation | High | PASS-4 / GC-3-E-02 | C |
| 101-G4b | ISO 42001 missing entirely | High | PASS-4 / GC-3-E-03 | C |
| 101-G4c | SOC 2 Type II not addressed | High | PASS-4 | C |
| 101-G5 | Python-only (TypeScript, Go, Rust adopters have no path) | High | PASS-3 | O |
| 101-G6a | No RFC/proposal process | Medium | PASS-5 / GC-3-G-02 | O |
| 101-G6b | No conformance certification mechanism | Medium | PASS-5 / GC-3-G-03 | O |
| 101-G7a | No dossier revocation/expiry model | Medium | PASS-1 / GC-1-A-10 | C |
| 101-G7b | No versioned capability claims for audit replay | Medium | PASS-4 | C |
| 101-AC1 | Constitutional governance layer (constitution.yaml) | Ahead-of-curve | PASS-6 / GC-4-A-01 | O |
| 101-AC2 | Federated Agent Trust Network | Ahead-of-curve | PASS-6 / GC-4-B-01 | O |
| 101-AC3 | Temporal authority windows | Ahead-of-curve | PASS-6 / GC-4-A-02 | O |

### PASS-2 — New gaps registered 2026-06-07

Gaps identified during PASS-1 gate review and PASS-2 scoping that have no prior source entry.

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| GC-3-A-03 | Zero-trust spec: establishment (key exchange), rotation (re-key events), revocation (dossier invalidation) — `governance/zero-trust.yaml` | Critical | PASS-2 | C |
| GC-3-B-06 | STRIDE threat model for multi-agent systems — `governance/threat-model.md` covering all six categories with mitigations | High | PASS-2 | C |
| GC-3-B-03-depth | CloudEvents binding depth to 5/5: `schemas/events/*.schema.json` for all 5 event types, delivery semantics, causality, idempotency, W3C trace-context (stub exists at 2/5) | Critical | PASS-2 | C |

### PASS-4 — New items registered 2026-06-08

Items identified during PASS-4 scoping that have no prior source entry.

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| GC-4-E-02 | Tamper-evident audit log hash chaining — `audit_log_chain` spec in observability-contract.yaml; SHA-256 chain fields in gc-agent-event.schema.json | High | PASS-4 | C |
| GC-4-E-03 | Security and anomaly detection event categories — `security_events` section (5 spans, 5 rules) in observability-contract.yaml; new gc_event_type values and fields in gc-agent-event.schema.json | High | PASS-4 | C |
| GC-4-E-04 | Signed compliance evidence export — `schemas/gc-compliance-evidence.schema.json` v1.0.0; JWS EdDSA signature block; control_frameworks array (NIST/ISO/SOC2/EU-AI-Act); bundle_hash integrity | High | PASS-4 | C |
| 100-N3 | Machine-readable governance record schema (GC-4-E-01) — full evidence record schema cross-referencing PASS trail | Medium | PASS-4 | O — partially addressed by GC-4-E-04; full schema TBD |

### DDR-6 — Timestamp requirement (registered 2026-06-06)

Gaps created by the AL:2 timestamp requirement (DDR-6). Spec additions to agent-dossier.yaml and handoff-envelope.schema.json are complete; the items below track implementation and enforcement.

| Gap | Description | Priority | PASS | Status |
| --- | --- | --- | --- | --- |
| GC-1-A-TL-01 | agent-dossier: emit handoff envelopes with `emitted_at` populated at transmission time; verify all emission sites in APO `escalation.py` and any future emitters | P1 | PASS-1 | C |
| GC-1-A-TL-02 | agent-dossier: emit telemetry events using the seven new lifecycle `event_type` values (`pass_written`, `scaffold_started`, `scaffold_completed`, `implementation_started`, `implementation_completed`, `doc_written`, `registry_updated`) from relevant agent execution paths | P1 | PASS-1 | C |
| GC-1-D-TL-01 | agent-project-orchestrator: enforce `time_loc` as a required key in every `telemetry.emit()` call; runtime validation MUST reject emission without it | P2 | PASS-2 | C |

---

## SYNTHESIS-DERIVED QUEUED WORK

Registered 2026-06-09 from 2-agent synthesis (Claude + ChatGPT, 102 sources). These items are not yet active batches. Full rationale in `docs/sessions/2026-06-09-combined-synthesis.md` and `DEV-RELEASE.md`.

### Regulatory Deadlines (time-bound — do not defer past stated dates)

| Regulation | Jurisdiction | Deadline | Relevant GC Work |
| --- | --- | --- | --- |
| EU AI Act — general applicability | EU | **August 2, 2026** | `control_frameworks` EU-AI-Act reference in `gc-compliance-evidence.schema.json`; four-tier risk labeling; conformance evidence export |
| Colorado SB26-189 ADMT regime | Colorado, USA | **January 1, 2027** | ADM transparency output in compliance evidence; jurisdiction-adaptive policy compiler (eco's responsibility, GC provides the evidence schema) |
| GDPR Article 17 right to erasure | EU | Active now | Governance record schema must support data-subject-rights audit trail |

### PASS-5 Open Items (not yet in near-term queued work)

| ID | Task | PASS | Status |
| --- | --- | --- | --- |
| 97-G15 | SLSA Level 1+ build provenance — add provenance attestation to PyPI and npm publish workflows; workflows exist but provenance not yet added | PASS-5 | O |
| 101-G6b | Conformance certification mechanism — beyond self-declare; verifier registry so "GC-conformant" has a verifiable meaning | PASS-5 | O |
| 100-N2 | Global cluster registry as a governed service | PASS-5 | O |
| 101-G5 | TypeScript + Go SDKs — Python-only blocks enterprise teams; TypeScript ONS impl done; full SDK parity open | PASS-3 | O |

### PASS-6 Items from Synthesis (not yet registered in gap checklist)

| ID | Task | Synthesis Ref | PASS | Notes |
| --- | --- | --- | --- | --- |
| SYN-ONS-PLATFORM | ONS platform compatibility layer — per-OS safe character sets, Windows reserved name exclusions (CON, NUL, COM1–COM9, LPT1–LPT9), forbidden characters, trailing space/dot rules, 260-char path limit; `platform:` field in ons-conformance.schema.json so repos declare `windows \| linux \| macos \| universal` and validator enforces it | ONS-PC-01/03 | PASS-6 | Required for DVP — Osprey vault runs on Windows/OneDrive; ONS-valid names can still be illegal on Windows without this layer |
| SYN-ONS-UNIVERSAL | UNIVERSAL conformance tier — validation mode above STANDARD: platform-safe on all OS + human-readable without spec knowledge + ISO/data industry best practice; the designated tier for document repositories and DVP adoption; ONS grammar defines structure, gc.profile.doc-vault defines vocabulary — UNIVERSAL is where both meet; sits between STANDARD and STRICT; no AST-level rules but stricter character set and readability constraints than STANDARD | ONS-PC-02 | PASS-6 | Enables DVP to enforce readable names without requiring STRICT mode; first naming standard to ship a human-readable tier with formal spec backing |
| SYN-DVP-AGENT-01 | Agent naming decision contract — machine-readable algorithm for constructing filenames from entity, domain, category, lifecycle state, version, date; belongs in doc-vault/DVP not ONS; ONS validates shape, DVP decides correct business/legal segments; agents execute deterministically, no guessing from prose | DVP-AGENT-01 | PASS-6 | Policy layer already exists in ai-access-boundaries.md and lifecycle.yml; enforcement layer is missing |
| SYN-DVP-AGENT-02 | Protected record manifest — `.governance/record-manifest.yml` with SHA-256 hashes, immutable flags, lifecycle state, access level, and authorized operations per record; covers rename/move/delete/read permissions; executed/issued/confirmation/received records immutable by default | DVP-AGENT-02 | PASS-6 | Stronger than a simple immutability list — becomes the machine-enforceable source of truth for all agent operations on governed records |
| SYN-DVP-AGENT-03 | Agent operation policy — defines what agents may do (suggest rename, stage rename, execute rename, create draft, redact copy, update index); sensitive or immutable records require Vault Owner approval before mutation; no agent may exceed declared operations | DVP-AGENT-03 | PASS-6 | Makes `.governance/` a permission contract, not just a briefing document |
| SYN-DVP-SEC-01 | Storage and encryption posture checks — DVP verifies declared posture: owner-only files must be in private/encrypted storage; public paths must not contain restricted classes; AI-accessible MCP paths must not include owner-only records; flags violations on scan | DVP-SEC-01 | PASS-6 | DVP cannot encrypt but can enforce storage boundary rules; closes the gap between access-matrix.template.yml policy and actual enforcement |
| SYN-DVP-AUDIT-01 | Unauthorized mutation detection — compare filesystem state against record-manifest.yml hashes; if a governed record changed without a logged DVP operation, flag as unlogged mutation; tamper-evidence without OS-level audit tooling | DVP-AUDIT-01 | PASS-6 | Closes Q5 security gap in DVP industry gap analysis; works in conjunction with DVP-AGENT-02 manifest |
| SYN-GC-HAT | Human-Agent Teaming Protocol — formal spec for human principals entering/exiting agentic loops; `human_in_the_loop` states; decision authority tokens; escalation SLAs | J2 | PASS-6 | No existing governance framework has this; complements constitutional governance layer |
| SYN-GC-GDPR | GDPR/privacy rights compliance mapping — data-subject rights (access, erasure, portability) mapped to GC governance record schema | Tier 1 standards | PASS-6 | Required for EU enterprise procurement |
| SYN-GC-A2A-V2 | A2A protocol full binding v2 — task lifecycle states, streaming responses, push notification contracts beyond current 5/5 depth spec (Google A2A April 2025 evolution) | E5 strategic | PASS-6 | Current A2A binding is comprehensive; this tracks evolution of the standard |

### Anti-Patterns (from synthesis Section F — what governance-commons must not become)

These are documented as constraints on the standards process:

| Anti-Pattern | Risk |
| --- | --- |
| Governance rules with no runtime enforcement path | Governance-as-documentation-theater; spec items must have a tested runtime path |
| Static compliance declarations without machine-readable evidence generation | Evidence must be generated and signed, not declared |
| No RFC/proposal process | Enterprises cannot list GC as a dependency without a WG structure; RFC process exists but must be public-facing |
| Spec growth without a conformance certification program | "Conformant" has no verifiable meaning without a verifier registry (101-G6b) |
| Capability claims without versioning | Audit replay is impossible without `declared_at` versioning; this is now spec-complete |
| Single-principal authority | Agents self-declaring their own authority have no external accountability anchor |

---

## NEAR-TERM QUEUED WORK

Work registered but deferred past the active batch. Items are promoted to "Immediate next tasks" when the preceding batch clears.

| ID | Task | Track / Area | PASS | Blocks | Status |
| --- | --- | --- | --- | --- | --- |
| ~~GC-3-B-01~~ | ~~Runtime agent discovery registry~~ | Bravo | PASS-3 | GC v1.3.0 | ✅ Done |
| ~~101-G1c~~ | ~~Transport binding (HTTP/2 SSE, WebSocket, gRPC, Kafka)~~ | Bravo | PASS-4 | cross-spec interop | ✅ Done |
| ~~GC-3-E-02~~ | ~~NIST AI RMF control evidence generation~~ | Echo | PASS-4 | GC v2.0.0 | ✅ Done |
| ~~GC-3-E-03~~ | ~~ISO 42001 mapping~~ | Echo | PASS-4 | GC v2.0.0 | ✅ Done |
| GC-2-A-01 | agent-dossier: orchestrator module split | Alpha | PASS-3 | PASS-3 packaging | O |
| GC-2-A-02 | agent-dossier: plugin interface (no hardcoded require()) | Alpha | PASS-3 | PASS-3 packaging | O |
| ~~GC-2-B-05~~ | ~~agent-matrix: named workflow pattern library~~ | Bravo | PASS-1 | GC v1.3.0 | ✅ Done |
| ~~GC-1-F-01~~ | ~~agent-team-protocol: fleet-escalation + team-lifecycle schemas~~ | ATP | PASS-1 | GC v1.2.0 | ✅ Done |
| ~~GC-1-F-02~~ | ~~agent-team-protocol: pytest test vectors for all 5 sections~~ | ATP | PASS-1 | GC v1.2.0 | ✅ Done |
| ~~GC-2-C-02~~ | ~~TypeScript reference implementation for ONS~~ | Charlie | PASS-3 | VS Code extension | ✅ Done |
| ~~GC-2-E-01~~ | ~~governance-commons-py: scaffold + PyPI publish infra~~ | Echo | PASS-3 | PyPI publish | ✅ Done |
| ~~GC-2-E-02~~ | ~~governance-commons-js: scaffold + npm publish infra~~ | Echo | PASS-3 | npm publish | ✅ Done |
| GC-AUDIT-PLAY-01 | GC-AUDIT Change Playbook / DEV-DOCS audit — PLAY formalized as pre-work declaration mapped to BUNT/RUN/DRIVE/PASS; schema validator, telemetry display, conditional Level 1 hook, JSON output, and per-level validation_profile enforcement active; broader commit/comment/push enforcement remains open | GC-AUDIT | DEV-ACCORD.06 | agent session compliance | O |

---

_This document is the single authority for Governance Commons execution planning._
_Do not create alternate execution plan documents — update this one._


## 2026-10-05 — Local reconciliation receipt

Authorized continuation: Jesse directed "DO IT" for the recommended Governance Commons reconciliation and governance debt work. Changes remain local and uncommitted. Current SDK remote 0.2.0 supersedes the older local working tree as canonical implementation; the unpublished local TypeScript parity/version draft is preserved separately. Agent Matrix examples are aligned with current schemas; the unsupported additional compliance event mapping remains queued. ONS lint whitespace and bootstrap authority pointers are repaired. GC-AUDIT recognizes public-safe stubs, existing local onboarding authority and registry-selected planning owners, with regression tests. Protected histories and queued ideas are retained. No RFC activation gate, release gate, public publication or trading action is completed by this work.

Reconciliation validation receipt (2026-10-05): SDK 219 Python tests and Node checks pass; Matrix nine CI validations and 232 tests pass; ONS validation and lint pass; 13 new authority regression fixtures plus 19 existing fixtures pass with compatible Pester runtimes. SDK draft files and 24 stale generated files are preserved; final wheel/sdist/npm archives exclude unpublished drafts. Bootstrap: zero errors, eight warnings. Planning: two errors, twelve warnings, both errors at protected Kinjuu DEV-PATH header. Registry: 126 pointers resolve. Governed closure remains OPEN; unchecked release gates remain unchecked. No commit or push.

## 2026-10-06 — Release authority and commit-readiness review

Kinjuu header format repaired under Jesse's explicit narrow exception; historical body unchanged. GC release ownership is `governance-commons/DEV-RELEASE.md`; the retained dev-docs copy is historical. Four historical completion checkboxes are reconciled against published registries, existing notes and ready manifest. Public Python 0.2.0 and npm 0.1.1 remain divergent from coordinated current SDK source. Website HTTPS proof remains open. SDK/Matrix/ONS working-tree changes are reviewed for commit readiness, not automatically committed or published.

## 2026-10-07 — RFC-0001 implementation checkpoint

RFC-0001 remains accepted and not active. The bounded public-boundary batch advances A-2 by
splitting normative specification compatibility from tested runtimes, implements A-3 and A-4 in
the charter, completes the ATP field/composition change in
A-5, and replaces the website's equal-status four-component presentation with explicit role,
maturity, version, evidence, and authority boundaries. A-1 remains open: APO's vendored Agent
Dossier schemas do not yet record release tag, immutable commit SHA, schema path, content digest,
and automated drift verification, so APO remains a reference-runtime candidate.
The A-2 requirement to generate or validate umbrella releases from component compatibility data
also remains open; the historical v1.2.0 manifest is not silently rewritten.

Activation gate state after the local batch:

- G-1 open: the five Agent Dossier schemas are present and return 200 from the
  repository's default GitHub Pages address, and the website build now verifies
  their paths and canonical `$id` values before upload. The Pages API reports no
  configured custom domain, so the same canonical `governancecommons.org` URLs
  return 404. The published files match the Agent Dossier v1.0.3 tag while their
  canonical path remains v1.0.2; v1.1.0 changes three schemas without changing
  those `$id` values. Do not complete G-1 or silently overwrite the published
  path until the external Pages/DNS configuration and release identity are
  reconciled and verified.
- G-2 locally satisfied candidate: Agent Matrix has an MIT license file consistent with its
  README and package metadata; remote/public verification waits on commit and publication.
- G-3 locally satisfied candidate: ONS README, canonical YAML, schema IDs, and latest release tag
  agree on v1.3.0; remote/public verification waits on commit and publication.
- G-4 locally implemented candidate: the site presents the three released specifications and
  separates runtime candidates, pre-release work, evidence contracts, and tooling. Public deploy
  verification remains open.
- G-5 open: current Agent Matrix main still aligns its current row to unreleased Agent Dossier
  v1.4.0. Do not change that compatibility claim without coordinated release/compatibility proof.

Additional release-truth blocker: published Python toolkit 0.2.0 reports ONS v1.4.0 while the ONS
repository's latest release and canonical surfaces are v1.3.0. Reconcile the toolkit ruleset and
release identity before using automated ONS output as proof for the v1.3.0 baseline. npm 0.2.0 is
not published; npm 0.1.1 remains latest despite the Trusted Publishing/OIDC workflow migration.
The v1.2.0 manifest also fails its current JSON Schema because `ready_at` is not declared and its
legacy `gc_pass_id` value does not match the schema pattern; reconcile that identifier contract
without erasing release history before treating manifest validation as clean.

## 2026-10-07 — RFC-0001 A-1 implementation

A-1 is locally implemented in Agent Project Orchestrator. APO's two vendored Agent Dossier
schemas are byte-identical to the released files in tag `v1.0.2` at immutable commit
`054e9cdf0be5dc8f94a16c908cd2b4d0440bb2ec`. APO now records the release tag, commit SHA,
released source path, SHA-256 digest, and embedded `$id` for each vendored schema. Its CLI,
regression suite, and GitHub Actions workflow fail on content or identifier drift. The release
artifacts' existing v1.0.0 `$id` values are preserved and disclosed rather than rewritten.

This evidence satisfies A-1's offline-vendoring conditions and supports APO's
**reference-runtime candidate** classification. It does not classify APO as a specification,
certify runtime behavior, resolve APO's separate packaging/runtime-data limits, or activate
RFC-0001. A-2 remains partial, and G-1 through G-5 remain the activation gate.

## 2026-10-07 — RFC-0001 A-2 release validation implementation

A-2's release-validation mechanism is implemented in `scripts/validate_release.py`.
It validates the manifest schema and derives compatibility checks from Agent Matrix's
normative rows at an immutable commit, verifies specification release tags, checks
exact Dossier alignment and minimum schema identity, and records source commits in
a JSON evidence report. Runtime observations do not affect specification compatibility.
Regression tests and CI enforce rejection of mismatched, held, duplicate, unpinned,
deprecated, or nonexistent compatibility selections. No release pins or tags changed.

The historical v1.2.0 manifest remains blocked: `ready_at` and legacy `gc_pass_id`
fail its schema, and its Dossier v1.1.0 pin differs from the Matrix v1.4.0 row's
v1.0.2 alignment. Resolve the schema/identifier contract and establish coordinated
compatibility evidence before declaring that manifest verified. G-5's current
Matrix row referencing unreleased Dossier v1.4.0 remains open. RFC-0001 remains
accepted and inactive. Website work remains parked.

## 2026-10-07 — Release-contract reconciliation

The v1.2.0 manifest now satisfies its structural schema. `ready_at` is explicitly
supported as historical provenance, and the ambiguous `GC-PASS-0015.00` citation
is retained in `historical_gate_review` rather than asserted as current review
authority. Protected DEV-PATH associates that citation with the June 8 PASS-4
gate; passchangelog associates it with the June 30 Change Playbook. Both source
records remain unchanged. No substitute PASS identity has been invented.

Readiness is withdrawn: the manifest is `planned`, Dossier and Matrix carry
`compat-hold`, and the hold list records their alignment disagreement plus the
unresolved historical review citation. Original version pins, tags, and the
June 17 readiness timestamp are preserved. Restoring readiness requires consumer
compatibility evidence and resolved review provenance. The schema enforces exact
pins, ok component compatibility, empty holds, and resolved historical provenance
for ready manifests. Release verification deliberately remains non-passing until
the underlying evidence exists. RFC-0001 remains accepted and inactive.

## 2026-10-07 — Dossier v1.1.0 / Matrix v1.4.0 compatibility closure

Consumer compatibility is established at immutable Agent Matrix commit
`296c587da1488c95e17f9627c343f0d67e72211a`. Its machine-readable evidence pins Dossier
tag `v1.1.0` at `f935146ea2762e3fcb2387a704313d2467233872` and Matrix tag `v1.4.0` at
`1812bed7f1d195a6de7fb31e9382c079d4ca1b4e`, records artifact SHA-256 digests, and tests
retained agent classes, event types, log levels, escalation names, and a Dossier-valid handoff
projection. Matrix-only `task_id` and `reason` remain routing context; Dossier `type`,
`emitted_at`, lifecycle, and expiry rules remain mandatory.

The v1.2.0 manifest now marks Dossier and Matrix compatibility `ok`, with no compatibility
holds, and validates against the immutable Matrix evidence source. This is bounded
specification-integration evidence, not schema identity, runtime interoperability, independent
adoption, or production-operation evidence. Dossier's divergent internal version labels remain
disclosed and unresolved. The manifest remains `planned`; the ambiguous historical
`GC-PASS-0015.00` review citation still blocks readiness. RFC-0001 remains accepted and inactive.

## 2026-10-07 — Founder ruling on duplicate GC-PASS-0015.00 citation

Founder, creator, and maintainer Jesse Ervin resolved the historical identity collision:
`GC-PASS-0015.00` authoritatively identifies the 2026-06-08 PASS-4 gate review recorded in
DEV-PATH. Its 2026-06-30 reuse in passchangelog for Change Playbook work was a clerical
duplicate and carries no separate release-review authority. Both historical source records
remain unchanged; this ruling clarifies their authority without rewriting history or inventing
a substitute PASS identity.

The manifest records the citation as `clarified`, not `ambiguous`. The June 8 PASS-4 gate
review is not a current GC v1.2.0 release review. GC v1.2.0 therefore remains `planned` pending
a current release review and its other open admission gates. Compatibility evidence, release
pins, tags, and RFC-0001 activation status are unchanged by this ruling.

## 2026-10-07 — GC v1.2.0 release advancement review

Founder/maintainer direction retains the established GC v1.2.0 public label rather than resetting
the umbrella release to v1.0.0. Registry commit `5987cd9` and GitHub Actions run `37711763406`
establish fresh-clone, clean-candidate-wheel CI for ONS and Dossier across the 3-OS × 3-Python
matrix; the parallel Node matrix validates the ONS-focused npm surface. Isolated registry installs
of Python 0.2.0 and npm 0.1.1 both installed and ran ONS validation successfully.

The public package boundary remains explicit: Python 0.2.0 does not expose Dossier validation,
and npm 0.2.0 is not published. Website commit `cd6c6b1` adds pinned install instructions and
corrects the prior attribution of source-only Dossier support to Python 0.2.0. Canonical HTTPS is
still blocked because GitHub will not bind `governancecommons.org` until the domain is verified for
the organization. The current release review therefore leaves the manifest `planned`; website
delivery and a coordinated SDK package-version/publication decision remain open.

## 2026-10-24 — OBDD-CA-01 proposed assurance implementation

OBDD-CA.01.00 is implemented as a **draft/proposed** standards candidate. The
human-supplied OBDD v1.1 Conformance and Assurance Annex is preserved as the
normative proposal for the newly merged, proposed GC-DD-01 Outcome-Bound
Development Directive. A machine-readable assurance record, deliberately incomplete
adopter template, fail-closed validator, regression suite, and CI gate implement
the annex's traceability and evidence boundaries.

This work does not formally approve OBDD v1.1, determine an adopter's laws or
legal role, verify the truth of supplied evidence, conduct an independent
assessment, or confer external certification. Those determinations remain with
the named accountable and competent authorities for each implementation.

## 2026-10-24 — OBDD v1.1 formally approved

Jesse Ervin identified himself as the sole current owner and authorized
approver for the `C:\dev` portfolio and `jj-ervin` GitHub work, then explicitly
stated: “I formally approve GC-DD-01 and OBDD-CA-01 for OBDD v1.1.”

GC-DD-01 and OBDD-CA-01 are therefore `accepted` for OBDD v1.1. The assurance
record contract, fail-closed validator, tests, and CI gates are accepted as the
annex's implementation surface. Acceptance does not determine adopter-specific
legal applicability, authenticate future evidence, constitute an independent
assessment, or confer certification under an external standard.

## 2026-10-27 — ZTA-08.02 draft control acceptance integration

**PROPOSED — requires AL:2 sign-off.** On `gc-audit-zta-001-draft`, the main
ZTA evaluator now has a bounded ZTA-08.02 whole-chain proof route for a signed,
current, revision-bound control policy and authenticated build, distribution,
and installation evidence covering an independently supplied scope inventory.
Verified negative evidence retains FAIL precedence. The draft implementation
and synthetic fixtures do not establish independent assurance, actual deployment
coverage, overall assessment eligibility, implementation closure, or release.
Owner review of the PR and hosted CI remain separate gates. Historical PLAY
records are unchanged.

## 2026-10-27 — GC-AUDIT sibling planning-owner validation

The planning validator accepts an optional outer portfolio boundary for a
registry in a separate control-plane checkout. Its default boundary remains
the target root. In the local `C:\dev` layout, the control-plane validation
checks 90 registered planning documents with zero errors and 12 existing
warnings. The pointer validator covers 160 registry path fields, including
planning keys previously omitted from its check. This is a tooling
compatibility change; it does not amend a GC
standard or close project, publication, or release gates.

## 2026-10-27 — GC-AUDIT-ZTA-001E final remediation candidate

**OWNER REVIEW CANDIDATE; final acceptance blocked.** The focused feature branch hardens the parser-backed GC-AUDIT operation-registry self-audit, adds adversarial registry and delegated-host fixtures, and separates ZTA-08.02 assessor data from caller-supplied trust authority. Local ZTA, schema, registry, OBDD, planning, PLAY, release-compatibility, and legacy ZT1–ZT8 checks are recorded in `gc-audit/specifications/GC-AUDIT-ZTA-001E-ACCEPTANCE-EVIDENCE.md`. Exact-head hosted CI, an independent review, a registered `gc-audit.zta` invocation, and actual target/host authority evidence remain open. No release, operational activation, certification, or PASS closure is claimed. `AGENTS.md` was checked and its bootstrap pointer remains current.

Hosted PR #9 checks subsequently passed at implementation commit `9effdd70ee89e9cab78e0523ad901f3c1fb8fc0a` across the registry and evaluator 3-OS × 2-Python matrices, schemas, OBDD, release compatibility, and lint. This supersedes only the pending-CI statement above; independent review, registration, real-target proof, and owner acceptance remain open.

## 2026-10-28 — GC-AUDIT-ZTA-001F security remediation candidate

**PROPOSED; owner review required.** A dedicated branch based on current `main`
and the audited PR #9 implementation fixes the conditional self-audit gate,
surfaces demonstrated static-source bypasses, blocks caller-selected authority
from producing ZTA-08.02 PASS, repairs adversarial fixtures, widens CI path
coverage, and tests resolved path containment. The new evidence and host
contract limitations are in `gc-audit/specifications/GC-AUDIT-ZTA-001F-SECURITY-REMEDIATION.md`.
The historical PLAY records and unrelated legacy ZT1–ZT8 behavior are
unchanged. No operational assurance, release, activation, or acceptance is
claimed. Exact-head hosted CI and owner review remain separate gates.

## 2026-10-28 — GC-AUDIT-PRODUCT-001 Gate 1 review candidate

**PROPOSED — requires AL:2 sign-off.** The dedicated Gate 1 branch adds a native, read-only `zta.library.v1` repository CLI and a digest-checked external `portal-kit` report at revision `a61f1ee5ab58f92cebe93e4da0e2d9ae4905afcb`. The evaluator returned 24 UNVERIFIED controls and BLOCKED release eligibility. The report, acceptance matrix, limitations, and reproduction steps are in `gc-audit/reports/portal-kit-gate1.md`. Local ZTA tests and schema fixtures pass; exact-head hosted CI and independent owner review remain required. The preflight stamp was late, and Level 1 validation retains the known REVIEW-GRAMMAR topology failure. No PASS closure, release, activation, or operational assurance is claimed. `AGENTS.md` was checked and its onboarding pointer remains current.

PR #12 code commit `1a447c6d3a97315f7a07f49412f4f7d9ec542e56` subsequently passed all 30 reported hosted checks, including Windows/Linux/macOS ZTA evaluator and registry matrices on Python 3.11/3.12. This is a proposed evidence update; AL:2 owner sign-off and merge remain pending.
