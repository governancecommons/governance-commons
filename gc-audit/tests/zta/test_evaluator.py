"""Negative and deterministic checks for the ZTA read-only core."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODULE = HERE.parents[1] / "tools" / "zta_evaluator.py"
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
