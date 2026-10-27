"""Verify a signed, bounded source-to-build statement for ZTA-08.02.

The verifier never executes a build or contacts a CI service. The statement
authenticates the named producer, not its independence or build reproducibility.
"""
import base64
import json
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

DOMAIN = "gc-audit.zta.build-provenance.v1"
FIELDS = {"domain", "target_id", "revision", "build_id", "artifact_sha256",
          "builder_key_id", "source_digest", "builder_spec_digest"}

def canonical(record):
    return json.dumps(record, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":")).encode("utf-8")

def verify_signed_build_provenance(*, envelope, trusted_builders,
                                   approved_source, approved_builder, release):
    if not isinstance(envelope, dict) or set(envelope) != {"payload", "signature"}:
        raise ValueError("invalid build provenance envelope")
    p = envelope["payload"]
    if not isinstance(p, dict) or set(p) != FIELDS or p["domain"] != DOMAIN:
        raise ValueError("invalid build provenance statement")
    if not isinstance(release, dict) or not {"target_id", "revision", "build_id", "sha256"} <= set(release):
        raise ValueError("missing independent release policy")
    for k, source_key in (("target_id", "target_id"), ("revision", "revision"),
                          ("build_id", "build_id"), ("artifact_sha256", "sha256")):
        if not isinstance(p[k], str) or not p[k] or p[k] != release[source_key]:
            raise ValueError("build provenance not bound to approved release")
    if (not isinstance(approved_source, dict) or set(approved_source) != {"revision", "source_digest"}
            or p["revision"] != approved_source["revision"]
            or p["source_digest"] != approved_source["source_digest"]):
        raise ValueError("independently approved source reference mismatch")
    if (not isinstance(approved_builder, dict) or set(approved_builder) != {"builder_key_id", "builder_spec_digest"}
            or p["builder_key_id"] != approved_builder["builder_key_id"]
            or p["builder_spec_digest"] != approved_builder["builder_spec_digest"]):
        raise ValueError("independently approved builder specification mismatch")
    if not isinstance(trusted_builders, dict) or p["builder_key_id"] not in trusted_builders:
        raise ValueError("build signer is not authorized")
    key = trusted_builders[p["builder_key_id"]]
    if not isinstance(key, bytes) or len(key) != 32:
        raise ValueError("invalid trusted builder key")
    try:
        signature = base64.b64decode(envelope["signature"], validate=True)
        Ed25519PublicKey.from_public_bytes(key).verify(signature, canonical(p))
    except (TypeError, ValueError, InvalidSignature) as exc:
        raise ValueError("build provenance signature invalid") from exc
    return {"control_id": "ZTA-08.02", "status": "SIGNED_BUILD_PROVENANCE",
            "target_id": p["target_id"], "revision": p["revision"],
            "build_id": p["build_id"], "artifact_digest": p["artifact_sha256"],
            "builder_key_id": p["builder_key_id"], "release_decision": "UNVERIFIED"}
