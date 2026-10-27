#!/usr/bin/env python3
"""GC-AUDIT ZTA-001B JSON Schema fixture runner (read only).

Requires Python 3.11+ and jsonschema>=4.18. Run:
  python -m pip install 'jsonschema[format]>=4.18'
  python gc-audit/tests/zta/validate-schemas.py
"""
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

root = Path(__file__).resolve().parents[2]
schema_dir = root / "schemas" / "zta"
fixtures = json.loads((Path(__file__).parent / "schema-fixtures.v1.json").read_text(encoding="utf-8"))
errors = []
validators = {}
for key in fixtures["valid"]:
    path = schema_dir / f"gc-audit.zta-{key}.v1.schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validators[key] = Draft202012Validator(schema, format_checker=FormatChecker())
for key, record in fixtures["valid"].items():
    found = list(validators[key].iter_errors(record))
    if found:
        errors.append(f"VALID fixture {key} rejected: {found[0].message}")
for name, fixture in fixtures["invalid"].items():
    if not list(validators[fixture["schema"]].iter_errors(fixture["record"])):
        errors.append(f"INVALID fixture {name} was accepted")
if errors:
    raise SystemExit("\n".join(errors))
print(f"ZTA schema fixtures PASS: {len(fixtures['valid'])} valid, {len(fixtures['invalid'])} invalid")
