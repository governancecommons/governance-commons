# GC-AUDIT HCI and Accessibility — Research Baseline v0.1

Status: DRAFT / RESEARCH ONLY. Not approved, registered, executable, or a conformance claim.
Initiatives: GC-AUDIT-HCI-001, GC-HCI-RESEARCH-001, GC-HCI-SPEC-001 (pending), GC-AUDIT-A11Y-001 / GC-A11Y-MAPPING-001 (pending).
Date: 2026-10-27.

## Purpose
Preserve in Git the source inventory, preliminary research-to-criterion mapping, methodology and accessibility-scoping decisions developed in the Governance Commons discussion. This checkpoint intentionally adds NO active operation to `GC-AUDIT-REGISTRY.yaml`, changes no schema or validation logic, and executes no audits.

## Contents
- `SOURCES.md`: eight uploaded research PDF references, bibliographic status, strengths and limitations.
- `HCI-TRACEABILITY-v0.1.md`: fifteen candidate HCI evaluation criteria, procedures, evidence and limits.
- `A11Y-SCOPE-v0.1.md`: separate accessibility audit scoping and normative research plan.

## Existing GC integration (preliminary inspection)
`gc-audit/README.md` identifies the central tool registry; `gc-audit/CONTRACTS.md` describes structured `gc-audit.result.v1` and PLAY record requirements; `gc-audit/GC-AUDIT-REGISTRY.yaml` owns allowlisted operations and security controls. No HCI/A11Y executable command or registry entry is introduced here. Before implementation, verify schema suitability, evidence handling, time_loc conventions, historical amendment semantics, and applicability of existing approval/authorization contracts. Do not assert compatibility on name alone.

## Research discipline
Maintain: Source → Claim → Evidence assessment → Operational definition → Procedure → Criterion → Validation → Versioned publication.
Distinct evidence classes: NORMATIVE (applicable binding standard/contract), EMPIRICAL (method-specific study), SYNTHESIS (research/practice interpretation), PRACTITIONER (guidance). A source paragraph is not a validated audit procedure. A heuristic judgment is not observed participant behavior. Not finding a problem is not evidence of conformance.

## Proposed status and outcomes
Research lifecycle: SOURCE_VERIFIED → CLAIM_ASSESSED → PROCEDURE_VALIDATED → CRITERION_APPROVED. These are proposed labels, not an implemented state machine.
Candidate evaluation outcomes: PASS, FAIL, REVIEW_REQUIRED, NOT_TESTED, NOT_APPLICABLE, INCONCLUSIVE. Final semantics must be reconciled against current machine-readable GC contracts before any schema changes.

## Explicit non-goals
No scores, certifications, WCAG conformance assertions, user-study claims, legal determinations, repository dependencies, operational tools, UI implementation, or changes to ZTA/AMD scope.

## Completion and next acceptance gate
This commit is a documented draft baseline only. Next: verify original passage-level references and contemporary standards; specify test protocols and evaluator agreement; reconcile real repository contracts; obtain owner acceptance before implementation.
