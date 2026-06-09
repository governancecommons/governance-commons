# RFC Process — Governance Commons

**Status:** Active  
**Authority:** AL:2  
**time.loc:** 2026-06-08T00:00:00Z

---

## When an RFC is required

An RFC is required for any public-facing change to a Governance Commons standard that affects
cross-spec compatibility, normative behavior, or the ecosystem charter. Specifically:

- Adding, removing, or changing a `MUST` or `MUST NOT` rule in any spec
- Introducing a new inter-spec contract (e.g., a shared schema field, a new handoff protocol)
- Changing the conformance profile definitions (advisory / standard / strict)
- Adding or removing a spec from the GC release manifest
- Changing the authority model (AL:1 / AL:2 / AL:3) or the RFC process itself

Changes that do **not** require an RFC:

- Bug fixes that correct spec language without changing normative behavior
- Clarifications that make existing rules unambiguous without adding new requirements
- Implementation work within a single spec's AL:1 scope (those follow the spec's own devpath)
- Adding examples, test vectors, or non-normative documentation

When in doubt, open an RFC. A rejected RFC is cheap; an unreviewed breaking change is not.

---

## RFC lifecycle

```
draft → open-for-comment → accepted
                        → rejected
                        → withdrawn
```

| State | Meaning |
|-------|---------|
| `draft` | Author is still writing; not open for comment |
| `open-for-comment` | Two-week comment window is running; community feedback welcome |
| `accepted` | AL:2 maintainer accepted the RFC; implementation may begin |
| `rejected` | RFC was reviewed and declined; reason recorded in the file |
| `withdrawn` | Author withdrew before or during comment window |

---

## Numbering and file naming

RFC numbers are assigned sequentially starting from `RFC-0001`. Number `RFC-0000` is reserved
for the process template.

File name format: `rfcs/RFC-NNNN-<slug>.md`

- `NNNN` is zero-padded to four digits
- `<slug>` is a short lowercase kebab-case description (e.g., `handoff-envelope-v2`, `add-atp-to-v1-3`)

Request a number by opening a GitHub issue in `governancecommons/governance-commons` with the
title `RFC: <slug>`. The maintainer assigns the next available number.

---

## Required sections

Every RFC file MUST include the following sections (use `RFC-0000-template.md` as a starting point):

1. **Header block** — RFC number, title, status, author, created date, target spec(s)
2. **Problem statement** — What is broken, missing, or needs changing, and why it matters
3. **Proposal** — The specific change being proposed, including normative language where applicable
4. **Alternatives considered** — Other approaches evaluated and why they were not chosen
5. **Prior art** — Relevant external standards, prior GC decisions, or related RFCs
6. **Compatibility impact** — Whether this is breaking; which specs and adopters are affected
7. **Implementation notes** — Optional guidance for implementers; not normative

---

## Comment window

Once an RFC is marked `open-for-comment`, a **two-week** comment window begins. The PR
description MUST include the comment window end date.

During this window:
- Anyone may comment on the PR
- The author may revise the RFC in response to feedback
- The AL:2 maintainer may extend the window for complex proposals

After the window closes, the maintainer merges (accepted) or closes (rejected) the PR.
An RFC that receives no substantive objection and no requests for extension is eligible
for acceptance at window close.

---

## Acceptance and implementation

An accepted RFC is merged into `rfcs/` with status `accepted`. It becomes a binding AL:2
decision recorded in `DEVPLAN.md` under the relevant PASS. Implementation MAY begin after
acceptance; it MUST NOT begin before.

If an RFC requires coordinated changes across multiple specs, the maintainer records a
compat-hold in `DEVPLAN.md` until all named consumers confirm compatibility (DDR-1).

---

## Rejection and withdrawal

A rejected RFC is merged with status `rejected` and a `rejection_reason` field in the header.
Rejected RFCs are preserved for historical reference. A new RFC on the same topic must address
the reasons for rejection.

A withdrawn RFC is closed as a PR and not merged. The author may re-open as a new RFC.
