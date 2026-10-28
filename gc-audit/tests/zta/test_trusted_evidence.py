"""Synthetic host roots and adversarial signed evidence regression checks."""
import base64
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from trusted_evidence import HostEvidenceVerifier, ReplayLedger, SCHEMAS
from verify_evidence_demo import run_demo
from zta_cli import verify as verify_repository_report
from portal_behavioral_assessment import verify_pilot
from zta_authenticated_packages import canonical_bytes
from zta_evaluator import digest

CATALOG = json.loads((HERE.parents[1] / "catalogs" / "gc-audit.zta-controls.v1.draft.json").read_text(encoding="utf-8"))
CONTROL = next(c for c in CATALOG["controls"] if c["control_id"] == "ZTA-02.01")
NOW = "2026-10-28T12:00:00Z"
REVISION = "a" * 40


def public_bytes(key):
    return key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def signed(payload, key):
    return {"payload": payload, "signature": base64.b64encode(key.sign(canonical_bytes(payload))).decode("ascii")}


class TrustedEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.root = Ed25519PrivateKey.generate()
        self.producer = Ed25519PrivateKey.generate()
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ledger = ReplayLedger(Path(self.temp.name) / "replay.sqlite")
        self.addCleanup(self.ledger.close)
        self.verifier = HostEvidenceVerifier(root_keys={"host-root": public_bytes(self.root)}, replay_ledger=self.ledger)
        self.policy = signed({
            "domain": "gc-audit.host-authority.v1", "policy_id": "local-pilot",
            "root_key_id": "host-root", "target_id": "portal", "revision": REVISION,
            "environment": "synthetic-loopback", "catalog_digest": digest(CATALOG),
            "controls": [{"control_id": CONTROL["control_id"], "objective_digest": digest(CONTROL["objective"]),
                          "methods": ["AUTOMATED_TEST"], "scopes": ["local-http"]}],
            "producers": [{"key_id": "producer-1", "public_key_b64": base64.b64encode(public_bytes(self.producer)).decode("ascii"),
                           "valid_from": "2026-10-28T11:00:00Z", "valid_until": "2026-10-28T13:00:00Z"}],
            "issued_at": "2026-10-28T11:00:00Z", "expires_at": "2026-10-28T13:00:00Z",
            "max_evidence_age_seconds": 3600, "revoked_evidence_ids": []}, self.root)
        observation = {"request": "anonymous dashboard", "observed_status": 401, "claim": "local assertion only"}
        self.envelope = signed({
            "domain": "gc-audit.evidence-envelope.v1", "evidence_id": "evidence-1",
            "nonce": "unique-nonce-0001", "policy_id": "local-pilot", "target_id": "portal",
            "revision": REVISION, "environment": "synthetic-loopback",
            "control_id": CONTROL["control_id"], "objective_digest": digest(CONTROL["objective"]),
            "method": "AUTOMATED_TEST", "scope": "local-http", "producer_key_id": "producer-1",
            "collected_at": "2026-10-28T11:30:00Z", "expires_at": "2026-10-28T12:30:00Z",
            "observation": observation, "observation_digest": digest(observation),
            "limitations": ["synthetic local request"]}, self.producer)

    def check(self, authority=None, envelopes=None, **overrides):
        kwargs = dict(authority=self.policy if authority is None else authority,
                      envelopes=[self.envelope] if envelopes is None else envelopes,
                      catalog=CATALOG, target_id="portal", revision=REVISION,
                      environment="synthetic-loopback", expected_control_ids={CONTROL["control_id"]}, as_of=NOW)
        kwargs.update(overrides)
        return self.verifier.verify(**kwargs)

    def resign_policy(self, changed):
        return signed(changed, self.root)

    def resign_evidence(self, changed):
        return signed(changed, self.producer)

    def test_contract_schemas_are_valid(self):
        for path in SCHEMAS.glob("*.schema.json"):
            Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))

    def test_committed_demo_and_historical_reports_reopen(self):
        reports = HERE.parents[1] / "reports"
        self.assertEqual(run_demo(), json.loads((reports / "evidence-001-verification.json").read_text(encoding="utf-8")))
        verify_repository_report(json.loads((reports / "portal-kit-gate1.json").read_text(encoding="utf-8")))
        verify_pilot(json.loads((reports / "portal-application-zta-pilot.json").read_text(encoding="utf-8")))

    def test_authenticated_local_evidence_is_never_control_pass(self):
        accepted = self.check()
        self.assertEqual(accepted["status"], "AUTHENTICATED")
        self.assertEqual(accepted["producer_authentication"], "SIGNATURE_VERIFIED")
        self.assertEqual(accepted["host_authority"], "CONFIGURED_ROOT_ONLY")
        self.assertEqual(accepted["control_status"], "UNVERIFIED")
        self.assertEqual(self.check()["status"], "REJECTED")
        self.assertIn("replayed", self.check()["reason"])

    def test_replay_survives_new_verifier_with_same_ledger_file(self):
        self.assertEqual(self.check()["status"], "AUTHENTICATED")
        second_ledger = ReplayLedger(Path(self.temp.name) / "replay.sqlite")
        try:
            second = HostEvidenceVerifier(root_keys={"host-root": public_bytes(self.root)}, replay_ledger=second_ledger)
            result = second.verify(authority=self.policy, envelopes=[self.envelope], catalog=CATALOG,
                target_id="portal", revision=REVISION, environment="synthetic-loopback",
                expected_control_ids={CONTROL["control_id"]}, as_of=NOW)
            self.assertEqual(result["status"], "REJECTED")
            self.assertIn("replayed", result["reason"])
        finally:
            second_ledger.close()

    def test_unknown_substituted_and_caller_embedded_roots(self):
        alternate = Ed25519PrivateKey.generate()
        forged = signed(self.policy["payload"], alternate)
        self.assertEqual(self.check(authority=forged)["status"], "REJECTED")
        unknown = copy.deepcopy(self.policy["payload"]); unknown["root_key_id"] = "other-root"
        self.assertEqual(self.check(authority=signed(unknown, alternate))["status"], "REJECTED")
        embedded = copy.deepcopy(self.envelope); embedded["trusted_roots"] = {"host-root": "caller-chosen"}
        self.assertEqual(self.check(envelopes=[embedded])["status"], "REJECTED")
        unknown_producer = copy.deepcopy(self.envelope["payload"])
        unknown_producer["producer_key_id"] = "other-producer"
        self.assertEqual(self.check(envelopes=[self.resign_evidence(unknown_producer)])["status"], "REJECTED")
        switched_producer = Ed25519PrivateKey.generate()
        self.assertEqual(self.check(envelopes=[signed(self.envelope["payload"], switched_producer)])["status"], "REJECTED")

    def test_modified_observation_and_signature(self):
        changed = copy.deepcopy(self.envelope); changed["payload"]["observation"]["observed_status"] = 200
        self.assertEqual(self.check(envelopes=[changed])["status"], "REJECTED")
        changed = copy.deepcopy(self.envelope); changed["signature"] = base64.b64encode(b"wrong").decode("ascii")
        self.assertEqual(self.check(envelopes=[changed])["status"], "REJECTED")

    def test_wrong_target_revision_environment(self):
        for field, value in (("target_id", "other"), ("revision", "b" * 40), ("environment", "production")):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.envelope["payload"]); changed[field] = value
                self.assertEqual(self.check(envelopes=[self.resign_evidence(changed)])["status"], "REJECTED")

    def test_expired_revoked_authority_and_producer(self):
        for field, value in (("expires_at", "2026-10-28T11:59:59Z"), ("revoked_at", "2026-10-28T11:59:59Z")):
            changed = copy.deepcopy(self.policy["payload"]); changed[field] = value
            self.assertEqual(self.check(authority=self.resign_policy(changed))["status"], "REJECTED")
        changed = copy.deepcopy(self.policy["payload"]); changed["producers"][0]["revoked_at"] = "2026-10-28T11:59:59Z"
        self.assertEqual(self.check(authority=self.resign_policy(changed))["status"], "REJECTED")
        revoked = HostEvidenceVerifier(root_keys={"host-root": public_bytes(self.root)},
                                       revoked_root_ids={"host-root"}, replay_ledger=self.ledger)
        self.assertEqual(revoked.verify(authority=self.policy, envelopes=[self.envelope], catalog=CATALOG,
            target_id="portal", revision=REVISION, environment="synthetic-loopback",
            expected_control_ids={CONTROL["control_id"]}, as_of=NOW)["status"], "REJECTED")
        for setting in ({"revoked_policy_ids": {"local-pilot"}},
                        {"revoked_producer_key_ids": {"producer-1"}}):
            verifier = HostEvidenceVerifier(root_keys={"host-root": public_bytes(self.root)},
                                            replay_ledger=self.ledger, **setting)
            result = verifier.verify(authority=self.policy, envelopes=[self.envelope], catalog=CATALOG,
                target_id="portal", revision=REVISION, environment="synthetic-loopback",
                expected_control_ids={CONTROL["control_id"]}, as_of=NOW)
            self.assertEqual(result["status"], "REJECTED")

    def test_unauthorized_control_method_scope_and_objective(self):
        for field, value in (("control_id", "ZTA-02.02"), ("method", "MANUAL_REVIEW"),
                             ("scope", "production"), ("objective_digest", "sha256:" + "0" * 64)):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.envelope["payload"]); changed[field] = value
                self.assertEqual(self.check(envelopes=[self.resign_evidence(changed)])["status"], "REJECTED")

    def test_duplicate_identifiers_and_missing_evidence(self):
        self.assertEqual(self.check(envelopes=[])["status"], "REJECTED")
        duplicate = copy.deepcopy(self.envelope["payload"]); duplicate["nonce"] = "unique-nonce-0002"
        self.assertEqual(self.check(envelopes=[self.envelope, self.resign_evidence(duplicate)])["status"], "REJECTED")
        duplicate = copy.deepcopy(self.envelope["payload"]); duplicate["evidence_id"] = "evidence-2"
        self.assertEqual(self.check(envelopes=[self.envelope, self.resign_evidence(duplicate)])["status"], "REJECTED")
        incomplete = copy.deepcopy(self.envelope); del incomplete["payload"]["observation_digest"]
        self.assertEqual(self.check(envelopes=[incomplete])["status"], "REJECTED")
        expanded = copy.deepcopy(self.policy["payload"])
        expanded["controls"][0]["scopes"].append("second-scope")
        self.assertIn("incomplete", self.check(authority=self.resign_policy(expanded))["reason"])

    def test_local_pass_claim_remains_unverified(self):
        changed = copy.deepcopy(self.envelope["payload"])
        changed["observation"] = {"claim": "PASS", "observed_status": 401}
        changed["observation_digest"] = digest(changed["observation"])
        result = self.check(envelopes=[self.resign_evidence(changed)])
        self.assertEqual(result["status"], "AUTHENTICATED")
        self.assertEqual(result["control_status"], "UNVERIFIED")
        extra = self.resign_evidence(changed); extra["payload"]["control_status"] = "PASS"
        self.assertEqual(self.check(envelopes=[extra])["status"], "REJECTED")


if __name__ == "__main__":
    unittest.main()
