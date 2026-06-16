# AI Access Boundaries — gc.profile.doc-vault

This document defines what AI systems, language models, and AI-assisted tools may and may not access in a repository governed by `gc.profile.doc-vault`.

---

## What AI may access

- Public governance files (README files, public templates, open schemas)
- Non-sensitive internal governance files (policies, SOPs, internal checklists)
- Naming and classification assistance (suggesting filenames, categorizing documents)
- Template generation (producing draft templates for human review)
- Folder structure analysis (identifying gaps, missing indexes, naming inconsistencies)
- Version index files (reading version history for non-sensitive records)
- Document-index files (reading the document registry)

---

## What AI must not access

- EIN letters and tax identification numbers
- Bank account numbers, routing numbers, and banking documents
- Signed legal agreements containing personal or financial data
- Personal addresses, phone numbers, and identification documents
- Social Security Numbers and government-issued ID numbers
- IP assignments containing private valuation or ownership details
- Credentials, passwords, API keys, and secrets
- Signature pages and notarized documents

---

## Redaction rule

When AI assistance is required for a document that contains restricted data, use a redacted copy. Remove or replace all restricted fields before providing the document to an AI system.

Log all redaction actions in the redaction log.

---

## AI-generated documents require human review

AI systems may generate:

- Draft templates
- Draft policy documents
- Draft governance schemas
- Draft folder structures
- Draft version indexes

AI-generated legal, tax, and compliance documents must be reviewed by a qualified human advisor before execution. AI output is never an executed record.

---

## AI must never receive secrets

No AI system, chat interface, or AI-assisted tool should ever be given:

- Passwords
- API keys or tokens
- Private keys
- Access credentials of any kind

If a document contains credentials, redact or remove them entirely before sharing.

---

## Scope note

These boundaries apply to all AI tools including but not limited to:

- Large language models (Claude, GPT, Gemini, etc.)
- AI coding assistants (Copilot, Codex, Cursor, etc.)
- AI document tools
- Automated classification or indexing systems

The same rules apply regardless of the AI provider or interface used.
