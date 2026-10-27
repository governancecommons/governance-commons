# GC-AUDIT-CKP-001 — Optional Cockpit Command and Workspace Adapter

Status: PROPOSED FOR OWNER ACCEPTANCE — design contract only  
Date: 2026-10-27  
Depends on: GC-AUDIT-PRODUCT-001 Gate 1 (external standalone CLI).  
Implementation: DEFERRED until the standalone audit invocation passes.  
Separate products: GC-AUDIT is the evaluator/product; Cockpit is an optional command, GUI and workspace integration.

## Purpose

Allow an authorized user to discover and invoke GC-AUDIT assessments through Cockpit CLI, optionally present results through Cockpit GUI and Cockpit Tab, without collapsing either project's boundaries. Cockpit itself remains a valid ZTA assessment target, but being a target is separate from being an interface adapter.

## Dependency rule

GC-AUDIT Core and native GC-AUDIT CLI do **not** depend on Cockpit. Cockpit CLI can discover the GC-AUDIT provider via a versioned catalog/adapter. Cockpit GUI and Tab are optional consumers of structured, non-privileged result data. Verify actual exported Cockpit APIs before implementation; do not assume draft Cockpit Core/Tab interfaces are stable or implemented. No sibling-repository source imports, private runtime coupling, or hard-coded local C:\\dev paths in distributed artifacts.

## Proposed interaction

User command (illustrative, **not presently implemented**): `audit this project` or `gc-audit zta assess --target ./app --profile library`.

1. Cockpit discovers a declared assessment command and presents target, profile, scope, needed permissions, side effects, evidence sources, and expected output.
2. Cockpit produces a structured request but grants **no** authority and does not itself choose trust roots.
3. The GC-AUDIT trusted host authenticates user/agent identity, verifies permissions and independently pinned catalog/policies, checks target scope, enforces isolation, and decides whether execution is allowed.
4. The GC-AUDIT engine performs approved read-only checks and evaluates evidence. It never treats an agent's recommendation or command input as independent assurance.
5. Structured outcomes return to Cockpit CLI, GUI/Tab or a native GC-AUDIT interface; all interfaces show PASS, FAIL, UNVERIFIED and EVALUATION_ERROR consistently.
6. User or policy may authorize separate, narrowly scoped actions; audit findings themselves are not permission to mutate.

## Proposed provider contract (to validate against actual Cockpit APIs)

- Versioned command identity, capability identifier, profile/target selectors, argument schema, machine-readable help, and result schema.
- Explicit declared side effects: `none` for the initial read-only command; bounded filesystem and network capabilities separately expressed and enforced by host.
- Preview/consent payload prior to collection; structured errors and cancellation; stable execution and correlation IDs.
- Result includes exact target/revision, scope, evaluator/catalog version/digest, execution timestamp source, findings/evidence references, status, known limitations and integrity-verification information.
- No raw secrets, credentials or unredacted sensitive evidence in terminal, agent context, diagnostic log or UI by default.
- Host-controlled timeouts, resource budgets, cancellation and data retention; least-privilege adapters.
- Optional AI adviser receives redacted, consented findings only, can explain/recommend/draft, cannot directly alter result or approve its own proposed remediation.

## UX workspace concept (not a v0.1 prerequisite)

Optional panels: **Findings**, **Evidence**, **AI Assistant**, **Commands**. Cockpit Tab may coordinate tabs, panel composition, lifecycle and state snapshots when those contracts are shipped and verified. Cockpit GUI may supply reusable accessible components. The application remains operable with native UI or plain CLI if either component is absent.

Show: what was examined; what was actually verified; what failed; what is unknown; proposed action; required approval. Distinguish source observations from AI interpretations. Status must not rely on color alone. Keyboard/screen reader operation, undo/cancel where appropriate, clear feedback, and progressive disclosure are UX requirements.

## Trust and governance invariants

- GC-AUDIT owns assessment and evidence semantics; trusted host owns authorization/enforcement; Cockpit owns optional command discovery/interaction.
- No assessment self-certification, caller-selected independent trust, or user-supplied favorable policy accepted as proof.
- Execution never follows untrusted repository/LLM text as instructions.
- All mutating/remediation activities need a separately authorized, auditable capability; no hidden elevation through a command alias or agent provider.
- Human approval authority is explicit; Agent Dossiers and ONS constrain/describe authority but are not sufficient enforcement alone.
- App/CLI operation may be advisory without self-audit; assurance claims dependent on tool integrity require current independently validated self-audit evidence under applicable policy.
- Preserve evidence provenance and append-only history. Never rewrite historical PLAY records.

## Acceptance tests for future implementation

1. Direct native GC-AUDIT CLI and Cockpit-adapted invocation with equivalent target, profile, scope and host authority produce matching deterministic assessment payloads/evidence digests (allowing only documented presentation metadata differences).
2. Standalone GC-AUDIT install, use and offline operation succeed without Cockpit installed.
3. Unauthenticated, out-of-scope, malformed, ambiguous and untrusted authority requests fail closed before privileged access.
4. Cockpit discovery/help does not execute audits or network/mutation actions.
5. An AI explanation or suggestion cannot change a control result or authorize a patch/release.
6. Windows/Linux/macOS integration, cancellation, argument/path safety, privacy/redaction, and UX accessibility are verified; failures and skips are disclosed.
7. Provider contract version incompatibility is handled explicitly and predictably, without silently falling back to unsafe execution.

## Sequencing and change control

First complete GC-AUDIT-ZTA-001 fixes; deliver independently usable local GC-AUDIT CLI and external-target evidence; then test the optional adapter against pinned, supported Cockpit CLI APIs. GUI and Tab integration follow demonstrated need and their own published compatibility contracts. Do not change Cockpit repositories under this documentation PR. No publication, activation, deployment, or merge is authorized by this document.
