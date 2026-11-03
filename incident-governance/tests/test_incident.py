import json
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "incident.schema.json").read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

class IncidentContractTests(unittest.TestCase):
    def test_schema_is_valid(self):
        Draft202012Validator.check_schema(SCHEMA)

    def test_three_scenarios(self):
        for name in ("against_ai", "caused_by_ai", "combined"):
            with self.subTest(name=name):
                data = json.loads((ROOT / "examples" / (name + ".json")).read_text())
                self.assertEqual(list(VALIDATOR.iter_errors(data)), [])

    def test_reject_bad_classification(self):
        data = json.loads((ROOT / "examples/against_ai.json").read_text())
        data["incident_type"] = "other"
        self.assertTrue(list(VALIDATOR.iter_errors(data)))

    def test_closed_requires_closure(self):
        data = json.loads((ROOT / "examples/combined.json").read_text())
        data["status"] = "closed"
        self.assertTrue(list(VALIDATOR.iter_errors(data)))

    def test_semantic_authorization(self):
        data = json.loads((ROOT / "examples/combined.json").read_text())
        data["response_actions"][0]["execution_status"] = "executed"
        self.assertTrue(any(a["execution_status"] == "executed" and (a["authorization"] != "approved" or not a.get("authorized_by")) for a in data["response_actions"]))

    def test_duplicate_decisions(self):
        data = json.loads((ROOT / "examples/combined.json").read_text())
        data["response_actions"].append(dict(data["response_actions"][0]))
        ids = [a["id"] for a in data["response_actions"]]
        self.assertNotEqual(len(ids), len(set(ids)))

if __name__ == "__main__":
    unittest.main()
