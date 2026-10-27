"""Bounded, read-only ZTA-08.02 whole-chain verification.

Trust roots and execution corroboration are caller supplied, outside target data.
The signed policy names every distribution and installation scope being assessed.
"""
import base64
import hashlib
from datetime import datetime

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from zta_artifact_chain import verify_release_artifact_chain
from zta_artifact_acceptance import screen_artifact_acceptance
from zta_build_provenance import verify_signed_build_provenance
from zta_build_execution import verify_build_execution
from zta_installation_attestation import verify_signed_installation
from zta_authenticated_packages import canonical_bytes

DOMAIN = "gc-audit.zta.artifact-control-policy.v1"
POLICY_FIELDS = {"domain", "target_id", "revision", "build_id", "sha256",
                 "source_digest", "builder_spec_digest", "builder_key_id",
                 "executor_key_id", "observer_key_ids", "scopes", "approver_key_id",
                 "issued_at", "expires_at", "max_observation_age_seconds"}
REQUIRED_PROOFS = frozenset({"source", "builder", "build-execution", "build-bytes",
                             "distribution", "installation"})


def _sha256(payload):
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("artifact proof bytes missing")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def verify_artifact_control(*, target_id, revision, policy_envelope, proof,
                            trusted_approvers, trusted_builders,
                            trusted_executors, trusted_observers,
                            corroborated_executions, required_scopes, as_of):
    """Return a PASS candidate only for a fully authenticated declared scope."""
    if not isinstance(policy_envelope, dict) or set(policy_envelope) != {"payload", "signature"}:
        raise ValueError("signed independent control policy required")
    policy = policy_envelope["payload"]
    if not isinstance(policy, dict) or set(policy) != POLICY_FIELDS or policy["domain"] != DOMAIN:
        raise ValueError("invalid artifact control policy")
    if (policy["target_id"], policy["revision"]) != (target_id, revision):
        raise ValueError("policy target or revision mismatch")
    try:
        issued = datetime.fromisoformat(policy["issued_at"].replace("Z", "+00:00"))
        expires = datetime.fromisoformat(policy["expires_at"].replace("Z", "+00:00"))
        assessed = datetime.fromisoformat(as_of.replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ValueError("explicit timezone-bound policy freshness required") from exc
    if any(t.tzinfo is None for t in (issued, expires, assessed)) or not issued <= assessed < expires:
        raise ValueError("artifact control policy not current at as-of time")
    age = policy["max_observation_age_seconds"]
    if type(age) is not int or not 0 < age <= 2592000:
        raise ValueError("invalid signed observation freshness policy")
    key_id = policy["approver_key_id"]
    key = trusted_approvers.get(key_id) if isinstance(trusted_approvers, dict) else None
    if not isinstance(key, bytes) or len(key) != 32:
        raise ValueError("independent policy approver not trusted")
    try:
        signature = base64.b64decode(policy_envelope["signature"], validate=True)
        Ed25519PublicKey.from_public_bytes(key).verify(signature, canonical_bytes(policy))
    except (ValueError, TypeError, InvalidSignature) as exc:
        raise ValueError("artifact control policy signature invalid") from exc
    if (not isinstance(proof, dict) or set(proof) != {
            "source_bytes", "builder_spec_bytes", "build_bytes", "signed_build",
            "signed_execution", "execution_id", "scopes", "requirements"}):
        raise ValueError("whole-chain proof incomplete")
    if set(proof["requirements"]) != REQUIRED_PROOFS or len(proof["requirements"]) != len(REQUIRED_PROOFS):
        raise ValueError("control-specific proof requirements incomplete")
    if (_sha256(proof["source_bytes"]) != policy["source_digest"]
            or _sha256(proof["builder_spec_bytes"]) != policy["builder_spec_digest"]
            or _sha256(proof["build_bytes"]) != policy["sha256"]):
        raise ValueError("source, builder, or build output differs from policy")
    scopes = policy["scopes"]
    if (not isinstance(scopes, list) or not scopes or len(scopes) != len(set(scopes))
            or any(not isinstance(scope, str) or not scope for scope in scopes)):
        raise ValueError("complete approved scope list required")
    if (not isinstance(required_scopes, (list, tuple)) or not required_scopes
            or len(required_scopes) != len(set(required_scopes))
            or set(required_scopes) != set(scopes)):
        raise ValueError("approved policy does not cover independent required scopes")
    observations = proof["scopes"]
    if not isinstance(observations, dict) or set(observations) != set(scopes):
        raise ValueError("distribution/install scope coverage incomplete")
    observers = policy["observer_key_ids"]
    if (not isinstance(observers, dict) or set(observers) != set(scopes)
            or any(not isinstance(v, str) or not v for v in observers.values())):
        raise ValueError("approved observers missing for scope")
    source = {"revision": revision, "source_digest": policy["source_digest"]}
    builder = {"builder_key_id": policy["builder_key_id"],
               "builder_spec_digest": policy["builder_spec_digest"]}
    executor = {"executor_key_id": policy["executor_key_id"],
                "builder_spec_digest": policy["builder_spec_digest"]}
    checked_scopes = []
    for scope in sorted(scopes):
        observed = observations[scope]
        if not isinstance(observed, dict) or set(observed) != {
                "distribution_bytes", "installed_bytes", "signed_installation"}:
            raise ValueError("scope proof incomplete")
        if (_sha256(observed["distribution_bytes"]) != policy["sha256"]
                or _sha256(observed["installed_bytes"]) != policy["sha256"]):
            raise ValueError("distributed or installed artifact substitution")
        release = {"target_id": target_id, "revision": revision,
                   "build_id": policy["build_id"], "install_scope": scope,
                   "sha256": policy["sha256"]}
        chain = verify_release_artifact_chain(
            target_id=target_id, revision=revision, trusted_release=release,
            build_bytes=proof["build_bytes"], installed_bytes=observed["installed_bytes"],
            observed_install={k: release[k] for k in ("target_id", "revision", "build_id", "install_scope")},
            signed_installation=observed["signed_installation"],
            trusted_observers=trusted_observers, signed_build=proof["signed_build"],
            trusted_builders=trusted_builders, approved_source=source,
            approved_builder=builder, signed_execution=proof["signed_execution"],
            trusted_executors=trusted_executors,
            corroborated_executions=corroborated_executions, approved_executor=executor,
            as_of=as_of, max_observation_age_seconds=age)
        provenance = verify_signed_build_provenance(
            envelope=proof["signed_build"], trusted_builders=trusted_builders,
            approved_source=source, approved_builder=builder, release=release)
        execution = verify_build_execution(
            envelope=proof["signed_execution"], trusted_executors=trusted_executors,
            corroborated_executions=corroborated_executions,
            approved_source=source, approved_builder=executor, release=release)
        installation = verify_signed_installation(
            envelope=observed["signed_installation"], trusted_observers=trusted_observers,
            release=release, installed_bytes=observed["installed_bytes"],
            as_of=as_of, max_age_seconds=age)
        if installation["observer_key_id"] != observers[scope]:
            raise ValueError("unapproved scope observer")
        screen_artifact_acceptance(
            chain=chain, provenance=provenance, execution=execution,
            installation=installation,
            independent_policy={"target_id": target_id, "revision": revision,
                "build_id": policy["build_id"], "install_scope": scope,
                "artifact_digest": policy["sha256"],
                "authorized_builder_keys": [policy["builder_key_id"]],
                "authorized_observer_keys": [observers[scope]],
                "corroborated_execution_ids": [proof["execution_id"]]})
        checked_scopes.append(scope)
    return {"control_id": "ZTA-08.02", "status": "WHOLE_CHAIN_VERIFIED",
            "target_id": target_id, "revision": revision,
            "artifact_digest": policy["sha256"], "scopes": checked_scopes,
            "policy_approver_key_id": key_id}
