"""Proof-package validation: never trust completeness declared by a target."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from zta_proof_packages import check_proof_package, ProofPackageError

D = "sha256:" + "a" * 64

def fixture():
    package = {
        "schema":"gc-audit.zta-proof-package.v1","version":"1.0.0","id":"p1",
        "target_id":"sample","revision":"abc123","control_id":"ZTA-08.02",
        "authority":{"key_id":"owner-key","role":"RELEASE_AUTHORITY","trust_reference":"approval-1"},
        "checker":{"id":"artifact-check","version":"1.0.0","spec_digest":D},
        "requirements":["build","installed"],
        "proofs":[{"requirement_id":req,"evidence_id":"e-"+req,"checker_result":"VERIFIED","digest":D}
                  for req in ("build","installed")],
        "artifact_origin":{"repository":"org/repo","source_revision":"abc123","build_reference":"ci-1"},
        "limitations":[]}
    args = {"target_id":"sample","revision":"abc123","expected_control":"ZTA-08.02",
            "trusted_requirements":{"ZTA-08.02":["build","installed"]},
            "approved_checkers":{"artifact-check":("1.0.0",D)},
            "verified_evidence_ids":{"e-build","e-installed"},
            "trusted_authority_keys":{"owner-key":b"trusted-public-key"},
            "independently_verified_results":{
                ("artifact-check","e-build","build"):("VERIFIED",D),
                ("artifact-check","e-installed","installed"):("VERIFIED",D)}}
    return package,args

class ProofPackages(unittest.TestCase):
    def test_complete_is_not_pass(self):
        p,a=fixture()
        result=check_proof_package(p,**a)
        self.assertEqual(result["status"],"PROOF_PACKAGE_COMPLETE")
        self.assertNotEqual(result["status"],"PASS")
    def test_target_cannot_reduce_requirements(self):
        p,a=fixture()
        p["requirements"]=["build"]
        p["proofs"]=p["proofs"][:1]
        with self.assertRaises(ProofPackageError): check_proof_package(p,**a)
    def test_no_self_verified_checker_results(self):
        p,a=fixture()
        a["independently_verified_results"]={}
        with self.assertRaises(ProofPackageError): check_proof_package(p,**a)
    def test_checker_substitution_rejected(self):
        p,a=fixture()
        p["checker"]["spec_digest"]="sha256:"+"b"*64
        with self.assertRaises(ProofPackageError): check_proof_package(p,**a)
    def test_rogue_authority_rejected(self):
        p,a=fixture()
        p["authority"]["key_id"]="untrusted"
        with self.assertRaises(ProofPackageError): check_proof_package(p,**a)
    def test_revision_and_control_substitution_rejected(self):
        for field,value in (("revision","other"),("control_id","ZTA-01.01")):
            with self.subTest(field=field):
                p,a=fixture()
                p[field]=value
                with self.assertRaises(ProofPackageError): check_proof_package(p,**a)
    def test_unverified_evidence_rejected(self):
        p,a=fixture()
        a["verified_evidence_ids"]={"e-build"}
        with self.assertRaises(ProofPackageError): check_proof_package(p,**a)
    def test_missing_proof_is_incomplete(self):
        p,a=fixture()
        p["proofs"]=p["proofs"][:1]
        result=check_proof_package(p,**a)
        self.assertEqual(result["status"],"INCOMPLETE")
        self.assertEqual(result["missing"],["installed"])
    def test_negative_or_inconclusive_cannot_pass(self):
        for state,outcome in (("FAILED","NEGATIVE_REVIEW_REQUIRED"),("INCONCLUSIVE","UNVERIFIED")):
            p,a=fixture()
            p["proofs"][0]["checker_result"]=state
            a["independently_verified_results"][("artifact-check","e-build","build")]=(state,D)
            self.assertEqual(check_proof_package(p,**a)["status"],outcome)
    def test_duplicate_proof_rejected(self):
        p,a=fixture()
        p["proofs"].append(copy.deepcopy(p["proofs"][0]))
        with self.assertRaises(ProofPackageError): check_proof_package(p,**a)
    def test_schema_rejects_unknown_fields(self):
        p,a=fixture()
        p["approves_everything"]=True
        with self.assertRaises(ProofPackageError): check_proof_package(p,**a)

if __name__=="__main__":
    unittest.main()
