# Conformance Badge Criteria — Governance Commons

**time.loc:** 2026-06-08T00:00:00Z  
**Defined in:** PASS-5 (GC-5-H-02)

---

## Profiles

Governance Commons defines three conformance profiles. A project declares the highest
profile it satisfies across each spec it adopts.

| Profile | Requirements |
| --- | --- |
| **advisory** | Structure and naming follow GC conventions; no validator run required |
| **standard** | An available published validator for the named specification and version passes with zero required-rule failures |
| **strict** | An available published strict profile passes with zero failures and the required signed evidence bundle is produced and retained |

Profiles are scoped to a named specification and version. They are not umbrella-level
certification. If no published validator supports a target, evidence must be labeled manual or
provisional; a `standard` or `strict` badge is not available on automated grounds.

---

## Per-spec criteria

### ONS (Ontic Namespace Structure)

| Profile | Criteria |
| --- | --- |
| advisory | All identifiers follow ONS naming grammar; cluster prefix is registered or clearly scoped |
| standard | `gc-validate --spec ons` passes; `rules.json` export is present if distributing a validator |
| strict | standard + `rules.json` is versioned and referenced in conformance report |

### Agent Dossier

| Profile | Criteria |
| --- | --- |
| advisory | A `dossier.yaml` (or equivalent) file exists and follows dossier schema structure |
| standard | Python `governance-commons` 0.2.0 `gc-validate --spec dossier` passes for a supported Agent Dossier document; any additional PASS or handoff checks are documented separately |
| strict | standard + signed handoff envelopes (JWS/Ed25519); signed evidence bundle submitted |

### Agent Matrix

| Profile | Criteria |
| --- | --- |
| advisory | An `agent-matrix.yaml` (or equivalent) file exists; capability profiles are declared |
| standard | Not currently available through the published shared `gc-validate` tool; use the source validator for development checks and label any public declaration manual or provisional |
| strict | Not currently available |

### Agent Project Orchestrator (APO) reference-runtime candidate

| Profile | Criteria |
| --- | --- |
| advisory | Implementation relationship may be described, but APO is not a Governance Commons specification |
| standard | Not available |
| strict | Not available |

Agent Team Protocol is pre-release and outside GC v1.2.0. Public conformance badges are not
available for it yet.

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
| --- | --- | --- |
| advisory | blue | `blue` |
| standard | green | `green` |
| strict | bright green | `brightgreen` |

---

## Declaring conformance

To appear in [ADOPTERS.md](../../ADOPTERS.md):

1. Name the specification and version being claimed.
2. Run an available published validator and retain its ConformanceReport, or document manual
   checks and label the result manual/provisional.
3. Open a PR against `governancecommons/governance-commons` adding your row to `ADOPTERS.md`.
4. Attach or link the evidence in the PR description.
5. For an available `strict` profile, attach the required signed evidence bundle.

Conformance declarations are self-reported. The GC maintainer reviews submissions for
completeness, not as an independent certifier.
