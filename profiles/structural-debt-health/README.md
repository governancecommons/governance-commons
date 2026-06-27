# gc.profile.structural-debt-health

**Governance Commons Structural Debt Health Profile**  
**Profile ID:** `gc.profile.structural-debt-health`  
**Version:** `0.1.0`  
**Status:** Draft

## What It Is

`gc.profile.structural-debt-health` defines a portable report contract for
structural debt scans in governed code repositories and portfolios.

It gives DCP, eco, and other tools a shared meaning for:

- tracked generated/debug artifacts
- legacy, shim, compatibility, workaround, and stale-reference markers
- intentional deprecation vocabulary in standards and schemas
- pass/warn/fail health semantics

## Layer Responsibilities

| Layer | Responsibility |
| --- | --- |
| Governance Commons | Defines this profile and report contract. |
| DCP | Implements portfolio scanning and emits a conforming JSON report. |
| eco | Consumes the report as a health signal. |

Governance Commons does not include validator implementation code in this
profile. Validator code belongs in DCP or another adopting tool.

## Minimum Report Contract

A conforming report includes:

```json
{
  "profile": "gc.profile.structural-debt-health",
  "profile_version": "0.1.0",
  "status": "pass | warn | fail",
  "checked_repos": 0,
  "checked_files": 0,
  "failure_count": 0,
  "warning_count": 0,
  "failures": [],
  "warnings": [],
  "generated_artifact_policy": "fail",
  "marker_policy": "warn"
}
```

## Status Semantics

| Status | Meaning |
| --- | --- |
| `pass` | No failures or visible warnings. |
| `warn` | No failures, but visible human-review warnings remain. |
| `fail` | Generated/debug artifacts, missing registered paths, or scanner execution failure. |

## Intentional Categories

The profile allows tools to suppress known non-debt categories:

- formal deprecation vocabulary in specs, schemas, and tests
- published schema or site copies
- changelog and history records
- known active compatibility support
- scanner/self and lockfile metadata

Suppressions must not hide generated/debug artifact failures.

