# GC-AUDIT-EVIDENCE-002 — Local host threat model and authority contract

Status: proposed implementation boundary. This document precedes the host adapter.

## Identities and resources

The intended deployment has three roles. A **host** process runs as an OS principal
that owns a private configuration directory, signed policy, and SQLite replay
ledger. A **collector** produces signed observation envelopes under a key delegated
by the policy; it can read target state within the approved method and scope but
cannot change host configuration. The **target** process controls its own repository
and application data; every byte it supplies is untrusted input to the host.

The local demonstration runs host, collector fixture and target fixture as the
same interactive Windows principal (`ProX\\Jess`, SID
`S-1-5-21-3393606127-3043414772-645588242-1003`). It can validate ACL
shape and reject untrusted input, but that principal can also edit all three
roles' files. No OS process isolation or independent host authority is claimed.
On POSIX CI the runner account similarly plays every role. A deployment may
claim enforced separation only after distinct principal identities and actual
file permissions are independently checked.

| Resource | Intended writer | Other roles |
| --- | --- | --- |
| Host directory, public trust roots, expected target context and revocations | Host administrator | Collector/target cannot modify |
| Signed authority policy in host directory | Host administrator | Collector/target cannot replace |
| Persistent replay SQLite database | Host process | Collector/target cannot modify or reset |
| Evidence envelope and target repository | Collector/target | Host reads as untrusted input |
| Verification receipt | Host process | Exported for inspection; no private keys |

## Threats and checks

The adapter must reject broad or unknown file access, unexpected owner, missing
or corrupt files, links/reparse points, path overlap with the target, package
attempts to supply host roots or policy, stale or revoked authority, mismatched
target/revision/environment, tampering, and replay across restarts. Host input
paths are set by deployment, not read from evidence. The existing verifier owns
signature, scope, freshness, revocation and replay decisions; the adapter must
not create another cryptographic decision path or promote control PASS.

The local host directory is not a sandbox. A same-principal attacker can alter
configuration or race filesystem checks. The adapter therefore emits only
`CONFIGURED_ROOT_ONLY` and `UNVERIFIED` control status. An authenticated
signature proves the producer key used, not the truth or sufficiency of its
observation. Production principal separation, secure provisioning, independent
root provenance and control-specific evaluation are outside this pilot.
