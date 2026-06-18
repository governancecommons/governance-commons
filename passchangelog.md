# PASSCHANGELOG — Governance Commons

Ecosystem-level governance decisions for the Governance Commons ecosystem.
For per-spec implementation changes, see each spec's own `passchangelog.md` and `CHANGELOG.md`.

ID format: GC-PASS-NNNN.NN (4-digit sequence — execution order). Newest first.

---

## Entry Formats

Use the format that matches `change_type`. Do not mix them.

---

### Format: build

For passes that create or extend something — new specs, schemas, rules, tooling.

```markdown
**pass_id**: GC-PASS-NNNN.NN
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
