# DEV-ACCORD.10 — Git Split Authorization Rule

**PASS ID:** DEV-ACCORD.10
**Canonical ID:** GC:2018
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-07-01T16:44:58Z
**Depends on:** GC:2011 (DEV-ACCORD.03), GC:2014 (DEV-ACCORD.06)
**Amends:** DEV-ACCORD.03 — adds git split discipline to the agent onboarding trail; DEV-ACCORD.06 — constrains publish workflow choices

---

## Summary

Agents must not create a new branch, pull-request chain, worktree, fork, or other
git topology split unless the human explicitly authorizes that split.

The default publish path is the current branch. In this portfolio, when the current
branch is `main` and direct push is permitted, agents stay on `main`, commit coherent
finished work there, and push `origin/main`.

Agents may and should recommend a split when it would reduce risk, but the split is
a human decision, not an agent default.

---

## Problem

Agent workflows often assume "create a branch and open a PR" as a safe default.
That default is wrong for portfolios where the owner intentionally works directly on
`origin/main` unless there is a concrete reason to split.

The incident that prompted this PASS: an agent was asked to commit and push existing
Cockpit work. The agent created a `codex/...` branch and draft PR without asking,
even though the user expected the work to land on `origin/main`. The branch was later
fast-forwarded back to `main`, but the error showed the missing rule: branch creation
is a topology change and requires authorization.

---

## Definitions

**Git split** means any action that moves work away from the current branch or creates
a parallel review/publish path, including:

- creating a new branch
- creating a worktree for the same repo
- creating a fork or pushing to a fork
- opening a pull request or draft pull request as the publish path
- creating a PR chain or stacked branch sequence
- splitting a user-requested publish operation across multiple branches

**Current-branch publish** means committing coherent completed work on the current
branch and pushing that same branch to its configured upstream.

---

## Default rule

Agents MUST default to current-branch publish.

If the user says "commit", "push", "ship it", "close the loop", "get it committed",
or equivalent, the agent must interpret that as current-branch publish unless the
user explicitly asks for a branch, PR, fork, worktree, or review chain.

No GC rule, plugin habit, or generic GitHub workflow may override this default.

---

## Authorization rule

Before performing any git split, the agent MUST:

1. Explain why a split is being recommended.
2. Name the exact split action proposed.
3. Name the proposed branch, worktree, fork, or PR shape.
4. Explain what happens if the work remains on the current branch.
5. Wait for explicit human authorization.

Acceptable authorization examples:

- "Yes, create that branch."
- "Open a PR for this."
- "Use a worktree."
- "Split this into a review branch."

Not authorization:

- "Commit it."
- "Push it."
- "Get this shipped."
- "Clean this up."
- Silence after the agent states an intention.

---

## When agents should recommend a split

Agents should recommend, but not perform, a split when any of the following is true:

| Condition | Why a split may help |
| --- | --- |
| Risky or experimental implementation | Keeps `main` from carrying uncertain behavior |
| Long-running work | Avoids leaving `main` half-built across sessions |
| Human review requested | Creates an explicit review surface before mainline movement |
| CI or repository policy blocks direct push | Lets required checks run before merge |
| Release or hotfix isolation needed | Keeps release stabilization separate from normal development |
| Mixed unrelated scopes | Lets each scope be reviewed and reverted independently |
| External collaborator needs an isolated test surface | Avoids treating in-progress work as mainline truth |
| Potentially destructive migration | Gives rollback and review a clear boundary |

If the human declines the split, the agent must either continue on the current branch
or explain the concrete blocker that prevents safe progress.

---

## Prohibited agent defaults

Agents MUST NOT create a branch or PR merely because:

- a plugin workflow prefers PRs
- the repo is on `main`
- the work touches packaging, install paths, dependencies, or release gates
- there are uncommitted changes
- the agent wants a tidier history
- the agent is unsure

Uncertainty is a reason to ask, not a reason to split.

---

## Dirty worktree obligation

When a worktree is dirty, agents must inventory the visible changes before committing
or pushing. If the visible changes are coherent with the user's requested scope, the
agent should include them in the current-branch publish. If the changes appear mixed
or unrelated, the agent must ask how to group them.

Agents must not use branch creation to avoid understanding a dirty worktree.

---

## Relationship to DEV-ACCORD.06

DEV-ACCORD.06 continues to govern change level, DEV-DOCS obligations, validation,
evidence, and commit trailers.

This PASS governs the git topology and publish path. A DRIVE or PASS-level change
does not automatically require a branch. It may justify recommending one, but
authorization is still required.

---

## Cluster Invariants

**DEV-ACCORD-CI-25 — Git splits require explicit human authorization**
No agent may create a branch, worktree, fork, pull request, draft pull request, PR
chain, or equivalent split from the current branch without explicit human approval.

**DEV-ACCORD-CI-26 — Current branch is the default publish path**
When asked to commit or push, agents must stay on and push the current branch unless
the human authorizes a split or the repository itself blocks the operation.

**DEV-ACCORD-CI-27 — Agents must recommend splits before performing them**
When a split seems useful, the agent must explain the reason, proposed shape, and
consequence of not splitting, then wait for authorization.

**DEV-ACCORD-CI-28 — Dirty worktrees must be understood, not escaped**
Agents must inventory and classify dirty worktree changes. Creating a branch to avoid
understanding existing uncommitted work is non-conformant.

---

## Outputs

- Git split authorization rule declared
- Current-branch publish declared as the default
- Split recommendation criteria declared
- Dirty worktree obligation declared
- Four new cluster invariants: DEV-ACCORD-CI-25 through DEV-ACCORD-CI-28
