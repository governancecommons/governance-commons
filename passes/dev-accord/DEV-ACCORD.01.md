# DEV-ACCORD.01 — Planning Document Standard: ONS Registration

**PASS ID:** DEV-ACCORD.01
**Canonical ID:** GC:2009
**Cluster:** DEV-ACCORD
**Authority:** AL:2
**Status:** ACCEPTED
**Timestamp:** 2026-06-27T00:00:00Z
**Depends on:** GC:2008 (DEV-ACCORD.00)

---

## Summary

Registers the four canonical planning document types declared by DEV-ACCORD.00 in the
ONS namespace, making them first-class named artifacts in the portfolio's naming
governance system.

---

## What this PASS does

1. Adds the `portfolio_doc_name` casing domain to `ons.yaml` — `DEV-UPPER-KEBAB` pattern
   (`^DEV-[A-Z]+(?:-[A-Z]+)*$`). Covers DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS and
   any future `DEV-` doc type admitted under DEV-ACCORD authority.

2. Adds the `portfolio` namespace domain to `ons.yaml` — covering portfolio-level planning
   and documentation artifacts. Registry required; default registry is
   `governance-commons/ons/registry/doc-types.yaml`.

3. Creates `ons/registry/doc-types.yaml` — the canonical doc type registry. Registers
   all four types with their `portfolio.planning.*` canonical names, casing domain, role,
   and governing PASS reference.

---

## Registered doc types

| Name | Canonical Name | Role |
| --- | --- | --- |
| DEV-PATH | portfolio.planning.dev-path | Phase history, decisions, PASS registry (append-only) |
| DEV-PLAN | portfolio.planning.dev-plan | Current execution state, active milestones, work queue |
| DEV-RELEASE | portfolio.planning.dev-release | Release contracts — what ships, conditions, downstream unlocks |
| DEV-TRACKS | portfolio.planning.dev-tracks | Parallel workstreams and dependencies |

---

## Constraints introduced

- Any new `DEV-*` planning doc type MUST be registered in `ons/registry/doc-types.yaml`
  before use across the portfolio.
- Canonical names follow the `portfolio.planning.{name}` pattern using lowercase dot-hierarchy.
- The `portfolio_doc_name` casing domain is the sole conformant casing pattern for `DEV-*`
  planning doc filenames; no other separator or case variant is permitted.

---

## Files changed

| File | Change |
| --- | --- |
| `governance-commons/ons/ons.yaml` | Added `portfolio_doc_name` casing rule; added `portfolio` namespace domain |
| `governance-commons/ons/registry/doc-types.yaml` | Created — canonical doc type registry |
| `governance-commons/passes/passes.registry.json` | Added GC:2009 entry |
| `governance-commons/passes/passes.registry.changelog.jsonl` | Appended create action |
| `governance-commons/passchangelog.md` | Appended GC-PASS-0011.00 |
