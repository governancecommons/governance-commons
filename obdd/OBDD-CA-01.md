# OBDD-CA-01 — Conformance and Assurance Annex

**Status:** Accepted<br>
**Applies to:** OBDD v1.1<br>
**Authority:** Jesse Ervin, owner and authorized approver<br>
**Approved:** 2026-10-24

In this annex, **OBDD** means Outcome-Bound Development and Delivery. The base
directive is [`GC-DD-01`](../passes/dev-accord/GC-DD-01.md), version 1.1.0,
status Accepted. Owner approval establishes the directive and this annex as the
OBDD v1.1 normative surface; it does not imply external certification.

## CA-01 — Applicable requirements

Implementations MUST identify the applicable laws, standards, organizational
policies, security requirements, and external obligations governing the
development activity.

A standard's appearance in an OBDD alignment matrix MUST NOT be interpreted as
universal applicability or certification.

## CA-02 — Traceability

Every externally mapped requirement MUST identify:

- The source, edition, and requirement identifier.
- The applicable OBDD provision.
- Whether the mapping is direct, partial, supporting, or not applicable.
- Any obligations that remain outside OBDD.
- Evidence necessary to verify implementation.
- Assessment status and responsible reviewer.

A mapping without sufficient evidence MUST NOT be represented as verified
conformity.

## CA-03 — Risk and impact assessment

An execution objective MUST receive a risk classification proportionate to its
autonomy, possible harm, security exposure, privacy implications, external
effects, and reversibility.

The classification MUST determine the appropriate level of review, testing,
authorization, documentation, and monitoring.

Applicable legal classifications MUST be determined independently of OBDD's
operational risk tiers.

## CA-04 — Agent security

Agent-executed workflows MUST enforce applicable authorization,
least-privilege, delegation, input-trust, output-verification, and tool-use
boundaries.

Untrusted external content MUST NOT be treated as instructions granting
authority.

High-impact actions MUST have explicit authorization consistent with the
applicable risk controls.

## CA-05 — Security assurance

Mandatory secure-development activities MUST NOT be waived solely to meet a
completion target.

Security findings MUST be dispositioned through an authorized process. Deferred
work MUST NOT contain an unresolved issue that prevents safe acceptance.

## CA-06 — Evidence integrity

Completion evidence MUST be traceable to actual execution, evaluation, review,
or authorized acceptance.

Implementations MUST identify the source and status of evidence.

Evidence MUST NOT be fabricated, silently altered, or represented as
independently verified when it is not.

Evidence retention and access controls MUST follow applicable organizational
and legal requirements.

## CA-07 — Human oversight

Accountable authorities MUST be identified.

Human approval requirements MUST reflect the activity's risk and applicable
obligations.

An AI agent MUST NOT approve a decision for which an independent human or other
authorized approver is required.

## CA-08 — Operational measurement

Implementations SHOULD measure whether OBDD improves successful delivery,
rework, unnecessary execution, change stability, and resource efficiency.

Where DORA metrics are adopted, they MUST retain their defined meaning and
appropriate unit of analysis.

Metrics MUST NOT replace direct acceptance evidence or become justification for
concealing defects.

## CA-09 — Regulatory applicability

Organizations subject to AI-specific regulation MUST establish their legal
role, relevant jurisdiction, system classification, applicable obligations, and
effective dates.

OBDD MUST support applicable requirements but MUST NOT claim to replace
system-level compliance assessments, technical documentation, oversight
procedures, or legally required conformity assessments.

## CA-10 — Independent assurance

Conformance claims MUST identify their assessment basis and assurance level.

Permitted labels are:

- **Designed:** Controls are documented but not implementation-tested.
- **Implemented:** Controls exist and have implementation evidence.
- **Verified:** Evidence has been evaluated against defined acceptance criteria.
- **Independently assessed:** A reviewer independent of implementation has
  evaluated the specified scope.

None of these labels implies certification under an external standard.

## CA-11 — Exceptions and compensating controls

Exceptions MUST identify the unmet requirement, rationale, risk, authority,
expiration or review condition, and compensating controls where appropriate.

An exception MUST NOT override a non-waivable legal or mandatory security
obligation.

## CA-12 — Maintenance

The authoritative requirements crosswalk MUST record the editions used and be
reviewed when relevant standards or laws materially change.

A source update MUST trigger an applicability and impact review, not automatic
scope expansion or automatic invalidation of previously accepted work.

## Executable assurance record

The normative requirements above are supported by the OBDD assurance-record
schema and validator in this repository. Validation establishes only that the
record is structurally complete and passes the published consistency checks. It
does not determine legal applicability, approve the activity, independently
assess evidence, or certify conformity.
