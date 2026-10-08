"""Release checks reject unsupported compatibility rather than inventing it."""

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml
from jsonschema import Draft202012Validator

from scripts.validate_release import ROOT, check_compatibility, validate_release


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
                    ("agent-dossier", "1.1.0"),
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
                        "dossier_specification_alignment": "1.1.0",
                        "status": "supported",
                    }
                ],
                "tested_runtimes": [{"min_orchestrator_version": "999.0.0"}],
            }
        }

    def test_supported_row_passes_despite_runtime_version(self):
        self.assertEqual(check_compatibility(self.manifest, self.matrix), [])

    def test_alignment_disagreement_requires_evidence(self):
        self.manifest["specs"][0]["pinned_version"] = "1.0.2"
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


class ManifestReadinessTests(unittest.TestCase):
    def setUp(self):
        schema_path = ROOT / "schemas/gc-release-manifest.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.validator = Draft202012Validator(schema)
        self.manifest = yaml.safe_load(
            (ROOT / "releases/gc-v1.2.0.yaml").read_text(encoding="utf-8")
        )

    def ready_candidate(self):
        candidate = deepcopy(self.manifest)
        candidate["status"] = "ready"
        candidate["compat_hold_items"] = []
        candidate.pop("historical_gate_review")
        for pin in candidate["specs"]:
            pin["compat_status"] = "ok"
        return candidate

    def test_planned_compatible_manifest_is_structurally_valid(self):
        self.assertEqual(list(self.validator.iter_errors(self.manifest)), [])
        self.assertEqual(self.manifest["status"], "planned")
        self.assertEqual(self.manifest["compat_hold_items"], [])
        compatibility = {
            pin["spec"]: pin["compat_status"] for pin in self.manifest["specs"]
        }
        self.assertEqual(compatibility["agent-dossier"], "ok")
        self.assertEqual(compatibility["agent-matrix"], "ok")
        self.assertEqual(self.manifest["ready_at"], "2026-06-17T00:00:00Z")
        self.assertNotIn("gc_pass_id", self.manifest)
        self.assertEqual(
            self.manifest["historical_gate_review"]["citation"], "GC-PASS-0015.00"
        )
        self.assertEqual(
            self.manifest["historical_gate_review"]["resolution"], "clarified"
        )

    def test_changing_status_alone_cannot_restore_readiness(self):
        self.manifest["status"] = "ready"
        self.assertTrue(list(self.validator.iter_errors(self.manifest)))

    def test_ready_requires_current_release_review_not_historical_gate(self):
        candidate = self.ready_candidate()
        candidate["historical_gate_review"] = self.manifest["historical_gate_review"]
        self.assertTrue(list(self.validator.iter_errors(candidate)))

    def test_ambiguous_historical_citation_remains_legacy_valid(self):
        candidate = deepcopy(self.manifest)
        candidate["historical_gate_review"]["resolution"] = "ambiguous"
        self.assertEqual(list(self.validator.iter_errors(candidate)), [])

    def test_ready_requires_pinned_versions(self):
        candidate = self.ready_candidate()
        del candidate["specs"][0]["pinned_version"]
        self.assertTrue(list(self.validator.iter_errors(candidate)))

    def test_ready_requires_ok_component_compatibility(self):
        candidate = self.ready_candidate()
        candidate["specs"][0]["compat_status"] = "compat-hold"
        self.assertTrue(list(self.validator.iter_errors(candidate)))

    def test_ready_requires_explicit_empty_hold_list(self):
        candidate = self.ready_candidate()
        del candidate["compat_hold_items"]
        self.assertTrue(list(self.validator.iter_errors(candidate)))

    def test_resolved_candidate_meets_only_structural_requirements(self):
        self.assertEqual(list(self.validator.iter_errors(self.ready_candidate())), [])


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
