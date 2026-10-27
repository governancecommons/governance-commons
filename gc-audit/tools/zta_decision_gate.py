"""Control decision-gate v1: deterministic, fail-closed candidate classification.

This module does not award PASS or NOT_APPLICABLE. A signed package or scope
review alone never establishes verified control behavior or full deployment scope.
"""
from __future__ import annotations

class DecisionGateError(ValueError):
    pass

def classify_control(*, control_id, mandatory, negative_evidence_ids=(),
                     proof_coverage=None, applicability=None, scope_review=None):
    if not isinstance(control_id, str) or not control_id:
        raise DecisionGateError("invalid control identifier")
    if type(mandatory) is not bool:
        raise DecisionGateError("mandatory must be boolean")
    negatives = sorted(set(negative_evidence_ids))
    if negatives:
        return {"control_id":control_id, "status":"FAIL",
                "reason":"verified negative observation overrides favorable evidence",
                "evidence_ids":negatives}
    proof_status = (proof_coverage or {}).get("status")
    applicability_status = (applicability or {}).get("status")
    review_status = (scope_review or {}).get("status")
    if proof_status not in (None, "PROOF_PACKAGE_COMPLETE", "INCOMPLETE",
                            "NEGATIVE_REVIEW_REQUIRED", "UNVERIFIED"):
        raise DecisionGateError("unsupported proof package status")
    if applicability_status not in (None, "APPLICABLE", "ABSENCE_CANDIDATE", "UNVERIFIED"):
        raise DecisionGateError("unsupported applicability status")
    if review_status not in (None, "SIGNED_SCOPE_REVIEW"):
        raise DecisionGateError("unsupported scope review status")
    if proof_status == "NEGATIVE_REVIEW_REQUIRED":
        return {"control_id":control_id, "status":"UNVERIFIED",
                "reason":"negative proof-package result requires verified failure adjudication"}
    if applicability_status == "APPLICABLE" and review_status:
        raise DecisionGateError("scope review conflicts with verified capability presence")
    if mandatory and review_status:
        raise DecisionGateError("mandatory control cannot be excluded by a scope review")
    if review_status and applicability_status != "ABSENCE_CANDIDATE":
        raise DecisionGateError("scope review lacks a corroborated absence candidate")
    if review_status:
        return {"control_id":control_id, "status":"UNVERIFIED",
                "reason":"signed N/A candidate requires approved full-scope exclusion policy"}
    if proof_status == "PROOF_PACKAGE_COMPLETE":
        return {"control_id":control_id, "status":"UNVERIFIED",
                "reason":"positive proof candidate requires control-specific execution assurance"}
    return {"control_id":control_id, "status":"UNVERIFIED",
            "reason":"control outcome lacks complete independently verified proof"}
