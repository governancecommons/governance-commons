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
2. Change normalizers to require `-Apply`; default to preview.
3. Remove mutating behavior from validation scripts.
4. Create `gc-audit/SCRIPTS.md` and classify every script as registered, wrapper, or internal.
5. Register or intentionally mark `dev-status.ps1` and `review-last-24h.ps1`.
6. Clarify shell-forbidden/internal-delegation rule and update child process calls.
7. Add fixture tests for zero-trust path containment and mutation safety.
8. Append DEV-ACCORD.05 amendment for registry-vs-table authority.
9. Add JSON output contract.
10. Define DXP package/tool registry schema.

## Zero-Trust Position

GC-AUDIT is aligned in intent, but not yet fully aligned in enforcement. The highest-risk gap is mutation safety: validation must never mutate, and normalization must never apply by omission. The next highest-risk gap is lack of self-validation for the allowlist registry itself.

Until those are fixed, Cockpit, Marlin, and DCP callers should treat GC-AUDIT as authoritative but should invoke mutating operations only with explicit human authorization and should prefer read-only validation surfaces.
