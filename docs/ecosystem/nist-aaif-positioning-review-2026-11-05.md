# NIST and AAIF positioning review — 2026-11-05

**Status:** Non-normative source reconciliation. No new GC strategy, standards
scope, affiliation, contribution, or release claim is approved here.
**Question:** Has GC addressed the concern that larger NIST and AAIF efforts
overlap its agent governance work?

## Finding

Yes, at the umbrella level. [RFC-0001](../../rfcs/RFC-0001-public-boundary-model.md)
was accepted on 2026-10-01 and explicitly treats AAIF as a close analogue. Its
Alternative 4.4 acknowledges direct Identity & Trust overlap in delegation and
permissions, rejects a scope-only defense, and records a conditional path for
contributing mature narrow artifacts. The RFC's five-layer public boundary is
accepted but remains inactive until gates G-1 through G-5 verify. The
[ecosystem landscape](standards-landscape.md) already lists the NIST AI Agent
Standards Initiative, AAIF, and NIST AI RMF. [DEV-PLAN](../../DEV-PLAN.md)
retains a strategic checkpoint before any new broad GC capability track.

The separate Registry SDK's `DEV-PLAN.md` describes its code and contract
workstream. Its lack of NIST/AAIF repositioning does not negate the umbrella
decision. The [website's ecosystem plan](../../governance-commons-www/content/plans/ecosystem-directory-observatory-2026-10-19.md)
and `/ecosystem` page provide initial orientation; they do not establish
version-by-version interoperability or an independent adoption case.

## Current external evidence

| Source | What it establishes | Limit |
| --- | --- | --- |
| [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative), updated 2026-08-14 | NIST is working on agent standards, open protocols, identity, security, and evaluation. | An initiative is not itself a published GC-to-NIST compatibility mapping. |
| [NIST NCCoE identity and authorization update](https://www.nist.gov/news-events/news/2026/09/comments-software-and-agentic-ai-identity-concept-paper), 2026-09-29 | NIST is pursuing practical agent identity and authorization work, with a DevSecOps use case. | The cited concept work is not a final interoperability standard. |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | The voluntary risk framework addresses trustworthy AI across design, use, and evaluation. | It does not exhaust NIST's agent-specific work. |
| [AAIF Identity & Trust](https://aaif.io/working-groups/identity-trust) and [Governance, Risk & Regulatory Alignment](https://aaif.io/working-groups/governance-risk-regulatory-alignment), checked 2026-11-05 | AAIF explicitly covers delegation, permission flow, agent trust, and regulatory mapping. | Working-group scope does not prove a specific GC artifact is compatible or accepted. |

The earlier claim that NIST appears mostly through AI RMF is too narrow as of
this review. The claim that AAIF addresses only infrastructure or
interoperability while GC uniquely owns agent authority is also unsupported.
The two external bodies have different institutional roles, but their work
touches overlapping technical questions. These are source-based scope
observations, not a determination that GC should merge, compete, or withdraw.

## GC overlap and bounded role

| GC surface | External overlap to test | Current honest claim |
| --- | --- | --- |
| Agent Dossier, Agent Matrix, Agent Team Protocol | NIST agent identity/authorization and AAIF Identity & Trust. | GC has its own versioned declarations and delegation rules; no external conformance or unique coverage is established by their existence. |
| Agent Project Orchestrator | NIST agent protocol work and AAIF Workflows & Process Integration. | Reference-runtime candidate under RFC-0001, not a competing universal protocol. |
| Governance Record and ConformanceReport | NIST risk evidence and AAIF governance/observability. | Potential evidence representation and validation contribution; not NIST compliance, AAIF endorsement, or proof of agent authorization. |
| Existing `governance/nist-ai-rmf-mapping.yaml` | NIST AI RMF outcomes. | A GC-authored mapping whose coverage claims need artifact-level review before public compliance language. |

## Next bounded work

1. Complete RFC-0001's A-1–A-5 implementation and G-1–G-5 activation evidence.
   Acceptance alone does not activate the public boundary.
2. Pick one independently useful GC artifact and obtain clean adopter evidence.
   Use a source-pinned fixture to test one NIST or AAIF semantic seam; record
   mismatch and unknown outcomes, not just passing examples.
3. Reassess contribution of that narrow artifact against AAIF's current
   submission criteria and demonstrated outside interest. Do not describe
   a contribution as affiliation or acceptance before the external body acts.
4. Keep the website's source-linked orientation distinct from normative
   compatibility, certification, regulatory, and release claims.

**Decision status:** RFC-0001 supplies the current accepted umbrella position.
The strategic checkpoint in `DEV-PLAN.md` remains open. This review does not
select an additional pivot or authorize a new GC capability track.
