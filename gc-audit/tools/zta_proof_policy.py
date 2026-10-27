"""ZTA-001C proof-admissibility boundary.

This module does NOT convert attestations or signatures into a PASS or N/A.
It checks whether evidence is even eligible for later control-specific review.
"""
from __future__ import annotations
from datetime import datetime, timezone

BEHAVIORAL_CONTROLS = frozenset({
    "ZTA-01.02", "ZTA-02.01", "ZTA-02.02", "ZTA-03.02",
    "ZTA-05.02", "ZTA-06.01", "ZTA-06.02", "ZTA-07.02",
    "ZTA-10.01", "ZTA-10.02", "ZTA-11.02", "ZTA-12.01", "ZTA-12.02",
})
BEHAVIORAL_METHODS = frozenset({"AUTOMATED_TEST", "CI_ATTESTATION", "RUNTIME_OBSERVATION"})
SCOPE_METHODS = frozenset({"STATIC_INSPECTION", "MANUAL_REVIEW", "CI_ATTESTATION", "AUTOMATED_TEST"})

def _timestamp(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("evidence timestamp requires timezone")
    return parsed.astimezone(timezone.utc)

def assess_admissibility(control_id, records, verified_ids, *, as_of=None, max_age_seconds=None):
    """Return admissible evidence IDs and disqualification reasons.

    Verified bytes establish integrity, not a correct observation, reliable
    producer, complete coverage, or sufficiency. Empty reasons is NOT PASS.
    """
    if (as_of is None) != (max_age_seconds is None):
        raise ValueError("as_of and max_age_seconds must be supplied together")
    if max_age_seconds is not None and (type(max_age_seconds) is not int or max_age_seconds < 0):
        raise ValueError("max_age_seconds must be nonnegative integer")
    now = _timestamp(as_of) if as_of is not None else None
    admitted, rejected = [], {}
    for e in records:
        if control_id not in e["control_ids"]:
            continue
        problems = []
        if e["evidence_id"] not in verified_ids:
            problems.append("content integrity not verified")
        if e["producer"]["identity_status"] != "VERIFIED":
            problems.append("producer identity not verified")
        if control_id in BEHAVIORAL_CONTROLS and e["method"] not in BEHAVIORAL_METHODS:
            problems.append("behavioral control requires behavioral proof")
        if now is not None:
            age = (now - _timestamp(e["collected_at"])).total_seconds()
            if age < 0:
                problems.append("observation is in the future")
            if age > max_age_seconds:
                problems.append("evidence too old")
        if problems:
            rejected[e["evidence_id"]] = problems
        else:
            admitted.append(e["evidence_id"])
    return {"admissible_ids": sorted(admitted), "rejected": dict(sorted(rejected.items())),
            "decision": "REVIEW_REQUIRED"}
