# GC-INCIDENT-001 draft package

Owner-approved scope, draft artifacts only; not released.

- `GC-INCIDENT-001.md`: normative proposal and boundaries
- `incident.schema.json`: JSON Schema Draft 2020-12
- `examples/`: three illustrative, synthetic records
- `mappings/`: research-only NIST topic/function crosswalks
- `tests/`: structural and selected semantic validation

Run `python -m pip install jsonschema PyYAML` then `python -m unittest discover -s tests -v` from this directory. The test suite is a draft validation harness, not a production certification.
