"""Validate an OBDD-CA-01 assurance record without making compliance claims."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "obdd-assurance-record.schema.json"


def _duplicates(values: list[str]) -> set[str]:
    return {value for value in values if values.count(value) > 1}


def semantic_errors(record: dict[str, Any]) -> list[str]:
    """Apply fail-closed cross-reference and assurance-level checks."""
    errors: list[str] = []
    requirements = {item["id"]: item for item in record.get("requirements", [])}
    evidence = {item["id"]: item for item in record.get("evidence", [])}

    for label, values in (
        ("requirement", [item["id"] for item in record.get("requirements", [])]),
        ("mapping", [item["id"] for item in record.get("mappings", [])]),
        ("evidence", [item["id"] for item in record.get("evidence", [])]),
    ):
        for duplicate in sorted(_duplicates(values)):
            errors.append(f"duplicate {label} id: {duplicate}")

    for requirement in record.get("requirements", []):
        if requirement["applicability"] == "applicable" and requirement["review_status"] == "not_assessed":
            errors.append(f"{requirement['id']}: applicable requirement is not assessed")
        if requirement["applicability"] == "undetermined" and record.get("status") != "draft":
            errors.append(f"{requirement['id']}: non-draft record has undetermined applicability")

    for mapping in record.get("mappings", []):
        prefix = mapping["id"]
        requirement = requirements.get(mapping["requirement_ref"])
        if requirement is None:
            errors.append(f"{prefix}: unknown requirement_ref {mapping['requirement_ref']}")
            continue
        if mapping["mapping_type"] == "not_applicable" and requirement["applicability"] != "not_applicable":
            errors.append(f"{prefix}: not_applicable mapping conflicts with requirement applicability")
        if requirement["applicability"] == "applicable" and mapping["mapping_type"] != "not_applicable" and not mapping["evidence_refs"]:
            errors.append(f"{prefix}: applicable mapping has no evidence")
        for evidence_ref in mapping["evidence_refs"]:
            if evidence_ref not in evidence:
                errors.append(f"{prefix}: unknown evidence_ref {evidence_ref}")
        if mapping["assessment_status"] in {"verified", "independently_assessed"}:
            if not mapping["evidence_refs"]:
                errors.append(f"{prefix}: verified mapping has no evidence")
            for evidence_ref in mapping["evidence_refs"]:
                item = evidence.get(evidence_ref)
                if item and item["status"] not in {"reviewed", "accepted"}:
                    errors.append(f"{prefix}: evidence {evidence_ref} is not reviewed or accepted")

    security = record.get("security", {})
    if security.get("high_impact_action") and not security.get("explicit_authorization_evidence"):
        errors.append("high-impact action lacks explicit authorization evidence")
    for evidence_ref in security.get("explicit_authorization_evidence", []):
        if evidence_ref not in evidence:
            errors.append(f"security: unknown authorization evidence_ref {evidence_ref}")
    for finding in security.get("open_findings", []):
        if finding["prevents_safe_acceptance"] and finding["disposition"] in {"open", "deferred", "accepted"}:
            errors.append(f"security finding {finding['id']} prevents safe acceptance")

    oversight = record.get("human_oversight", {})
    if record.get("status") != "draft" and not oversight.get("accountable_authorities"):
        errors.append("non-draft record lacks an accountable authority")
    approval_ids = {item["id"] for item in oversight.get("approvals", [])}
    for approval in oversight.get("approvals", []):
        if approval["evidence_ref"] not in evidence:
            errors.append(f"approval {approval['id']}: unknown evidence_ref {approval['evidence_ref']}")
    for required in oversight.get("required_approvals", []):
        if record.get("status") != "draft" and required not in approval_ids:
            errors.append(f"required approval is missing: {required}")

    for claim in record.get("assurance_claims", []):
        prefix = f"claim {claim['scope']}"
        for evidence_ref in claim["evidence_refs"]:
            if evidence_ref not in evidence:
                errors.append(f"{prefix}: unknown evidence_ref {evidence_ref}")
        if claim["level"] in {"implemented", "verified", "independently_assessed"} and not claim["evidence_refs"]:
            errors.append(f"{prefix}: {claim['level']} requires evidence")
        if claim["level"] == "independently_assessed" and not claim["assessor_independent"]:
            errors.append(f"{prefix}: independent assessment requires an independent assessor")

    for exception in record.get("exceptions", []):
        if exception["requirement_ref"] not in requirements:
            errors.append(f"exception {exception['id']}: unknown requirement_ref {exception['requirement_ref']}")

    regulatory = record.get("regulatory_context", {})
    if regulatory.get("ai_specific_regulation_applicable") == "yes":
        for field in ("legal_role", "system_classification"):
            if not regulatory.get(field):
                errors.append(f"regulatory_context: {field} required when AI-specific regulation applies")
        for field in ("jurisdictions", "effective_dates"):
            if not regulatory.get(field):
                errors.append(f"regulatory_context: {field} required when AI-specific regulation applies")
    if regulatory.get("ai_specific_regulation_applicable") == "unknown" and record.get("status") != "draft":
        errors.append("non-draft record has unknown AI-specific regulatory applicability")

    risk = record.get("objective", {}).get("risk", {})
    if risk.get("tier") == "unclassified" and record.get("status") != "draft":
        errors.append("non-draft record has unclassified risk")
    if record.get("status") in {"verified", "independently_assessed"} and not record.get("assurance_claims"):
        errors.append("verified record has no assurance claim")

    maintenance = record.get("maintenance", {})
    if record.get("status") != "draft" and not maintenance.get("last_reviewed_at"):
        errors.append("non-draft record has no maintenance review date")
    return errors


def validate(path: Path, schema_path: Path = SCHEMA_PATH) -> dict[str, Any]:
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    structural = sorted(
        (f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}" for error in validator.iter_errors(record)),
    )
    semantic = [] if structural else semantic_errors(record)
    return {
        "subject": str(path),
        "schema": str(schema_path),
        "valid": not structural and not semantic,
        "structural_errors": structural,
        "semantic_errors": semantic,
        "assurance_boundary": "Validation is not legal advice, approval, independent assessment, certification, or proof that evidence is genuine.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--schema", type=Path, default=SCHEMA_PATH)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    result = validate(args.record, args.schema)
    if args.as_json:
        print(json.dumps(result, indent=2))
    else:
        print("PASS" if result["valid"] else "FAIL", result["subject"])
        for error in result["structural_errors"] + result["semantic_errors"]:
            print(f"- {error}")
        print(result["assurance_boundary"])
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
