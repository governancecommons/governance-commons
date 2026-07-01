# DEV-ACCORD.07 — Planning Container Lock

**PASS ID:** DEV-ACCORD.07
**Canonical ID:** GC:2015
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-30T00:00:00Z
**Depends on:** GC:2010 (DEV-ACCORD.02), GC:2014 (DEV-ACCORD.06)
**Amends:** DEV-ACCORD.02 (GC:2010) — clarifies that PASS is not a structural planning container

---

## Summary

DEV-ACCORD.02 listed PASS alongside Phase, Wave, and Track in a flat vocabulary table,
implying they are the same kind of thing. They are not.

Phase, Wave, and Track are structural planning containers — they answer where work sits
in the roadmap. PASS is a governance contract — it answers what was agreed and what done
means. PASS may span multiple Tracks or Waves; it is not contained by the planning
hierarchy.

This PASS declares the planning container lock and separates PASS from the structural
planning vocabulary.

---

## Structural Planning Containers

These are the only three GC structural planning containers:

| Term | Answers | Role |
| --- | --- | --- |
| Phase | What era is the project in? | Macro arc of the project — preserved in DEV-PATH.md |
| Wave | What delivery batch within this phase? | Sequences work inside a phase |
| Track | What persistent workstream owns this? | Parallel lanes — CLI, schema, UI, runtime, release, docs |

Phase contains Waves. Tracks run parallel within and across Waves. There are exactly
three structural planning containers. A fourth requires a GC amendment before use.

---

## PASS is a Governance Contract, Not a Planning Container

PASS answers: did we agree to this? what does done mean? is it closed?

PASS is not nested inside Phase, Wave, or Track. A PASS references one or more Tracks
and anchors to a Wave, but it is not contained by them — it may span multiple Tracks
or multiple Waves when the work requires it.

Treating PASS as a fourth planning layer alongside Phase/Wave/Track is non-conformant
with this PASS.

---

## Cluster Invariants

**DEV-ACCORD-CI-17 — PASS is a governance contract, not a planning container**
PASS is not a structural planning container alongside Phase, Wave, and Track. Docs and
agents that list PASS as a planning layer in the same category as Phase/Wave/Track are
non-conformant.

**DEV-ACCORD-CI-18 — Exactly three structural planning containers**
Phase, Wave, and Track are the only GC-recognized structural planning containers. No
agent or project instruction file may introduce a fourth without a GC amendment.

---

## Outputs

- Planning container lock declared: Phase, Wave, Track — exactly three
- PASS declared as governance contract, not a planning container
- Cross-cutting nature of PASS declared: may span multiple Tracks or Waves
- Two new cluster invariants: DEV-ACCORD-CI-17, DEV-ACCORD-CI-18
- DEV-ACCORD.02 flat vocabulary table clarified
