# Governance Commons — Charter

**AUTHORITY LEVEL: AL:3**
**Status:** ACTIVE
**Established:** 2026-06-05

AL:3 entries are inviolable invariants. They can only be changed by the founding maintainer and
require a new GC-CHARTER entry in this file. AL:2 decisions (ecosystem plan) and AL:1 decisions
(per-repo devpaths) operate within the constraints set here, not above them.

---

## GC-CHARTER-001 — Founding Maintainer

**jj-ervin** (Jess Ervin) is the founding maintainer of Governance Commons.

AL:3 decisions require founding maintainer approval. There is no other mechanism for changing
charter entries while the project is pre-public-governance. A steering committee or working group
structure, when established (target PASS-5), will define how AL:3 authority is delegated.

---

## GC-CHARTER-002 — Licensing

All Governance Commons specifications, schemas, tooling, and documentation are licensed under
**Apache License 2.0** unless explicitly stated otherwise in a sub-repo's LICENSE file.

Contributions to Governance Commons repos imply the contributor grants a license under Apache 2.0.
No contributor license agreement (CLA) is currently required. This will be revisited at PASS-5
when the public release train and GitHub org are established.

---

## GC-CHARTER-003 — Project Name and Namespace

The canonical project name is **Governance Commons**. The canonical domain is **governancecommons.org**.

- All schema `$id` URLs MUST use the `governancecommons.org` base domain
- The GitHub organization MUST be `governancecommons` when created
- Per-standard subdomains (`agent-dossier.org`, etc.) redirect to `governancecommons.org/{standard}/`
- No third party may use the name "Governance Commons" to describe a competing or incompatible
  standard without prior written consent from the founding maintainer

---

## GC-CHARTER-004 — Standard Independence

Each Governance Commons standard (agent-dossier, agent-matrix, ONS, agent-project-orchestrator)
is independently versioned and independently releasable. No standard requires another to
release in lock-step.

GC ecosystem release milestones (e.g., GC v1.2.0) are informational pinning contracts for adopters.
They do not gate or block any standard's own release cadence.

This invariant (DDR-2 at AL:2) is promoted to AL:3 because collapsing standard independence would
require migrating all standards and all adopters simultaneously — a class of change that cannot be
undone without breaking the ecosystem.

---

## GC-CHARTER-005 — Reference, Not Inherit

Governance Commons standards reference each other; they do not inherit from each other.

A standard may declare a `compat:` constraint naming a minimum version of a peer standard, but
it MUST NOT embed or reproduce normative content from a peer standard's source files. Cross-standard
references use published schema `$id` URIs and git tag pins. This ensures each standard can be
adopted independently without pulling in the full ecosystem.

---

## Appendix: Authority Level Summary

| Level | Who | Scope | Change mechanism |
| --- | --- | --- | --- |
| AL:3 | Founding maintainer only | Charter invariants (this file) | New GC-CHARTER-NNN entry |
| AL:2 | GC project maintainer | Ecosystem plan, compatibility constraints, release milestones | GC-PASS entry in passchangelog.md |
| AL:1 | Spec owner | Per-repo devpath, architecture, release cadence | Repo-level PASS entry in spec's passchangelog.md |
