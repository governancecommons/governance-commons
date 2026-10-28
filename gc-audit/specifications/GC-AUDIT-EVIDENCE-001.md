# GC-AUDIT-EVIDENCE-001 — Configured-root evidence authentication pilot

Status: owner review candidate. No production host authority, ZTA control PASS, release or deployment.

## Scope and compatibility

The pilot adds one versioned signed host-policy contract, one signed producer-evidence envelope, one structured verification result, and a host-owned SQLite replay receipt ledger. It reuses the existing Ed25519 canonical JSON signature pattern and the existing ZTA catalog/evaluator digest semantics. It does not change the evaluator's `PASS` rules, Gate 1 repository CLI, Portal behavioral adapter, universal target direction, or historical PLAY/report records. Both prior machine reports are reopened in regression tests.

The verifier takes independently configured roots, revocations, clock, target context and replay storage through a host-created object. The library can authenticate against those inputs but cannot prove that the calling process itself obtained them from an independent, protected deployment source. Its verification result always says `host_authority: CONFIGURED_ROOT_ONLY` and `control_status: UNVERIFIED`. A caller who can replace the entire host object can create a different configured-root world; no independent-authority claim follows from that. Production host configuration, protected key lifecycle, runtime confinement and control-specific proof remain separate gates.

## Reproducible signed demonstration

The [demo package](../reports/evidence-001-demo-package.json) is signed by a synthetic host root and a separately delegated synthetic producer. Its [public root](../reports/evidence-001-demo-root.json) is kept outside the package; neither private key is stored. Fixed assessment time is `2026-10-28T12:00:00Z` and the synthetic target is `demo-app` at revision `dddddddddddddddddddddddddddddddddddddddd`, environment `synthetic-test`, control `ZTA-02.01`, method `AUTOMATED_TEST`, scope `local-fixture`. This is a cryptographic test fixture, not an actual Portal observation or independently governed root.

The [verification report](../reports/evidence-001-verification.json) records one `AUTHENTICATED` package and five `REJECTED` variants: replay, modified observation, wrong target, missing evidence, and substituted root. All six have `control_status: UNVERIFIED`. The root digest is `sha256:4eec57e607cc2ff0e722b7ddfa8db6ce879a5c5481e03d173b74bc646907bc0e`; package digest is `sha256:1b45232f8868a5cd8e71610f9a8b659020ed8c2c9e1c84bf4a71b18c21987537`; verification report digest is `sha256:c981bd00ce89f6b8ca4b7bfb41c1593b0dab3e97e46df3a01b6b71010fac84b9`.

With Python 3.11+ and `jsonschema[format]>=4.18,<5` and `cryptography>=42,<47` installed, run from the Governance Commons root:

```text
python gc-audit/tools/verify_evidence_demo.py --verify gc-audit/reports/evidence-001-verification.json
python -m unittest discover -s gc-audit/tests/zta -p 'test_*.py' -q
```

The adversarial suite also covers unknown and substituted producer keys, changed signatures, wrong revision/environment, expired and revoked host/producer authority, unapproved control/objective/method/scope, duplicate evidence IDs/nonces, missing required scope evidence, caller-embedded trust-root substitution, and a signed local `PASS` claim that remains `UNVERIFIED`. The demo ledger is disposable for reproducibility; a deployed host must use durable, access-controlled replay storage outside the target.

## OBDD classification

**BLOCKER:** protected host configuration and deployment evidence for any independent authority or operational security claim. **REQUIRED:** exact-head Windows/Linux/macOS CI, owner review of the PR, and AL:2 acceptance of the proposed planning note. **DEFERRED:** evaluator control-PASS integration, production key management, deployment, GUI, AI, Cockpit and automated remediation. A signed observation only authenticates its configured producer; it does not establish observation truth, full ZTA coverage, release eligibility or certification.
