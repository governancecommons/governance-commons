# GC-AUDIT-ZTA-001C — Positive proof checker boundary

**Status:** Initial source-backed proof checker committed; full PASS and NOT_APPLICABLE control decisions remain NOT IMPLEMENTED.

## Implemented checker

`zta_positive_checks.verify_artifact_pair` can verify **exact build and installed artifact bytes** against a SHA-256 digest provided by the **trusted release authority outside the target**. It binds the expected digest to `target_id` and `revision`. It accepts raw, pre-supplied bytes, never launches target code, downloads artifacts or mutates files.

The caller is responsible for supplying trustworthy, independently collected build and installed artifacts and an approved reference digest. A target-controlled reference digest does not establish approval. The checker is not connected to `evaluate` as an automatic PASS route because `ZTA-08.02` also covers end-to-end build/distribution integrity: matching bytes alone does not verify provenance, all distribution hops, release approval or actual deployment state.

The output is `BYTE_INTEGRITY_VERIFIED`, **not** `PASS`. The full control evaluator continues to block release if applicable proof remains insufficient.

## Acceptance and next gate

The checker has positive and adversarial tests for equal bytes, build/installation tampering, wrong revision, wrong target, malformed digest and empty/wrongly typed payload. Tests run through the existing evaluator-core GitHub Actions workflow.

**Next required gate:** version a trusted proof-package contract identifying the independent authority, precise scoped claims, coverage, target revision, test specification, artifact origin, and independent verifier inputs. Add explicit per-control completeness rules and coverage checks. Only then allow a validated full-control `PASS`. `NOT_APPLICABLE` additionally requires independent evidence of the absent capability and no contradicting observations. Do not produce PASS/N/A based solely on target assertions or signer identity.

This proof checker is separate from `gc-audit.zerotrust` ZT1–ZT8; neither is modified.
