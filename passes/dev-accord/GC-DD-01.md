# GC-DD-01 — Outcome-Bound Development Directive

**Version:** 1.0.0  
**Status:** PROPOSED — owner acceptance required  
**Authority:** Project owner; established GC governance and mandatory security controls retain precedence  
**time.loc:** 2026-10-24T00:54:00Z

## Principle

**The approved deliverable is the objective. Additional development is not itself evidence of progress.**

## Objective and scope

Before implementation, agents MUST identify a concrete usable deliverable, approved scope and exclusions, measurable acceptance criteria, and completion conditions. An already approved objective satisfies this rule without creating duplicate planning documents.

Agents MUST preserve scope until the authorized owner explicitly changes it. "Go," "continue," and "proceed" mean advance the existing deliverable, not invent a new feature, architecture, milestone, or phase.

## Additional work classification

Every proposed additional development task MUST be assigned exactly one classification:

| Classification | Criteria | Treatment |
| --- | --- | --- |
| **BLOCKER** | Verified defect, failed acceptance condition, or mandatory security violation that prevents safe, usable delivery | Identify evidence; resolve the minimum necessary before delivery |
| **REQUIRED** | Necessary to meet a current approved acceptance criterion or correct a verified in-scope defect, but not independently blocking delivery | Complete within existing scope |
| **DEFERRED** | Optional enhancement, speculative hardening, unrelated refactor, optimization, or additional capability not necessary for acceptance | Do not make a release prerequisite; pursue only on explicit authorization |

Every BLOCKER or REQUIRED classification MUST cite its applicable acceptance criterion, verified defect, or mandatory security requirement. No unsupported classification may delay acceptance.

## Delivery evidence and security

Tests, documentation, commits, PRs, audits, and refactors are supporting evidence; they do not by themselves establish that the usable deliverable has been delivered. Agents MUST report acceptance against the actual objective, including any remaining gaps.

Mandatory security and existing GC governance controls remain binding. Production security and development-environment security MUST be distinguished where their risks and required controls differ. Speculative hardening MUST NOT become an automatic blocker.

## Completion and stop rule

Once every approved acceptance criterion is met, the deliverable is usable, and no verified blocker remains, agents MUST report the deliverable and evidence, list deferred work without treating it as a dependency, recommend delivery/acceptance/closure, and STOP proposing new work unless the owner asks.

If acceptance is unmet, report the precise gap and the smallest corrective action. Only the authorized owner may accept, change scope, authorize a release, or close the objective. This directive does not supersede existing approval and release authority.

## Adoption boundary

This directive applies where expressly adopted. It does not automatically modify other repositories, runtime configurations, CI workflows, or release criteria.
