import copy, json, pathlib, unittest
from jsonschema import Draft202012Validator, FormatChecker
ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT/'incident.schema.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())

def semantic_errors(record):
    errors=[]
    decisions=record['decisions']
    ids=[d['decision_id'] for d in decisions]
    if len(ids)!=len(set(ids)): errors.append('duplicate decision IDs')
    if record['status'] in ('closed','dismissed') and not decisions: errors.append('terminal state without decision')
    if record['status']=='closed':
        close=record['closure']
        if close and (close['approval_decision_ref'] not in ids or not close['lessons_learned']): errors.append('closure lacks approval or lessons')
    for a in record['response_actions']:
        if a['status'] in ('authorized','executed') and (not a['decision_ref'] or a['decision_ref'] not in ids): errors.append('action without decision')
        if a['status']=='executed' and not a['execution_evidence_ref']: errors.append('executed action without evidence')
    if record['status']=='dismissed' and not any(d['kind']=='dismiss' for d in decisions): errors.append('dismissal decision absent')
    return errors

class TestIncident(unittest.TestCase):
    def test_schema_is_valid(self): Draft202012Validator.check_schema(SCHEMA)
    def test_examples(self):
        for f in (ROOT/'examples').glob('*.json'):
            with self.subTest(f=f.name):
                obj=json.loads(f.read_text()); self.assertEqual(list(VALIDATOR.iter_errors(obj)),[]); self.assertEqual(semantic_errors(obj),[])
    def test_invalid_type(self):
        obj=json.loads((ROOT/'examples'/'against_ai.json').read_text()); obj['incident_type']='other'
        self.assertTrue(list(VALIDATOR.iter_errors(obj)))
    def test_invalid_closure(self):
        obj=json.loads((ROOT/'examples'/'against_ai.json').read_text()); obj['status']='closed'
        self.assertTrue(list(VALIDATOR.iter_errors(obj)))
    def test_unauthorized_execution(self):
        obj=json.loads((ROOT/'examples'/'against_ai.json').read_text()); obj['response_actions'][0]['status']='executed'
        self.assertTrue(semantic_errors(obj))
    def test_duplicate_decision(self):
        obj=json.loads((ROOT/'examples'/'against_ai.json').read_text()); obj['decisions'].append(copy.deepcopy(obj['decisions'][0]))
        self.assertTrue(semantic_errors(obj))

if __name__=='__main__': unittest.main()
