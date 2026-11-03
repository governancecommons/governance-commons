# GC-INCIDENT-001 — AI Incident Governance

Version: 0.1.0 (draft) | Status: Proposed | Authority: Owner-approved development scope, not ratified standard

## Purpose
Provide a portable, auditable incident-governance record for attacks against AI, incidents caused or contributed to by AI, and combined incidents. This contract governs decisions and evidence; it does not perform containment.

## Requirements
- INC-001: Classify incidents as against_ai, caused_by_ai, or combined; preserve uncertainty.
- INC-002: Identify an accountable human or organization for active response.
- INC-003: Reference evidence by identifier, source and integrity metadata when available; never require secret contents inline.
- INC-004: Record authorizer and authorization status for elevated containment or recovery actions. Proposed actions are not executed actions.
- INC-005: Preserve material decisions, status transitions, timestamps and provenance.
- INC-006: Identify external reporting profile, destination and authorization when a report is issued.
- INC-007: Protect sensitive incident evidence; do not publish evidence by default.
- INC-008: Require outcome, residual-risk disposition and accountable closure for closed incidents.
- INC-009: Reference existing GC agent, governance and conformance artifacts without redefining them.
- INC-010: Distinguish observed facts, allegations, estimates and confirmed findings.

## Lifecycle
reported → triaged → active_response → recovery_monitoring → closed. A documented dismissal is permitted for false positives. Reopening requires a new auditable decision. Status is a snapshot; operational enforcement and transition validation require semantic checks.

## Boundaries
NIST IR 8621 informs the AI-specific threat model and incident-management research; NIST SP 800-61 Rev. 3 informs incident-response governance. Neither document is claimed to mandate these exact fields or lifecycle states. OECD and ISO/IEC 25870 reporting adapters are deferred.

## Acceptance
Schema, three valid example scenarios, invalid-case tests, source-mapped NIST crosswalks, and repository CI must be verified before release. No live monitoring, automated containment or portal UI is included.
