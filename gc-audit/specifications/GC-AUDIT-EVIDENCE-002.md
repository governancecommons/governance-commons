# GC-AUDIT-EVIDENCE-002 — Protected local host pilot

Status: proposed owner-review implementation. No production authority or control PASS.

## Host contract

The [threat model](GC-AUDIT-EVIDENCE-002-THREAT-MODEL.md) identifies the host,
collector and target identities and their writable resources before implementation.
`tools/local_evidence_host.py` is a loading and filesystem adapter around the
existing `HostEvidenceVerifier`; it does not verify signatures a second way.
The deployment supplies an absolute host directory and a separate SHA-256 pin
of `config.json`. The untrusted evidence package may contain only a version
marker and envelopes. Fixed host filenames are `config.json`, `authority.json`
and `replay.sqlite`. No package field can select a root or policy.

`config.json` has the versioned `gc-audit.local-host-config.v1` schema. It pins
the expected target path, exact Git HEAD, environment, control IDs, catalog,
signed policy digest, public root keys and root/policy/producer revocations.
The signed policy delegates producers and approved collection methods/scopes.
The host checks its principal, path identity, owner and permissions, denies
links/reparse points, multiply linked host files and host/target overlap, checks the target Git HEAD and
clean worktree, verifies SQLite integrity, then calls the existing verifier.
Target Git inspection disables repository-configured fsmonitor commands and
optional locks, and ignores system/global Git configuration.
Any loading or filesystem failure returns `REJECTED` with a digest-checked
`gc-audit.local-host-receipt.v1` receipt. The receipt exports digests and
provenance, not private keys. It always retains `CONFIGURED_ROOT_ONLY` and
`UNVERIFIED` control status.

On POSIX, host files must be owned by the current UID and have no group/other
access; the host directory must also be private. On Windows, `pwsh` reads the
actual owner SID and DACL. The host directory must have inheritance disabled;
allow ACEs may name only the current SID, SYSTEM or Administrators. The demo
config and ledger are disposable and created outside `C:\dev`. An actual
deployment must provision its pin independently of the target and protect the
host directory against the target's OS identity.

## Demonstration and inspection

The [machine report](../reports/evidence-002-local-host.json) records the host
principal, exact synthetic target revision, public root and policy, signed
envelope, configuration and five receipts. One fresh package authenticated;
replay in a new process, tampered observation, replaced configuration and
revoked policy were rejected. Its SHA-256 canonical report digest is recorded
in the report itself (`sha256:e6c7f61a2b609c1820639205cb8bab4e5b5f69c83a731a2021bcbb299f7eebef`).
The synthetic target was exactly `c6c9a2a2318473e7ad16684258beb36442637542`.
The temporary SQLite ledger persisted across separate
verification child processes and was then removed with the fixture.

With Python 3.11+, Git, `jsonschema[format]>=4.18,<5`,
`cryptography>=42,<47`, and `pwsh` on Windows, run from the repository root:

```text
python gc-audit/tools/verify_local_host_demo.py --verify gc-audit/reports/evidence-002-local-host.json
python gc-audit/tools/verify_local_host_demo.py --output <path-outside-repo>
python -m unittest discover -s gc-audit/tests/zta -p 'test_*.py' -q
```

`--verify` checks report and receipt digests, the signed authority and envelope
through the original verifier, the catalog pin and claimed result states. It
cannot replay the removed host filesystem, independently reproduce each negative
host-state mutation, or prove the ACL observed at run time. The digests are
unkeyed integrity metadata; they do not authenticate the report publisher.
`--output` provisions fresh synthetic keys, private host files and a Git target
in a disposable directory; new digests are expected. The source fixture is
test-only and its signing private keys are never exported.

## Results and limits

The local run uses the interactive Windows SID recorded in the report for the
host, collector fixture and target fixture. A private ACL under one SID does
not protect host resources from a target process running as that same SID.
The deployment pin is supplied by the demo harness and is not an independent
root of trust. Cross-platform CI checks file-mode and ACL behavior where the
runner permits it; these are compatibility tests, not deployment isolation.
Protected production provisioning and distinct enforced principals remain a
**BLOCKER** for an independent-host claim. Owner review and exact-head CI are
**REQUIRED**. Production deployment, control-PASS integration, Portal changes,
Cockpit/UI, AI integration and automated remediation are **DEFERRED**.

EVIDENCE-001 reported 193 Python ZTA test cases. The PR #15 exact-head hosted
evaluator logs also report 193 on each of the six OS/Python matrix jobs; the
six matrix jobs are not six distinct test suites. This pilot adds 13 test cases,
for 206 total. The local Windows suite ran 204 before the final hard-link and
target fsmonitor cases were added, with no skips or failures; both added cases
passed separately.
Hosted exact-head counts and any
platform skips are reported at PR closeout. PLAY timing fields
with null endpoints and zero durations in EVIDENCE-001 and this pilot are
schema placeholders for unmeasured work, never measured zero-duration claims.
The wrong-owner test is an injected owner result, because the disposable runner
does not change another account's ownership. The inaccessible-storage tests
cover missing and corrupt storage; they do not establish a distinct-principal
write-denial experiment.
