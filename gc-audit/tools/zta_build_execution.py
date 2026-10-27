"""Independently corroborate a signed build-execution observation.

A CI producer signature alone is insufficient: the exact execution tuple must
also appear in a verifier-controlled corroboration registry. Neither a signature
nor corroboration proves hermeticity or reproducibility.
"""
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN = "gc-audit.zta.build-execution.v1"
FIELDS = {"domain","target_id","revision","source_digest","build_id",
          "builder_spec_digest","artifact_sha256","execution_id",
          "execution_outcome","executor_key_id"}

def canonical(data):
    return json.dumps(data,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def verify_build_execution(*, envelope, trusted_executors,
                           corroborated_executions, approved_source,
                           approved_builder, release):
    if not isinstance(envelope,dict) or set(envelope)!={"payload","signature"}:
        raise ValueError("invalid build execution envelope")
    p=envelope["payload"]
    if not isinstance(p,dict) or set(p)!=FIELDS or p["domain"]!=DOMAIN:
        raise ValueError("invalid build execution statement")
    if p["execution_outcome"]!="SUCCESS" or not isinstance(p["execution_id"],str) or not p["execution_id"]:
        raise ValueError("missing successful build execution")
    checks=((p["target_id"],release.get("target_id")),
            (p["revision"],release.get("revision")),
            (p["build_id"],release.get("build_id")),
            (p["artifact_sha256"],release.get("sha256")),
            (p["revision"],approved_source.get("revision")),
            (p["source_digest"],approved_source.get("source_digest")),
            (p["executor_key_id"],approved_builder.get("executor_key_id")),
            (p["builder_spec_digest"],approved_builder.get("builder_spec_digest")))
    if any(not isinstance(a,str) or not a or a!=b for a,b in checks):
        raise ValueError("build execution does not match independent policy")
    key_id=p["executor_key_id"]
    if not isinstance(trusted_executors,dict) or key_id not in trusted_executors:
        raise ValueError("untrusted execution signer")
    public_key=trusted_executors[key_id]
    if not isinstance(public_key,bytes) or len(public_key)!=32:
        raise ValueError("invalid executor trust root")
    try:
        signature=base64.b64decode(envelope["signature"],validate=True)
        Ed25519PublicKey.from_public_bytes(public_key).verify(signature,canonical(p))
    except (ValueError,TypeError,InvalidSignature) as exc:
        raise ValueError("invalid build execution signature") from exc
    observed=(p["target_id"],p["revision"],p["source_digest"],p["build_id"],
              p["builder_spec_digest"],p["artifact_sha256"],p["execution_outcome"],key_id)
    if not isinstance(corroborated_executions,dict) or corroborated_executions.get(p["execution_id"])!=observed:
        raise ValueError("independent execution corroboration absent or mismatched")
    return {"control_id":"ZTA-08.02","status":"BUILD_EXECUTION_CORROBORATED",
            "execution_id":p["execution_id"],"revision":p["revision"],
            "artifact_digest":p["artifact_sha256"],"release_decision":"UNVERIFIED"}
