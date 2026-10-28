# GC-AUDIT-ZTA-002A — Control-specific sufficiency specification

Status: PROPOSED for AL:2 review. Specification only; no implementation, operational assurance, deployment or release.
Date: 2026-10-28.
References: GC-AUDIT-TARGET-001, GC-AUDIT-EVIDENCE-001/002, GC-AUDIT-ZTA-001; catalog `gc-audit.zta-controls.v1.draft.json`; OBDD.

## Purpose and scope

Define required evidence and failure predicates for three existing ZTA controls. Reuse the existing authoritative evaluator, proof/decision gate, local host verifier and evidence formats. Do not grant `PASS` solely on signed bytes, local assertions, repository inventories, or synthetic credentials. The Portal application pilot remains evidence of selected local behavior, not operational conformance.

## Catalog mappings and exact boundaries

- `ZTA-01.02` — Identity verification: a component claiming authentication verifies the principal before protected access. Portal pilot mapped anonymous HTTP 401 and synthetic owner HTTP 200; synthetic sessions do not verify production GitHub OAuth.
- `ZTA-02.01` — Authorization enforcement: policy decision precedes every privileged action at an enforceable boundary. Portal pilot mapped reviewer import denial and local editorial role separation; no general bypass coverage.
- `ZTA-02.02` — Authorization replay prevention: expired, consumed or mismatched authorization cannot trigger new privileged action. Revoking a session is relevant evidence but cannot by itself prove this separate authorization-decision replay objective.

## Common gates for admissible control PASS

1. Approved exact target and environment, revision/build and catalog/profile versions.
2. Applicability recorded by an authorized evaluator from actual implemented capabilities, not inferred from arbitrary target text.
3. Operation inventory and trust boundary, with named policy decision and enforcement components.
4. Host-authorized scoped collection under an independently governed root; collector identity, role, method, clock and freshness independently verified.
5. Authentic evidence bound to exact target, revision, environment, control objective, operation and test result, with reproducible negative and positive cases.
6. Complete control-specific proof coverage for the approved scope, including direct bypass paths and relevant adverse observations.
7. No contradictory verified negative observation, revoked policy, stale credential or trust-boundary ambiguity.
8. Human acceptance/release authorization separate from evaluator verdict.

Until distinct enforceable host/collector/target principals and independent provisioning have been demonstrated, the EVIDENCE-002 `CONFIGURED_ROOT_ONLY` classification cannot justify operational PASS. Any future narrowly scoped PASS route requires explicit owner-approved proof policy and adversarial regression tests, not a blanket signature shortcut.

## ZTA-01.02 — Identity verification

Required for possible PASS: inventory of protected operations; verified external identity mechanism and its configured trust boundary; authorized-success and missing/invalid/forged identity denial tests at the enforcement point; expired and revoked session rejection; confirmed direct-route protection within scope; trusted host evidence with exact revision/environment binding.

FAIL only on verified observation of a principal not independently authenticated gaining protected access. Missing paths, synthetic session insertion or incomplete OAuth validation means UNVERIFIED, not PASS or FAIL.

## ZTA-02.01 — Authorization enforcement

Required for possible PASS: fixed permission matrix mapped to every selected privileged operation; proof that server/store enforcement occurs before action; allowed-role success and unauthorized-role denial; direct endpoint/action invocation without UI; changed/disabled role rejection; side-effect checks showing denial truly prevented the action; independently authenticated host test evidence and bypass review.

FAIL only on verified privileged execution despite denial/absence of required decision. An HTTP 403 alone does not establish no side effect. A subset of operations cannot imply application-wide enforcement.

## ZTA-02.02 — Authorization replay prevention

Required for possible PASS: identified reusable authorization tokens, decisions and grants; named lifecycle and binding to actor, operation, target and expiry; first permitted execution; repeated/consumed token denial; expired/stale grant denial; cross-operation and cross-target substitution denial; state/side-effect evidence; trusted host provenance.

FAIL only on verified renewed privileged execution from an expired/consumed/mismatched authorization. Session revocation alone is insufficient to establish the replay property. If the system has no applicable reusable authorization decisions, an authorized applicability review must document it; do not assume N/A based on absence of a test.

## Decision matrix

| Evidence state | Result |
| --- | --- |
| Complete scoped, admissible proof of objective and no verified adverse evidence | PASS may become eligible only under explicitly approved future policy |
| Independently corroborated objective violation | FAIL under the existing negative-observation decision gate |
| Valid local positive and negative tests but no independent host authority | UNVERIFIED |
| Signed producer message with untrusted or caller-selected root | REJECTED/UNVERIFIED |
| Missing coverage, ambiguous applicability, stale or conflicting evidence | UNVERIFIED (or evaluation error if malformed) |
| Target or collector claims compliance in prose | UNVERIFIED |

No aggregate compliance score or operational release approval is generated from these draft sufficiency rules.

## Negative and adversarial test plan

- Anonymous access; forged identity/session; expired/revoked session; disabled membership; same-user cross-workspace access.
- Allowed and denied roles; direct route, missing CSRF, forged origin; denial with side-effect inspection; bypass of designated policy enforcement.
- Reused authorization decision; expired/consumed grant; changed target, actor, revision or action.
- Wrong/unknown collector, unauthorized method/scope; signature modification, replay across process restart, clock/freshness, revoked host policy, substituted configuration root, tampered report.
- Distinct-principal host isolation demonstration must occur before stronger authority claims; same-principal fixture must remain CONFIGURED_ROOT_ONLY.
- Historical Portal, repository and EVIDENCE-001/002 exports continue to verify without rewriting.

## Bounded implementation acceptance

1. Versioned machine-readable sufficiency policy for only these three controls with distinct applicability, required observation kinds and authority prerequisites.
2. Deterministic tests of missing, present, adverse, replayed and contradictory evidence; no unauthorized PASS route.
3. An evidence-to-control mapping for the Portal pilot that truthfully retains currently UNVERIFIED results.
4. Human-readable explanations showing which exact proof item is missing and what to test next.
5. Cross-platform regressions, exact-target evidence, and a separate PR for owner review.
6. No Portal runtime changes, operational ZTA claims, release/activation or broad framework refactor in this milestone.

## OBDD classification

BLOCKER for operational PASS: independent host roots, OS-enforced identity separation, authentic runtime proof and complete control coverage. REQUIRED: three bounded sufficiency contracts, negative tests, evidence mapping, preservation of existing gates. DEFERRED: remaining 21 controls, production deployment, automatic remediation, new AI/Cockpit/UI features, generalized compliance certification.

Stop once the three-control mapping and deterministic evaluation requirements are demonstrated.