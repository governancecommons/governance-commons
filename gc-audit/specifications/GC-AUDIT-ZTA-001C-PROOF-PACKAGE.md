# GC-AUDIT-ZTA-001C — Trusted Proof Package v1

**Status:** Implemented schema and standalone completeness verifier; NOT a full control PASS evaluator.  
**Contract:** `gc-audit.zta-proof-package.v1` (JSON Schema 2020-12).  
**Code:** `gc-audit/tools/zta_proof_packages.py`

## Verification boundaries

A proof package identifies target/revision/control, named checker/version/specification digest, independent authority key ID, artifact origin, required control claims, evidence IDs, and per-requirement checker results.

The **caller**, not the package or target, supplies the trusted control requirement set, approved checker/version/specification digests, evidence-integrity-verified IDs, external authority identities, and independent checker results. The verifier rejects incomplete coverage, unauthorized substitutions, wrong revision, duplicate proof records, missing evidence, and uncorroborated positive assertions.

`PROOF_PACKAGE_COMPLETE` means only that independently provided checker-result tuples match a fully covered requirement set. **It does not mean `PASS`.** A key ID in `authority` is a lookup label, not a signature, producer authentication, or a valid release authorization. A string declaring a checker result is not evidence that the checker was executed or reviewed.

Before enabling any ZTA `PASS`, implement authenticated package-to-authority binding, independently verified checker execution/artifacts, control-specific proof requirements, negative-observation conflict precedence, profile applicability, and control-revision freshness rules. False PASS remains prohibited. N/A requires independently established absence of a capability, not a package declaration.

This milestone does not register `gc-audit.zta`, mutate ZT1–ZT8, or change release eligibility. The package verifier is a **read-only component**, and the existing main evaluator still blocks unconditional release.

## Tests

`python -m unittest discover -s gc-audit/tests/zta -p 'test_*.py' -v`

Positive and negative cases include missing requirements, spoofed independent checker outputs, wrong checker digest, untrusted identity labels, revision/control mismatch, missing evidence, inconclusive and failed checks, duplicate claims, and unexpected fields. CI must pass before this increment is accepted.

## ZTA-08.02 evaluator integration (2026-10-27)

`zta_evaluator.evaluate(..., artifact_assessment=..., as_of=...)` accepts a
bounded in-memory proof for ZTA-08.02. The caller supplies a signed
`gc-audit.zta.artifact-control-policy.v1` payload and trusted approver, builder,
executor, and installation observer public keys from outside the target. The
policy pins target and revision, source and builder specification digests,
build ID, artifact digest, authorized signer IDs, every distribution/install
scope, and a timezone-bound validity interval. `required_scopes` is a separate
caller-owned inventory; it must match the signed policy exactly. `as_of` is an
explicit assessment input and must fall within that interval.

The proof supplies exact source, builder specification, build, distribution,
and installed bytes; signed source-to-build, corroborated build-execution, and
signed installation observations; and the fixed control-specific requirement
set. Every declared scope is checked. The result carries deterministic policy
and proof references in `evidence_ids`; their contents are bound through the
assessment input digest. The auditor does not build, install, fetch, execute,
or modify the target.

| Condition | ZTA-08.02 outcome |
| --- | --- |
| Approved current policy, complete matching scopes and bytes, authenticated and corroborated chain | PASS |
| Verified negative observation, including when favorable proof exists | FAIL |
| Missing, unsigned, untrusted, expired, stale-revision, tampered, partial, or conflicting positive proof | UNVERIFIED |
| Malformed assessment input contract | EVALUATION_ERROR |

This is a control-level PASS for the exact supplied revision and scopes, not
release eligibility. Other controls remain UNVERIFIED without their own proof;
the assessment remains release BLOCKED. A locally generated fixture proves
logic behavior only. A real assessment requires independently governed trust
roots, required-scope inventory, current observations, and owner review. The
signature verifies approver attribution, not that the approver is independent
in an organizational sense. The current signed installation statement has no
observation timestamp; the approved policy's expiry and explicit `as_of` bound
policy freshness, while the evidence producer and owner remain responsible for
the observation's actual collection time and completeness. Unknown distribution
routes or undeclared deployment scopes remain outside this bounded proof.
