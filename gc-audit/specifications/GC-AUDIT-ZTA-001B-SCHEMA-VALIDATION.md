# GC-AUDIT-ZTA-001B — Schema validation and implementation contract

**Status:** SCHEMAS COMMITTED; evaluator and CI validation NOT IMPLEMENTED.  
**Authority:** GC-AUDIT-ZTA-001-V1-ACCEPTANCE-CONTRACT.md.  
**Schema dialect:** JSON Schema Draft 2020-12.

## Files
- `gc-audit/schemas/zta/gc-audit.zta-controls.v1.schema.json`
- `gc-audit/schemas/zta/gc-audit.zta-profile.v1.schema.json`
- `gc-audit/schemas/zta/gc-audit.zta-target.v1.schema.json`
- `gc-audit/schemas/zta/gc-audit.zta-evidence.v1.schema.json`
- `gc-audit/schemas/zta/gc-audit.zta-result.v1.schema.json`
- `gc-audit/schemas/zta/gc-audit.zta-risk-decision.v1.schema.json`

## Validation boundaries
Schemas verify record shape, required fields, enum values, basic formats and disallow unknown top-level fields other than namespaced `extensions`. Enforce `format` as an assertion in conforming validators. They deliberately **do not** claim to prove the following cross-record or semantic invariants:
- Exactly one instance of each 24 control ID, with no duplicate IDs in nested record arrays.
- Valid references between actor/component/resource/control IDs and known catalog/profile versions.
- Profile inheritance is acyclic, and conflicting overlays are rejected.
- Evidence source bytes match digest, producer is trusted, revision is correct, method proves claim, and freshness policy is satisfied.
- Result values are evidence-supported; evaluator owns PASS/FAIL/UNVERIFIED/NOT_APPLICABLE, stable sorting and canonical SHA-256.
- Risk authority, scope, expiry and release policy are independently enforced.
- Historical append-only invariants per GC-AUDIT-AMD-001.
- A schema-valid record is **not** a passing security assessment.

## Required CI fixtures before 001B acceptance
1. A valid instance for each of six schemas.
2. Negative instances missing a required field, with unknown field, invalid major version, invalid control ID, invalid status/severity, malformed SHA-256 and invalid timestamp.
3. Semantic negative fixtures for duplicate control IDs, wrong-revision evidence, cyclic profile, missing trust references, invalid authority, invalid exclusion.
4. A validating Draft 2020-12 engine must run the above in CI and assert failure where expected. Format assertion must be explicitly enabled.
5. ZT1–ZT8 and existing registry/script behavior must remain unchanged.

**Important:** Committing the schemas does not satisfy CI fixture execution or independent verification. No executable ZTA operation is registered by this change.
