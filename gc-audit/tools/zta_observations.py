"""Verify signed, revision-bound negative control observations.

Caller supplies trusted Ed25519 public keys from an authority controlled outside
the target. A verified signature authenticates a producer's observation, not the
independent truth of a deployed system's runtime behavior. Only FAIL is supported.
"""
from __future__ import annotations
import base64
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN = "gc-audit.zta.negative-observation.v1"
REQUIRED = {"domain","target_id","revision","control_id","evidence_id",
            "test_id","observation","producer_key_id"}

def verify_negative_observation(envelope, trust_roots, canonical):
    if not isinstance(envelope, dict) or set(envelope) != {"payload","signature"}:
        raise ValueError("malformed observation envelope")
    p = envelope["payload"]
    if not isinstance(p, dict) or set(p) != REQUIRED:
        raise ValueError("malformed observation payload")
    if p["domain"] != DOMAIN or p["observation"] != "VIOLATION":
        raise ValueError("unsupported observation semantics")
    for key in REQUIRED - {"domain","observation"}:
        if not isinstance(p[key], str) or not p[key]:
            raise ValueError("invalid observation identifier")
    key_id = p["producer_key_id"]
    if key_id not in trust_roots:
        raise ValueError("untrusted observation producer")
    try:
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key = Ed25519PublicKey.from_public_bytes(trust_roots[key_id])
        public_key.verify(signature, canonical(p))
    except (ValueError, TypeError, InvalidSignature) as exc:
        raise ValueError("observation signature invalid") from exc
    return p
