"""Evidence-based artifact-chain candidate and attack regression tests."""
import hashlib
import base64
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from zta_artifact_chain import verify_release_artifact_chain
from zta_installation_attestation import DOMAIN,canonical
from zta_build_provenance import DOMAIN as BUILD_DOMAIN,canonical as build_canonical

class ArtifactChainTests(unittest.TestCase):
    def setUp(self):
        self.data=b"release artifact bytes"
        self.policy={"target_id":"app","revision":"commit-a","sha256":"sha256:"+hashlib.sha256(self.data).hexdigest(),"build_id":"build-42","install_scope":"linux-x64/production"}
        self.observation={k:self.policy[k] for k in ("target_id","revision","build_id","install_scope")}
        signer=Ed25519PrivateKey.generate()
        self.trust={"observer":signer.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)}
        payload={"domain":DOMAIN,**self.observation,"artifact_sha256":self.policy["sha256"],"observer_key_id":"observer"}
        self.signed={"payload":payload,"signature":base64.b64encode(signer.sign(canonical(payload))).decode()}
        self.source={"revision":"commit-a","source_digest":"sha256:"+"a"*64}
        self.builder={"builder_key_id":"builder","builder_spec_digest":"sha256:"+"b"*64}
        build_signer=Ed25519PrivateKey.generate()
        self.builder_keys={"builder":build_signer.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)}
        build_payload={"domain":BUILD_DOMAIN,"target_id":"app","revision":"commit-a",
                       "build_id":"build-42","artifact_sha256":self.policy["sha256"],
                       "builder_key_id":"builder","source_digest":self.source["source_digest"],
                       "builder_spec_digest":self.builder["builder_spec_digest"]}
        self.build_signed={"payload":build_payload,"signature":base64.b64encode(
            build_signer.sign(build_canonical(build_payload))).decode()}
    def check(self,build=None,installed=None,policy=None,observed=None):
        return verify_release_artifact_chain(target_id="app",revision="commit-a",
            trusted_release=self.policy if policy is None else policy,
            build_bytes=self.data if build is None else build,
            installed_bytes=self.data if installed is None else installed,
            observed_install=self.observation if observed is None else observed,
            signed_installation=self.signed,trusted_observers=self.trust,
            signed_build=self.build_signed,trusted_builders=self.builder_keys,
            approved_source=self.source,approved_builder=self.builder)
    def test_matching_artifacts_only_candidate(self):
        r=self.check()
        self.assertEqual(r["status"],"ARTIFACT_CHAIN_CANDIDATE")
        self.assertEqual(r["release_decision"],"UNVERIFIED")
        self.assertTrue(r["limitations"])
    def test_unsigned_chain_rejected(self):
        with self.assertRaises(ValueError):
            verify_release_artifact_chain(target_id="app",revision="commit-a",
                trusted_release=self.policy,build_bytes=self.data,installed_bytes=self.data,
                observed_install=self.observation)
    def test_unsigned_build_rejected(self):
        with self.assertRaises(ValueError):
            verify_release_artifact_chain(target_id="app",revision="commit-a",
                trusted_release=self.policy,build_bytes=self.data,installed_bytes=self.data,
                observed_install=self.observation,signed_installation=self.signed,
                trusted_observers=self.trust)
    def test_installed_tampering(self):
        with self.assertRaises(ValueError):self.check(installed=self.data+b"x")
    def test_build_tampering(self):
        with self.assertRaises(ValueError):self.check(build=self.data+b"x")
    def test_untrusted_revision(self):
        with self.assertRaises(ValueError):
            self.check(observed=dict(self.observation,revision="older"))
    def test_other_build(self):
        with self.assertRaises(ValueError):
            self.check(observed=dict(self.observation,build_id="build-99"))
    def test_other_scope(self):
        with self.assertRaises(ValueError):
            self.check(observed=dict(self.observation,install_scope="staging"))
    def test_missing_release_scope(self):
        p=dict(self.policy)
        del p["install_scope"]
        with self.assertRaises(ValueError):self.check(policy=p)
    def test_malformed_pin(self):
        with self.assertRaises(ValueError):self.check(policy=dict(self.policy,sha256="sha256:bogus"))
    def test_wrong_target(self):
        with self.assertRaises(ValueError):self.check(observed=dict(self.observation,target_id="other"))
if __name__=="__main__":
    unittest.main()
