# GC-DD-01 — Outcome-Bound Development Directive

**Version:** 1.1.0<br>
**Status:** ACCEPTED<br>
**Authority:** Jesse Ervin, owner and authorized approver; established GC governance and mandatory security controls retain precedence<br>
**Approved:** 2026-10-24<br>
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

## Amendment GC-DD-01-RP-002 — Resource protection and delegation control (2026-10-28)

**Owner-directed corrective amendment.** Applies to agents preparing delegation instructions as well as agents executing them. It preserves the directive's existing approval, security, and adoption boundaries.

### Least-cost delegation gate

Before transferring any work to Codex, Work, another agent, or a metered execution environment, the delegating agent MUST:

1. Identify the exact approved deliverable, acceptance criteria, and the operations requiring the destination environment.
2. Perform feasible research, standards review, specification, acceptance planning, and prompt preparation in the already available lower-cost environment.
3. Remove completed, exploratory, duplicated, speculative, and unrelated tasks from the delegated assignment.
4. Delegate the smallest independently verifiable execution change. A comprehensive prompt is not evidence of necessary scope.

If the work can reasonably be completed without metered delegation, the agent MUST NOT delegate it merely for convenience or completeness. The delegating agent is accountable for unnecessary work included in its instructions, even if the executor follows them exactly.

### Owner-authorized resource envelope

Every metered delegation MUST have an explicit owner-authorized resource envelope: allowed objective and tools, limits on time/credits/tokens/cost where supported, retry and subagent limits, and stop conditions. Unspecified limits do not constitute unlimited authority. The agent MUST disclose any limit that the platform cannot reliably measure or enforce; prompt-only instructions MUST NOT be presented as hard enforcement.

"Go," "continue," "proceed," and "finish" authorize only work within the existing approved scope and envelope. Only the owner can expand either. Classification as BLOCKER or REQUIRED does not grant additional spending authority.

### Execution and stop discipline

Agents MUST NOT autonomously expand milestones, launch recursive investigations, add optional refactoring or hardening, or continue improving an accepted deliverable. Verification MUST be the minimum sufficient for the approved acceptance criteria and mandatory security controls, without omitting required checks.

The executor MUST stop at the earliest of: accepted deliverable complete; resource envelope exhausted; next action outside authorized scope or authority; unresolved blocker within remaining limits; or no remaining justified acceptance work. On stop, preserve inspectable partial results and report completed work, remaining acceptance gaps, usage if observable, evidence, and deferred work. Reverification must not erase historical evidence.

### Delegation-design incident handling

If a handoff unnecessarily consumes scarce execution resources, record it as a **delegation-design failure**, not solely an executor failure. Preserve useful outputs and identify the smallest correction. A corrective proposal does not authorize another execution run or receive an automatic resource budget.

This amendment does not establish a new runtime, audit engine, monitoring service, or external platform-level budget enforcement. Existing mandatory security controls, owner acceptance, repository adoption, and release approvals remain authoritative.
