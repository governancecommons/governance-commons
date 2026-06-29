# GC Template: Repository License Audit

**STUB — v0.1**
**Status:** Template only. Future: auto-populated by `dcp audit licenses`.

---

## Metadata

| Field | Value |
| --- | --- |
| Audit date | YYYY-MM-DD |
| Auditor | |
| Portfolio root | |
| Entity | |
| IP assignment executed | yes / no / pending |

---

## License Policy Reference

| Layer | Expected license | Rationale |
| --- | --- | --- |
| Open standards (specs, schemas, primitives) | Apache 2.0 | Drives adoption; patent grant protects ecosystem |
| Developer tools (distributable) | GPL v3 + commercial dual | Open use free; proprietary use requires license |
| Commercial products | BUSL 1.1 → Apache 2.0 (4yr) | Monetization window with eventual open release |
| Utilities and modules | MIT | Maximum adoption for low-risk dependencies |
| Early-stage / internal only | None (all rights reserved) | Default copyright; decide at commercialization |

---

## Audit Results

| Repo | Path | License found | Copyright holder | Policy match | Action required |
| --- | --- | --- | --- | --- | --- |
| | | | | yes / no / n/a | |

---

## Findings

### Missing license files

<!-- Repos with no LICENSE file -->

### Wrong copyright holder

<!-- Repos where LICENSE names a person instead of the LLC -->

### Policy mismatches

<!-- Repos where actual license doesn't match expected layer policy -->

---

## Remediation Checklist

- [ ] IP assignment document executed (personal → LLC)
- [ ] All open standards have Apache 2.0
- [ ] All commercial products have BUSL 1.1 or equivalent
- [ ] All distributable tools have dual license (open + commercial)
- [ ] All copyright holders updated to LLC name
- [ ] Changes committed and pushed to all affected repos

---

## Notes

<!-- Any exceptions, intentional deviations, or deferred decisions -->
