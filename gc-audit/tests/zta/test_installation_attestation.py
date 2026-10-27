"""Authenticated installation observation adversarial tests."""
import base64
import hashlib
import sys
import unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from zta_installation_attestation import DOMAIN, canonical, verify_signed_installation

class InstallationAttestationTests(unittest.TestCase):
    def setUp(self):
        self.blob = b"versioned installed payload"
        self.signer = Ed25519PrivateKey.generate()
        pub = self.signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        self.trust = {"deployment-observer": pub}
        self.release = {"target_id": "app", "revision": "rev-A",
                        "build_id": "build-1", "install_scope": "linux-prod",
                        "sha256": "sha256:" + hashlib.sha256(self.blob).hexdigest()}
        self.payload = {"domain": DOMAIN, "target_id": "app", "revision": "rev-A",
                        "build_id": "build-1", "install_scope": "linux-prod",
                        "artifact_sha256": self.release["sha256"],
                        "observer_key_id": "deployment-observer"}
    def envelope(self):
        return {"payload": self.payload.copy(),
                "signature": base64.b64encode(self.signer.sign(canonical(self.payload))).decode()}
    def verify(self, envelope=None, release=None, blob=None, trust=None):
        return verify_signed_installation(
            envelope=self.envelope() if envelope is None else envelope,
            trusted_observers=self.trust if trust is None else trust,
            release=self.release if release is None else release,
            installed_bytes=self.blob if blob is None else blob)
    def test_verified_is_not_pass(self):
        result = self.verify()
        self.assertEqual(result["status"], "SIGNED_INSTALLATION_OBSERVATION")
        self.assertEqual(result["release_decision"], "UNVERIFIED")
    def test_tamper_payload(self):
        envelope = self.envelope()
        envelope["payload"]["install_scope"] = "staging"
        with self.assertRaises(ValueError): self.verify(envelope=envelope)
    def test_tamper_signature(self):
        envelope = self.envelope()
        envelope["signature"] = base64.b64encode(b"X" * 64).decode()
        with self.assertRaises(ValueError): self.verify(envelope=envelope)
    def test_unknown_observer(self):
        with self.assertRaises(ValueError): self.verify(trust={})
    def test_installed_substitution(self):
        with self.assertRaises(ValueError): self.verify(blob=b"modified")
    def test_wrong_revision(self):
        with self.assertRaises(ValueError): self.verify(release=dict(self.release, revision="rev-B"))
    def test_wrong_build(self):
        with self.assertRaises(ValueError): self.verify(release=dict(self.release, build_id="build-2"))
    def test_scope_mismatch(self):
        with self.assertRaises(ValueError): self.verify(release=dict(self.release, install_scope="mac-prod"))
    def test_key_substitution(self):
        other = Ed25519PrivateKey.generate().public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        with self.assertRaises(ValueError): self.verify(trust={"deployment-observer": other})

if __name__ == "__main__":
    unittest.main()
