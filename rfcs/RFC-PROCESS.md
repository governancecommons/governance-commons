# RFC Process — Governance Commons

**Status:** Active  
**Authority:** AL:2  
**time.loc:** 2026-06-08T00:00:00Z
**Amended:** 2026-08-29 — fixed two-week delay replaced with proportional review

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
| --- | --- |
| `draft` | Author is still writing; not open for comment |
| `open-for-comment` | A declared public review window is running; community feedback welcome |
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

## Review and comment window

Every RFC requires documented maintainer review before acceptance. There is no universal
minimum waiting period.

The maintainer selects and records one of two review modes in the PR description:

- **Maintainer review** — appropriate when no known external adopter or contributor is
  materially affected. The RFC may be accepted as soon as the documented review is complete
  and no unresolved objection remains.
- **Public comment** — required when a known external adopter or contributor is materially
  affected, or when the maintainer determines that the proposal's risk or reach warrants
  broader review. The PR description states the end date and the reason for the chosen period.

During a public comment window:
- Anyone may comment on the PR
- The author may revise the RFC in response to feedback
- The AL:2 maintainer may extend the window when unresolved material questions remain

After required review is complete, the maintainer merges (accepted) or closes (rejected) the
PR. Silence alone is not evidence of review; the acceptance record MUST identify the review
performed and address any substantive objections received.

---

## Acceptance and implementation

An accepted RFC is merged into `rfcs/` with status `accepted`. It becomes a binding AL:2
decision recorded in `DEV-PLAN.md` under the relevant PASS. Implementation MAY begin after
acceptance; it MUST NOT begin before.

If an RFC requires coordinated changes across multiple specs, the maintainer records a
compat-hold in `DEV-PLAN.md` until all named consumers confirm compatibility (DDR-1).

---

## 2026-08-29 maintainer correction

The original fixed two-week window was introduced during the PASS-5 bootstrap batch without
a recorded rationale, external requirement, community decision, or participating adopter
body. It also made correction of the RFC process circular: changing this process requires an
RFC, while the process itself imposed a fixed delay before that correction could take effect.

The founder and AL:2 maintainer explicitly authorized replacement of that fixed delay with the
proportional review rule above. This is a correction to a pre-adoption bootstrap process, not a
general precedent for bypassing accepted RFCs, unresolved objections, affected adopters, or
future multi-maintainer governance.

---

## Rejection and withdrawal

A rejected RFC is merged with status `rejected` and a `rejection_reason` field in the header.
Rejected RFCs are preserved for historical reference. A new RFC on the same topic must address
the reasons for rejection.

A withdrawn RFC is closed as a PR and not merged. The author may re-open as a new RFC.
