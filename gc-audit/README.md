# GC-AUDIT Registry

## Standalone ZTA repository pilot

The native Gate 1 CLI runs with Python 3.11 or 3.12, Git, `jsonschema[format]>=4.18,<5`, and `cryptography>=42,<47`. From this repository root, after installing those Python dependencies, run:

```text
python gc-audit/tools/zta_cli.py assess --target <absolute-local-git-root> --target-id <identifier> --profile zta.library.v1 --authorize-local-read --output <path-outside-target>/report.json
python gc-audit/tools/zta_cli.py verify --report <path-outside-target>/report.json --target <absolute-local-git-root>
```

`--authorize-local-read` records the operator's explicit selection of a local target. The command requires a clean Git tree and reads only local Git metadata and the bundled ZTA catalog. It does not execute target code, invoke Cockpit or an AI provider, or make network calls. Install dependencies before running offline. Export is written only outside the target. `verify` can reopen the report without the target, or compare the exact revision and tracked blob manifest when `--target` is supplied.

The supported `zta.library.v1` pilot uses the existing deterministic evaluator. Its 24 control results remain `UNVERIFIED` without independently authenticated, revision-bound proof. The Git inventory verifies repository facts, not runtime Zero Trust behavior. The report's SHA-256 digest detects accidental or hostile edits to an existing report but is not a signature or an authority grant. See [the real portal-kit pilot](reports/portal-kit-gate1.md) for findings, limits, and acceptance status.

## Portal application behavioral pilot

With Node.js 22+ installed, the [Portal pilot adapter](tools/portal_behavioral_assessment.py) starts the actual local Portal HTTP server using a disposable data directory and synthetic memberships, then exercises selected request and editorial-store boundaries. It accepts only a clean, explicitly authorized local Portal checkout. Example:

```text
python gc-audit/tools/portal_behavioral_assessment.py assess --target <absolute-Portal-root> --authorize-local-test --output <path-outside-Portal>/portal-application-zta-pilot.json
python gc-audit/tools/portal_behavioral_assessment.py verify --report <path-outside-Portal>/portal-application-zta-pilot.json --target <absolute-Portal-root>
```

The adapter requires the same Python dependencies as the repository pilot. Its evidence is `LOCAL_ASSERTION_ONLY`; it does not authenticate a host or convert HTTP statuses into ZTA control PASS. The [pilot assessment](reports/portal-application-zta-pilot.md) records the actual target revision, methods, observations, limits and reproducibility steps.

## Signed evidence verification pilot

`tools/trusted_evidence.py` provides versioned, Ed25519 signed host-policy and producer-evidence verification with freshness, revocation, scope, exact-target and persistent replay checks. A valid package authenticates a producer **relative to a host-configured root** and leaves every ZTA control `UNVERIFIED`. See [the contract](CONTRACTS.md#trusted-evidence-authentication-v1) and [the synthetic proof](specifications/GC-AUDIT-EVIDENCE-001.md). Reproduce its accepted and rejected packages with:

```text
python gc-audit/tools/verify_evidence_demo.py --verify gc-audit/reports/evidence-001-verification.json
```

## Local host integration pilot

`tools/local_evidence_host.py` loads a host-owned configuration, signed policy
and persistent replay ledger outside the target, checks owner/permissions and
path boundaries, then calls the existing evidence verifier. It requires a
deployment-supplied configuration digest pin. The [threat model and assessment](specifications/GC-AUDIT-EVIDENCE-002.md)
document the exact roles, filesystem checks, synthetic demonstration and
remaining same-principal limit. Reopen the [machine report](reports/evidence-002-local-host.json) with:

```text
python gc-audit/tools/verify_local_host_demo.py --verify gc-audit/reports/evidence-002-local-host.json
```

The demo is not an operational host command. It retains `CONFIGURED_ROOT_ONLY`
and `UNVERIFIED` rather than claiming independent authority or ZTA control PASS.

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
