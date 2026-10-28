# GC-AUDIT-ZTA-001F — Security remediation and authority boundary

Status: owner review candidate. No operational security assurance, release, or activation.

## Host authority contract

`artifact_assessment` contains the policy envelope and proof. The separately
passed `artifact_authority` is still **caller input** in this library execution
mode. Its keys, catalog digest, objectives, corroborated executions, and required
scopes can be changed together by a caller. Signature checks and digest matching
therefore establish consistency against the supplied roots, not independent
authority. A consistent whole chain remains `UNVERIFIED` in the control result;
verified negative observations retain `FAIL` precedence. Release eligibility
remains `BLOCKED`.

Before a host can make a stronger claim, the host must own and authenticate an
authority contract independently of the assessed target and evaluator caller.
That contract must pin the normative catalog and profile revisions, trust-key
identities and lifecycle, approver and builder policy, required platform and
installation scopes, execution corroboration source, target revision, and
freshness time. Verification must bind the contract to the actual host identity
and assessment invocation. The host must deny caller substitution of any root,
catalog, policy, or scope. Runtime enforcement and observed negative-path tests
are separately required for operational assurance. This repository has no such
host verifier or verified host evidence; this implementation intentionally has
no ZTA-08.02 `PASS` route. A future route requires a separately reviewed,
host-owned contract and new adversarial tests.

## Registry boundary

Structural registry validation permits a planned or absent self-audit when no
assurance policy requires it. An active self-audit must have its exact executable
registration and zero-trust declaration. The `--require-self-audit` switch is
the explicit required-assurance gate; the canonical CI uses it. The validator
reports `self_audit_readiness` separately from `REGISTRY_CONTRACT_VALID`.

PowerShell source matching reports known write cmdlets in read-only registrations
and indirect or computed invocation. It is a static alarm, not a sandbox. The
`--require-runtime-assurance` gate fails closed because no trusted-host runtime
confinement evidence is available. Unrecognized PowerShell syntax can still
escape the patterns; only independently tested host restrictions can support a
runtime-security claim.

`--repo-root` selects the checkout independent of its physical directory name;
the default is the registry file's repository. The resolved repository must be
inside the resolved portfolio root, and resolved scripts must remain under its
tools directory. Tests cover traversal, sibling prefixes, file links, repository
ancestor links, and Windows junctions where the OS permits fixture creation.

## Finding disposition

| Finding | Remediation | Remaining gate |
| --- | --- | --- |
| F01 | Conditional readiness and required gate | Host chooses and enforces policy |
| F02 | Demonstrated bypasses flagged; runtime gate fails closed | Trusted-host confinement and denial tests |
| F03 | Caller-chosen consistent chain cannot PASS | Independent host authority contract and proof |
| F04 | Cause-specific negative fixtures and bypass regressions | None for these fixtures |
| F05 | Transitive tools, catalog, schemas, specs, and tests trigger 3-OS checks | Exact-final-commit hosted CI |
| F06 | Resolved-root containment and link/junction fixtures | Platform skips disclosed in evidence |
| F07 | Historical PLAY unchanged; this record and PR provide corrections | Owner review and separate acceptance |

Additional work: **BLOCKER** for any operational assurance or positive ZTA-08.02
claim: host authority and runtime confinement proof. **REQUIRED** before
implementation acceptance: exact-head CI and independent owner review.
**DEFERRED**: GUI, AI advisers, Cockpit adapters, other audit domains, and
unrelated legacy ZT1–ZT8 revisions.
