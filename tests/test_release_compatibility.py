"""Release checks reject unsupported compatibility rather than inventing it."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

from scripts.validate_release import check_compatibility, validate_release


class ReleaseCompatibilityTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {
            "release_id": "GC-v1.3.0",
            "compat_hold_items": [],
            "specs": [
                {
                    "spec": name,
                    "min_version": pin,
                    "pinned_version": pin,
                    "compat_status": "ok",
                }
                for name, pin in [
                    ("agent-dossier", "1.0.2"),
                    ("agent-matrix", "1.4.0"),
                    ("ons", "1.3.0"),
                ]
            ],
        }
        self.matrix = {
            "versioning": {
                "normative_compatibility": [
                    {
                        "matrix_version": "1.4.0",
                        "dossier_specification_alignment": "1.0.2",
                        "status": "supported",
                    }
                ],
                "tested_runtimes": [{"min_orchestrator_version": "999.0.0"}],
            }
        }

    def test_supported_row_passes_despite_runtime_version(self):
        self.assertEqual(check_compatibility(self.manifest, self.matrix), [])

    def test_alignment_disagreement_requires_evidence(self):
        self.manifest["specs"][0]["pinned_version"] = "1.1.0"
        self.assertTrue(
            any(
                "declared alignment" in e
                for e in check_compatibility(self.manifest, self.matrix)
            )
        )

    def test_duplicate_row_fails(self):
        self.matrix["versioning"]["normative_compatibility"] *= 2
        self.assertTrue(check_compatibility(self.manifest, self.matrix))

    def test_duplicate_spec_fails(self):
        self.manifest["specs"].append(deepcopy(self.manifest["specs"][0]))
        self.assertTrue(check_compatibility(self.manifest, self.matrix))

    def test_hold_fails(self):
        self.manifest["compat_hold_items"] = ["consumer confirmation pending"]
        self.assertTrue(check_compatibility(self.manifest, self.matrix))

    def test_runtime_cannot_enter_new_specification_release(self):
        self.manifest["specs"].append({"spec": "agent-project-orchestrator"})
        self.assertTrue(check_compatibility(self.manifest, self.matrix))

    def test_legacy_runtime_pin_does_not_decide_compatibility(self):
        self.manifest["release_id"] = "GC-v1.2.0"
        self.manifest["specs"].append(
            {"spec": "agent-project-orchestrator", "pinned_version": "0.0.0"}
        )
        self.assertEqual(check_compatibility(self.manifest, self.matrix), [])

    def test_unreleased_or_missing_row_fails(self):
        self.manifest["specs"][1]["pinned_version"] = "9.0.0"
        self.assertTrue(check_compatibility(self.manifest, self.matrix))

    def test_deprecated_row_fails(self):
        self.matrix["versioning"]["normative_compatibility"][0]["status"] = "deprecated"
        self.assertTrue(check_compatibility(self.manifest, self.matrix))

    def test_unpinned_manifest_cannot_claim_verified_compatibility(self):
        del self.manifest["specs"][0]["pinned_version"]
        self.assertTrue(check_compatibility(self.manifest, self.matrix))


class GitEvidenceTests(unittest.TestCase):
    def setUp(self):
        ReleaseCompatibilityTests.setUp(self)
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.matrix["versioning"]["normative_compatibility"][0][
            "min_dossier_schema_version"
        ] = "1.0.0"
        self.manifest.update(
            gc_schema_version="1.0.0",
            gc_version="1.3.0",
            declared_at="2026-10-07T00:00:00Z",
            declared_by="test",
            status="planned",
        )
        for pin in self.manifest["specs"]:
            pin["repo"] = f"governancecommons/{pin['spec']}"
            repo = self.root / pin["spec"]
            repo.mkdir()
            self.command(repo, "init")
            self.command(repo, "config", "user.email", "test@example.invalid")
            self.command(repo, "config", "user.name", "Test")
            if pin["spec"] == "agent-matrix":
                (repo / "agent-matrix.yaml").write_text(
                    yaml.safe_dump(self.matrix), encoding="utf-8"
                )
            elif pin["spec"] == "agent-dossier":
                (repo / "schemas").mkdir()
                (repo / "schemas/agent-dossier-instance.schema.json").write_text(
                    json.dumps({"$id": "https://example.invalid/v/1.0.0/schema.json"}),
                    encoding="utf-8",
                )
            else:
                (repo / "README.md").write_text("Test ONS artifact", encoding="utf-8")
            self.command(repo, "add", ".")
            self.command(repo, "commit", "-m", "fixture")
            self.command(repo, "tag", f"v{pin['pinned_version']}")
        self.manifest_path = self.root / "manifest.yaml"
        self.manifest_path.write_text(yaml.safe_dump(self.manifest), encoding="utf-8")

    def command(self, repo, *args):
        return subprocess.check_output(
            ["git", "-C", str(repo), *args], stderr=subprocess.PIPE
        )

    def test_committed_component_artifacts_pass(self):
        report = validate_release(self.manifest_path, self.root, "HEAD")
        self.assertEqual(report["errors"], [])
        self.assertEqual(len(report["evidence"]["agent-dossier"]["commit"]), 40)

    def test_unrelated_working_tree_does_not_become_evidence(self):
        (self.root / "agent-matrix/agent-matrix.yaml").write_text(
            "invalid working tree", encoding="utf-8"
        )
        self.assertTrue(
            validate_release(self.manifest_path, self.root, "HEAD")["passed"]
        )

    def test_missing_release_tag_fails(self):
        self.command(self.root / "ons", "tag", "-d", "v1.3.0")
        report = validate_release(self.manifest_path, self.root, "HEAD")
        self.assertFalse(report["passed"])
        self.assertTrue(any("evidence unavailable" in e for e in report["errors"]))

    def test_manifest_schema_failure_is_reported(self):
        self.manifest["unexpected_field"] = True
        self.manifest_path.write_text(yaml.safe_dump(self.manifest), encoding="utf-8")
        report = validate_release(self.manifest_path, self.root, "HEAD")
        self.assertFalse(report["passed"])
        self.assertTrue(any("manifest schema" in e for e in report["errors"]))


if __name__ == "__main__":
    unittest.main()
