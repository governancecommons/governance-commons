"""Adversarial tests for the GC-AUDIT operation allowlist."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "tools" / "validate_operation_registry.py"
spec = importlib.util.spec_from_file_location("gc_registry_validator", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BASE = """schema: gc-audit.registry.v1
security:
  execution_model: allowlist
  shell: forbidden
  internalScripts: []
tools:
  - id: gc-audit.validate
    status: active
    mutates: false
    steps:
      - script: governance-commons/gc-audit/tools/validate-check.ps1
  - id: gc-audit.normalize
    status: active
    mutates: true
    requiresExplicitApply: true
    steps:
      - script: governance-commons/gc-audit/tools/normalize-check.ps1
  - id: gc-audit.future
    status: planned
    mutates: false
    steps: []
"""

class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.portfolio = Path(self.temp.name)
        tools = self.portfolio / "governance-commons" / "gc-audit" / "tools"
        tools.mkdir(parents=True)
        (tools / "validate-check.ps1").write_text("param([string] $Root)", encoding="utf-8")
        (tools / "normalize-check.ps1").write_text(
            "param([switch] $Apply, [switch] $DryRun)\nif ($Apply) { 'change' }",
            encoding="utf-8")
        self.text = BASE

    def check(self):
        return mod.validate_registry(self.text, self.portfolio)

    def test_valid(self):
        self.assertEqual(self.check()["status"], "REGISTRY_CONTRACT_VALID")

    def test_duplicate_yaml_key(self):
        self.text += "\nschema: gc-audit.registry.v1\n"
        with self.assertRaises(mod.RegistryError): self.check()

    def test_duplicate_operation(self):
        self.text += """
  - id: gc-audit.validate
    status: active
    mutates: false
    steps:
      - script: governance-commons/gc-audit/tools/validate-check.ps1
"""
        with self.assertRaises(mod.RegistryError): self.check()

    def test_traversal(self):
        self.text = self.text.replace("validate-check.ps1", "../../evil.ps1")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_absolute_windows_path(self):
        self.text = self.text.replace(
            "governance-commons/gc-audit/tools/validate-check.ps1", "C:\\temp\\evil.ps1")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_network_url(self):
        self.text = self.text.replace(
            "governance-commons/gc-audit/tools/validate-check.ps1", "https://bad.example/x.ps1")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_prefix_collision(self):
        self.text = self.text.replace(
            "governance-commons/gc-audit/tools/validate-check.ps1",
            "governance-commons-evil/gc-audit/tools/validate-check.ps1")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_symlink_escape(self):
        external = self.portfolio / "outside.ps1"
        external.write_text("'bad'", encoding="utf-8")
        link = self.portfolio / "governance-commons" / "gc-audit" / "tools" / "validate-check.ps1"
        link.unlink()
        try:
            link.symlink_to(external)
        except (NotImplementedError, OSError):
            self.skipTest("symlink unavailable")
        # Points outside the repository, even though inside the portfolio; tighten
        # containment by an explicit script path prefix check in the validator.
        with self.assertRaises(mod.RegistryError): self.check()

    def test_mutating_validator(self):
        p = self.portfolio / "governance-commons" / "gc-audit" / "tools" / "validate-check.ps1"
        p.write_text("param([switch] $FixNotes)", encoding="utf-8")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_normalizer_missing_apply(self):
        p = self.portfolio / "governance-commons" / "gc-audit" / "tools" / "normalize-check.ps1"
        p.write_text("param([switch] $DryRun)", encoding="utf-8")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_indirect_process_invocation_requires_review(self):
        p = self.portfolio / "governance-commons" / "gc-audit" / "tools" / "validate-check.ps1"
        p.write_text("return & $PowerShellHost @args 2>&1", encoding="utf-8")
        result = self.check()
        self.assertEqual(result["delegation_review"], "REQUIRED")
        self.assertIn("validate-check.ps1", result["indirect_delegation_scripts"])

    def test_direct_shell_spawn_rejected(self):
        p = self.portfolio / "governance-commons" / "gc-audit" / "tools" / "validate-check.ps1"
        p.write_text("Start-Process pwsh -ArgumentList '-c echo bad'", encoding="utf-8")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_expression_evaluation_rejected(self):
        p = self.portfolio / "governance-commons" / "gc-audit" / "tools" / "validate-check.ps1"
        p.write_text("Invoke-Expression $command", encoding="utf-8")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_planned_operation_executable(self):
        self.text = self.text.replace(
            "status: planned\n    mutates: false\n    steps: []",
            "status: planned\n    mutates: false\n    steps:\n      - script: governance-commons/gc-audit/tools/validate-check.ps1")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_unregistered_internal_exemption(self):
        self.text = self.text.replace("internalScripts: []", """internalScripts:
    - script: governance-commons/gc-audit/tools/validate-check.ps1
      internal: true""")
        with self.assertRaises(mod.RegistryError): self.check()

if __name__ == "__main__":
    unittest.main()
