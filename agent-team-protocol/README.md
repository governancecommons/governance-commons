# agent-team-protocol

**Status:** Planned — scaffold only

Fleet-level governance specification for multi-agent systems.

## Scope

This spec will own what `agent-matrix` explicitly does not: governance at the boundary between agents in a coordinated fleet.

| Concern | This spec |
|---------|-----------|
| Delegation | How one agent authorizes another to act on its behalf, with scope constraints |
| Trust topology | Trust chains between agents — which agent can authorize which |
| Shared audit trail | Fleet-level audit log across multiple agents working a shared task |
| Fleet escalation | Escalation paths that span agent boundaries |
| Team formation | How agent fleets are assembled for a task and dissolved on completion |

## Relationship to existing specs

- Consumes `agent-matrix` (routing, capability, identity) as a runtime primitive
- Consumes `agent-dossier` (per-agent contract) as a runtime primitive
- Does not replace either — extends them to the fleet level

## See also

- `governance-commons/agent-matrix/DEVPLAN.md` — Successor Spec section
- `governance-commons/agent-matrix/DEVPATH.md` — DDR-AM-4 (scope boundary decision)
- DCP Team Kit (`docs/team-kit/`) — the human-governance counterpart (process patterns for human teams running agent fleets)
