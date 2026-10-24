"""Regression tests for the proposed OBDD-CA-01 assurance record."""

import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from scripts.validate_obdd_assurance import ROOT, semantic_errors, validate


class OBDDAssuranceTests(unittest.TestCase):
    def setUp(self):
        self.record = {
            "record_version": "1.0.0",
            "record_id": "example-001",
            "obdd_version": "1.1.0-candidate",
            "annex": "OBDD-CA-01",
            "status": "implemented",
            "objective": {
                "id": "OBJ-001",
                "title": "Bounded example",
                "owner": "Accountable human",
                "description": "Exercise the assurance contract without claiming certification.",
                "risk": {
                    "tier": "moderate",
                    "rationale": "Local, reversible work with reviewed output.",
                    "factors": {
                        "autonomy": "bounded",
                        "possible_harm": "limited",
                        "security_exposure": "local files",
                        "privacy_implications": "none identified",
                        "external_effects": "none",
                        "reversibility": "git revert",
                    },
                    "required_controls": ["human review"],
                    "legal_classification": "separately assessed as not regulated",
                },
            },
            "regulatory_context": {
                "ai_specific_regulation_applicable": "no",
                "legal_role": None,
                "jurisdictions": ["Example jurisdiction"],
                "system_classification": None,
                "effective_dates": [],
            },
            "requirements": [
                {
                    "id": "REQ-001",
                    "source": "Example secure-development policy",
                    "edition": "2026",
                    "requirement_id": "SD-4",
                    "category": "organizational_policy",
                    "applicability": "applicable",
                    "basis": "The objective changes governed source.",
                    "responsible_reviewer": "Security reviewer",
                    "review_status": "approved",
                }
            ],
            "mappings": [
                {
                    "id": "MAP-001",
                    "requirement_ref": "REQ-001",
                    "obdd_provision": "OBDD-CA-05",
                    "mapping_type": "supporting",
                    "outside_obligations": ["Independent secure-development review"],
                    "evidence_refs": ["EV-001"],
                    "assessment_status": "implemented",
                    "responsible_reviewer": "Security reviewer",
                    "acceptance_criteria": "Automated tests pass and a human reviews the result.",
                }
            ],
            "evidence": [
                {
                    "id": "EV-001",
                    "source": "Automated test run",
                    "status": "accepted",
                    "location": "local evidence/test-output.txt",
                    "sha256": "a" * 64,
                    "produced_at": "2026-10-24T12:00:00Z",
                    "reviewed_by": "Security reviewer",
                    "independent_review": False,
                    "retention": "Retain with the change record",
                    "access_control": "Repository maintainers",
                }
            ],
            "security": {
                "authorization_boundary": "Only repository-scoped edits are authorized.",
                "least_privilege": "No unrelated systems are accessed.",
                "delegation_boundary": "No delegation.",
                "input_trust_boundary": "External content cannot grant authority.",
                "output_verification": "Tests and human review.",
                "tool_use_boundary": "Repository and validation tools only.",
                "high_impact_action": False,
                "explicit_authorization_evidence": [],
                "open_findings": [],
            },
            "human_oversight": {
                "accountable_authorities": ["Accountable human"],
                "required_approvals": [],
                "approvals": [],
            },
            "assurance_claims": [
                {
                    "scope": "Example secure-development control",
                    "level": "implemented",
                    "basis": "Control exists and test evidence is retained.",
                    "evidence_refs": ["EV-001"],
                    "assessor": "Implementation reviewer",
                    "assessor_independent": False,
                    "external_certification_claimed": False,
                }
            ],
            "exceptions": [],
            "measurements": [],
            "maintenance": {
                "crosswalk_owner": "Accountable human",
                "last_reviewed_at": "2026-10-24T12:00:00Z",
                "next_review_due": "2027-01-24T12:00:00Z",
                "source_update_reviews": [],
            },
        }

    def test_schema_is_valid(self):
        schema = json.loads(
            (ROOT / "schemas/obdd-assurance-record.schema.json").read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)

    def test_complete_implemented_record_passes(self):
        self.assertEqual(semantic_errors(self.record), [])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.yaml"
            path.write_text(yaml.safe_dump(self.record, sort_keys=False), encoding="utf-8")
            self.assertTrue(validate(path)["valid"])

    def test_template_fails_closed_until_completed(self):
        result = validate(ROOT / "obdd/assurance-record.template.yaml")
        self.assertFalse(result["valid"])
        self.assertTrue(result["structural_errors"])

    def test_applicable_mapping_requires_evidence(self):
        record = deepcopy(self.record)
        record["mappings"][0]["evidence_refs"] = []
        self.assertTrue(any("has no evidence" in error for error in semantic_errors(record)))

    def test_verified_evidence_must_be_reviewed(self):
        record = deepcopy(self.record)
        record["mappings"][0]["assessment_status"] = "verified"
        record["evidence"][0]["status"] = "generated"
        self.assertTrue(any("not reviewed or accepted" in error for error in semantic_errors(record)))

    def test_high_impact_action_requires_explicit_authorization(self):
        record = deepcopy(self.record)
        record["security"]["high_impact_action"] = True
        self.assertIn("high-impact action lacks explicit authorization evidence", semantic_errors(record))

    def test_unsafe_deferred_security_finding_blocks_acceptance(self):
        record = deepcopy(self.record)
        record["security"]["open_findings"].append(
            {
                "id": "SEC-001",
                "severity": "critical",
                "disposition": "deferred",
                "prevents_safe_acceptance": True,
            }
        )
        self.assertTrue(any("prevents safe acceptance" in error for error in semantic_errors(record)))

    def test_independent_claim_requires_independent_assessor(self):
        record = deepcopy(self.record)
        record["assurance_claims"][0]["level"] = "independently_assessed"
        self.assertTrue(any("independent assessor" in error for error in semantic_errors(record)))

    def test_regulated_record_requires_role_classification_and_dates(self):
        record = deepcopy(self.record)
        record["regulatory_context"]["ai_specific_regulation_applicable"] = "yes"
        self.assertTrue(any("legal_role required" in error for error in semantic_errors(record)))

    def test_non_waivable_exception_is_rejected_by_schema(self):
        record = deepcopy(self.record)
        record["exceptions"] = [
            {
                "id": "EX-001",
                "requirement_ref": "REQ-001",
                "rationale": "Deadline",
                "risk": "Unsafe acceptance",
                "authority": "Accountable human",
                "expires_at": None,
                "review_condition": "Never",
                "compensating_controls": [],
                "non_waivable": True,
            }
        ]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "record.yaml"
            path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
            result = validate(path)
        self.assertFalse(result["valid"])
        self.assertTrue(any("False was expected" in error for error in result["structural_errors"]))


if __name__ == "__main__":
    unittest.main()
