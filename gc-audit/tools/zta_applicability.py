"""Independent applicability screening for GC-AUDIT ZTA.

Inventory absence is never enough for NOT_APPLICABLE: independently attested
scope completeness, source coverage, policy triggers and conflict review are
separate requirements. This function returns REVIEW_REQUIRED, never N/A.
"""
from __future__ import annotations

def screen_applicability(*, control_id, target_id, revision, capability,
                         trusted_capability_policy, observations,
                         independently_verified_observations,
                         required_scopes=None):
    """Check an externally supplied set of observation records.

    Independent verification is a caller-owned mapping of observation ID to its
    exact (target, revision, capability, outcome, scope) tuple. A target cannot
    validate its own observations. No return value authorizes N/A.
    """
    if not isinstance(trusted_capability_policy, dict) or (
            trusted_capability_policy.get(control_id) != capability):
        raise ValueError("missing independent capability policy")
    if not isinstance(observations, (list, tuple)) or not observations:
        return {"status":"UNVERIFIED","reason":"no independent capability observations"}
    if not isinstance(independently_verified_observations, dict):
        raise ValueError("independent observation verification required")
    seen=set()
    absent_scopes=set()
    conflicts=[]
    incomplete=False
    for item in observations:
        if not isinstance(item, dict) or set(item) != {
                "id","target_id","revision","capability","outcome","scope",
                "inventory_complete"}:
            raise ValueError("malformed applicability observation")
        oid=item["id"]
        if not isinstance(oid,str) or not oid or oid in seen:
            raise ValueError("duplicate or invalid applicability observation")
        seen.add(oid)
        if any(item[k] != expected for k,expected in (
                ("target_id",target_id),("revision",revision),
                ("capability",capability))):
            raise ValueError("cross-target, stale, or mismatched capability observation")
        if item["outcome"] not in ("PRESENT","ABSENT","UNKNOWN"):
            raise ValueError("invalid applicability outcome")
        if not isinstance(item["scope"],str) or not item["scope"]:
            raise ValueError("invalid applicability scope")
        if type(item["inventory_complete"]) is not bool:
            raise ValueError("invalid completeness assertion")
        expected=(target_id,revision,capability,item["outcome"],
                  item["scope"],item["inventory_complete"])
        if independently_verified_observations.get(oid) != expected:
            raise ValueError("unverified applicability observation")
        if item["outcome"]=="PRESENT":
            conflicts.append(oid)
        elif item["outcome"]=="ABSENT" and item["inventory_complete"]:
            absent_scopes.add(item["scope"])
        else:
            incomplete=True
    if required_scopes is not None:
        if (not isinstance(required_scopes, (list, tuple)) or not required_scopes
                or any(not isinstance(scope, str) or not scope for scope in required_scopes)
                or len(set(required_scopes)) != len(required_scopes)):
            raise ValueError("invalid independent required scope policy")
    if conflicts:
        return {"status":"APPLICABLE","reason":"verified capability presence",
                "conflicting_ids":sorted(conflicts)}
    if required_scopes is not None and not set(required_scopes) <= absent_scopes:
        return {"status":"UNVERIFIED", "reason":"independent required inventory scope not covered"}
    if incomplete or not absent_scopes:
        return {"status":"UNVERIFIED","reason":"absence or inventory coverage insufficient"}
    return {"status":"ABSENCE_CANDIDATE","reason":
            "independently corroborated scoped inventory absence; human review and full scope proof required",
            "verified_scopes":sorted(absent_scopes)}
