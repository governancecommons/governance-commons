# GC-HCI-RESEARCH-001 — Research-to-Audit Traceability Matrix v0.1

Status: **DRAFT CANDIDATES ONLY**. No criterion is approved, implemented, validated for reviewer agreement, or an evidence-based claim about any application.

## Candidate matrix
| ID | Evaluation question | Sources | Proposed observable procedure | Evidence to capture | Limitations |
|---|---|---|---|---|---|
| HCI-DISC-001 | Can intended users discover a task-relevant action? | S01 Ch 4; S04 Ch 8; S02 Ch 1 | Neutral task, record first and subsequent actions; separate expert inspection of signifiers | Audience, task, start state, action trace, assistance, outcome | One task/participant does not establish general discoverability |
| HCI-MENT-001 | Do users' predicted consequences match behavior? | S01 Chs 1–2; S05 mental-model topics | Ask for prediction before controlled action, compare with observed result | Prior expectation, actual output, task and conditions | Mismatch has multiple possible causes |
| HCI-FEED-001 | Is status/outcome communicated during execution? | S01 Chs 1,4; S04 Ch 8 | Exercise pending/success/failure/interruption states | State sequence, messages, perception/interpretation | Visual presence alone does not establish comprehension |
| HCI-CLAR-001 | Are consequences of impactful actions clear? | S01 Chs 2,4; S04 Ch 8 | Ask what will happen before action; check preview/confirmation and actual result | Prediction, UI, irreversible effects | Not all actions warrant confirmation |
| HCI-IA-001 | Can users locate content within the information organization? | S03 Chs 3–6; S04 Ch 2 | Representative retrieval tasks from defined entry points | Information inventory, navigation path, outcome | Audience and domain sensitive |
| HCI-LABEL-001 | Do labels convey expected contents/actions? | S03 Ch 7; S02 Chs 3–4 | Ask participant expectation for label in context, inspect target | Wording, predictions, actual destination | Interpretation varies by population |
| HCI-NAV-001 | Can users navigate, orient and backtrack? | S03 Ch 8; S02 Chs 6–7; S04 Ch 3 | Follow multi-step task from declared entry point | Wayfinding trace, state, return attempts | Task setup changes outcomes |
| HCI-FIND-001 | Does search/retrieval support declared information needs? | S03 Chs 3,9 | Record query, search results, refinements, success/abandonment | Query, index scope, retrieval result | Only applicable where search exists |
| HCI-ERR-001 | Can users prevent, understand and recover from relevant errors? | S01 Ch 5; S04 Chs 8,10 | Controlled invalid input and failure scenarios | Error state, message, recovery trace, saved work | Unrecoverable effects may exist |
| HCI-CTRL-001 | Is meaningful control or reversibility available when appropriate? | S01 Chs 2,5; S04 Ch 8 | Try cancel, undo, revise, halt; compare represented vs actual control | Commands, system transitions, outcomes | Undo is not universally possible |
| HCI-COG-001 | Are recognition and recall demands appropriate for users/tasks? | S01 Ch 3; S05 recognition/memory topics; S04 Ch 3 | Observe reliance on hidden commands, earlier instructions or remembered context | Task steps, prior experience, cues | No fixed magic-number memory threshold |
| HCI-CONS-001 | Are equivalent interactions predictable and consistent? | S04 Chs 2,8; S01 Ch 4; S08 §2.1 | Compare equivalent operations; test predicted behavior | Control/command semantics, comparison outcomes | Context can justify variation |
| HCI-VIS-001 | Does presentation help people identify task-relevant priorities? | S06 hierarchy/spacing; S04 Chs 4–5 | Ask users to locate priority task targets; label expert-only judgments | Layout state, task result, interpretation | Aesthetics cannot be scored as usability |
| HCI-TOOL-001 | Can novice and experienced users access relevant capabilities? | S08 §2.1; S04 Chs 1,8 | Distinct novice and experienced tasks; record discovery and capability ceiling | Expertise, help paths, task attempts | Historical tooling concepts need contemporary validation |
| HCI-AUTO-001 | Is assisted/automated action behavior predictable and controllable? | S08 §2.1; S01 Chs 2,5; S04 Ch 8 | Ambiguous instruction, preview, authorization, execution, cancellation scenarios | Input, interpretation, permission, actual side effects | No direct modern AI-interface validation from this corpus |

## Fully worked candidate: HCI-DISC-001
- Namespace: `gc-audit.hci` (proposed, not registered).
- Type: evidence-informed heuristic OR observed empirical task evaluation, explicitly tagged; not a normative WCAG requirement.
- Context: declared user group, task, permitted assistance, software version, initial state.
- Procedure: (1) define realistic task; (2) capture initial state; (3) present neutral task without naming control; (4) record selection sequence and requests for assistance; (5) elicit participant expectation; (6) record outcome and separate observation from interpretation; (7) describe limits.
- Evidence: task and user definition, evaluator/method, version, state, interaction trace, errors, participant feedback, artifacts, provenance.
- Allowed finding: bounded participant observation or expert-identified potential problem.
- Forbidden finding: universal intuitiveness, representative prevalence, or verified psychological cause based on sparse evidence.
- Applicability: each platform requires its own adapted task and interaction procedure.

## Validation contract proposal (not yet executed)
A. Content validity: check original source passage and what it actually claims.
B. Repeatability: independent reviewers use same protocol and compare decisions.
C. Discrimination: include clear, adverse and ambiguous fixtures; allow NOT_TESTED/INCONCLUSIVE.
D. Context: vary declared population and task before generalization.
E. Utility: criterion yields reproducible, actionable findings and is not redundant.
Do not invent agreement statistics, thresholds or observed participants.

## Initial pilot proposals (NOT run)
- GC Portal: article discovery → evidence inspection → editorial approval/rejection → publication confirmation/error recovery.
- GC public site: entry → news/report navigation → source/provenance inspection → return/search.
- Cockpit CLI (later specialist pilot): command discovery → ambiguity → preview/authorization → execution feedback.

## Implementation gates
Draft the evaluation contract, evidence schema mapping, reviewer/AI authority and criteria versioning; inspect existing `gc-audit` machine contracts; validate procedures; receive owner approval; only then register and implement any commands. No change to ZTA/AMD scopes.
