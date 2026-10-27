"""ZTA-08.02 bounded artifact chain check.

Independently pinned source revision, build and installed artifacts are checked
against supplied raw bytes. Pins are trusted policy inputs, not target claims.
A positive result is a review candidate, never a full-control PASS.
"""
from __future__ import annotations
import hashlib
import hmac
from zta_positive_checks import verify_artifact_pair
from zta_installation_attestation import verify_signed_installation

def verify_release_artifact_chain(*, target_id, revision, trusted_release,
                                  build_bytes, installed_bytes, observed_install,
                                  signed_installation=None, trusted_observers=None):
    if not isinstance(trusted_release,dict) or set(trusted_release)!={"target_id","revision","sha256","build_id","install_scope"}:
        raise ValueError("independent release policy incomplete")
    if not isinstance(observed_install,dict) or set(observed_install)!={"target_id","revision","build_id","install_scope"}:
        raise ValueError("invalid independent installation observation")
    if not all(isinstance(trusted_release[k],str) and trusted_release[k]
               for k in ("target_id","revision","build_id","install_scope")):
        raise ValueError("invalid release identifiers")
    if not all(observed_install[k]==trusted_release[k] for k in observed_install):
        raise ValueError("installation does not match trusted release target, revision or scope")
    if signed_installation is None or not isinstance(trusted_observers,dict) or not trusted_observers:
        raise ValueError("authenticated installation evidence and external trust roots required")
    attested=verify_signed_installation(
        envelope=signed_installation, trusted_observers=trusted_observers,
        release=trusted_release, installed_bytes=installed_bytes)
    if attested["status"]!="SIGNED_INSTALLATION_OBSERVATION":
        raise ValueError("installation observation not authenticated")
    result=verify_artifact_pair(target_id,revision,
        {k:trusted_release[k] for k in ("target_id","revision","sha256")},
        build_bytes,installed_bytes)
    return {"control_id":"ZTA-08.02","status":"ARTIFACT_CHAIN_CANDIDATE",
            "target_id":target_id,"revision":revision,
            "build_id":trusted_release["build_id"],
            "install_scope":trusted_release["install_scope"],
            "observer_key_id":attested["observer_key_id"],
            "artifact_digest":result["artifact_digest"],
            "limitations":["source-to-build provenance not independently established",
                           "installation observer identity not authenticated here",
                           "distribution integrity outside supplied artifacts not established"],
            "release_decision":"UNVERIFIED"}
