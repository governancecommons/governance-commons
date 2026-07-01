# DEV-ACCORD.08 — DEV-DOCS Privacy Default

**PASS ID:** DEV-ACCORD.08
**Canonical ID:** GC:2016
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-07-01T00:00:00Z
**Depends on:** GC:2011 (DEV-ACCORD.03), GC:2012 (DEV-ACCORD.04)
**Amends:** DEV-ACCORD.03 (GC:2011) — replaces the planning doc visibility table and private doc rule

---

## Summary

DEV-ACCORD.03 classified `DEV-PATH.md`, `DEV-PLAN.md`, `DEV-TRACKS.md`,
`DEV-RELEASE.md`, and agent bootstrap files as "public repo" visibility. That
classification was incorrect for a commercial product portfolio where those docs
contain private strategy, operating model, roadmap, and agent instructions.

This PASS establishes that DEV-DOCS are **private by default**. Public distribution
repos must exclude them via `.gitignore`. Canonical DEV-DOCS live in the local
working copy or a private control plane. An optional public-safe stub is defined for
bootstrap files in public clones.

The change is not a reversal of DEV-ACCORD doctrine. It is a precision: *tracked*
does not mean *tracked in a public repo*. DEV-DOCS are required for local and agent
operation. They are not required to be publicly distributed.

---

## Problem

DEV-ACCORD.03's visibility table implied a default of public exposure for all planning
and bootstrap docs. This created a conflict: portfolio owners building commercial
products have a legitimate interest in keeping internal roadmaps, planning state, and
agent operating instructions private, even when the product code ships publicly.

The prior private doc rule was too narrow — it only covered `MARKET.md` and `DIST.md`.
All other DEV-DOCS defaulted to public, which was wrong.

Additionally, `projects.yaml` holds canonical pointers to per-repo DEV-DOCS. Those
pointers continue to work in the local working copy. They do not require the files to
be present in a public clone. Remote agents operating on a public clone that lacks
bootstrap files already have a fallback defined in DEV-ACCORD.04: ask the user for
bootstrap context before acting.

---

## Revised planning doc visibility table

Replaces the table in DEV-ACCORD.03 § "Planning doc roles":

| Doc | Owns | Visibility |
| --- | --- | --- |
| `DEV-PATH.md` | Phase history, design decisions, PASS registry — append-only | **private by default** |
| `DEV-PLAN.md` | Current execution state, active milestones, priority work queue | **private by default** |
| `DEV-TRACKS.md` | Parallel workstreams and dependencies | **private by default** |
| `DEV-RELEASE.md` | External release table, entry conditions, release notes | **private by default** |
| `AGENTS.md` | GC bootstrap pointer — routes agents to onboarding authority | **private by default; public-safe stub permitted** |
| `CLAUDE.md` | Claude Code adapter — routes to AGENTS.md | **private by default; public-safe stub permitted** |
| `MARKET.md` | Positioning, audiences, channels, messaging | **private repo only** (unchanged) |
| `DIST.md` | Distribution tiers, revenue streams, commercial milestones | **private repo only** (unchanged) |

**Private by default** means the file must be excluded from public distribution
repositories via `.gitignore`. It must be present in the local working copy and any
private control plane or private repo. It must not be published as part of a release
artifact, package, or distribution bundle.

**Private repo only** (unchanged from DEV-ACCORD.03) means the file must never
appear in a public repo under any form — not even as a stub.

---

## Revised private doc rule

Replaces the "Private doc rule" section in DEV-ACCORD.03:

> All DEV-DOCS are private by default. Public distribution repositories must exclude
> DEV-DOCS using `.gitignore`. The canonical location for DEV-DOCS is the local
> working copy. Private or offline backup (e.g., OneDrive, ProtonDrive, private git
> remote) is strongly recommended.
>
> `MARKET.md` and `DIST.md` carry an additional, stricter constraint: they must
> **never** be committed to a public repository in any form. No pointer files, stubs,
> or redirects for these docs may appear in public repos.
>
> No new strategy doc types may be introduced without a DEV-ACCORD update.

---

## Required .gitignore block for public distribution repos

Every public distribution repo must include the following block in its `.gitignore`.
Comments must be preserved so the intent is self-documenting:

```gitignore
# Internal dev docs — local/private only, not for public distribution
AGENTS.md
CHATGPT.md
CLAUDE.md
DEV-PATH.md
DEV-PLAN.md
DEV-RELEASE.md
DEV-TRACKS.md
REVIEW-GRAMMAR.md
```

Additional private doc types (`MARKET.md`, `DIST.md`, and any future additions
declared by DEV-ACCORD amendment) must also be present in this block if they exist
in the project.

---

## Public-safe stub (optional)

A public distribution repo MAY include a public-safe stub for `AGENTS.md` and/or
`CLAUDE.md` when the repo owner wants to signal agent behavior to external
contributors or runtime hosts. If a stub is used, it must conform to all of the
following:

1. It must identify itself as a public stub in its first line.
2. It must not contain internal governance doctrine, reading order, or planning
   pointers that are private.
3. It must direct contributors to `README.md` or `CONTRIBUTING.md` for public
   contribution guidance.
4. It may state that internal governance docs exist but are private.

If no stub is provided, DEV-ACCORD.04 already governs the fallback: an agent
operating on a public clone that finds no bootstrap file must ask the user for
bootstrap context before modifying files. This is correct behavior and requires
no workaround.

Example minimal public-safe stub for `AGENTS.md`:

```markdown
# AGENTS.md

This repository's internal governance and planning docs are private.
External contributors: see README.md and CONTRIBUTING.md.
Automated agents: no internal bootstrap is available in this clone.
Ask the repository owner for operating context before modifying files.
```

---

## Relationship to projects.yaml canonical pointers

`projects.yaml` holds `canonical:`, `path:`, `tracks:`, and `release:` pointers
to per-repo DEV-DOCS. These pointers remain valid. They resolve correctly in the
local working copy where the files are present. They do not require the files to
exist in public clones. `projects.yaml` itself is not a public distribution
artifact; it lives in the control plane.

---

## Artifact exclusion (distribution layer)

In addition to `.gitignore`, project-type-specific artifact configs must exclude
DEV-DOCS from published packages:

| Ecosystem | Config | Key |
| --- | --- | --- |
| npm / Node | `package.json` | `files` array (allowlist) or `.npmignore` |
| Python | `MANIFEST.in` | `exclude` directives |
| VS Code extension | `.vscodeignore` | explicit exclusion lines |
| PyInstaller / binary | spec file | explicit exclusion or data exclusion |

Artifact exclusion is enforced separately from `.gitignore`. Both must be present
when applicable.

---

## Cluster Invariants

**DEV-ACCORD-CI-19 — DEV-DOCS are private by default**
All DEV-DOCS (`DEV-PATH.md`, `DEV-PLAN.md`, `DEV-TRACKS.md`, `DEV-RELEASE.md`,
`AGENTS.md`, `CLAUDE.md`) are private by default. Public distribution repos must
exclude them. Presence in the local working copy is required. Public exposure
requires an explicit classification override in a future DEV-ACCORD amendment.

**DEV-ACCORD-CI-20 — Public distribution repos must carry the DEV-DOCS .gitignore block**
Any repo distributed publicly must include the required `.gitignore` block defined in
this PASS. Absence of this block in a public repo is a conformance violation.

**DEV-ACCORD-CI-21 — Public-safe stubs must not contain private doctrine**
If a public-safe `AGENTS.md` or `CLAUDE.md` stub is present in a public repo, it
must not contain internal governance reading order, planning pointers, or agent
operating instructions. A stub that leaks private doctrine is non-conformant.

---

## What does not change

- DEV-ACCORD.04's bootstrap file requirements continue to apply to the local
  working copy and any private clone.
- The agent-trail reading sequence defined in DEV-ACCORD.03 is unchanged.
- DEV-ACCORD.04's fallback rule (agent must ask for context when no bootstrap
  file is found) is unchanged and sufficient for public clone scenarios.
- `MARKET.md` and `DIST.md` private repo rules are unchanged and still carry
  the stricter "never in a public repo" constraint.
- PASS ID numbering, cluster invariant numbering, and DEV-ACCORD amendment
  process are unchanged.

---

## Outputs

- DEV-ACCORD.03 visibility table replaced: all DEV-DOCS are now private by default
- DEV-ACCORD.03 private doc rule expanded: covers all DEV-DOCS, not just MARKET.md/DIST.md
- Required `.gitignore` block defined for public distribution repos
- Public-safe stub pattern defined (optional)
- Artifact exclusion layer declared alongside `.gitignore`
- Three new cluster invariants: DEV-ACCORD-CI-19 through DEV-ACCORD-CI-21
- Relationship to `projects.yaml` canonical pointers clarified
