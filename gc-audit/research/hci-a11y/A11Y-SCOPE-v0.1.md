# GC-AUDIT-A11Y-001 — Accessibility Research and Scoping v0.1

Status: DRAFT / NOT AN IMPLEMENTED AUDIT / NOT A CONFORMANCE ASSERTION.

## Independent optional capability
Proposed namespace: `gc-audit.a11y`. Independent from `gc-audit.hci`, Cockpit, eco and frontend frameworks; reuse GC evidence/reporting contracts only after verification. Optional adoption may be mandated by an adopting organization's own acceptance profile.

## Initial target
Web/browser-rendered workflows; proposed default **WCAG 2.2 Level AA**, conditional on declared profile and applicable obligations. The audit cannot infer entire-product conformance from a small sample or an automated scan. Desktop, terminal, mobile-native, embedded and assistive technology profiles require separately specified applicability.

## Authority and verification queue
- W3C WCAG 2.2: authoritative success criteria (normative when adopted/applicable).
- W3C ACT Rules: informative test rules; coverage is limited, results not equivalent to full WCAG conformance.
- W3C WCAG-EM / evaluation resources: methodological guidance; verify current version/status.
- WAI-ARIA Authoring Practices: patterns/guidance; verify applicability to selected control.
- EN 301 549: check published version versus legally harmonized version.
- Revised U.S. Section 508, ADA Title II: check governing requirements and dates before mapping.
- WCAG 3.0: research status only until formally applicable.
- ISO and practitioner texts: contextual support; do not substitute for normative text.

This file does NOT claim that the above standards have been fully mapped or their latest versions verified at commit time.

## Unapproved candidate areas (no normative mappings yet)
- A11Y-KEY-001: keyboard operability.
- A11Y-FOC-001: focus behavior and visibility.
- A11Y-NAME-001: accessible names/roles/states.
- A11Y-STAT-001: status messages.
- A11Y-FORM-001: form labels/instructions/errors.
- A11Y-CONTRAST-001: applicable contrast requirements.
- A11Y-STRUCT-001: semantic structure/relationships.
- A11Y-RESP-001: reflow/resize-related behavior.

Each candidate must map to **specific WCAG success criterion ID, version, level and exceptions**, plus applicable method and test coverage, before acceptance. A11Y IDs are local audit criteria, not W3C criteria.

## Evaluation evidence model proposal
Target/version; workflow/scope; normative profile; requirement ID; procedure/version; tool/version; browser/platform/AT configuration; test inputs; observed result; screenshot/log/trace where appropriate; method (automatic/manual/assisted); reviewer role; limitations; outcome; provenance/integrity; human decision.

Separate automated findings, manual observations, WCAG success-criterion determinations, sampled-workflow conclusions and whole-product claims. Candidate outcomes: PASS, FAIL, REVIEW_REQUIRED, NOT_TESTED, NOT_APPLICABLE, INCONCLUSIVE, subject to current GC schema reconciliation.

## Initial pilot candidates (not performed)
GC Portal editorial sign-in/review/approval; GC public site news navigation; Cockpit GUI/Web component interaction. No repository mutation, publication, certification, or executable audit is approved by this research checkpoint.

## Next milestone
GC-A11Y-MAPPING-001: verify standards and obligations using authoritative text, establish normative traceability matrix, testing procedures and coverage; then freeze owner-approved v0.1 contract. Keep HCI and A11Y separate and coordinate only shared evidence semantics.
