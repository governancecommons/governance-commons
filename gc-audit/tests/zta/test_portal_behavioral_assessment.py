"""Portable report integrity and authority boundary checks."""
import copy
import json
from pathlib import Path
import sys
import unittest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
from portal_behavioral_assessment import verify_pilot, sha256
from zta_evaluator import AssessmentInputError, digest

REPORT = HERE.parents[1] / "reports" / "portal-application-zta-pilot.json"


class PortalBehavioralReportTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads(REPORT.read_text(encoding="utf-8"))

    def test_export_reopens_without_portal_checkout(self):
        verify_pilot(self.report)
        self.assertEqual(len(self.report["application_pilot"]["observations"]), 11)
        self.assertEqual({r["status"] for r in self.report["result"]["control_results"]}, {"UNVERIFIED"})

    def test_forged_pass_with_recomputed_outer_digest_is_rejected(self):
        forged = copy.deepcopy(self.report)
        forged["result"]["control_results"][0]["status"] = "PASS"
        forged["report_digest"] = digest({k: v for k, v in forged.items() if k != "report_digest"})
        with self.assertRaises(AssessmentInputError):
            verify_pilot(forged)

    def test_observation_tamper_is_rejected(self):
        changed = copy.deepcopy(self.report)
        changed["application_pilot"]["observations"][0]["observed"] = 200
        changed["report_digest"] = digest({k: v for k, v in changed.items() if k != "report_digest"})
        with self.assertRaises(AssessmentInputError):
            verify_pilot(changed)

    def test_probe_text_digest_is_line_ending_stable(self):
        self.assertEqual(sha256(b"first\nsecond\n"), sha256(b"first\r\nsecond\r\n"))


if __name__ == "__main__":
    unittest.main()
