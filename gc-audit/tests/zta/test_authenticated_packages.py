"""Authenticated proof-package security regression tests."""
import base64
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from zta_authenticated_packages import DOMAIN, canonical_bytes, authenticate_proof_package
from zta_proof_packages import ProofPackageError

D="sha256:"+"a"*64

def scenario():
    sk=Ed25519PrivateKey.generate()
    pub=sk.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
    p={"schema":"gc-audit.zta-proof-package.v1","version":"1.0.0","id":"p1",
       "target_id":"sample","revision":"abc123","control_id":"ZTA-08.02",
       "authority":{"key_id":"owner-key","role":"RELEASE_AUTHORITY","trust_reference":"approval-1"},
       "checker":{"id":"artifact-check","version":"1.0.0","spec_digest":D},
       "requirements":["build","installed"],
       "proofs":[{"requirement_id":v,"evidence_id":"e-"+v,"checker_result":"VERIFIED","digest":D}
                 for v in ("build","installed")],
       "artifact_origin":{"repository":"org/repo","source_revision":"abc123","build_reference":"ci-1"},
       "limitations":[]}
    inputs={"target_id":"sample","revision":"abc123","expected_control":"ZTA-08.02",
            "trusted_requirements":{"ZTA-08.02":["build","installed"]},
            "approved_checkers":{"artifact-check":("1.0.0",D)},
            "verified_evidence_ids":{"e-build","e-installed"},
            "independently_verified_results":{
                ("artifact-check","e-build","build"):("VERIFIED",D),
                ("artifact-check","e-installed","installed"):("VERIFIED",D)}}
    envelope={"domain":DOMAIN,"package":p}
    envelope["signature"]=base64.b64encode(sk.sign(canonical_bytes(envelope))).decode("ascii")
    return envelope, {"owner-key":pub}, inputs, sk

class AuthenticatedProofTests(unittest.TestCase):
    def test_authenticated_complete_not_pass(self):
        env,roots,args,_=scenario()
        result=authenticate_proof_package(env,trusted_public_keys=roots,**args)
        self.assertEqual(result["authentication"],"SIGNATURE_VERIFIED")
        self.assertEqual(result["status"],"PROOF_PACKAGE_COMPLETE")
        self.assertNotIn("PASS",result.values())
    def test_tamper_and_replay_revision_rejected(self):
        for field,value in (("revision","wrong"),("control_id","ZTA-02.01")):
            with self.subTest(field=field):
                env,roots,args,_=scenario()
                env["package"][field]=value
                with self.assertRaises(ProofPackageError):
                    authenticate_proof_package(env,trusted_public_keys=roots,**args)
    def test_signed_attestation_cannot_invent_check_results(self):
        env,roots,args,sk=scenario()
        args["independently_verified_results"]={}
        with self.assertRaises(ProofPackageError):
            authenticate_proof_package(env,trusted_public_keys=roots,**args)
    def test_unknown_key_rejected(self):
        env,_,args,_=scenario()
        with self.assertRaises(ProofPackageError):
            authenticate_proof_package(env,trusted_public_keys={},**args)
    def test_changed_domain_rejected(self):
        env,roots,args,_=scenario()
        env["domain"]="another.domain"
        with self.assertRaises(ProofPackageError):
            authenticate_proof_package(env,trusted_public_keys=roots,**args)
    def test_signature_substitution_rejected(self):
        env,roots,args,_=scenario()
        env["signature"]=base64.b64encode(b"X"*64).decode("ascii")
        with self.assertRaises(ProofPackageError):
            authenticate_proof_package(env,trusted_public_keys=roots,**args)
    def test_owner_key_cannot_waive_missing_requirement(self):
        env,roots,args,sk=scenario()
        env["package"]["requirements"]=["build"]
        env["package"]["proofs"]=env["package"]["proofs"][:1]
        env["signature"]=base64.b64encode(
            sk.sign(canonical_bytes({"domain":DOMAIN,"package":env["package"]}))).decode("ascii")
        with self.assertRaises(ProofPackageError):
            authenticate_proof_package(env,trusted_public_keys=roots,**args)
    def test_signer_identity_cannot_be_switched(self):
        env,roots,args,_=scenario()
        env["package"]["authority"]["key_id"]="other-key"
        with self.assertRaises(ProofPackageError):
            authenticate_proof_package(env,trusted_public_keys=roots,**args)

if __name__=="__main__":
    unittest.main()
