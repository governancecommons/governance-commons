"""Adversarial tests for the GC-AUDIT operation allowlist."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import os
import subprocess

MODULE = Path(__file__).resolve().parents[1] / "tools" / "validate_operation_registry.py"
spec = importlib.util.spec_from_file_location("gc_registry_validator", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BASE = """schema: gc-audit.registry.v1
authority: DEV-ACCORD.05
updated: '2026-07-01'
description: test
security:
  execution_model: allowlist
  shell: forbidden
  path_policy: scripts must resolve under the portfolio root
  mutation_policy: test
  owner: GC-AUDIT
  evidenceBundles: {}
  contracts: {}
  playValidationProfiles: {}
  internalScripts: []
categories:
  repo-health: {label: Health, description: test}
  repo-repair: {label: Repair, description: test}
tools:
  - id: gc-audit.validate
    verb: validate
    category: repo-health
    status: active
    mutates: false
    steps:
      - script: governance-commons/gc-audit/tools/validate-check.ps1
  - id: gc-audit.normalize
    verb: normalize
    category: repo-repair
    status: active
    mutates: true
    requiresExplicitApply: true
    steps:
      - script: governance-commons/gc-audit/tools/normalize-check.ps1
  - id: gc-audit.future
    verb: future
    category: repo-health
    status: planned
    mutates: false
    steps: []
  - id: gc-audit.registry
    verb: registry
    category: repo-health
    status: active
    mutates: false
    zeroTrust:
      failClosed: true
      networkRegistryFetch: forbidden
      pathContainment: portfolio-root-for-registry-paths
      schemaInference: forbidden
      explicitAuthorizationRequired: [normalization-apply, schema-authority-change, git-branch-or-remote-split]
    steps:
      - script: governance-commons/gc-audit/tools/validate-registry.ps1
  - id: gc-audit.zerotrust
    verb: zerotrust
    category: repo-health
    status: active
    mutates: false
    zeroTrust: {selfApplying: true}
    steps:
      - script: governance-commons/gc-audit/tools/validate-zero-trust.ps1
docs: {}
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
        (tools / "validate-registry.ps1").write_text("param()", encoding="utf-8")
        (tools / "validate-zero-trust.ps1").write_text("param()", encoding="utf-8")
        self.text = BASE

    def check(self):
        return mod.validate_registry(self.text, self.portfolio,
            self.portfolio / "governance-commons")

    def test_valid(self):
        self.assertEqual(self.check()["status"], "REGISTRY_CONTRACT_VALID")
        self.assertEqual(self.check()["self_audit_readiness"], "READY")
        self.assertEqual(self.check()["runtime_security_assurance"], "UNVERIFIED")

    def test_duplicate_yaml_key(self):
        self.text += "\nschema: gc-audit.registry.v1\n"
        with self.assertRaises(mod.RegistryError): self.check()

    def test_malformed_yaml(self):
        self.text += "\n  bad: [\n"
        with self.assertRaises(mod.RegistryError): self.check()

    def test_missing_authority(self):
        self.text = self.text.replace("authority: DEV-ACCORD.05", "authority: attacker")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_unknown_operation_field_or_alias(self):
        self.text = self.text.replace("id: gc-audit.validate", "id: gc-audit.validate\n    aliases: [gc-audit.normalize]", 1)
        with self.assertRaises(mod.RegistryError): self.check()

    def test_unknown_step_metadata(self):
        self.text = self.text.replace("validate-check.ps1", "validate-check.ps1\n        command: pwsh -File evil.ps1", 1)
        with self.assertRaises(mod.RegistryError): self.check()

    def test_unknown_category(self):
        self.text = self.text.replace("category: repo-health\n    status: active",
                                      "category: attacker\n    status: active", 1)
        with self.assertRaisesRegex(mod.RegistryError, "unknown operation verb/category"):
            self.check()

    def test_malformed_operation_id(self):
        self.text = self.text.replace("gc-audit.validate", "gc-audit.validate/../evil", 1)
        with self.assertRaises(mod.RegistryError): self.check()

    def test_inconsistent_apply_metadata(self):
        self.text = self.text.replace("mutates: false", "mutates: false\n    requiresExplicitApply: true", 1)
        with self.assertRaises(mod.RegistryError): self.check()

    def test_missing_self_audit_operation(self):
        self.text = self.text[:self.text.index("  - id: gc-audit.zerotrust")] + "docs: {}\n"
        self.assertEqual(self.check()["self_audit_readiness"], "UNAVAILABLE")
        with self.assertRaisesRegex(mod.RegistryError, "required self-audit assurance unavailable"):
            mod.validate_registry(self.text, self.portfolio,
                self.portfolio / "governance-commons", require_self_audit=True)

    def test_advisory_operation_without_self_audit_is_structurally_valid(self):
        self.text = self.text[:self.text.index("  - id: gc-audit.registry")] + "docs: {}\n"
        result = self.check()
        self.assertEqual(result["status"], "REGISTRY_CONTRACT_VALID")
        self.assertEqual(result["self_audit_readiness"], "UNAVAILABLE")

    def test_planned_self_audit_cannot_claim_active_assurance(self):
        self.text = self.text.replace("status: active\n    mutates: false\n    zeroTrust: {selfApplying: true}\n    steps:\n      - script: governance-commons/gc-audit/tools/validate-zero-trust.ps1",
            "status: planned\n    mutates: false\n    zeroTrust: {selfApplying: true}\n    steps: []")
        with self.assertRaisesRegex(mod.RegistryError, "planned self-audit claims"):
            self.check()

    def test_missing_authorization_claim(self):
        self.text = self.text.replace("schema-authority-change, ", "")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_redirected_self_audit(self):
        self.text = self.text.replace("validate-zero-trust.ps1", "validate-check.ps1")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_unsafe_argument_mapping(self):
        self.text = self.text.replace("validate-check.ps1", "validate-check.ps1\n        targetArg: '-Command evil'", 1)
        with self.assertRaises(mod.RegistryError): self.check()

    def test_duplicate_operation(self):
        self.text = self.text.replace("docs: {}", """
  - id: gc-audit.validate
    verb: validate
    category: repo-health
    status: active
    mutates: false
    steps:
      - script: governance-commons/gc-audit/tools/validate-check.ps1
docs: {}""")
        with self.assertRaisesRegex(mod.RegistryError, "duplicate or malformed operation ID"):
            self.check()

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

    def test_unc_windows_path(self):
        self.text = self.text.replace("governance-commons/gc-audit/tools/validate-check.ps1", r"\\server\share\evil.ps1")
        with self.assertRaises(mod.RegistryError): self.check()

    def test_file_uri(self):
        self.text = self.text.replace("governance-commons/gc-audit/tools/validate-check.ps1", "file:///tmp/evil.ps1")
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
      internal: true
      reason: internal fixture""")
        with self.assertRaisesRegex(mod.RegistryError, "internal helper exposed as operation"):
            self.check()

    def test_planned_self_audit_is_structural_only(self):
        self.text = self.text.replace("status: active\n    mutates: false\n    zeroTrust: {selfApplying: true}\n    steps:\n      - script: governance-commons/gc-audit/tools/validate-zero-trust.ps1",
            "status: planned\n    mutates: false\n    steps: []")
        self.assertEqual(self.check()["self_audit_readiness"], "UNAVAILABLE")
        with self.assertRaisesRegex(mod.RegistryError, "required self-audit assurance unavailable"):
            mod.validate_registry(self.text, self.portfolio,
                self.portfolio / "governance-commons", require_self_audit=True)

    def test_active_self_audit_requires_zero_trust(self):
        self.text = self.text.replace("    zeroTrust: {selfApplying: true}\n", "")
        with self.assertRaisesRegex(mod.RegistryError, "active self-audit lacks zero-trust"):
            self.check()

    def test_empty_active_self_audit_rejected(self):
        self.text = self.text.replace(
            "steps:\n      - script: governance-commons/gc-audit/tools/validate-zero-trust.ps1",
            "steps: []")
        with self.assertRaisesRegex(mod.RegistryError, "empty active operation"):
            self.check()

    def test_runtime_assurance_requires_trusted_host(self):
        with self.assertRaisesRegex(mod.RegistryError, "trusted-host enforcement"):
            mod.validate_registry(self.text, self.portfolio,
                self.portfolio / "governance-commons", require_runtime_assurance=True)

    def test_read_only_write_command_is_flagged(self):
        p = self.portfolio / "governance-commons/gc-audit/tools/validate-check.ps1"
        p.write_text("'bad' | Set-Content -LiteralPath out.txt", encoding="utf-8")
        self.assertIn("validate-check.ps1", self.check()["read_only_write_scripts"])

    def test_computed_shell_invocation_is_flagged(self):
        p = self.portfolio / "governance-commons/gc-audit/tools/validate-check.ps1"
        p.write_text("& (Get-Command pwsh) -Command 'echo bad'", encoding="utf-8")
        self.assertIn("validate-check.ps1", self.check()["indirect_delegation_scripts"])

    def test_repository_ancestor_symlink_escape(self):
        outside = Path(self.temp.name).parent / (Path(self.temp.name).name + "-outside")
        outside.mkdir()
        self.addCleanup(lambda: outside.rmdir())
        repo = self.portfolio / "governance-commons"
        tools = repo / "gc-audit/tools"
        for item in tools.iterdir():
            item.unlink()
        tools.rmdir()
        (repo / "gc-audit").rmdir()
        repo.rmdir()
        try:
            repo.symlink_to(outside, target_is_directory=True)
        except (NotImplementedError, OSError):
            self.skipTest("directory symlink unavailable")
        with self.assertRaisesRegex(mod.RegistryError, "escapes containment root"):
            self.check()

    @unittest.skipUnless(os.name == "nt", "Windows junction fixture only")
    def test_repository_ancestor_junction_escape(self):
        outside = Path(self.temp.name).parent / (Path(self.temp.name).name + "-junction-outside")
        outside.mkdir()
        self.addCleanup(lambda: outside.rmdir())
        repo = self.portfolio / "governance-commons"
        tools = repo / "gc-audit/tools"
        for item in tools.iterdir():
            item.unlink()
        tools.rmdir()
        (repo / "gc-audit").rmdir()
        repo.rmdir()
        env = dict(os.environ, GC_TEST_LINK=str(repo), GC_TEST_TARGET=str(outside))
        result = subprocess.run(["powershell", "-NoProfile", "-Command",
            "New-Item -ItemType Junction -Path $env:GC_TEST_LINK -Target $env:GC_TEST_TARGET | Out-Null"],
            capture_output=True, text=True, env=env)
        if result.returncode:
            self.skipTest("Windows junction unavailable: " + result.stderr.strip())
        with self.assertRaisesRegex(mod.RegistryError, "escapes containment root"):
            self.check()

if __name__ == "__main__":
    unittest.main()
