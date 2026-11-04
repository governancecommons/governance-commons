# RFC-0002 — Human–AI Interaction Assurance Boundary

| Field | Value |
| --- | --- |
| RFC number | `RFC-0002` — allocated from founder authorization on 2026-11-04; [number request](https://github.com/governancecommons/governance-commons/issues/22) |
| Title | Human–AI Interaction Assurance Boundary |
| Status | `open-for-comment` — proposal only; no acceptance or activation |
| Author | jj-ervin (founder direction; draft prepared by Codex) |
| Created | 2026-11-04 |
| Target spec | New, independently versioned Human–AI Interaction Assurance specification, if accepted |
| Charter entry affected | `GC-CHARTER-004` (AL:3); separate founder approval required for amendment |
| Breaking | No for current specifications; opt-in addition only |
| Review mode | Public comment, selected from founder authorization; comments through 2026-11-18 23:59 America/Los_Angeles |

The comment window and this RFC do not schedule a GC release. RFC acceptance, specification implementation, charter amendment, and public activation are separate decisions.

## Problem statement

Human-facing AI systems can expose actions whose effects, access scope, progress, approval needs, and recovery paths are difficult for people to understand. Familiar controls and accessible names also vary across applications. A product can pass automated checks while leaving users unable to predict, inspect, interrupt, or recover from assisted work. The full workspace design direction and acceptance expectations are preserved in `docs/proposals/human-centered-workspace.md`, but that proposal is not a portable normative standard.

GC already has draft HCI research, five HCI evidence schemas, and separate accessibility audit procedures. These do not establish a binding HCI specification or an executable `gc-audit.hci` operation. The active specification family in `GC-CHARTER-004` lists Agent Dossier, Agent Matrix, and ONS. The OSS core baseline is frozen. A new GC specification therefore requires an explicit authority and scope decision before implementation or conformance claims.

## Proposal

### Scope and adoption unit

Create one optional, independently versioned specification for **human–AI interaction assurance**. It governs observable interaction semantics, accessibility evidence, AI transparency, human control, recovery, and evaluation for user-facing systems that offer AI-assisted actions. It does not prescribe a UI framework, component library, icon package, brand, layout dimensions, or the five-region workspace shell. Products may use the workspace proposal and Cockpit GUI acceptance contract as non-normative reference examples.

An adopter MUST declare its target people, critical tasks, user-facing surfaces, supported modalities and devices, consequential AI actions, applicable requirements, exceptions, and the exact specification version. A system without user-facing AI-assisted actions is outside this specification's scope; it may still use the non-normative design guidance.

For this proposal, a **consequential action** can materially change persisted work, affect an external system or another person, disclose data, alter access, incur meaningful cost, or create an effect the user cannot readily reverse. The eventual specification must operationalize this boundary with examples and adverse fixtures before claiming repeatable conformance.

### Draft normative requirements

These proposed rules are for the future specification. They are **not active** while this RFC is under review. Stable rule identifiers and conformance profiles will be assigned only through that specification's approved versioning process.

1. **Predictable action semantics.** An adopter MUST document the action, visible label or equivalent cue, accessible name, expected effect, and supported input methods for each consequential control. Equivalent actions MUST use consistent meaning within the declared product scope. Icons and color MUST NOT be the sole carrier of a consequential action or status. A specific icon family or visual metaphor is not required.
2. **Accessible operation.** An adopter MUST declare the accessibility standard and evaluation method applicable to each modality. A web adopter claiming this specification MUST evaluate applicable WCAG 2.2 Level A and AA criteria, including complete processes and required human or assistive-technology checks, using the existing GC A11Y domain and procedure mapping rather than a duplicate set of controls. A failed, missing, inconclusive, or untested required check MUST NOT support a conformance claim. Native and non-web surfaces MUST declare their applicable platform criteria and evidence instead of claiming WCAG web conformance by analogy.
3. **AI action transparency.** Before a consequential AI-assisted action, the interface MUST communicate the intended action, affected objects or data scope, material effects, and whether human approval is required. During execution it MUST provide understandable progress, interruption, failure, and approval-needed states. Afterward it MUST identify completed changes and the available review or recovery path. Disclosure detail MAY scale with risk and user task; it MUST remain accessible at the point of decision.
4. **Meaningful human control.** An adopter MUST identify which actions can be approved, rejected, stopped, revised, or reversed, and MUST explain irreversible or non-interruptible effects before the user commits to them. The interface MUST NOT imply that an action can be undone or stopped when the implementation cannot provide that control. This rule does not weaken existing authorization constraints in Agent Matrix or other applicable GC contracts.
5. **Continuity and recovery.** The interface MUST communicate saved, pending, failed, and recovered work states for declared critical tasks. It MUST provide a documented recovery path for foreseeable errors and interrupted assisted work, or explain a material limitation. Session restoration, autosave, and undo are implementation choices unless promised by the product's declared acceptance contract.
6. **Evidence-based evaluation.** Before implementing a covered workflow, the adopter MUST record target users and tasks, expected behavior, accessibility scope, visual and state references where relevant, acceptance criteria, and evidence owners. Evaluation MUST distinguish automated checks, expert judgment, actual rendered inspection, representative participant observation, and owner approval. A conformance claim MUST include versioned evidence of applicable accessibility checks and observed critical-task outcomes; CI success, a concept image, or synthetic fixtures alone MUST NOT establish usability, visual acceptance, or accessibility conformance. No universal task-success percentage is imposed by this RFC.

Accessibility is an independently reported, required part of the proposed specification where applicable. An adopter cannot satisfy it by passing general HCI or usability checks. Outcomes remain separate when evidence is incomplete or a criterion is not applicable with rationale.

### Proposed charter and activation boundary

No charter file is changed by this RFC draft. If the founder later approves activation, the proposed `GC-CHARTER-004` family sentence would become:

> The active Governance Commons specification family consists of Agent Dossier, Agent Matrix, ONS, and Human–AI Interaction Assurance. Each specification is independently versioned and independently releasable; no specification requires another to release in lock-step.

Activation would also require a named, versioned specification artifact, its own conformance and evidence contract, compatibility review, and founder-approved charter amendment. It would remain outside the frozen GC v1.2.0 core baseline. RFC acceptance would authorize specification work only; it would not perform that amendment, add a release-manifest entry, register an audit operation, certify adopters, or activate the specification.

## Alternatives considered

| Alternative | Disposition |
| --- | --- |
| Put all general UI and workspace design in GC | Declined as the proposed normative scope: it exceeds GC's current active family and would prescribe product choices without demonstrated portable evidence. Retain the full direction as non-normative guidance. |
| Maintain a separately governed general HCI standard | Viable if the founder declines GC scope. GC-AUDIT could reference its published version; ownership, versioning, and maintenance would need a separate decision. |
| Use only Cockpit GUI's design system | Insufficient for portable assurance across independent applications; keep Cockpit GUI as an implementation and product evidence source. |
| Treat accessibility alone as the HCI standard | Insufficient for AI transparency, user control, action semantics, recovery, and observed task outcomes. Accessibility remains independently verifiable. |
| Extend ONS | Declined: ONS governs naming, not human-facing action semantics or usability evidence. |

## Prior art

- `GC-CHARTER-004` and `GC-CHARTER-005` require independently versioned standards and reference rather than inheritance. RFC-0001 distinguishes specifications from tooling, publication infrastructure, and maintainer workspace.
- Open GC research PR #5 contains fifteen draft HCI evaluation questions and explicitly separates expert inference from observed participant behavior. `gc-audit/hci/README.md` documents candidate evidence schemas and no active HCI audit command.
- `gc-audit/specifications/GC-AUDIT-A11Y-001.md` and `GC-A11Y-PROCEDURES-003.md` supply the existing ten assessment domains and eighteen draft procedures. Their identifiers are retained; this RFC does not duplicate or renumber them.
- [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplies testable web accessibility criteria. [W3C WCAG-EM 2.0](https://www.w3.org/TR/WCAG-EM/) supplies informative evaluation methodology; it does not add or replace WCAG requirements. Neither establishes general HCI usability from an accessibility result.
- The Cockpit GUI visual acceptance contract and DCP adoption proposal show how a product can declare references, interaction states, and evidence without making their exact UI composition a GC rule.

## Compatibility impact

- **Current GC specifications:** no existing Agent Dossier, Agent Matrix, or ONS rule, schema, identifier, version, or release pin changes in this RFC draft.
- **GC-AUDIT:** candidate HCI schemas and A11Y procedures remain at their existing status. The known invalid HCI finding schema and incomplete accessibility manual evidence must be resolved in their own authorized work before any related conformance claim. No audit operation is registered here.
- **Adopters:** no current project is automatically enrolled. DCP and Cockpit GUI proposals may choose to align after an accepted specification exists; project-specific acceptance plans remain independently reviewable now.
- **Breaking consumers:** none identified for the proposed opt-in addition. If implementation later changes an existing GC contract, DDR-1 requires a named compatibility hold and consumer confirmation before activation.
- **Release and charter:** GC v1.2.0 remains unchanged. The AL:3 charter amendment and any future manifest entry require separate founder decisions.

## Implementation notes

1. Reconcile research passages and criterion definitions, including evaluator agreement and adverse fixtures, before turning draft HCI questions into normative rules.
2. Define the independently versioned spec identity and applicability/conformance profiles. Reuse or reference existing GC A11Y procedures and HCI evidence shapes; fix schema defects under a separate authorized change.
3. Pilot against real, declared tasks and participants. Preserve evaluator method, source commit, device, assistive technology, actual rendered states, privacy treatment, and evidence limitations. Synthetic fixtures remain test data.
4. Keep `gc-audit.hci` inactive until a read-only, allowlisted implementation and registry change have independent approval and validation.
5. Ask the founder to review the exact charter amendment, compatibility evidence, and release posture only after the specification is independently reviewable. No merge or release follows automatically from the public-comment window.
