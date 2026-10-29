# GC-AUDIT-A11Y-001 — Governance Commons public site pilot

Status: bounded automated observation, 2026-10-28 UTC. No WCAG conformance claim or manual reviewer sign-off.

## Scope and method

The owner explicitly authorized read-only assessment of `https://governancecommons.org`. The proposed `/components/` route returned HTTP 404 in the availability check, so `/ecosystem/` replaced it. The six sampled pages were `/`, `/ecosystem/`, `/about/`, `/observatory/`, `/conformance/`, and `/release/`. Each returned HTTP 200 in the assessment. This was a structured, small public sample, not all pages or complete processes under [WCAG-EM 2.0](https://www.w3.org/TR/2026/NOTE-wcag-em-2-20260723/).

Chromium 156.0.8078.4, Playwright 1.64.1 and axe-core 4.14.0 ran in a fresh browser context at 1280×800 CSS pixels. The browser's direct proxy was blocked; the assessor fetched only authorized HTTPS-origin GET resources after public IPv4 validation. WebSockets, service workers, active requests and outside-origin traffic were blocked. The six pages used 20 resource requests, about 2.4 MB, with no blocked request in the final run. The report records timestamps, individual URLs, tool versions, request observations, element selectors, rule outcomes and integrity digests.

The tool also recorded page structure, 320 CSS-pixel page-wide horizontal overflow and a 200% root-font-size override. No page-wide overflow was observed in those two configurations. These checks are geometry observations; they do not establish successful text-only zoom, no clipped content, or full WCAG 1.4.4/1.4.10 coverage.

## Confirmed automated rule failures

| ID | WCAG | URL/element | Behavior and impact | Remediation and reverification |
| --- | --- | --- | --- | --- |
| `A11Y-8c978c93bd9749b3` | 1.4.3 AA | `/release/`, first `pre > code` | Axe measured foreground `#124234` on `#111a16` at 1.56:1 for normal-size text, below 4.5:1. The code text may be difficult to read for people with low vision. Severity **High** reflects a substantial reading barrier; task-specific impact needs human review. | Adjust code text/background colors to at least 4.5:1, including relevant states. Re-run axe `color-contrast`, inspect computed colors and visually verify the rendered code block. |
| `A11Y-f5a31284a26ce587` | 1.4.3 AA | `/release/`, second `pre > code` | Same measured colors and 1.56:1 ratio. | Apply and verify the same correction on the second block. |

These are automated rule failures tied to [WCAG 2.2 SC 1.4.3](https://www.w3.org/TR/2024/REC-WCAG22-20241212/#contrast-minimum). The machine report contains each selector, observation, severity rationale, evidence reference, remediation and verification instruction. No live site change was made.

## Open review and interpretation

- Axe produced 56 `needs-manual-review` node results: 55 color-contrast inconclusive nodes and one `aria-prohibited-attr` inconclusive node. These are not confirmed failures or passes.
- The 55-criterion ledger contains one criterion with automated failure evidence, 38 requiring manual review and 16 not tested by the representative domain mappings. None was inferred to pass from an automated rule pass. WCAG 4.1.1 was excluded as obsolete.
- Keyboard traversal, focus order, accessible-name accuracy, image alternative quality, form/error behavior, dynamic announcements, responsive content visibility, and screen-reader operation were not manually performed. The sample had no forms; that does not establish whole-site form inapplicability.
- The source draft `GC-A11Y-01` through `GC-A11Y-18` was preserved without treating its proposed procedures as executed evidence. No HCI or legal conclusion is drawn from this scan.

## Evidence and reproduction

Machine report: [a11y-001-governancecommons-org.json](a11y-001-governancecommons-org.json). Human-readable finding report: [a11y-001-governancecommons-org.md](a11y-001-governancecommons-org.md). SHA-256 canonical report digest: `sha256:08e2b4cbe571e563863b95ef22d77b8727b6d1e159b0a6025f6df8996666acf2`. The digest is an integrity check, not an authenticated attestation. The manifest and each finding are embedded in the report. A future rerun should use `--prior` to link the old digest while preserving both directories.

From `gc-audit/a11y` after `npm ci` and `npx playwright install chromium`:

```text
node src/cli.mjs assess --origin https://governancecommons.org --paths /,/ecosystem/,/about/,/observatory/,/conformance/,/release/ --authorize-read-only yes --target-id governancecommons.org --output NEW_DIRECTORY
node src/cli.mjs verify --report ../reports/a11y-001-governancecommons-org.json
```

Reproduction against a live site can differ as content and CSS change. The report is tied to its recorded time and browser/tool versions, not a pinned deployment revision.
