# GC-AUDIT-A11Y-001 — Authoritative Milestone Specification

**Milestone:** GC-AUDIT-A11Y-001  
**Version:** 0.1.0  
**Repository:** `governancecommons/governance-commons`  
**Initial target:** `https://governancecommons.org`  
**Normative standard:** WCAG 2.2 Levels A and AA  
**Methodology:** W3C WCAG-EM  
**Status:** Owner-approved implementation scope, defined in ChatGPT

## 1. Objective

Implement a portable, read-only accessibility assessment capability within the existing GC-AUDIT architecture.

The capability must identify accessibility barriers, retain supporting evidence, explain their impact on users, provide actionable remediation guidance, and support reverification.

Do not create a competing audit engine, accessibility certification service, or compliance scoring system.

## 2. A11Y-01 through A11Y-10 — Assessment Domains

These identifiers represent ten assessment domains, **not individual WCAG success criteria**.

| ID | Assessment domain | Representative WCAG 2.2 criteria | Method |
| --- | --- | --- | --- |
| A11Y-01 | Semantic HTML and document structure | 1.3.1, 1.3.2, 2.4.6, 4.1.2 | Automated and manual |
| A11Y-02 | Keyboard access and focus management | 2.1.1, 2.1.2, 2.4.3, 2.4.7, 2.4.11 | Manual and automation |
| A11Y-03 | Accessible names, roles and states | 2.4.4, 2.5.3, 4.1.2 | Automated and manual |
| A11Y-04 | Forms, labels, validation and errors | 3.3.1–3.3.4, 3.3.7, 3.3.8 | Manual and automation |
| A11Y-05 | Color contrast and visual presentation | 1.4.1, 1.4.3, 1.4.11, 1.4.12 | Automated and visual |
| A11Y-06 | Responsive layouts, zoom and reflow | 1.3.4, 1.4.4, 1.4.10, 2.5.8 | Browser and manual |
| A11Y-07 | Images and non-text alternatives | 1.1.1, applicable 1.2.x criteria | Automated and editorial |
| A11Y-08 | Dynamic content and announcements | 2.2.2, 2.3.1, 4.1.3 | Interaction and assistive technology |
| A11Y-09 | Navigation and comprehensibility | 2.4.1, 2.4.2, 2.4.5, 3.2.3, 3.2.4 | Manual |
| A11Y-10 | Screen-reader compatibility | Cross-cutting applicable criteria | Assistive technology and manual |

The complete WCAG 2.2 A/AA criterion set must remain available for mapping and applicability decisions. The representative criteria listed above are not exhaustive.

WCAG 2.2 criterion 4.1.1 Parsing is obsolete and must not be treated as an active failure criterion.

### Relationship to GC-A11Y-01 through GC-A11Y-18

An existing draft reportedly defines `GC-A11Y-01` through `GC-A11Y-18`.

**Preserve that existing draft and its identifiers.**

The ten domains above organize assessment capabilities. The eighteen existing identifiers may define more granular controls.

Do not delete, overwrite, renumber, or automatically replace the eighteen controls. Inspect the actual draft and create a mapping between those controls and the ten assessment domains.

Where requirements overlap, reuse the existing control. Where they differ, document the difference. Do not implement duplicate controls simply because identifiers differ.

## 3. Assessment Evidence Contract

Every finding must identify:

- Stable finding identifier
- Assessment target and URL
- Relevant component, element or application state
- WCAG success criterion and level
- Evaluation procedure and method
- Tool or reviewer identity and version where applicable
- Observation timestamp
- Evidence references
- Observed behavior
- Accessibility impact
- Severity and justification
- Recommended remediation
- Reverification procedure
- Assessment limitations

### Permitted result states

- `verified-failure`
- `verified-pass`
- `observation`
- `needs-manual-review`
- `not-applicable`
- `not-tested`
- `inconclusive`

An automated scan passing must never imply full WCAG conformance.

No untested, incomplete or inconclusive criterion may be silently converted into a verified pass.

Severity is distinct from normative conformance status.

### Severity levels

- **Critical:** An essential task is inaccessible without a viable alternative.
- **High:** Major barrier to navigation, understanding or task completion.
- **Medium:** Significant difficulty or avoidable workaround.
- **Low:** Limited or isolated accessibility impact.

## 4. Architecture Decisions

**A11Y-ADR-01:** Reuse existing GC-AUDIT assessment infrastructure.

**A11Y-ADR-02:** External targets must not require Governance Commons SDK, Cockpit, or target-side instrumentation.

**A11Y-ADR-03:** Initial assessment execution must be read-only.

**A11Y-ADR-04:** Human evaluation and automation findings must be distinguishable.

**A11Y-ADR-05:** Do not use an overall accessibility score as the primary assessment result or acceptance gate.

**A11Y-ADR-06:** Preserve existing authorization, target-scoping, provenance, evidence-integrity, and trust boundaries.

Use established GC-AUDIT contracts wherever possible.

Do not introduce another evidence ledger, reporting service, or universal assessment runtime.

## 5. Website Pilot

**Authorized target:** `https://governancecommons.org`

Proposed six-page maximum sample:

1. `/`
2. `/components/`
3. `/about/`
4. `/observatory/`
5. `/conformance/`
6. `/release/`

Verify which pages exist. If a proposed route is unavailable, select another representative public page within the six-page limit and document the substitution.

### Required assessment scenarios

- Automated accessibility checks using an established engine such as axe-core.
- Keyboard navigation and visible focus.
- Accessible names, roles and states.
- Semantic HTML, headings and landmarks.
- Image alternatives.
- Color contrast.
- 200% text resizing.
- Reflow at the WCAG-required equivalent viewport.
- Accessible navigation and links.
- Dynamic behavior when present.
- Screen-reader review where actually available.

Document browser, viewport, tool versions, test conditions, and manual-review limitations.

Do not claim screen-reader verification if no screen-reader evaluation was performed.

Do not modify the live website.

## 6. AC-01 through AC-12 — Acceptance Criteria

| ID | Requirement |
| --- | --- |
| AC-01 | Existing GC-AUDIT target, evidence, authorization and reporting contracts are reused. |
| AC-02 | WCAG 2.2 A/AA criteria are mapped with valid normative references and applicability handling. |
| AC-03 | Read-only external website assessment enforces authorization and navigation boundaries. |
| AC-04 | At least one independent external test fixture works without a Governance Commons SDK or Cockpit dependency. |
| AC-05 | Automated accessibility checks produce evidence-linked findings with appropriate uncertainty. |
| AC-06 | Manual-review procedures cover all ten accessibility assessment domains. |
| AC-07 | Human-readable reporting explains accessibility impact, evidence, remediation and reverification. |
| AC-08 | Machine-readable report and evidence manifest export through existing mechanisms. |
| AC-09 | A bounded governancecommons.org pilot produces a reproducible assessment report with no more than six sampled pages. |
| AC-10 | Tests prove that untested criteria cannot become passes and incomplete assessments cannot claim full conformance. |
| AC-11 | No modifications to the live website or unrelated audit domains occur. |
| AC-12 | Independent CLI or library execution is documented and verified with clean installation and tests. |

## 7. Definition of Done

GC-AUDIT-A11Y-001 v0.1 is complete when:

1. AC-01 through AC-12 have passing acceptance evidence.
2. The portable accessibility assessment executes successfully.
3. The public website pilot produces a real assessment package.
4. The report distinguishes verified failures, observations, manual-review requirements, and untested criteria.
5. At least one deliberately inaccessible test fixture demonstrates defect detection, remediation guidance, and successful reverification.
6. Evidence and provenance are retained using existing GC-AUDIT contracts.
7. Existing regression and security checks remain green.
8. An independent consumer can run the assessment.
9. The milestone is presented for owner approval.

A complete WCAG conformance claim is not required.

## 8. Development Discipline

Follow GC-DD-01 / OBDD.

**BLOCKER**

- Unsafe external website access
- Missing or incompatible evidence integrity
- Inability to respect authorized scope
- Inability to execute the required assessment safely

**REQUIRED**

- Portable A11Y profile
- WCAG mapping
- Automated check integration
- Manual-review procedures
- Human-centered reporting
- Evidence export
- Bounded website pilot
- Regression and security testing

**DEFERRED**

- Full-site scanning
- Continuous monitoring
- Browser extensions
- Compliance certification
- Automated AI remediation
- HCI/usability scoring
- Multi-application management dashboards
- Unrelated audit framework expansion

## 9. Implementation Instructions

Treat this specification as the authoritative milestone scope for GC-AUDIT-A11Y-001.

Inspect the existing eighteen-control GC-A11Y draft before making changes. Preserve its identifiers and reconcile them with the ten assessment domains.

Use the repository's existing document layout to establish a canonical specification file, for example `docs/audits/GC-AUDIT-A11Y-001.md` if that matches conventions.

Implement the smallest viable solution satisfying AC-01 through AC-12.

Run the bounded website pilot, preserve evidence, complete the acceptance matrix, and open a focused pull request.

Do not merge, deploy, or modify the public website without separate owner authorization.

**Final objective: A working, independently usable accessibility audit that gives developers evidence-backed, actionable guidance.**
