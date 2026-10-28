"""Real local Git and hostile report checks for the standalone pilot."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import zta_cli as cli
from zta_evaluator import AssessmentInputError, digest


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "external"
        self.root.mkdir()
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        (self.root / "README.md").write_text("pilot\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(self.root), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(self.root), "-c", "user.name=Test",
                        "-c", "user.email=test@example.invalid", "commit", "-qm", "initial"], check=True)

    def test_deterministic_read_only_export_and_reopen(self):
        before = cli.git(self.root, "status", "--porcelain=v1", "--untracked-files=all")
        first = cli.make_report(self.root, "external")
        self.assertEqual(first, cli.make_report(self.root, "external"))
        self.assertEqual(first["result"]["release_eligibility"], "BLOCKED")
        self.assertEqual({r["status"] for r in first["result"]["control_results"]}, {"UNVERIFIED"})
        exported = Path(self.temp.name) / "report.json"
        exported.write_bytes(cli.canonical(first) + b"\n")
        cli.verify(json.loads(exported.read_text(encoding="utf-8")), self.root)
        self.assertEqual(before, cli.git(self.root, "status", "--porcelain=v1", "--untracked-files=all"))

    def test_forged_pass_and_tamper_rejected(self):
        report = cli.make_report(self.root, "external")
        forged = copy.deepcopy(report)
        forged["result"]["control_results"][0]["status"] = "PASS"
        forged["report_digest"] = digest({k: v for k, v in forged.items() if k != "report_digest"})
        with self.assertRaisesRegex(AssessmentInputError, "evaluator result mismatch"):
            cli.verify(forged)
        changed = copy.deepcopy(report)
        changed["manifest"]["entries"][0]["git_blob_oid"] = "0" * 40
        with self.assertRaisesRegex(AssessmentInputError, "report digest mismatch"):
            cli.verify(changed)

    def test_dirty_target_and_unsupported_profile_fail_closed(self):
        (self.root / "new.txt").write_text("untracked", encoding="utf-8")
        with self.assertRaisesRegex(AssessmentInputError, "not clean"):
            cli.make_report(self.root, "external")
        self.assertEqual(cli.main(["assess", "--target", str(self.root), "--target-id", "external",
                                   "--profile", cli.PROFILE, "--authorize-local-read",
                                   "--output", str(self.root / "report.json")]), 2)
        with self.assertRaises(SystemExit):
            cli.main(["assess", "--target", str(self.root), "--target-id", "external",
                      "--profile", "zta.service.v1", "--authorize-local-read",
                      "--output", str(Path(self.temp.name) / "report.json")])


if __name__ == "__main__":
    unittest.main()
