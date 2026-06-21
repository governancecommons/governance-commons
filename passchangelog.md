# PASSCHANGELOG — Governance Commons

Ecosystem-level governance decisions for the Governance Commons ecosystem.
For per-spec implementation changes, see each spec's own `passchangelog.md` and `CHANGELOG.md`.

ID format: GC-PASS-NNNN.NN (4-digit sequence — execution order). Newest first.

**PASS structure:**

- `NNNN.00` — **Primary Pass.** Always required. Defines the intent, scope, success criteria, inputs, and outputs for the entire pass family. Every sub-pass and compound pass hangs off this anchor.
- `NNNN.01` – `NNNN.09` — **Sub-passes.** Discrete work items within the primary pass scope.
- `NNNN.10` – `NNNN.99` — **Compound passes.** A cluster of sub-passes that must be grouped together.

A bare `GC-PASS-NNNN` (no decimal suffix) is always wrong. Do not write it.

**Timestamp requirement:** Every PASS entry must include a `**timestamp**` field in ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`). This is mandatory — no PASS entry is complete without it. Agents must record the actual time of the decision, not omit it.

---

## Entry Formats

Use the format that matches `change_type`. Do not mix them.

---

### Format: build

For passes that create or extend something — new specs, schemas, rules, tooling.

```markdown
**pass_id**: GC-PASS-NNNN.NN
**timestamp**: YYYY-MM-DDTHH:MM:SSZ
**change_type**: build
**authority_level**: AL:1 | AL:2 | AL:3
**status**: ACCEPTED
**affected_surfaces**: (specs, schemas, agents, or tooling that now depend on this)

**what**: (the artifact, field, rule, or behavior that now exists)
**why**: (the trigger — the gap, requirement, or contradiction that made this necessary)
**new_constraints**: (rules future passes must respect because of this — or "none")
**reasoning**: (what was weighed, what was rejected, what prevents this from being undone carelessly)
```

---

### Format: fix

For passes that resolve a problem — bugs, contradictions, drift, bad prior decisions.

```markdown
**pass_id**: GC-PASS-NNNN.NN
**timestamp**: YYYY-MM-DDTHH:MM:SSZ
**change_type**: fix
**authority_level**: AL:1 | AL:2 | AL:3
**status**: ACCEPTED
**affected_surfaces**: (what was broken and what else was touched to fix it)

**problem**: (what was wrong)
**why_problem**: (why it matters — the actual consequence if left unfixed)
**fix_approach**: (what the right fix is and why that approach over alternatives)
**what_was_done**: (the concrete change made)
**prevention**: (what now exists or must be done to stop this class of problem recurring)
```

---

### Format: governance

For passes that open/close phases, register authority decisions, or record ecosystem-level rulings.

```markdown
**pass_id**: GC-PASS-NNNN.NN
**timestamp**: YYYY-MM-DDTHH:MM:SSZ
**change_type**: governance
**authority_level**: AL:1 | AL:2 | AL:3
**status**: ACCEPTED
**affected_surfaces**: (what this decision governs or constrains)

**summary**: (what was decided and why — include scope, what was opened/closed, and any new constraints)
**new_constraints**: (rules future passes must respect because of this — or "none")
```

---

## GC-PASS-0009.00 — 2026-06-20

**pass_id**: GC-PASS-0009.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (ECO: and GC: namespaces, CANON cluster complete), eco (ECO: namespace, initial registry)

**what**: CANON.03 accepted as the Migration Protocol for eco and GC as CANON first-adopters. Formally reverses unauthorized named-cluster-only rule (agent drift, pre-2026-04-12, ACES.01 Inv#6 and Inv#14 violated, no governance record). Declares ECO: namespace (prefix ECO, owner jj-ervin, authority jj-ervin, 5 active layer bands: authority 0000-0999, operational 1000-1999, domain 2000-2999, platform 3000-3999, data-interop 4000-4999, reserved 9000-9999). Declares GC: namespace (prefix GC, owner jj-ervin, authority jj-ervin, 4 active layer bands: authority 0000-0999, operational 1000-1999, standards 2000-2999, platform 3000-3999, reserved 9000-9999). Declares assignment algorithm (8 rules A-1 through A-8 governing layer-band mapping, chronological ordering, cluster-header priority, legacy supersession, gap permission). Declares legacy ID mapping rules and conflict resolution rules (4 rules C-1 through C-4). Assigns GC: canonical IDs: GC:0001 (GC.00 charter), GC:1001-1002 (APO.00, ATP.00), GC:2001-2004 (CANON.00-03), GC:2005-2007 (ONS.00-02). Assigns ECO: canonical IDs: ECO:0001-0007 (ACES.00-06), ECO:1001-1003 (OG.00-02), ECO:1004-1007 (RT.00, EV.00, OPS.00, REM.00). Resolves CANON bootstrap condition: GC:2004 = CANON.03 (self-assigned, explicitly authorized and documented). Declares follow-on implementation task for remaining ~150+ eco PASSes, governed by A-1 through A-8 with no additional governance PASS required. Produces companion artifacts: governance-commons/passes/{namespace.yaml, layers.yaml, passes.registry.json, passes.registry.changelog.jsonl} (GC: namespace, 10 initial entries); eco/passes/{namespace.yaml, layers.yaml, passes.registry.json, passes.registry.changelog.jsonl} (ECO: namespace, 14 initial entries). CANON cluster is now complete: CANON.00-03 accepted, GC:2001-2004 assigned, bootstrap resolved.
**why**: CANON.00-02 established the canonical identifier standard but could not assign IDs (bootstrap condition). CANON.03 is the authorized migration act that executes the first-adopter assignments and formally closes the drift issue that prompted CANON's creation. Without CANON.03, the system remains in the bootstrap state — the standard exists but no canonical IDs are assigned.
**new_constraints**: All future ECO: and GC: assignments must follow Rules A-1 through A-8. Legacy ID mapping rules govern how legacy numbered forms are preserved. The follow-on migration task for remaining eco PASSes requires allocation authority authorization per assignment block (R-AA-1). No canonical IDs may be assigned outside a migration PASS or its follow-on continuation artifact. The OPS.00 duplicate-supersedes typo in CANON.03 line 479 was corrected before commit; the registry (passes.registry.json) has the correct entry.

---

## GC-PASS-0008.00 — 2026-06-20

**pass_id**: GC-PASS-0008.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (all adopters), passes/canon/CANON.02.md, schemas/canon-registry-entry.schema.json

**what**: CANON.02 accepted as the normative Registry Governance specification. Declares: registry file format (JSON required, YAML permitted; passes.registry.json naming; one file per namespace; entries array is sole authority); full entry schema (14 required fields: id, alias, legacy_ids, title, layer, cluster, parent, status, timestamp, path, supersedes, superseded_by, depends_on, originating_pass; 6 optional standard fields; extension model via lowercase namespace-prefixed keys); status taxonomy (proposed, draft, accepted, sealed, superseded, reserved; 4 transition rules; superseded is terminal); write authority enforcement (allocation_authority from namespace.yaml; agents require authorizing PASS for binding writes; changelog written atomically; automation authorized by PASS; extends GC-CONSTRAINT-001 to registry writes); schema validation contract (11 pre-write checks; CRITICAL/ERROR/WARN error taxonomy); append-only changelog (.jsonl format; 5 required fields; 5 action values; CI-enforced append-only); CI integration contract (9 required checks; violation reporting format; build fails on CRITICAL/ERROR); dependency validation (same-namespace MUST resolve; cross-namespace via external_registries; superseded dependency is WARN; circular deps are CRITICAL; known_superseded_dependencies suppression); registry-as-governed-artifact (version control is provenance; every write traceable to PASS; schema changes require CANON amendment; $canon_version mismatch is CRITICAL). Companion artifact published: schemas/canon-registry-entry.schema.json (JSON Schema draft/2020-12, additionalProperties: true for extensions). 44 normative rules across 9 rule families.
**why**: CANON.01 specified how identifiers are formed and governed; CANON.02 specifies how the registry that records those identifiers is structured, validated, and protected as governed infrastructure. Without CANON.02, an adopter has rules for IDs but no governed place to store them.
**new_constraints**: All CANON-conformant registries must declare $canon_version: CANON.02. Agents must not write binding registry entries without an authorizing PASS (R-WA-2). Changelog is append-only (R-CL-2). CI must run all 9 required checks on registry-touching commits (R-CI-1 through R-CI-9). Schema file changes require a CANON amendment PASS (R-GA-3).

---

## GC-PASS-0007.00 — 2026-06-20

**pass_id**: GC-PASS-0007.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (all adopters), passes/canon/CANON.01.md

**what**: CANON.01 accepted as the normative PASS Identifier Governance specification. Declares canonical ID grammar (^[A-Z]{2,6}:[0-9]{4}$, ABNF, 7 validity rules), ONS conformance rule (NAMESPACE matches governance_cluster pattern; canonical ID is conformant specialization of qualification_authority), namespace declaration specification (namespace.yaml, 8 required fields, 4 ownership rules), layers declaration specification (layers.yaml, 3 required fields per entry, 7 normative rules, ECO: reference grammar as informative), alias model (named-cluster and legacy alias types, namespace-scoped resolution, 4-step resolver protocol, 6 rules), allocation authority model (traceability, delegation, range reservation, 7 rules), sub-pass relationship model (flat IDs only, parent and cluster as registry fields, 5 rules), immutability specification (immutable at assignment not at sealing, 4-step supersession protocol, 7 rules), and normative requirements summary (37 rules across 7 rule families).
**why**: CANON.00 declared the format and principles; CANON.01 is the normative external-facing specification that adopting organizations implement. Without CANON.01, adoption requires inferring rules from CANON.00's prose — producing inconsistent implementations.
**new_constraints**: All canonical ID assignments MUST conform to R-ID-1 through R-ID-7. Alias resolution MUST be namespace-scoped (R-AL-6). ID assignments MUST trace to a PASS decision (R-AA-1). Superseded PASSes MUST remain in the registry permanently (R-IM-6). CANON.02 (registry governance) is required before any conformant registry can be declared complete.

---

## GC-PASS-0006.00 — 2026-06-20

**pass_id**: GC-PASS-0006.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (all adopters), eco (first organizational adopter), registry/clusters.yaml, passes/canon/CANON.00.md

**what**: CANON cluster established. CANON.00 accepted as the founding record of the Canonical PASS Identifier Standard. Declares the canonical ID format (NAMESPACE:NNNN), alias model (named cluster IDs are ergonomic aliases, never stable citation targets), immutability rule (IDs never move or are reused — mistakes corrected by supersession), layer band grammar (per-namespace declaration; ECO: reference grammar: 0000s authority, 1000s operational, 2000s domain, 3000s platform, 4000s data/interop, 9000s reserved), registry minimum model (id, alias, legacy_ids, title, layer, cluster, parent, status, timestamp, path, supersedes, superseded_by, depends_on), external adopter model (self-declared prefix, no GC registration required), and 8 cluster invariants (CANON-CI-1 through CANON-CI-8). CANON cluster registered in registry/clusters.yaml. Four-PASS cluster structure declared: CANON.00 (header), CANON.01 (ID governance), CANON.02 (registry governance), CANON.03 (eco migration). Bootstrap condition acknowledged: CANON.00 has no canonical ID until CANON.03 assigns it.
**why**: Two compounding failures required a governing standard: (1) unauthorized agent drift — the named-cluster-only rule in eco's PASS-INDEX was written without a governing decision or founder sign-off; (2) portability gap — named cluster identifiers (ACES.01, OG.02) are opaque outside eco, making PASS records non-portable for external GC adopters. Neither failure could be resolved by a passchangelog entry alone.
**new_constraints**: All future PASS identifier assignments must follow CANON-CI-8 (migration is governed — no casual number assignment outside a migration PASS). The registry is a governed artifact per CANON-CI-5. No canonical IDs may be assigned until CANON.01 and CANON.02 are accepted and CANON.03 executes migration.

---

## GC-PASS-0005.00 — 2026-06-07

**pass_id**: GC-PASS-0005.00
**change_type**: governance
**authority_level**: AL:2
**summary**: PASS-2 Batch 2 delivery. Closed GC-3-A-03 (zero-trust spec).
Published `governance/zero-trust.yaml` — the normative zero-trust security
specification for Governance Commons multi-agent systems. Covers three pillars:
(1) Establishment — four-phase per-interaction trust protocol (dossier retrieval,
status/expiry validation, public key extraction from crypto_identity.did or
public_key, Ed25519 JWS signature verification against canonical payload) with
caching rules (TTL 300s, mandatory re-validation on each use, immediate
invalidation on revocation signal); (2) Rotation — re-key event procedure
(new key generation, dual-sign transition envelope proving identity continuity,
PASS entry with change_type security, telemetry registry_updated event,
24-hour transition window, secure old-key deletion); rotation triggers
(scheduled 90-day recommended / 365-day maximum, operator-directed,
algorithm-deprecation); (3) Revocation — five triggers (compromised,
decommissioned, authority_withdrawn, superseded, policy_violation), six-step
procedure (immediate signing halt, dossier status → revoked, PASS entry,
propagation, in-flight envelope rejection, session termination), 30-second
clock-skew tolerance for revocation timestamp. Key material handling rules
(no private key in artifacts, secure storage, single-use-per-agent, CSPRNG
requirement, secure deletion). Conformance profiles (advisory / standard /
strict) with per-level enforcement requirements. Residual risks table pointing
to PASS-3 key registry, real-time revocation, and transport binding work.
**status**: ACCEPTED
**affected_specs**: governance-commons

---

## GC-PASS-0004.00 — 2026-06-07

**pass_id**: GC-PASS-0004.00
**change_type**: governance
**authority_level**: AL:2
**summary**: PASS-2 Batch 1 delivery. Closed GC-3-A-01 (handoff envelope JWS/Ed25519
signature schema), GC-3-A-02 (agent identity DID-compatible binding), and GC-3-B-06
(STRIDE threat model for multi-agent systems). Agent-dossier spec advanced to v1.3.0:
new `crypto_identity` block in identity_block (did or public_key in base58btc/multibase);
new `signature_block` in handoff_protocol (EdDSA algorithm, protected_header, signature,
key_hint; strict profile mandates signature on all envelopes); updated schemas
(`agent-dossier-instance.schema.json`, `handoff-envelope.schema.json`) and new
`handoff-envelope-signature.schema.json`. Governance Commons root: `governance/`
directory created; `governance/threat-model.md` published covering all six STRIDE
categories (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service,
Elevation of Privilege) with concrete multi-agent threat entries, normative mitigations
cross-referenced to agent-dossier spec and multi-agent.yaml (T-001 through T-006),
and a residual risk table pointing to PASS-3 zero-trust key infrastructure work.
**status**: ACCEPTED
**affected_specs**: agent-dossier, governance-commons

---

## GC-PASS-0003.00 — 2026-06-07

**pass_id**: GC-PASS-0003.00
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

## GC-PASS-0002.00 — 2026-06-05

**pass_id**: GC-PASS-0002.00
**change_type**: governance
**authority_level**: AL:2
**summary**: Established unified per-repo planning structure across all four core spec repos. Each spec (agent-dossier, agent-matrix, ons, agent-project-orchestrator) now has DEV-PATH.md, DEV-PLAN.md, TRACKS.md, and passchangelog.md under AL:1 authority. Stale planning files in agent-project-orchestrator (DevPath-v1.0.md, DevPlan-v1.0.md, Tracks.md) replaced with canonical-format equivalents. ROADMAP.md in agent-dossier retired; deferred items carried forward in agent-dossier DEV-PLAN.md.
**status**: ACCEPTED
**affected_specs**: agent-dossier, agent-matrix, ons, agent-project-orchestrator

---

## GC-PASS-0001.00 — 2026-06-05

**pass_id**: GC-PASS-0001.00
**change_type**: governance
**authority_level**: AL:2
**summary**: Governance Commons ecosystem planning infrastructure declared. DEV-PATH.md (ecosystem phases, authority model, design decisions DDR-1 through DDR-5), DEV-PLAN.md (execution plan, gap analysis checklist, charter and process), TRACKS.md (portfolio overview, dependency map), projects.yaml (machine-readable project registry with compat: fields), tools/gc-status.ps1 (status dashboard), docs/ (charter, architecture, rfc, conformance), and tools/ directory structure established at governance-commons root. PASS-0 bootstrap phase initiated. Five design decisions from source_102 answered and recorded as binding AL:2 decisions.
**status**: ACCEPTED
**affected_specs**: governance-commons

---

## GC-PASS-0006.00 — 2026-06-16

**pass_id**: GC-PASS-0006.00
**change_type**: governance
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons profiles/, dxp-org/dvp (new repo unblocked)

**what**: PASS-6 formally opened. Scope: optional category-defining profiles and the Doc Vault
Plane (DVP) capability track. gc.profile.doc-vault v0.1.0 (committed 2026-06-15, 674ac0f) is
accepted as the PASS-6 seed artifact. DVP repository creation is now unblocked.

**why**: gc.profile.doc-vault was developed and committed during the Osprey LLC vault setup
session on 2026-06-15. The work proved that GC profiles for non-code repositories are viable
and that document governance is an accessible adoption wedge. PASS-6 scope was fully documented
in DEV-PLAN.md (added 2026-06-15) but could not begin formally without AL:2 sign-off.
The OSS baseline is frozen at PASS-5 Batch 2; PASS-6 extends without modifying it.

**new_constraints**:

- All PASS-6 profiles must use "aligned with," "informed by," "supports readiness for" language.
  No profile may claim compliance, certification, or audit-readiness.
- Validator code belongs in DCP, not in GC profile definitions.
- gc.profile.code-repo must reconcile with existing agent-dossier/agent-matrix work before build.
- gc.profile.agent-vault scope must be evaluated as a sub-component of all profiles vs.
  standalone before committing to a standalone build.
- DVP is a separate product from DCP; it must not modify DCP or absorb DCP scope.

**reasoning**: The PASS-6 boundary (optional profiles as extensions, not baseline changes)
was established during the OSS freeze decision (2026-06-09, PASS-5 Batch 2). Opening PASS-6
does not reopen the baseline. The Osprey session proved the doc-vault concept end-to-end with
a real entity — that is sufficient evidence to open the track. DVP creation was explicitly
listed as blocked on this sign-off; unblocking it was the primary trigger for this entry.

---

<!-- New entries go above this line, newest first -->
