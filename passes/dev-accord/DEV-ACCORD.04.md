# DEV-ACCORD.04 — Agent Bootstrap Standard

**PASS ID:** DEV-ACCORD.04
**Canonical ID:** GC:2012
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-28T00:00:00Z
**Depends on:** GC:2008 (DEV-ACCORD.00), GC:2011 (DEV-ACCORD.03)

---

## Summary

DEV-ACCORD.04 defines the standard bootstrap contract for agents operating in
GC-conformant repositories.

The standard separates two ideas that must not be confused:

- **Normative GC requirement:** what a GC-conformant agent or adapter must read
  before acting.
- **Platform behavior:** what a specific runtime happens to auto-discover.

GC defines the former. Vendor runtimes may or may not implement the latter.

---

## Standard bootstrap file

Every GC-conformant repository MUST provide an `AGENTS.md` file at the repository
root.

`AGENTS.md` is the canonical cross-agent bootstrap file. It MUST point to the
repository's canonical agent onboarding authority, such as
`governance-commons/passes/dev-accord/DEV-ACCORD.03.md` for this portfolio.

`AGENTS.md` MUST NOT contain duplicate governance doctrine when a governed
onboarding authority exists. It is a bootstrap pointer, not the authority itself.

---

## Agent-specific adapter files

Agent-specific files MAY exist when a platform requires or benefits from a
runtime-specific filename.

Examples:

| Runtime or host | Adapter file | Status under this standard |
| --- | --- | --- |
| Claude Code | `CLAUDE.md` | permitted adapter |
| ChatGPT / Codex-style hosts | `AGENTS.md` | canonical bootstrap |
| GitHub Copilot | `.github/copilot-instructions.md` | permitted adapter |
| Cursor | `.cursorrules` or successor project rule file | permitted adapter |
| Gemini / local LLM runners | host-defined | permitted adapter |

Adapter files MUST contain only:

1. A pointer to `AGENTS.md` or the canonical onboarding authority.
2. Runtime-specific mechanics that cannot live in the shared standard.

Adapter files MUST NOT contain independent portfolio governance, reading order,
authority rules, or project-specific doctrine. Those belong in the canonical
onboarding authority.

---

## Conformance rule

An agent or host claiming GC conformance MUST satisfy one of these paths before
taking action in a repository:

1. Read `AGENTS.md` directly.
2. Read a runtime adapter file that points to `AGENTS.md`.
3. Read a runtime adapter file that points directly to the canonical onboarding
   authority declared by `AGENTS.md`.

If none of those paths is available, the agent MUST ask the user for the
bootstrap context before modifying files.

---

## No auto-discovery overclaim

This standard does not assert that all agent platforms automatically read
`AGENTS.md`.

Instead, it defines `AGENTS.md` as the normative GC bootstrap file. Runtime
support is a platform behavior and must be documented separately from the GC
requirement.

Correct claim:

> GC-conformant agents read `AGENTS.md` before acting.

Incorrect claim:

> All agents automatically read `AGENTS.md`.

---

## Bootstrap hierarchy

The preferred hierarchy is:

```text
AGENTS.md
  -> canonical onboarding authority (for this portfolio: DEV-ACCORD.03)
       -> execution model (DEV-ACCORD.02)
       -> project registry and planning docs
```

Runtime adapters point into that hierarchy. They do not own it.

---

## Validation contract

A GC bootstrap validator SHOULD check:

1. `AGENTS.md` exists at repository root.
2. `AGENTS.md` points to the canonical onboarding authority.
3. Runtime adapter files, if present, point to `AGENTS.md` or the canonical
   onboarding authority.
4. Runtime adapter files do not duplicate governance doctrine.
5. Any claim about auto-reading is scoped to a verified runtime, not universal.

Validation warnings:

- Missing runtime adapter for a known active host.
- Adapter contains substantial governance content instead of a pointer.
- Adapter references a stale or missing onboarding authority.

Validation errors:

- Missing `AGENTS.md` in a repository claiming GC bootstrap conformance.
- Conflicting reading orders across bootstrap files.
- Universal auto-discovery claims not backed by runtime-specific evidence.

---

## Relationship to DEV-ACCORD.03

DEV-ACCORD.03 defines the portfolio onboarding content: reading order, portfolio
rules, ecosystem overview, and planning doc roles.

DEV-ACCORD.04 defines how agents find that content.

Together:

- DEV-ACCORD.03 answers: "What must an agent know before acting here?"
- DEV-ACCORD.04 answers: "How does an agent reliably find that authority?"

---

## Cluster invariants

DEV-ACCORD-CI-6 — `AGENTS.md` is the GC bootstrap file
Every GC-conformant repository MUST provide root-level `AGENTS.md`.

DEV-ACCORD-CI-7 — Platform adapters are not governance authorities
Runtime-specific files MAY point to the bootstrap authority but MUST NOT own
portfolio governance.

DEV-ACCORD-CI-8 — Runtime behavior is not universalized
Standards text MUST distinguish normative GC requirements from verified
platform auto-discovery behavior.

---

## Outputs

- `AGENTS.md` declared as the canonical GC cross-agent bootstrap file.
- Agent-specific bootstrap files defined as adapters.
- Auto-discovery overclaim prohibited.
- Validation contract established for future bootstrap validators.

---

## Reversibility

Reversing this standard requires a future DEV-ACCORD PASS that supersedes
DEV-ACCORD.04, declares a replacement bootstrap file name or mechanism, and
provides migration rules for existing `AGENTS.md` and adapter files.
