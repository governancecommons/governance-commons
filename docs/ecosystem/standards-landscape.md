# Governance Commons Standards & Ecosystem Landscape

**Status:** Initial research inventory
**Last verified:** 2026-09-30
**Purpose:** Establish the first public-facing inventory of external standards, protocols, organizations, and research ecosystems that GC should monitor, crosswalk, align with, or contribute to.

This is a living document. It is not a ranking.

## 1. Agent standards and ecosystem coordination

| Entity / work | Scope | GC relationship | Initial action |
| --- | --- | --- | --- |
| NIST AI Agent Standards Initiative | Industry-led standards, open protocols, agent interoperability and security coordination, gap analysis | REFERENCE + CROSSWALK + RESEARCH | Track outputs; map GC concepts to NIST work; distinguish guidance/research from normative standards. |
| Agentic AI Foundation (AAIF) | Open agent ecosystem; Identity & Trust, Observability & Traceability, Governance/Risk/Regulatory Alignment, Security & Privacy, Accuracy & Reliability, Workflows & Process Integration, Taxonomy & Landscape | REFERENCE + CROSSWALK + RESEARCH + CONTRIBUTE | Treat as a major ecosystem coordination point; monitor working groups and identify mature GC material suitable for contribution. |
| Agent Governance Foundation / AAP | Agent authorization/governance including delegation, revocation, policy, audit/provenance, and authorization decisions | CROSSWALK + RESEARCH + INTEROPERATE | Compare authorization/delegation semantics with ATP, Agent Matrix, Governed Event, and Governance Record. Avoid duplicating authorization machinery without evidence of a gap. |
| Model Context Protocol | Agent/tool/resource interoperability | ALIGN + INTEROPERATE + CROSSWALK | Map MCP interactions and tool scopes to GC governance/evidence boundaries. |
| Agent2Agent | Agent-to-agent interoperability and task exchange | ALIGN + INTEROPERATE + CROSSWALK | Map A2A task lifecycle and interaction evidence into GC governed-event research. |
| Linux Foundation | Neutral/open-source project hosting and ecosystem infrastructure | REFERENCE + RESEARCH | Monitor as a potential home for mature interoperable artifacts. |

## 2. Identity, credentials, and provenance

| Entity / work | Scope | GC relationship | Initial action |
| --- | --- | --- | --- |
| W3C Verifiable Credentials | Machine-verifiable digital credentials and credential exchange | ADOPT + ALIGN + CROSSWALK | Treat credentials and attestations as possible evidence inputs rather than inventing another credential mechanism. |
| W3C DID ecosystem | Decentralized identifiers | REFERENCE + ALIGN + CROSSWALK | Map identity evidence to GC entity identity and governed-event context where useful. |
| C2PA | Content provenance and authenticity, Content Credentials, attestations | REFERENCE + CROSSWALK + RESEARCH | Study provenance chains as a model for evidence/history representation beyond media. Do not claim equivalence between C2PA provenance and GC governance evidence. |

## 3. Observability and telemetry

| Entity / work | Scope | GC relationship | Initial action |
| --- | --- | --- | --- |
| OpenTelemetry | Vendor-neutral telemetry and semantic conventions; emerging AI-agent observability conventions | ALIGN + INTEROPERATE + CROSSWALK | Keep telemetry separate from governance semantics; map observations/events into governed-event/evidence representations where justified. |

## 4. Security

| Entity / work | Scope | GC relationship | Initial action |
| --- | --- | --- | --- |
| OWASP GenAI Security Project | Security risks and practical guidance for generative and agentic AI | REFERENCE + CROSSWALK + WARN | Map security findings to governance evidence and lifecycle events; preserve OWASP scope and terminology. |

## 5. AI governance, management, risk, and impact

| Entity / work | Scope | GC relationship | Initial action |
| --- | --- | --- | --- |
| ISO/IEC 42001 | AI management systems | REFERENCE + CROSSWALK | Maintain existing GC mapping and distinguish management-system requirements from technical agent governance. |
| ISO/IEC 42005 | AI system impact assessment | REFERENCE + CROSSWALK + RESEARCH | Investigate how impact-assessment evidence can be represented without turning an impact assessment into an authorization decision. |
| ISO/IEC 23894 | AI risk management guidance | REFERENCE + CROSSWALK | Map risk-management concepts to GC evidence/interpretation boundaries. |
| NIST AI Risk Management Framework | AI risk management framework | REFERENCE + CROSSWALK | Maintain existing GC mapping; distinguish risk-framework guidance from runtime authorization or event evidence. |
| EU AI Act ecosystem | Law/regulation and associated standards/guidance | REFERENCE + CROSSWALK + WARN | Explain legal requirements and standards relationships with explicit source/date context; never present GC as legal advice or regulatory authority. |

## 6. Standards infrastructure

GC should maintain a selective reference set for:

- IETF — Internet protocols, security, identity, authorization, and related standards.
- W3C — Web standards, identity, credentials, and interoperability.
- IEEE — technical standards and professional/engineering communities.
- OASIS — enterprise, security, and interoperability standards.
- ETSI — European ICT and digital standards.
- CEN/CENELEC — European standardization relevant to AI and regulatory implementation.
- ISO/IEC JTC 1/SC 42 — international AI terminology, governance, risk, and management standards.

These should be crosswalked selectively by topic rather than presented as a flat directory.

## 7. Research and evaluation ecosystem

GC should maintain a research index covering:

- academic AI and agent research;
- security research;
- evaluation and benchmark projects;
- reliability and robustness research;
- human-agent interaction research;
- provenance and information-integrity research;
- agent identity and authorization research;
- observability and telemetry research.

Prefer primary papers, standards, technical reports, official project repositories, and reproducible artifacts.

## 8. GC's own work

GC's work should appear beside external work, not above it.

| GC artifact/concept | Primary ecosystem questions |
| --- | --- |
| Agent Dossier | identity, declaration, evidence |
| Agent Matrix | capabilities, routing, identity, constraints |
| Agent Team Protocol | delegation, trust boundaries, revocation |
| APO | execution/orchestration reference runtime |
| ONS | naming/identity interoperability |
| Governance Record | durable governed evidence |
| ConformanceReport | validation/conformance evidence |
| Governed Event | event boundary for governance-relevant evidence |
| time.loc | temporal/provenance context |
| Evidence ≠ Authority | prevents evidence from silently becoming authority |
| Meaning ≠ Metric | prevents measurements from silently becoming universe meaning |
| Diagnostic Non-Dispositive | prevents diagnostics from silently becoming decisions |
| Non-Exhaustiveness / Anti-Authority | prevents GC from claiming the ecosystem is exhausted or GC-owned |
| Provenance-bounded claims | keeps conclusions tied to evidentiary scope |

## 9. Initial interoperability hypothesis

GC should investigate, without assuming it is already implemented:

**External identity / authorization / execution / observability systems → governed events → GC evidence record → bounded interpretation**

This does not make GC the authority that issued an authorization, executed an action, or generated telemetry.

A useful question is:

> **What can legitimately be established from the combined evidence, and what cannot?**

This is where Governed Event, time.loc, Governance Record, and the evidence/authority distinction may provide a complementary layer across otherwise different ecosystems.

## 10. Decision rule for future additions

A new ecosystem project should be added when it materially helps answer at least one of:

1. Who or what is being identified?
2. What is being authorized?
3. What can an actor or system do?
4. What happened?
5. When did it happen?
6. What evidence supports the claim?
7. How is provenance preserved?
8. How is risk assessed?
9. How is behavior observed or evaluated?
10. What obligations or constraints apply?
11. How do different standards interoperate?
12. What remains uncertain or contested?

The absence of an entry must never be interpreted as evidence that a project or standard is unimportant. The landscape is explicitly non-exhaustive.
