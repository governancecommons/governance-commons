# GC-AUDIT Gap Analysis

**Date:** 2026-07-01  
**Scope:** `governance-commons/gc-audit/`, registry validation profile, and DEV-ACCORD.05 GC-AUDIT declarations.

## Summary

GC-AUDIT has the right ownership shape: authoritative scripts live in GC, callers are expected to discover tools from `GC-AUDIT-REGISTRY.yaml`, and DXP package registry validation fails closed until schema authority exists.

The remaining gaps are mostly contract drift between the registry, scripts, and standards:

- mutating scripts are dry-run capable but still apply by omission instead of requiring explicit `-Apply`
- one validation script exposes a mutating switch
- some active scripts/wrappers are not registry-addressable
- `SCRIPTS.md` is referenced but missing
- the registry has no self-audit that checks its own allowlist, script paths, mutation contracts, and docs pointers
- several scripts spawn PowerShell child processes even though the registry security model says shell execution is forbidden
- there is no repeatable test suite for GC-AUDIT edge cases such as path containment and malicious registry paths
- Change Playbook execution levels are commit-enforced, but GC-AUDIT does not yet audit whether every agent session declared a play before work or updated local DEV-DOCS after the play

## Method

This analysis uses the portfolio 12-question framework from `docs/gap-analysis-framework.md`, plus the Stranger Test:

> Can a stranger install this, run it, produce evidence, verify that evidence, and trust the release artifact?

For GC-AUDIT, the answer is currently **not yet**. A portfolio insider can run the tools, but a new user cannot yet discover every command contract, get structured evidence, verify mutation safety, or trust release provenance without reading implementation details.

## 12-Question Robust Gap Pass

| Question | GC-AUDIT finding | Closure state | Priority |
| --- | --- | --- | --- |
| Q1 Regulatory Compliance | GC-AUDIT does not yet map validation/evidence outputs to EU AI Act Article 12 logging, Article 13 transparency, GDPR retention/data subject rights, or NIST AI RMF evidence expectations. | open | P1 |
| Q2 Standards Compliance | No SLSA/SBOM/provenance contract for GC-AUDIT releases; no RFC 2119-style command contract; no formal JSON result schema for conformance tooling. | open | P1 |
| Q3 De Facto Standards | No GitHub Actions/GitLab CI wrapper, no OpenTelemetry/CloudEvents emission, no standard JSON output for app/CLI integration. | open | P1 |
| Q4 Industry Best Practice | No continuous self-audit of the allowlist registry, no fault-injection fixtures, and no mutation safety gate that fails if normalizers apply by omission. | open | P0 |
| Q5 Security Posture | Zero-trust intent exists, but threat model coverage is incomplete: child shell delegation, mutating validation switches, path containment tests, and script allowlist self-validation remain gaps. | spec-complete | P0 |
| Q6 Operational Maturity | There is no runbook for failed validators, no common diagnostic artifact, no stable machine-readable exit/finding contract, and no recovery guidance for partial normalization. | open | P1 |
| Q7 Developer Experience / Adoption Friction | `SCRIPTS.md` pointer is stale inside GC, command discovery depends on reading YAML, normalizers do not have a clear preview/apply UX, and install/use docs are not stranger-proof. | open | P0 |
| Q8 Ecosystem Interoperability | Cockpit, Marlin, and DCP can call scripts, but GC-AUDIT lacks a stable operation API contract for TypeScript/Node callers, CI systems, IDEs, or remote runners. | open | P1 |
| Q9 Organizational / Process Maturity | DEV-ACCORD.05 declares ownership, but the implementation table is stale and there is no maintenance process for registry changes, new operations, deprecation, or Change Playbook play declaration before agent work. | spec-complete | P1 |
| Q10 Documentation / Discoverability | Registry, profile docs, and REVIEW-GRAMMAR exist, but the actual script reference is missing and wrappers/internal tools are not classified. | open | P0 |
| Q11 Testing Strategy | No fixture-based regression suite exists for malicious paths, missing registry docs, dry-run/apply behavior, DXP fail-closed behavior, validation mutation prevention, or Change Playbook/DEV-DOCS compliance. | open | P0 |
| Q12 Ahead of the Curve | The category-defining move is governance diff + audit replay for GC-AUDIT: replay a past RUN/commit against current GC rules and show what would pass, warn, or fail. | open | P2 |

## Stranger Test Breakdown

| Capability | Current state | Gap |
| --- | --- | --- |
| Install GC-AUDIT | Available as repo scripts, not packaged. | Needs package/install surface or Marlin-managed install contract. |
| Run GC-AUDIT | Scripts run locally and registry lists operations. | Needs a stable command adapter and script reference. |
| Produce evidence | Console output exists. | Needs structured evidence output and optional signed bundle. |
| Verify evidence | Exit codes exist for most validators. | Needs schema, provenance, and reproducible fixture tests. |
| Trust artifact | Source is pushed to main. | Needs release provenance, SBOM, and self-validation of registry allowlist. |

## Quick Audit: Change Playbook and DEV-DOCS

Current DEV-ACCORD.06 behavior:

- every commit must carry `Change-Level: BUNT | RUN | DRIVE | PASS`
- the agent determines the execution level before committing
- DEV-DOCS update obligations vary by execution level
- `DRIVE` and `PASS` require DEV-DOCS updates
- `BUNT` and some `RUN` changes may use `Dev-Docs: not-needed` with a reason

Gap:

- the standard does not yet require a pre-work declaration of the current play
- the standard does not yet define `PLAY` as the session/work-unit declaration that maps to BUNT, RUN, DRIVE, or PASS
- GC-AUDIT does not yet validate whether local DEV-DOCS were updated after every play
- GC-AUDIT does not yet distinguish "commit trailer present" from "agent declared the play before acting"
- the user/agent responsibility boundary is implicit: DEV-ACCORD.06 says agents determine the level, but it does not say when the user must authorize or override that determination

Approved direction:

- Agents should propose and declare the play before work starts.
- The user should authorize upgrades, ambiguity, or governance-sensitive cases, especially `PASS`, cross-project work, branch/split recommendations, or authority changes.
- Every play should end with a DEV-DOCS check. If DEV-DOCS are not updated, the agent should explicitly record why the local DEV-DOCS did not need an update.
- If the desired policy is "always update local DEV-DOCS after every play," DEV-ACCORD.06 needs an amendment because the current accepted rule allows `Dev-Docs: not-needed` for BUNT and some RUN changes.

Recommended GC-AUDIT addition:

- add a Change Playbook/DEV-DOCS validator that audits recent commits and local planning docs together
- validate that each recent commit has a Change-Level trailer
- validate that DRIVE/PASS commits touched relevant DEV-DOCS
- warn when RUN commits alter project truth without DEV-DOCS updates
- support a future `PLAY` record once DEV-ACCORD defines where that declaration lives

## P0 Gaps

### 1. Explicit apply is not enforced by normalizers

**Current state:** `gc-audit.normalize` declares `requiresExplicitApply: true`, and normalizer steps declare `supportsDryRun: true`. The normalizer scripts apply changes when `-DryRun` is omitted.

**Why it matters:** This is not preview-first in a zero-trust command surface. A caller omission can mutate files.

**Recommended fix:** Add `-Apply` to each normalizer and make the default behavior preview-only. Reject `-Apply -DryRun` together.

Affected scripts:

- `gc-audit/tools/normalize-bootstrap.ps1`
- `gc-audit/tools/normalize-planning.ps1`
- `gc-audit/tools/normalize-pointers.ps1`

### 2. Validation surface contains a mutating option

**Current state:** `validate-pointers.ps1` is registered as non-mutating validation, but it exposes `-FixNotes`.

**Why it matters:** A validation verb must be read-only. This breaks the registry's `mutates: false` contract.

**Recommended fix:** Remove or deprecate `-FixNotes` from `validate-pointers.ps1`; route that behavior through `normalize-pointers.ps1 -Apply`.

### 3. GC-AUDIT registry has no self-validation

**Current state:** `GC-AUDIT-REGISTRY.yaml` is authoritative, but no validator checks the registry itself.

**Why it matters:** Cockpit, Marlin, DCP, and agents rely on this registry as the allowlist. If it drifts, callers inherit bad command surfaces.

**Recommended fix:** Add `validate-gc-audit-registry.ps1` or extend `validate-registry.ps1` with `-Profile gc-audit`.

Checks should include:

- every registered script path resolves under the declared containment root
- every active tool has at least one step
- every planned tool has no runnable steps
- `mutates: true` tools require explicit apply
- dry-run support in registry matches script parameters
- no validate operation exposes mutating switches
- docs pointers resolve, including `SCRIPTS.md`
- unregistered scripts are either intentionally private helpers or registered

### 4. Change Playbook PLAY and DEV-DOCS audit is missing

**Current state:** DEV-ACCORD.06 defines BUNT, RUN, DRIVE, and PASS execution levels and says the agent determines the execution level before committing. It does not define a pre-work `PLAY` declaration, and GC-AUDIT does not yet audit whether local DEV-DOCS were updated after every play.

**Why it matters:** Commit trailers are after-the-fact evidence. The portfolio needs a before/during/after loop: declare the play, perform the work, update or explicitly exempt DEV-DOCS, validate, then commit.

**Recommended fix:** Audit DEV-ACCORD.06 and decide whether to amend it so every agent session declares a `PLAY` mapped to BUNT/RUN/DRIVE/PASS before work starts. Add a GC-AUDIT validator for Change Playbook and DEV-DOCS compliance.

Open policy questions:

- Is `PLAY` a new official term, or just a human-friendly alias for `Change-Level`?
- Does the agent always declare the play, or does the user authorize the play before work starts?
- Should every play update local DEV-DOCS, or should BUNT/RUN exemptions remain valid when explicitly justified?
- Where does a pre-work PLAY declaration live: session transcript, RUN record, DEV-DOCS, commit trailer, or evidence bundle?

## P1 Gaps

### 4. Missing script reference document

**Current state:** `GC-AUDIT-REGISTRY.yaml` references `SCRIPTS.md`, but no `SCRIPTS.md` exists in the GC repo.

**Why it matters:** The registry's docs pointer is stale and callers do not have a script-level reference contract.

**Recommended fix:** Create `gc-audit/SCRIPTS.md` or update the registry pointer to an existing doc. Prefer `gc-audit/SCRIPTS.md` so the reference stays inside the owning toolchain directory.

### 5. Active scripts not registered as operations

**Current state:** The following scripts exist but are not directly registry-addressable:

- `gc-audit/tools/dev-status.ps1`
- `gc-audit/tools/review-last-24h.ps1`

**Why it matters:** DEV-ACCORD.05 says callers must discover runnable operations from the registry. Useful wrappers should either be registered or explicitly marked internal.

**Recommended fix:** Register `dev-status.ps1` under `repo-status`. Either register `review-last-24h.ps1` as a compatibility wrapper or mark it private/internal in `SCRIPTS.md`.

### 6. Shell-forbidden model is underspecified against child PowerShell calls

**Current state:** Some GC-AUDIT scripts spawn `pwsh` or `powershell` to call other allowlisted scripts.

Examples:

- `validate-registry.ps1` delegates DCP validation through `powershell`
- `validate-recent-work.ps1` invokes validators through `pwsh`
- `review-last-24h.ps1` invokes `validate-recent-work.ps1` through `pwsh`

**Why it matters:** The registry says `shell: forbidden`, but internal delegation is not clearly separated from arbitrary shell execution.

**Recommended fix:** Define a stricter rule:

- external callers must not execute through a shell
- internal GC-AUDIT delegation may only invoke allowlisted scripts by resolved path
- no string-built shell commands
- child process use must be portable across Windows PowerShell and PowerShell 7, or avoided

Then update implementation to match the rule.

### 7. DEV-ACCORD.05 implementation table is stale

**Current state:** DEV-ACCORD.05 declares initial GC-AUDIT implementations, but newer scripts are not reflected there.

Missing or changed surfaces include:

- `validate-git-split.ps1`
- `validate-registry.ps1`
- normalizers
- `dev-status.ps1`
- `review-last-24h.ps1`

**Why it matters:** The registry is operational authority, but the PASS text is the standard authority. Drift between them makes it harder for agents and apps to know which source to trust.

**Recommended fix:** Append a DEV-ACCORD.05 amendment stating that `GC-AUDIT-REGISTRY.yaml` is the current executable allowlist and the table is historical/bootstrap unless amended.

## P2 Gaps

### 8. No structured output contract

**Current state:** Most scripts print human-readable console output. Cockpit, Marlin, and DCP menus will need stable machine-readable results.

**Recommended fix:** Add common `-Json` or `-OutputFormat json` support for validators and reports, with a shared result schema:

- status
- errors
- warnings
- findings
- checked paths
- profile or operation id
- exit code semantics

### 9. No regression test suite for GC-AUDIT behavior

**Current state:** Validation is mostly manual/script execution. There are no fixture-based tests for malicious registry paths, missing docs pointers, mutating switch detection, or dry-run/apply behavior.

**Recommended fix:** Add a small test harness under `gc-audit/tests/` with isolated fixtures. Pester is a natural fit for PowerShell, but a simple PowerShell test runner is enough for Phase 1.

Minimum tests:

- registry path escape is rejected
- absolute registry path is rejected
- network registry URL is rejected
- DXP profile fails closed
- normalizers do not mutate without `-Apply`
- validation scripts expose no mutating switches
- registry self-validation catches missing script docs

### 10. DXP package registry schema remains undefined

**Current state:** DXP validation intentionally fails closed.

**Recommended fix:** Define the package/tool registry schema before implementing DXP validation. Keep install-source, command, version, dependency, and audit/status surfaces explicit rather than inferred.

## Suggested Repair Order

1. Add GC-AUDIT registry self-validation.
2. Add Change Playbook/DEV-DOCS audit, including the proposed PLAY declaration question.
3. Change normalizers to require `-Apply`; default to preview.
4. Remove mutating behavior from validation scripts.
5. Create `gc-audit/SCRIPTS.md` and classify every script as registered, wrapper, or internal.
6. Register or intentionally mark `dev-status.ps1` and `review-last-24h.ps1`.
7. Clarify shell-forbidden/internal-delegation rule and update child process calls.
8. Add fixture tests for zero-trust path containment and mutation safety.
9. Append DEV-ACCORD.05/06 amendments for registry authority and PLAY/DEV-DOCS policy if approved.
10. Add JSON output contract.
11. Define DXP package/tool registry schema.

## Zero-Trust Position

GC-AUDIT is aligned in intent, but not yet fully aligned in enforcement. The highest-risk gap is mutation safety: validation must never mutate, and normalization must never apply by omission. The next highest-risk gap is lack of self-validation for the allowlist registry itself.

Until those are fixed, Cockpit, Marlin, and DCP callers should treat GC-AUDIT as authoritative but should invoke mutating operations only with explicit human authorization and should prefer read-only validation surfaces.
