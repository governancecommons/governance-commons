"""Narrow positive checker: ZTA-08.02 artifact byte-integrity verification.

The caller MUST source the immutable expected digest from trusted release authority
outside target-controlled input. This checks exact build and installed bytes, not
reproducible builds, distribution-channel compromise, or broader supply-chain safety.
No execution, network access, or target writes.
"""
from __future__ import annotations
import hashlib
import hmac

def verify_artifact_pair(target_id, revision, expected, build_bytes, installed_bytes):
    if not isinstance(expected, dict) or set(expected) != {"target_id","revision","sha256"}:
        raise ValueError("invalid trusted artifact pin")
    if expected["target_id"] != target_id or expected["revision"] != revision:
        raise ValueError("trusted pin does not match target revision")
    pinned = expected["sha256"]
    if not isinstance(pinned, str) or len(pinned) != 71 or not pinned.startswith("sha256:"):
        raise ValueError("invalid trusted SHA-256 pin")
    try:
        bytes.fromhex(pinned[7:])
    except ValueError as exc:
        raise ValueError("invalid trusted SHA-256 pin") from exc
    if not isinstance(build_bytes, bytes) or not isinstance(installed_bytes, bytes):
        raise ValueError("artifact inputs must be raw bytes")
    if not build_bytes or not installed_bytes:
        raise ValueError("empty build or installation artifact")
    a = hashlib.sha256(build_bytes).digest()
    b = hashlib.sha256(installed_bytes).digest()
    pinned_raw = bytes.fromhex(pinned[7:])
    if not hmac.compare_digest(a, pinned_raw) or not hmac.compare_digest(b, pinned_raw):
        raise ValueError("artifact byte integrity mismatch")
    return {"control_id":"ZTA-08.02", "status":"BYTE_INTEGRITY_VERIFIED",
            "artifact_digest":pinned, "target_id":target_id, "revision":revision,
            "scope":"build and installed artifact bytes only"}
