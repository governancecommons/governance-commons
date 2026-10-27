"""Authenticate a proof package without elevating its claims to a control PASS.

Trusted Ed25519 keys, independent checker results and control requirements
must come from an owner-controlled source, never from the target package.
"""
from __future__ import annotations
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from zta_proof_packages import ProofPackageError, check_proof_package

DOMAIN = "gc-audit.zta.proof-package-envelope.v1"

def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def authenticate_proof_package(envelope, *, trusted_public_keys, **verification_inputs):
    """Return authenticated package coverage; never produce PASS.

    The signature binds the exact domain separator and package bytes. Trust key
    IDs are looked up in a caller-owned map. Checker results are independently
    provided and must match through check_proof_package.
    """
    if not isinstance(envelope, dict) or set(envelope) != {"domain", "package", "signature"}:
        raise ProofPackageError("invalid authenticated package envelope")
    if envelope["domain"] != DOMAIN or not isinstance(envelope["package"], dict):
        raise ProofPackageError("invalid package domain")
    package = envelope["package"]
    authority = package.get("authority")
    if not isinstance(authority, dict) or not isinstance(authority.get("key_id"), str):
        raise ProofPackageError("invalid package authority")
    key_id = authority["key_id"]
    key_bytes = trusted_public_keys.get(key_id)
    if not isinstance(key_bytes, bytes):
        raise ProofPackageError("unknown trusted signer")
    try:
        signature = base64.b64decode(envelope["signature"], validate=True)
        key = Ed25519PublicKey.from_public_bytes(key_bytes)
        key.verify(signature, canonical_bytes({"domain": DOMAIN, "package": package}))
    except (ValueError, TypeError, InvalidSignature) as exc:
        raise ProofPackageError("invalid package signature") from exc
    # Do not allow independently supplied package-level identity to override
    # the public key actually used to authenticate the payload.
    result = check_proof_package(
        package, trusted_authority_keys={key_id: key_bytes}, **verification_inputs
    )
    return {"authentication": "SIGNATURE_VERIFIED", **result}
