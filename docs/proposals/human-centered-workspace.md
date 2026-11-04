# Human-centered workspace and interaction — standards proposal

**Status:** draft proposal; not an accepted GC standard or conformance profile.
**Date:** 2026-11-04
**Identifier:** unassigned. `HCI-001` and `GC-UIS-001` were conversation candidates, not registered identifiers.

## Authority and scope

This proposal concerns portable, observable quality for human-facing AI workspaces. It does not require a common component library, icon package, visual identity, layout dimensions, or product type. Governance Commons would own the requirements and evidence contract only after the RFC and maintainer review required by `rfcs/RFC-PROCESS.md`. DCP can record project applicability and evidence; development workflows can check it; each product implements its own interface.

The proposed standard is one cohesive HCI contract with interaction, accessibility, visual, and evaluation domains. Accessibility is a required, independently verifiable profile wherever applicable, never an optional usability proxy. Existing `GC-A11Y-01` through `GC-A11Y-18` procedures and `A11Y-01` through `A11Y-10` assessment domains retain their meanings. This proposal neither renumbers them nor creates a second WCAG audit engine. ONS continues to own naming conventions, not interface behavior.

## Experience outcomes to evaluate

Familiarity, predictability, user control, continuity, and recoverability are the five proposed experience outcomes. Evaluate them against declared users, tasks, devices, and usage contexts; do not assume every person expects every feature. A project explains inapplicable patterns rather than silently omitting them.

1. **Workspace and information architecture.** Provide understandable global navigation, an explorer or organizer, a dominant primary work area, an optional contextual panel, and restrained status feedback. Responsive layouts may collapse or reflow these regions. Support software, research, creative, business, and physical projects without assuming a repository or IDE. A project may offer list, grid, board, calendar, timeline, document, or other task-appropriate views over the same underlying information.
2. **Familiar navigation and editing.** Specify the expected behavior of tabs, breadcrumbs, back/forward history, recent items, scoped and global search, selection, context menus, drag/drop, direct editing, split views, resizable panels, undo/redo, autosave, and remembered settings where relevant. Navigation locations and behavior should remain stable across workspaces. Actions need visible feedback, including pending, success, failure, disabled, and recovery states.
3. **Conversation beside work.** Provide an approachable natural-language entry point with attachments and follow-up where AI interaction is offered. Keep the artifact visible or easy to inspect beside the conversation. Direct editing remains available. AI plans, progress, access scope, affected objects, proposed changes, approval needs, stop/interrupt, and supported reversal should be understandable before consequential action.
4. **Progressive complexity and continuity.** Offer useful defaults with advanced tools available on demand, without permanent user tiers. Restore project, tabs, layout, unfinished work, and recent activity as the product contract allows. Explain where content is stored, what the AI can access, and whether work was saved or failed. Use quiet, actionable notifications. Desktop and mobile can expose different task-appropriate views while preserving coherent navigation and review.
5. **Visual language and semantics.** Establish readable hierarchy, consistent typography, spacing, control states, responsive behavior, and considered light/dark themes. Permit adjustable density, font scale, and layout where supported. Use conventional icon metaphors consistently; pair icons with visible labels when recognition, risk, or context requires it. Do not make touch use depend on hover or communicate critical state by color alone.

## Icon and action mapping

Before implementation, each product records its action → icon → visible label → tooltip/help text → accessible name → expected behavior mapping, including keyboard and touch behavior, disabled and destructive states, and exceptions. Test specialized or ambiguous icons with representative users. A search magnifier, settings gear, folder, trash, plus, close, back, and similar conventional metaphors are examples, not a mandated asset set. A product may select Lucide or another coherent family and document platform-native exceptions; GC would not mandate a library.

The original design discussion named Home, Search, Menu, Settings, Folder, File, Add, Edit, Save, Delete, Download, Upload, Back, Forward, Refresh, Close, Sidebar, Split view, More, Filter, Help, Alerts, Account, Attach, Undo, Redo, Copy, Confirm, Run, Stop, Preview, and Open link as candidate actions. Their glyphs and labels require context-specific review; legacy metaphors such as a floppy disk for Save should be tested rather than assumed universally recognized.

## Design and acceptance before implementation

For each target screen or workflow, record target users, tasks and mental models; information architecture; wireframes and reference screens; viewport and responsive expectations; interaction and icon mappings; accessibility target and methods; and visual, behavioral, and usability acceptance criteria. The owner approves references and criteria before UI implementation. Product-specific thresholds require a reasoned task and participant plan; a suggested 90% onboarding task-success target is not a universal rule.

Verification compares actual rendered screenshots or recordings with approved references at declared viewports and zoom, including empty, populated, loading, pending, error, success, and recovery states. Record source commit, browser/device, evaluator, date, deviations, and disposition. Automated checks can test semantics and regressions; screenshots alone cannot prove behavior or accessibility. Observe representative participants doing real tasks, including comprehension, task completion, errors, recovery, and icon recognition. Keep expert review, automated results, participant observations, and owner approval distinct. CI success alone does not establish visual or usability acceptance.

## Existing contract crosswalk and decision gates

| Concern | Existing authority or artifact | Proposed relationship |
| --- | --- | --- |
| WCAG 2.2 A/AA web assessment | `gc-audit/specifications/GC-AUDIT-A11Y-001.md` and `GC-A11Y-PROCEDURES-003.md` | Reuse ten domains and eighteen procedures; independently report applicable accessibility outcomes and incomplete manual checks. |
| HCI evidence structure | `schemas/gc-hci-*.v0.1.schema.json` and `gc-audit/hci/README.md` | Reuse profile, criterion, evidence, finding and report shapes; these schemas alone do not establish an executable audit or aggregate acceptance. |
| HCI research | Open research baseline PR #5 | Reconcile source and criterion traceability before normative publication; do not treat draft research as verified user evidence. |
| Naming | ONS | Keep ONS identifiers and naming separate from visual and interaction semantics. |
| Product acceptance | Product-specific reference and test plan | Declare applicability, approved references, functional/visual/usability outcomes and evidence links per product. |

Before any normative status or identifier is assigned, resolve GC charter fit, overlaps, WCAG applicability, evaluator method, accessibility profile boundary, schema/version compatibility, and affected adopters through the RFC process. No HCI audit operation, release gate, conformance claim, or requirement on existing projects is activated by this proposal.

## Architecture review — proposed disposition, 2026-11-04

`GC-CHARTER-004` names Agent Dossier, Agent Matrix, and ONS as the active specification family. `DEV-PATH.md` freezes the OSS core baseline and routes new category-defining capability to optional PASS-6 profiles. `DEV-PLAN.md` also calls for a strategic checkpoint before opening a broad GC capability track and places adoption-interface tooling outside GC. The existing HCI schemas and research are GC-AUDIT candidates, not an accepted HCI standard. Consequently, this document cannot itself establish general UI-design authority for GC.

**Recommended boundary for review:** preserve the complete workspace direction here as a non-normative reference and in product acceptance plans. If GC is to own a binding specification, scope it to independently adoptable **human–AI interaction assurance**: predictable action and icon semantics, accessible controls, observable feedback, AI access and change transparency, meaningful human control, recovery, applicable accessibility evidence, and valid human evaluation. Familiar tabs, panel layout, icon-family choice, exact visual language, and feature priority remain product-specific examples unless a portable, evidence-backed rule is separately justified. This recommendation keeps the HCI interaction, accessibility, visual, and evaluation domains together for assessment without mandating one interface design.

**Required decision path:** the founder approved drafting the bounded GC proposal on 2026-11-04. [Issue #22](https://github.com/governancecommons/governance-commons/issues/22) records the number request, and [RFC-0002](../../rfcs/RFC-0002-human-ai-interaction-assurance.md) is the public-comment draft. `HCI-001` and `GC-UIS-001` remain unallocated specification names. RFC acceptance, the AL:3 `GC-CHARTER-004` amendment, frozen-baseline exception, implementation, and release remain separate decisions. No activation follows from authorization to draft.

**Alternative if GC scope is declined:** keep the general-purpose HCI standard in an independently governed package and let GC-AUDIT reference its published version for evaluation. DCP and Cockpit GUI can still use the product acceptance requirements already recorded in their review proposals. This alternative avoids changing the GC charter but requires separate standards ownership and versioning.
