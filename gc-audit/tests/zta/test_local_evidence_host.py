"""Local host boundary tests; no production configuration or credentials."""
import base64
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from local_evidence_host import LocalEvidenceHost, host_principal
from trusted_evidence import ReplayLedger
from zta_authenticated_packages import canonical_bytes
from zta_evaluator import digest

CATALOG = json.loads((HERE.parents[1] / "catalogs" / "gc-audit.zta-controls.v1.draft.json").read_text(encoding="utf-8"))
CONTROL = next(c for c in CATALOG["controls"] if c["control_id"] == "ZTA-02.01")
NOW = "2026-10-28T12:00:00Z"


def signed(payload, key):
    return {"payload": payload, "signature": base64.b64encode(key.sign(canonical_bytes(payload))).decode("ascii")}


def public_key(key):
    return base64.b64encode(key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode("ascii")


class LocalHostTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gc-evidence-host-")
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name).resolve()
        self.host_dir = base / "host"
        self.target = base / "target"
        self.host_dir.mkdir()
        self.target.mkdir()
        self.private_dir(self.host_dir)
        for command in (["git", "init", "-q", str(self.target)],
                        ["git", "-C", str(self.target), "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-q", "--allow-empty", "-m", "fixture"]):
            subprocess.run(command, check=True, capture_output=True)
        self.revision = subprocess.run(["git", "-C", str(self.target), "rev-parse", "HEAD"],
                                       check=True, capture_output=True, text=True).stdout.strip()
        self.root = Ed25519PrivateKey.generate()
        self.producer = Ed25519PrivateKey.generate()
        self.policy = signed({
            "domain": "gc-audit.host-authority.v1", "policy_id": "local-host-pilot", "root_key_id": "host-root",
            "target_id": "fixture-target", "revision": self.revision, "environment": "test-local",
            "catalog_digest": digest(CATALOG), "controls": [{"control_id": CONTROL["control_id"],
                "objective_digest": digest(CONTROL["objective"]), "methods": ["AUTOMATED_TEST"], "scopes": ["fixture"]}],
            "producers": [{"key_id": "producer", "public_key_b64": public_key(self.producer),
                "valid_from": "2026-10-28T11:00:00Z", "valid_until": "2026-10-28T13:00:00Z"}],
            "issued_at": "2026-10-28T11:00:00Z", "expires_at": "2026-10-28T13:00:00Z",
            "max_evidence_age_seconds": 3600, "revoked_evidence_ids": []}, self.root)
        observation = {"claim": "local assertion", "observed_status": 403}
        envelope = signed({"domain": "gc-audit.evidence-envelope.v1", "evidence_id": "local-1",
            "nonce": "local-unique-nonce-1", "policy_id": "local-host-pilot", "target_id": "fixture-target",
            "revision": self.revision, "environment": "test-local", "control_id": CONTROL["control_id"],
            "objective_digest": digest(CONTROL["objective"]), "method": "AUTOMATED_TEST", "scope": "fixture",
            "producer_key_id": "producer", "collected_at": "2026-10-28T11:30:00Z",
            "expires_at": "2026-10-28T12:30:00Z", "observation": observation,
            "observation_digest": digest(observation), "limitations": ["synthetic fixture"]}, self.producer)
        self.package = {"schema": "gc-audit.local-evidence-package.v1", "envelopes": [envelope]}
        self.config = {"schema": "gc-audit.local-host-config.v1", "host_id": "fixture-host",
            "host_principal": host_principal(), "target_root": str(self.target),
            "target_id": "fixture-target", "revision": self.revision, "environment": "test-local",
            "control_ids": [CONTROL["control_id"]], "catalog_digest": digest(CATALOG),
            "policy_digest": digest(self.policy), "root_keys": [{"key_id": "host-root", "public_key_b64": public_key(self.root)}],
            "revoked_root_ids": [], "revoked_policy_ids": [], "revoked_producer_key_ids": []}
        self.write_private("config.json", self.config)
        self.write_private("authority.json", self.policy)
        ledger = ReplayLedger(self.host_dir / "replay.sqlite")
        ledger.close()
        self.private_file(self.host_dir / "replay.sqlite")
        self.package_path = base / "package.json"
        self.write_package(self.package)

    def private_dir(self, path):
        if os.name == "nt":
            subprocess.run(["icacls", str(path), "/inheritance:r"], check=True, capture_output=True)
            subprocess.run(["icacls", str(path), "/grant:r", f"*{host_principal()}:(OI)(CI)F"], check=True, capture_output=True)
            subprocess.run(["icacls", str(path), "/setowner", f"*{host_principal()}"], check=True, capture_output=True)
        else:
            path.chmod(0o700)

    def private_file(self, path):
        if os.name == "nt":
            subprocess.run(["icacls", str(path), "/setowner", f"*{host_principal()}"], check=True, capture_output=True)
        else:
            path.chmod(0o600)

    def write_private(self, name, value):
        path = self.host_dir / name
        path.write_text(json.dumps(value), encoding="utf-8")
        self.private_file(path)

    def write_package(self, value):
        self.package_path.write_text(json.dumps(value), encoding="utf-8")

    def verify(self, *, pin=None):
        return LocalEvidenceHost(self.host_dir, expected_config_digest=pin or digest(self.config)).verify(
            self.package_path, CATALOG, assessed_at=NOW)

    def test_authenticated_receipt_and_replay_after_restart(self):
        first = self.verify()
        self.assertEqual(first["status"], "AUTHENTICATED", first["reason"])
        self.assertEqual(first["control_status"], "UNVERIFIED")
        self.assertEqual(first["host_authority"], "CONFIGURED_ROOT_ONLY")
        self.assertEqual(first["receipt_digest"], digest({k: v for k, v in first.items() if k != "receipt_digest"}))
        second = self.verify()
        self.assertEqual(second["status"], "REJECTED")
        self.assertIn("replayed", second["reason"])

    def test_config_replacement_and_wrong_owner_or_permissions(self):
        original_pin = digest(self.config)
        changed = copy.deepcopy(self.config)
        changed["root_keys"][0]["public_key_b64"] = public_key(Ed25519PrivateKey.generate())
        self.write_private("config.json", changed)
        self.assertIn("deployment pin", self.verify(pin=original_pin)["reason"])
        self.write_private("config.json", self.config)
        if os.name == "nt":
            subprocess.run(["icacls", str(self.host_dir), "/grant", "*S-1-1-0:(OI)(CI)R"], check=True, capture_output=True)
        else:
            self.host_dir.chmod(0o755)
        self.assertIn("host", self.verify()["reason"])

    def test_wrong_owner_and_principal_are_rejected(self):
        changed = copy.deepcopy(self.config); changed["host_principal"] = "different-principal"
        self.write_private("config.json", changed)
        self.assertIn("principal", self.verify(pin=digest(changed))["reason"])
        self.write_private("config.json", self.config)
        if os.name == "nt":
            from local_evidence_host import _windows_acl
            def wrong_owner(path):
                value = _windows_acl(path)
                if path == self.host_dir:
                    value["owner"] = "S-1-5-21-0-0-0-9999"
                return value
            with patch("local_evidence_host._windows_acl", side_effect=wrong_owner):
                self.assertIn("owner", self.verify()["reason"])
        else:
            with patch("local_evidence_host.os.geteuid", return_value=os.geteuid() + 1):
                self.assertIn("owner", self.verify()["reason"])

    def test_missing_replay_storage_and_policy_replacement(self):
        ledger = self.host_dir / "replay.sqlite"
        ledger.unlink()
        self.assertEqual(self.verify()["status"], "REJECTED")
        self.assertFalse(ledger.exists(), "verification must not recreate missing ledger")
        created = ReplayLedger(ledger); created.close(); self.private_file(ledger)
        changed = copy.deepcopy(self.policy)
        changed["signature"] = base64.b64encode(b"wrong").decode("ascii")
        self.write_private("authority.json", changed)
        self.assertIn("authority policy differs", self.verify()["reason"])

    def test_untrusted_key_revocation_and_expiration(self):
        other = copy.deepcopy(self.config)
        other["root_keys"][0]["public_key_b64"] = public_key(Ed25519PrivateKey.generate())
        self.write_private("config.json", other)
        self.assertEqual(self.verify(pin=digest(other))["status"], "REJECTED")
        self.write_private("config.json", self.config)
        for field, value in (("revoked_root_ids", ["host-root"]),
                             ("revoked_policy_ids", ["local-host-pilot"]),
                             ("revoked_producer_key_ids", ["producer"])):
            changed = copy.deepcopy(self.config); changed[field] = value
            self.write_private("config.json", changed)
            self.assertEqual(self.verify(pin=digest(changed))["status"], "REJECTED")
        self.write_private("config.json", self.config)
        expired = copy.deepcopy(self.policy["payload"]); expired["expires_at"] = "2026-10-28T11:59:59Z"
        changed_policy = signed(expired, self.root)
        self.write_private("authority.json", changed_policy)
        changed = copy.deepcopy(self.config); changed["policy_digest"] = digest(changed_policy)
        self.write_private("config.json", changed)
        self.assertEqual(self.verify(pin=digest(changed))["status"], "REJECTED")

    def test_wrong_revision_environment_and_tampering(self):
        changed = copy.deepcopy(self.config); changed["revision"] = "0" * 40
        self.write_private("config.json", changed)
        self.assertIn("target revision", self.verify(pin=digest(changed))["reason"])
        changed = copy.deepcopy(self.config); changed["environment"] = "production"
        self.write_private("config.json", changed)
        self.assertEqual(self.verify(pin=digest(changed))["status"], "REJECTED")
        self.write_private("config.json", self.config)
        modified = copy.deepcopy(self.package)
        modified["envelopes"][0]["payload"]["observation"]["observed_status"] = 200
        self.write_package(modified)
        self.assertEqual(self.verify()["status"], "REJECTED")

    def test_links_overlap_bad_ledger_and_caller_authority(self):
        changed = copy.deepcopy(self.config); changed["target_root"] = str(self.host_dir)
        self.write_private("config.json", changed)
        self.assertIn("overlap", self.verify(pin=digest(changed))["reason"])
        self.write_private("config.json", self.config)
        modified = copy.deepcopy(self.package); modified["root_keys"] = self.config["root_keys"]
        self.write_package(modified)
        self.assertIn("envelopes only", self.verify()["reason"])
        self.write_package(self.package)
        ledger = self.host_dir / "replay.sqlite"
        ledger.write_bytes(b"not sqlite")
        self.assertEqual(self.verify()["status"], "REJECTED")

    def test_link_substitution(self):
        config_path = self.host_dir / "config.json"
        outside = Path(self.temp.name) / "substitute.json"
        outside.write_text(json.dumps(self.config), encoding="utf-8")
        try:
            config_path.unlink()
            config_path.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.write_private("config.json", self.config)
            if os.name != "nt":
                self.skipTest("symlink creation not available for this runner")
            alias = Path(self.temp.name) / "host-junction"
            subprocess.run(["cmd", "/c", "mklink", "/J", str(alias), str(self.host_dir)],
                           check=True, capture_output=True)
            try:
                outcome = LocalEvidenceHost(alias, expected_config_digest=digest(self.config)).verify(
                    self.package_path, CATALOG, assessed_at=NOW)
                self.assertIn("link", outcome["reason"])
            finally:
                alias.rmdir()
            return
        self.assertIn("link", self.verify()["reason"])

    def test_hard_link_substitution(self):
        alias = self.host_dir / "config-alias.json"
        try:
            os.link(self.host_dir / "config.json", alias)
        except OSError:
            self.skipTest("hard link creation not available for this runner")
        self.assertIn("hard links", self.verify()["reason"])
        alias.unlink()

    def test_signed_pass_claim_stays_unverified(self):
        modified = copy.deepcopy(self.package)
        modified["envelopes"][0]["payload"]["observation"] = {"claim": "PASS"}
        modified["envelopes"][0]["payload"]["observation_digest"] = digest({"claim": "PASS"})
        modified["envelopes"][0] = signed(modified["envelopes"][0]["payload"], self.producer)
        self.write_package(modified)
        outcome = self.verify()
        self.assertEqual(outcome["status"], "AUTHENTICATED", outcome["reason"])
        self.assertEqual(outcome["control_status"], "UNVERIFIED")

    def test_traversal_is_rejected(self):
        traversed = self.host_dir.parent / "target" / ".." / "host"
        outcome = LocalEvidenceHost(traversed, expected_config_digest=digest(self.config)).verify(
            self.package_path, CATALOG, assessed_at=NOW)
        self.assertIn("traversal", outcome["reason"])

    def test_target_configured_fsmonitor_is_disabled(self):
        subprocess.run(["git", "-C", str(self.target), "config", "core.fsmonitor", "exit 67"],
                       check=True, capture_output=True)
        outcome = self.verify()
        self.assertEqual(outcome["status"], "AUTHENTICATED", outcome["reason"])


class LocalHostReportTests(unittest.TestCase):
    def test_committed_receipts_reopen(self):
        from verify_local_host_demo import verify_report
        report = json.loads((HERE.parents[1] / "reports" / "evidence-002-local-host.json").read_text(encoding="utf-8"))
        verify_report(report)


if __name__ == "__main__":
    unittest.main()
