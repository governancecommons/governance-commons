# [entity name] — Document Lifecycle & Version Governance Policy
**Policy Code:** [policy code]  
**Status:** Draft  
**Version:** v0-1  
**Effective Date:** [effective date]  
**Approved By:** [approver]  
**Applies To:** [entity name] and all wholly-owned subsidiaries

---

## 1. Purpose

This policy establishes the mandatory lifecycle, versioning, storage, and archival standards for all legal, governance, operational, and intellectual-property documents produced or maintained by [entity name].

Its purpose is to ensure:

- integrity of official records
- traceable version history
- non-repudiable audit trails
- consistent naming and storage conventions
- separation of editable sources from executed records
- long-term organizational continuity

This policy is binding across all [entity name] entities.

---

## 2. Scope

This policy applies to all documents classified as:

- **Legal** — operating agreements, articles, resolutions, filings, registered agent documents
- **Governance** — policies, procedures, charters, standards
- **IP & Ownership** — assignments, licensing agreements, transfers
- **Financial & Tax** — EIN letters, bank agreements, CPA deliverables, tax records
- **Contracts** — vendor agreements, NDAs, service agreements

It does not apply to ephemeral working notes, internal chat logs, or non-binding drafts outside the formal lifecycle.

---

## 3. Document Classes

| class | examples | default retention |
|---|---|---|
| legal-formation | articles, operating agreement, EIN | permanent |
| legal-contract | vendor agreements, NDAs | seven-years |
| governance-policy | internal policies, SOPs | until-superseded then seven-years |
| ip-assignment | pre-formation assignments, licensing | permanent |
| finance-tax | tax returns, bank statements | seven-years |
| finance-banking | account agreements, statements | seven-years |
| admin-filing | state filings, annual reports | permanent |
| project-record | project charters, briefs | until-project-close |
| reference | guidance docs, templates | one-year or until-superseded |

---

## 4. Document Lifecycle

### 4.1 Internal Documents

All internally produced governed documents follow this lifecycle:

```
draft → review → approved-for-execution → executed → (superseded) → archived
```

**Draft** — Editable `.docx` stored in `working/`. Version begins at `v0-1`.

**Review** — Under formal review in `review/`. Version increments through `v0-x`.

**Approved for Execution** — Approved and ready for signing. No further edits permitted.

**Executed** — Signed or formally adopted. Immutable `.pdf` in `executed/` alongside `.docx` source. Version is `v1-0` or above. PDFs must never be overwritten.

**Superseded** — Replaced by a newer executed version. Moves to `archive/superseded/`.

**Archived** — No longer active. Retained per retention schedule.

### 4.2 External Records

External documents bypass the internal lifecycle and enter as one of three status types:

**`issued`** — Formally assigned by a government authority (EIN letter, licenses, permits).

**`confirmation`** — Receipt or acknowledgment that an action occurred (filing receipts, confirmations).

**`received`** — Sent by a third party (bank agreements, CPA deliverables, vendor contracts originated externally).

External records are treated as immutable from point of receipt.

---

## 5. File Naming Standard

All governed documents follow this naming schema:

```
[entity prefix].{domain}.{category}.{status}.{version}.{date}.{extension}
```

**Status values:**

| status | applies to |
|---|---|
| draft | internal draft |
| review | under formal review |
| executed | signed or filed by [entity name] |
| source | editable DOCX paired with executed PDF |
| issued | assigned by an authority |
| confirmation | receipt or acknowledgment |
| received | sent by a third party |
| amendment | change to an executed agreement |
| restated | materially revised replacement |

**Examples:**
```
[entity prefix].legal.operating-agreement.draft.v0-1.YYYY-MM-DD.docx
[entity prefix].legal.operating-agreement.executed.v1-0.YYYY-MM-DD.pdf
[entity prefix].legal.operating-agreement.source.v1-0.YYYY-MM-DD.docx
[entity prefix].legal.ein-letter.issued.v1-0.YYYY-MM-DD.pdf
[entity prefix].legal.state-filing-receipt.confirmation.v1-0.YYYY-MM-DD.pdf
```

---

## 6. Version Semantics

| version | meaning |
|---|---|
| v0-1 | initial draft |
| v0-2 through v0-9 | revised drafts |
| v1-0 | first executed version |
| v1-1 | amendment or minor revision |
| v2-0 | restated or materially revised agreement |

Executed versions may only be replaced by amendments or restatements. They must never be overwritten.

---

## 7. File Formats

**DOCX** — Editable source. Used for drafting, editing, tracked changes, and template reuse.

**PDF** — Official record. Used for signed documents, filings, and archival proof.

The PDF is the legal snapshot. The DOCX is the editable source. Both must be retained for all internally executed documents. External records are retained in the format received.

---

## 8. External Documents

External records enter the repository directly as `issued`, `confirmation`, or `received`. They:

- Bypass the draft/review/executed workflow
- Are treated as immutable from point of receipt
- Are retained in the format received
- Receive the same metadata, access level, and retention category as equivalent internal records

---

## 9. README and Platform Exceptions

README files (`.md`) used for folder navigation and documentation purposes are exempt from the full version control lifecycle. They should be:

- Updated in place as the folder contents change
- Kept current and accurate
- Not treated as governed records subject to the executed/archive workflow

Templates stored in `templates/` folders are also exempt from the executed lifecycle unless formally adopted as policy.

---

## 10. Version Index Requirement

Each governed document folder must contain a version index file:

```
[entity prefix].{domain}.{category}.version-index.{year}.md
```

Required columns: `version | status | date | file | owner | notes`

The version index is mandatory. It is the authoritative version log, audit trail, and chain-of-custody record.

---

## 11. Storage & Access

**Storage locations:**
- Private cloud — all legal, financial, IP, and executed documents
- Local encrypted backup — redundant copy of all critical documents
- Public repositories — only non-sensitive governance schemas, templates, and README files

**Access levels:** owner-only | trusted-advisor | division-level | internal | public

Never store EIN letters, bank documents, tax records, signatures, or personal data in public repositories or AI-accessible systems without redaction.

---

## 12. Archive Rules

- Old drafts → `archive/old-drafts/`
- Superseded executed records → `archive/superseded/`
- Destroyed records require a destruction log entry before deletion
- Legal hold prevents all disposition and destruction
- Archive index must record: original path, archive date, reason, superseded_by, retention category

---

## 13. Compliance & Enforcement

This policy is binding for all [entity name] entities and personnel. Violations must be corrected immediately. [approver] is the final authority on interpretation and enforcement.

---

## 14. Policy Review

This policy must be reviewed annually or upon major structural changes to [entity name].

---

*This document is subject to [policy code] versioning. When executed, the signed PDF becomes the official record.*
