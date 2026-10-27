# GC-AUDIT-ZTA-001D — Adversarial findings reconciliation

Status: DRAFT — read-only inspection of repository main on 2026-10-27.
Purpose: reconcile the submitted adversarial review against merged code before changing enforcement. This report is not an independent security certification.

## Findings and actual closure state

| ID | Submitted issue | Verified repository evidence | Disposition |
| --- | --- | --- | --- |
| AR-01 | 24-control predicates unfrozen | `gc-audit/catalogs/gc-audit.zta-controls.v1.draft.json` exists and `gc-audit/tools/zta_catalog_authority.py` checks all 24 objectives plus an externally pinned catalog digest; only ZTA-08.02 has a complete favorable decision path. | REQUIRED: control-by-control normative sufficiency/adversarial acceptance before enabling further PASS routes |
| AR-02 | Host delegation can launder positive claims | `zta_decision_gate.py` defaults unsupported positive proof to UNVERIFIED. ZTA-08.02 special-case requires separate signed, corroborated evidence. No general delegated-host PASS procedure verified. | REQUIRED before any host-delegated PASS |
| AR-03 | Evidence producer authentication weak | ZTA-08.02 authenticates owner policy, build, execution, installation observers, but caller-owned trust roots and corroboration remain operational assurance dependencies. | PARTIAL: verify external provenance and ownership in real pilot |
| AR-04 | Normalizers mutate without explicit apply | All three `normalize-*.ps1` scripts declare `-Apply`, reject `-Apply -DryRun`, and default to preview. | HISTORICALLY RESOLVED by source inspection; black-box tests still needed |
| AR-05 | Validator exposes mutating `-FixNotes` | `validate-pointers.ps1` no longer exposes that switch. | HISTORICALLY RESOLVED by source inspection; black-box regression still needed |
| AR-06 | Audit registry lacks strong self-audit | `validate-zero-trust.ps1` currently scrapes YAML with regex rather than parsing/validating a canonical structured registry; `validate-registry.ps1` checks GC/DCP/DXP profile registries, not the GC-AUDIT operation allowlist. | OPEN: fail-closed structured allowlist self-validation, mutation/step metadata, path/alias checks |
| AR-07 | Child shell use despite shell-forbidden declaration | ZT4 uses textual shell patterns and emits warnings on matching child process invocations; not a runtime confinement guarantee. | OPEN: inventory actual delegated calls, bound allowed executables and arguments, add negative tests |
| AR-08 | Weak malicious path and Windows/Linux edge tests | Existing `gc-audit/tests` files cover selected Pester scenarios; the minimum path-escape/absolute/network/normalizer fixture set is still described in TESTING-STRATEGY.md rather than fully present as named suites. | OPEN: cross-platform malicious-path fixtures |
| AR-09 | Evidence from static inspection only | ZTA-08.02 verifies signed byte-bound build and installation claims; other controls have no enabled PASS paths. | PARTIAL: independent behavioral evidence for later controls |
| AR-10 | Reassessment and independent-review triggers | Production activation and independently governed trust roots remain outside implementation tests. | DEFERRED until pilot design; do not grant release eligibility |

## Current high-priority threat: registry poisoning

The registry declares `security.execution_model: allowlist`, `shell: forbidden`, and a portfolio-root path policy. Its current ZT1/ZT3 scanner extracts `script:` lines and internal flags with regular expressions. It checks for path containment and unregistered scripts, but a regex-derived view is not a complete semantic parse of the YAML authority document.

Acceptance before registering `gc-audit.zta`:
1. Reject malformed YAML, duplicate keys and operation IDs, unknown executable steps, unsafe paths, absolute paths, traversal and network URIs, including platform-specific variants.
2. Enforce containment after normalization and symlink resolution; reject paths escaping the approved root.
3. Validate declared mutability against supported command flags; no validator may expose apply/fix/write behavior.
4. Fail closed on missing authority, ambiguous aliases and inconsistent allowlist entries. Do not silently downgrade these to warnings.
5. Execute adversarial fixture tests on Windows, Linux and macOS wherever the PowerShell runtime is supported.
6. Keep existing `gc-audit.zerotrust` behavior stable until a replacement checker has acceptance evidence.

## GC-DD-01 work classification

**BLOCKER:** An executable registry allowlist can be redirected to attacker-controlled scripts or unsafe paths without rejection. Verify with negative fixture before calling it a proven exploitable vulnerability.

**REQUIRED:** Add deterministic self-audit and regression tests; independently review outstanding delegation and scope-authorization guarantees before activation.

**DEFERRED:** Broad new PASS routes, continuous scanning infrastructure, UI, publication, certification, and unrelated framework refactoring.

## Scope boundary

This draft records source-derived findings only. No vulnerability exploitation, runtime control-plane assurance, independent sign-off, registration, activation or release is claimed. The next implementation increment should be one parser-backed, fail-closed registry validator plus targeted tests, not new ZTA control families.
