# NIST agent identity × GC zero-trust seam — 2026-11-05

**Status:** Non-normative, document-level semantic test. This is not NIST
conformance, a runtime security test, or an amendment to GC's active AL:2
specification.

## Pinned inputs and method

- **External prompt:** NIST NCCoE, *Accelerating the Adoption of Software and
  AI Agent Identity and Authorization*, February 2026 **draft concept paper**,
  [official PDF](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf),
  SHA-256 `b303f7fba8c916f440a9435fa48d0e4465553f6b974d3157a1494747589e0b71`.
  The paper asks implementation questions; it does not specify conformance
  requirements. Its page 4 asks how an agent proves authority for a particular
  action and how “on behalf of” delegation binds to a human. Page 6 names
  access delegation, logging, and data-flow provenance as areas of interest.
- **GC artifact:** [`governance/zero-trust.yaml`](../../governance/zero-trust.yaml)
  at umbrella commit `91cb20d85c425144ccf6b393c75f978091d1d889`,
  SHA-256 `910378613d70d9438d243604a79c7e585f10bc9f636ca1ed5df6038a8bbbfe10`.
  This test reads that file alone. Linked Agent Dossier schemas, implementations,
  and deployed systems were not tested.

For each hypothetical case below, compare the NIST question to an explicit
rule in the pinned GC artifact. “Answered” means this artifact gives a rule
for the case. “Partial” means it covers only part of the question. “Unknown”
means this document-level test cannot decide an implementation outcome.

## Fixture cases and observations

| Case | Given / when | NIST prompt | Observed in pinned GC artifact | Result |
| --- | --- | --- | --- | --- |
| ZT-1: agent handoff | An active agent sends a signed handoff to a peer in strict profile. | How is the agent identified and authenticated? (pp. 4, 6) | `establishment` requires a current dossier from a trusted source, status/expiry check, Ed25519 signature verification, and key-hint binding to `from_agent`; `principles` calls for per-handoff verification. | **Answered at specification level.** No verifier execution or interoperability was demonstrated. |
| ZT-2: action on behalf of a person | The same authenticated agent requests a specific tool action for a named human. | How does it prove authority for that action, bind the human, and carry delegated scope? (p. 4) | `least-privilege` limits agents to dossier `authority_scope` and `tool_permissions`. The `establishment` phases verify the agent and envelope, but define no human-principal binding or action-specific delegation proof. The `revoked_by` field can name a human when revoking a dossier; it is not a per-action grant. | **Partial.** Agent-level scope is stated; a human-to-agent, action-specific proof is not answered by this artifact. Whether another GC component supplies one is unknown here. |
| ZT-3: withdrawn authority | A governance actor withdraws the agent's standing authority before another handoff. | How can authorization change after initial trust? (p. 4) | `revocation` defines `authority_withdrawn`, status checks on each envelope, and cache invalidation; `residual_risks.no-realtime-revocation-signal` admits a possible 300-second standard-profile window. | **Partial.** Dossier-level withdrawal has rules, but the specification records a propagation gap; runtime timing was not measured. |

## Result and next bounded decision

The concrete overlap is real: both sources address agent identity,
authorization, delegation, and revocation. The **specific seam** is the
distinction between verifying an agent's standing dossier authority and proving
that a human authorized a particular action. This test finds an answer for the
first and only a partial answer for the second in `governance/zero-trust.yaml`.
It does not establish a GC-wide absence, a NIST defect, or a requirement to
add a new GC protocol.

Before any normative design change, inspect the linked Agent Dossier handoff
contract and one actual verifier path against ZT-2. Record the authority source,
action/resource binding, human-principal evidence, and denial behavior. If
those are absent, propose a separately reviewed, narrow contract change under
the existing GC decision process. Recheck the NIST source before relying on
it for a later design decision; its project is evolving.

## Follow-up: handoff contract and runtime trace (2026-11-05)

This follow-up closes the inspection requested above. It reads the clean
`agent-dossier` repository at `c87c8b72cadd244ce0b66e8b8de89c8887eb0d68`
and the clean `agent-project-orchestrator` repository at
`e14340200f22d0e7de72c5e1e6d965cf0de7eaf8`. Neither repository was edited.

| Check | Evidence | Observed result |
| --- | --- | --- |
| Handoff contract | [Agent Dossier handoff specification](https://github.com/governancecommons/agent-dossier/blob/c87c8b72cadd244ce0b66e8b8de89c8887eb0d68/agent-dossier.yaml) `handoff_protocol`; [JSON Schema](https://github.com/governancecommons/agent-dossier/blob/c87c8b72cadd244ce0b66e8b8de89c8887eb0d68/schemas/handoff-envelope.schema.json) | The specification makes envelope signatures optional outside strict profile and requires verification when present. The schema requires agent IDs and task-continuity fields, but has `additionalProperties: false` and no dedicated human principal, action/resource grant, or delegation-proof property. |
| Schema fixture | Validate the existing `examples/valid/handoff-envelope.yaml` with the pinned JSON Schema and a YAML loader that preserves timestamps as strings; then add either `human_principal: human-a` or `authorization_proof: unverified-string`. | Baseline **valid**; each added property **invalid** as an unexpected additional property. This is a shape check, not cryptographic signature verification. |
| Runtime path | [Task model](https://github.com/governancecommons/agent-project-orchestrator/blob/e14340200f22d0e7de72c5e1e6d965cf0de7eaf8/models/task.py) → [Dispatcher.dispatch](https://github.com/governancecommons/agent-project-orchestrator/blob/e14340200f22d0e7de72c5e1e6d965cf0de7eaf8/orchestrator/dispatcher.py) → [BaseAgent.check_permission](https://github.com/governancecommons/agent-project-orchestrator/blob/e14340200f22d0e7de72c5e1e6d965cf0de7eaf8/agents/base.py); [handoff builder](https://github.com/governancecommons/agent-project-orchestrator/blob/e14340200f22d0e7de72c5e1e6d965cf0de7eaf8/orchestrator/escalation.py) and [model](https://github.com/governancecommons/agent-project-orchestrator/blob/e14340200f22d0e7de72c5e1e6d965cf0de7eaf8/models/handoff.py) | `Task` allows extra properties. Dispatch selects an agent and calls `execute`; the base tool check takes a tool name, not a human principal or proof. The handoff builder emits an unsigned envelope. No incoming envelope signature or human-delegation verifier was found in this inspected path. |
| Temporary dispatch probe | Two in-memory tasks with the same assigned probe agent and `human_principal=human-a`: one with no proof, one with `authorization_proof=unverified-string`; a temporary audit log was used. | Both returned `DONE` and reached the probe agent. The probe did no real tool action and had no governance record attached. This establishes only that this dispatch path does not require or verify the supplied human authorization evidence. |

**Refined finding:** The Agent Dossier contract describes agent signature
verification, but its published envelope shape cannot carry those two proposed
human-delegation fields directly. The selected orchestrator path does not
implement the NIST question's action-specific human authorization check.
This is a bounded contract/runtime seam, not evidence that every GC consumer
lacks such a check or that a deployed system accepted an unauthorized action.

**Next decision:** Identify the intended authority source and denial boundary
for human-to-agent actions, then submit a narrowly scoped contract and verifier
proposal for owner review. Preserve the current agent-to-agent handoff semantics
until that proposal specifies compatibility and enforcement behavior.
