# AGENT PREFLIGHT

Status: active
Authority: DEV-ACCORD.03 agent-trail protocol
Scope: Governance Commons standard profile for GC-conformant agent sessions

This file is the canonical preflight contract for GC-governed sessions.
Portfolio root files may mirror or point here, but this is the authority source.

## Required Order (before edits, planning updates, or terminal actions)

1. AGENTS.md
2. governance-commons/passes/dev-accord/DEV-ACCORD.03.md
3. PROTECTED.md
4. DEV-CONTROL-PLANE.md
5. docs/REVIEW-GRAMMAR.md
6. governance-commons/passes/dev-accord/DEV-ACCORD.02.md
7. governance-commons/passes/dev-accord/DEV-ACCORD.06.md
8. governance-commons/passes/dev-accord/DEV-ACCORD.10.md
9. projects.yaml
10. Target project DEV-PATH.md
11. Target project DEV-PLAN.md

## Turn-Opening Contract

At the top of each working turn, post exactly one of the following:

PREFLIGHT: complete | project=<path> | order=AGENTS>03>PROTECTED>CONTROL-PLANE>REVIEW-GRAMMAR>02>06>10>projects.yaml>DEV-PATH>DEV-PLAN

PREFLIGHT: blocked | missing=<file list> | action=read missing files first

## Non-Compliance Rule

If work starts before preflight completion:
- Stop immediately.
- Disclose non-compliance plainly.
- Run full preflight in order.
- Resume only after posting PREFLIGHT: complete.

## Universal PLAY Closeout Rule

After every PLAY, every GC-conformant agent in every environment and platform
must include:

1. PLAY telemetry table: read, plan, execute, verify, close, and total duration.
2. Latest PLAY summary: play_id, repo, level, status, scope, DEV-DOCS result,
   commit reference when produced, and validation checks.
3. Next recommended logical step, or the specific blocker/authorization required.

This rule is universal GC behavior declared by DEV-ACCORD.06. It is not optional
and is not specific to one agent, shell, operating system, UI, or runtime.

## Project-Hop Rule

When switching repos in one session, re-read that repo's DEV-PATH.md and DEV-PLAN.md and post a fresh stamp.

## Canonical Order Token

This line is the machine-readable source of truth for the stamp order field.
`validate-agent-preflight.ps1` reads it to build the validation pattern dynamically.
Update this line when DEV-ACCORD.03 changes the agent-trail — the validator updates automatically.

```text
order-token: AGENTS>03>PROTECTED>CONTROL-PLANE>REVIEW-GRAMMAR>02>06>10>projects.yaml>DEV-PATH>DEV-PLAN
```

## Machine Validation

Use the GC tool implementation at:

governance-commons/gc-audit/tools/validate-agent-preflight.ps1

Compatibility adapter (portfolio root):

validate-agent-preflight.ps1
