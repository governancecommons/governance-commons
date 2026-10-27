"""Independent artifact-pin positive proof, with negative adversarial cases."""
import hashlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from zta_positive_checks import verify_artifact_pair

class ArtifactPositiveTests(unittest.TestCase):
    def setUp(self):
        self.build = b"approved-release-artifact-binary"
        self.pin = {"target_id":"sample","revision":"abc123",
                    "sha256":"sha256:"+hashlib.sha256(self.build).hexdigest()}
    def test_correct_build_and_installed_bytes(self):
        result = verify_artifact_pair("sample","abc123",self.pin,self.build,self.build)
        self.assertEqual(result["status"],"BYTE_INTEGRITY_VERIFIED")
        self.assertNotEqual(result["status"],"PASS")
    def test_modified_installed_artifact(self):
        with self.assertRaises(ValueError):
            verify_artifact_pair("sample","abc123",self.pin,self.build,self.build+b"attack")
    def test_modified_build_artifact(self):
        with self.assertRaises(ValueError):
            verify_artifact_pair("sample","abc123",self.pin,b"modified",self.build)
    def test_wrong_revision(self):
        with self.assertRaises(ValueError):
            verify_artifact_pair("sample","other",self.pin,self.build,self.build)
    def test_wrong_target(self):
        with self.assertRaises(ValueError):
            verify_artifact_pair("imposter","abc123",self.pin,self.build,self.build)
    def test_malformed_pin(self):
        pin=dict(self.pin,sha256="sha256:"+("z"*64))
        with self.assertRaises(ValueError):
            verify_artifact_pair("sample","abc123",pin,self.build,self.build)
    def test_empty_and_text_rejected(self):
        for x in (b"", "text", None):
            with self.subTest(value=x):
                with self.assertRaises(ValueError):
                    verify_artifact_pair("sample","abc123",self.pin,self.build,x)

if __name__ == "__main__":
    unittest.main()
