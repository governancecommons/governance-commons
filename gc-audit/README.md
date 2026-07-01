# GC-AUDIT Registry

**Status:** active
**Authority:** DEV-ACCORD.05

This directory owns the central GC-AUDIT tool index.

The current registry is:

```text
GC-AUDIT-REGISTRY.yaml
```

Authoritative GC-AUDIT scripts live under:

```text
governance-commons/gc-audit/tools/
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
