# A11Y manual review template

Use a new dated record for each evaluation. Record reviewer, role, browser/OS/assistive technology versions, page and state, viewport, exact actions, observed behavior, criterion ID and applicability rationale, evidence file/hash, result and limitations. Use `not-applicable` only with a criterion-specific explanation. Do not mark a criterion `verified-pass` from an axe pass or from this checklist alone. Preserve previous evidence and link reverification to its earlier report digest.

| Domain | Human procedure and evidence to record |
| --- | --- |
| A11Y-01 Structure | Navigate headings and landmarks; inspect reading order, lists and relationships. Record DOM/accessibility-tree inventory and the traversal sequence. |
| A11Y-02 Keyboard and focus | From a fresh load, use Tab, Shift+Tab, Enter, Space and Escape for every essential action. Record focus order, visible indicator, occlusion, traps and task outcome. |
| A11Y-03 Names, roles, states | Compare visible labels with computed names; operate controls and record before/after roles, values and states. |
| A11Y-04 Forms and errors | Identify forms; use safe local/staging fixtures for submission cases. On the public website, do not submit. Record labels, instructions, errors, recovery and applicable exceptions. |
| A11Y-05 Visual presentation | Measure text/non-text contrast in relevant states, check color independence and WCAG text spacing. Record colors, ratio, font size and exception rationale. |
| A11Y-06 Responsive and reflow | Test equivalent 320 CSS-pixel width, 200% text resize and relevant orientation/zoom, inspect clipping and task function. Record viewport/DPR/zoom and screenshots. |
| A11Y-07 Non-text alternatives | Classify informative, functional and decorative images and any media. Review alternatives in context and record asset, role and rationale. |
| A11Y-08 Dynamic announcements | Trigger actual status changes where safe; inspect focus, live region and announcement timing. Record interaction and assistive technology transcript. |
| A11Y-09 Navigation | Compare titles, link purposes, bypass links and repeated navigation across sampled routes. Record task path and deviations. |
| A11Y-10 Screen reader | Use a named screen reader/browser/OS combination on representative complete tasks. Record spoken output, navigation mode, control operation, reviewer and limitations. If unavailable, retain `needs-manual-review`. |

For each confirmed failure record a stable finding ID, exact WCAG criterion/level, URL/state, user impact, severity rationale, reproducible steps, remediation, verification procedure, evidence digest and provenance. Keep advisory usability observations separate from normative WCAG failures.
