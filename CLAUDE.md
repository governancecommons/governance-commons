# CLAUDE.md — Agent Onboarding for governance-commons

This file is read automatically at session start. Follow all rules below before acting.

---

## What this repo is

`governance-commons` is the portable standards layer for the eco ecosystem.
It contains GC: canonical governance standards (CANON, ONS, agent dossier, agent team
protocol, agent matrix, agent roster) that are adopted by eco and other conformant systems.

Do not make eco-specific changes here. GC standards must remain portable and ecosystem-agnostic.

## Canonical planning docs — read in order

1. `DEV-PATH.md` — phase history and decision record (append-only)
2. `DEV-PLAN.md` — current execution plan
3. `TRACKS.md` — workstream overview
4. `passes/` — accepted PASS records (GC: canonical IDs per CANON.03)

## Key rules

- **Append-only docs**: `DEV-PATH.md` and `passchangelog.md` are append-only. Do not rewrite them.
- **Do not rename files** without explicit instruction.
- **Do not delete queued work** — append to `DEV-PLAN.md` under `## QUEUED IDEAS` instead.
- **PASS IDs**: all GC PASSes use `GC:NNNN` canonical IDs per CANON.03. See `passes/passes.registry.json`.
- **Namespace**: this repo owns the `GC:` namespace. `ECO:` IDs belong in the eco repo.

## Tooling compliance (non-negotiable)

Enforced by `anti_stall.lint_compliance` in
`agent-project-orchestrator/governance/multi-agent.yaml` (`fix_dont_narrate` rule).
Narrating why a warning is acceptable is a violation. Fix it in the same output.

**MD060 — Markdown table separators**
All table separator rows must use `| --- | --- |` format. Compact (`|---|`) and long-dash
(`|------|`) formats are both violations.
Fix: `'| ' + ' | '.join(['---'] * col_count) + ' |'` — apply to the whole file.

If you produce a markdown table and the separator is wrong, fix it before moving on.
Do not commit files with MD060 violations.
