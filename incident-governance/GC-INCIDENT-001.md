# GC-INCIDENT-001 — AI Incident Governance

Version: 0.1.0 (implementation draft)
Status: Owner-approved scope; not yet adopted or released in the repository
Date: 2026-11-03

## 1. Purpose and boundaries

GC-INCIDENT-001 specifies an interoperable, machine-readable record for governance of incidents involving AI systems. It governs classification, human accountability, evidence references, material decisions, response actions, reporting, recovery, and closure. It does not detect attacks, execute containment, provide a SIEM/SOAR, replace legal reporting obligations, or certify compliance with external standards.

## 2. Classification

`incident_type` MUST be one of `against_ai`, `caused_by_ai`, `combined`. `combined` indicates both domains, not necessarily proven causation. The record MUST distinguish observed facts, allegations, and hypotheses. Severity is local to the reporting organization; `severity_rationale` MUST explain the assignment. `unknown` severity is permitted during triage.

## 3. Lifecycle

States: `reported`, `triaged`, `active_response`, `recovery_monitoring`, `closed`, `dismissed`. Transitions MUST be recorded as append-only material decisions with timestamp, authority and rationale. A closed incident MAY be reopened by recording a transition to `active_response` or `triaged`; earlier history MUST be preserved. A dismissed report MUST record the dismissal rationale. Status is a snapshot, not a substitute for event history.

## 4. Normative requirements

- INC-001: Records MUST classify AI involvement as against, caused, or combined.
- INC-002: Active incidents MUST identify an accountable human or organization, including an authority identifier; automated agents cannot self-approve elevated actions.
- INC-003: Evidence references MUST identify the source, integrity status, and access classification. Confidential content SHOULD remain outside the incident record.
- INC-004: Elevated containment and recovery actions MUST record authorizing human authority, decision reference, and execution outcome; proposals alone are not execution evidence.
- INC-005: Material state changes and decisions MUST have immutable identifiers, times, and rationale; implementations SHOULD provide append-only storage and tamper-evidence beyond schema validation.
- INC-006: External reports MUST record the applicable profile/version, destination, status, and disclosure authority. Export is not proof of regulatory fulfillment.
- INC-007: Evidence and public reports MUST apply privacy and least-disclosure controls; the incident record MUST NOT embed credentials or sensitive forensic payloads.
- INC-008: Closure MUST include outcome, residual risks, approval reference and lessons learned, even if some fields remain unknown.
- INC-009: Related GC artifacts MUST be referenced by stable identifiers/URIs, not copied into the incident record.
- INC-010: Uncertainty MUST be explicit; unknown, unavailable, not-applicable, unverified, and confirmed are distinct concepts.

## 5. Validation and enforcement

The JSON Schema validates structural requirements and a limited set of conditional invariants. The semantic validator MUST additionally check: valid lifecycle transitions and chronological decision history; action authorization and execution evidence; immutable event IDs; evidence access and hash verification where available; reporting profile version and authorization; closure approval and non-empty lessons; consistency between incident type and findings; and that no secrets are embedded. Runtime authorization and storage immutability require external controls and cannot be proven by JSON Schema alone.

## 6. Compatibility

Existing Governance Record, Agent Dossier, Agent Matrix, Agent Team Protocol, Observatory Core, Portal, and ConformanceReport remain unchanged. `related_gc_artifacts` holds references. The existing ConformanceReport may carry validation results by setting `spec=gc-incident` and `spec_version=0.1.0` after a validator exists. No automatic integration is implied.

## 7. Standards mapping caveat

NIST IR 8621 informs AI-specific incident-management challenges but is not itself a mandatory conformance standard. NIST SP 800-61 Rev. 3 supplies incident-response process guidance; this governance record alone does not implement operational response. OECD reporting and ISO/IEC 25870 require separate source-verified mapping work before claiming field-level conformance.

## 8. Release acceptance

Three examples (against, caused, combined) validate. Invalid fixtures fail. Semantic checks pass. A mapping file distinguishes support from gaps. Backward compatibility is maintained. Owner approval is required for release.
