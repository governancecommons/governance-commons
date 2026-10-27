# GC-AUDIT-PRODUCT-001 — Portable, Evidence-First Audit Product Charter

Status: PROPOSED FOR OWNER ACCEPTANCE — documentation only  
Date: 2026-10-27  
Owner: Governance Commons maintainer  
Initial release target: GC-AUDIT v0.1  
Related: GC-AUDIT-ZTA-001, GC-AUDIT-CKP-001, GC-DD-01 / OBDD

## Outcome and user

Make GC-AUDIT usable by a developer outside Governance Commons to assess an authorized local application or repository, understand what is verified versus unknown, receive actionable guidance, and export evidence that another person can inspect. Success is a completed real-user workflow, **not** a collection of schemas, passing synthetic fixtures, or an AI-generated compliance claim.

Initial users: individual developers and small engineering teams. First profile: application-level Zero Trust Architecture (ZTA). GC-AUDIT is an assessment engine, **not** a Zero Trust enforcement product or certification authority.

## v0.1 deliverables and boundaries

1. **Portable core and CLI:** versioned assessment input, profile, findings, and results; local read-only target selection; documented command; deterministic fail-closed outcomes; offline operation without AI. Implement one real external-target assessment before UI work.
2. **Evidence and assurance:** provenance including exact target revision/scope, methods, hashes, verification status, authority provenance, freshness/expiration, limitations, and reproducible export. Evidence from an assessed target cannot establish its own independent authority.
3. **Human-readable findings:** severity, source, controls, reasons, status, uncertainty, recommended next action; a minimal local read-only viewer only after the CLI pilot acceptance gate.
4. **AI advisory adapter:** optional provider-neutral assistance for explanation, prioritization, suggested tests, and remediation drafts. Advice never overrides deterministic evaluator outcomes and cannot independently approve, release, or mutate.
5. **Interoperability:** documented import/export adapters and at least one existing-scanner integration. Prefer established formats when appropriate (SARIF findings, SPDX/CycloneDX inventories, SLSA/in-toto provenance), rather than inventing replacements.

No managed multi-tenant SaaS, autonomous production changes, broad vulnerability scanner, multiple fully supported domains, blanket compliance certification, or unrestricted tool execution in v0.1.

## Authority and execution architecture

Separate interfaces (native CLI; optional Cockpit adapter; later UI/API), trusted host (identity, scopes, policy, clock, isolation, evidence sourcing), deterministic evaluator, evidence collectors/adapters, and optional AI advisers. The assessed repository, assessment input, tool outputs, and model output are untrusted. The host must source and enforce trusted authority independently. No network access or mutation by default. Explicit human grants govern consequential actions. Audit machinery self-audit is **conditional on assurance claims that depend on tool integrity**, not mandatory for each exploratory scan; its status and limitations must be reported accurately. The trusted release/assurance path may require current engine/registry integrity evidence.

Present PASS, FAIL, UNVERIFIED, EVALUATION_ERROR distinctly. Missing or unverifiable proofs never imply PASS. Verified negative evidence takes precedence under the relevant control policy. No generic "compliant" or ELIGIBLE label without authenticated scope, complete required coverage, applicable risk/authorization gate, and actual evidence. AI suggestions and scanner claims remain advisory until verified.

## User journey

Discover/select local authorized target → choose profile/scope → preview collection/side effects → run allowed checks → inspect PASS/FAIL/UNVERIFIED results and supporting evidence → ask optional AI for explanations/remediation drafts → separately authorize any action → independently retest → export inspectable report and decision record.

The UI should make five answers immediate: what was assessed, what was verified, what failed, what is unknown, and what action is possible. Use progressive disclosure, plain-language labels, keyboard navigation, accessible status indicators, transparent permission prompts, and no misleading score that hides uncertainty.

## Acceptance matrix

| ID | Verifiable acceptance requirement |
| --- | --- |
| GC-P01 | A new user can install and launch from documented instructions in a clean environment. |
| GC-P02 | Select and scope a real, authorized external local repository without editing GC-internal governance files. |
| GC-P03 | Read-only execution is tested, including no mutation and no implicit network calls. |
| GC-P04 | PASS / FAIL / UNVERIFIED / EVALUATION_ERROR and their precedence have positive, negative, and adversarial regression tests. |
| GC-P05 | A pilot user can explain the principal finding and its evidentiary limitations using the interface/report. |
| GC-P06 | Findings show grounded next steps with no automatic authorization. |
| GC-P07 | Export, reopen, and verify an evidence report with target, revision, scope, catalog and manifest integrity. |
| GC-P08 | Spoofed/caller-controlled trust roots, digests, policies, time or roles cannot produce a trusted assurance PASS. |
| GC-P09 | The deterministic workflow works offline and without an AI service. |
| GC-P10 | Optional AI mock/provider test proves advice is separate from assessment and cannot change authority. |
| GC-P11 | Windows/Linux/macOS supported paths pass hosted compatibility checks, with skips and environment limits documented. |
| GC-P12 | One actual external-target pilot with captured steps, test evidence, defects and corrected outcome. |
| GC-P13 | UI (when included) targets WCAG 2.2 AA with automated **and** manual keyboard/screen-reader checks. |
| GC-P14 | Approval boundaries demonstrably prevent unauthorized consequential changes and agent self-approval. |

Evidence must be tied to exact tested commits/versions. A passing CI matrix alone is insufficient for user acceptance or real-system security assurance.

## Quality / standards mapping policy

Keep a versioned mapping of objective → applicability → evidence requirement → verification method → result → standard clause/source/date. Label mappings as law (only if jurisdiction/role applies), normative standard requirement, voluntary guidance, GC policy, or advisory. No claim of certification from a mapping alone.

- ZTA: NIST SP 800-207/207A; CISA Zero Trust Maturity Model.
- Application and development security: NIST SP 800-218 SSDF; SP 800-53 families; OWASP ASVS.
- Software supply chain: SLSA, in-toto, Sigstore/OpenSSF as applicable.
- AI risk/security: NIST AI RMF; ISO/IEC 42001 and 23894; applicable OWASP LLM/agentic security guidance.
- Human-centered quality: ISO 9241-210; ISO/IEC 25010; WCAG 2.2.
- Regulatory obligations (EU AI Act, GDPR, NIS2, etc.) require product, actor, jurisdiction and effective-date analysis; do not imply universal applicability.

Quality attributes: security (independent roots, fail-closed), usability (guided and inspectable), desirability (measured pilot outcomes), serviceability (modular adapters, diagnostics, migration/version policies), portability (local/offline, OS matrix, self-host-first), domain extensibility (versioned separate profiles), privacy (minimal collection, consent before AI data sharing), reliability (deterministic engine, repeatable evidence).

## Delivery sequence and exit gates

**Gate 0 — Security prerequisite:** close demonstrated GC-AUDIT-ZTA-001 adversarial failures. PR #9 and its follow-on remediation remain separately governed; do not fold this product scope into PR #9. False assurance and registry/trust-boundary defects block trusted use.

**Gate 1 — Externally usable CLI:** real authorized target, read-only profile invocation, structured result and verifiable export, clean install and adversarial checks. This is the first independently useful artifact.

**Gate 2 — Interaction and integration:** minimal local viewer, one scanner adapter, optional AI **advisory-only** integration, accessibility verification.

**Gate 3 — Adoption:** stranger/pilot test, collect task-completion, time-to-first-assessment, comprehension, severe interpretation errors, and remaining defects. Fix only verified blockers. Owner explicitly accepts release.

One user must be able to install, assess, locate evidence, distinguish unknown from PASS, understand a recommendation, and export/reopen the report without maintainer intervention. No stage auto-authorizes the next.

## Multi-domain preservation and internal governed-repository use

**Normative architecture decision:** GC-AUDIT remains a first-class, reusable Governance Commons capability for governed-repository development, including planning, implementation guidance, code/configuration inspection, authorized verification, evidence recording, and approval workflows. Portable distribution is an **additional consumer** of the same authoritative audit capabilities, not a replacement, fork, or extraction that disables the internal functions.

The shared framework must be multi-domain: an audit registry, common evidence/provenance and reporting contracts, versioned profile discovery, applicability decisions, results, human review and AI-advisory interfaces. **Each domain** must independently specify its catalog, target boundaries, applicability, methods, evidence strength, statuses and limitations; a general shared framework does **not** imply that all methods or PASS criteria are interchangeable.

Audit families and boundaries (registration/implementation is not asserted for proposed names):

| Family | Role | Status/assurance boundary |
| --- | --- | --- |
| Existing GC audit operations, including registry and workflow/governance checks | Preserve current internal validation and guided coding workflows | Inventory and actual registration must be verified in repository before expanding or renaming operations. |
| `gc-audit.zerotrust` | Existing ZT1–ZT8 audit of GC tooling/registry posture | Not comprehensive application-level Zero Trust verification. |
| `gc-audit.zta` | Application-level Zero Trust architecture assessment | Separately developed under GC-AUDIT-ZTA-001, gated on independently trusted evidence; current implementation/activation gaps remain. |
| `gc-audit.a11y` (proposed) | Accessibility tests and review, with WCAG applicability | Automated test results do not establish full accessibility conformance; human evaluation is required where relevant. |
| `gc-audit.hci` (proposed) | Interaction quality, usability, information architecture and human-centered evaluation | Heuristic expert findings are distinct from observed user behavior; claims about user outcomes require appropriate empirical evidence. |
| Additional versioned domains | Security, software quality, agent governance and future profiles | Require separate acceptance and authoritative methods before advertised as supported. |

Internal governed development may select applicable guidance and checks by objective, change set, risks and governing policy across **all** supported audit families: plan → develop → inspect → explain/recommend → independently verify → record. AI advisers may propose checks, improvements and bounded automation but cannot convert recommendations into verified results or approve their own changes. Self-audit remains conditional on the assurance claim and host policy, not compulsory for every advisory code review.

**Same-engine contract:** internal GC operations, the native portable CLI, optional Cockpit adapters, and eventual apps consume the same versioned implementations and domain-specific control semantics. No duplicated internal/external engine, silent change in evaluation criteria, or weakening of existing GC functionality for commercialization. Backward compatibility and migration rules must be documented.

**Release sequencing:** ZTA remains the **first external pilot**, not the sole or permanent product domain. A11Y and HCI progress as independent audit development tracks with their own review and evidence gates; they are **not** made required implementations for the GC-AUDIT v0.1 ZTA pilot. Domain architecture and preservation are required now; broad feature completion is explicitly DEFERRED. This amendment does not authorize new operations, code changes, deployments, PR merges or activation.

## Future compatibility without current scope expansion

Later: explicit patch proposal and sandboxed test automation; human-approved PR drafting; governed multi-agent workflows with role/capability grants, independent retest and revocation; multiple domain profiles (agent security, HCI, accessibility), optional hosted services and enterprise integrations. All require separate demand/evidence and owner authorization.

## References and dependencies

GC-AUDIT-CKP-001 defines the **optional** Cockpit CLI/GUI/Tab interaction adapter. The core/CLI must remain fully usable without Cockpit. Existing Agent Dossier, Agent Matrix, ONS, OBDD, and append-only governance records can inform agent permissions and audit traceability but are not execution permissions by themselves.

**Completion rule:** stop when the approved deliverable and evidence are satisfied; classify new work BLOCKER, REQUIRED or DEFERRED. Do not create successive architecture phases as a substitute for working product delivery.
