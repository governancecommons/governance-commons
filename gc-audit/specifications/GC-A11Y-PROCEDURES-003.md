# GC-A11Y-PROCEDURES-003 — Accessibility audit procedures and evidence contract

Status: SPECIFICATION DRAFT — repository committed; NOT IMPLEMENTED, NOT VERIFIED, NOT CERTIFIED  
Date: 2026-10-27  
Owner: Governance Commons  
Target: WCAG 2.2 Level A and AA for applicable web content  
Scope: 18 individual procedures, evidence, adjudication, coverage and handoff.

## Principles and boundaries

1. These are proposed test procedures, not proof that the tests have run or that any application conforms.
2. Automated results alone cannot pass a procedure requiring human/assistive-technology testing.
3. Normative WCAG findings are separate from advisory accessibility and human-factors findings.
4. Records are append-only; subsequent corrections reference original record ID and content hash.
5. Never record credentials, tokens, session cookies, recovery codes, or unnecessary personal information.
6. Evaluate complete processes and entire pages where relevant. Sampling by itself is not whole-product conformance.
7. Every WCAG 2.2 A/AA criterion must appear in a machine-checkable criterion ledger, including any criteria not explicitly listed below. Any criterion lacking coverage blocks a claim of complete coverage. WCAG 2.2 criterion 4.1.1 is obsolete and is not independently graded.
8. Procedures are reusable for Governance Commons and other web interfaces; applicability must be declared for each target.
9. Stable IDs GC-A11Y-01..18; changing meaning requires versioning, not silent replacement.

## Execution envelope

An evaluation declares: `evaluation_id`, product and build/commit SHA, target routes and states, included/excluded scope and reasons, WCAG version/level, OS/browser/AT versions, device and CSS viewport, evaluator identity, instrument versions, `time_loc`, test plan, criterion coverage, and limitations. Include critical tasks and complete processes; common templates, interactions, navigation and unusual states, mobile/reflow, and representative sample selection rationale.

For each procedure, record: `test_id`, `procedure_version`, `evaluation_id`, `target`, `criterion_refs`, `method`, `preconditions`, `steps`, `expected`, `observed`, `result`, `applicability`, `exceptions`, `evidence_refs`, `evaluator`, `time_loc`, `limitations`, `review`. Each evidence reference has an ID, type, capture method, file or URI, SHA-256 integrity digest, capture timestamp, privacy classification and redaction status. Distinguish observation from inference.

Procedure results: PASS (all applicable required subchecks pass with adequate evidence), FAIL (at least one demonstrated applicable violation), INCONCLUSIVE (insufficient/ambiguous/blocked evidence), NOT_APPLICABLE (all subchecks genuinely inapplicable with documented justification), NOT_TESTED (not executed). Preserve subcheck outcomes; one FAIL makes overall test FAIL; evidence absent for required manual testing cannot yield PASS. Evaluation summary: COMPLETE_WITH_FAILURES, COMPLETE_WITHOUT_DETECTED_FAILURES, or INCOMPLETE. None of these alone means WCAG conformance or legal compliance.

Evidence may include DOM/accessibility-tree snapshots, semantic inventories, quantitative measurements, screenshots, sanitized interaction/video captures, keyed transcripts, AT announcement notes, tool outputs and human attestations. Screenshots alone are not sufficient proof of keyboard operability, spoken announcement, or workflow completion.

## Individual procedures

Each procedure is run over all applicable sampled pages/components/states, with exceptions adjudicated against the exact normative WCAG criterion. The mapped criteria below are starting references rather than an exhaustive coverage ledger.

### GC-A11Y-01 — Semantic structure and landmarks

- **WCAG references:** 1.3.1, 1.3.2, 2.4.1, 2.4.6, 4.1.2.
- **Method:** Automated + manual.
- **Steps:** Inspect heading hierarchy, landmarks, lists, tables, structural relationships and reading order in DOM, accessibility tree and rendered presentation; navigate by headings/landmarks.
- **Pass:** Meaningful relationships programmatically determinable, reading order meaningful, and bypass mechanism operable; heading structure conveys hierarchy.
- **Required evidence:** E01: heading/landmark inventories, accessibility tree, reading-order walkthrough, selectors, reviewer judgment.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-02 — Accessible names, roles and states

- **WCAG references:** 1.3.1, 2.5.3, 4.1.2.
- **Method:** Automated + manual.
- **Steps:** Inventory controls; inspect computed role, accessible name, value/state/description; operate controls and compare changes.
- **Pass:** Accessible properties correctly express function/state; where required, accessible name contains visible label.
- **Required evidence:** E02: control inventory, DOM/accessibility properties, before/after state snapshots, screenshots and selectors.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-03 — Keyboard operability

- **WCAG references:** 2.1.1, 2.1.2, 2.1.4.
- **Method:** Manual + automated.
- **Steps:** From fresh load execute each essential action by keyboard; operate widgets/menus/forms, exit composites and test relevant character-key shortcuts.
- **Pass:** Functionality available without pointer or unqualified timing dependence; no keyboard trap; shortcuts conform.
- **Required evidence:** E03: keyed event/focus transcript, video or detailed observation, final task outcomes, reproduction steps.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-04 — Focus visibility and order

- **WCAG references:** 2.4.3, 2.4.7, 2.4.11, 3.2.1; 2.4.13 AAA advisory.
- **Method:** Manual + automated.
- **Steps:** Traverse forward/backward; evaluate indicator visibility, focus order, focus scroll, sticky overlays and coverage by authored content.
- **Pass:** Logical meaningful focus progression; indicator visible and focused element not entirely hidden by authored content.
- **Required evidence:** E04: ordered focus map, focused screenshots, viewport, occlusion observations and reviewer decision.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-05 — Screen-reader compatibility

- **WCAG references:** 1.1.1, 1.3.1, 1.3.2, 4.1.2, 4.1.3 and context-dependent criteria.
- **Method:** Manual assistive technology.
- **Steps:** Use named screen reader/browser/OS combination; traverse landmarks/headings/links/forms, operate a complete critical task and observe announcements.
- **Pass:** Meaningful operation and information under tested AT setup; no unsupported generalization to all AT.
- **Required evidence:** E05: exact AT/software versions, task plan, observed spoken/braille announcements and operation transcript, reviewer attestation.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-06 — Images and non-text alternatives

- **WCAG references:** 1.1.1, 1.4.5; 1.4.9 AAA advisory.
- **Method:** Automated + manual.
- **Steps:** Classify meaningful, functional, decorative, complex images and image-of-text cases; inspect alternatives in context.
- **Pass:** Appropriate equivalent alternative for meaningful images; purpose labels for functions; decorative assets avoid irrelevant announcements.
- **Required evidence:** E06: asset IDs, classification, alternatives, contextual screenshots, reviewer rationale.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-07 — Contrast and color independence

- **WCAG references:** 1.4.1, 1.4.3, 1.4.11; 1.4.6 AAA advisory.
- **Method:** Automated + manual.
- **Steps:** Measure foreground/background contrast in relevant text and component states, including icons and indicators; remove color cue for information.
- **Pass:** Normal text >=4.5:1; qualifying large text >=3:1; applicable non-text >=3:1, subject to normative exceptions; meaning not color-only.
- **Required evidence:** E07: CSS/computed colors, contrast calculations, state/element selectors, screenshots and exception rationale.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-08 — Zoom and text spacing

- **WCAG references:** 1.4.4, 1.4.12.
- **Method:** Browser + manual.
- **Steps:** Test 200% text resize/zoom where applicable, and WCAG text-spacing overrides; inspect clipping, overlap, truncation and task operation.
- **Pass:** No loss of content/function at required settings under applicable exceptions.
- **Required evidence:** E08: settings and text-spacing CSS overrides, before/after screenshots, affected elements and functional observations.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-09 — Reflow and orientation

- **WCAG references:** 1.3.4, 1.4.10.
- **Method:** Browser + manual.
- **Steps:** Evaluate 320 CSS px width equivalent, 256 CSS px height equivalent where appropriate, and supported orientation changes; inspect scrolling and content preservation.
- **Pass:** No prohibited two-direction scroll or unintended orientation lock; normative exceptions identified.
- **Required evidence:** E09: viewport dimensions, DPR, scroll geometry, orientations, screenshots, exception classification.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-10 — Forms, validation and recovery

- **WCAG references:** 1.3.5, 3.3.1–3.3.4, 3.3.7, 4.1.3.
- **Method:** Functional + manual.
- **Steps:** Submit missing, invalid and valid inputs; inspect labels, autocomplete/input purpose, accessible errors/suggestions and repeated data; correct and resubmit.
- **Pass:** Applicable error identification, instructions, protections and recovery; unnecessary repeated entry avoided.
- **Required evidence:** E10: sanitized inputs and outputs, field associations, error-state screenshots, announcements, recovery transcript.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-11 — Navigation and wayfinding

- **WCAG references:** 2.4.1, 2.4.2, 2.4.4–2.4.6, 3.2.3–3.2.4; 2.4.8 AAA advisory.
- **Method:** Functional + manual.
- **Steps:** Compare navigation, titles, labels and link purpose across routes; bypass repeated content; traverse representative task path.
- **Pass:** Normative navigation identifiers, purpose and consistency criteria satisfied; confusing wayfinding tracked separately as human-factors finding.
- **Required evidence:** E11: route map, title/heading/link inventories, comparison, task navigation transcript.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-12 — Dynamic content/status announcements

- **WCAG references:** 4.1.2, 4.1.3, 3.2.2.
- **Method:** Functional + assistive technology.
- **Steps:** Trigger loading, results, progress, selection, errors, and completion; track focus and accessible announcement timing.
- **Pass:** Qualifying status messages determinable without focus movement; controls report accurate states; context changes meet criteria.
- **Required evidence:** E12: triggers, before/after accessibility tree, AT announcement transcript, focus trace and event timeline.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-13 — Dialogs, overlays and disclosure

- **WCAG references:** 2.1.1, 2.1.2, 2.4.3, 2.4.11, 4.1.2.
- **Method:** Functional + manual.
- **Steps:** Open/operate/close modal dialogs, nonmodal overlays, menus, popovers and disclosures; inspect roles, labeling, focus and background behavior.
- **Pass:** Each pattern accessible; modal focus appropriately managed; escape/exit and focus restoration appropriate; no traps.
- **Required evidence:** E13: component classification, accessible names/roles/states, keyboard and focus sequence, observed background interaction.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-14 — Pointer, touch and alternative input

- **WCAG references:** 2.5.1–2.5.8 as applicable.
- **Method:** Manual + measurement.
- **Steps:** Inspect multi-point/path gestures, dragging alternatives, pointer cancellation, hover/focus supplementary content, speech-label alignment and target sizes/spacing.
- **Pass:** Applicable alternatives provided; activation behavior compliant; target >=24x24 CSS px or documented WCAG 2.2 exception.
- **Required evidence:** E14: measured target rectangles/gaps, gesture and pointer traces, alternative task recordings, exceptions.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-15 — Motion, flashing and time limits

- **WCAG references:** 2.2.1, 2.2.2, 2.3.1; 2.3.3 AAA advisory.
- **Method:** Manual + analyzer.
- **Steps:** Inventory timeouts, auto-updates, animation, flash and motion triggers; exercise pause/stop/hide and time adjustment; analyze flashes when relevant.
- **Pass:** Applicable timing/motion controls and flash threshold satisfied; reduced-motion preference reported separately unless tied to normative criterion.
- **Required evidence:** E15: time measurements, media/animation settings, recordings, controls demonstration, flash analysis and exemptions.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-16 — Media captions and alternatives

- **WCAG references:** 1.2.1–1.2.5 as applicable; 1.2.6–1.2.9 AAA advisory.
- **Method:** Manual + functional.
- **Steps:** Inventory prerecorded/live audio/video; review captions, transcripts, audio descriptions, timing and accessible media controls.
- **Pass:** Applicable media alternatives and synchronized captions/audio description requirements met for each classified media type.
- **Required evidence:** E16: asset/media type, caption/transcript/audio description refs, sample timestamps, playback review, exception decisions.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-17 — Authentication and complete processes

- **WCAG references:** 3.3.7, 3.3.8, plus all criteria applying to workflow steps.
- **Method:** End-to-end + assistive technology.
- **Steps:** Complete representative authentication, verification, recovery and essential multi-step tasks via keyboard/AT; inspect cognitive function challenges and repeated entry.
- **Pass:** Applicable accessible authentication requirements met; each step in complete required processes fulfills applicable criteria.
- **Required evidence:** E17: sanitized account-role/task trace, step outcomes, AT record, interruption/recovery evidence; NO secrets/tokens/passwords.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

### GC-A11Y-18 — Help, language, instructions and comprehension

- **WCAG references:** 3.1.1, 3.1.2, 3.2.6, 3.3.2; 3.1.3–3.1.6 AAA advisory.
- **Method:** Manual + functional.
- **Steps:** Inspect document/part language, instructions, consistently positioned repeated help, and essential task comprehension; separate test observations from hypotheses.
- **Pass:** Normative language, help and instruction criteria satisfied; usability insights are non-normative until independently validated.
- **Required evidence:** E18: language properties, help placement comparison, instructions inventory, task notes, screenshots and hypothesis labels.
- **Failure/inconclusive:** Record observed breach as FAIL with evidence; absent required evidence is INCONCLUSIVE, never PASS. NOT_APPLICABLE requires criterion-specific justification.

## WCAG coverage and human-factors boundary

Build an independent machine-readable ledger enumerating **all** WCAG 2.2 Level A/AA success criteria (not just the mapped references above). Each row records criterion ID/level, relevant procedure(s), page/complete-process scope, applicability and rationale, coverage FULL/PARTIAL/MISSING, outcome, evidence refs, exception, reviewer and procedure version. Gate any coverage/conformance assertion on a complete ledger with no unresolved applicable criteria. Specifically reconcile criteria not obviously exercised here (including audio control, link navigation mechanisms, input and focus triggered change, text presentation and orientation). Evaluate WCAG conformance at full-page and complete-process granularity; do not infer it from sampled successes.

Finding types: NORMATIVE_ACCESSIBILITY (proven applicable WCAG violation), ADVISORY_ACCESSIBILITY (accessibility issue beyond mandatory rule), HUMAN_FACTORS (observed usability concern/hypothesis). Remediation severity CRITICAL/HIGH/MODERATE/LOW is independent of normative pass/fail; explain affected task and interaction mode.

## Quality and acceptance gates

- Procedure definitions and criterion ledger parse and validate deterministically; results are reproducible for fixed inputs.
- Positive, negative, missing-evidence and N/A fixtures for each of the 18 procedures.
- A fixture with keyboard trap and a fixture with inaccessible control must fail.
- Manual/AT procedures reject automated-only PASS.
- Appending a correction references original ID and SHA-256, preserving original evidence; no record rewrite.
- Error cases fail closed without fabricated observations.
- Evidence redaction and secret-exclusion tested.
- No production execution, certification, PR merge, publication or adoption-ready claim without real evidence and owner authorization.
- Existing GC-AUDIT registry/runtime remain unchanged until separately reviewed implementation.

## Research provenance (non-normative)

Human-centered procedure design is informed by user-provided: Don Norman, *The Design of Everyday Things* (discoverability/feedback/error); Steve Krug, *Don't Make Me Think, Revisited* (wayfinding/usability); Rosenfeld/Morville/Arango, *Information Architecture for the Web and Beyond* (navigation/labels); Tidwell/Brewer/Valencia, *Designing Interfaces* (interaction patterns); Wathan/Schoger, *Refactoring UI* (hierarchy/type/contrast); Susan Weinschenk, *100 Things Every Designer Needs to Know About People* (cognition); Jennifer Niederst Robbins, *Learning Web Design* (HTML/responsive); Myers/Hudson/Pausch, *Past, Present, and Future of User Interface Software Tools* (predictability). These are not WCAG compliance authority.

Normative reference: W3C WCAG 2.2, https://www.w3.org/TR/WCAG22/ ; evaluation methodology: https://www.w3.org/TR/WCAG-EM/ . Check exact criterion wording and conformance requirements against the normative source during implementation.

## Next milestone

GC-A11Y-IMPLEMENT-004: inspect actual GC-AUDIT structure and contracts before editing; implement procedure definitions, criterion ledger, evidence validators and test fixtures on a feature branch, preserve backward compatibility and security, run CI, submit PR for owner review. **This committed file is the specification only.**
