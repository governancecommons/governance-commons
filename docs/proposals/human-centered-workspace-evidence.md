# Human-centered workspace proposal — review evidence

**Date:** 2026-11-04
**Scope:** documentation proposal only; branch `proposal/hci-workspace-standard-20261104`.
**Disposition:** proposed for maintainer review; no GC standard, HCI operation, accessibility conformance, or release acceptance claimed.

## Source and authority checks

- Read GC charter/planning authority, RFC process, `GC-AUDIT-A11Y-001`, `GC-A11Y-PROCEDURES-003`, HCI schema README, ONS boundary, and open HCI research PR #5.
- Existing HCI schemas model profile, criterion, evidence, finding and report data, but do not operate an audit or prove participant behavior.
- The proposal preserves the ten A11Y assessment domains and eighteen procedure IDs and leaves the identifier unassigned pending RFC review.

## Validation record

| Check | Result | Limit |
| --- | --- | --- |
| `validate-planning.ps1 -TargetPath .` | PASS, 27 planning docs | Planning shape only. |
| `validate-playbook.ps1 -TargetPath .` | PASS, 0 warnings | PLAY schema only; preflight stamp was late. |
| `validate-recent-work.ps1 -Level 1 -Summary` | FAIL | Inherited review-grammar topology failure; other eight reported health categories passed. |
| `validate-recent-work.ps1 -Level 4 -Summary` | FAIL | Same review-grammar failure; two pre-existing unchecked `DEV-RELEASE.md` gates remain. |
| `validate-zero-trust.ps1 -TargetPath . -PortfolioRoot C:\dev` | PASS, 0 errors and 2 warnings | Existing unregistered `validate-portfolio-health.ps1` and shell-delegation warning. |
| `uv run --no-project --with jsonschema python -m unittest discover -s gc-audit/hci/tests -v` | FAIL, 3 errors in 4 tests | Existing finding schema puts `allOf` under `properties`, invalid under JSON Schema 2020-12. No schema was edited here. |
| `git diff --check` | PASS | Whitespace only. |

No screenshots, participant sessions, accessibility review, or production UI verification occurred. The HCI schema defect and GC-AUDIT topology failure need separately authorized remediation; this proposal does not narrow or override those failures. The review PR and exact commit identify the final Git artifact.

## 2026-11-04 architecture review addendum

The charter review found that `GC-CHARTER-004` currently enumerates Agent Dossier, Agent Matrix, and ONS. The GC OSS baseline is frozen, and the existing HCI research and schema work is candidate GC-AUDIT infrastructure rather than normative HCI authority. The proposal now recommends a bounded human–AI interaction assurance scope while retaining the complete workspace design as non-normative product guidance. [Issue #22](https://github.com/governancecommons/governance-commons/issues/22) requests the maintainer's scope decision and RFC number. No AL:2 or AL:3 decision, RFC acceptance, charter amendment, or standard activation has occurred.

## 2026-11-04 founder authorization addendum

The founder confirmed GC ownership of the bounded human–AI interaction assurance proposal and authorized an RFC draft. `RFC-0002` is the numbered public-comment draft. This authorization resolves the *drafting* scope; it does not accept the RFC, amend `GC-CHARTER-004`, activate a specification, publish a release, or certify a product. The HCI specification identifier remains unassigned.

### RFC draft verification

The draft contains all seven sections required by `rfcs/RFC-PROCESS.md`; it preserves the separate charter activation gate and proposes no changes to existing spec schemas or controls. The planning validator passed all 27 documents, PLAY validation passed with zero warnings, the staged PASS-citation check passed, and `git diff --cached --check` was clean. W3C's current WCAG 2.2 Recommendation and WCAG-EM 2.0 Group Note were checked as primary sources; the RFC distinguishes the normative WCAG criteria from the informative methodology. GC-AUDIT Level 1/4 were not rerun because their inherited failure class had already repeated in the previous proposal and the validation-loop stop rule calls for a separate tooling PLAY.
