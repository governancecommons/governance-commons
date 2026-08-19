# PASSCHANGELOG — Governance Commons

Ecosystem-level governance decisions for the Governance Commons ecosystem.
For per-spec implementation changes, see each spec's own `passchangelog.md` and `CHANGELOG.md`.

Entry index: GC-PASS-NNNN.NN (4-digit sequential row number — not a PASS identity). Newest first.

**PASS identity** — use `CLUSTER.NN` alias (e.g. `DEV-ACCORD.02`) or `GC:NNNN`
canonical ID (e.g. `GC:2010`) to refer to a PASS. `GC-PASS-NNNN.NN` is only the
changelog row number. Do not use it as a PASS reference in docs, code, or links.

**PASS structure** (see DEV-ACCORD.02 / GC:2010 for the governing standard):

- `CLUSTER.NN.00` — **Primary PASS.** Owns the goal, defines scope, Done-when, inputs, outputs.
- `CLUSTER.NN.01` – `CLUSTER.NN.09` — **Sub-PASSes.** Discrete tasks within the primary PASS scope.
- `CLUSTER.NN.10` – `CLUSTER.NN.99` — **Compound PASSes.** A cluster of sub-PASSes that execute in parallel.

**Timestamp requirement:** Every PASS entry must include a `**timestamp**` field in ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ`). This is mandatory — no PASS entry is complete without it. Agents must record the actual time of the decision, not omit it.

---

## Entry Formats

Use the format that matches `change_type`. Do not mix them.

---

### Format: build

For passes that create or extend something — new specs, schemas, rules, tooling.

```markdown
**pass_id**: GC-PASS-NNNN.NN
**timestamp**: YYYY-MM-DDTHH:MM:SSZ
**change_type**: build
**authority_level**: AL:1 | AL:2 | AL:3
**status**: ACCEPTED
**affected_surfaces**: (specs, schemas, agents, or tooling that now depend on this)

**what**: (the artifact, field, rule, or behavior that now exists)
**why**: (the trigger — the gap, requirement, or contradiction that made this necessary)
**new_constraints**: (rules future passes must respect because of this — or "none")
**reasoning**: (what was weighed, what was rejected, what prevents this from being undone carelessly)
```

---

### Format: fix

For passes that resolve a problem — bugs, contradictions, drift, bad prior decisions.

```markdown
**pass_id**: GC-PASS-NNNN.NN
**timestamp**: YYYY-MM-DDTHH:MM:SSZ
**change_type**: fix
**authority_level**: AL:1 | AL:2 | AL:3
**status**: ACCEPTED
**affected_surfaces**: (what was broken and what else was touched to fix it)

**problem**: (what was wrong)
**why_problem**: (why it matters — the actual consequence if left unfixed)
**fix_approach**: (what the right fix is and why that approach over alternatives)
**what_was_done**: (the concrete change made)
**prevention**: (what now exists or must be done to stop this class of problem recurring)
```

---

### Format: governance

For passes that open/close phases, register authority decisions, or record ecosystem-level rulings.

```markdown
**pass_id**: GC-PASS-NNNN.NN
**timestamp**: YYYY-MM-DDTHH:MM:SSZ
**change_type**: governance
**authority_level**: AL:1 | AL:2 | AL:3
**status**: ACCEPTED
**affected_surfaces**: (what this decision governs or constrains)

**summary**: (what was decided and why — include scope, what was opened/closed, and any new constraints)
**new_constraints**: (rules future passes must respect because of this — or "none")
```

---

## GC-PASS-0022.00 — 2026-08-19

**pass_id**: GC-PASS-0022.00
**timestamp**: 2026-08-19T00:00:00Z
**change_type**: fix
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: DEV-ACCORD.03 (GC:2011) reading order, Agent-Trail table, bootstrap router

**problem**: The Capability Contract package (`dev-docs/_root/contracts/`) — the portfolio's shared `<domain>.<resource>.<action>` vocabulary for what a project provides/consumes/prohibits for another — was frozen at v0.1 on 2026-08-17 with a working validator and two pilot adoptions, but DEV-ACCORD.03's mandatory reading order never referenced it.
**why_problem**: An agent following the onboarding protocol exactly as written had no path to discovering the package existed. This produced the exact failure the package was built to prevent: mid-task on marlin's INIT.30.08, an agent (Claude) found marlin already had three uncoordinated ad-hoc "capability" vocabularies and, lacking any pointer to the canonical one, began drafting a fourth reconciliation scheme instead of the correct action (flag the overlap, do nothing further without instruction).
**fix_approach**: Add the package as its own reading-order step rather than folding it into an existing step (e.g. `projects.yaml`), since its trigger condition (about to name/declare a cross-project capability) is narrower and more specific than "read the registry." Mirror the addition in the Agent-Trail table (kept in sync with reading order by convention) and add a dedicated bootstrap-router row so low-risk/read-only tasks aren't forced to load it unless the task shape actually matches.
**what_was_done**: Inserted reading-order step 8 (`dev-docs/_root/contracts/README.md`), renumbered the former step 8 to 9; added a matching "Capability vocabulary" row to the Agent-Trail table; added a router row for "Naming/declaring what a project provides, consumes, or prohibits for another project"; added an `Amended by` line to the file header.
**prevention**: Any future portfolio-wide shared-vocabulary package (interfaces.yaml, authority.yaml, operations.yaml, when built) should be added to this same reading order at creation time, not retrofitted after a drift incident.

---

## GC-PASS-0021.00 — 2026-07-05

**pass_id**: GC-PASS-0021.00
**timestamp**: 2026-07-05T00:00:00Z
**change_type**: build
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: DEV-ACCORD.06 (Change Playbook amendment); all GC-conformant agents; PLAY.jsonl closeout obligations; compound-PASS-brief gate

**what**: Amendment to DEV-ACCORD.06 / GC:2014 declaring three overhead-relief changes: (1) BUNT PLAYs are exempt from the PLAY.jsonl record and five-bucket timing table required by CI-33 — a commit trailer and one-line next step is sufficient; (2) single-repo, single-lane RUN PLAYs may record `timing` as one collapsed `{started_at, ended_at, duration_ms}` object instead of the five-bucket breakdown; (3) the compound-PASS-brief gate (CI-38) now triggers only for batches that are cross-repo, cross-agent, touch more than 3 files, or contain a DRIVE/PASS-trigger change (governance-standard-file edits always count as PASS-trigger regardless of size). Adds DEV-ACCORD-CI-47 through DEV-ACCORD-CI-49.
**why**: The portfolio owner reported spending more session time on governance bookkeeping (PLAY telemetry, closeout sections, blocking briefs) than on the underlying dev work. Review of DEV-ACCORD.06's closeout amendments found that CI-33/34/35 had erased BUNT's intended lightweight tier by requiring the full closeout on every PLAY regardless of level, and that CI-38's brief gate had no size floor, blocking trivial same-repo batches the same as genuine cross-repo/multi-agent work.
**new_constraints**: (1) BUNT closeout is commit-trailer-only; PLAY.jsonl and timing tables apply to RUN/DRIVE/PASS. (2) Single-lane RUN may use collapsed timing. (3) Compound-PASS-brief gate applies only above the stated size/scope floor; edits to GC standard files remain PASS-trigger regardless of size.
**reasoning**: Preserves DRIVE/PASS-level rigor (full timing, full closeout, blocking brief for genuinely cross-cutting work) while removing the bookkeeping tax on trivial, single-repo, single-lane work — the exact case the BUNT tier was originally meant to cover before the closeout amendments made it universal. The governance-standard-file carve-out in CI-49 keeps this change from reopening the CI-38 incident: an agent still cannot use the size floor as a loophole to edit DEV-ACCORD/CANON files without a brief.

---

## GC-PASS-0020.00 — 2026-07-02

**pass_id**: GC-PASS-0020.00
**timestamp**: 2026-07-02T02:55:00Z
**change_type**: fix
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: DEV-ACCORD.06.md (correction note added); one commit trailer (`2d4a24d`, left unamended); passchangelog.md GC-PASS-0018.00 entry; DEV-PATH.md 2026-07-01 note

**problem**: The 2026-07-01 compound-PASS-default amendment (commit `2d4a24d`, `GC-PASS-0018.00`) was drafted and cited under the working name "DEV-ACCORD.11" in its `DEV-ACCORD.06.md` section heading, in the `passchangelog.md` GC-PASS-0018.00 entry, in a `DEV-PATH.md` note, and in the commit's own `Pass-ID: DEV-ACCORD.11` trailer — without ever being assigned a canonical ID, given its own `passes/dev-accord/DEV-ACCORD.11.md` file, or entered in `passes/passes.registry.json`. `validate-registry.ps1` did not catch this because it only cross-checks `.md` files under `passes/` that declare a `Canonical ID:` header; a name used only in prose or a commit trailer is invisible to that check. Caught during a portfolio-owner review questioning whether PASS labeling discipline was actually being enforced.
**why**: Reaching for a fresh `CLUSTER.NN` name while drafting a governance amendment, without running the registration step, is exactly the failure mode DEV-ACCORD-CI-8 (no casual number assignment outside a migration PASS) exists to prevent — reached from a different direction: not an unauthorized number assignment, but a PASS-shaped citation with no registry entry behind it at all.
**new_constraints**: (1) Any `Pass-ID:` trailer, PASS-shaped heading, or PASS cross-reference must resolve to an actual `passes/passes.registry.json` entry, or be explicitly marked as a working name pending registration (DEV-ACCORD-CI-41, declared in the corresponding DEV-ACCORD.06 amendment). (2) The governed identity of the 2026-07-01 compound-PASS-default content and the 2026-07-02 `validation_profile` content is DEV-ACCORD.06 / GC:2014 — cite it that way, not `DEV-ACCORD.11`.
**reasoning**: The correction is applied in place (a note above the misattributed heading in `DEV-ACCORD.06.md`) and via this append-only changelog entry, not by rewriting the `2d4a24d` commit trailer or editing the historical `GC-PASS-0018.00` entry — consistent with this portfolio's append-only doctrine (PROTECTED.md) and git-history policy (no rewriting commits without explicit authorization). Retroactively manufacturing a `DEV-ACCORD.11.md` file and registry entry to match the mistaken name was considered and rejected: it would misrepresent the actual decision sequence (implying a separately reviewed and accepted PASS that never happened) and itself be exactly the casual number assignment DEV-ACCORD-CI-8 forbids.

---

## GC-PASS-0019.00 — 2026-07-02

**pass_id**: GC-PASS-0019.00
**timestamp**: 2026-07-02T02:15:00Z
**change_type**: fix
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: passchangelog.md row-number index only; no PASS identity, alias, or canonical ID changed

**problem**: Row number `GC-PASS-0006.00` was assigned twice — once to the CANON cluster founding entry (2026-06-20, CANON.00/CANON cluster establishment) and once to the PASS-6 opening entry (2026-06-16, Doc Vault Plane track). Row number `GC-PASS-0013.00` was also assigned twice — once to DEV-ACCORD.03 (2026-06-28, Agent Onboarding Protocol) and once to DEV-ACCORD.04 (2026-06-28, Agent Bootstrap Standard). Both collisions predate this fix and were caught during a validator hardening review, not during original entry creation.
**reasoning**: Per DEV-ACCORD.02, `GC-PASS-NNNN.NN` is a passchangelog row index, not a PASS identity — the PASS identity of every affected entry (`DEV-ACCORD.03` / `GC:2011`, `DEV-ACCORD.04` / `GC:2012`, `CANON.00`, the PASS-6 opening record) is unambiguous and unaffected by this collision; only the row-index column has a duplicate value. `passchangelog.md` is append-only (PROTECTED.md Rule 1) and CANON.01 R-IM-6 requires superseded or corrected PASSes to remain in the registry permanently rather than be edited in place. The correct fix is therefore a pointer-only correction, not a renumbering of the four existing entries.
**what**: This entry records the collision for the audit trail. The four affected entries keep their original row numbers, timestamps, and content unchanged: `GC-PASS-0006.00 — 2026-06-20` (CANON.00), `GC-PASS-0006.00 — 2026-06-16` (PASS-6 opening), `GC-PASS-0013.00 — 2026-06-28` (DEV-ACCORD.03), `GC-PASS-0013.00 — 2026-06-28` (DEV-ACCORD.04). Readers must disambiguate by date and title, not row number alone, for these four entries specifically. All row numbers assigned from `GC-PASS-0014.00` onward are confirmed unique (verified by full-file scan as part of this fix).
**new_constraints**: (1) Row-number collisions in `passchangelog.md` are corrected by an append-only pointer entry, never by editing the colliding rows. (2) Before assigning the next `GC-PASS-NNNN.NN` row number, the agent must confirm no existing entry already uses it (a `grep '^## GC-PASS-NNNN'` check is sufficient) — this collision happened because that check was skipped at least twice.

---

## GC-PASS-0018.00 — 2026-07-01

**pass_id**: GC-PASS-0018.00
**timestamp**: 2026-07-01T19:00:00Z
**change_type**: build
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: DEV-ACCORD.06 (Change Playbook amendment); DEV-ACCORD.02 compound PASS numbering (referenced, not altered); `gc-audit/PLAY-OBLIGATIONS.md`; `gc-audit/CONTRACTS.md`; all GC-conformant agents

**what**: DEV-ACCORD.11 — Compound PASS Operating Rhythm Hardening, declared as an amendment to DEV-ACCORD.06. Declares a compound-PASS-default trigger table (batch language, "all N", parallelize, cross-repo work all default to proposing a compound PASS rather than a chain of single PASSes); a required compound PASS brief (goal / sub-PASS lanes / repos / files / validation gates / commit plan / blockers) that the human must explicitly confirm before any file edit begins; next-recommended-step classification (`Compound PASS` / `Single PASS` / `DRIVE` / `RUN` / `BUNT` / `Blocked`), refining DEV-ACCORD-CI-35; and a release/evidence-review threshold limiting full release/evidence review to compound-PASS close, release-gate/version change, or explicit human request. Adds DEV-ACCORD-CI-36 through DEV-ACCORD-CI-38.
**why**: The portfolio owner reported that single-lane PASS-by-PASS execution was too slow for "do as much as possible" requests, and that release/evidence review after every small PLAY was adding drag without adding safety. Independent review (ChatGPT, requested by the owner) converged on the same diagnosis: GC's governance obligations are sound but under-batched. The brief-before-execution requirement (CI-38) exists because an agent attempted this exact change directly against DEV-ACCORD.06 without declaring a PLAY or presenting a brief first; the owner caught and reverted it before any commit.
**new_constraints**: (1) Batch-language and cross-repo requests default to a compound PASS proposal, not a single-PASS chain. (2) A compound PASS may not begin execution, including file edits, until the human confirms the compound PASS brief. (3) Every PLAY closeout's next recommended step must be classified as Compound PASS, Single PASS, DRIVE, RUN, BUNT, or Blocked — an unclassified next step is non-conformant. (4) Full release/evidence review is required only at compound-PASS close, release-gate/version change, or explicit request — not after every small RUN or BUNT.
**reasoning**: The fix preserves every existing per-lane obligation (DEV-DOCS, validation, commit trailer) while removing the planning-granularity tax that was making batchable work feel like a chain of single PASSes. Requiring a confirmed brief before execution closes the exact gap that produced the incident this PASS responds to: GC's rules were previously enforced by an agent's voluntary compliance with prose instructions, with no explicit human-confirmation checkpoint before a PASS-level file edit. Naming the release/evidence-review threshold explicitly (rather than leaving it to agent judgment) prevents the fix from drifting into skipped validation.

---

## GC-PASS-0017.00 — 2026-07-01

**pass_id**: GC-PASS-0017.00
**timestamp**: 2026-07-01T16:44:58Z
**change_type**: build
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: DEV-ACCORD cluster; all GC-conformant agents; git publish workflows; DEV-ACCORD.03 reading order; DEV-ACCORD.06 Change Playbook

**what**: DEV-ACCORD.10 (GC:2018) — Git Split Authorization Rule. Declares that agents must not create a new branch, PR chain, worktree, fork, draft PR, or equivalent git topology split without explicit human authorization. Establishes current-branch publish as the default for "commit", "push", "ship it", "close the loop", and equivalent requests. Defines when agents should recommend a split, what they must disclose before asking, and the dirty worktree obligation: inventory and classify existing changes rather than escaping them by branch creation. Adds DEV-ACCORD-CI-25 through DEV-ACCORD-CI-28.
**why**: An agent converted a user request to commit and push Cockpit work into a new `codex/...` branch and draft PR without asking, despite the portfolio owner's preference to stay on `origin/main` unless a split is explicitly authorized. Generic GitHub plugin habits and branch-first workflows are not sufficient authority to change a repo's publish topology.
**new_constraints**: (1) Git splits require explicit human authorization. (2) Current-branch publish is the default when the user asks to commit or push. (3) Agents may recommend a split only after explaining why, naming the proposed shape, and explaining what happens without it. (4) Dirty worktrees must be inventoried and understood; branch creation must not be used to avoid scope analysis.
**reasoning**: Branches, PRs, forks, and worktrees are topology changes, not neutral implementation details. They alter review flow, history shape, and user expectations. The correct default depends on the owner's workflow, not on an agent or plugin's preferred habit. Requiring explicit authorization preserves agent ability to recommend safer split workflows while keeping the human in control of when the repo leaves the current-branch path.

---

## GC-PASS-0016.00 — 2026-06-30

**pass_id**: GC-PASS-0016.00
**timestamp**: 2026-06-30T00:00:00Z
**change_type**: fix
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: DEV-ACCORD cluster; DEV-ACCORD.02 three-layer model; all agents and docs that reference the PASS tier; docs/REVIEW-GRAMMAR.md

**problem**: DEV-ACCORD.02 declared a three-layer model (Governance / Execution / Audit) that omitted the planning structure entirely and misnamed the PASS tier. Listing PASS alongside Phase, Wave, and Track in the vocabulary table implied they were the same kind of thing — structural planning containers. They are not. Phase, Wave, and Track are structural containers that answer where work sits. PASS converts planning intent into a governed commitment. Conflating them caused agents to treat PASS as a fourth planning layer rather than a cross-cutting bridge, producing vocabulary confusion and incorrect DEV-DOCS structure.
**fix**: DEV-ACCORD.07 (GC:2015) replaces the three-layer model with a four-tier model: Planning (Phase, Wave, Track) / Bridge (PASS, Sub-PASS) / Execution (RUN) / Audit (Evidence Bundle). PASS is formally declared the bridge tier. Phase, Wave, and Track are formally declared the planning tier. The vocabulary table is restructured by tier. DEV-ACCORD.02 is amended in place with forward pointers to DEV-ACCORD.07.
**new_constraints**: (1) PASS is the bridge tier — not a planning layer. Docs and agents that treat PASS as a structural planning container are non-conformant. (2) Phase, Wave, and Track are the only three GC structural planning containers. A fourth requires a GC amendment. (3) A PASS may cross planning boundaries — spanning multiple Tracks or Waves is conformant.
**reasoning**: The bridge framing resolves the long-standing ambiguity between "where work sits" and "what governs it". PASS has always been cross-cutting in practice — a PASS that touches CLI, schema, and docs spans three Tracks. Calling it a planning layer implies it should be confined to one. The bridge tier makes explicit what was always true: PASS is the handoff from planning to execution, not a position in the planning hierarchy.

---

## GC-PASS-0015.00 — 2026-06-30

**pass_id**: GC-PASS-0015.00
**timestamp**: 2026-06-30T00:00:00Z
**change_type**: build
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: All portfolio commits and agents; DEV-ACCORD cluster; pre-commit/pre-push hooks; CI; DEV-ACCORD.05 trailer spec (superseded)

**what**: DEV-ACCORD.06 (GC:2014) — Change Playbook. Declares four change classes: BUNT (tiny tactical, no behavioral effect), RUN (normal bounded work), DRIVE (meaningful milestone movement — version bumps, API changes, packaging, dependency changes, milestone closures), PASS (governed contract — multi-step, cross-cutting, standard-changing). Defines per-class obligations for DEV-DOCS updates, validation, and evidence. Declares escalation rules with an explicit trigger table and a highest-class-wins rule. Declares the unified commit trailer schema — absorbing the `Dev-Docs:` field introduced in DEV-ACCORD.05 — so that all trailer fields are owned in one place. Specifies enforcement at pre-commit, pre-push, agent, and CI layers. Adds cluster invariants CI-13 through CI-16.
**why**: DEV-ACCORD.02 defined only PASS and RUN as a binary, leaving no classification for changes that are meaningful but don't warrant a full governance contract. This gap caused recurring DEV-DOCS drift — DRIVE-class changes (version bumps, formula completions, dependency additions) had no named obligation and routinely shipped without updating DEV-DOCS. DEV-ACCORD.05 introduced a `Dev-Docs:` trailer field in isolation; adding a `Change-Level:` field as a separate PASS would have produced two independent trailer specs that grow apart over time. DEV-ACCORD.06 closes both gaps: names the missing class (DRIVE), and unifies the trailer schema so future fields have one owner.
**new_constraints**: (1) Every commit must carry `Change-Level:` and `Dev-Docs:` trailer fields. (2) DRIVE-trigger changes (version, API, packaging, install path, milestone, dependency) must be classified DRIVE at minimum. (3) Highest class wins when a commit spans multiple levels. (4) The commit trailer schema is owned by DEV-ACCORD.06; new fields require a DEV-ACCORD amendment. (5) The `Dev-Docs:` field defined in DEV-ACCORD.05 is now governed by DEV-ACCORD.06.
**reasoning**: The DRIVE class was chosen over alternatives like "SIGNIFICANT RUN" because it continues the sports vocabulary (BUNT → RUN → DRIVE → PASS) and the metaphor holds: a drive in football is sustained forward movement that changes field position, just as a DRIVE change moves the project's release or state forward in a way that must be recorded. The unified trailer approach was chosen over piecemeal field introduction because trailer fields interact — `Dev-Docs: not-needed` only makes sense alongside a `Change-Level` that tells you why, and `Validation:` only makes sense for DRIVE and PASS. Declaring them together makes the schema coherent and prevents future PASSes from adding conflicting fields.

---

## GC-PASS-0014.00 — 2026-06-30

**pass_id**: GC-PASS-0014.00
**timestamp**: 2026-06-30T00:00:00Z
**change_type**: build
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: All portfolio projects and agents; DEV-ACCORD cluster; docs/REVIEW-GRAMMAR.md; dxp-init (Marlin); future GC-AUDIT tooling; pre-commit/pre-push hooks

**what**: DEV-ACCORD.05 (GC:2013) — DEV-DOCS Suite and GC-AUDIT Declaration. Establishes a four-term vocabulary with no overlap: DEV-DOCS (the planning doc suite), DEV-ACCORD (the governing standard), GC-AUDIT (the validation/audit toolchain), and Marlin (install wizard only). Declares DEV-DOCS as the collective name for DEV-PATH, DEV-PLAN, DEV-TRACKS, and DEV-RELEASE. Declares GC-AUDIT as the portfolio-wide owner of validate, normalize, de-stale, adversarial audit, trace, and release-readiness operations. Promotes REVIEW-GRAMMAR.md from working grammar to GC standard component and canonical verb registry for GC-AUDIT. Declares existing validators (validate-planning, validate-bootstrap, validate-pointers, validate-debt) as GC-AUDIT implementations. Specifies GC-AUDIT invocation interface (`dcp audit <verb>`). Declares DEV-DOCS maintenance gate with `Dev-Docs:` commit trailer and pre-commit/pre-push enforcement layers. Declares stale reference rule and de-stale triggers. Specifies Marlin delegation pattern: Marlin calls GC-AUDIT, never reimplements it.
**why**: The portfolio lacked a single term for the planning doc suite, causing agents and humans to use inconsistent language ("the planning docs", "development docs", "the four docs"). De-stale and other audit operations had no declared owner — ChatGPT's review suggested placing de-stale in Marlin, which is wrong (Marlin is an installer, not an auditor). DEV-DOCS drift after code changes was a recurring problem with no enforcement mechanism. Niji's v0.9 state demonstrated the exact failure: code was complete but README, DEV-TRACKS, DEV-RELEASE, and guidance docs told different stories because no gate existed to require updates. This PASS closes all three gaps: naming, ownership, and gate.
**new_constraints**: (1) DEV-DOCS is the required term for the planning doc suite. (2) GC-AUDIT is the required term for the validation/audit toolchain; no other tool may own audit logic. (3) Marlin must not reimplement GC-AUDIT operations. (4) Commits with meaningful changes require `Dev-Docs: updated` or `Dev-Docs: not-needed` with reason. (5) REVIEW-GRAMMAR verb names are the standard for all GC-AUDIT implementations. (6) These constraints cannot be overridden by project-level instruction files.
**reasoning**: Marlin as de-stale owner was rejected because it conflates install and audit concerns — Marlin's job is to set up an environment, not to be the portfolio's health-check authority. GC-AUDIT as a separate named concept allows the toolchain to run independently of whether Marlin was used to install a project. The commit trailer approach was chosen over blanket pre-commit blocks because blocks create friction on trivial commits (typos, comments) and get bypassed; trailers are auditable and low-ceremony. REVIEW-GRAMMAR promotion avoids defining verb names in two places — the PASS declares the registry, the registry defines the verbs.

---

## GC-PASS-0013.00 — 2026-06-28

**pass_id**: GC-PASS-0013.00
**timestamp**: 2026-06-28T00:00:00Z
**change_type**: build
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: CLAUDE.md (c:\dev); all agents operating in this portfolio; future CODEX.md, COPILOT.md

**what**: DEV-ACCORD.03 (GC:2011) — Agent Onboarding Protocol. Moves all portfolio governance (reading order, portfolio rules, ecosystem overview, planning doc roles) out of CLAUDE.md and into a GC standard. CLAUDE.md stripped to a three-line stub that points to this standard. Agent bootstrap files (CLAUDE.md, CODEX.md, COPILOT.md) are now thin wrappers only — no governance content belongs in them. DEV-ACCORD.03 is the single source of truth for any agent onboarding in this portfolio, regardless of which agent it is.
**why**: All portfolio governance was living in CLAUDE.md, a Claude-specific file. Codex, Copilot, and any future agent had no access to the reading order, portfolio rules, or ecosystem overview — they would operate blind or require manual re-briefing each session. The design intent was always for GC standards to own governance and agent files to be thin wrappers. DEV-ACCORD.03 corrects the mistake and makes the system work as intended.
**new_constraints**: (1) Agent bootstrap files must contain only a pointer to DEV-ACCORD.03 — no governance content. (2) Any new agent added to the portfolio must register a bootstrap file in the DEV-ACCORD.03 agent table before its first session. (3) All portfolio rules, reading order, and ecosystem overview live in DEV-ACCORD.03 and are updated there — never in agent-specific files.
**reasoning**: CLAUDE.md was named after Claude and read only by Claude Code. Moving governance into it created a single-agent dependency on a multi-agent portfolio. The fix is structural: governance-commons owns governance, agent files own only the bootstrap pointer. This is the same separation applied to all other GC standards — the standard is portable; the adopter is agent-specific.

---

## GC-PASS-0012.00 — 2026-06-28

**pass_id**: GC-PASS-0012.00
**timestamp**: 2026-06-28T00:00:00Z
**change_type**: build
**authority_level**: AL:1
**status**: ACCEPTED
**affected_surfaces**: all agents operating under GC governance; all projects with PASS-governed work; dxp-init evidence bundle pipeline

**what**: DEV-ACCORD.02 (GC:2010) — Execution model standard. Defines three layers: (1) PASS (governance contract — planned work with Done-when criteria, track, wave, seven required fields); (2) RUN (execution event — every code change regardless of size, always produces a git commit, significant RUNs produce a signed evidence bundle); (3) Evidence Bundle (signed, machine-verifiable audit record of a RUN, Stranger-test compliant). Defines PASS numbering: .00 primary, .01–.09 sub-PASSes, .10–.99 compound (parallel execution cluster). Defines parallelism declaration via `Parallel with:` and `Batch:` metadata fields. Defines multi-agent coordination doctrine: PASS is the shared contract all agents read before starting work.
**why**: PASS doctrine existed only in dxp-init DEV-PATH.md (INIT-D17), making it invisible to agents working on eco, arche, cockpit, lasso, or any other portfolio project. The RUN concept did not exist — there was no governed vocabulary for execution events smaller than a PASS (one-line fixes, hotfixes, trivial commits). Without RUN, the governance model had a gap: significant work was governed by PASSes, but the bulk of daily work (small changes) had no governance vocabulary at all. DEV-ACCORD.02 closes both gaps.
**new_constraints**: (1) Every agent under GC governance must understand PASS, RUN, and Evidence Bundle before performing planned work. (2) Every code change is a RUN, including trivial fixes. (3) Significant RUNs must produce a signed evidence bundle. (4) PASS required fields: PASS ID, Status, Track, Wave, Timestamp, Authority, Author — all seven mandatory. (5) Private signing keys must never appear in any repo.
**reasoning**: PASS without RUN leaves a vocabulary gap at the execution layer. Agents need a word for "what I just did" that is smaller than a PASS and larger than nothing. RUN fills that gap without adding ceremony — every commit was already a RUN, it just had no name. The evidence bundle was already implemented in dxp-init (INIT.06); DEV-ACCORD.02 makes it the canonical audit artifact for a RUN at the GC level, not just a dxp-init feature.

---

## GC-PASS-0011.00 — 2026-06-27

**pass_id**: GC-PASS-0011.00
**timestamp**: 2026-06-27T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: ONS spec (ons.yaml), ons/registry/doc-types.yaml (new), GC passes registry, all agents and validators that consume ONS namespace domains

**what**: DEV-ACCORD.01 (GC:2009) — ONS registration for portfolio planning doc types. (1) Adds `portfolio_doc_name` casing domain to ons.yaml — `DEV-UPPER-KEBAB` pattern `^DEV-[A-Z]+(?:-[A-Z]+)*$` covering all `DEV-*` planning doc types. (2) Adds `portfolio` namespace domain to ons.yaml — registry-required, default registry at `governance-commons/ons/registry/doc-types.yaml`, collision scope is the global portfolio doc type namespace. (3) Creates `ons/registry/doc-types.yaml` — registers DEV-PATH (`portfolio.planning.dev-path`), DEV-PLAN (`portfolio.planning.dev-plan`), DEV-RELEASE (`portfolio.planning.dev-release`), DEV-TRACKS (`portfolio.planning.dev-tracks`) with roles, casing domain, and governing PASS reference.
**why**: DEV-ACCORD.00 declared the four doc types as canonical but did not formally register them in ONS. Without ONS registration, the names have no collision scope, no casing rule, and no namespace domain — agents and validators cannot reference them as first-class ONS entities. This PASS closes that gap and makes the doc types formally governed.
**new_constraints**: (1) Any new `DEV-*` planning doc type MUST be registered in `ons/registry/doc-types.yaml` before portfolio-wide use. (2) Canonical name form is `portfolio.planning.{lowercase-type}` using dot-hierarchy. (3) `portfolio_doc_name` is the sole conformant casing pattern for `DEV-*` planning doc filenames.
**reasoning**: Registering in ONS rather than just DEV-ACCORD makes the doc types visible to all tools that consume ONS — including the GC SDK validator and any future LSP. The `portfolio` domain is distinct from `governance` (PASS records), `product` (runtime namespaces), and `agentic` (agent identifiers). Canonical name form uses lowercase dot-hierarchy (`portfolio.planning.dev-path`) per existing product/agentic domain conventions, even though the filename form uses UPPER-KEBAB — this mirrors how other languages separate identifier form from wire/storage form.

---

## GC-PASS-0010.00 — 2026-06-27

**pass_id**: GC-PASS-0010.00
**timestamp**: 2026-06-27T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: all DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS files across the portfolio; validate-planning.ps1; projects.yaml consumers; all agents reading planning docs

**what**: DEV-ACCORD.00 (GC:2008) — Planning Document Standard cluster header. Declares the canonical planning doc types (DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS, all DEV-prefixed), the H1 naming rule (`# {DOC-TYPE} — {Project-Scope}` with em dash U+2014), disambiguation rule, canonical doc rule (exclusive content ownership per type), append-only constraint for DEV-PATH, and the full validation contract. Enforced by validate-planning.ps1 at c:\dev root.
**why**: Planning docs across 20+ portfolio projects had no governing standard. H1 format was inconsistent (hyphens vs em dash, reversed order, missing doc type prefix). Two files shared the exact same H1 causing agent disambiguation failures. No validator existed — drift was discovered manually, session by session. TRACKS.md did not follow the DEV- prefix convention.
**new_constraints**: (1) H1 MUST be `# {DOC-TYPE} — {Project-Scope}` — type-first, em dash separator, unique scope. (2) Canonical doc types are DEV-PATH, DEV-PLAN, DEV-RELEASE, DEV-TRACKS — TRACKS.md is legacy and must be migrated. (3) DEV-PATH is append-only; H1 conformance corrections are the only permitted non-append edit. (4) validate-planning.ps1 is now the DEV-ACCORD conformance gate.
**reasoning**: H1 format was patched manually in multiple sessions without a mechanism to prevent recurrence. A GC standard makes the rule citable, enforceable, and portable. Em dash was chosen over hyphen because hyphens appear inside project names and are syntactically ambiguous as separators. DEV-TRACKS over TRACKS aligns the naming convention with all other doc types. AUTHORITY LEVEL and Status are warnings (not errors) to avoid burying real errors under legacy debt noise.

---

## GC-PASS-0009.00 — 2026-06-20

**pass_id**: GC-PASS-0009.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (ECO: and GC: namespaces, CANON cluster complete), eco (ECO: namespace, initial registry)

**what**: CANON.03 accepted as the Migration Protocol for eco and GC as CANON first-adopters. Formally reverses unauthorized named-cluster-only rule (agent drift, pre-2026-04-12, ACES.01 Inv#6 and Inv#14 violated, no governance record). Declares ECO: namespace (prefix ECO, owner jj-ervin, authority jj-ervin, 5 active layer bands: authority 0000-0999, operational 1000-1999, domain 2000-2999, platform 3000-3999, data-interop 4000-4999, reserved 9000-9999). Declares GC: namespace (prefix GC, owner jj-ervin, authority jj-ervin, 4 active layer bands: authority 0000-0999, operational 1000-1999, standards 2000-2999, platform 3000-3999, reserved 9000-9999). Declares assignment algorithm (8 rules A-1 through A-8 governing layer-band mapping, chronological ordering, cluster-header priority, legacy supersession, gap permission). Declares legacy ID mapping rules and conflict resolution rules (4 rules C-1 through C-4). Assigns GC: canonical IDs: GC:0001 (GC.00 charter), GC:1001-1002 (APO.00, ATP.00), GC:2001-2004 (CANON.00-03), GC:2005-2007 (ONS.00-02). Assigns ECO: canonical IDs: ECO:0001-0007 (ACES.00-06), ECO:1001-1003 (OG.00-02), ECO:1004-1007 (RT.00, EV.00, OPS.00, REM.00). Resolves CANON bootstrap condition: GC:2004 = CANON.03 (self-assigned, explicitly authorized and documented). Declares follow-on implementation task for remaining ~150+ eco PASSes, governed by A-1 through A-8 with no additional governance PASS required. Produces companion artifacts: governance-commons/passes/{namespace.yaml, layers.yaml, passes.registry.json, passes.registry.changelog.jsonl} (GC: namespace, 10 initial entries); eco/passes/{namespace.yaml, layers.yaml, passes.registry.json, passes.registry.changelog.jsonl} (ECO: namespace, 14 initial entries). CANON cluster is now complete: CANON.00-03 accepted, GC:2001-2004 assigned, bootstrap resolved.
**why**: CANON.00-02 established the canonical identifier standard but could not assign IDs (bootstrap condition). CANON.03 is the authorized migration act that executes the first-adopter assignments and formally closes the drift issue that prompted CANON's creation. Without CANON.03, the system remains in the bootstrap state — the standard exists but no canonical IDs are assigned.
**new_constraints**: All future ECO: and GC: assignments must follow Rules A-1 through A-8. Legacy ID mapping rules govern how legacy numbered forms are preserved. The follow-on migration task for remaining eco PASSes requires allocation authority authorization per assignment block (R-AA-1). No canonical IDs may be assigned outside a migration PASS or its follow-on continuation artifact. The OPS.00 duplicate-supersedes typo in CANON.03 line 479 was corrected before commit; the registry (passes.registry.json) has the correct entry.

---

## GC-PASS-0008.00 — 2026-06-20

**pass_id**: GC-PASS-0008.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (all adopters), passes/canon/CANON.02.md, schemas/canon-registry-entry.schema.json

**what**: CANON.02 accepted as the normative Registry Governance specification. Declares: registry file format (JSON required, YAML permitted; passes.registry.json naming; one file per namespace; entries array is sole authority); full entry schema (14 required fields: id, alias, legacy_ids, title, layer, cluster, parent, status, timestamp, path, supersedes, superseded_by, depends_on, originating_pass; 6 optional standard fields; extension model via lowercase namespace-prefixed keys); status taxonomy (proposed, draft, accepted, sealed, superseded, reserved; 4 transition rules; superseded is terminal); write authority enforcement (allocation_authority from namespace.yaml; agents require authorizing PASS for binding writes; changelog written atomically; automation authorized by PASS; extends GC-CONSTRAINT-001 to registry writes); schema validation contract (11 pre-write checks; CRITICAL/ERROR/WARN error taxonomy); append-only changelog (.jsonl format; 5 required fields; 5 action values; CI-enforced append-only); CI integration contract (9 required checks; violation reporting format; build fails on CRITICAL/ERROR); dependency validation (same-namespace MUST resolve; cross-namespace via external_registries; superseded dependency is WARN; circular deps are CRITICAL; known_superseded_dependencies suppression); registry-as-governed-artifact (version control is provenance; every write traceable to PASS; schema changes require CANON amendment; $canon_version mismatch is CRITICAL). Companion artifact published: schemas/canon-registry-entry.schema.json (JSON Schema draft/2020-12, additionalProperties: true for extensions). 44 normative rules across 9 rule families.
**why**: CANON.01 specified how identifiers are formed and governed; CANON.02 specifies how the registry that records those identifiers is structured, validated, and protected as governed infrastructure. Without CANON.02, an adopter has rules for IDs but no governed place to store them.
**new_constraints**: All CANON-conformant registries must declare $canon_version: CANON.02. Agents must not write binding registry entries without an authorizing PASS (R-WA-2). Changelog is append-only (R-CL-2). CI must run all 9 required checks on registry-touching commits (R-CI-1 through R-CI-9). Schema file changes require a CANON amendment PASS (R-GA-3).

---

## GC-PASS-0007.00 — 2026-06-20

**pass_id**: GC-PASS-0007.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (all adopters), passes/canon/CANON.01.md

**what**: CANON.01 accepted as the normative PASS Identifier Governance specification. Declares canonical ID grammar (^[A-Z]{2,6}:[0-9]{4}$, ABNF, 7 validity rules), ONS conformance rule (NAMESPACE matches governance_cluster pattern; canonical ID is conformant specialization of qualification_authority), namespace declaration specification (namespace.yaml, 8 required fields, 4 ownership rules), layers declaration specification (layers.yaml, 3 required fields per entry, 7 normative rules, ECO: reference grammar as informative), alias model (named-cluster and legacy alias types, namespace-scoped resolution, 4-step resolver protocol, 6 rules), allocation authority model (traceability, delegation, range reservation, 7 rules), sub-pass relationship model (flat IDs only, parent and cluster as registry fields, 5 rules), immutability specification (immutable at assignment not at sealing, 4-step supersession protocol, 7 rules), and normative requirements summary (37 rules across 7 rule families).
**why**: CANON.00 declared the format and principles; CANON.01 is the normative external-facing specification that adopting organizations implement. Without CANON.01, adoption requires inferring rules from CANON.00's prose — producing inconsistent implementations.
**new_constraints**: All canonical ID assignments MUST conform to R-ID-1 through R-ID-7. Alias resolution MUST be namespace-scoped (R-AL-6). ID assignments MUST trace to a PASS decision (R-AA-1). Superseded PASSes MUST remain in the registry permanently (R-IM-6). CANON.02 (registry governance) is required before any conformant registry can be declared complete.

---

## GC-PASS-0006.00 — 2026-06-20

**pass_id**: GC-PASS-0006.00
**timestamp**: 2026-06-20T00:00:00Z
**change_type**: build
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons (all adopters), eco (first organizational adopter), registry/clusters.yaml, passes/canon/CANON.00.md

**what**: CANON cluster established. CANON.00 accepted as the founding record of the Canonical PASS Identifier Standard. Declares the canonical ID format (NAMESPACE:NNNN), alias model (named cluster IDs are ergonomic aliases, never stable citation targets), immutability rule (IDs never move or are reused — mistakes corrected by supersession), layer band grammar (per-namespace declaration; ECO: reference grammar: 0000s authority, 1000s operational, 2000s domain, 3000s platform, 4000s data/interop, 9000s reserved), registry minimum model (id, alias, legacy_ids, title, layer, cluster, parent, status, timestamp, path, supersedes, superseded_by, depends_on), external adopter model (self-declared prefix, no GC registration required), and 8 cluster invariants (CANON-CI-1 through CANON-CI-8). CANON cluster registered in registry/clusters.yaml. Four-PASS cluster structure declared: CANON.00 (header), CANON.01 (ID governance), CANON.02 (registry governance), CANON.03 (eco migration). Bootstrap condition acknowledged: CANON.00 has no canonical ID until CANON.03 assigns it.
**why**: Two compounding failures required a governing standard: (1) unauthorized agent drift — the named-cluster-only rule in eco's PASS-INDEX was written without a governing decision or founder sign-off; (2) portability gap — named cluster identifiers (ACES.01, OG.02) are opaque outside eco, making PASS records non-portable for external GC adopters. Neither failure could be resolved by a passchangelog entry alone.
**new_constraints**: All future PASS identifier assignments must follow CANON-CI-8 (migration is governed — no casual number assignment outside a migration PASS). The registry is a governed artifact per CANON-CI-5. No canonical IDs may be assigned until CANON.01 and CANON.02 are accepted and CANON.03 executes migration.

---

## GC-PASS-0005.00 — 2026-06-07

**pass_id**: GC-PASS-0005.00
**change_type**: governance
**authority_level**: AL:2
**summary**: PASS-2 Batch 2 delivery. Closed GC-3-A-03 (zero-trust spec).
Published `governance/zero-trust.yaml` — the normative zero-trust security
specification for Governance Commons multi-agent systems. Covers three pillars:
(1) Establishment — four-phase per-interaction trust protocol (dossier retrieval,
status/expiry validation, public key extraction from crypto_identity.did or
public_key, Ed25519 JWS signature verification against canonical payload) with
caching rules (TTL 300s, mandatory re-validation on each use, immediate
invalidation on revocation signal); (2) Rotation — re-key event procedure
(new key generation, dual-sign transition envelope proving identity continuity,
PASS entry with change_type security, telemetry registry_updated event,
24-hour transition window, secure old-key deletion); rotation triggers
(scheduled 90-day recommended / 365-day maximum, operator-directed,
algorithm-deprecation); (3) Revocation — five triggers (compromised,
decommissioned, authority_withdrawn, superseded, policy_violation), six-step
procedure (immediate signing halt, dossier status → revoked, PASS entry,
propagation, in-flight envelope rejection, session termination), 30-second
clock-skew tolerance for revocation timestamp. Key material handling rules
(no private key in artifacts, secure storage, single-use-per-agent, CSPRNG
requirement, secure deletion). Conformance profiles (advisory / standard /
strict) with per-level enforcement requirements. Residual risks table pointing
to PASS-3 key registry, real-time revocation, and transport binding work.
**status**: ACCEPTED
**affected_specs**: governance-commons

---

## GC-PASS-0004.00 — 2026-06-07

**pass_id**: GC-PASS-0004.00
**change_type**: governance
**authority_level**: AL:2
**summary**: PASS-2 Batch 1 delivery. Closed GC-3-A-01 (handoff envelope JWS/Ed25519
signature schema), GC-3-A-02 (agent identity DID-compatible binding), and GC-3-B-06
(STRIDE threat model for multi-agent systems). Agent-dossier spec advanced to v1.3.0:
new `crypto_identity` block in identity_block (did or public_key in base58btc/multibase);
new `signature_block` in handoff_protocol (EdDSA algorithm, protected_header, signature,
key_hint; strict profile mandates signature on all envelopes); updated schemas
(`agent-dossier-instance.schema.json`, `handoff-envelope.schema.json`) and new
`handoff-envelope-signature.schema.json`. Governance Commons root: `governance/`
directory created; `governance/threat-model.md` published covering all six STRIDE
categories (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service,
Elevation of Privilege) with concrete multi-agent threat entries, normative mitigations
cross-referenced to agent-dossier spec and multi-agent.yaml (T-001 through T-006),
and a residual risk table pointing to PASS-3 zero-trust key infrastructure work.
**status**: ACCEPTED
**affected_specs**: agent-dossier, governance-commons

---

## GC-PASS-0003.00 — 2026-06-07

**pass_id**: GC-PASS-0003.00
**change_type**: governance
**authority_level**: AL:2
**summary**: Published `docs/observability-contract.yaml` — the ecosystem-level OpenTelemetry
semantic conventions for all `gc.agent.*` instrumentation. Defines required span attributes
(`gc.agent.id`, `gc.agent.class`, `gc.agent.dossier_version`, `gc.agent.event_type`,
`gc.trace_id`, `gc.event_id`, `gc.time_loc`, `gc.severity`, `gc.summary`), OTel severity number
mapping (debug→1/TRACE, info→9/INFO, warning→13/WARN, error→17/ERROR, critical→21/FATAL), log
record field conventions, metric conventions, and 7 compliance rules (obs-1 through obs-7).
Enforces DDR-6 L3: `gc.time_loc` is required on every `gc.agent.*` event; consumers MUST reject
events without it. Closes GC-3-E-01.
**status**: ACCEPTED
**affected_specs**: agent-dossier, agent-project-orchestrator, governance-commons

---

## GC-PASS-0002.00 — 2026-06-05

**pass_id**: GC-PASS-0002.00
**change_type**: governance
**authority_level**: AL:2
**summary**: Established unified per-repo planning structure across all four core spec repos. Each spec (agent-dossier, agent-matrix, ons, agent-project-orchestrator) now has DEV-PATH.md, DEV-PLAN.md, TRACKS.md, and passchangelog.md under AL:1 authority. Stale planning files in agent-project-orchestrator (DevPath-v1.0.md, DevPlan-v1.0.md, Tracks.md) replaced with canonical-format equivalents. ROADMAP.md in agent-dossier retired; deferred items carried forward in agent-dossier DEV-PLAN.md.
**status**: ACCEPTED
**affected_specs**: agent-dossier, agent-matrix, ons, agent-project-orchestrator

---

## GC-PASS-0001.00 — 2026-06-05

**pass_id**: GC-PASS-0001.00
**change_type**: governance
**authority_level**: AL:2
**summary**: Governance Commons ecosystem planning infrastructure declared. DEV-PATH.md (ecosystem phases, authority model, design decisions DDR-1 through DDR-5), DEV-PLAN.md (execution plan, gap analysis checklist, charter and process), TRACKS.md (portfolio overview, dependency map), projects.yaml (machine-readable project registry with compat: fields), tools/gc-status.ps1 (status dashboard), docs/ (charter, architecture, rfc, conformance), and tools/ directory structure established at governance-commons root. PASS-0 bootstrap phase initiated. Five design decisions from source_102 answered and recorded as binding AL:2 decisions.
**status**: ACCEPTED
**affected_specs**: governance-commons

---

## GC-PASS-0006.00 — 2026-06-16

**pass_id**: GC-PASS-0006.00
**change_type**: governance
**authority_level**: AL:2
**status**: ACCEPTED
**affected_surfaces**: governance-commons profiles/, dxp-org/dvp (new repo unblocked)

**what**: PASS-6 formally opened. Scope: optional category-defining profiles and the Doc Vault
Plane (DVP) capability track. gc.profile.doc-vault v0.1.0 (committed 2026-06-15, 674ac0f) is
accepted as the PASS-6 seed artifact. DVP repository creation is now unblocked.

**why**: gc.profile.doc-vault was developed and committed during the Osprey LLC vault setup
session on 2026-06-15. The work proved that GC profiles for non-code repositories are viable
and that document governance is an accessible adoption wedge. PASS-6 scope was fully documented
in DEV-PLAN.md (added 2026-06-15) but could not begin formally without AL:2 sign-off.
The OSS baseline is frozen at PASS-5 Batch 2; PASS-6 extends without modifying it.

**new_constraints**:

- All PASS-6 profiles must use "aligned with," "informed by," "supports readiness for" language.
  No profile may claim compliance, certification, or audit-readiness.
- Validator code belongs in DCP, not in GC profile definitions.
- gc.profile.code-repo must reconcile with existing agent-dossier/agent-matrix work before build.
- gc.profile.agent-vault scope must be evaluated as a sub-component of all profiles vs.
  standalone before committing to a standalone build.
- DVP is a separate product from DCP; it must not modify DCP or absorb DCP scope.

**reasoning**: The PASS-6 boundary (optional profiles as extensions, not baseline changes)
was established during the OSS freeze decision (2026-06-09, PASS-5 Batch 2). Opening PASS-6
does not reopen the baseline. The Osprey session proved the doc-vault concept end-to-end with
a real entity — that is sufficient evidence to open the track. DVP creation was explicitly
listed as blocked on this sign-off; unblocking it was the primary trigger for this entry.

---

## GC-PASS-0013.00 — 2026-06-28

**pass_id**: GC-PASS-0013.00
**change_type**: governance
**authority_level**: AL:1
**summary**: Accepted DEV-ACCORD.04 (GC:2012), the Agent Bootstrap Standard. Declares
`AGENTS.md` as the canonical GC cross-agent bootstrap file, defines runtime-specific files
such as `CLAUDE.md` as adapters rather than governance authorities, and prohibits universal
auto-discovery claims unless backed by runtime-specific evidence. Clarifies that GC defines
what conformant agents must read; vendor and host runtimes determine whether that file is
auto-discovered.
**status**: ACCEPTED
**affected_specs**: DEV-ACCORD, agent onboarding, agent bootstrap files

---

<!-- New entries go above this line, newest first -->
