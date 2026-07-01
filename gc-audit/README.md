# GC-AUDIT Registry

**Status:** active
**Authority:** DEV-ACCORD.05

This directory owns the central GC-AUDIT tool index.

The current registry is:

```text
GC-AUDIT-REGISTRY.yaml
```

The current gap analysis is:

```text
GC-AUDIT-GAP-ANALYSIS.md
```

The testing strategy, vocabulary, and fixture approach live at:

```text
TESTING-STRATEGY.md
```

PLAY execution-level obligations and close requirements live at:

```text
PLAY-OBLIGATIONS.md
```

Machine-readable caller contracts live at:

```text
CONTRACTS.md
```

Authoritative GC-AUDIT scripts live under:

```text
governance-commons/gc-audit/tools/
```

Agent preflight authority lives at:

```text
governance-commons/gc-audit/AGENT-PREFLIGHT.md
```

Portfolio-root `.ps1` files are compatibility adapters only. Security-sensitive
callers, including Marlin, Cockpit, and DCP menus, must discover runnable
audit/status/repair/planning operations through the registry instead of
hardcoding script paths or inventing new operation names.

Registry rules:

- Operations use REVIEW-GRAMMAR verb names.
- Scripts are allowlisted by relative path.
- Script paths are resolved relative to the portfolio/control-plane root, not `C:\dev`.
- Callers execute without a shell.
- Mutating operations require preview or explicit apply.
- Unimplemented verbs fail closed until an active allowlisted implementation is registered.

Preflight validator examples:

```powershell
governance-commons/gc-audit/tools/validate-agent-preflight.ps1 -Text "PREFLIGHT: complete | project=c:/dev | order=AGENTS>03>PROTECTED>CONTROL-PLANE>REVIEW-GRAMMAR>02>06>10>projects.yaml>DEV-PATH>DEV-PLAN" -Mode FirstResponse
governance-commons/gc-audit/tools/validate-agent-preflight.ps1 -FilePath .\session-note.md -Mode Session
governance-commons/gc-audit/tools/validate-ci-invariants.ps1 -TargetPath C:\dev\governance-commons
```

## Registry Validation Profiles

Registry validation is profile-based:

```powershell
governance-commons/gc-audit/tools/validate-registry.ps1 -Profile gc
governance-commons/gc-audit/tools/validate-registry.ps1 -Profile dcp -TargetPath C:\dev
governance-commons/gc-audit/tools/validate-registry.ps1 -Profile dxp
```

- `gc` validates GC PASS registry, namespace, layers, changelog, and PASS headers.
- `dcp` validates portfolio `projects.yaml` pointer truth.
- `dxp` fails closed until the DXP/Marlin package registry schema is defined.
