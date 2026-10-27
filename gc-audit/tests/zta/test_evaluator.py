"""Negative and deterministic checks for the ZTA read-only core."""
import copy
import importlib.util
import json
import unittest
import sys
import base64
import hashlib
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE.parents[1] / "tools" / "zta_evaluator.py"
sys.path.insert(0, str(MODULE.parent))
spec = importlib.util.spec_from_file_location("zta_evaluator", MODULE)
zta = importlib.util.module_from_spec(spec)
spec.loader.exec_module(zta)
FIXTURE = json.loads((HERE / "schema-fixtures.v1.json").read_text(encoding="utf-8"))["valid"]

def records():
    c = copy.deepcopy(FIXTURE["controls"])
    p = copy.deepcopy(FIXTURE["profile"])
    t = copy.deepcopy(FIXTURE["target"])
    p["catalog_digest"] = zta.digest(c)
    return c, p, t

class EvaluatorTests(unittest.TestCase):
    def test_fail_closed_and_deterministic(self):
        c,p,t=records()
        a=zta.evaluate(c,p,t)
        self.assertEqual(a,zta.evaluate(c,p,t))
        self.assertEqual(len(a["control_results"]),24)
        self.assertTrue(all(x["status"]=="UNVERIFIED" for x in a["control_results"]))
        self.assertEqual(a["release_eligibility"],"BLOCKED")
        zta.validate("result",a)
    def test_catalog_tamper(self):
        c,p,t=records()
        c["controls"][0]["objective"]="malicious change"
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t)
    def test_duplicate_catalog_control(self):
        c,p,t=records()
        c["controls"][1]["control_id"]=c["controls"][0]["control_id"]
        p["catalog_digest"]=zta.digest(c)
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t)
    def test_stale_evidence_rejected(self):
        c,p,t=records()
        e=copy.deepcopy(FIXTURE["evidence"])
        e["revision"]="wrong revision"
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,[e])
    def test_no_unsafe_profile_interpretation(self):
        c,p,t=records()
        p["inherits"]=["unknown"]
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t)
    def test_no_unproven_pass(self):
        c,p,t=records()
        e=copy.deepcopy(FIXTURE["evidence"])
        a=zta.evaluate(c,p,t,[e])
        self.assertFalse(any(x["status"]=="PASS" for x in a["control_results"]))
    def test_supplied_bytes_integrity_cannot_create_pass(self):
        import hashlib
        c,p,t=records()
        e=copy.deepcopy(FIXTURE["evidence"])
        payload=b"bounded fixture from separately approved tests"
        e["source_digest"]="sha256:"+hashlib.sha256(payload).hexdigest()
        evidence=zta.verify_evidence_bytes(e, {"fixtures/sample":payload})
        self.assertEqual(evidence["integrity"],"VERIFIED")
        self.assertEqual(evidence["producer_identity"],"UNVERIFIED")
        assessed=zta.evaluate(c,p,t,[e],evidence_sources={"fixtures/sample":payload})
        self.assertEqual(assessed["release_eligibility"],"BLOCKED")
        self.assertTrue(all(x["status"]=="UNVERIFIED" for x in assessed["control_results"]))
    def test_tampered_evidence_rejected(self):
        import hashlib
        c,p,t=records()
        e=copy.deepcopy(FIXTURE["evidence"])
        e["source_digest"]="sha256:"+hashlib.sha256(b"legit").hexdigest()
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,[e],evidence_sources={"fixtures/sample":b"tampered"})
    def test_missing_evidence_bytes_rejected(self):
        c,p,t=records()
        e=copy.deepcopy(FIXTURE["evidence"])
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,[e],evidence_sources={})
    def test_profile_inheritance_resolution(self):
        c,p,t=records()
        parent=copy.deepcopy(p)
        parent["profile_id"]="zta.library.v1"
        parent["mandatory_control_ids"]=["ZTA-01.01"]
        child=copy.deepcopy(p)
        child["profile_id"]="zta.cli-hosted.v1"
        child["inherits"]=["zta.library.v1"]
        child["mandatory_control_ids"]=["ZTA-02.01"]
        t["profile_id"]="zta.cli-hosted.v1"
        resolved=zta.resolve_profile(child,[parent])
        self.assertEqual(resolved["mandatory_control_ids"],["ZTA-01.01","ZTA-02.01"])
        assessment=zta.evaluate(c,child,t,inherited_profiles=[parent])
        self.assertEqual(assessment["release_eligibility"],"BLOCKED")
    def test_profile_cycle_rejected(self):
        c,p,t=records()
        p["inherits"]=["zta.cli-hosted.v1"]
        other=copy.deepcopy(p)
        other["profile_id"]="zta.cli-hosted.v1"
        other["inherits"]=["zta.library.v1"]
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,inherited_profiles=[other])
    def test_control_evidence_trace_does_not_promise_pass(self):
        c,p,t=records()
        e=copy.deepcopy(FIXTURE["evidence"])
        e["control_ids"]=["ZTA-01.01","ZTA-05.01"]
        result=zta.evaluate(c,p,t,[e])
        values={r["control_id"]:r for r in result["control_results"]}
        self.assertEqual(values["ZTA-01.01"]["evidence_ids"],["ev1"])
        self.assertEqual(values["ZTA-05.01"]["evidence_ids"],["ev1"])
        self.assertEqual(values["ZTA-01.01"]["status"],"UNVERIFIED")
        self.assertEqual(values["ZTA-05.01"]["status"],"UNVERIFIED")
        self.assertEqual(result["release_eligibility"],"BLOCKED")
        self.assertEqual(result,zta.evaluate(c,p,t,[e]))
    def test_inherited_conditional_cannot_silently_be_ignored(self):
        c,p,t=records()
        parent=copy.deepcopy(p)
        parent["conditional_rules"]=[{"control_id":"ZTA-02.01","when":"privileged dispatch"}]
        child=copy.deepcopy(p)
        child["profile_id"]="zta.cli-hosted.v1"
        child["inherits"]=["zta.library.v1"]
        t["profile_id"]="zta.cli-hosted.v1"
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,child,t,inherited_profiles=[parent])
    def test_duplicate_parent_profile_rejected(self):
        c,p,t=records()
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,inherited_profiles=[copy.deepcopy(p)])
    def test_target_declared_absence_is_not_n_a(self):
        c,p,t=records()
        t["capabilities"]=[]
        result=zta.evaluate(c,p,t)
        self.assertTrue(all(r["status"]!="NOT_APPLICABLE" for r in result["control_results"]))
    def test_signed_negative_observation_fails_one_control(self):
        c,p,t=records()
        e=copy.deepcopy(FIXTURE['evidence'])
        signer=Ed25519PrivateKey.generate()
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        pub=signer.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
        payload={'domain':'gc-audit.zta.negative-observation.v1','target_id':t['target_id'],
                 'revision':t['revision'],'control_id':'ZTA-01.01','evidence_id':'ev1',
                 'test_id':'denial-test-1','observation':'VIOLATION','producer_key_id':'ci-trusted'}
        data=zta.canonical(payload)
        envelope={'payload':payload,'signature':base64.b64encode(signer.sign(data)).decode()}
        e['source_digest']='sha256:'+hashlib.sha256(data).hexdigest()
        e['producer']={'identity':'ci-trusted','identity_status':'VERIFIED'}
        a=zta.evaluate(c,p,t,[e],evidence_sources={'fixtures/sample':data},
                       negative_observations=[envelope],trusted_observation_keys={'ci-trusted':pub})
        values={r['control_id']:r for r in a['control_results']}
        self.assertEqual(values['ZTA-01.01']['status'],'FAIL')
        self.assertEqual(values['ZTA-01.02']['status'],'UNVERIFIED')
        self.assertEqual(a['release_eligibility'],'BLOCKED')
        self.assertEqual(a['findings'][0]['control_id'],'ZTA-01.01')
        envelope['payload']['revision']='different'
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,[e],evidence_sources={'fixtures/sample':data},
                         negative_observations=[envelope],trusted_observation_keys={'ci-trusted':pub})
    def test_unsigned_or_untrusted_negative_rejected(self):
        c,p,t=records()
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,negative_observations=[{'payload':{},'signature':'bad'}])
    def test_unsigned_package_policy_rejected(self):
        c,p,t=records()
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,authenticated_packages=[{"package":{"control_id":"ZTA-08.02"}}])
    def test_package_with_fake_signer_does_not_pass(self):
        c,p,t=records()
        policy={"trusted_public_keys":{},"trusted_requirements":{"ZTA-08.02":["build"]},
                "approved_checkers":{},"independently_verified_results":{}}
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,authenticated_packages=[{
                "domain":"gc-audit.zta.proof-package-envelope.v1",
                "package":{"control_id":"ZTA-08.02","authority":{"key_id":"forged"}},
                "signature":"AA=="}],proof_policy=policy)
    def test_signed_complete_package_cannot_become_pass(self):
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        from zta_authenticated_packages import DOMAIN, canonical_bytes
        c,p,t=records()
        signer=Ed25519PrivateKey.generate()
        pub=signer.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
        payload=b"externally supplied bytes"
        e=copy.deepcopy(FIXTURE["evidence"])
        e["control_ids"]=["ZTA-08.02"]
        e["source_digest"]="sha256:"+hashlib.sha256(payload).hexdigest()
        d="sha256:"+"a"*64
        pkg={"schema":"gc-audit.zta-proof-package.v1","version":"1.0.0","id":"pkg1",
             "target_id":t["target_id"],"revision":t["revision"],"control_id":"ZTA-08.02",
             "authority":{"key_id":"release-owner","role":"RELEASE_AUTHORITY","trust_reference":"owner-pin"},
             "checker":{"id":"artifact","version":"1.0.0","spec_digest":d},
             "requirements":["match-build"],
             "proofs":[{"requirement_id":"match-build","evidence_id":"ev1",
                        "checker_result":"VERIFIED","digest":d}],
             "artifact_origin":{"repository":"org/repo","source_revision":t["revision"],
                                "build_reference":"ci1"},"limitations":[]}
        signed={"domain":DOMAIN,"package":pkg}
        signed["signature"]=base64.b64encode(signer.sign(canonical_bytes(signed))).decode()
        policy={"trusted_public_keys":{"release-owner":pub},
                "trusted_requirements":{"ZTA-08.02":["match-build"]},
                "approved_checkers":{"artifact":("1.0.0",d)},
                "independently_verified_results":{("artifact","ev1","match-build"):("VERIFIED",d)}}
        assessed=zta.evaluate(c,p,t,[e],evidence_sources={"fixtures/sample":payload},
                    authenticated_packages=[signed],proof_policy=policy)
        control=next(r for r in assessed["control_results"] if r["control_id"]=="ZTA-08.02")
        self.assertEqual(control["status"],"UNVERIFIED")
        self.assertEqual(assessed["release_eligibility"],"BLOCKED")
        policy["independently_verified_results"]={}
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,[e],evidence_sources={"fixtures/sample":payload},
                         authenticated_packages=[signed],proof_policy=policy)
    def test_assessment_digest_changes_with_evidence_input(self):
        c,p,t=records()
        e=copy.deepcopy(FIXTURE["evidence"])
        first=zta.evaluate(c,p,t,[e])
        e["limitations"]=["restricted observation scope"]
        second=zta.evaluate(c,p,t,[e])
        self.assertNotEqual(first["normalized_digest"],second["normalized_digest"])
        self.assertNotEqual(first["extensions"]["gc.zta"]["input_digest"],
                            second["extensions"]["gc.zta"]["input_digest"])
    def test_evidence_order_does_not_change_logical_digest(self):
        c,p,t=records()
        first=copy.deepcopy(FIXTURE["evidence"])
        second=copy.deepcopy(first)
        second["evidence_id"]="ev2"
        second["source_refs"]=["fixtures/second"]
        a=zta.evaluate(c,p,t,[first,second])
        b=zta.evaluate(c,p,t,[second,first])
        self.assertEqual(a,b)
    def test_target_revision_changes_assessment_digest(self):
        c,p,t=records()
        a=zta.evaluate(c,p,t)
        t["revision"]="next-revision"
        b=zta.evaluate(c,p,t)
        self.assertNotEqual(a["normalized_digest"],b["normalized_digest"])
    def test_bad_reference_rejected(self):
        c,p,t=records()
        t["control_responsibilities"][0]["component_id"]="nonexistent"
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t)
    def test_evaluator_refuses_freshness_without_policy(self):
        c,p,t=records()
        with self.assertRaises(zta.AssessmentInputError):
            zta.evaluate(c,p,t,as_of="2026-10-27T00:00:00Z")

if __name__=="__main__":
    unittest.main()
