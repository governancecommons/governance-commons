import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from zta_evaluator import evaluate, AssessmentInputError
from test_evaluator import records

class ScopeIntegrationTests(unittest.TestCase):
    def test_requires_external_policy(self):
        c,p,t = records()
        with self.assertRaises(AssessmentInputError):
            evaluate(c,p,t,scope_approvals=[{"payload":{"control_id":"ZTA-06.02"}}])

    def test_unscreened_control_fails_closed(self):
        c,p,t = records()
        policy={"capabilities":{},"required_scopes":{},
                "verified_observations":{},"authorized_approvers":{}}
        with self.assertRaises(AssessmentInputError):
            evaluate(c,p,t,applicability_observations={},applicability_policy=policy,
                scope_approvals=[{"payload":{"control_id":"ZTA-06.02"}}])

if __name__ == "__main__":
    unittest.main()
