"""GC-INCIDENT-001 draft structural and semantic validation."""
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((Path(__file__).parent / 'incident.schema.json').read_text())
VALIDATOR = Draft202012Validator(SCHEMA, format_checker=FormatChecker())
TRANSITIONS = {
    'reported': {'triaged', 'dismissed'},
    'triaged': {'active_response', 'dismissed'},
    'active_response': {'recovery_monitoring', 'closed'},
    'recovery_monitoring': {'active_response', 'closed'},
    'closed': {'triaged', 'active_response'},
    'dismissed': {'triaged'},
}

def validate(record):
    errors = [f'schema: {e.message}' for e in VALIDATOR.iter_errors(record)]
    if errors:
        return errors
    decisions = record['decisions']
    ids = [d['decision_id'] for d in decisions]
    if len(ids) != len(set(ids)):
        errors.append('duplicate decision IDs')
    evidence_ids = [e['evidence_id'] for e in record['evidence_refs']]
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append('duplicate evidence IDs')
    action_ids = [a['action_id'] for a in record['response_actions']]
    if len(action_ids) != len(set(action_ids)):
        errors.append('duplicate action IDs')
    chronology = [d['at'] for d in decisions]
    if chronology != sorted(chronology):
        errors.append('decision history out of order')
    last_state = 'reported'
    for d in decisions:
        if 'to_status' in d:
            if d.get('from_status') != last_state or d['to_status'] not in TRANSITIONS[last_state]:
                errors.append('invalid lifecycle transition')
            last_state = d['to_status']
        if d['kind'] == 'close' and d.get('to_status') != 'closed':
            errors.append('closure decision must transition to closed')
    if last_state != record['status']:
        errors.append('status does not match decision history')
    if record['status'] == 'dismissed' and not any(d['kind'] == 'dismiss' for d in decisions):
        errors.append('dismissal requires dismissal decision')
    if record['status'] == 'closed':
        closure = record['closure']
        if closure and (closure['approval_decision_ref'] not in ids or not closure['lessons_learned']):
            errors.append('closure missing approval or lessons learned')
        if closure and not any(d['decision_id'] == closure['approval_decision_ref'] and d['kind'] == 'close' for d in decisions):
            errors.append('closure approval must reference closure decision')
    for action in record['response_actions']:
        if action['status'] in ('authorized', 'executed', 'failed'):
            ref = action['decision_ref']
            if not ref or not any(d['decision_id'] == ref and d['kind'] == 'authorize' for d in decisions):
                errors.append('action lacks authorizing decision')
        if action['status'] in ('executed', 'failed') and action['execution_evidence_ref'] not in evidence_ids:
            errors.append('executed action lacks referenced evidence')
    for report in record['external_reports']:
        if report['status'] in ('submitted', 'acknowledged'):
            ref = report['disclosure_authority_ref']
            if not ref or not any(d['decision_id'] == ref and d['kind'] == 'disclose' for d in decisions):
                errors.append('submitted report lacks disclosure decision')
    return errors

if __name__ == '__main__':
    import sys
    paths = [Path(p) for p in sys.argv[1:]]
    if not paths:
        sys.exit('Usage: python validate_incident.py incident.json [incident.json ...]')
    failed = False
    for path in paths:
        issues = validate(json.loads(path.read_text()))
        print(f'{path}: ' + ('PASS' if not issues else 'FAIL: ' + '; '.join(issues)))
        failed |= bool(issues)
    sys.exit(1 if failed else 0)
