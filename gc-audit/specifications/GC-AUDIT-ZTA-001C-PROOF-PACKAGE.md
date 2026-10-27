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
