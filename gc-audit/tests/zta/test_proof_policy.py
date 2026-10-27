"""Proof-policy adversarial coverage: admissibility is not a control PASS."""
import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import zta_proof_policy as policy
FIXTURE = json.loads((HERE / "schema-fixtures.v1.json").read_text(encoding="utf-8"))["valid"]["evidence"]

class ProofAdmissibilityTests(unittest.TestCase):
    def evidence(self, method="AUTOMATED_TEST", status="VERIFIED"):
        e=copy.deepcopy(FIXTURE)
        e["control_ids"]=["ZTA-02.01"]
        e["method"]=method
        e["producer"]["identity_status"]=status
        return e
    def test_signed_words_are_not_proof(self):
        e=self.evidence(status="ASSERTED")
        result=policy.assess_admissibility("ZTA-02.01",[e],{"ev1"})
        self.assertEqual(result["admissible_ids"],[])
        self.assertIn("producer identity not verified",result["rejected"]["ev1"])
    def test_document_only_cannot_establish_behavior(self):
        e=self.evidence(method="ARCHITECTURE_CONTRACT")
        result=policy.assess_admissibility("ZTA-02.01",[e],{"ev1"})
        self.assertEqual(result["admissible_ids"],[])
        self.assertIn("behavioral control requires behavioral proof",result["rejected"]["ev1"])
    def test_valid_candidate_requires_review(self):
        e=self.evidence()
        result=policy.assess_admissibility("ZTA-02.01",[e],{"ev1"})
        self.assertEqual(result["admissible_ids"],["ev1"])
        self.assertEqual(result["decision"],"REVIEW_REQUIRED")
    def test_unchecked_digest_is_not_admissible(self):
        result=policy.assess_admissibility("ZTA-02.01",[self.evidence()],set())
        self.assertEqual(result["admissible_ids"],[])
    def test_stale_future_and_boundaries(self):
        e=self.evidence()
        e["collected_at"]="2026-10-27T00:00:00Z"
        now="2026-10-27T00:00:11Z"
        self.assertIn("evidence too old",policy.assess_admissibility(
            "ZTA-02.01",[e],{"ev1"},as_of=now,max_age_seconds=10)["rejected"]["ev1"])
        self.assertEqual(policy.assess_admissibility(
            "ZTA-02.01",[e],{"ev1"},as_of=now,max_age_seconds=11)["admissible_ids"],["ev1"])
        self.assertIn("observation is in the future",policy.assess_admissibility(
            "ZTA-02.01",[e],{"ev1"},as_of="2026-10-26T23:59:59Z",max_age_seconds=100)["rejected"]["ev1"])
    def test_freshness_arguments_must_be_complete(self):
        with self.assertRaises(ValueError):
            policy.assess_admissibility("ZTA-02.01",[],set(),as_of="2026-10-27T00:00:00Z")
    def test_unrelated_control_is_not_admitted(self):
        result=policy.assess_admissibility("ZTA-08.01",[self.evidence()],{"ev1"})
        self.assertEqual(result["admissible_ids"],[])

if __name__=="__main__":
    unittest.main()
