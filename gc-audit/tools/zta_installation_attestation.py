"""Authenticated installation observation for ZTA-08.02.

Verification attests to one observed artifact at one deployment scope.
It does NOT establish trusted source-to-build provenance, observer independence,
or full-control PASS. Trust roots must originate outside target inputs.
"""
import base64
import hashlib
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN = "gc-audit.zta.installation-observation.v1"
FIELDS = {"domain", "target_id", "revision", "build_id", "install_scope",
          "artifact_sha256", "observer_key_id"}

def canonical(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")

def verify_signed_installation(*, envelope, trusted_observers, release,
                               installed_bytes):
    if not isinstance(envelope, dict) or set(envelope) != {"payload", "signature"}:
        raise ValueError("invalid observation envelope")
    payload = envelope["payload"]
    if not isinstance(payload, dict) or set(payload) != FIELDS or payload["domain"] != DOMAIN:
        raise ValueError("invalid installation observation payload")
    if not isinstance(release, dict) or set(release) != {
            "target_id", "revision", "build_id", "install_scope", "sha256"}:
        raise ValueError("invalid independent release pin")
    for key in ("target_id", "revision", "build_id", "install_scope"):
        if not isinstance(release[key], str) or not release[key] or payload[key] != release[key]:
            raise ValueError("observation/release identity mismatch")
    if payload["artifact_sha256"] != release["sha256"]:
        raise ValueError("observed digest differs from release pin")
    if not isinstance(installed_bytes, bytes) or not installed_bytes:
        raise ValueError("installed artifact bytes required")
    calculated = "sha256:" + hashlib.sha256(installed_bytes).hexdigest()
    if calculated != release["sha256"]:
        raise ValueError("installed artifact differs from trusted release")
    key_id = payload["observer_key_id"]
    if not isinstance(key_id, str) or not isinstance(trusted_observers, dict) or key_id not in trusted_observers:
        raise ValueError("untrusted installation observer")
    key_bytes = trusted_observers[key_id]
    if not isinstance(key_bytes, bytes) or len(key_bytes) != 32:
        raise ValueError("invalid observer public key")
    try:
        sig = base64.b64decode(envelope["signature"], validate=True)
        Ed25519PublicKey.from_public_bytes(key_bytes).verify(sig, canonical(payload))
    except (ValueError, TypeError, InvalidSignature) as exc:
        raise ValueError("installation signature invalid") from exc
    return {"control_id": "ZTA-08.02", "status": "SIGNED_INSTALLATION_OBSERVATION",
            "observer_key_id": key_id, "target_id": release["target_id"],
            "revision": release["revision"], "build_id": release["build_id"],
            "install_scope": release["install_scope"], "artifact_digest": calculated,
            "release_decision": "UNVERIFIED"}
