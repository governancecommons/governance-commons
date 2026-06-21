# Adopters — Governance Commons

This file lists projects and organizations that have declared conformance with one or more
Governance Commons standards. Conformance is self-declared until a certification program
exists (targeted for PASS-6).

---

## How to add your project

1. Verify your conformance level using the GC validator:
   ```
   gc-validate --spec <spec-name> --profile <advisory|standard|strict>
   ```
2. Open a pull request adding a row to the table below.
3. Include your conformance report (output of `gc-report`) as a PR attachment or linked artifact.

See [docs/conformance/badge-criteria.md](docs/conformance/badge-criteria.md) for the full
criteria matrix and badge embedding instructions.

---

## Adopters

| Project | Organization | Spec(s) | Profile | Declared | Link |
| --- | --- | --- | --- | --- | --- |
| _(none yet — be the first)_ | | | | | |

---

## Conformance profiles

| Profile | Meaning |
| --- | --- |
| **advisory** | Aware of the standard; structure and naming follow GC conventions |
| **standard** | Passes `gc-validate` for all `MUST` rules at the standard profile |
| **strict** | Passes `gc-validate` at the strict profile; submits a signed evidence bundle |

Full criteria: [docs/conformance/badge-criteria.md](docs/conformance/badge-criteria.md)
