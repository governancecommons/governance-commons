# Governance Commons — Multi-Agent STRIDE Threat Model

**Authority level:** AL:2
**Status:** Active
**Version:** 1.0.0
**Issued:** 2026-06-07T00:00:00Z
**Closes:** GC-3-B-06

---

## Purpose

This document applies the STRIDE threat modeling framework to multi-agent governance systems
conforming to the Governance Commons standards. It covers threats at the agent identity,
handoff envelope, orchestration, telemetry, and governance artifact layers.

Each STRIDE category maps to one or more concrete threats, paired with mitigations that
reference normative controls in the Governance Commons spec suite. Cross-references to
`agent-project-orchestrator/governance/multi-agent.yaml` threat entries (T-001 through T-006)
and `agent-dossier.yaml` threat entries are included where applicable.

---

## STRIDE Summary

| Category | Threat | Primary Control |
|----------|--------|-----------------|
| **S**poofing | Forged agent identity in handoff envelopes | Ed25519 signature + DID identity binding |
| **T**ampering | In-transit envelope modification; YAML injection | JWS signature over canonical payload; strict parser rules |
| **R**epudiation | Denial of issued handoffs or actions | PASS changelog + telemetry trace + signed envelopes |
| **I**nformation Disclosure | Secrets in telemetry or artifacts | Privacy rules; tool permission scoping |
| **D**enial of Service | Resource exhaustion; stall attacks | Resource budgets; anti-stall rules; orchestrator enforcement |
| **E**levation of Privilege | Capability overreach; prompt injection | Handshake declaration; runtime contract; authority hierarchy |

---

## S — Spoofing

Spoofing threats arise when an actor falsely claims the identity of a legitimate agent
or orchestrator.

### S-01: Forged `from_agent` in handoff envelopes

**Threat:** A malicious or compromised agent sets `from_agent` to another agent's `agent_id`
in a handoff envelope, causing the receiving agent to treat the forgery as legitimate work
from a trusted peer.

**Impact:** Unauthorized work delegation; bypassed authority checks; corrupted audit trail.

**Mitigations:**
- **Ed25519 signature on handoff envelopes** (`agent-dossier.yaml` `handoff_protocol.signature_block`,
  `schemas/handoff-envelope-signature.schema.json`): the `from_agent`'s signing key is bound to its
  declared `crypto_identity`; receivers MUST verify the signature before accepting the envelope.
- **DID-compatible identity binding** (`agent-dossier.yaml` `identity_block.crypto_identity`,
  `schemas/agent-dossier-instance.schema.json`): the `from_agent`'s public key is declared
  in its dossier; forging the `from_agent` field while providing a valid signature is
  computationally infeasible without the corresponding private key.
- **Dossier status check**: receivers MUST verify dossier status is `active` before accepting work
  (dossier_lifecycle rules). Revoked or expired dossiers are rejected at the gate.

**Related entries:** T-006 (multi-agent.yaml — prompt injection as identity confusion vector);
`capability_confusion` (agent-dossier.yaml threat_model).

---

### S-02: Impersonation of the orchestrator

**Threat:** A rogue agent issues orchestration commands (task assignments, handoff routing)
by impersonating the orchestrator, causing other agents to accept unauthorized work.

**Impact:** Unauthorized task execution; authority hierarchy bypass.

**Mitigations:**
- Orchestrator identity is declared in its own dossier with `agent_class: orchestration`.
  Agents SHOULD verify the orchestrator's dossier and `crypto_identity` before accepting
  new task assignments.
- All handoffs are routed through the orchestrator only (`multi-agent.yaml` `handoff.routing`).
  Peer-to-peer task delegation (`peer_to_peer: false`) prevents agents from injecting work
  directly.
- **Key-binding**: signed envelopes from the orchestrator carry its Ed25519 signature.
  Agents that store the orchestrator's public key can detect impersonation attempts.

---

## T — Tampering

Tampering threats arise when an attacker modifies data in transit or at rest to change
agent behavior without detection.

### T-01: In-transit handoff envelope modification

**Threat:** An attacker intercepts a handoff envelope and modifies fields such as
`to_agent`, `task_state`, `remaining_work`, or `artifacts` before delivery, redirecting
work or injecting false context.

**Impact:** Misdirected work; corrupted task state; false audit evidence.

**Mitigations:**
- **JWS signature over canonical payload** (`handoff_protocol.signature_block`): any
  modification of the signed payload invalidates the Ed25519 signature. Receivers MUST
  reject envelopes whose present signature fails verification.
- The canonical signing payload excludes the `signature` field and uses JSON with
  lexicographically sorted keys — this deterministic form prevents normalization attacks.

**Related entries:** T-002 (multi-agent.yaml — task queue corruption); `handoff_context_loss`
(agent-dossier.yaml threat_model).

---

### T-02: YAML injection into governance artifacts

**Threat:** Malicious content delivered as YAML input uses anchors, aliases, or duplicate
keys to cause parser confusion, silently overriding governance constraints.

**Impact:** Constraint bypass; unauthorized permission escalation through parser quirks.

**Mitigations:**
- **YAML governance block** (`agent-dossier.yaml` `yaml_governance_block`): anchors and
  aliases are **not allowed** (`allowed: false`); duplicate keys are **not allowed**.
  Parsers MUST reject documents that violate these rules.
- **Strict parsing lint rule** (`parsing_lint_rules`): `Parsers MUST reject duplicate keys`.
- Validator enforces these rules at activation time — a dossier that fails YAML governance
  MUST NOT be used to activate an agent.

**Related entries:** T-005 (multi-agent.yaml — schema injection).

---

### T-03: Governance artifact mutation without changelog

**Threat:** A governed artifact (dossier, schema, policy file) is modified without a
corresponding PASS changelog entry, creating a discrepancy between declared and actual state.

**Impact:** Silent policy drift; undetectable compliance violations; replay of stale artifacts.

**Mitigations:**
- **PASS changelog requirement** (`agent-dossier.yaml` `compliance_layer`):
  `pass_changelog_required_for_standard_changes: true`. Systems MUST record a PASS entry
  for every standard-level change.
- **Telemetry trace requirement**: `trace_required_for_runtime_mutations: true`. Runtime
  mutations emit a telemetry event with `event_type: action` or `event_type: decision`,
  preventing silent changes.
- **SHA-256 artifact hashes** (`reproducibility_block`): handoff envelope `artifacts` array
  carries optional `sha256` digests; receivers can detect artifact substitution.

**Related entries:** `audit_gap` (agent-dossier.yaml threat_model).

---

## R — Repudiation

Repudiation threats arise when an agent or human denies having performed an action that
affected the system, and no audit record exists to refute the denial.

### R-01: Agent denies issuing a handoff envelope

**Threat:** An agent claims it did not emit a handoff envelope that caused downstream
actions, particularly if the envelope contained erroneous or harmful instructions.

**Impact:** Unaccountable delegation; audit gaps in incident response.

**Mitigations:**
- **emitted_at timestamp** (DDR-6, `handoff_protocol.timestamp_rules`): the RFC3339 UTC
  `emitted_at` field creates a temporal record at transmission; timestamp is required and
  MUST be set by the emitting agent.
- **Ed25519 signature** (`signature_block`): when present, the signature cryptographically
  binds the envelope to the from_agent's private key. An agent cannot repudiate a validly
  signed envelope without claiming key compromise.
- **Telemetry event** (`telemetry_trace_schema`): `event_type: handoff` is emitted by the
  sending agent at transmission; this event is part of the immutable audit trail.

---

### R-02: Missing PASS entry for a material governance change

**Threat:** A governance change is applied without a PASS entry, making it impossible to
determine when, by whom, and why the change was made.

**Impact:** Incomplete audit trail; compliance certification failure.

**Mitigations:**
- PASS changelog entries are **required** for all standard-level changes. Any PASS entry
  MUST carry `pass_id`, `timestamp`, `specification_version`, `change_type`, `summary`,
  `authoring_agent`, and `compatibility_impact` (`pass_changelog_schema`).
- Ecosystem-level decisions require GC-PASS entries in `passchangelog.md` at the
  governance-commons root (AL:2).
- **Telemetry event**: `event_type: pass_written` is emitted when a PASS entry is recorded,
  adding a second independently verifiable record.

---

## I — Information Disclosure

Information disclosure threats arise when an agent leaks sensitive data — credentials,
PII, business logic, or internal system state — through telemetry, handoff artifacts,
or error messages.

### I-01: Secrets in telemetry events

**Threat:** An agent emits tool call outputs, environment variables, or intermediate
computation results through `telemetry.emit()` that contain API keys, tokens, or PII.

**Impact:** Credential exposure; compliance violation (GDPR, SOC 2); secret rotation overhead.

**Mitigations:**
- **Privacy rules** (`telemetry_trace_schema.privacy_rules`):
  - `minimize_sensitive_data: true` — agents MUST minimize what is included in telemetry.
  - `redact_secrets: true` — secrets MUST be redacted before emission.
  - `record_policy_basis: true` — any data inclusion decision MUST record its policy basis.
- Tool permission scoping (`tool_permissions`): agents may only access approved scopes.
  This limits the surface area of data an agent can encounter and potentially leak.

**Related entries:** T-006 (multi-agent.yaml — prompt injection as a data exfiltration vector).

---

### I-02: Sensitive content in handoff envelope artifacts

**Threat:** A handoff envelope's `artifacts` array or `assumptions`/`risks` fields contain
literal secret values, internal system paths, or user-identifiable information passed to
a downstream agent.

**Impact:** Secret propagation across trust boundaries; PII in audit records.

**Mitigations:**
- The `artifacts` array carries **references** (path + version + optional sha256), not
  artifact content. Agents MUST NOT embed raw file contents in envelope fields.
- Agents MUST apply the same `redact_secrets` rule to envelope fields as to telemetry.
- **Principle of least context**: handoff envelopes SHOULD include only the context
  necessary for the receiving agent to continue the task.

---

## D — Denial of Service

Denial-of-service threats arise when an agent consumes excessive resources (compute,
tokens, time, API calls) or enters a stall state, preventing legitimate work from
completing.

### D-01: Runaway agent resource exhaustion

**Threat:** An agent enters an unbounded retry loop, generates extremely long outputs,
or issues excessive tool calls, consuming all available compute budget and blocking other
agents.

**Impact:** Task queue starvation; cost overrun; orchestrator instability.

**Mitigations:**
- **Per-agent resource budget** (`resource_budget` in agent-dossier-instance):
  `retry_limit`, `time_limit`, `token_limit`, `tool_call_limit`, `cost_limit` are
  declared per agent and MUST be enforced by the orchestrator.
- Orchestrator kills agents that breach their resource budget (T-004, multi-agent.yaml).
- **Bounded retries rule** (`anti_stall_rules`): `Retry loops MUST have explicit limits
  and failure handling`.

**Related entries:** T-004 (multi-agent.yaml — runaway agent); `resource_exhaustion`
(agent-dossier.yaml threat_model).

---

### D-02: Agent stall attack

**Threat:** An agent halts all progress (e.g., waits on an external dependency that never
resolves) without emitting heartbeats or escalating, holding a task slot indefinitely.

**Impact:** Task queue deadlock; silent work loss; orchestrator unable to reassign task.

**Mitigations:**
- **Anti-stall rules** (`anti_stall_rules`): `no_silent_waiting` — agents MUST NOT wait
  indefinitely without recording a polling or escalation policy.
- **Max idle time** (`multi-agent.yaml` `anti_stall.max_idle_ms`): stall detection fires
  after `max_idle_ms`; heartbeat interval enforces liveness.
- **On-stall response** (`anti_stall.on_stall`): emit stall event → request next task
  from orchestrator → escalate if no response after 5000ms.
- `explicit_blockers` anti-stall rule: agents MUST identify the blocking fact and required
  input before declaring blocked.

**Related entries:** T-003 (multi-agent.yaml — agent stall).

---

### D-03: Task queue corruption blocking all agents

**Threat:** The task queue (`tasks/task-queue.json`) is corrupted or hand-edited,
causing the orchestrator to produce invalid task assignments or enter an error loop
that prevents any task from being dispatched.

**Impact:** Complete work stoppage; orchestrator restart required.

**Mitigations:**
- `task-queue.json` is a **compiled artifact** — it is always regenerated by
  `compile_task.py` from DevPath + Tracks and MUST NOT be hand-edited (T-002,
  multi-agent.yaml).
- Schema validation on load: the orchestrator validates the task queue on boot; a
  corrupt queue triggers level-2 escalation rather than silent operation with bad state.

---

## E — Elevation of Privilege

Elevation of privilege threats arise when an agent obtains capabilities or authority
beyond what its dossier declares, enabling it to take actions that should require
higher authority.

### E-01: Capability overreach via forged capability declaration

**Threat:** An agent declares an `authority_scope` or `tool_permissions` in its
runtime contract that exceeds what is authorized in its dossier, then exercises those
inflated capabilities.

**Impact:** Unauthorized file system access; unauthorized API calls; governance artifact
mutation.

**Mitigations:**
- **Runtime contract enforcement**: the orchestrator loads the agent's runtime contract
  and validates it against the dossier. Contracts that grant permissions absent from
  the dossier MUST trigger a level-3 compliance stop (T-002 escalation in agent-c,
  multi-agent.yaml).
- **Handshake capability declaration** (`handshake_specification`): the agent declares
  `agent_class`, `authority_scope`, and `tool_permissions` at handshake time; the
  orchestrator MUST verify these against the active dossier before accepting work.
- **Default-deny permission model** (`tool_permissions`): `default: deny`;
  `explicit_allow_required: true`; `least_privilege_required: true`.

**Related entries:** `capability_confusion` (agent-dossier.yaml threat_model).

---

### E-02: Prompt injection bypassing authority hierarchy

**Threat:** Content ingested from an external source (web page, user input, tool output)
contains instructions that cause the agent to act outside its declared authority scope
or violate governance constraints.

**Impact:** Authority hierarchy bypass; unauthorized actions taken on behalf of the agent;
governance artifact mutation without PASS entry.

**Mitigations:**
- **Authority hierarchy preservation** (`agent_agreement`): agents MUST preserve the
  user → operator → system authority hierarchy. External content MUST be treated as
  data, not instructions.
- **Record suspicious instruction conflicts**: agents MUST log instruction conflicts in
  telemetry as `event_type: escalation` with `severity: warning` or higher.
- **Compliance stop** (`escalation_protocol` level 3): if prompt injection is suspected
  to have caused a policy-violating action, the agent MUST stop and preserve the audit
  trail.
- Treat untrusted content as data: the `prompt_injection` threat entry in
  `agent-dossier.yaml` and T-006 in `multi-agent.yaml` both establish this as a
  first-class mitigation.

**Related entries:** T-006 (multi-agent.yaml — prompt injection); `prompt_injection`
(agent-dossier.yaml threat_model).

---

### E-03: Orchestrator authority usurpation via forged runtime contract

**Threat:** A compromised agent delivers a modified `runtime-contract.yaml` to the
orchestrator claiming permissions that include orchestration-level authorities (e.g.,
`agent_class: orchestration`, broad `authority_scope`).

**Impact:** Full orchestrator-level privilege for an unauthorized agent.

**Mitigations:**
- **Runtime contract version check** (`multi-agent.yaml` escalation level 3 for agent-b):
  `Contract grants permissions absent from dossier → Halt and preserve audit trail`.
- `specification_version` in the runtime contract MUST match the dossier's declared version;
  mismatches trigger level-2 escalation (T-001, multi-agent.yaml).
- Dossier-level authority cannot be escalated through the runtime contract — the runtime
  contract is a compiled subset of the dossier, not an extension of it.

---

## Cross-Reference Index

### multi-agent.yaml threat entries

| ID | Description | STRIDE category | Section above |
|----|-------------|-----------------|---------------|
| T-001 | Agent contract drift | E | E-03 |
| T-002 | Task queue corruption | T, D | T-03, D-03 |
| T-003 | Agent stall | D | D-02 |
| T-004 | Runaway agent | D | D-01 |
| T-005 | Schema injection (YAML) | T | T-02 |
| T-006 | Prompt injection | S, E | S-01, E-02 |

### agent-dossier.yaml threat_model entries

| ID | STRIDE category | Section above |
|----|-----------------|---------------|
| prompt_injection | S, E | S-01, E-02 |
| capability_confusion | E | E-01 |
| handoff_context_loss | T | T-01 |
| audit_gap | R, T | R-02, T-03 |
| resource_exhaustion | D | D-01, D-02 |

---

## Residual Risk and Open Items

The following threats are acknowledged but not fully mitigated by PASS-2 controls.
They are tracked for resolution in later PASSes.

| Threat | Gap | Target PASS |
|--------|-----|-------------|
| Key distribution — how do receivers obtain and trust from_agent public keys? | No public key infrastructure or key registry defined yet | PASS-3 (GC-3-A-03 zero-trust spec) |
| Key revocation — if an agent's private key is compromised, how is the public key revoked? | Dossier revocation model exists but no real-time revocation signal | PASS-2 (GC-3-A-03) |
| Transport-layer threats (eavesdropping, replay across sessions) | No transport binding defined yet | PASS-3 (101-G1c) |
| Federated trust — cross-cluster agent identity verification | No federation model | PASS-6 (GC-4-B-01) |

---

*This document is authoritative at AL:2. Changes require a GC-PASS entry.*
