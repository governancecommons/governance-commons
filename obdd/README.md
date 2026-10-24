# Outcome-Bound Development and Delivery (OBDD)

This directory contains the accepted OBDD v1.1 conformance and assurance
surface. Acceptance does not establish universal legal applicability or
external certification.

The current base directive is
[`GC-DD-01`](../passes/dev-accord/GC-DD-01.md), version 1.1.0, accepted by
Jesse Ervin as owner and authorized approver on 2026-10-24. OBDD-CA-01 is its
accepted conformance and assurance annex.

## Current artifact

- [`OBDD-CA-01.md`](OBDD-CA-01.md) — accepted Conformance and Assurance Annex.
- [`assurance-record.template.yaml`](assurance-record.template.yaml) — an
  intentionally incomplete adopter template.
- [`../schemas/obdd-assurance-record.schema.json`](../schemas/obdd-assurance-record.schema.json)
  — the machine-readable record contract.
- [`../scripts/validate_obdd_assurance.py`](../scripts/validate_obdd_assurance.py)
  — structural and semantic validation.

## Using the assurance record

1. Copy `assurance-record.template.yaml` into the adopting project's evidence
   area.
2. Identify the execution objective, accountable authority, jurisdiction,
   legal role, applicable external requirements, risk classification, security
   controls, evidence, approvals, exceptions, and review dates.
3. Run:

   ```powershell
   python scripts/validate_obdd_assurance.py path\to\assurance-record.yaml
   ```

4. Treat a successful validation as evidence that the record is internally
   complete and consistent. It is not an external certification or a substitute
   for legal, security, privacy, or independent assessment.

The template fails validation until deployment-specific determinations and
evidence are supplied. That behavior is intentional.
