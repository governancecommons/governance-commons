# gc.profile.doc-vault

**Governance Commons Doc Vault Profile**  
**Profile ID:** gc.profile.doc-vault  
**Version:** 0.1.0  
**Status:** Draft

---

## What is gc.profile.doc-vault?

`gc.profile.doc-vault` is a Governance Commons profile for governed document repositories. It defines what a well-organized, version-controlled, and policy-aligned document repository should look like — for legal records, finance records, IP vaults, operating agreements, policies, contracts, compliance folders, and founder/business records.

It is not a profile for code repositories. It is not a certification product. It is a governance standard.

---

## What problem does it solve?

Most small businesses, LLCs, studios, and solo operators have document chaos:

- Files named inconsistently or without version numbers
- No clear distinction between drafts, official records, and archived versions
- Legal and financial docs mixed with working notes
- No record of what is current, what is superseded, or what needs review
- Folders that AI agents, advisors, and collaborators cannot navigate reliably

`gc.profile.doc-vault` solves this by defining a clear structure, lifecycle, naming standard, metadata schema, retention rules, and access model for any business document repository.

---

## What it is for

- Single-member LLCs and multi-entity holding structures
- IP vaults and creative asset governance
- Legal document folders (operating agreements, resolutions, filings)
- Finance and tax record management
- Compliance and policy folders
- Business operating records
- Any structured document repository where version control and record integrity matter

---

## What it is not

- It is not a certification product. It does not make your organization SOC 2 compliant, ISO certified, or audit-ready by itself.
- It is not a code repository profile. Use other Governance Commons profiles for software projects.
- It does not replace legal or tax advice. Templates and retention schedules require review by qualified advisors.

---

## Standards alignment

This profile is informed by and aligned with:

- ISO 15489 records management principles
- ISO 9001-style documented information controls
- NIST Cybersecurity Framework 2.0 governance concepts
- ARMA Generally Accepted Recordkeeping Principles
- SOC 2 readiness concepts (not a claim of compliance)

See `standards-map.md` for the full alignment map.

---

## How it works

```
Governance Commons   defines what a governed doc repo looks like
ONS                  defines how records and files are named
DCP (future)         validates whether a repo conforms
```

DCP is not part of this profile's core responsibility. This profile defines the standard. A future validator may inspect conformance, but no validator code is included here.

---

## Adoption

To adopt this profile, add a `.governance/` folder to your document repository root containing:

```
.governance/
├── profile.yml       ← declares gc.profile.doc-vault
├── retention.yml     ← your retention schedule
└── ons.yml           ← your entity prefix and naming rules
```

See `examples/` for a complete adoption example using Osprey Holding LLC.
