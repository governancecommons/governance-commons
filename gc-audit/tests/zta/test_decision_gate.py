"""ZTA control decision gate adversarial regression tests."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from zta_decision_gate import classify_control, DecisionGateError

class DecisionGateTests(unittest.TestCase):
    def assess(self, **kwargs):
        return classify_control(control_id="ZTA-08.02", mandatory=False, **kwargs)
    def test_complete_positive_package_still_unverified(self):
        x=self.assess(proof_coverage={"status":"PROOF_PACKAGE_COMPLETE"})
        self.assertEqual(x["status"],"UNVERIFIED")
    def test_signed_scope_review_still_unverified(self):
        x=self.assess(applicability={"status":"ABSENCE_CANDIDATE"},
                      scope_review={"status":"SIGNED_SCOPE_REVIEW"})
        self.assertEqual(x["status"],"UNVERIFIED")
    def test_failure_overrides_signed_positive_and_scope_review(self):
        x=self.assess(negative_evidence_ids=["e2","e1","e2"],
                      proof_coverage={"status":"PROOF_PACKAGE_COMPLETE"},
                      applicability={"status":"ABSENCE_CANDIDATE"},
                      scope_review={"status":"SIGNED_SCOPE_REVIEW"})
        self.assertEqual(x["status"],"FAIL")
        self.assertEqual(x["evidence_ids"],["e1","e2"])
    def test_presence_conflicts_with_scope_approval(self):
        with self.assertRaises(DecisionGateError):
            self.assess(applicability={"status":"APPLICABLE"},
                        scope_review={"status":"SIGNED_SCOPE_REVIEW"})
    def test_mandatory_control_not_excludable(self):
        with self.assertRaises(DecisionGateError):
            classify_control(control_id="ZTA-08.02",mandatory=True,
                             applicability={"status":"ABSENCE_CANDIDATE"},
                             scope_review={"status":"SIGNED_SCOPE_REVIEW"})
    def test_unsigned_absence_is_unverified(self):
        self.assertEqual(self.assess(applicability={"status":"ABSENCE_CANDIDATE"})["status"],
                         "UNVERIFIED")
    def test_negative_package_claim_is_not_automatically_verified_failure(self):
        self.assertEqual(self.assess(proof_coverage={"status":"NEGATIVE_REVIEW_REQUIRED"})["status"],
                         "UNVERIFIED")
    def test_unsupported_result_rejected(self):
        with self.assertRaises(DecisionGateError):
            self.assess(proof_coverage={"status":"PASS"})
    def test_delegated_host_claim_cannot_pass(self):
        result = classify_control(control_id="ZTA-06.02", mandatory=True,
            proof_coverage={"status":"PROOF_PACKAGE_COMPLETE"})
        self.assertEqual(result["status"], "UNVERIFIED")
    def test_verified_host_failure_overrides_positive_claim(self):
        result = classify_control(control_id="ZTA-06.02", mandatory=True,
            negative_evidence_ids=["host-bypass"],
            proof_coverage={"status":"PROOF_PACKAGE_COMPLETE"})
        self.assertEqual(result["status"], "FAIL")
if __name__=="__main__":
    unittest.main()
