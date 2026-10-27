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
