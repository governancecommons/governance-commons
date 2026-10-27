"""Build-execution assurance must reject forged and uncorroborated claims."""
import base64
import sys
import unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from zta_build_execution import DOMAIN,canonical,verify_build_execution

class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.sk=Ed25519PrivateKey.generate()
        self.keys={"ci":self.sk.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)}
        self.source={"revision":"rev","source_digest":"sha256:"+"a"*64}
        self.builder={"executor_key_id":"ci","builder_spec_digest":"sha256:"+"b"*64}
        self.release={"target_id":"app","revision":"rev","build_id":"build-5","sha256":"sha256:"+"c"*64}
        self.p={"domain":DOMAIN,"target_id":"app","revision":"rev","source_digest":self.source["source_digest"],
                "build_id":"build-5","builder_spec_digest":self.builder["builder_spec_digest"],
                "artifact_sha256":self.release["sha256"],"execution_id":"run-1",
                "execution_outcome":"SUCCESS","executor_key_id":"ci"}
        self.registry={"run-1":("app","rev",self.source["source_digest"],"build-5",
                       self.builder["builder_spec_digest"],self.release["sha256"],"SUCCESS","ci")}
    def envelope(self):
        return {"payload":dict(self.p),"signature":base64.b64encode(self.sk.sign(canonical(self.p))).decode()}
    def check(self,envelope=None,**overrides):
        args=dict(envelope=self.envelope() if envelope is None else envelope,
                  trusted_executors=self.keys,corroborated_executions=self.registry,
                  approved_source=self.source,approved_builder=self.builder,release=self.release)
        args.update(overrides)
        return verify_build_execution(**args)
    def test_success_is_still_not_pass(self):
        r=self.check()
        self.assertEqual(r["status"],"BUILD_EXECUTION_CORROBORATED")
        self.assertEqual(r["release_decision"],"UNVERIFIED")
    def test_signed_but_uncorroborated_rejected(self):
        with self.assertRaises(ValueError):self.check(corroborated_executions={})
    def test_wrong_independent_result_rejected(self):
        with self.assertRaises(ValueError):self.check(corroborated_executions={"run-1":("SUCCESS",)})
    def test_signature_substitution_rejected(self):
        e=self.envelope()
        e["signature"]=base64.b64encode(b"x"*64).decode()
        with self.assertRaises(ValueError):self.check(envelope=e)
    def test_source_substitution_rejected(self):
        with self.assertRaises(ValueError):
            self.check(approved_source=dict(self.source,source_digest="sha256:"+"d"*64))
    def test_builder_substitution_rejected(self):
        with self.assertRaises(ValueError):
            self.check(approved_builder=dict(self.builder,builder_spec_digest="sha256:"+"d"*64))
    def test_revoked_executor_rejected(self):
        with self.assertRaises(ValueError):self.check(trusted_executors={})
    def test_failed_execution_rejected(self):
        self.p["execution_outcome"]="FAIL"
        with self.assertRaises(ValueError):self.check()
    def test_wrong_release_rejected(self):
        with self.assertRaises(ValueError):self.check(release=dict(self.release,build_id="other"))
if __name__=="__main__":
    unittest.main()
