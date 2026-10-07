# Adopters — Governance Commons

This file lists projects and organizations that have declared conformance with one or more
named Governance Commons specifications at named versions. Declarations are self-reported;
Governance Commons does not operate a certification program.

---

## How to add your project

1. Choose the named specification and exact version your system implements.
2. Check the support matrix in
   [docs/conformance/badge-criteria.md](docs/conformance/badge-criteria.md). When the published
   Python toolkit supports the selected specification, run:
   ```
   gc-validate --spec <spec-name> --profile <advisory|standard|strict>
   ```
3. Where no published validator supports the selected specification and version, label the
   declaration `manual` or `provisional` and document the checks performed. Do not present a
   repository test suite as independent certification.
4. Open a pull request adding a row to the table below.
5. Include the generated ConformanceReport or documented manual evidence as a linked artifact.

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
| **standard** | Passes an available published validator for all evaluated `MUST` rules |
| **strict** | Passes an available published strict profile and retains the required signed evidence bundle |

Full criteria: [docs/conformance/badge-criteria.md](docs/conformance/badge-criteria.md)
