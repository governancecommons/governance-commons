"""ZTA-08.02 whole-chain acceptance screening.

Checks cross-evidence consistency of already VERIFIED component outputs. This is
not a cryptographic verifier: never pass unchecked input directly to this gate.
The evaluator must retain FAIL precedence and release BLOCKED pending trusted
execution, policy and independent review.
"""
from __future__ import annotations

def screen_artifact_acceptance(*, chain, provenance, execution, installation,
                               independent_policy):
    if not isinstance(independent_policy, dict) or set(independent_policy) != {
            "target_id", "revision", "build_id", "install_scope", "artifact_digest",
            "authorized_builder_keys", "authorized_observer_keys",
            "corroborated_execution_ids"}:
        raise ValueError("complete external artifact control policy required")
    if any(not isinstance(item, dict) for item in (chain, provenance, execution, installation)):
        raise ValueError("complete verified component results required")
    statuses=((chain,"ARTIFACT_CHAIN_CANDIDATE"),
              (provenance,"SIGNED_BUILD_PROVENANCE"),
              (execution,"BUILD_EXECUTION_CORROBORATED"),
              (installation,"SIGNED_INSTALLATION_OBSERVATION"))
    if any(item.get("control_id")!="ZTA-08.02" or item.get("status")!=status
           for item,status in statuses):
        raise ValueError("missing verified ZTA-08.02 component status")
    for key in ("target_id","revision","build_id","install_scope","artifact_digest"):
        expected=independent_policy[key]
        if not isinstance(expected,str) or not expected or chain.get(key)!=expected:
            raise ValueError("artifact chain diverges from external policy")
    for item,fields in (
            (provenance,("target_id","revision","build_id","artifact_digest")),
            (installation,("target_id","revision","build_id","install_scope","artifact_digest")),
            (execution,("revision","artifact_digest"))):
        if any(item.get(key)!=independent_policy[key] for key in fields):
            raise ValueError("cross-evidence release mismatch")
    builders=independent_policy["authorized_builder_keys"]
    observers=independent_policy["authorized_observer_keys"]
    execution_ids=independent_policy["corroborated_execution_ids"]
    if (not isinstance(builders,(list,tuple)) or not builders
            or not isinstance(observers,(list,tuple)) or not observers
            or not isinstance(execution_ids,(list,tuple)) or not execution_ids):
        raise ValueError("external signer and execution policies missing")
    if (chain.get("builder_key_id") not in builders
            or provenance.get("builder_key_id")!=chain.get("builder_key_id")
            or chain.get("observer_key_id") not in observers
            or installation.get("observer_key_id")!=chain.get("observer_key_id")
            or chain.get("build_execution_id") not in execution_ids
            or execution.get("execution_id")!=chain.get("build_execution_id")):
        raise ValueError("signer or execution evidence conflicts with approved policy")
    if any(item.get("release_decision")!="UNVERIFIED" for item in statuses_to_results(statuses)):
        raise ValueError("component attempted unsupported release approval")
    return {"control_id":"ZTA-08.02", "status":"WHOLE_CHAIN_REVIEW_CANDIDATE",
            "target_id":independent_policy["target_id"],
            "revision":independent_policy["revision"],
            "artifact_digest":independent_policy["artifact_digest"],
            "release_decision":"UNVERIFIED",
            "remaining_requirements":[
                "independent trust-root and CI provenance review",
                "approved control-specific sufficiency criteria",
                "negative evidence and deployment-scope adjudication"]}

def statuses_to_results(statuses):
    return [item for item,_ in statuses]
