# GC Review Templates

Standardized review and audit templates for portfolio governance.

These templates define the canonical format for recurring governance reviews.
They are consumed by humans running reviews manually and will eventually be
executed by DCP audit tooling (`dcp audit *`, `dcp review *`).

## Templates

| Template | File | Tool command (future) |
| --- | --- | --- |
| Portfolio deliverability review | [deliverable-review.md](deliverable-review.md) | `dcp review deliverables` |
| Repository license audit | [license-audit.md](license-audit.md) | `dcp audit licenses` |
| Compliance and regulatory review | [compliance-review.md](compliance-review.md) | `dcp audit compliance` |

## How to use now (manual)

1. Copy the relevant template
2. Fill in each section against the current state of the portfolio
3. Save the output to `docs/reviews/YYYY-MM-DD-<type>.md` in the portfolio root
4. Review outputs are version-controlled snapshots — do not overwrite, append new runs

## Future tool behavior

DCP audit commands will read `projects.yaml` and known standards (ONS, GC profiles,
GEE schema) to auto-populate these templates. Human review is always required for
compliance and regulatory sections — no automated verdicts.

See `dxp-org/devx-control-plane/DEV-PLAN.md` Track K for tool roadmap.
