import copy
import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate_incident import validate

class SemanticValidationTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads((ROOT / 'examples' / 'combined.json').read_text())

    def test_all_examples(self):
        for path in (ROOT / 'examples').glob('*.json'):
            with self.subTest(path=path.name):
                self.assertEqual(validate(json.loads(path.read_text())), [])

    def test_duplicate_decision_rejected(self):
        self.record['decisions'].append(copy.deepcopy(self.record['decisions'][0]))
        self.assertTrue(validate(self.record))

    def test_unauthorized_execution_rejected(self):
        self.record['response_actions'][0]['status'] = 'executed'
        self.assertTrue(validate(self.record))

    def test_invalid_transition_rejected(self):
        self.record['decisions'][0]['to_status'] = 'closed'
        self.assertTrue(validate(self.record))

    def test_missing_disclosure_authority_rejected(self):
        self.record['external_reports'].append(dict(profile='test', profile_version='1', destination='example',
            status='submitted', disclosure_authority_ref=None))
        self.assertTrue(validate(self.record))

    def test_duplicate_evidence_rejected(self):
        self.record['evidence_refs'].append(copy.deepcopy(self.record['evidence_refs'][0]))
        self.assertTrue(validate(self.record))

if __name__ == '__main__':
    unittest.main()
