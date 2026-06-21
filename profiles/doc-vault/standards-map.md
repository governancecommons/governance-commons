# Standards Alignment Map — gc.profile.doc-vault

This map describes how `gc.profile.doc-vault` relates to established records management and governance standards.

**Important:** This profile does not make an organization compliant, certified, audit-ready, or legally sufficient under any of these standards. Language used throughout is intentionally qualified: "aligned with," "informed by," "supports readiness for," and "provides structure for."

---

## ISO 15489 — Records Management

ISO 15489 establishes fundamental concepts and principles for creating, capturing, and managing records, including metadata, policies, responsibilities, monitoring, and records processes.

`gc.profile.doc-vault` is **aligned with** ISO 15489 in the following ways:

- Defines required metadata fields for each record (record_id, document_type, lifecycle_state, retention_category, etc.)
- Requires a document lifecycle with defined states from creation through disposition
- Requires retention schedules with defined categories and periods
- Requires archive rules including disposition, destruction logging, and legal hold
- Requires version indexes as chain-of-custody records
- Supports policies for records integrity, access control, and sensitive data handling

---

## ISO 9001 — Documented Information Controls

ISO 9001 Clause 7.5 requires organizations to control documented information: ensuring it is available, protected, accessible, and preserved with version integrity.

`gc.profile.doc-vault` **provides structure for** ISO 9001-style document control:

- Separates editable sources (DOCX) from official records (PDF)
- Requires version numbering and version indexes
- Defines review and approval stages before execution
- Prevents overwriting of executed records
- Requires archival of superseded versions
- Defines access levels to protect sensitive documented information

---

## NIST Cybersecurity Framework 2.0

NIST CSF 2.0 includes governance outcomes around identity management, access control, data security, and information protection.

`gc.profile.doc-vault` **supports readiness for** NIST CSF 2.0 concepts in the following areas:

- Access control: defines owner-only, trusted-advisor, division-level, internal, and public access tiers
- Data security: defines sensitive data flags and handling rules
- AI access boundaries: defines what AI systems may and may not access
- Audit trail: requires version indexes and chain-of-custody logs
- Incident response readiness: includes legal hold rules and destruction logging

---

## ARMA Generally Accepted Recordkeeping Principles (GARP)

ARMA's principles emphasize accountability, transparency, integrity, protection, compliance, availability, retention, and disposition.

`gc.profile.doc-vault` is **informed by** ARMA GARP principles:

| ARMA Principle | Profile Support |
| --- | --- |
| Accountability | Managing Member ownership and policy enforcement |
| Transparency | Version indexes, audit trails, chain-of-custody logs |
| Integrity | Immutable executed records, checksum support |
| Protection | Access matrix, sensitive data flags, AI boundaries |
| Compliance | Retention schedules, legal hold overrides |
| Availability | Defined storage locations, structured folder hierarchy |
| Retention | Retention schedule template with defined categories |
| Disposition | Archive rules, destruction logging, legal hold prevention |

---

## SOC 2 Readiness Concepts

SOC 2 evaluates security, availability, processing integrity, confidentiality, and privacy controls.

`gc.profile.doc-vault` **supports readiness for** SOC 2 concepts but **does not claim SOC 2 compliance**:

- Access controls and access level definitions support CC6 (Logical and Physical Access)
- Audit logs and version indexes support CC7 (System Operations)
- Sensitive data handling and AI boundaries support CC9 (Risk Mitigation)
- Retention and disposal rules support A1 (Availability) and C1 (Confidentiality)

A SOC 2 audit requires a qualified auditor. This profile provides structural readiness only.

---

## Internal Governance / Founder-Led LLC Controls

For single-member LLCs, holding companies, studios, and small businesses without formal compliance teams, `gc.profile.doc-vault` **provides structure for** practical internal governance:

- Defines which documents are owner-only vs. advisor-accessible vs. division-level
- Provides policy templates that can be adopted without legal infrastructure
- Defines a practical document lifecycle usable by a solo founder
- Provides folder structure that scales from single-member LLC to multi-entity holding
- Supports AI-assisted document management with defined safety boundaries
