# GC-AUDIT-ZTA-001 — v1.0 Acceptance Contract

**Contract version:** 1.0.0 (specification baseline)  
**Specification status:** FROZEN FOR IMPLEMENTATION; owner release acceptance and conformance remain separate  
**Implementation status:** NOT IMPLEMENTED; no audit PASS, certification, deployment, or release implied  
**Date:** 2026-10-27  
**Authority:** Governance Commons, GC-AUDIT-ZTA-001. Supersedes the provisional design decisions in `GC-AUDIT-ZTA-001-DRAFT.md` for this milestone only.

## 1. Objective, boundaries, non-goals

Deliver a reusable, deterministic, **read-only**, evidence-backed application-level Zero Trust assessment via `gc-audit.zta`. Preserve unchanged the existing `gc-audit.zerotrust` operation and ZT1–ZT8 tooling-posture semantics, existing playbook validation, and historical `PLAY.jsonl` data. Cockpit CLI is a reference **consumer** of the assessment, not an implementation dependency or a place to host GC security logic. The actual CKP-CLI-008 security audit and remediation belong in its separate repository/conversation.

This is an **assessment**, not runtime Zero Trust enforcement, automatic scanning of every vulnerability, penetration testing, external certification, or certification to NIST. Normative GC controls distinguish applicability from evidence sufficiency; third-party frameworks are informative mappings only. Apply NIST SP 800-207 (resource protection/access control), SP 800-218 (secure software development), CISA ZT Maturity Model (context), OWASP ASVS (app verification) and SLSA (artifact provenance) only where relevant. Do not assert that each GC control is mandated by a cited framework.

## 2. Roles and enforceable trust boundaries

GC owns catalog, profiles and audit policy. GC-AUDIT owns the read-only evaluator and reports. A target component owns its implementation claims. The trusted execution host owns authentication, authorization, policy enforcement, privileges and persistent execution audit **when delegated**. An evidence producer owns the veracity of observed/test artifacts; a verifier validates attribution, integrity, scope, relevance and sufficiency. A human owner approves risk decisions and releases. A user confirmation is **not** host authorization; a same-user local process split is **not** an OS sandbox. A delegation claim alone can never PASS.

Protected-resource inventory is mandatory: identify resources, allowed actors, interactions, execution capability, sensitive data, and boundary crossings. Contradictory discoveries are reported as gaps. Targets with no applicable capability may support N/A controls but must prove the absence of that capability through scope evidence.

## 3. Normative atomic controls

Each of the following is a separately assessed obligation. A .01 baseline applies if its stated capability/operation exists; .02 is conditional on the stated trigger. Every row supplies objective/threat, applicability predicate, accepted evidence class, verification/failure predicate, default failure severity, and remediation responsibility. Automated verification should use supplied signed/attributable CI tests or verified static fixtures as indicated; source review and system-boundary reasoning may require an accountable manual reviewer. Severity may be adjusted only with documented threat/impact reasoning, never to suppress the finding.

| ID | Control | Required objective / threat addressed | Applicability trigger | Required evidence (minimum) | FAIL if verified | Default severity | Remediation owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ZTA-01.01 | Actor attribution | All protected requests have actor kind and traceable asserted identity; verified identity is separately marked | protected operation exists | request/host actor mapping plus spoof test | Reject claims of verified identity from untrusted input | High | application or host |
| ZTA-01.02 | Identity verification | A component claiming authentication verifies a principal before protected access | authentication is performed | credential verifier tests and hostile identity fixtures | Unverified identity accepted as authenticated | High | authenticating component |
| ZTA-02.01 | Authorization enforcement | Policy decision precedes every privileged action at an enforceable boundary | privileged action exists | denial-path behavioral tests linked to revision | Execution permitted after deny or without decision | Critical | trusted enforcement host |
| ZTA-02.02 | Replay prevention | Reuse of expired, consumed, mismatched authorization cannot trigger new privileged action | authorizations/tokens are reusable inputs | replay and cross-operation negative tests | Replayed decision executes without fresh authorization | High | policy enforcement host |
| ZTA-03.01 | Capability allowlisting | Effective callable operations are explicit and bounded; unlisted operations fail closed | dispatch/execution exists | allowlist diff and unknown-command tests | Unlisted capability executes | High | dispatcher or host |
| ZTA-03.02 | Runtime privilege | Process and resource grants are limited to required operations | privileged OS/resource access exists | effective permissions and denial test | Unnecessary high-impact permissions are required or exploited | High | execution host |
| ZTA-04.01 | Provider registration | Providers have unique declared identity and cannot be silently replaced | plugin/provider registry exists | registration rules, duplicate and substitution tests | Undeclared or substituted provider resolves | High | provider registry |
| ZTA-04.02 | Provider origin | Executable providers are bound to verified origin or approved provenance | external or separately packaged provider loads | integrity checks and tampered-provider tests | Untrusted changed provider loads as approved | High | provider loader |
| ZTA-05.01 | Input validation | Untrusted names, parameters and serialized inputs are validated before action | untrusted inputs exist | negative schema/fuzz boundary cases | Undeclared or malformed input reaches action | High | input boundary owner |
| ZTA-05.02 | Injection isolation | Untrusted content cannot alter command/program structure | commands/queries/scripts are constructed | metacharacter and argument-boundary tests | Untrusted input changes executable structure | Critical | command builder or host |
| ZTA-06.01 | Enforcement non-bypass | Untrusted clients cannot reach protected execution around the designated enforcement point | client/host trust crossing exists | call graph and bypass negative tests | Direct untrusted bypass reaches privileged action | Critical | trusted host |
| ZTA-06.02 | Delegation proof | Delegated enforcement guarantees have a named component, contract and observed proof | security requirement delegated | host contract plus bound host test evidence | Delegation claimed as PASS without host proof | High | delegating integrator and host |
| ZTA-07.01 | Secret exposure | Credentials are not exposed through untrusted results, diagnostics or logs | secrets may be processed | redacted fixture/secret scan output samples | Secret material disclosed to unauthorized actor | High | secret-handling component |
| ZTA-07.02 | Secret lifecycle | Stored/transmitted secrets use appropriate access controls and are retired safely | target stores/transmits/manages secrets | storage access and lifecycle verification | Unauthorized access or plaintext disclosure at trust crossing | High | secret store or host |
| ZTA-08.01 | Component provenance | Distributed components and dependencies are inventoried and revision-linked | packaged/distributed artifact exists | lockfile/SBOM or equivalent package inventory and hashes | Unknown/unverifiable executable component represented as verified | Medium | build/release owner |
| ZTA-08.02 | Artifact integrity | Released artifact is consistently bound to intended source/build inputs | build or distribution exists | build outputs digest and installed-artifact checks | Artifact substitution or mismatch accepted | High | build/release owner |
| ZTA-09.01 | Evidence attribution | Security decisions/claims are linked to producer, revision, integrity and limitations | audit evidence is produced | evidence fixture and tampering tests | Unattributed/tampered evidence produces PASS | High | evidence producer and assessor |
| ZTA-09.02 | History integrity | Original assessments/records remain immutable; revalidation and corrections are separate linked events | governance records exist | append-only mutation tests | Historical record silently rewritten | High | governance record keeper |
| ZTA-10.01 | Fail closed | Missing, errored or denied authorization cannot turn into permitted privileged action | protected authorization is required | exception and absent-policy negative tests | Execution succeeds on uncertain/denied policy | Critical | execution enforcement owner |
| ZTA-10.02 | Failure bounds | Time, output, resource and interruption behavior is defined and tested | long-running/external operation exists | timeout/overflow/cancellation tests | Unbounded exposure or falsely reported rollback/success | Medium | operation executor |
| ZTA-11.01 | Trust-crossing inventory | Relevant network and IPC interfaces and trust assumptions are declared | network/IPC or external boundary exists | interface map plus discovery cross-check | Material external crossing omitted to excuse control | High | system integrator |
| ZTA-11.02 | Transport protection | Cross-boundary messages authenticate peers and protect integrity/confidentiality as needed | sensitive or privileged network/IPC transport exists | peer spoof/tamper tests and transport settings | Untrusted peer can issue privileged calls or intercept secrets | High | transport owner |
| ZTA-12.01 | Platform parity | Declared support platforms preserve security-denial and authorization invariants | multiple supported platforms declared | OS-specific equivalent negative tests | Supported OS permits unauthorized operation | High | application and host |
| ZTA-12.02 | Platform-specific hazards | Path/shell/process/encoding mechanics are validated per supported platform | platform-dependent mechanisms exist | symlink/case/path/process negative fixtures | Platform quirk bypasses required invariant | High | platform adapter |

**Verification sufficiency by class:** documentation alone cannot prove runtime authorization, least privilege, replay resistance, sandbox/isolation, injection safety, or cross-platform parity; behavioral negative tests or directly inspectable equivalent runtime enforcement are required. For static-only claims, revision-bound code inspection with a verifiable reviewer and reproducer may suffice. Manual assessments require reviewer identity, methodology, scope and limitations. Absence of proof yields UNVERIFIED; verified counterexamples yield FAIL even with contradictory favorable evidence. The auditor may not run arbitrary target code to collect missing proof.

## 4. Versioned profiles and applicability

- `zta.library.v1`: portable package/SDK; baseline 01.01, 05.01, 07.01, 08.01, 09.01, 10.01 and relevant other controls triggered by actual capability. Delegated host obligations remain UNVERIFIED if the profile explicitly requires host proof.
- `zta.cli-hosted.v1`: library baseline plus 02.01, 03.01, 05.02, 06.01, 06.02, 10.02 and 12.01 where execution and declared platforms apply; remaining controls use predicates.
- `zta.service.v1`: library baseline plus 01.02, 02.01, 02.02, 03.02, 07.02, 10.02, 11.01, 11.02 where authentication, service operation, secrets and transport exist.

These profile lists are **minimum explicit obligations**, not exhaustive exclusions: any control whose applicability predicate is satisfied must be evaluated regardless of whether enumerated in the profile. Profile inheritance is compositional; contradictory overlays fail evaluation. A profile cannot downgrade mandatory controls silently. No feature can be created merely to make a control applicable. Each exclusion must name the control, explain the absent capability and cite valid architectural evidence; invalid exclusions are evaluation errors, not NOT_APPLICABLE.

## 5. Normative wire contracts (JSON Schema Draft 2020-12)

Every JSON record has `schema` (exact discriminator), `version` (semantic major version 1), `id` (non-empty stable ID), no unknown top-level fields except namespaced `extensions`, and structural validation before evaluation. Arrays carrying sets have unique stable identifiers. Version 1 readers must reject unknown major versions; additive optional fields may appear only under an explicitly versioned extension namespace. Schemas must be published with test fixtures:

| Contract | Mandatory fields and invariants |
| --- | --- |
| `gc-audit.zta-controls.v1` | `schema,version,id,controls[]`; each control requires `control_id,objective,threats[],applicability,required_evidence[],verification,fail_predicate,severity,remediation_role,standard_mappings[]`; 24 distinct approved IDs, immutable catalog digest |
| `gc-audit.zta-profile.v1` | `schema,version,id,catalog_digest,profile_id,inherits[],mandatory_control_ids[],conditional_rules[],exclusion_rules[],policy_version`; no cyclic inheritance or conflicting predicates |
| `gc-audit.zta-target.v1` | `schema,version,id,target_id,revision,profile_id,resources[],actors[],trust_boundaries[],components[],capabilities[],control_responsibilities[],evidence_manifest_digest`; revision is immutable commit SHA or content digest; all referenced component/actor IDs resolve |
| `gc-audit.zta-evidence.v1` | `schema,version,id,evidence_id,target_id,revision,control_ids[],producer,source_refs[],source_digest,method,collected_at,environment,limitations[]`; `producer` distinguishes authenticated verified identity from asserted identity; evidence timestamps ISO-8601 with timezone; digest verified against available bytes |
| `gc-audit.zta-result.v1` | `schema,version,id,target_id,revision,profile_id,catalog_digest,policy_version,control_results[],findings[],normalized_digest,assessment_state`; every applicable required control has one of PASS, FAIL, UNVERIFIED, NOT_APPLICABLE, with evidence refs and explanation; no aggregate pass percentage |
| `gc-audit.zta-risk-decision.v1` | `schema,version,id,decision_id,assessment_digest,authority,scope,findings[],rationale,residual_risk,review_trigger,expires_at,decision`; decision never mutates control results and cannot claim validity beyond scope/expiry |

Historical evidence amendment events are governed **only** by GC-AUDIT-AMD-001. This contract defines references to amendment identifiers if present; it does not invent a second amendment authority or rewrite PLAY records. Signature infrastructure is optional in v1; evidence origin assurance must still be honestly represented and verified. A hash without trustworthy producer attribution establishes integrity comparison only.

## 6. Registry and evaluation contract

Register `gc-audit.zta` as a separate `repo-audit` operation with `mutates:false`, required target/profile/manifest, output `gc-audit.zta-result.v1`, and **no arbitrary script execution, dependency installation, secret reading, network access, artifact modification or auto-remediation**. Network reads are forbidden by default; externally collected evidence must arrive as bounded supplied data. Registration must preserve `gc-audit.zerotrust` and ZT1–ZT8 behavior.

Pipeline: (1) validate schemas/version (2) bind target to source revision/digest (3) resolve profile and capabilities/trust boundaries (4) validate applicability and exclusions (5) validate evidence integrity, identity claims, scope, freshness and revision (6) evaluate each atomic control using explicit predicates (7) render deterministic sorted control results, findings and digests (8) compute policy eligibility independently. **Input contract errors** such as malformed schema, cycles, mismatched catalogs and unsupported versions are EVALUATION_ERROR, not target FAIL. Findings require concrete evidence; missing proof yields UNVERIFIED.

Reproducibility: canonicalize JSON objects by stable key ordering, sorted set-valued arrays, and stable UTF-8 serialization; preserve semantically ordered arrays. Hash logical normalized inputs/results using SHA-256. Keep observation timestamps and volatile execution metadata in an envelope excluded from the normalized assessment digest. No implicit date/time/network-dependent evaluation; freshness comparisons require an explicitly supplied as-of timestamp bound into policy context.

## 7. Result semantics, severity, acceptance

`PASS` sufficient applicable verified proof; `FAIL` verified violation; `UNVERIFIED` missing/invalid/stale/contradictory evidence unresolved; `NOT_APPLICABLE` evidence-backed valid exclusion. Invalid input is `EVALUATION_ERROR` (operation failure) and cannot yield a successful release conclusion.

Findings classified Critical (credible catastrophic/uncontrolled execution impact), High (material bypass/escalation), Medium (bounded exploitable issue), Low (limited consequence/defense in depth); override needs recorded rationale. Verified Critical and High findings block unconditional release. Mandatory enforcement/authorization UNVERIFIED also blocks. Medium/Low must be remediated or dispositioned by identifiable authorized human acceptance with expiry and review trigger. No risk decision converts FAIL to PASS. Assessment state (`VALID`, `INVALID`) and release eligibility (`ELIGIBLE`, `BLOCKED`, `CONDITIONAL`) are distinct. `CONDITIONAL` means an authorized decision explicitly accepts remaining permissible risk and must never be presented as an unconditional pass. No automated risk acceptance.

## 8. Reassessment, history, compatibility

Reassess affected controls after changes to auth/policy, command/provider dispatch, untrusted input parsing, secrets, dependencies/artifact build, IPC/network, supported platform or audit catalog/profile. Each new release candidate requires current, revision-linked applicable-control evidence. Historical reports remain immutable; new validation is a new assessment and historical amendment uses GC-AUDIT-AMD-001. A security-sensitive source change invalidates evidence that is not shown to remain applicable to that revision. Existing v1 GC-AUDIT result/playbook contracts stay intact; adapter/wrapper integration cannot reinterpret historical status.

## 9. Required acceptance fixtures and release tests

| Test | Mandatory expected result |
| --- | --- |
| ZT1–ZT8 prior behavior | All unchanged behavior and prior golden tests pass |
| Registry discovery and version gating | One separate `gc-audit.zta`; unknown major/profile rejected |
| Valid secure fixture | Only supported, applicable controls PASS |
| Verified authorization bypass | ZTA-02.01 FAIL and release BLOCKED |
| Host authorization evidence absent | Required delegated control UNVERIFIED; release BLOCKED |
| Expired/replayed authorization | ZTA-02.02 FAIL when trigger applies |
| Untrusted command injection | ZTA-05.02 FAIL when exploit fixture succeeds |
| Provider replacement | ZTA-04.01/.02 FAIL when relevant boundary compromised |
| Verified no-network/no-IPC scope | Supported NOT_APPLICABLE for transport controls |
| Unjustified exclusion and hidden capability | EVALUATION_ERROR or explicit contradictory-scope finding; never PASS |
| Evidence tamper, wrong revision or forged provenance | Reject evidence; no PASS |
| Contradictory results | Counterexample retained; no false PASS |
| Same canonical inputs twice | Byte-identical logical results and digest |
| Read-only boundary test | Target tree and registry unchanged; no unauthorized network, write, process execution |
| Invalid risk authority and expired acceptance | Release BLOCKED; underlying FAIL unchanged |
| Windows/Linux/macOS declared support | Equivalent negative security invariants or UNVERIFIED, never synthetic PASS |
| Historical records | No mutation of PLAY or past assessments; append-only references |
| Failure behavior | Missing/invalid evidence yields UNVERIFIED; malformed contract yields EVALUATION_ERROR |

Independent reviewer must inspect test false-negative coverage, trace control-to-evidence-to-finding, review severity/application exclusions, and reproduce representative negative fixtures. Do not mark release-ready from green CI alone.

## 10. Definition of done and dependency gates

**SPECIFICATION DONE (this document):** all 24 controls, three profiles, schemas' required fields, status semantics, risk policy, lifecycle, boundaries and acceptance fixtures defined. This is a *design baseline only*.

**IMPLEMENTATION DONE (future and separately approved):** registry operation active; machine schemas present/validated; evaluator meets determinism/read-only contract; all required positive/negative fixtures and ZT1–ZT8 regression pass; independent review complete; docs provide real invocation, input/output examples and limitations; owner accepts specific release revision.

Implementation lanes: A contract freeze (this milestone), B machine-readable schemas, C read-only evaluator, D report/release integration, E adversarial/cross-platform verification and external review. GC-AUDIT-AMD-001 integration is a compatibility boundary, not a pretext to modify historical records. Cockpit CLI remediation and formal CKP-CLI-008 assessment remain separate.

Deferred: runtime ZT enforcement, continuous monitoring, cloud policy engines, mandatory signatures/HSM, dashboard, unattended pentesting, auto-remediation and enterprise compliance certification.

## 11. Design consistency decisions

1. Read-only evaluation accepts evidence generated by separately authorized systems; auditor itself never probes by executing target code.
2. No static/document-only PASS for behavioral host security guarantees.
3. Capability-based applicability prevents irrelevant controls and unearned exclusions.
4. Profile minimal sets cannot silently override catalog applicability.
5. Findings vs evidence vs human release decisions are distinct records.
6. Logical deterministic digest excludes volatile envelope fields.
7. Existing GC tooling ZT1–ZT8 and historical governance records are preserved.
8. No numerical conformance percentage; no unwarranted certification claim.

**Freeze scope:** changes to normative control meaning, wire fields, pass semantics, or release thresholds require a versioned contract amendment and owner decision. This freeze does **not** authorize implementation, represent test results, or declare v1.0 shipped.
