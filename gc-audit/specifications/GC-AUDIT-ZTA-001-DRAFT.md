# GC-AUDIT-ZTA-001 — Application-Level Zero Trust Audit Specification

**Status: DRAFT — NOT IMPLEMENTED — NOT FROZEN**  
**Milestone:** GC-AUDIT-ZTA-001A / candidate v0.1  
**Owner:** Governance Commons  
**Created:** 2026-10-27  
**Purpose:** Durable record of owner-approved architecture boundaries and proposed specification work developed in the GC-AUDIT-ZTA design conversation. This document does not represent auditor implementation, completed conformance, passing tests, or release authorization.

## Outcome and scope

Provide a reusable, read-only, evidence-backed, deterministic application-level Zero Trust assessment operation, `gc-audit.zta`. It complements but MUST NOT replace, weaken, or silently reinterpret existing `gc-audit.zerotrust` and its ZT1–ZT8 GC-AUDIT tooling posture checks. Cockpit CLI (`jj-ervin/cockpit-cli`) is the first intended reference consumer, but its actual security assessment and remediation belong to CKP-CLI-008 in the Cockpit CLI project, not in this specification.

The audit must be architecture-aware, evaluate explicitly identified protected resources and actor/trust boundaries, preserve application versus trusted-host ownership, and refuse unsupported claims of verification or compliance. Assessment is not an external certification.

## Existing capability and gap

`gc-audit.zerotrust` is registered as read-only and invokes `gc-audit/tools/validate-zero-trust.ps1`. Its checks are ZT1 path containment, ZT2 mutation safety, ZT3 script registration, ZT4 shell delegation, ZT5 fail-closed defaults, ZT6 explicit authorization declarations, ZT7 registry network isolation, and ZT8 evidence-principal presence/configuration. The current implementation uses textual inspection, pattern matching, and filesystem checks; these are useful posture signals, **not** proof of application-level runtime Zero Trust guarantees. Existing `gc-audit.result.v1` output is not universally emitted by every validator; do not assume `gc-audit.zta` is implemented.

## Source alignment

- NIST SP 800-207: resource-centered, explicit trust/access decisions and policy enforcement; a reference architecture, not a requirement to deploy a distinct policy server in every app.
- NIST SP 800-218 SSDF: secure software development and supply-chain practices.
- CISA Zero Trust Maturity Model: contextual governance and architecture guidance.
- OWASP ASVS and SLSA: selectively applicable application controls and build provenance.

Distinguish GC **normative** controls from **mapped** external guidance and **advisory** recommendations. Never assert official NIST/CISA/OWASP compliance or certification based solely on this audit.

## Proposed 24-control catalog

IDs are stable within this **draft**, but normative detailed predicates, evidence sufficiency and severity rules remain to be frozen. The .01 control is the profile baseline **when its protected capability exists**; .02 is conditional upon capability/deployment context. Absence or delegation does not automatically satisfy a control.

| Domain | Topic | Baseline control | Conditional control |
| --- | --- | --- | --- |
| ZTA-01 | Identity and actor attribution | ZTA-01.01: Identify actors; distinguish asserted from verified identity | ZTA-01.02: Authenticate identity where target performs identity verification |
| ZTA-02 | Authentication and authorization boundaries | ZTA-02.01: Authorize at protected operation boundary | ZTA-02.02: Prevent replay and unauthorized decision reuse |
| ZTA-03 | Least-privilege execution | ZTA-03.01: Constrain exposed execution capabilities | ZTA-03.02: Enforce runtime least privilege |
| ZTA-04 | Provider registration and origin integrity | ZTA-04.01: Constrain provider registration and resolution | ZTA-04.02: Verify provider origin and integrity |
| ZTA-05 | Input validation and command injection resistance | ZTA-05.01: Validate untrusted command inputs | ZTA-05.02: Prevent unsafe command construction |
| ZTA-06 | Trusted-host versus untrusted-client isolation | ZTA-06.01: Prevent enforcement boundary bypass | ZTA-06.02: Verify delegated host guarantees |
| ZTA-07 | Credential and secret handling | ZTA-07.01: Prevent improper credential exposure | ZTA-07.02: Protect secret lifecycle |
| ZTA-08 | Dependency and supply-chain integrity | ZTA-08.01: Establish dependency and artifact provenance | ZTA-08.02: Verify build and distribution integrity |
| ZTA-09 | Evidence logging and provenance | ZTA-09.01: Produce attributable tamper-detectable evidence | ZTA-09.02: Preserve historical lineage |
| ZTA-10 | Failure handling and fail-closed behavior | ZTA-10.01: Deny uncertain unauthorized operations | ZTA-10.02: Bound timeouts resources and partial failure |
| ZTA-11 | Network and interprocess trust | ZTA-11.01: Identify external trust crossings | ZTA-11.02: Protect applicable IPC/network communications |
| ZTA-12 | Cross-platform security invariants | ZTA-12.01: Preserve security invariants across supported platforms | ZTA-12.02: Validate platform-specific mechanisms |

Each atomic control's eventual normative record MUST contain: objective; protected resource; threat hypothesis; applicability predicate; required/conditional criteria; required evidence; automated/manual verification procedure; failure and uncertainty predicates; default severity and context adjustment; accountable remediation component; external mappings and version.

## Proposed profile taxonomy

- `zta.library.v1`: library/SDK and consumer boundary; untrusted inputs, inert behavior, provenance and explicit delegated responsibilities.
- `zta.cli-hosted.v1`: CLI and declared trusted-host execution; authorization handoff, provider trust, replay, process isolation and fail-closed conditions.
- `zta.service.v1`: API/web service; authentication, sessions, data access, resource-level authorization, network transport.

Profiles share catalog definitions and may compose explicit overlays. If inheritance introduces incompatible requirements, reject the assessment rather than choosing a weaker requirement. A primary profile is required. A target manifest must declare `target_id`, immutable `revision`/artifact digest, `profile_id`, `resources[]`, `actors[]`, `trust_boundaries[]`, `components[]`, `capabilities[]`, `control_responsibilities[]` and `evidence_manifest`. Contradictions between declared and observed capabilities remain findings.

## Operation proposal — not registered

```yaml
id: gc-audit.zta
verb: zta
category: repo-audit
status: planned
mutates: false
profileRequired: true
targetRequired: true
assessmentContract: gc-audit.zta-assessment.v1
evidenceContract: gc-audit.zta-evidence.v1
outputContract: gc-audit.zta-result.v1
networkFetch: forbidden-by-default
```

No arbitrary target code execution, dependency installation, network access, credential access, remediation, or target mutation is authorized by an assessment. Behavioral evidence can be generated by separately authorized CI/test systems; this operation evaluates bounded submitted artifacts and provenance.

## Proposed versioned record types

1. `gc-audit.zta-controls.v1`: atomic catalog definitions.
2. `gc-audit.zta-profile.v1`: applicability, inheritance and control requirements.
3. `gc-audit.zta-target.v1`: revision-bound target/trust-boundary manifest.
4. `gc-audit.zta-evidence.v1`: evidence ID, source reference/hash, producer identity, timestamps, observation type, revision binding and limitations.
5. `gc-audit.zta-result.v1`: per-control dispositions, findings, provenance references, normalized assessment digest.
6. `gc-audit.zta-risk-decision.v1`: authorized human decision, scope, rationale, expiry/review trigger and residual risk.
7. Historical amendments: **owned by GC-AUDIT-AMD-001**, not a separately redefined ZTA amendment schema.

Evidence, finding, and release decision are separate. An integrity hash alone does not authenticate a producer. Canonical evaluation inputs are catalog, profile, manifest, evidence, and policy versions; timestamps belong in a separate envelope where needed so logical digests remain deterministic. Invalid evidence, mismatched revision, stale provenance or insufficient behavioral proof cannot produce PASS.

## Result and release semantics

- `PASS`: applicable control met with sufficient, validated evidence.
- `FAIL`: verified violation of an applicable control.
- `UNVERIFIED`: applicable but evidence missing, stale, insufficient or unresolved.
- `NOT_APPLICABLE`: specifically justified, evidence-supported profile exclusion.
- **EVALUATION_ERROR** is separate from control outcomes for malformed input, unsupported version or inconsistent assessment definitions.

Findings have Critical / High / Medium / Low severity based on actual threat, likelihood and impact, with documented context; missing evidence is not falsely characterized as an exploited vulnerability. Critical and High violations block unconditional release; UNVERIFIED mandatory authorization/enforcement boundaries also block. Medium/Low findings require remediation or explicit authorized risk disposition. Accepted risk does **not** rewrite a FAIL into PASS. A release decision is a separate governed action.

## Read-only assessment lifecycle

1. Validate schema and supported versions.
2. Resolve immutable target and its explicit resources, actors, capabilities and trust boundaries.
3. Expand the profile, apply applicability predicates, and reject unsupported exclusions.
4. Validate evidence integrity, producer, scope, revision and freshness.
5. Evaluate individual controls with explicit sufficient-proof and negative predicates.
6. Emit machine-readable normalized findings and reproducible digest.
7. Derive release eligibility under human-authorized policy, without changing findings.

Reassess relevant domains when authorization, providers, inputs, secrets, dependencies, network/IPC, operating-system support or profile schemas change. A release candidate requires current evidence for all applicable mandatory controls. Original PLAY.jsonl and audit results remain immutable; corrections and historical revalidation belong to GC-AUDIT-AMD-001 and must append rather than overwrite.

## Responsibility separation

Governance Commons defines catalog, profiles, evidence and release contracts. GC-AUDIT implements read-only assessment. Targets supply verifiable boundary assertions and application proof. Trusted hosts own authentication, authorization, execution privileges and persistent audit where delegated. The owner approves applicability and risks. Delegation alone must never produce PASS, and a CLI library must not be forced to invent host services it cannot correctly own.

## Adversarial acceptance matrix (future implementation)

Tests must cover: existing ZT1–ZT8 regression; registry discovery and version rejection; secure fixture PASS; injected authorization bypass FAIL; missing host authorization UNVERIFIED and release block; unjustified exclusion error; justified no-network NOT_APPLICABLE; hash mismatch and wrong-revision rejection; conflicting evidence visibility; deterministic identical results; read-only filesystem/network behavior; invalid risk authority rejection; append-only historical integrity; Windows/Linux/macOS invariants when declared supported. Include negative fixtures to measure false-negative behavior and independent review.

## Proposed implementation gates — NOT AUTHORIZED

- 001A: complete atomic control and profile specification.
- 001B: versioned schemas and evaluation semantics.
- 001C: read-only evaluator with adversarial fixtures.
- 001D: reporting/release integration and amendment compatibility.
- 001E: independent review and owner acceptance.

The present document is the **draft design deliverable**, not completion of these gates.

## Unresolved before contract freeze

1. Define exact applicability predicates, evidence sufficiency, failure rules and severity for each of 24 controls.
2. Specify fields and validation invariants for all record contracts, including version compatibility.
3. Establish proof limits for delegated host enforcement and manually attested claims.
4. Review GC-AUDIT implementation constraints without duplicating weak regex-based assurances in the new assessor.
5. Complete contradiction review and obtain owner acceptance for the frozen version.

## Deferred

Runtime enforcement service, cloud identity system, universal OS sandbox, mandatory signing infrastructure, automatic scanning/remediation, continuous monitoring and comprehensive penetration testing are outside v0.1 unless separately approved. Cockpit-specific remediation remains outside this repository milestone.

## Governance / development discipline

Per GC-DD-01 / OBDD, prioritize the approved deliverable, require evidence, and classify additional work as BLOCKER, REQUIRED or DEFERRED. This draft preserves the specification in Git without claiming an implemented audit or prematurely authorizing Codex development.
