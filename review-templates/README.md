# GC Review Templates

Standardized review and audit templates for portfolio governance.

These templates define the **canonical format** for recurring governance reviews.
They describe structure and scoring — not where outputs land. Output location is
determined by the consuming tool (DCP, DVP, or the adopting portfolio's config).

## Templates

| Template | File | DCP command (future) |
| --- | --- | --- |
| Portfolio deliverability review | [deliverable-review.md](deliverable-review.md) | `dcp review deliverables` |
| Repository license audit | [license-audit.md](license-audit.md) | `dcp audit licenses` |
| Compliance and regulatory review | [compliance-review.md](compliance-review.md) | `dcp audit compliance` |

## Authoritative source

This folder (`governance-commons/review-templates/`) is the authoritative source for
these templates. Consuming tools (DCP, DVP) bundle copies of these templates at release
time. If a bundled copy diverges from this folder, this folder wins.

## How to use (manual, without DCP tooling)

1. Copy the relevant template into your portfolio
2. Fill in each section against current state
3. Save the filled output as a dated snapshot (e.g., `YYYY-MM-DD-license-audit.md`)
4. Snapshots are immutable records — do not overwrite; create a new file each run

**Where to save:** Your portfolio's configured reviews output location.
If using DCP: `docs/reviews/` at your portfolio root (see devx-control-plane).
If using DVP: your vault's `.governance/reviews/` folder.
If standalone: any version-controlled folder you designate.

## Future tool behavior

DCP audit commands will read `projects.yaml` and GC standards (ONS, GC profiles,
GEE schema) to auto-populate these templates and emit dated snapshots to the
configured output path. Human review is always required for compliance and
regulatory sections — no automated verdicts.

See `devx-control-plane/DEV-PLAN.md` Track K for the DCP tool roadmap.
