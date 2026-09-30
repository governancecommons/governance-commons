# RFC-0001 — Governance Commons Public Boundary Model

Number assigned 2026-08-29 in [governancecommons/governance-commons#1](https://github.com/governancecommons/governance-commons/issues/1). This draft is not accepted and does not activate the proposed boundary model.

---

## 1. Header block

| Field | Value |
| --- | --- |
| RFC number | `RFC-0001` |
| Title | Governance Commons Public Boundary Model |
| Status | `open-for-comment` |
| Author | jj-ervin |
| Created | 2026-08-28 |
| Target specs | Agent Dossier, Agent Matrix, ONS, Agent Team Protocol, Agent Project Orchestrator |
| Charter entries affected | `GC-CHARTER-003`, `GC-CHARTER-004` (both AL:3) |
| Coordinated multi-spec change | Yes — compat-hold applies per DDR-1 |

---

## 2. Problem statement

Governance Commons currently presents itself publicly as an umbrella over four interoperable standards. That presentation does not match the artifacts, and the mismatch is load-bearing in five specific ways.

**The umbrella name means six different things.** "Governance Commons" is simultaneously the public mission, the standards family, a published PyPI package, a local maintainer workspace, a website repository, and the GitHub organization. A prospective adopter cannot tell which one they are being asked to adopt.

**Adoption is presented as all-or-nothing.** Public language invites adopting "Governance Commons" rather than a named specification at a named version. There is no smaller unit a project can honestly claim.

**The documented adoption path does not execute.** `ADOPTERS.md` instructs adopters to verify conformance with `gc-validate --spec <spec-name>`. That command accepts only `ons` and `capabilities`. It cannot validate Agent Dossier, Agent Matrix, or Agent Project Orchestrator — three of the four advertised standards.

**The charter enumerates a component that is not a specification.** `GC-CHARTER-004` lists `agent-project-orchestrator` in the standards family. It is an application with a runtime, a CLI, and a task queue. It also validates against vendored copies of Agent Dossier's schemas rather than the published ones, so it does not currently demonstrate the specification it is grouped with.

**Version identity is not single-valued.** ONS reports different versions in its README, its canonical YAML, its schema `$id`s, and its release tag. Agent Matrix carries three simultaneous `$id` versions. There is no one number a citation can name.

Left unaddressed, each of these converts into a false public claim the moment anyone outside the project reads the material.

---

## 3. Proposal

### 3.1 A five-layer boundary

| Layer | Contents | What it is to a user |
| --- | --- | --- |
| 1. Public umbrella | Mission, standards home, shared vocabulary, publication identity | Citeable, not adoptable |
| 2. Specifications | Agent Dossier, Agent Matrix, ONS | The adoption units |
| 3. Reference tooling | GC Toolkit (validators, CLIs, SDKs) | What you install |
| 4. Publication infrastructure | `governancecommons.org`, site repositories | Where you learn and verify |
| 5. Maintainer workspace | Planning, release records, internal coordination | Not a product |

Adoption claims are scoped to a component and version — "This project uses Agent Dossier, a Governance Commons specification" — never to the umbrella. Where no tool exists to verify a claim, the claim is marked manual, provisional, or not yet verifiable.

### 3.2 Normative changes proposed

| # | Change | Target |
| --- | --- | --- |
| A-1 | Agent Project Orchestrator is reclassified from standard to **reference-runtime candidate**, earning the label only once it consumes canonical released Agent Dossier schemas. Vendoring remains permitted for offline use where each vendored schema records its release tag, immutable commit SHA, schema path, and content digest, with automated drift detection. | `GC-CHARTER-004` |
| A-2 | The compatibility table is split into **normative standards compatibility**, from which umbrella releases are derived, and **non-normative "tested with"** runtime and tooling versions. `min_orchestrator_version` no longer determines an umbrella standards release. Umbrella releases are generated or validated from component compatibility data, not hand-authored. | `GC-CHARTER-004`, Agent Matrix schema |
| A-3 | PyPI `governance-commons` is recorded as a **transitional exception**, ending once a GC Toolkit package exists at functional parity with migration documentation, and the old package has carried a deprecation notice for at least one release cycle. npm uses a scoped name such as `@governancecommons/toolkit`. | `GC-CHARTER-003` |
| A-4 | The third-party name-use restriction is replaced with a naming policy that **permits accurate nominative statements** ("compatible with Agent Dossier") while **prohibiting implied endorsement, certification, or official affiliation**. The policy states plainly that no certification program currently exists. | `GC-CHARTER-003` |
| A-5 | Agent Team Protocol's `trust_levels` is renamed `delegation_tiers`, and a normative composition rule is added: (1) a delegation grant may include only authority the delegator holds under Agent Matrix, and the recipient must satisfy Agent Matrix trust requirements for every delegated capability; (2) prohibited-action and `requires_human_approval_for` constraints remain attached to the delegated action and may not be weakened or bypassed. | Agent Team Protocol, inter-spec contract |

### 3.3 Two milestones

Acceptance authorizes the transition. It does not activate it.

| Milestone | Effect |
| --- | --- |
| **RFC acceptance** | Implementation of A-1–A-5 and G-1–G-5 is authorized. Existing public classification remains in effect. The RFC describes a pending transition. Compat-hold recorded in `DEV-PLAN.md` per DDR-1. |
| **Activation and publication** | Occurs only after G-1–G-5 verify. The boundary model becomes effective public doctrine. |

Activation gate:

| # | Condition |
| --- | --- |
| G-1 | Agent Dossier canonical schema URLs resolve |
| G-2 | Agent Matrix has an actual license file |
| G-3 | ONS canonical version surfaces agree |
| G-4 | The website accurately presents the three-member family |
| G-5 | The Agent Matrix compatibility row no longer references a nonexistent Agent Dossier version |

G-4 and G-5 are implementation-dependent and cannot precede acceptance; G-1 through G-3 may proceed independently. The gate permits honest publication. It does not establish clean adoptability — Agent Matrix's failing CI and non-validating examples sit outside it by design and remain disclosed defects after activation.

---

## 4. Alternatives considered

### 4.1 Monolithic installable product

Governance Commons as one thing a user installs and adopts wholesale.

**Rejected.** It maximizes the cost of trying any part of the work. A team that wants only agent identity declarations would have to accept routing, naming, orchestration, and evidence discipline to get it. It also contradicts `GC-CHARTER-004`'s standard-independence invariant, which is AL:3 precisely because collapsing independence would force all standards and all adopters to migrate simultaneously.

### 4.2 Loose brand with no umbrella releases

Governance Commons as naming only, with no coordinated compatibility milestones.

**Rejected.** It removes the one thing an adopter most needs from a multi-component family: a statement of which versions are known to work together. The existing compatibility table already does this job; discarding it would trade a solvable coordination problem for an unsolvable integration problem, and would leave cross-spec claims like Agent Team Protocol consuming Agent Matrix with nowhere to be recorded.

### 4.3 Internal maintainer governance only

No public standards family; the specifications remain workspace doctrine.

**Rejected, but it is the honest fallback.** This is a genuinely defensible option — the work already functions as governance tooling for a single multi-agent workflow, and it has no external adopters to disappoint. It is rejected because the specifications contain material with plausible external value that internal-only status would strand, and because artifacts are already published to PyPI, GitHub releases, and a public website. Withdrawing to internal-only is now a de-publication exercise, not a default. **If the activation gate proves unreachable, this alternative should be reconsidered rather than shipping a boundary model over unfetchable specifications.**

### 4.4 Contribute to an existing umbrella instead of maintaining one

Fold the differentiated material into an established vendor-neutral foundation rather than operating a separate umbrella.

This alternative was not in the original set and was surfaced by the prior-art research below. It is included because reviewers are likely to ask it first.

The Agentic AI Foundation hosts Model Context Protocol, goose, and AGENTS.md; Agent2Agent was accepted as a hosted project on **2026-08-17**. As of the membership announcement of 2026-08-12 it comprises **247 member organizations**. Its working groups overlap Governance Commons directly — including **Identity & Trust**, **Observability & Traceability**, **Governance/Risk/Regulatory Alignment**, and **Taxonomy & Landscape**.

**A scope-based defence is not available.** AAIF's Identity & Trust working group explicitly covers delegation protocols and permission flow. Any argument that AAIF concerns interoperability while Governance Commons concerns authority is disproved by AAIF's own program and MUST NOT be used in this RFC.

**Position: reject wholesale folding as the immediate path.** Governance Commons will operate as a maintainer-led sociotechnical specification incubator, will not claim foundation-grade neutrality, and will treat contribution of mature narrow artifacts to AAIF as a desired downstream path. Formal contribution is to be reconsidered after activation, clean adoptability of at least one component, and evidence of outside interest or participation.

This rests on present readiness, mission, and operating model — not on a scope distinction. AAIF's published project criteria expect demonstrated adoption and implementation quality, a contributor community, clear governance and security practices, and a realistic 6–12 month roadmap, and look for projects "healthy enough to grow beyond one company or one maintainer group."

Governance Commons does not presently satisfy AAIF's demonstrated-adoption and multi-maintainer community expectations: it has no recorded adopters, no independent contributors, and sole AL:3 authority vested in one maintainer per `GC-CHARTER-001`. Readiness against its remaining criteria — implementation quality, governance and security practices, and roadmap — would require a separate assessment and is not established here either way. Submission now would therefore be premature.

The three reconsideration conditions above are the honest gate. Meeting them would make contribution of a narrow artifact — most plausibly the agent authority and revocation lifecycle, or cost-aware routing metadata — a credible next step rather than a premature one.

### 4.5 The proposal

Public umbrella, independently adoptable specifications, optional tooling, and generated compatibility milestones.

**Chosen** because it is the only option that preserves component independence, permits partial adoption, matches how comparable ecosystems are structured, and can be stated honestly today with the activation gate disclosing what is not yet true.

---

## 5. Prior art

This section answers one question. It is deliberately not a feature-by-feature protocol comparison.

> How do other standards ecosystems separate the umbrella organization, independently versioned specifications, reference implementations, tooling, compatibility claims, and publication infrastructure?

### 5.1 Agentic AI Foundation — umbrella governance

Formed under the Linux Foundation in December 2025 as a vendor-neutral home for agentic AI infrastructure. Hosts MCP (contributed by Anthropic), goose (Block), and AGENTS.md (OpenAI); A2A was accepted as a hosted project on 2026-08-17. Membership stood at 247 organizations as of 2026-08-12, across tiers, with a governing board and eight working groups.

*Naming, resolved:* AAIF's governing page titles the body **Technical Committee**; "Technical Steering Committee" appears only in that page's meta description and, separately, in the A2A announcement, where it refers to A2A's own project committee rather than a foundation body. This RFC uses **Technical Committee**. The general rule stands: any reference to AAIF governance bodies MUST take its title from the specific governing document cited, not from secondary coverage.

**Relevance.** AAIF is the closest live analogue to what Governance Commons proposes to be, and it demonstrates the separation this RFC argues for: the foundation is the umbrella and the neutrality guarantee; the protocols are independently governed specifications; SDKs are separate again. It also demonstrates the cost — that separation is backed by a board, a Technical Committee, a trademark regime, and hundreds of participating organizations. A single-maintainer umbrella can adopt the *structure* but cannot claim the *neutrality*, and this RFC should not imply otherwise.

### 5.2 Model Context Protocol — version identity

MCP uses date-based identifiers (`YYYY-MM-DD`) marking the last backwards-incompatible change; the version is deliberately **not** incremented for backwards-compatible changes. Revisions carry one of three states: Draft, Current, or **Final** — "past, complete specifications that will not be changed." Individual features carry their own lifecycle, with deprecated features documenting a migration path and remaining for at least twelve months before becoming eligible for removal. Version negotiation is per-request, and clients and servers MAY support multiple versions simultaneously.

**Relevance.** This is a useful versioning precedent for the version-identity problem in Section 2, not a complete remedy: Governance Commons additionally needs one authoritative release identity per specification and synchronized publication across README, canonical file, schema `$id`, and release tag, which MCP's scheme alone does not supply. MCP has exactly one version identifier per revision, it becomes immutable at Final, and feature-level change is handled by a deprecation lifecycle rather than by version proliferation. Governance Commons currently has the inverse: multiple version claims per specification and no immutability guarantee. Note also that the Agent Matrix MCP citation is pinned to `2025-03-26` while the current revision is `2026-07-28` — several revisions stale, and predating the extensions framework and deprecation policy.

### 5.3 CloudEvents — specification and tooling separation

The core specification lives in one repository and is release-tagged. Language SDKs live in separate repositories and version independently. Protocol bindings and event formats are documented in the specification repository but are explicitly **optional**. A feature support table tracks which bindings and formats each SDK actually implements.

**Relevance.** Two transferable design precedents. First, optional bindings around a small required core is a precedent worth evaluating against Agent Matrix's 23 mandatory top-level sections, which is why its minimal example cannot validate; it is a precedent, not an automatic prescription, and the required-core boundary would still need to be designed. Second, the **feature support table** is precisely the artifact Governance Commons is missing: a published statement of which specifications GC Toolkit actually validates, which would have prevented `ADOPTERS.md` from documenting a conformance path that does not execute.

### 5.4 OpenTelemetry — independent versioning at scale

Component version tracks advance independently: the specification at 1.60.0, OTLP at 1.11.0, and semantic conventions at 1.44.0, with API, SDK, and contrib components versioned separately again per language. A published status summary declares maturity per component. Semantic convention changes such as attribute and metric renames are permitted only when describable in a schema file format published alongside.

**Relevance.** OpenTelemetry is the strongest evidence that independent versioning across an umbrella is workable at scale, and it supplies a mechanism Governance Commons lacks: machine-readable schema files **designed to support mechanical migration** between versions rather than migration by changelog.

That mechanism must not be cited as mature practice. OpenTelemetry's own stability rules state that "there is a moratorium on relying on schema transformations for telemetry stability," and the schema specification deliberately limits transformations "to the bare minimum that is necessary to handle the most common changes," explicitly declining to describe the full shape of telemetry. The lesson for Governance Commons is that a published migration mechanism is valuable even before it is load-bearing — and that independent versioning relocates coordination cost rather than removing it.

### 5.5 Agent2Agent — adjacent protocol and governance precedent

A2A defines cross-platform agent communication and task exchange, and was accepted as an AAIF hosted project on 2026-08-17.

**Relevance.** Agent Matrix's task lifecycle vocabulary already matches A2A's task states, which is genuine alignment worth preserving. The governance transfer is the more important datum: A2A's authors concluded that a neutral foundation was the right long-term home for a widely-implemented agent protocol. That is directly relevant to alternative 4.4.

### 5.6 Sources

Cited from primary sources and refreshed for review on 2026-10-01. External endpoints are point-in-time evidence and should be refreshed again before acceptance if material facts change.

**Review refresh (2026-10-01):** The AAIF submission page now describes the foundation as having **250+ member organizations**; the 2026-08-12 AAIF announcement recorded **247** members at that earlier point in time. AAIF's current Identity & Trust working-group page explicitly covers **delegation protocols, cross-domain identity, and permission flow**. AAIF's current working-group landscape also includes Governance, Risk & Regulatory Alignment, Observability & Traceability, Workflows & Process Integration, and Taxonomy & Landscape. These current pages reinforce rather than remove the overlap described in Alternative 4.4. MCP's current documented revision is **2026-07-28**, with Draft / Current / Final revision states and a documented deprecation lifecycle. CloudEvents currently lists **v1.0.2** as its latest released core specification while maintaining a working draft, and its SDK requirements continue to distinguish SDK governance from the core specification and maintain a feature-support table. OpenTelemetry's current stability documentation continues to document the schema-transformation moratorium and published schema URLs.

| Claim | Primary source |
| --- | --- |
| AAIF working groups and scope | <https://aaif.io/> |
| A2A accepted as hosted project, 2026-08-17 | <https://aaif.io/blog/a2a-joins-aaif> |
| 247 member organizations, 2026-08-12 | <https://aaif.io/news/agentic-ai-foundation-welcomes-57-new-members> |
| AAIF project submission criteria | <https://aaif.io/submit-a-project> |
| AAIF Technical Committee (body name and review role) | <https://aaif.io/submit-a-project> |
| AAIF formation and contributed projects | <https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation> |
| MCP versioning, revision states, deprecation policy | <https://modelcontextprotocol.io/docs/2026-07-28/learn/versioning> |
| CloudEvents spec and SDK separation | <https://github.com/cloudevents/spec> |
| CloudEvents SDK feature support table | <https://github.com/cloudevents/spec/blob/main/cloudevents/SDK.md> |
| OpenTelemetry component version numbers | <https://opentelemetry.io/docs/specs/> |
| OTel schema transformation moratorium | <https://opentelemetry.io/docs/specs/otel/versioning-and-stability/> |
| OTel schema scope limitation | <https://opentelemetry.io/docs/specs/otel/schemas/> |

---

## 6. Compatibility impact

**Breaking for the public presentation layer and two specification artifacts; no known released-adopter migration is expected.** A-2 changes the Agent Matrix schema, and A-5 renames an Agent Team Protocol field and adds normative behaviour. All other components are unchanged normatively.

| Affected | Impact |
| --- | --- |
| Adopters | **None recorded or known to the maintainer.** `ADOPTERS.md` lists none, and no adopter has identified themselves. Unreported use cannot be ruled out, so this is a statement about available evidence rather than a guarantee that no consumer exists. On that evidence no external migration is expected, and this is the cheapest moment to make the change; the window narrows as use grows. |
| Agent Dossier | No normative change. Version identity reconciliation only. |
| Agent Matrix | Schema change under A-2 to split the compatibility table. Existing consumers of `compatibility_table` would need to read the normative half. No other section changes. |
| ONS | No normative change. Version surfaces reconciled to a single value. |
| Agent Team Protocol | **Breaking within a pre-release specification.** `trust_levels` is renamed and a normative composition rule is added. Acceptable because ATP is v0.1 with no CI, no reference implementation, and no consumers. |
| Agent Project Orchestrator | Removed from the standards family. Retains its releases and tags; reclassified, not withdrawn. |
| GC Toolkit / PyPI | No immediate change. `governance-commons` remains published under a recorded transitional exception. |
| Website | Must be updated at activation, not at acceptance. |

**Charter impact.** `GC-CHARTER-003` and `GC-CHARTER-004` are AL:3 and require founding-maintainer approval plus new charter entries. `GC-CHARTER-004`'s standard-independence invariant is preserved, not weakened: umbrella releases remain derived and non-gating.

---

## 7. Implementation notes

Non-normative.

- **Sequence G-1 first.** The canonical schema endpoint is a hosting configuration change, and it converts every schema `$id` in the family from unresolvable to resolvable. Nothing else in the gate unblocks as much.
- **Pin A-1 against release artifacts, not the served URL.** Recording tag, commit SHA, schema path, and content digest lets drift detection work before G-1 lands, decoupling the two.
- **Draft A-1 and A-2 together.** They touch the same compatibility table from opposite directions.
- **A-5's rename is cosmetic; the composition rule is not.** The rule is a security property — without it, delegation could route around a `requires_human_approval_for` constraint. It warrants its own review attention regardless of ATP's family status.
- **Consider adopting a feature support table** for GC Toolkit, following CloudEvents. It is a small artifact that prevents a whole class of false conformance claim.
- **Consider MCP-style revision states** (Draft / Current / Final) for Governance Commons specifications. Immutability at Final is what makes a citation stable, and it is currently the property the family most visibly lacks.
