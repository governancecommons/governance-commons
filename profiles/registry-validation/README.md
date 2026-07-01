# gc.profile.registry-validation

**Governance Commons Registry Validation Profile**  
**Profile ID:** `gc.profile.registry-validation`  
**Version:** `0.1.0`  
**Status:** Draft

## What It Is

`gc.profile.registry-validation` defines how GC-AUDIT validates registry truth
across three registry profiles:

| Profile | Registry | Status |
| --- | --- | --- |
| `gc` | `passes.registry.json`, registry changelog, namespace, layers | active |
| `dcp` | `projects.yaml` portfolio registry | active |
| `dxp` | DXP/Marlin package and tool registry | planned |

The profile belongs to GC-AUDIT. DCP, Cockpit, Marlin, and agents may call the
tools, but they must not duplicate registry validation logic.

## Zero-Trust Alignment

Registry validation is validate-only by default and fails closed:

- runnable validation scripts are GC-AUDIT allowlist entries
- registry paths must be local relative paths inside the portfolio root
- external registry paths must be local relative paths inside the portfolio root
- network registry fetches and absolute registry paths are forbidden
- `dxp` remains blocked until package/tool schema authority is declared
- normalization apply, schema authority changes, and git branch/remote splits require explicit human authorization

The portfolio root is not machine-specific. Callers may pass `-PortfolioRoot`
when GC-AUDIT is installed in CI, a packaged app, a nested workspace, or any
layout where the governance-commons repository is not a direct child of the
portfolio/control-plane root.

## Active Validator

```powershell
governance-commons/gc-audit/tools/validate-registry.ps1 -Profile gc
governance-commons/gc-audit/tools/validate-registry.ps1 -Profile gc -PortfolioRoot <portfolio-root>
governance-commons/gc-audit/tools/validate-registry.ps1 -Profile dcp
```

`-Profile dxp` intentionally fails until the DXP/Marlin registry schema exists.

## GC Checks

The `gc` profile validates:

- registry JSON and changelog JSONL parse
- registry paths resolve
- PASS files with `Canonical ID` appear in the registry
- PASS headers agree with registry ID, alias, cluster, status, timestamp, and dependencies
- registry layers exist in `passes/layers.yaml`
- registry namespace matches `passes/namespace.yaml`
- local dependencies resolve
- external dependencies resolve when requested
- registry entries have changelog rows

## DCP Checks

The `dcp` profile delegates to `validate-pointers.ps1` for `projects.yaml`
pointer truth. Deeper DCP registry checks may be added without moving ownership
out of GC-AUDIT.

## DXP Status

The `dxp` profile is blocked until the DXP/Marlin package and tool registry schema
is defined. The validator must fail closed rather than inventing a registry shape.

## Normalization

Registry normalization is planned and must be preview-first. Applying a
normalization requires explicit human authorization and must write a diff report
before changing files.
