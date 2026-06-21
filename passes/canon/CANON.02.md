PASS CANON.02 — Registry Governance

[NP-METADATA]
- PASS ID: CANON.02
- Canonical ID: PENDING — assigned by CANON.03 (Migration Protocol)
- Name: Registry Governance — Normative Specification
- Domain: governance.pass.identity
- Role: CREATE
- Predecessor: CANON.01
- Actor: Jess Ervin (GC founder) + Claude (claude-sonnet-4-6)
- Date: 2026-06-20
- time.loc: 2026-06-20T00:00:00Z
- Authority: AL:2 — GC maintainer decision
- Status: ACCEPTED

[PREDECESSOR IMPORT]
This PASS operates under all invariants declared in CANON.00 (CANON-CI-1 through CANON-CI-8)
and all normative rules declared in CANON.01 (R-ID-1 through R-IM-7).
No CANON invariant or normative rule is waived or modified by this PASS.

[INTENT]
Specify the normative registry governance standard. This PASS governs what the registry
is, what it contains, how it is written, how it is validated, and how it is protected as
governed infrastructure.

This PASS:
- Specifies the registry file format, root structure, and metadata
- Specifies the full entry schema — all required and optional fields, types, and constraints
- Specifies all valid status values with their semantics and transition rules
- Specifies the extension model for namespace-specific fields
- Specifies the write authority declaration format and enforcement rules
- Specifies the schema validation contract: what is validated, error types, failure handling
- Specifies the append-only changelog: requirement, format, and what constitutes an append
- Specifies the CI integration contract: what CI must check and how to report violations
- Specifies dependency validation: depends_on resolution, cross-namespace, superseded handling
- Declares the registry as a governed artifact with provenance chain requirements
- Publishes the normative JSON Schema for registry entries as a companion artifact

This PASS does not:
- Assign canonical IDs to existing PASSes (CANON.03)
- Modify the canonical ID grammar (CANON.01)
- Modify alias model rules (CANON.01)
- Govern PASS content (ACES, OG, domain clusters)

[BOUNDARIES]
INCLUDES:
- Registry file format: root structure, metadata block, entries array
- Entry schema: field-by-field specification with types, constraints, and validation rules
- Status value taxonomy: all valid statuses with semantics and valid transitions
- Extension model: namespace-prefixed extension fields, validation responsibility
- Write authority: declaration format, enforcement, agent restrictions
- Schema validation contract: pre-write checks, error taxonomy, failure handling
- Append-only changelog: requirement, entry format, immutability rules
- CI integration contract: required checks, violation format, pass/fail criteria
- Dependency validation: same-namespace and cross-namespace depends_on resolution
- Registry-as-governed-artifact: provenance chain requirements, traceability
- Companion artifact: schemas/canon-registry-entry.schema.json (JSON Schema draft/2020-12)

EXCLUDES:
- Canonical ID grammar (CANON.01 R-ID-1 through R-ID-7)
- Alias model and resolution protocol (CANON.01 R-AL-1 through R-AL-6)
- Allocation authority model (CANON.01 R-AA-1 through R-AA-7)
- Retroactive ID assignment for existing PASSes (CANON.03)
- ECO: or GC: specific registry content (each namespace's own registry file)
- PASS content governance

DEPENDS ON:
- CANON.01 (normative ID grammar, alias model, allocation authority, field names)
- CANON.00 (invariants — especially CANON-CI-4, CANON-CI-5, CANON-CI-7, CANON-CI-8)
- governance-commons/schemas/ (existing schema format conventions)
- governance-commons/governance/agent-constraints.yaml (GC-CONSTRAINT-001 write authority pattern)

MUST NOT TOUCH:
- CANON.00 and CANON.01 (sealed upon acceptance)
- ONS.00 and ONS.01
- governance-commons/governance/agent-constraints.yaml (not in CANON scope to modify)
- Any existing PASS content

---

[REGISTRY FILE SPECIFICATION]

Format

A CANON-conformant registry MUST be a valid JSON file. YAML is permitted as an
alternative human-readable format provided the adopter maintains a JSON canonical
form that is the authoritative source for tooling and CI. When JSON and YAML copies
diverge, the JSON form governs.

  R-RF-1  A registry file MUST be named using the pattern passes.registry.json
          (for JSON) or passes.registry.yaml (for YAML canonical form).

  R-RF-2  A registry file MUST be committed to the adopter's version-controlled
          governance repository. It MUST NOT be generated at runtime only.

  R-RF-3  A registry file MUST contain exactly one namespace's records.
          An organization with multiple namespaces MUST maintain separate registry
          files per namespace.

Root structure

A conformant registry file MUST have the following root structure:

  {
    "$canon_version": "<string>",
    "namespace":      "<NAMESPACE prefix>",
    "meta":           { <metadata block> },
    "entries":        [ <entry objects> ]
  }

$canon_version (required, string)
  The version of the CANON standard this registry conforms to.
  For registries conforming to this PASS: "$canon_version": "CANON.02"

namespace (required, string)
  The namespace prefix this registry governs. MUST match the prefix declared in
  namespace.yaml and MUST conform to CANON.01 R-ID-2 (^[A-Z]{2,6}$).

meta (required, object)
  Registry-level metadata. Required fields:

    created_at (string, ISO 8601)
      When this registry file was first created.

    updated_at (string, ISO 8601)
      When the registry was last modified. MUST be updated on every write.

    allocation_authority (string)
      The declared allocation authority for this namespace. MUST match the value
      declared in namespace.yaml. This field is informational — the namespace.yaml
      is the authoritative source.

    namespace_file (string)
      Relative path to the namespace declaration file (namespace.yaml).

    layers_file (string)
      Relative path to the layers declaration file (layers.yaml).

    changelog_file (string)
      Relative path to the append-only registry changelog.

    canon_version (string)
      Duplicate of $canon_version for tooling that reads meta separately.

entries (required, array)
  Array of entry objects. MAY be empty on initial creation. Each object MUST
  conform to the entry schema declared in [ENTRY SCHEMA].

  R-RF-4  The entries array MUST be the sole authoritative source of record for
          canonical ID assignments in this namespace. No separate list, index, or
          document supersedes the registry entries array.

---

[ENTRY SCHEMA]

Each entry in the entries array is an object representing one canonical ID assignment
or reservation. Required and optional fields are declared below.

Required fields (MUST be present in every entry)

  id (string)
    The canonical ID. MUST conform to CANON.01 R-ID-1: ^[A-Z]{2,6}:[0-9]{4}$
    MUST match the namespace declared in the registry root.
    MUST be unique within the registry (no two entries may share the same id).

  alias (string | null)
    The primary human-readable name for this PASS. Typically the named cluster
    identifier (e.g., "ACES.01", "OG.02"). MUST be unique within the namespace
    (no two entries may share the same alias), except when alias is null.
    null is permitted only for reserved entries that have not yet been named.

  legacy_ids (array of strings)
    Prior identifiers from systems predating CANON adoption. Empty array ([]) when
    there are no legacy IDs. MUST NOT be null. Once a value is added, it MUST NOT
    be removed (CANON.01 R-AL-5).

  title (string)
    Human-readable name for this PASS. Non-empty string. Not required to be unique.

  layer (string)
    The layer name from the namespace's layers declaration file.
    MUST match a declared layer name in the layers file.
    For reserved entries where the layer is not yet determined: "unassigned".

  cluster (string | null)
    The named cluster this PASS belongs to (e.g., "ACES", "OG", "CANON").
    MUST match the NAMESPACE-part of the alias if alias is a cluster identifier
    (CANON.01 R-SP-4). null is permitted for PASSes that do not belong to a cluster.

  parent (string | null)
    Canonical ID of the parent PASS (cluster header). MUST conform to R-ID-1 if
    non-null. MUST reference an entry in this registry or a cross-namespace entry
    resolvable via depends_on validation. null for root PASSes.

  status (string)
    One of the valid status values declared in [STATUS VALUES].
    MUST be present. MUST be a valid status string.

  timestamp (string, ISO 8601)
    The ISO 8601 datetime when the PASS was accepted or when this entry was created
    (for reserved entries). MUST include timezone offset or Z.

  path (string | null)
    Relative path to the PASS document from the repository root.
    null is permitted only for reserved entries where no document exists yet.
    Once a document exists, path MUST be set and MUST reference an existing file.

  supersedes (array of canonical ID strings)
    Canonical IDs this PASS supersedes. Empty array ([]) when none. Each entry
    MUST conform to R-ID-1. Cross-namespace supersession is permitted.

  superseded_by (string | null)
    Canonical ID of the PASS that supersedes this one. null when not superseded.
    When set: MUST conform to R-ID-1. This entry's status MUST be "superseded".

  depends_on (array of canonical ID strings)
    Canonical IDs this PASS depends on. Empty array ([]) when none. Each entry
    MUST conform to R-ID-1. Cross-namespace dependencies are permitted.
    See [DEPENDENCY VALIDATION] for resolution rules.

  originating_pass (string)
    The canonical ID or named form of the PASS that authorized this entry's
    creation. MUST be non-empty. For entries created during the bootstrap period
    (before CANON.03 assigns canonical IDs to CANON cluster PASSes), the named
    form (e.g., "CANON.03") is accepted. After the bootstrap period, this field
    MUST be a canonical ID conforming to R-ID-1.

Optional standard fields (SHOULD be present when applicable)

  description (string)
    One or two sentences describing what this PASS governs. Recommended for all
    entries. Required for cluster header entries (alias ending in ".00").

  reserved_for (string)
    Description of the intended future use. MUST be present when status is
    "reserved". Not present when status is anything else.

  reserved_by (string)
    Named form or canonical ID of the PASS that declared this reservation.
    MUST be present when status is "reserved".

  range (string)
    When a reservation covers a range of IDs, declares the range: "NNNN-NNNN".
    Present only in reserved entries. Applies to the id value and contiguous IDs
    up to the range end.

  sealed_at (string, ISO 8601)
    Datetime when this PASS was sealed. Present only when status is "sealed".

  superseded_at (string, ISO 8601)
    Datetime when this PASS was superseded. Present only when status is "superseded".

---

[STATUS VALUES]

Every entry MUST declare one of the following status values. Status values are
case-sensitive lowercase strings.

  "proposed"
    The ID has been discussed but not yet formally assigned. A proposed entry is
    a placeholder; no PASS document is required. The canonical ID is not yet
    binding — it may be changed before assignment is confirmed.
    Valid next statuses: draft, accepted, reserved (if repurposed as a reservation)

  "draft"
    The ID is assigned and a PASS document exists but the PASS has not yet been
    accepted. The assignment is binding (ID is immutable, CANON-CI-1), but the
    PASS content may still change before acceptance.
    Valid next statuses: accepted, superseded (if abandoned)

  "accepted"
    The PASS is accepted. Its governance decisions are in effect. The ID and the
    PASS content are both binding. This is the standard operating status for most PASSes.
    Valid next statuses: sealed, superseded

  "sealed"
    The PASS content is immutable. A PASS is sealed when its content is finalized and
    no further amendments to the document itself are permitted. Amendments to the
    governance it establishes require a new PASS that supersedes this one.
    Valid next statuses: superseded (only)

  "superseded"
    This PASS has been replaced by a newer PASS. The superseded_by field MUST be set.
    The entry remains in the registry permanently (CANON.01 R-IM-6).
    Valid next statuses: none (superseded is terminal)

  "reserved"
    The ID is reserved for future use. No PASS has been assigned. The entry MUST
    include reserved_for and reserved_by fields.
    Valid next statuses: draft, accepted (when the ID is used), proposed

Transition rules

  R-SV-1  Status transitions MUST follow the valid next statuses declared above.
          A registry write that attempts an invalid transition (e.g., sealed → accepted,
          superseded → accepted) MUST be rejected by schema validation.

  R-SV-2  A "superseded" status is terminal. Once an entry is superseded, its status
          MUST NOT change.

  R-SV-3  Only entries with status "superseded" may have a non-null superseded_by field.
          An entry that sets superseded_by MUST also set status to "superseded".

  R-SV-4  An entry with status "reserved" MUST have null for alias (or a placeholder),
          null for path, and null for parent unless the reservation target is known.

---

[EXTENSION MODEL]

An adopter MAY add namespace-specific fields to registry entries beyond the required
and optional standard fields declared above. Extension fields are governed by the
adopter's own governance system, not by CANON.

Naming convention

  R-EX-1  Extension fields MUST be prefixed with the lowercase namespace and a colon:
          <lowercase-namespace>:<field-name>
          Examples: eco:energy_tier, acme:cost_center, cityx:review_board

  R-EX-2  Extension field names MUST NOT start with a reserved prefix.
          Reserved prefixes: canon:, gc:, ons: (these are CANON and GC standard
          namespaces; fields using these prefixes as extensions may conflict with
          future standard fields).

  R-EX-3  Extension fields MUST NOT duplicate or shadow a required or optional standard
          field name declared in this PASS. A field named eco:id or eco:status would
          shadow required fields and MUST NOT be used.

Validation responsibility

  R-EX-4  CANON schema validation validates only required and optional standard fields.
          Extension field validation is the adopter's responsibility.
          An entry that fails extension field validation but passes CANON standard field
          validation is a CANON-conformant entry with an adopter-level validation failure.

  R-EX-5  The companion JSON Schema (schemas/canon-registry-entry.schema.json) uses
          additionalProperties: true to permit extension fields. Adopters MAY layer
          their own schema atop the CANON schema to validate extension fields.

---

[WRITE AUTHORITY]

Write authority for a registry is declared in the namespace's namespace.yaml
(allocation_authority field, per CANON.01). This section specifies how that
authority is enforced operationally.

  R-WA-1  Only the declared allocation authority MAY write new entries to the registry.
          An entry written without the declared allocation authority is unauthorized
          and MUST be treated as ungoverned until ratified by a PASS decision.

  R-WA-2  Agents MUST NOT write new registry entries without an authorizing PASS decision.
          This extends GC-CONSTRAINT-001 (agent-constraints.yaml AC-001) to registry writes:
          proposing a registry entry (status: proposed) is permitted without a PASS; writing
          a binding entry (status: draft, accepted, sealed, or reserved) requires a PASS.

  R-WA-3  Status updates to existing entries (e.g., accepted → sealed, accepted → superseded)
          are also writes requiring PASS authorization.

  R-WA-4  Changelog entries (see [APPEND-ONLY CHANGELOG]) MUST be written atomically
          with the registry change they record. A registry write without a corresponding
          changelog entry is incomplete and MUST be flagged by CI (see R-CI-4).

Write authority declaration format

The allocation_authority field in namespace.yaml declares write authority. The format
is a free-form string identifying the person, role, or process that holds write authority.

  Example values:
    "jj-ervin (GC founder)"
    "ECO project maintainer — jj-ervin"
    "eco-ci-bot (authorized by ECO:NNNN)"

For automated write authority (e.g., a CI process that writes migration entries):

  R-WA-5  An automated write authority MUST be authorized by a PASS that explicitly
          grants that automation the right to write. The authorizing PASS ID MUST be
          referenced in the namespace.yaml automation_authorized_by field.

---

[SCHEMA VALIDATION CONTRACT]

Every write to the registry MUST pass validation before it is committed. Validation
is pre-write: a write that fails validation MUST NOT be committed to the registry.

Validation scope

  Pre-write validation checks all of the following on the proposed entry:

  1. Schema conformance — all required fields present, all fields correctly typed,
     status is a valid value, id conforms to R-ID-1, alias unique within namespace,
     legacy_ids is an array, depends_on entries conform to R-ID-1

  2. ID uniqueness — no existing entry in the registry has the same id value

  3. Alias uniqueness — no existing entry in the registry has the same alias value
     (excluding null aliases)

  4. Namespace consistency — the id's namespace prefix matches the registry's
     declared namespace

  5. Layer consistency — the layer value exists in the namespace's layers file

  6. Status transition — if updating an existing entry, the transition is valid
     per R-SV-1 through R-SV-4

  7. Superseded_by consistency — if superseded_by is set, the referenced id exists
     in the registry and the entry's status is "superseded"

  8. Supersedes consistency — if supersedes is non-empty, each referenced id exists
     in the registry (or is a known cross-namespace ID) and that entry's superseded_by
     references this entry's id

  9. Depends_on validation — all depends_on entries resolve (see [DEPENDENCY VALIDATION])

  10. Originating PASS — originating_pass is non-empty and references a valid PASS
      (a PASS that exists in this registry or is a known canonical form)

  11. Path exists — if path is non-null and status is accepted or higher, the file
      at the declared path exists in the repository

Error taxonomy

  CRITICAL — the entry MUST NOT be written; validation fails entirely
    - id does not conform to R-ID-1
    - id is already in use by a different entry (duplicate)
    - Required field absent or null (when null is not permitted)
    - Status is not a valid value
    - Status transition is invalid

  ERROR — the entry MUST NOT be written; may be resolved without escalation
    - alias conflicts with an existing alias in the namespace
    - namespace mismatch (id prefix does not match declared namespace)
    - layer value does not exist in the layers file
    - superseded_by set but status is not "superseded"
    - superseded_by references a non-existent id
    - depends_on entry fails resolution (see R-DV-3)
    - path declared but file does not exist (for accepted+ status entries)

  WARN — entry may be written; warning is logged in the changelog
    - depends_on references a superseded ID (R-DV-4)
    - originating_pass is in named form rather than canonical ID
      (permitted during bootstrap; warned after bootstrap period)
    - alias is null for a non-reserved entry
    - description absent for a cluster header entry

  R-SVC-1  Validation MUST be performed before any write to the registry.
           Validation tools MUST implement all CRITICAL and ERROR checks.
           WARN checks are RECOMMENDED for all implementations.

  R-SVC-2  A validation tool that does not implement a required check MUST
           declare which checks it omits. Partial validation is permitted only
           when declared; undeclared partial validation is not CANON-conformant.

---

[APPEND-ONLY CHANGELOG]

Every write to the registry MUST produce a corresponding changelog entry. The changelog
is a governed record of every state change to the registry.

  R-CL-1  The changelog MUST be a separate file from the registry.
          RECOMMENDED filename: passes.registry.changelog.jsonl
          (newline-delimited JSON, one entry per line)

  R-CL-2  The changelog is append-only. Past entries MUST NOT be modified or deleted.
          A changelog that has been edited is no longer CANON-conformant.

  R-CL-3  Every registry write MUST produce at least one changelog entry.
          The changelog entry MUST be written in the same commit as the registry write.
          A registry write without a corresponding changelog entry is incomplete (R-WA-4).

Changelog entry format

Each changelog entry is a JSON object on a single line:

  {
    "timestamp":        "<ISO 8601>",
    "action":           "<action value>",
    "id":               "<canonical ID affected>",
    "changed_fields":   ["<field names>"],
    "previous_status":  "<prior status or null>",
    "new_status":       "<new status>",
    "authorizing_pass": "<canonical ID or named form of authorizing PASS>",
    "author":           "<identity string>",
    "note":             "<optional free-form note>"
  }

Valid action values:
  create      — a new entry was added to the registry
  update      — one or more fields of an existing entry were changed
  reserve     — a reserved entry was added
  supersede   — an existing entry's status was changed to superseded
  ratify      — a previously unauthorized entry was ratified by a PASS decision

  R-CL-4  The changed_fields array MUST list every field that changed in this write.
          For create and reserve actions, changed_fields MUST be ["*"] or list all
          fields in the new entry.

  R-CL-5  authorizing_pass MUST reference the PASS that authorized this registry write.
          For writes during the bootstrap period, the named form is accepted.
          After the bootstrap period, this field MUST be a canonical ID.

---

[CI INTEGRATION CONTRACT]

CI MUST run registry validation on every commit or pull request that modifies any of:
  - The registry file (passes.registry.json or passes.registry.yaml)
  - The layers declaration file (layers.yaml)
  - The namespace declaration file (namespace.yaml)
  - The registry changelog file (passes.registry.changelog.jsonl)

Required CI checks

  R-CI-1  Schema validation
    Run the full entry schema validation (all CRITICAL and ERROR checks from
    [SCHEMA VALIDATION CONTRACT]) against every entry in the registry, not only
    new or modified entries. A change to the layers file may invalidate existing
    layer fields; schema validation re-checks all entries.

  R-CI-2  ID uniqueness across full registry
    Confirm no two entries share the same id value.

  R-CI-3  Alias uniqueness within namespace
    Confirm no two entries (excluding null aliases) share the same alias value.

  R-CI-4  Changelog completeness
    Confirm that every modified or added registry entry has a corresponding
    changelog entry in the same commit. Detect: registry write with no changelog
    entry; changelog entry referencing a non-existent id.

  R-CI-5  Depends-on resolution
    Run depends_on validation for all entries with non-empty depends_on arrays.
    For cross-namespace entries: fetch the external registry and validate resolution.
    For same-namespace entries: validate against the current registry file.
    Superseded dependency: emit WARN, not ERROR (per R-DV-4).

  R-CI-6  Status transition check
    For entries whose status changed since the previous commit, confirm the
    transition is valid (R-SV-1 through R-SV-4).

  R-CI-7  Path existence check
    For all entries with status accepted, sealed, or superseded and a non-null path:
    confirm the file exists at the declared path.

  R-CI-8  Append-only changelog enforcement
    Confirm no existing changelog entry has been modified or deleted. Compare the
    previous commit's changelog against the current changelog; new lines are
    permitted, existing lines MUST be identical.

  R-CI-9  Namespace consistency
    Confirm every entry's id prefix matches the namespace declared in the registry
    root meta block.

Violation reporting

  R-CI-10  CI MUST report violations with the following fields:
    - check_id: the rule ID (e.g., R-CI-4)
    - severity: CRITICAL, ERROR, or WARN
    - entry_id: the canonical ID of the affected entry (or "registry" for root-level)
    - message: human-readable description of the violation
    - field: the specific field that failed (when applicable)

  R-CI-11  CI MUST fail the build on any CRITICAL or ERROR violation.
           CI MUST emit warnings on WARN violations without failing the build.
           WARN violations SHOULD be resolved before the registry is considered stable.

---

[DEPENDENCY VALIDATION]

The depends_on field declares governance dependencies. A PASS that depends on another
PASS cannot be considered well-governed if its dependency is missing, unresolvable, or
has been superseded without acknowledgment.

Same-namespace resolution

  R-DV-1  A depends_on entry whose NAMESPACE matches the current registry's namespace
          MUST resolve to an entry in the current registry with status != superseded,
          unless the dependency is explicitly acknowledged as superseded (R-DV-5).

  R-DV-2  A depends_on entry that does not resolve within the current registry is an
          ERROR-level validation failure.

Cross-namespace resolution

  R-DV-3  A depends_on entry whose NAMESPACE differs from the current registry's
          namespace MUST be resolved by fetching the external namespace's registry.
          The external registry MUST be declared accessible (via a URL or file path
          declared in namespace.yaml external_registries field).
          If the external registry is not accessible, the validation MAY degrade to
          a WARN (not ERROR) to avoid blocking builds due to network unavailability.

  R-DV-4  A depends_on entry that resolves to a superseded canonical ID in any
          namespace is a WARN-level violation, not an ERROR.
          The WARN message MUST include the superseded_by value so the maintainer
          can update the dependency. The adopter SHOULD update the dependency to
          the superseding ID.

  R-DV-5  An adopter MAY explicitly acknowledge a superseded dependency by adding the
          entry to a known_superseded_dependencies array in the registry meta block.
          A known superseded dependency produces no validation warning.
          The known_superseded_dependencies entry MUST include:
            - id: the superseded canonical ID
            - superseded_by: the superseding canonical ID
            - acknowledged_by: the canonical ID or named form of the PASS that
              acknowledged this dependency is intentionally retained

Circular dependency detection

  R-DV-6  A circular depends_on chain (A depends on B depends on A) is a CRITICAL
          validation failure. CI MUST detect cycles of any length.

---

[REGISTRY AS GOVERNED ARTIFACT]

The registry is not a convenience file. It is a governed artifact under CANON-CI-4.
This section declares what that means operationally.

Provenance chain

  R-GA-1  The registry file MUST be committed to version control. The version control
          history is the registry's provenance chain. Every change to the registry is
          traceable to a commit, a commit message, and an authorizing PASS.

  R-GA-2  Every registry write MUST be traceable to a PASS decision via the
          originating_pass field of the affected entry and the authorizing_pass field
          of the changelog entry. An entry with no traceable PASS is an ungoverned entry.

  R-GA-3  The registry schema file (schemas/canon-registry-entry.schema.json) is also
          a governed artifact. Changes to the schema file MUST be accompanied by a
          CANON amendment PASS. The schema version is declared in the schema's $id field.

Registry amendment path

  When the CANON standard changes in a way that requires new registry fields or new
  validation rules, a CANON amendment PASS is written. The amendment PASS:
  - Declares which fields are added, changed, or removed
  - Declares the new $canon_version string for the registry root
  - Declares a transition period during which both old and new versions are accepted
  - Updates schemas/canon-registry-entry.schema.json

  R-GA-4  A registry that declares "$canon_version": "CANON.02" MUST conform to this
          PASS. A registry declaring a future version MUST conform to that version's
          CANON amendment PASS. Version mismatch is a CRITICAL validation failure.

---

[COMPANION ARTIFACT: registry entry schema]

This PASS produces a JSON Schema file at:
  governance-commons/schemas/canon-registry-entry.schema.json

The schema validates individual entry objects. The root registry structure (meta block,
entries array) is validated by a separate root schema declared in the same file.

The schema is normative: it MUST be consistent with the field definitions in this PASS.
If the prose and the schema conflict, this PASS governs; the schema SHOULD be corrected.

Schema version identifier: CANON.02
Schema $id: https://governancecommons.org/schemas/canon-registry-entry/CANON.02.json

The companion schema file is written as a separate output of this PASS.
See schemas/canon-registry-entry.schema.json.

---

[NORMATIVE REQUIREMENTS SUMMARY]

  Rule      Level   Statement
  --------  ------  ---------------------------------------------------------------
  R-RF-1    MUST    Registry file named passes.registry.json or passes.registry.yaml
  R-RF-2    MUST    Registry committed to version-controlled repository
  R-RF-3    MUST    One registry file per namespace
  R-RF-4    MUST    entries array is the sole authoritative source for canonical IDs
  R-SV-1    MUST    Status transitions follow declared valid next statuses
  R-SV-2    MUST    "superseded" is terminal; status must not change after
  R-SV-3    MUST    superseded_by set only when status is "superseded"
  R-SV-4    MUST    Reserved entries have null alias, null path, null parent (unless known)
  R-EX-1    MUST    Extension fields prefixed with lowercase namespace and colon
  R-EX-2    MUST    Extension fields must not use reserved prefixes (canon:, gc:, ons:)
  R-EX-3    MUST    Extension fields must not shadow required/optional standard fields
  R-EX-4    —       CANON schema validates standard fields only; extensions are adopter's
  R-EX-5    —       Companion schema uses additionalProperties: true for extensions
  R-WA-1    MUST    Only declared allocation authority may write binding entries
  R-WA-2    MUST    Agents must not write binding entries without an authorizing PASS
  R-WA-3    MUST    Status updates require PASS authorization
  R-WA-4    MUST    Changelog entry written atomically with registry write
  R-WA-5    MUST    Automated write authority must be authorized by a PASS
  R-SVC-1   MUST    Validation performed before any write
  R-SVC-2   MUST    Partial validation implementations must declare which checks are omitted
  R-CL-1    MUST    Changelog is a separate file (RECOMMENDED: .jsonl format)
  R-CL-2    MUST    Changelog is append-only; past entries must not be modified or deleted
  R-CL-3    MUST    Every registry write produces at least one changelog entry
  R-CL-4    MUST    changed_fields lists every changed field
  R-CL-5    MUST    authorizing_pass references authorizing PASS
  R-CI-1    MUST    CI runs full schema validation on every registry-touching commit
  R-CI-2    MUST    CI checks ID uniqueness across full registry
  R-CI-3    MUST    CI checks alias uniqueness within namespace
  R-CI-4    MUST    CI checks changelog completeness
  R-CI-5    MUST    CI runs depends_on validation for all entries
  R-CI-6    MUST    CI checks status transition validity
  R-CI-7    MUST    CI checks path existence for accepted+ entries
  R-CI-8    MUST    CI enforces changelog append-only (no edits to past entries)
  R-CI-9    MUST    CI checks namespace consistency across all entries
  R-CI-10   MUST    CI reports violations with check_id, severity, entry_id, message, field
  R-CI-11   MUST    CI fails build on CRITICAL or ERROR; warns on WARN
  R-DV-1    MUST    Same-namespace depends_on resolves to non-superseded entry
  R-DV-2    MUST    Unresolvable depends_on is an ERROR
  R-DV-3    MUST    Cross-namespace depends_on resolved via external registry
  R-DV-4    WARN    Superseded dependency is a WARN, not ERROR
  R-DV-5    —       Adopter may acknowledge superseded dependency to suppress WARN
  R-DV-6    MUST    Circular depends_on chain is a CRITICAL failure
  R-GA-1    MUST    Registry committed to version control
  R-GA-2    MUST    Every registry write traceable to a PASS via originating_pass
  R-GA-3    MUST    Schema file changes require a CANON amendment PASS
  R-GA-4    MUST    Registry $canon_version must match declared PASS; mismatch is CRITICAL

---

[REASONING — 5 QUESTIONS]

1. Why is the registry append-only with a separate changelog rather than relying on
   git history alone?
   Git history is an implementation detail of one storage model. The CANON standard is
   storage-agnostic: a future adopter may use a database, an immutable ledger, or a
   distributed registry that does not use git. The append-only changelog is a
   storage-independent audit trail that any implementation must maintain. Git history
   is sufficient evidence for the git case; the changelog requirement ensures that
   non-git implementations also produce an auditable record.

2. Why are WARN violations not build-blocking?
   A superseded dependency (R-DV-4) is the canonical example of a WARN: the governance
   is slightly stale but the dependent PASS is still valid and well-understood. Blocking
   builds on WARNs would prevent adopters from merging work while a dependency migration
   is in progress. The WARN is the signal that cleanup is needed; the ERROR is reserved
   for states that represent actual governance gaps (unresolvable depends_on, invalid
   transitions) rather than known-stale states.

3. Why does the extension model use lowercase namespace prefixes rather than uppercase?
   Extension fields are not canonical IDs (which use uppercase NAMESPACE). Using lowercase
   for extensions creates a visual distinction: eco:energy_tier is clearly an extension
   field; ECO:0001 is clearly a canonical ID. The contrast prevents agents and tools from
   confusing field naming conventions with ID conventions.

4. Why require CI checks on layers and namespace files, not only registry files?
   A change to layers.yaml can invalidate existing registry entries (R-LY-4): if a layer
   range is narrowed or removed, all entries in that range suddenly have invalid layer
   fields. A change to namespace.yaml can change the declared allocation authority —
   meaning all future writes may be unauthorized under the old authority. These files are
   interdependent with the registry; CI must treat them as a coherent system.

5. Why is path existence checked only for accepted+ status, not for draft?
   A draft entry (status: draft) means the PASS document may still be in flight —
   being edited in a separate branch, not yet committed, or awaiting review. Requiring
   path existence for draft entries would block the allocation of an ID before the
   document is ready, defeating the purpose of the draft status. Once a PASS reaches
   accepted, the document MUST exist because the governance decisions in it are in effect.

---

[OUTPUTS]
- PASS CANON.02 accepted as the normative Registry Governance specification
- Registry file specification declared: format, root structure, metadata block (R-RF-1–4)
- Entry schema declared: all required and optional standard fields with types and constraints
- Status value taxonomy declared: 5 statuses with semantics and transition rules (R-SV-1–4)
- Extension model declared: naming convention, validation responsibility (R-EX-1–5)
- Write authority specification declared: enforcement, agent restrictions (R-WA-1–5)
- Schema validation contract declared: 11 pre-write checks, error taxonomy (R-SVC-1–2)
- Append-only changelog declared: requirement, format, action values (R-CL-1–5)
- CI integration contract declared: 9 required checks, violation reporting (R-CI-1–11)
- Dependency validation declared: same-namespace, cross-namespace, circular (R-DV-1–6)
- Registry-as-governed-artifact declared: provenance chain requirements (R-GA-1–4)
- Companion artifact: schemas/canon-registry-entry.schema.json (written separately)
- 44 normative rules across 9 rule families

[DELTA SUMMARY]
- Registry file format: JSON required; YAML permitted as human-readable alternate; filename
  pattern passes.registry.json; one file per namespace; entries array is sole authority
- Entry schema: 14 required fields (id, alias, legacy_ids, title, layer, cluster, parent,
  status, timestamp, path, supersedes, superseded_by, depends_on, originating_pass);
  6 optional standard fields (description, reserved_for, reserved_by, range, sealed_at,
  superseded_at); extension field model via namespace-prefixed lowercase keys
- Status taxonomy: proposed, draft, accepted, sealed, superseded, reserved; 4 transition
  rules; superseded is terminal; superseded_by requires status == superseded
- Write authority: allocation_authority from namespace.yaml; agents require authorizing PASS
  for binding writes; changelog written atomically with registry write; automation authorized
  by PASS; extends GC-CONSTRAINT-001 pattern to registry writes
- Schema validation: 11 pre-write checks; CRITICAL (id format, duplicates, missing required,
  invalid status/transition), ERROR (alias conflict, namespace mismatch, bad layer, path
  missing, bad superseded_by, bad depends_on), WARN (superseded dependency, named bootstrap
  originating_pass, null alias on non-reserved, missing cluster-header description)
- Append-only changelog: .jsonl format; 5 required fields per entry; 5 valid action values
  (create, update, reserve, supersede, ratify); append-only enforced by CI (R-CI-8)
- CI integration: 9 required checks (schema, ID uniqueness, alias uniqueness, changelog
  completeness, depends_on, status transition, path existence, append-only, namespace
  consistency); violation reporting format (check_id, severity, entry_id, message, field);
  build fails on CRITICAL/ERROR; warns on WARN
- Dependency validation: same-namespace MUST resolve to non-superseded; cross-namespace via
  external_registries in namespace.yaml (network failure degrades to WARN); superseded
  dependency is WARN; acknowledged superseded dependencies suppress WARN; circular deps
  are CRITICAL
- Registry-as-governed-artifact: version control is provenance chain; every write traceable
  to PASS; schema file changes require CANON amendment; $canon_version mismatch is CRITICAL

[CONSTRAINT VALIDATION]
- CANON-CI-4 (registry as governed artifact): R-WA-1 through R-WA-5 enforce write authority;
  R-GA-1 through R-GA-4 enforce provenance and traceability; R-CL-2 enforces append-only
- CANON-CI-7 (legacy IDs preserved): entry schema requires legacy_ids array (never null);
  R-SVC CHECK 1 validates it; removal of a legacy_id value is prevented by R-CL-2
  (changelog is append-only; a write removing a legacy_id would produce a violating
  update entry that CI must reject via R-CI-4)
- CANON-CI-8 (migration is governed): R-WA-2 (agents require PASS for binding writes);
  R-GA-2 (every write traces to PASS via originating_pass) together enforce this
- CANON-CI-1 (immutable IDs): R-SV-2 (superseded is terminal); R-SVC ERROR check for
  duplicate IDs; R-CI-2 (ID uniqueness) — together prevent ID reassignment
- CANON-CI-3 (flat IDs): no hierarchical field in entry schema; parent field is a
  canonical ID reference (flat), not a path or dotted notation
- Does not assign canonical IDs: confirmed; all assignments deferred to CANON.03
- Does not redefine canonical ID grammar: confirmed; all id field validation references
  CANON.01 R-ID-1 pattern

[REVERSIBILITY]
Reversing CANON.02 requires a CANON amendment PASS that:
- explicitly supersedes this PASS
- documents which registry governance rules change and why
- declares a transition period and $canon_version migration path
- addresses whether existing registries conforming to CANON.02 remain valid or must migrate
- confirms the companion schema file (canon-registry-entry.schema.json) is updated
Until such a PASS exists, CANON.02 is the normative registry governance specification.

[HANDOFF]

next_action: Write companion artifact — schemas/canon-registry-entry.schema.json
  The JSON Schema file must implement CRITICAL and ERROR validation checks from this PASS.
  Schema $id: https://governancecommons.org/schemas/canon-registry-entry/CANON.02.json
  Format: JSON Schema draft/2020-12 (consistent with existing GC schemas)
  additionalProperties: true (extension model per R-EX-4 and R-EX-5)

next_action_after_schema: Write CANON.03 — Migration Protocol (eco first-adopter)
  Must answer: what happens to legacy 000.xx–0167.xx IDs; which named PASS becomes first
  canonical ECO: ID; legacy_id population; conflict resolution; allocation authority for
  ECO:; formal reversal of the unauthorized named-cluster-only rule; ECO: layers.yaml;
  ECO: namespace.yaml; initial ECO: registry file.

required_inputs for CANON.03:
  - CANON.01 (ID grammar, namespace declaration, alias model, R-AA rules)
  - CANON.02 (entry schema, status values, write authority, originating_pass bootstrap rule)
  - eco/passes/PASS-INDEX.md (inventory of all named cluster PASSes to migrate)
  - eco/passes/ (individual PASS files for timestamp and dependency data)
  - eco passchangelog (legacy PASS history)
  - GC passchangelog (GC-PASS-0001 through GC-PASS-0008 for GC: namespace migration)

forbidden_scopes for CANON.03:
  - Do not modify canonical ID grammar
  - Do not modify registry schema beyond what is declared in CANON.02
  - Do not modify CANON.01 or CANON.02

[FINALIZATION]
PASS CANON.02 is ACCEPTED as the normative Registry Governance specification.
All CANON-conformant registries MUST conform to the rules declared in this PASS.
The companion schema artifact (schemas/canon-registry-entry.schema.json) is a required
output of this PASS and must be written before CANON.03 begins.
CANON.03 is the next required PASS after the companion schema is complete.
