"""Adversarial checks for authenticated build provenance."""
import base64
import sys
import unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from zta_build_provenance import DOMAIN, canonical, verify_signed_build_provenance

class BuildProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.sk = Ed25519PrivateKey.generate()
        self.keys = {"ci": self.sk.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)}
        self.source = {"revision": "rev-1", "source_digest": "sha256:"+"a"*64}
        self.builder = {"builder_key_id": "ci", "builder_spec_digest": "sha256:"+"b"*64}
        self.release = {"target_id": "app", "revision": "rev-1", "build_id": "job-2",
                        "sha256": "sha256:"+"c"*64, "install_scope": "production"}
        self.payload = {"domain": DOMAIN, "target_id": "app", "revision": "rev-1",
                        "build_id": "job-2", "artifact_sha256": self.release["sha256"],
                        "builder_key_id": "ci", "source_digest": self.source["source_digest"],
                        "builder_spec_digest": self.builder["builder_spec_digest"]}
    def envelope(self):
        return {"payload": dict(self.payload),
                "signature": base64.b64encode(self.sk.sign(canonical(self.payload))).decode()}
    def check(self, envelope=None, **overrides):
        args = dict(envelope=self.envelope() if envelope is None else envelope,
                    trusted_builders=self.keys, approved_source=self.source,
                    approved_builder=self.builder, release=self.release)
        args.update(overrides)
        return verify_signed_build_provenance(**args)
    def test_signed_statement_is_not_pass(self):
        r = self.check()
        self.assertEqual(r["status"], "SIGNED_BUILD_PROVENANCE")
        self.assertEqual(r["release_decision"], "UNVERIFIED")
    def test_signature_tampering(self):
        env = self.envelope()
        env["signature"] = base64.b64encode(b"x"*64).decode()
        with self.assertRaises(ValueError): self.check(env)
    def test_payload_tampering(self):
        env = self.envelope()
        env["payload"]["build_id"] = "job-3"
        with self.assertRaises(ValueError): self.check(env)
    def test_source_substitution(self):
        with self.assertRaises(ValueError):
            self.check(approved_source=dict(self.source, source_digest="sha256:"+"d"*64))
    def test_builder_spec_substitution(self):
        with self.assertRaises(ValueError):
            self.check(approved_builder=dict(self.builder, builder_spec_digest="sha256:"+"d"*64))
    def test_release_substitution(self):
        with self.assertRaises(ValueError):
            self.check(release=dict(self.release, sha256="sha256:"+"d"*64))
    def test_untrusted_signer(self):
        with self.assertRaises(ValueError): self.check(trusted_builders={})
    def test_incomplete_policy(self):
        with self.assertRaises(ValueError): self.check(approved_source={"revision": "rev-1"})

if __name__ == "__main__":
    unittest.main()
