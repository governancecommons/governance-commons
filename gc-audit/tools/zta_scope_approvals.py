"""Authenticate a bounded ZTA non-applicability reviewer decision.

A signature proves who signed the decision, not whether inventory coverage
is true. The caller independently supplies exact scope screening outcome.
No automatic NOT_APPLICABLE is returned.
"""
from __future__ import annotations
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN="gc-audit.zta.scope-approval.v1"
FIELDS={"domain","target_id","revision","control_id","capability",
        "required_scopes","observation_ids","decision","approver_key_id"}
def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def verify_scope_approval(envelope, *, target_id, revision, control_id,
                          capability, required_scopes, verified_screen,
                          authorized_approvers):
    if not isinstance(envelope,dict) or set(envelope)!={"payload","signature"}:
        raise ValueError("invalid scope approval envelope")
    p=envelope["payload"]
    if not isinstance(p,dict) or set(p)!=FIELDS or p["domain"]!=DOMAIN:
        raise ValueError("invalid scope approval domain or payload")
    if (p["target_id"],p["revision"],p["control_id"],p["capability"]) != (
            target_id,revision,control_id,capability):
        raise ValueError("scope approval target/revision/control mismatch")
    if p["decision"]!="APPROVE_ABSENCE_REVIEW":
        raise ValueError("unsupported scope approval decision")
    if (not isinstance(p["required_scopes"],list) or
            len(p["required_scopes"])!=len(set(p["required_scopes"])) or
            not p["required_scopes"] or
            any(not isinstance(x,str) or not x for x in p["required_scopes"]) or
            set(p["required_scopes"])!=set(required_scopes)):
        raise ValueError("approved scopes differ from independent requirements")
    if (not isinstance(p["observation_ids"],list) or not p["observation_ids"] or
            len(p["observation_ids"])!=len(set(p["observation_ids"])) or
            any(not isinstance(x,str) or not x for x in p["observation_ids"])):
        raise ValueError("invalid approved observation identifiers")
    if verified_screen.get("status")!="ABSENCE_CANDIDATE":
        raise ValueError("independently verified absence candidate required")
    if not set(required_scopes)<=set(verified_screen.get("verified_scopes",[])):
        raise ValueError("missing independently verified scopes")
    key_id=p["approver_key_id"]
    if not isinstance(key_id,str) or key_id not in authorized_approvers:
        raise ValueError("unauthorized scope reviewer")
    key_bytes=authorized_approvers[key_id]
    if not isinstance(key_bytes,bytes):
        raise ValueError("invalid trusted reviewer key")
    try:
        signature=base64.b64decode(envelope["signature"],validate=True)
        Ed25519PublicKey.from_public_bytes(key_bytes).verify(signature,canonical(p))
    except (ValueError,TypeError,InvalidSignature) as exc:
        raise ValueError("invalid scope approval signature") from exc
    return {"status":"SIGNED_SCOPE_REVIEW","control_id":control_id,
            "reviewer_key_id":key_id,"release_decision":"UNVERIFIED"}
