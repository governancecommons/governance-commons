"""Keep the draft catalog exactly anchored to the frozen normative control table."""
import json
import re
import unittest
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[2]
CATALOG=ROOT/"catalogs"/"gc-audit.zta-controls.v1.draft.json"
SCHEMA=ROOT/"schemas"/"zta"/"gc-audit.zta-controls.v1.schema.json"
CONTRACT=ROOT/"specifications"/"GC-AUDIT-ZTA-001-V1-ACCEPTANCE-CONTRACT.md"

class NormativeCatalogTests(unittest.TestCase):
    def test_schema_and_exact_normative_trace(self):
        catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
        schema=json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(catalog)
        rows=[line.split("|")[1:-1] for line in CONTRACT.read_text(encoding="utf-8").splitlines()
              if re.match(r"^\| ZTA-\d\d\.0[12] \|",line)]
        self.assertEqual(len(rows),24)
        controls={c["control_id"]:c for c in catalog["controls"]}
        self.assertEqual(len(controls),24)
        self.assertEqual(set(controls),{r[0].strip() for r in rows})
        for cells in rows:
            cid,name,objective,trigger,evidence,failure,severity,role=[x.strip() for x in cells]
            c=controls[cid]
            with self.subTest(control=cid):
                self.assertEqual(c["objective"],name+": "+objective)
                self.assertEqual(c["applicability"]["capability"],trigger)
                self.assertEqual(c["required_evidence"],[evidence])
                self.assertEqual(c["fail_predicate"],failure)
                self.assertEqual(c["severity"],severity.upper())
                self.assertEqual(c["remediation_role"],role)
                self.assertIn("not yet approved",c["verification"]["sufficiency"])
    def test_fixture_is_not_normative_catalog(self):
        draft=json.loads(CATALOG.read_text(encoding="utf-8"))
        fixtures=json.loads((ROOT/"tests"/"zta"/"schema-fixtures.v1.json").read_text(encoding="utf-8"))
        self.assertNotEqual(draft,fixtures["valid"]["controls"])
        self.assertNotEqual(draft["id"],"fixture-controls")

if __name__=="__main__":
    unittest.main()
