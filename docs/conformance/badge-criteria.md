# Conformance Badge Criteria — Governance Commons

**time.loc:** 2026-06-08T00:00:00Z  
**Defined in:** PASS-5 (GC-5-H-02)

---

## Profiles

Governance Commons defines three conformance profiles. A project declares the highest
profile it satisfies across each spec it adopts.

| Profile | Requirements |
|---------|-------------|
| **advisory** | Structure and naming follow GC conventions; no validator run required |
| **standard** | `gc-validate --spec <name> --profile standard` passes with zero failures |
| **strict** | `gc-validate --spec <name> --profile strict` passes with zero failures; a signed `gc-compliance-evidence` bundle is produced and retained |

---

## Per-spec criteria

### ONS (Ontic Namespace Structure)

| Profile | Criteria |
|---------|---------|
| advisory | All identifiers follow ONS naming grammar; cluster prefix is registered or clearly scoped |
| standard | `gc-validate --spec ons` passes; `rules.json` export is present if distributing a validator |
| strict | standard + `rules.json` is versioned and referenced in conformance report |

### Agent Dossier

| Profile | Criteria |
|---------|---------|
| advisory | A `dossier.yaml` (or equivalent) file exists and follows dossier schema structure |
| standard | `gc-validate --spec dossier` passes; PASS IDs follow `PASS-YYYY-NNNN` format; handoff envelopes carry `emitted_at` |
| strict | standard + signed handoff envelopes (JWS/Ed25519); signed evidence bundle submitted |

### Agent Matrix

| Profile | Criteria |
|---------|---------|
| advisory | An `agent-matrix.yaml` (or equivalent) file exists; capability profiles are declared |
| standard | `gc-validate --spec matrix` passes; SLO/SLI fields present; MCP tool scopes declared |
| strict | standard + A2A and CloudEvents bindings present; signed evidence bundle submitted |

### Agent Project Orchestrator (APO)

| Profile | Criteria |
|---------|---------|
| advisory | A `runtime-contract.yaml` (or equivalent) exists; task graph follows APO schema |
| standard | `gc-validate --spec apo` passes; `time_loc` present in all `telemetry.emit()` calls |
| strict | standard + per-agent resource budgets enforced; signed evidence bundle submitted |

---

## Badge embedding

Badges use [shields.io](https://shields.io) static badge format. Replace `<profile>` with
`advisory`, `standard`, or `strict`, and `<spec>` with the spec short name.

**Markdown:**
```markdown
![gc-ons: standard](https://img.shields.io/badge/gc--ons-standard-green)
![gc-dossier: standard](https://img.shields.io/badge/gc--dossier-standard-green)
![gc-matrix: advisory](https://img.shields.io/badge/gc--matrix-advisory-blue)
![gc-apo: strict](https://img.shields.io/badge/gc--apo-strict-brightgreen)
```

**Color by profile:**

| Profile | Color | shields.io value |
|---------|-------|-----------------|
| advisory | blue | `blue` |
| standard | green | `green` |
| strict | bright green | `brightgreen` |

**Ecosystem badge** (lowest profile declared across all adopted specs):
```markdown
![Governance Commons: standard](https://img.shields.io/badge/Governance%20Commons-standard-green)
```

---

## Declaring conformance

To appear in [ADOPTERS.md](../../ADOPTERS.md):

1. Run `gc-validate` and capture the conformance report: `gc-report --output report.json`
2. Open a PR against `governancecommons/governance-commons` adding your row to `ADOPTERS.md`
3. Attach or link your conformance report in the PR description
4. For `strict` profile: attach the signed `gc-compliance-evidence` bundle

Conformance declarations are self-certified. The GC maintainer reviews for completeness,
not for re-validation of your results.
