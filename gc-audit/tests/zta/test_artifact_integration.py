"""End-to-end ZTA-08.02 acceptance and adversarial regressions."""
import base64
import copy
import hashlib
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import zta_evaluator as zta
from zta_artifact_control import DOMAIN, REQUIRED_PROOFS
from zta_authenticated_packages import canonical_bytes
from zta_installation_attestation import DOMAIN as INSTALL_DOMAIN, canonical as install_canonical
from test_artifact_chain import ArtifactChainTests

FIXTURE = json.loads((HERE / "schema-fixtures.v1.json").read_text(encoding="utf-8"))["valid"]


class ArtifactIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.chain = ArtifactChainTests()
        self.chain.setUp()
        self.catalog = copy.deepcopy(FIXTURE["controls"])
        self.profile = copy.deepcopy(FIXTURE["profile"])
        self.profile["catalog_digest"] = zta.digest(self.catalog)
        self.target = copy.deepcopy(FIXTURE["target"])
        self.target["target_id"] = "app"
        self.target["revision"] = "commit-a"
        self.approver = Ed25519PrivateKey.generate()
        self.assessment = self.make_assessment()

    def make_assessment(self, scopes=("linux-x64/production",)):
        c = self.chain
        policy = {"domain": DOMAIN, "target_id": "app", "revision": "commit-a",
                  "build_id": "build-42", "sha256": c.policy["sha256"],
                  "source_digest": c.source["source_digest"],
                  "builder_spec_digest": c.builder["builder_spec_digest"],
                  "builder_key_id": "builder", "executor_key_id": "executor",
                  "observer_key_ids": {s: "observer" for s in scopes},
                  "scopes": list(scopes), "approver_key_id": "owner",
                  "issued_at": "2026-10-01T00:00:00Z", "expires_at": "2026-11-01T00:00:00Z"}
        envelope = {"payload": policy, "signature": base64.b64encode(
            self.approver.sign(canonical_bytes(policy))).decode()}
        observations = {}
        for scope in scopes:
            payload = dict(c.signed["payload"], install_scope=scope)
            # The test fixture's signing key is regenerated here for each scope.
            observer = Ed25519PrivateKey.generate()
            c.trust["observer"] = observer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
            signed = {"payload": payload, "signature": base64.b64encode(
                observer.sign(install_canonical(payload))).decode()}
            observations[scope] = {"distribution_bytes": c.data,
                                   "installed_bytes": c.data, "signed_installation": signed}
        # One trust key must authenticate every scope in this fixture.
        if len(scopes) > 1:
            observer = Ed25519PrivateKey.generate()
            c.trust["observer"] = observer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
            for observed in observations.values():
                payload = observed["signed_installation"]["payload"]
                observed["signed_installation"]["signature"] = base64.b64encode(
                    observer.sign(install_canonical(payload))).decode()
        proof = {"source_bytes": b"source",
                 "builder_spec_bytes": b"builder", "build_bytes": c.data,
                 "signed_build": c.build_signed, "signed_execution": c.signed_execution,
                 "execution_id": "job-run-42", "scopes": observations,
                 "requirements": sorted(REQUIRED_PROOFS)}
        policy["source_digest"] = "sha256:" + hashlib.sha256(proof["source_bytes"]).hexdigest()
        policy["builder_spec_digest"] = "sha256:" + hashlib.sha256(proof["builder_spec_bytes"]).hexdigest()
        # Sign the component observations for the actual source and builder bytes.
        c.source["source_digest"] = policy["source_digest"]
        c.builder["builder_spec_digest"] = policy["builder_spec_digest"]
        c.executor_policy["builder_spec_digest"] = policy["builder_spec_digest"]
        build_signer = Ed25519PrivateKey.generate()
        c.builder_keys["builder"] = build_signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        build_payload = dict(c.build_signed["payload"], source_digest=policy["source_digest"],
                             builder_spec_digest=policy["builder_spec_digest"])
        from zta_build_provenance import canonical as build_canonical
        proof["signed_build"] = {"payload": build_payload, "signature": base64.b64encode(
            build_signer.sign(build_canonical(build_payload))).decode()}
        executor = Ed25519PrivateKey.generate()
        c.executor_keys["executor"] = executor.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        execution_payload = dict(c.signed_execution["payload"],
                                 source_digest=policy["source_digest"],
                                 builder_spec_digest=policy["builder_spec_digest"])
        from zta_build_execution import canonical as execution_canonical
        proof["signed_execution"] = {"payload": execution_payload, "signature": base64.b64encode(
            executor.sign(execution_canonical(execution_payload))).decode()}
        c.executions["job-run-42"] = ("app", "commit-a", policy["source_digest"],
            "build-42", policy["builder_spec_digest"], policy["sha256"], "SUCCESS", "executor")
        envelope["signature"] = base64.b64encode(self.approver.sign(canonical_bytes(policy))).decode()
        return {"policy_envelope": envelope, "proof": proof,
                "trusted_approvers": {"owner": self.approver.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)},
                "trusted_builders": c.builder_keys, "trusted_executors": c.executor_keys,
                "trusted_observers": c.trust, "corroborated_executions": c.executions,
                "required_scopes": list(scopes)}

    def assess(self, assessment=None, **kwargs):
        return zta.evaluate(self.catalog, self.profile, self.target,
                            as_of="2026-10-27T00:00:00Z",
                            artifact_assessment=self.assessment if assessment is None else assessment,
                            **kwargs)

    def control(self, result):
        return next(c for c in result["control_results"] if c["control_id"] == "ZTA-08.02")

    def test_complete_chain_passes_only_artifact_control_and_is_deterministic(self):
        first = self.assess()
        self.assertEqual(first, self.assess())
        self.assertEqual(self.control(first)["status"], "PASS")
        self.assertEqual(len(self.control(first)["evidence_ids"]), 2)
        self.assertEqual(first["release_eligibility"], "BLOCKED")
        self.assertTrue(all(c["status"] == "UNVERIFIED" for c in first["control_results"]
                            if c["control_id"] != "ZTA-08.02"))
        zta.validate("result", first)

    def test_declared_platform_scopes_all_required(self):
        assessment = self.make_assessment(("linux", "windows", "macos"))
        self.assertEqual(self.control(self.assess(assessment))["status"], "PASS")
        del assessment["proof"]["scopes"]["windows"]
        self.assertEqual(self.control(self.assess(assessment))["status"], "UNVERIFIED")

    def test_tampering_and_incomplete_proof_never_pass(self):
        cases = []
        for path, value in (("build_bytes", b"changed"), ("source_bytes", b"changed"),
                            ("builder_spec_bytes", b"changed")):
            altered = copy.deepcopy(self.assessment)
            altered["proof"][path] = value
            cases.append(altered)
        for field in ("distribution_bytes", "installed_bytes"):
            altered = copy.deepcopy(self.assessment)
            altered["proof"]["scopes"]["linux-x64/production"][field] = b"changed"
            cases.append(altered)
        altered = copy.deepcopy(self.assessment)
        altered["proof"]["signed_build"]["signature"] = "AA=="
        cases.append(altered)
        altered = copy.deepcopy(self.assessment)
        altered["proof"]["scopes"]["linux-x64/production"]["signed_installation"]["signature"] = "AA=="
        cases.append(altered)
        altered = copy.deepcopy(self.assessment)
        altered["policy_envelope"]["payload"]["revision"] = "stale"
        cases.append(altered)
        altered = copy.deepcopy(self.assessment)
        altered["proof"]["requirements"].remove("distribution")
        cases.append(altered)
        altered = copy.deepcopy(self.assessment)
        altered["corroborated_executions"] = {}
        cases.append(altered)
        altered = copy.deepcopy(self.assessment)
        altered["required_scopes"] = ["linux-x64/production", "windows"]
        cases.append(altered)
        altered = copy.deepcopy(self.assessment)
        altered["trusted_approvers"] = {}
        cases.append(altered)
        for altered in cases:
            with self.subTest(altered=altered):
                self.assertEqual(self.control(self.assess(altered))["status"], "UNVERIFIED")

    def test_expired_or_missing_as_of_cannot_pass(self):
        expired = zta.evaluate(self.catalog, self.profile, self.target,
            as_of="2026-11-01T00:00:00Z", artifact_assessment=self.assessment)
        self.assertEqual(self.control(expired)["status"], "UNVERIFIED")
        missing = zta.evaluate(self.catalog, self.profile, self.target,
            artifact_assessment=self.assessment)
        self.assertEqual(self.control(missing)["status"], "UNVERIFIED")

    def test_evaluation_is_read_only(self):
        with patch("pathlib.Path.write_bytes", side_effect=AssertionError("write")), \
             patch("pathlib.Path.write_text", side_effect=AssertionError("write")), \
             patch("subprocess.Popen", side_effect=AssertionError("process")), \
             patch("socket.socket", side_effect=AssertionError("network")):
            self.assertEqual(self.control(self.assess())["status"], "PASS")

    def test_separate_incomplete_or_contradictory_package_cannot_pass(self):
        from zta_decision_gate import classify_control
        result = classify_control(control_id="ZTA-08.02", mandatory=True,
            artifact_verification={"status": "WHOLE_CHAIN_VERIFIED"},
            proof_coverage={"status": "INCOMPLETE"})
        self.assertEqual(result["status"], "UNVERIFIED")

    def test_verified_negative_observation_overrides_complete_chain(self):
        signer = Ed25519PrivateKey.generate()
        payload = {"domain": "gc-audit.zta.negative-observation.v1",
                   "target_id": "app", "revision": "commit-a", "control_id": "ZTA-08.02",
                   "evidence_id": "ev-negative", "test_id": "substitution",
                   "observation": "VIOLATION", "producer_key_id": "ci"}
        raw = zta.canonical(payload)
        evidence = copy.deepcopy(FIXTURE["evidence"])
        evidence.update(evidence_id="ev-negative", target_id="app", revision="commit-a",
                        control_ids=["ZTA-08.02"], source_digest="sha256:" + hashlib.sha256(raw).hexdigest(),
                        producer={"identity": "ci", "identity_status": "VERIFIED"})
        envelope = {"payload": payload, "signature": base64.b64encode(signer.sign(raw)).decode()}
        result = self.assess(evidence_records=[evidence], evidence_sources={"fixtures/sample": raw},
            negative_observations=[envelope], trusted_observation_keys={"ci": signer.public_key().public_bytes(
                Encoding.Raw, PublicFormat.Raw)})
        self.assertEqual(self.control(result)["status"], "FAIL")
        self.assertEqual(result["release_eligibility"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
