"""Read-only validation of a scoped proof package, not a generic PASS oracle.

An externally trusted control-policy mapping must specify *all* requirements.
Neither package requirements nor package authority are independently trusted.
"""
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = Path(__file__).resolve().parents[1] / "schemas" / "zta" / "gc-audit.zta-proof-package.v1.schema.json"

class ProofPackageError(ValueError):
    pass

def check_proof_package(package, *, target_id, revision, expected_control,
                        trusted_requirements, approved_checkers, verified_evidence_ids,
                        trusted_authority_keys, independently_verified_results):
    """Return a bounded review result; do not grant whole-control PASS.

    independently_verified_results is a trusted caller-owned mapping from
    (checker id, evidence id, requirement id) to (checker result, digest).
    The package cannot populate it.  Trust roots and requirement sets MUST
    originate outside the target/package.
    """
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    error = next(iter(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(package)), None)
    if error:
        raise ProofPackageError("invalid proof package: " + error.message)
    if (package["target_id"], package["revision"], package["control_id"]) != (
            target_id, revision, expected_control):
        raise ProofPackageError("target, revision or control mismatch")
    authority = package["authority"]
    if authority["key_id"] not in trusted_authority_keys:
        raise ProofPackageError("untrusted authority")
    checker = package["checker"]
    if checker["id"] not in approved_checkers or (
            checker["version"], checker["spec_digest"]) != approved_checkers[checker["id"]]:
        raise ProofPackageError("unapproved checker or specification")
    if expected_control not in trusted_requirements:
        raise ProofPackageError("missing independent control policy")
    required = set(trusted_requirements[expected_control])
    if not required or set(package["requirements"]) != required:
        raise ProofPackageError("requirements do not match independent control policy")
    if package["artifact_origin"]["source_revision"] != revision:
        raise ProofPackageError("artifact source revision mismatch")
    observations = {}
    for item in package["proofs"]:
        requirement = item["requirement_id"]
        if requirement not in required or requirement in observations:
            raise ProofPackageError("unexpected or duplicate requirement proof")
        if item["evidence_id"] not in verified_evidence_ids:
            raise ProofPackageError("unverified evidence")
        key = (checker["id"], item["evidence_id"], requirement)
        actual = independently_verified_results.get(key)
        if actual != (item["checker_result"], item["digest"]):
            raise ProofPackageError("checker result not independently corroborated")
        observations[requirement] = item["checker_result"]
    missing = required - set(observations)
    if missing:
        return {"status":"INCOMPLETE", "missing":sorted(missing), "control_id":expected_control}
    if any(value == "FAILED" for value in observations.values()):
        return {"status":"NEGATIVE_REVIEW_REQUIRED", "missing":[], "control_id":expected_control}
    if any(value == "INCONCLUSIVE" for value in observations.values()):
        return {"status":"UNVERIFIED", "missing":[], "control_id":expected_control}
    return {"status":"PROOF_PACKAGE_COMPLETE", "missing":[], "control_id":expected_control,
            "proof_ids":sorted({item["evidence_id"] for item in package["proofs"]})}
