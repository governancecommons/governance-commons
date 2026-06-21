PASS CANON.01 — PASS Identifier Governance

[NP-METADATA]
- PASS ID: CANON.01
- Canonical ID: PENDING — assigned by CANON.03 (Migration Protocol)
- Name: PASS Identifier Governance — Normative Specification
- Domain: governance.pass.identity
- Role: CREATE
- Predecessor: CANON.00
- Actor: Jess Ervin (GC founder) + Claude (claude-sonnet-4-6)
- Date: 2026-06-20
- time.loc: 2026-06-20T00:00:00Z
- Authority: AL:2 — GC maintainer decision
- Status: ACCEPTED

[PREDECESSOR IMPORT]
This PASS operates under all invariants declared in CANON.00 (CANON-CI-1 through CANON-CI-8).
CANON.00 is the authoritative invariant source for the CANON cluster.
No CANON invariant is waived or modified by this PASS.

[INTENT]
Specify the normative rules for PASS identifier governance. This PASS is the external-facing
standard: an organization adopting CANON reads CANON.01 to know exactly what they must do.

This PASS:
- Declares the canonical ID format in full, with validity rules and RFC 2119 conformance language
- Specifies namespace declaration: what an adopter declares, what the declaration contains
- Specifies the layers declaration: format, required fields, coverage rules
- Specifies alias rules: what aliases are, where they live, how they are resolved
- Specifies the allocation authority model: who assigns IDs and how that authority is recorded
- Specifies the range reservation mechanism
- Specifies the sub-pass relationship model in the registry
- Specifies the immutability enforcement protocol including supersession
- Declares ONS conformance requirements for namespace prefixes

This PASS does not:
- Define the registry schema (CANON.02)
- Assign any canonical IDs to existing PASSes (CANON.03)
- Govern PASS content or governance rules
- Modify ONS naming grammar (ONS.00 and ONS.01 govern this)

[BOUNDARIES]
INCLUDES:
- Canonical ID grammar and validity rules
- Namespace declaration specification and format
- Layers declaration specification and format
- Alias model: types, uniqueness, resolution protocol
- Allocation authority model: declaration, traceability, constraints
- Range reservation: what it is, how it is recorded, how it is released
- Sub-pass relationship model: parent field, cluster field, grouping semantics
- Immutability specification: what is immutable, supersession protocol, post-supersession
- ONS conformance rule for namespace prefixes

EXCLUDES:
- Registry schema field definitions beyond what alias and legacy_ids contain (CANON.02)
- Registry write authority mechanics, CI integration, changelog requirements (CANON.02)
- Retroactive ID assignment for existing PASSes (CANON.03)
- ECO: or GC: specific layer band assignments (each namespace's layers declaration file)
- PASS content governance (ACES, OG, domain clusters)

DEPENDS ON:
- CANON.00 (cluster header — invariants, canonical ID format declaration, cluster structure)
- ONS.00 (Ontic Namespace Structure — naming grammar authority)
- ONS.01 (ONS Lint Rule Catalog — casing and pattern enforcement)

MUST NOT TOUCH:
- CANON.00 (cluster header — sealed upon acceptance)
- ONS.00 and ONS.01 (not in CANON scope)
- Any existing PASS content

---

[CANONICAL ID FORMAT SPECIFICATION]

The canonical ID format is:

  NAMESPACE:NNNN

Formal grammar (ABNF):

  canonical-id  = namespace ":" nnnn
  namespace     = 2*6UPALPHA
  nnnn          = 4DIGIT
  UPALPHA       = %x41-5A   ; uppercase ASCII A–Z
  DIGIT         = %x30-39   ; 0–9

Normative rules:

  R-ID-1  A canonical ID MUST match the pattern ^[A-Z]{2,6}:[0-9]{4}$.
          Any string that does not match this pattern is not a canonical ID.

  R-ID-2  NAMESPACE MUST be 2–6 uppercase ASCII letters (A–Z only).
          No digits, hyphens, underscores, or other characters are permitted in NAMESPACE.

  R-ID-3  NNNN MUST be exactly four digits, zero-padded.
          ECO:0001 is valid. ECO:1 and ECO:01 and ECO:00001 are not valid.

  R-ID-4  NNNN MUST be in the range 0001–9999.
          NNNN 0000 is reserved in every namespace and MUST NOT be assigned to any PASS.

  R-ID-5  The separator MUST be a single colon character (U+003A).
          No other separator is valid. Spaces around the colon are not permitted.

  R-ID-6  Canonical IDs are case-sensitive. ECO:0001 and eco:0001 are not the same string.
          Implementations MUST treat them as different identifiers.

  R-ID-7  A canonical ID is globally unique within its namespace.
          ECO:0001 and GC:0001 are different identifiers belonging to different namespaces.
          Within the ECO: namespace, ECO:0001 MUST refer to exactly one PASS.

Valid examples:
  ECO:0001    GC:1001    ACME:0042    CITYX:2500    AB:9001

Invalid examples:
  ECO:1       — NNNN not zero-padded to 4 digits
  eco:0001    — NAMESPACE not uppercase
  ECO:0000    — 0000 is reserved
  ECO:10000   — NNNN exceeds 4 digits
  E:0001      — NAMESPACE too short (minimum 2 characters)
  TOOLONGNS:0001  — NAMESPACE exceeds 6 characters
  ECO-0001    — invalid separator (hyphen instead of colon)

---

[ONS CONFORMANCE]

The NAMESPACE portion of a canonical ID MUST conform to the ONS governance_cluster
casing rule declared in ONS.00 and enforced by ONS.01:

  Pattern:  ^[A-Z]{2,6}$
  Rule:     UPPER
  Domain:   governance_cluster

This rule requires NAMESPACE to be entirely uppercase ASCII, 2–6 characters. CANON
inherits this constraint from ONS rather than redefining it. If ONS updates the
governance_cluster rule, CANON.01 MUST be amended before the new ONS rule applies
to CANON namespace prefixes. Until such an amendment exists, the rule above is binding.

The full canonical ID NAMESPACE:NNNN is analogous to the ONS qualification_authority
pattern (UPPER:integer), with the stricter CANON-specific constraint that the integer
portion is exactly 4 zero-padded digits (R-ID-3). The CANON pattern is a conformant
specialization of the ONS qualification_authority pattern — it satisfies the broader
pattern while adding the zero-padding and length constraint.

---

[NAMESPACE DECLARATION]

An organization adopts CANON by declaring a namespace. Namespace declaration is
self-declared — no registration with Governance Commons is required. The declaring
organization is responsible for prefix uniqueness.

Declaration document

Each adopting organization MUST maintain a namespace declaration document. The
RECOMMENDED filename is namespace.yaml. The declaration MUST contain:

  prefix:
    description: The namespace prefix string. MUST conform to R-ID-2.
    example: ECO

  owner:
    description: The organization or individual that owns this namespace.
    example: "eco ecosystem — jj-ervin"

  description:
    description: One sentence describing what governance domain this namespace covers.

  allocation_authority:
    description: >
      The identity (person, role, or process) with authority to assign canonical IDs
      within this namespace. Only the declared allocation authority may assign new
      NAMESPACE:NNNN identifiers. See [ALLOCATION AUTHORITY] section.

  registry_file:
    description: Relative path to the conformant PASS registry for this namespace.
    example: "passes/passes.registry.json"

  layers_file:
    description: Relative path to the layers declaration file for this namespace.
    example: "passes/layers.yaml"

  created_at:
    description: ISO 8601 timestamp of namespace declaration.

  canon_version:
    description: The version of the CANON standard this namespace declaration conforms to.
    example: "CANON.01"

Optional fields:

  collision_note:
    description: >
      If the organization knows of another namespace with the same or similar prefix,
      this field documents the known collision and how the organization has scoped their
      use to avoid ambiguity.

  external_dependencies:
    description: >
      List of external namespace prefixes this namespace's PASSes may cite in depends_on.
      Informational; does not restrict what depends_on may contain.

Namespace declaration MUST be committed to the adopter's governance repository. It is
a governed document — changes to the declaration (especially allocation_authority and
prefix) require a PASS decision in the adopter's governance system.

Prefix ownership

  R-NS-1  A namespace prefix is owned by the organization that first declares it.
          Governance Commons does not adjudicate prefix disputes.

  R-NS-2  An organization MUST NOT issue canonical IDs under a prefix it does not own.
          ECO:NNNN records may only be issued by the eco ecosystem allocation authority.

  R-NS-3  If a prefix collision is discovered after deployment, the later adopter SHOULD
          choose a new prefix. The earlier adopter's records take precedence in any
          tooling that uses the declared namespace registry.

  R-NS-4  A prefix that has been used to issue canonical IDs MUST NOT be abandoned without
          a public deprecation record declaring the last valid ID issued and the date of
          deprecation.

---

[LAYERS DECLARATION]

Each namespace MUST maintain a layers declaration file that maps NNNN ranges to named
governance layers. The RECOMMENDED filename is layers.yaml.

Required fields per layer entry:

  range:
    description: >
      The NNNN range this layer covers, inclusive on both ends.
      Format: "NNNN-NNNN" where both values are 4-digit zero-padded integers.
    example: "0000-0999"

  name:
    description: A short lowercase identifier for this layer.
    example: "authority"

  description:
    description: One sentence describing what governance concern this layer covers.

Normative rules:

  R-LY-1  Layer ranges within a namespace MUST NOT overlap.
          If 0000-0999 is declared as authority, no other layer may include any value
          in that range.

  R-LY-2  NNNN 0000 MUST NOT appear as an assignable range.
          The 0000 value is reserved (R-ID-4). A layer that begins at 0000 covers
          the range 0000-XXXX for documentary purposes only; 0000 itself is not
          assignable. Implementations MUST NOT assign a PASS to NNNN 0000.

  R-LY-3  Layer ranges do not need to be contiguous or cover the full 0001-9999 space.
          A namespace may declare layers for only the ranges it currently uses.
          Unspecified ranges are implicitly unallocated.

  R-LY-4  A PASS assigned an ID in a given range MUST be categorized under the layer
          whose range includes that NNNN value. If no layer covers that NNNN, the
          assignment is a layer violation and SHOULD be corrected by amending the
          layers file to add a covering layer entry.

  R-LY-5  Adding a new layer entry or extending a range is permitted without a migration
          PASS, provided the new or extended range does not overlap existing ranges.

  R-LY-6  Removing a layer entry or narrowing a range that covers existing assigned IDs
          is not permitted without a PASS decision that either reassigns the affected
          IDs to a new layer or confirms the affected IDs are all superseded.

  R-LY-7  The 9000-9999 range SHOULD be declared as reserved in any conformant namespace.
          Reserved means no PASSes are assigned to this range without an explicit PASS
          decision expanding the layers declaration to cover a specific purpose.

ECO: reference layer grammar (informative, not normative for other adopters)

  This is the starter grammar — short enough to memorize, portable enough for any adopter
  to reuse as a starting point. ECO: declares this in its own layers.yaml; CANON does not
  mandate it for other namespaces.

  0000-0999  authority       — agent identity, invariants, conduct standards
  1000-1999  operational     — executable asset governance, pipeline governance
  2000-2999  domain          — vertical and industry-specific governance
  3000-3999  platform        — platform architecture, naming, release governance
  4000-4999  data-interop    — schemas, data contracts, interoperability rules
  9000-9999  reserved        — future use, experimental ranges, emergency governance

An external adopter MAY use these same bands, different bands, or a subset of bands.
CANON does not require band alignment across namespaces.

---

[ALIAS MODEL]

An alias is any non-canonical identifier that resolves to a canonical ID.

Two alias types:

  named-cluster alias
    A governance cluster identifier of the form CLUSTER.SEQ (per ONS governance_id_grammar).
    Examples: ACES.01, OG.02, EDGE.06, CANON.00
    These are the human-readable names used inside the adopting organization.

  legacy alias
    A prior identifier from a governance system that predates CANON adoption.
    Examples: 000.01, 0097.00, GC-PASS-0003.00
    These are preserved permanently after migration.

Where aliases live

  Aliases are stored in the PASS registry entry for their canonical ID:
  - named-cluster aliases → the `alias` field (single string; the primary human name)
  - legacy identifiers → the `legacy_ids` array (zero or more prior IDs)

Normative rules:

  R-AL-1  An alias is never a stable citation target. Tooling, CI, and external references
          MUST use the canonical form. Aliases are for human readability only.

  R-AL-2  Within a namespace, every alias MUST be unique.
          Two different canonical IDs within the same namespace MUST NOT share the same
          alias string. If a naming conflict exists, the later PASS takes a different alias;
          the earlier PASS keeps its existing alias.

  R-AL-3  The same alias string MAY exist in different namespaces.
          ACES.01 in the ECO: namespace resolves to ECO:0001.
          ACES.01 in the ACME: namespace (if ACME had such a PASS) would resolve to ACME:XXXX.
          These are different resolutions; context (the namespace) determines which applies.

  R-AL-4  Aliases are immutable once a canonical ID is assigned.
          A named-cluster alias may not be transferred to a different canonical ID.
          If a cluster is reorganized and the alias would be misleading, the affected
          PASS SHOULD be superseded and the new PASS gets the new alias. The old alias
          remains with the superseded record.

  R-AL-5  Legacy aliases are preserved permanently.
          Once a legacy_id is recorded, it MUST NOT be removed from the registry entry.
          A tool that receives a legacy alias SHOULD resolve it to the canonical ID.

Alias resolution protocol

  Tools and agents that encounter an identifier MUST determine whether it is a canonical
  ID (matches R-ID-1) or an alias (does not match R-ID-1) before processing it.

  Resolution steps:
  1. If the identifier matches ^[A-Z]{2,6}:[0-9]{4}$, it is a canonical ID. Look it up
     directly in the appropriate namespace registry.
  2. If the identifier does not match, treat it as an alias. Search the registry for an
     entry where alias == identifier or legacy_ids contains identifier.
  3. If no entry is found in step 2, the identifier is unresolvable. Treat as an error.
  4. Aliases are resolved within the context of the current namespace. If the namespace
     is ambiguous, the resolver MUST require the caller to specify a namespace.

  R-AL-6  A resolver MUST NOT guess the namespace when resolving an alias.
          If context does not determine the namespace, resolution MUST fail with an
          "ambiguous alias" error, not silently resolve to a default namespace.

---

[ALLOCATION AUTHORITY]

The allocation authority for a namespace is the entity declared in the namespace
declaration document's `allocation_authority` field. Only the declared allocation
authority may assign new NAMESPACE:NNNN identifiers.

  R-AA-1  A canonical ID assignment MUST be traceable to a PASS decision.
          An ID that appears in the registry without an associated PASS record is
          an ungoverned entry and MUST be treated as invalid until a governing PASS
          is produced that ratifies the assignment.

  R-AA-2  The allocation authority MUST be declared in the namespace declaration.
          If no allocation authority is declared, no canonical IDs may be assigned
          in that namespace until the declaration is corrected.

  R-AA-3  The allocation authority MAY delegate to a process (e.g., a CI-enforced
          migration PASS) but may not delegate to an agent acting without a PASS record.
          All delegation must be traceable.

  R-AA-4  An allocation authority change requires a PASS decision in the adopter's
          governance system and MUST update the namespace declaration document.

Sequential assignment

  IDs within a namespace do not need to be assigned sequentially. Gaps are permitted
  and expected — a migration PASS may assign ECO:0042 without first assigning 0001-0041.
  Unassigned IDs in a range are implicitly available for future allocation.

  R-AA-5  An ID MUST NOT be assigned to more than one PASS, ever.
          Once assigned, the ID is permanently bound to that PASS record, even after
          supersession.

Range reservation

  A PASS may declare a reservation of a range of IDs for future use. A reservation:
  - Blocks those IDs from being assigned to a different purpose
  - Does not constitute a PASS assignment (reserved IDs are not assigned PASSes)
  - Is recorded as a registry entry with status: "reserved"

  Reserved registry entry minimum fields:
    id:           "NAMESPACE:NNNN" — the reserved ID or the first ID in a reserved range
    status:       "reserved"
    reserved_for: description of the intended future use
    reserved_by:  the canonical ID or named form of the PASS that declared the reservation
    range:        "NNNN-NNNN" if a range is reserved (optional; single ID if absent)

  R-AA-6  A reservation MUST be recorded in the registry before it takes effect.
          Verbal or document-only reservations without a registry entry are not enforceable.

  R-AA-7  A reservation MAY be released by a subsequent PASS that either:
          (a) assigns the reserved range to a specific purpose, or
          (b) explicitly withdraws the reservation and marks the IDs as available.

---

[SUB-PASS RELATIONSHIP MODEL]

All PASSes have flat canonical IDs. There is no hierarchy in the ID itself. Parent-child
relationships and cluster groupings are expressed entirely through registry fields.

parent field

  A PASS that is a logical sub-component of another PASS declares the parent PASS's
  canonical ID in its `parent` registry field.

  Example:
    CANON.01 is a sub-PASS of the CANON cluster. Its registry entry declares:
      parent: "<CANON.00 canonical ID, assigned by CANON.03>"

  R-SP-1  The parent field MUST reference a valid, non-superseded canonical ID.
          A PASS whose parent is superseded SHOULD be updated to reference the superseding
          PASS, or superseded itself if the parent's content no longer applies.

  R-SP-2  The parent relationship is informational, not governing.
          A sub-PASS is a full, independent PASS with its own canonical ID, its own
          invariants, and its own acceptance record. The parent field describes
          organizational grouping; it does not make the sub-PASS subordinate in authority.

  R-SP-3  A PASS without a parent is a root PASS. Root PASSes are typically cluster
          headers (the CLUSTER.00 record). Root PASSes declare parent: null.

cluster field

  A PASS's `cluster` field declares the named cluster it belongs to (e.g., "CANON",
  "ACES", "OG"). This is the ergonomic grouping that corresponds to the named-cluster
  alias system.

  R-SP-4  A PASS's cluster field MUST match the NAMESPACE-part of its alias, if one
          exists. If a PASS has alias "ACES.01", its cluster field MUST be "ACES".

  R-SP-5  The cluster field is a registry convenience field; it does not affect the
          canonical ID or the ID's immutability.

Cluster header convention

  The first PASS in any named cluster SHOULD be the cluster header, with alias CLUSTER.00.
  The cluster header declares what the cluster governs and what sub-PASSes it contains.
  All subsequent PASSes in the cluster declare parent: <cluster-header-canonical-id>.

  This convention is a SHOULD, not a MUST. Legacy clusters that predate CANON may not
  have a formal cluster header. During migration (CANON.03), such clusters SHOULD be
  noted as having no declared header rather than retroactively creating one.

---

[IMMUTABILITY SPECIFICATION]

A canonical ID becomes immutable at the moment it is assigned to a PASS. Assignment
occurs when a registry entry is written with status "accepted" or "sealed" (or
equivalent non-draft, non-reserved status).

What immutability means

  R-IM-1  Once a canonical ID is assigned (status accepted or higher), the binding
          between the ID and its PASS MUST NOT change.
          The ID always refers to the same PASS record, even after that record is
          superseded.

  R-IM-2  The NAMESPACE portion of a canonical ID MUST NOT change after assignment.
          ECO:0001 cannot become GC:0001 or ACME:0001. The namespace is part of the
          immutable binding.

  R-IM-3  The NNNN portion of a canonical ID MUST NOT change after assignment.
          ECO:0001 cannot become ECO:0042. The number is part of the immutable binding.

  R-IM-4  A canonical ID MUST NOT be reassigned after the bound PASS is superseded.
          The superseded PASS retains the ID permanently. The superseding PASS receives
          a new canonical ID.

  R-IM-5  The registry entry for an assigned ID MAY be updated in limited ways:
          - status may change from accepted → sealed, or accepted → superseded
          - superseded_by may be set (to record the superseding canonical ID)
          - path may be updated if the document moves (with a changelog entry)
          All other fields are immutable once status reaches accepted.

Supersession protocol

  When a PASS is found to be wrong, outdated, or in need of replacement:

  Step 1  Write a new PASS that addresses the deficiency.
          The new PASS declares what it supersedes in its supersedes[] registry field.

  Step 2  Assign a new canonical ID to the new PASS through the normal allocation process
          (a migration PASS if this is a legacy record, or normal allocation if new).

  Step 3  Update the old PASS's registry entry:
          - Set status to "superseded"
          - Set superseded_by to the new PASS's canonical ID
          - Do not alter any other fields

  Step 4  The old PASS document SHOULD have a supersession notice appended at the top:
          "SUPERSEDED by <new canonical ID> — <date>"
          The document content MUST NOT be edited; only the notice is appended.

  R-IM-6  A superseded PASS remains in the registry permanently.
          It is never deleted. Its canonical ID is never reassigned. It remains
          resolvable as a historical record.

  R-IM-7  A superseded PASS MUST NOT be cited as a live governance reference.
          Tooling that discovers a dependency on a superseded ID SHOULD warn the caller
          that the cited PASS has been superseded and provide the superseded_by ID.

---

[NORMATIVE REQUIREMENTS SUMMARY]

The following table collects all MUST/SHOULD/MAY requirements declared in this PASS.
These are the rules an organization implements when adopting CANON.

  Rule     Level   Statement
  -------  ------  ---------------------------------------------------------------
  R-ID-1   MUST    Canonical IDs match ^[A-Z]{2,6}:[0-9]{4}$
  R-ID-2   MUST    NAMESPACE is 2–6 uppercase ASCII letters only
  R-ID-3   MUST    NNNN is exactly 4 zero-padded digits
  R-ID-4   MUST    NNNN 0000 is reserved; never assigned
  R-ID-5   MUST    Separator is a single colon character
  R-ID-6   MUST    Canonical IDs are case-sensitive
  R-ID-7   MUST    Within a namespace, a canonical ID refers to exactly one PASS
  R-NS-1   —       Prefix ownership is first-declared; no GC adjudication
  R-NS-2   MUST    Organizations only issue IDs under prefixes they own
  R-NS-3   SHOULD  Later adopters choose new prefix on collision discovery
  R-NS-4   MUST    Used prefixes MUST NOT be abandoned without a deprecation record
  R-LY-1   MUST    Layer ranges within a namespace must not overlap
  R-LY-2   MUST    NNNN 0000 must not be assignable in any layer declaration
  R-LY-3   —       Layers need not be contiguous or cover the full 0001-9999 space
  R-LY-4   MUST    Assigned IDs must fall within a declared layer range
  R-LY-5   —       Adding a new non-overlapping layer does not require a migration PASS
  R-LY-6   MUST    Removing or narrowing a range over assigned IDs requires a PASS decision
  R-LY-7   SHOULD  9000-9999 should be declared as reserved in any conformant namespace
  R-AL-1   MUST    Aliases are never stable citation targets; tooling MUST use canonical form
  R-AL-2   MUST    Within a namespace, aliases must be unique
  R-AL-3   —       Same alias string may exist in different namespaces
  R-AL-4   MUST    Aliases are immutable once a canonical ID is assigned
  R-AL-5   MUST    Legacy aliases must not be removed from registry entries
  R-AL-6   MUST    Resolvers must not guess the namespace for an alias
  R-AA-1   MUST    ID assignments must trace to a PASS decision
  R-AA-2   MUST    Allocation authority must be declared in namespace declaration
  R-AA-3   MUST    Delegation must be traceable; agents cannot allocate without a PASS record
  R-AA-4   MUST    Allocation authority changes require a PASS decision
  R-AA-5   MUST    An ID must not be assigned to more than one PASS, ever
  R-AA-6   MUST    Reservations must be recorded in the registry before taking effect
  R-AA-7   —       Reservations may be released by a subsequent PASS
  R-SP-1   MUST    Parent field must reference a valid, non-superseded canonical ID
  R-SP-2   —       Sub-PASS is a full independent PASS; parent is organizational only
  R-SP-3   —       Root PASSes (cluster headers) declare parent: null
  R-SP-4   MUST    Cluster field must match the NAMESPACE-part of the alias
  R-SP-5   —       Cluster field is a convenience field; does not affect ID immutability
  R-IM-1   MUST    ID-to-PASS binding must not change after assignment
  R-IM-2   MUST    NAMESPACE must not change after assignment
  R-IM-3   MUST    NNNN must not change after assignment
  R-IM-4   MUST    A canonical ID must not be reassigned after its PASS is superseded
  R-IM-5   MAY     Registry entries may be updated in limited ways after acceptance
  R-IM-6   MUST    Superseded PASSes remain in the registry permanently
  R-IM-7   SHOULD  Tooling should warn on dependency on a superseded ID

---

[REASONING — 5 QUESTIONS]

1. Why exactly four zero-padded digits (0001–9999)?
Four digits gives 9,999 possible IDs per namespace — sufficient for any governance system
likely to be built in the near to medium term. Zero-padding ensures consistent string length,
which simplifies sorting, display, and pattern matching. An unpadded integer (ECO:1 vs ECO:001
vs ECO:0001) creates ambiguity in string comparison and display. Four digits is the minimum
length that covers plausible governance growth while remaining short enough to memorize and type.
Three digits (999 IDs) is too small for a mature ecosystem; five digits (99,999) would be
unusual enough to seem over-engineered for a governance system.

2. Why is alias resolution namespace-scoped rather than global?
Global alias resolution requires a global registry — a single source of truth that every
adopter must consult. That creates a centralization dependency incompatible with the
self-declaration model. Namespace-scoped resolution means an adopter's tools only need to
know about the namespaces they depend on. When depends_on references a cross-namespace
ID (ECO:0001), the resolver consults the ECO: registry — not a global alias table.
This keeps CANON decentralized while making cross-namespace dependencies explicit.

3. Why are sub-pass relationships in the registry rather than in the ID?
Hierarchical IDs (ECO:1000.01) embed structure that can become incorrect as the governance
system evolves — a sub-pass may be promoted to a root PASS, a cluster may be reorganized,
a PASS may be extracted from one cluster and placed in another. When structure is in the ID,
the ID must change when structure changes, which violates immutability. When structure is
in the registry, the ID is stable and the organizational relationship can evolve without
invalidating citations.

4. Why does immutability apply at assignment time rather than at sealing time?
Sealing is a governance status indicating a PASS's content is frozen. Assignment is when
a number is bound to a PASS. These are different events and should have different
immutability guarantees. A PASS's content may still be in draft when its ID is assigned
(the number is reserved for it). Making the ID immutable at assignment time, not at sealing
time, means that tooling can cite the ID even before the PASS is sealed, and the citation
will remain valid after sealing. If immutability only triggered at sealing, the period
between assignment and sealing would be ungoverned.

5. Why is ONS conformance declared as a dependency rather than restating the rules?
Restating ONS rules in CANON.01 would create two authoritative sources for the same
rule — a classic governance duplication problem. If ONS updates the governance_cluster
pattern (e.g., to allow longer prefixes), CANON.01 would need to be amended separately.
By declaring ONS.00 and ONS.01 as dependencies and explicitly referencing their rules,
CANON.01 inherits ONS governance: an ONS amendment that changes the relevant rule
automatically triggers the requirement for a CANON.01 amendment. The dependency chain
is the governance chain.

---

[OUTPUTS]
- PASS CANON.01 accepted as the normative PASS Identifier Governance specification
- Canonical ID grammar declared: ^[A-Z]{2,6}:[0-9]{4}$ with R-ID-1 through R-ID-7
- ONS conformance rule declared: NAMESPACE conforms to ONS governance_cluster pattern
- Namespace declaration specification declared: namespace.yaml format and required fields
- Layers declaration specification declared: layers.yaml format, required fields, R-LY rules
- Alias model declared: two alias types, uniqueness rules, resolution protocol, R-AL rules
- Allocation authority model declared: traceability, delegation, reservation, R-AA rules
- Sub-pass relationship model declared: parent field, cluster field, R-SP rules
- Immutability specification declared: what is immutable, supersession protocol, R-IM rules
- Normative requirements summary table: all MUST/SHOULD/MAY rules in one reference

[DELTA SUMMARY]
- Declared canonical ID grammar with formal ABNF, validity rules (R-ID-1–7), valid/invalid
  examples; reserved NNNN 0000 in all namespaces
- Declared ONS conformance: NAMESPACE matches governance_cluster pattern ^[A-Z]{2,6}$;
  CANON canonical ID is a conformant specialization of ONS qualification_authority
- Declared namespace declaration: namespace.yaml format; 8 required fields; 2 optional fields;
  prefix ownership rules (R-NS-1–4); self-declaration model; no GC registration required
- Declared layers declaration: layers.yaml format; 3 required fields per entry; 7 normative
  rules (R-LY-1–7); ECO: reference grammar (0000s–9000s) as informative, not normative;
  9000-9999 SHOULD be reserved in all conformant namespaces
- Declared alias model: 2 alias types (named-cluster, legacy); alias stored in alias and
  legacy_ids fields; 6 rules (R-AL-1–6); namespace-scoped resolution protocol; 4-step
  resolver algorithm; ambiguous alias must error, not silently resolve
- Declared allocation authority model: must be declared in namespace.yaml; ID assignments
  must trace to PASS; delegation must be traceable; 7 rules (R-AA-1–7); sequential gaps
  permitted; range reservation mechanism (reserved status + minimum fields)
- Declared sub-pass model: flat IDs only; parent field (canonical ID reference); cluster
  field (matches alias NAMESPACE-part); 5 rules (R-SP-1–5); cluster header convention
  (SHOULD, not MUST); legacy clusters without headers noted during migration
- Declared immutability: immutable at assignment (not at sealing); 7 rules (R-IM-1–7);
  4-step supersession protocol; superseded PASSes permanent; tooling SHOULD warn on
  superseded dependency
- Published normative requirements summary table: 37 rules across 7 rule families

[CONSTRAINT VALIDATION]
- Does not assign canonical IDs: confirmed; all assignments deferred to CANON.03
- Does not define registry schema beyond alias and legacy_ids field descriptions: confirmed;
  full schema, write authority, CI integration, and changelog are CANON.02 scope
- Does not modify ONS: confirmed; ONS is declared as dependency, not redefined
- Does not govern PASS content: confirmed; all rules govern IDs, namespaces, layers,
  and aliases — not what a PASS says
- CANON-CI-1 (immutable): R-IM-1 through R-IM-7 enforce immutability; supersession protocol
  provides the correction path without violating immutability
- CANON-CI-2 (numbers canonical): R-AL-1 (aliases not stable citation targets) enforces this
- CANON-CI-3 (flat IDs): sub-pass model explicitly prohibits hierarchy in ID; parent/cluster
  are registry-only fields
- CANON-CI-4 (registry governed): allocation authority traceability (R-AA-1 through R-AA-4)
  and reserved entry requirements begin the registry governance chain; CANON.02 completes it
- CANON-CI-5 (layers per-namespace): ECO: reference grammar is declared informative; R-LY rules
  govern the grammar without mandating specific band values
- CANON-CI-7 (legacy preserved): R-AL-5 (legacy aliases must not be removed) enforces this
- CANON-CI-8 (migration governed): R-AA-1 (assignments trace to PASS) and R-AA-3 (agents
  cannot allocate without PASS) together enforce governed migration

[REVERSIBILITY]
Reversing CANON.01 requires a CANON amendment PASS that:
- explicitly supersedes this PASS
- documents which normative rules changed and why
- confirms that existing conformant implementations remain valid or declares a transition period
- addresses any rule changes that affect immutability guarantees already relied upon
Until such a PASS exists, CANON.01 is the normative PASS Identifier Governance specification.

[HANDOFF]

next_action: Write CANON.02 — Registry Governance
  Must specify: full registry schema (all required and optional fields with types and
  constraints), extension model (how adopters add namespace-specific fields), write
  authority declaration format, schema validation contract and error types, append-only
  changelog requirement and format, CI integration contract (what CI must check and how
  to report violations), dependency validation (how depends_on entries are validated),
  and the registry-as-governed-artifact declaration with provenance chain requirements.

required_inputs for CANON.02:
  - CANON.01 (this file — alias model, registry field names, allocation authority model)
  - CANON.00 (invariants — especially CANON-CI-4 registry as governed artifact)
  - governance-commons existing schemas (schemas/) for format consistency
  - GC governance/agent-constraints.yaml (write authority pattern already in use)

forbidden_scopes for CANON.02:
  - Do not assign ECO: or GC: numbers — CANON.03 scope
  - Do not modify the canonical ID grammar declared here
  - Do not redefine alias model rules declared here
  - Do not govern PASS content

next_after_CANON.02: Write CANON.03 — Migration Protocol (eco first-adopter)

[FINALIZATION]
PASS CANON.01 is ACCEPTED as the normative PASS Identifier Governance specification.
All organizations adopting CANON MUST conform to the rules declared in this PASS.
CANON.02 is the next required PASS.
