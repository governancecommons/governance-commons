# GC-HCI-CONTRACT-001 — HCI evaluation contracts v0.1

**Status:** implementation candidate; no HCI audit operation activated.  
**Authority:** GC-AUDIT contracts, with owner acceptance still required.

## Contract inventory
The five schemas in `schemas/gc-hci-*.v0.1.schema.json` define evaluation profiles, criteria, evidence, findings and reports. All use JSON Schema Draft 2020-12. Fixtures under `gc-audit/hci/fixtures/` are **synthetic test data**, not empirical results.

## Compatibility with existing Governance Commons
- `gc-audit.result.v1` remains unchanged. It retains `pass|warn|fail|skipped`. HCI criterion `outcome` is a separate field with six states. A reporting adapter must not reduce `INCONCLUSIVE`, `REVIEW_REQUIRED` or `NOT_EVALUATED` to a readiness pass.
- `governed-event/0.1` remains unchanged. A governed HCI observation, review decision or lifecycle transition must be emitted using a valid registered event profile and all twelve required envelope fields. Detailed task traces remain separately referenced evidence artifacts.
- Governed Event requires a **full embedded** `time.loc` record (v1.1 or v1.2), not a bare timestamp. The evidence schema's `recorded_at` is only a descriptive timestamp; it is not a substitute for Governed Event provenance.
- `unsigned` or `UNSIGNED` does **not** establish tamper verification. GC evidence bundle signing is currently disabled in the inspected registry.
- Historical evidence is immutable. Amendments must be append-only and reference prior identifiers and hashes. Do not activate a proprietary amendment mechanism before GC-AUDIT-AMD-001 is accepted.
- `gc-audit.hci` is **not registered or executable** by this change. Adding an audit command needs a separately verified, allowlisted, read-only implementation and approved registry change.

## Outcome reporting
| HCI finding | Mapping recommendation |
| --- | --- |
| SATISFIED | pass only if every required applicable criterion is satisfied |
| NOT_SATISFIED | fail if acceptance requires the criterion |
| INCONCLUSIVE | warn or fail-closed under acceptance gating |
| REVIEW_REQUIRED | warn or fail-closed under acceptance gating |
| NOT_APPLICABLE | exclude from denominator with rationale |
| NOT_EVALUATED | warn or fail-closed under acceptance gating |

This table is guidance for a future adapter, **not** an implemented aggregate algorithm. Report readiness must be computed by a future evaluator from the approved profile and verified findings; JSON Schema alone does not enforce count consistency or evidence-reference resolution.

## Validity constraints
Expert review is never participant behavior. A synthetic fixture is never evidence of actual usability. Source-backed practitioner guidance is not an automatically applicable legal requirement. Each sourced claim carries its own evidence classification and limitations.

## Tests
Run `python -m unittest discover -s gc-audit/hci/tests -v` with `jsonschema` installed. The tests verify five positive fixtures, negative missing-field cases and a rejected invalid outcome. They do not constitute an executed HCI pilot.
