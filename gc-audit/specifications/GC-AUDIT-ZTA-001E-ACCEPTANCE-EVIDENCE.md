# GC-AUDIT-ZTA-001E — Final remediation acceptance evidence

Status: OWNER REVIEW CANDIDATE; acceptance and activation blocked.
Scope: Governance Commons `gc-audit.zta` evaluator and operation-registry security boundary. Baseline: `d570609f767c00465efcc39080f433757d830e5f` on `main`, 2026-10-27. This report describes local verification of the feature branch; hosted CI and owner review are separate evidence.

## Finding disposition

| PR #7 finding | Disposition at this revision | Evidence and limit |
| --- | --- | --- |
| AR-01 24 control predicates | Deferred for additional PASS routes | Catalog has 24 objectives and an external digest check. Only ZTA-08.02 can receive favorable control verification. |
| AR-02 host delegation | Open for real host | ZTA-06.02 remains UNVERIFIED on positive package claims; verified bypass observations yield FAIL. No real delegated host proof supplied. |
| AR-03 evidence producer authority | Partially remediated | ZTA-08.02 input now separates untrusted assessment data from caller-supplied authority. The host must authenticate and protect that authority independently. |
| AR-04/05 mutation defaults | Historically resolved | Existing normalizers require `-Apply`; `-FixNotes` is absent. Existing ZT1–ZT8 audit reports no errors; black-box mutation tests remain open. |
| AR-06 registry self-audit | Remediated as static contract validation | YAML parser rejects duplicate keys, malformed/unknown authority, IDs, fields, aliases, inconsistent mutation/authorization metadata, unsafe paths, redirected self-audit steps, and missing self-audit operations. Its registry policy is repository-owned and still needs independent review/pinning for production use. |
| AR-07 shell delegation | Open for runtime proof | Static scan flags indirect calls in `validate-recent-work.ps1` and `validate-registry.ps1`. It is not an execution sandbox. Existing ZT4 warning for `validate-portfolio-health.ps1` remains. |
| AR-08 malicious paths/OS parity | Local fixtures added; hosted pending | Windows absolute/UNC, URI, traversal, prefix collision, symlink, malformed metadata and alias cases exercise the parser. The Windows symlink fixture skips if link creation is unavailable. Hosted Windows/Linux/macOS matrix must be checked at the PR head. |
| AR-09 static-only evidence | Open outside ZTA-08.02 | No new favorable control route. Synthetic ZTA-08.02 chain tests do not prove an actual target. |
| AR-10 reassessment/independent review | Deferred to pilot/release decision | No operational activation or independent review claimed. |

## Requirement to test trace

| Requirement | Verification |
| --- | --- |
| Fail-closed semantic registry | `test_operation_registry.py` (28 cases, one platform skip) and self-audit CLI on the canonical registry. |
| Separate assessor data from trusted authority | `test_artifact_integration.py::test_assessment_cannot_supply_its_own_authority`; ZTA evaluator suite. |
| Delegated host claim cannot PASS; negative precedence | `test_decision_gate.py` host cases and existing negative-observation fixtures. |
| Incomplete/stale/tampered chain cannot PASS | `test_artifact_integration.py` and the other ZTA evaluator tests. |
| Schema contract | `gc-audit/tests/zta/validate-schemas.py`: 6 valid and 21 invalid fixtures. |
| Legacy posture | `validate-zero-trust.ps1`: ZT1–ZT8, 0 errors, 2 warnings. |
| Planning, PLAY, OBDD and release compatibility | `validate-planning.ps1`, `validate-playbook.ps1`, OBDD and release compatibility unit tests, and `scripts/validate_release.py`. |

## Local verification and provenance

At the feature branch working revision, isolated Python 3.13 environments produced: 174 ZTA unit tests PASS; 28 registry tests PASS with one Windows symlink skip; 6 positive and 21 negative schema fixtures PASS; 10 OBDD tests PASS; 22 release compatibility tests PASS. The canonical operation registry self-audit returned `REGISTRY_CONTRACT_VALID` and `delegation_review: REQUIRED`. Planning checked 27 documents with no errors. PLAY checked 26 records with no errors, including the late current record. The GC v1.2.0 release manifest compatibility check passed, but it does not establish package publication or GC-AUDIT ZTA release readiness. `git diff --check` and `git fsck --no-reflogs` passed; fsck reported dangling objects, not corruption.

The Level 1 diagnostic failed its review-grammar check because this independent checkout lacks the file at the validator's expected in-repo path; the canonical file is `C:\dev\portfolio-control\docs\REVIEW-GRAMMAR.md`. This known topology mismatch is not waived as green. The first-response preflight stamp was omitted in this session, so preflight conformance is blocked.

## Readiness and owner decision

**Evaluator readiness:** bounded ZTA-08.02 control verification is locally tested. Other controls default to UNVERIFIED absent independent proof. The evaluator has no registered `gc-audit.zta` operation or general consumer invocation contract yet, so implementation acceptance is blocked.

**Operational readiness:** blocked. No actual target assessment, production trust-root ownership, delegated-host assurance, independently verified installation scope, independent security review, or release artifact proof was supplied. Green fixtures and CI cannot substitute for these.

**Recommended owner decision: BLOCK final acceptance and activation.** Review the focused remediation PR; require exact-head hosted CI and independent review before considering the implementation gate. Separately decide the safe operation registration/invocation contract and a real pilot with owner-controlled authority. No merge, tag, publication, activation, certification, or risk acceptance is implied by this document.
