# DEV-ACCORD.02 — Execution Model: PASS, RUN, and Evidence Bundle

**PASS ID:** DEV-ACCORD.02
**Canonical ID:** GC:2010
**Cluster:** DEV-ACCORD
**Authority:** AL:1
**Status:** ACCEPTED
**Timestamp:** 2026-06-28T00:00:00Z
**Depends on:** GC:2008 (DEV-ACCORD.00)

---

## Summary

Defines the three-layer execution model governing all planned work across the
portfolio. Every agent operating under GC governance must understand PASS, RUN,
and Evidence Bundle before performing any planned work.

---

## Three-layer model

| Layer | Unit | Question it answers |
| --- | --- | --- |
| Governance | PASS | Did we agree to this? Is it done? |
| Execution | RUN | Who did what, when, in which commit? |
| Audit | Evidence Bundle | Can this be verified without repo access? |

*Phase, Wave, and Track are the structural planning containers. PASS is a governance
contract that may span them. See DEV-ACCORD.07 (GC:2015) for the planning container lock.*

---

## Controlled DEV-DOCS flow vocabulary

GC uses two separate axes:

1. **Planning structure** — where work sits in the roadmap and DEV-DOCS.
2. **Execution level** — how much governance a unit of work requires.

DEV-ACCORD recognizes only these planning and execution unit terms:

| Term | Answers | Why it exists |
| --- | --- | --- |
| Phase | What era is the project in? | Preserves product history and major evolution in `DEV-PATH.md`. |
| Wave | What delivery batch is this? | Sequences work inside a phase without pretending every track ships at once. |
| Track | What persistent workstream owns this? | Keeps CLI, schema, UI, runtime, release, docs, and similar streams distinct. |
| PASS | What governed contract defines done? | Gives humans and agents shared scope, Done-when criteria, dependencies, and closure. |
| Sub-PASS | What child contract can close or fail independently? | Splits a parent PASS only when a piece needs its own Done-when criteria. |
| RUN | What execution event happened? | Records who did work, when, in which commit, and under what PASS if any. |
| Evidence Bundle | How is the RUN or validation independently verifiable? | Carries signed or machine-checkable proof. |
| Work Item | What local planning row tracks a task? | Lets plans list small items without promoting everything to a PASS. |
| Gate | What check must pass before closure? | Prevents false closure of PASSes, releases, or RUNs. |
| Release | What packaged version or distribution target ships? | Separates shipment from internal planning progress. |

Agents must not invent new planning or execution unit types in GC-governed docs.
Any unit term not listed in the table above is invalid for DEV-ACCORD taxonomy.

DEV-ACCORD.06 adds the Change Playbook execution levels: `BUNT`, `RUN`, `DRIVE`,
and `PASS`. These are valid execution levels, not additional Phase/Wave/Track
planning units. When deciding DEV-DOCS obligations, validation, evidence, or
trailer requirements, DEV-ACCORD.06 governs.

`RUN` and `PASS` intentionally appear on both axes:

| Term | Planning / execution meaning | Change Playbook execution-level meaning |
| --- | --- | --- |
| RUN | An execution event: work happened. | A normal bounded change with local impact. |
| PASS | A governance contract: scope and Done-when are agreed. | Work whose governance weight requires PASS-level obligations. |

`Flow` is not a DEV-ACCORD governance unit. It may appear only as ordinary prose
for a user flow, command flow, data flow, or process flow. Governed work still
maps to the planning structure above and to a DEV-ACCORD.06 execution level.

If a new unit type is genuinely needed, it requires a GC amendment before use.
Until then, map the work to Phase, Wave, Track, PASS, RUN, Evidence Bundle,
Work Item, Gate, or Release.

### Status vocabulary boundary

PASS closure status is only `OPEN` or `CLOSED`.

Document lifecycle status, such as `DRAFT`, `ACCEPTED`, or `SUPERSEDED`, may
describe the governance document itself. It must not be used as PASS closure
status unless a future DEV-ACCORD amendment changes the PASS status vocabulary.

DEV-ACCORD also forbids invented status values in planning and registry docs.
Agents must use the status vocabulary declared by the artifact they are editing.
If the artifact does not declare a vocabulary, use the GC defaults:

| Scope | Allowed statuses |
| --- | --- |
| Project registry | `active`, `stable`, `wip`, `scaffold`, `archive` |
| PASS closure | `OPEN`, `CLOSED` |
| Planning work item | `planned`, `queued`, `open`, `in-progress`, `blocked`, `done`, `deferred` |
| Gap closure | `open`, `spec-complete`, `release-complete`, `runtime-complete` |
| Release | `planned`, `in-progress`, `blocked`, `released`, `deferred` |
| Document lifecycle | `draft`, `active`, `accepted`, `superseded`, `archived` |

Any status value not listed in the relevant table above is invalid unless the
target artifact explicitly declares it. Put nuance in notes or prose instead of
inventing a new status.

---

## 1. PASS — governance contract

*DEV-ACCORD.07 (GC:2015): PASS is a governance contract, not a structural planning container alongside Phase/Wave/Track. It may span multiple Tracks or Waves.*

A PASS is the planning and governance unit for significant work. It defines a
goal, declares when the work is done, and records what was built.

### PASS identity

Every PASS has two identifiers:

| Identifier | Format | Example | Purpose |
| --- | --- | --- | --- |
| Alias | CLUSTER.NN | INIT.06, DEV-ACCORD.02 | Human-readable; used in all references |
| Canonical ID | GC:NNNN | GC:2010 | Permanent, immutable registry ID |

`GC-PASS-NNNN.NN` is a **passchangelog row index** — a sequential number for
each entry in the governance changelog. It is not a PASS identity. Do not use
it to refer to a PASS in documentation, code, or cross-references. Always use
the alias (`CLUSTER.NN`) or canonical ID (`GC:NNNN`).

### Numbering

```text
CLUSTER.NN.00   Primary PASS — owns the goal, defines scope and Done-when
CLUSTER.NN.01   Sub-PASS — discrete task under the primary
CLUSTER.NN.02   Sub-PASS — discrete task
…
CLUSTER.NN.10   Compound PASS — cluster of sub-PASSes that execute in parallel
CLUSTER.NN.20   Compound PASS — another parallel execution cluster
```

The `CLUSTER.NN` prefix is always present. A bare sequence number with no
cluster is not a valid PASS identity.

### Declaring parallelism

When sub-PASSes can run simultaneously, declare it on each record:

```text
**Parallel with:** NNNN.02, NNNN.03
**Batch:** schema-work
```

Compound PASSes (.10, .20 …) name the parallel batch at the PASS level.
`Parallel with:` declares it inline at the sub-PASS level. Both are valid —
use whichever fits the work.

### Required fields for every PASS

| Field | Example |
| --- | --- |
| PASS ID | INIT.06 |
| Status | OPEN / CLOSED |
| Track | H — Evidence profiles |
| Wave | 4 — depends on INIT.05 |
| Timestamp | 2026-06-28T00:00:00Z |
| Authority | AL:1 |
| Author | jj-ervin |

### When to open a PASS

Open a PASS when work has any of:

- Explicit Done-when criteria
- More than one git commit expected
- Dependencies on other PASSes
- Multi-agent coordination need (shared contract)

### When NOT to open a PASS

Do not open a PASS for one-line fixes, typo corrections, trivial hotfixes, or
config tweaks with a single obvious commit. These are RUNs — they just do not
need a governance contract.

---

## 2. RUN — execution event

A RUN is any single execution of work, regardless of size. Every code change
is a RUN. A PASS is closed by one or more RUNs. A RUN without a PASS is valid
for trivial fixes.

### RUN record

Every RUN produces at minimum a git commit. A full RUN record:

```text
Agent:      Claude Sonnet 4.6
PASS ref:   INIT.06  (or "standalone" for trivial fixes)
Commit:     8106518
Timestamp:  2026-06-28T18:30:00Z
Output:     src/core/evidence.ts — signBundle(), verifyBundle()
```

Significant RUNs — those producing audit output, implementing security
controls, or closing a PASS — should also produce a signed evidence bundle.

### PASS + RUN relationship

```text
PASS.00  (contract: what we agreed to build)
  └── RUN.01  agent: Claude,  output: keystore.ts,   commit: 0c2c7d8
  └── RUN.02  agent: Claude,  output: evidence.ts,   commit: 0c2c7d8
  └── RUN.03  agent: Codex,   output: one-line fix,  commit: 8106518
```

The PASS is the contract. RUNs are execution. Every RUN is traceable. The
PASS is the shared surface that lets multiple agents coordinate without
guessing scope or Done-when criteria.

---

## 3. Evidence Bundle — audit record

A signed, machine-readable record of a RUN. Allows independent verification
of who ran what, when, with what result.

Key properties:

- Ed25519 / JWS compact serialization (RFC 8037, `alg: EdDSA`)
- Public key embedded in `gc-principal.yaml`; private key stays in OS config dir
- **Stranger test:** a third party with only the bundle + public key can verify
  the run without repo access
- Emitted via `marlin audit validate --evidence <dir>`

---

## Multi-agent coordination

When Claude, Codex, Copilot, or any future agent works on the same project,
the PASS is the shared contract. All agents read the same Done-when criteria,
the same track, the same wave. No agent needs to guess what done means or what
another agent built.

**Before starting any planned work, every agent must:**

1. Read the PASS for this work unit
2. Read Done-when criteria
3. Read Depends-on
4. Check whether a prior RUN already closed any sub-tasks

---

## Files changed

Doctrine-only PASS. No implementation files created. Doctrine takes effect
immediately upon acceptance.

---

## Constraints introduced

- Every agent operating under GC governance must understand PASS, RUN, and
  Evidence Bundle before performing planned work.
- PASS identity is `CLUSTER.NN` (alias) or `GC:NNNN` (canonical). `GC-PASS-NNNN.NN`
  is a passchangelog row index — never a PASS identity.
- Every PASS must carry the seven required fields listed above.
- Every code change is a RUN, including one-line fixes.
- Significant RUNs must produce a signed evidence bundle.
- The private key for signing must never appear in the repo.
