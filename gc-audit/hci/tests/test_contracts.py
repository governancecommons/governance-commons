"""GC-HCI-CONTRACT-001 schema fixture conformance tests; stdlib unittest + jsonschema."""
import json
import pathlib
import unittest

from jsonschema import Draft202012Validator, FormatChecker

ROOT = pathlib.Path(__file__).resolve().parents[3]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "gc-audit" / "hci" / "fixtures"
KINDS = ("profile", "criterion", "evidence", "finding", "report")

class HCIContractTests(unittest.TestCase):
    def _pair(self, kind):
        schema = json.loads((SCHEMAS / f"gc-hci-{kind}.v0.1.schema.json").read_text(encoding="utf-8"))
        fixture = json.loads((FIXTURES / f"{kind}.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        return Draft202012Validator(schema, format_checker=FormatChecker()), fixture

    def test_valid_fixtures(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                validator, fixture = self._pair(kind)
                self.assertEqual(list(validator.iter_errors(fixture)), [])

    def test_missing_required_field_rejected(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                validator, fixture = self._pair(kind)
                del fixture["id"]
                self.assertTrue(list(validator.iter_errors(fixture)))

    def test_invalid_outcome_rejected(self):
        validator, fixture = self._pair("finding")
        fixture["outcome"] = "PASS"
        self.assertTrue(list(validator.iter_errors(fixture)))

    def test_unsigned_not_signature_verified(self):
        validator, fixture = self._pair("evidence")
        fixture["integrity"]["state"] = "SIGNATURE_VERIFIED"
        self.assertTrue(list(validator.iter_errors(fixture)))

if __name__ == "__main__":
    unittest.main()
