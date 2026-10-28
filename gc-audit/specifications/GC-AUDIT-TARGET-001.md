# GC-AUDIT-TARGET-001 — Universal Assessment Targets

Status: Proposed owner-approved direction; implementation gated separately.
Date: 2026-10-28
Related: GC-AUDIT-PRODUCT-001, GC-AUDIT-CKP-001, GC-AUDIT-ZTA-001, OBDD.

## Purpose

GC-AUDIT remains an internal governed-development capability and becomes a portable, independently useful assessment tool. It must support authorized external repositories, public websites, applications, APIs/services, AI agents and multi-agent systems through target adapters. The existing Git-based CLI is the first adapter, not the universal model. External users need not adopt Governance Commons, Cockpit or an AI provider.

## Separate assessment surfaces

A source repository supplies revision, source and configuration evidence, but does not establish deployed application security. An application needs behavioral evidence for its authorization, identity and execution requirements. Deployment assurance additionally needs trusted operational observations. Public website checks provide bounded visible accessibility, interaction and configuration observations. AI agent and multi-agent audits inspect delegation, oversight, tool permissions and evidence continuity. These scopes must never be silently conflated.

## Versioned target descriptor

Specify target identifier and type; owner/authorized operator; source, build, test, staging, production or public-observation surface; locator and exact revision or endpoint identity; requested domain profiles and applicability; allowed and forbidden collection methods; permissions and authorization expiry; evidence provenance, time, digests, producer verification and limitations. The trusted host must enforce authority separately from target-supplied data.

## Multi-domain audit semantics

Share registry, evidence, reporting, guidance and human approval infrastructure. Keep each domain's methods and assurance separate: ZTA needs verified enforcement evidence; A11Y needs criterion-specific automated and human review; HCI heuristic findings must not be presented as observed user outcomes; agent governance needs corroboration of authority and behavior. Repository security is distinct from application ZTA. Missing evidence remains UNVERIFIED. AI advisers can guide, explain and recommend, but cannot authenticate their own findings or authorize consequential changes.

## Security and usability contract

Default read-only, offline and least-privilege. Public observations are non-intrusive; authenticated or active tests require specific authorization and environment controls. Declare network, data handling and side effects before execution. Results show target, exact scope, methods, status, provenance, uncertainties and actionable next steps. Canonical exports and verification must distinguish integrity digests from authenticated attestations.

## Bounded implementation order

1. Preserve and separately complete PR #12 as the honest Git repository CLI pilot; 24 UNVERIFIED controls are not an application ZTA verdict.
2. First application-level ZTA pilot: identify portal-kit's actual app and authorization boundaries; use an authorized isolated test environment; verify selected behavioral controls using independent evidence. If the app cannot be exercised, report that as a blocker rather than manufacturing PASS.
3. First non-intrusive website pilot: provide limited A11Y/HCI observations with accurate manual-review requirements and no full-conformance claim.
4. Defer general-purpose adapters for further platforms, automated modification, hosted service and broad compliance certification until justified by real pilot demand.

## Acceptance gates

A new user can select an external target, understand the supported assessment scope, complete a safe authorized run, inspect evidence and export/reopen results. Adapter and domain contracts are versioned and tested. Repository-only observations cannot certify runtime controls; website automated checks cannot certify full accessibility or user experience. Supported platforms, authorization, no-mutation defaults, tampering resistance and relevant negative tests are verified. Owner review and explicit approval are required before release or operational assurance.

## Internal preservation

Inside Governance Commons, the same core must guide planning, design, implementation, testing, verification and recording across ZTA, A11Y, HCI and other governed audits. The portable product extends, rather than forks or removes, that functionality. Cockpit is an optional consumer. New work is BLOCKER, REQUIRED or DEFERRED under OBDD; do not expand the first pilot into an unbounded product rebuild.
