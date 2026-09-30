# GC Ecosystem Relationship Taxonomy

**Status:** Research / documentation taxonomy
**Non-normative**

## Purpose

This vocabulary gives Governance Commons a consistent way to describe how GC relates to external standards, protocols, organizations, research programs, and open-source projects.

It prevents a directory entry from silently becoming an endorsement, dependency, certification, or authority claim.

## Relationship labels

### REFERENCE
GC considers the work relevant enough to link, explain, or index.

Does not imply adoption, endorsement, compatibility, or affiliation.

### ALIGN
GC intentionally uses compatible terminology, concepts, requirements, or design patterns.

### INTEROPERATE
A concrete technical relationship exists or is being evaluated.

Evidence should include an implementation, fixture, test, protocol binding, or explicit interoperability statement.

### CROSSWALK
GC maps concepts between two systems.

A crosswalk should distinguish equivalent, partially overlapping, complementary, different scope, unresolved, and not equivalent.

### ADOPT
GC deliberately relies on an external specification or artifact instead of defining a duplicate GC mechanism.

Record the exact external specification/version and reason for adoption.

### CONTRIBUTE
GC has a candidate contribution that may be useful to an external community.

CONTRIBUTE does not mean the external project has accepted it. Acceptance must be documented separately.

### RESEARCH
The relationship is under investigation. This is the default when evidence is insufficient for a stronger claim.

### WARN
GC has identified a documented limitation, risk, ambiguity, conflict, stale reference, or implementation hazard.

Warnings must identify evidence and avoid turning an unresolved concern into a categorical conclusion.

### DISTINGUISH
GC documents a meaningful difference in scope, semantics, authority, evidence model, lifecycle, or implementation.

## Status language

Use:

- **Documented** — directly supported by a primary source or verified implementation evidence.
- **Observed** — supported by an artifact or implementation inspection but not necessarily normative.
- **Interpretation** — GC's analysis of documented material.
- **Proposal** — a possible future GC or ecosystem action.
- **Unresolved** — evidence is insufficient to decide.
- **Not verified** — GC has not established the claim.

Avoid words such as best, leading, authoritative, complete, first, or universal unless explicitly attributed to a source and necessary for context.

## Required ecosystem metadata

| Field | Requirement |
| --- | --- |
| Source | Primary source preferred |
| Version | Exact version/revision when applicable |
| Date | Publication or verification date |
| Scope | What the source actually covers |
| GC relationship | One or more taxonomy labels |
| Evidence | What supports the statement |
| Status | Documented, observed, interpretation, proposal, unresolved, or not verified |
| Next action | Adopt, align, crosswalk, research, contribute, warn, or none |

## Core Commons rule

> **No relationship label grants authority to either side.**

GC may document another project's authority within that project's own scope while preserving the distinction between:

**who says something → what evidence supports it → what the evidence establishes → what remains interpretation.**
