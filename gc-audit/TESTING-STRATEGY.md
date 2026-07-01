# GC-AUDIT Testing Strategy

**Status:** active
**Authority:** DEV-ACCORD.05 / GC-AUDIT
**Updated:** 2026-07-01

This document defines testing terminology in the context of GC-AUDIT, explains why
each validator exists, and describes the fixture approach for the regression suite.

---

## Testing Vocabulary

### Project context

| Term | Meaning in GC-AUDIT context |
| --- | --- |
| Greenfield testing | Testing a new validator or operation against a clean scaffold repo with no prior governance state. Used when writing a new script to confirm it handles the happy path before encountering real-world drift. |
| Brownfield testing | Testing against an existing portfolio repo with real governance history, partial compliance, and accumulated drift. The primary mode for GC-AUDIT fixture tests — real repos are the target, so tests must reflect real conditions. |

### Testing approach

| Term | Meaning in GC-AUDIT context |
| --- | --- |
| Black-box testing | Validate a script by its inputs and outputs only — exit code, stdout patterns, and file mutations — without relying on internal implementation details. GC-AUDIT fixture tests are black-box: they call scripts as a caller would and assert the result. |
| White-box testing | Validate a script by inspecting its internals — variable state, function calls, branching logic. Useful for unit-testing individual helper functions inside a validator, but not the primary GC-AUDIT approach. |
| Regression testing | Confirm that a previously-passing check still passes, and that a previously-detected violation is still detected. GC-AUDIT regression fixtures prove the suite does not silently stop catching known violations after a script is modified. |
| Fault injection | Deliberately introduce a bad governance state — missing PASS, escaped path, mutating switch in a validator, empty order-token — to verify the script detects and reports it correctly. The primary technique for testing GC-AUDIT validators. |
| Smoke test | A Level 1 `gc-audit validate` run. Confirms that all validators execute without crashing and return a result. Does not prove deep coverage — it proves the toolchain is alive. |

---

## Why Each GC-AUDIT Test Is Necessary

| Validator | Why it exists | Silent failure mode if skipped |
| --- | --- | --- |
| `validate-bootstrap.ps1` | Ensures every repo routes agents to DEV-ACCORD.03 before they act. | Agents in new or cloned repos have no governance context; they read nothing and act on stale assumptions. |
| `validate-planning.ps1` | Ensures DEV-DOCS use canonical file names and are present where expected. | Planning doc naming drift accumulates silently; agents and tools look for `DEV-PLAN.md` and miss `dev-plan.md`. |
| `validate-pointers.ps1` | Ensures every planning file pointer in `projects.yaml` resolves on disk. | Dead pointers send callers to 404s; the portfolio registry claims files exist that don't. |
| `validate-review-grammar.ps1` | Ensures REVIEW-GRAMMAR is present and adopted in each repo. | Agents use informal verbs; command vocabulary diverges across repos and sessions. |
| `validate-debt.ps1` | Detects TODO/FIXME/STUB/TBD markers in planning docs and source. | Technical debt signals accumulate invisibly; a PASS file marked STUB passes review as if complete. |
| `validate-git-split.ps1` | Ensures no unauthorized branch, PR chain, worktree, or fork has been created. | DEV-ACCORD.10's single-branch publish default is bypassed silently; split authority decisions happen without human authorization. |
| `validate-ci-invariants.ps1` | Ensures DEV-ACCORD-CI invariant IDs are unique across all markdown. | Duplicate CI IDs make cluster invariants ambiguous; agents cannot determine which rule governs a conflict. |
| `validate-agent-preflight.ps1` | Confirms the agent declared and completed the GC agent-trail reading sequence before acting. | Work starts without governance context; the agent operates on assumptions rather than current portfolio state. |
| `validate-zero-trust.ps1` | Audits the zero-trust posture of GC-AUDIT itself — path containment, mutation safety, allowlist coverage, shell delegation, fail-closed defaults. | Mutation leaks into validators silently; shell delegation creeps in; allowlist registry drifts without detection. |
| `validate-registry.ps1` | Validates the GC PASS registry, DCP projects.yaml, and (future) DXP package registry for internal consistency. | Registry entries diverge from PASS files; Canonical IDs become unreliable; callers trust a registry that no longer reflects reality. |

---

## Fixture Approach (P2-2)

GC-AUDIT tests use a **brownfield black-box** strategy:

- Tests call scripts as a caller would (via PowerShell invocation with arguments).
- Tests assert exit codes and stdout patterns — not internal state.
- Fixture repos are minimal real-governance-shaped directories, not mocked objects.
- Each fixture targets one specific violation or valid state.

Minimum fixture set:

| Fixture | What it tests |
| --- | --- |
| `path-escape/` | Registry path with `../` — must exit 1 |
| `absolute-path/` | Registry path starting with `C:\` — must exit 1 |
| `network-url/` | Registry path starting with `https://` — must exit 1 |
| `dxp-fail-closed/` | DXP profile — must exit 1 with "fail closed" message |
| `normalizer-no-apply/` | Normalizer called without `-Apply` — must not mutate any file |
| `mutating-switch-in-validator/` | Synthetic validator with `-Fix` switch — `validate-zero-trust` must detect it |
| `missing-order-token/` | `AGENT-PREFLIGHT.md` without `order-token:` line — preflight must exit 1 |
| `valid-preflight-complete/` | Valid `PREFLIGHT: complete` stamp — must exit 0 |
| `valid-preflight-blocked/` | Valid `PREFLIGHT: blocked` stamp — must exit 0 |
| `duplicate-ci-id/` | Two markdown files declaring the same `DEV-ACCORD-CI-9` — must exit 1 |

Fixture location: `governance-commons/gc-audit/tests/`

Test runner: Pester (preferred) or a plain PowerShell runner if Pester is not available.
Each test file is named after its fixture: `path-escape.Tests.ps1`, etc.
