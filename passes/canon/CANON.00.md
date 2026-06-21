PASS CANON.00 — Canonical PASS Identifier Standard (Cluster Header)

[NP-METADATA]
- PASS ID: CANON.00
- Canonical ID: PENDING — assigned by CANON.03 (Migration Protocol)
- Name: Canonical PASS Identifier Standard — Cluster Header
- Domain: governance.pass.identity
- Role: CREATE
- Predecessor: GC-PASS-0005.00 (last accepted GC governance decision)
- Actor: Jess Ervin (GC founder) + Claude (claude-sonnet-4-6)
- Date: 2026-06-20
- time.loc: 2026-06-20T00:00:00Z
- Authority: AL:2 — GC maintainer decision
- Status: ACCEPTED
- Registry: registry/clusters.yaml — CANON cluster entry required (output of this PASS)

---

[PROBLEM]

Two compounding issues make the current PASS identifier system ungoverned and non-portable.

Issue 1 — Unauthorized drift
The rule "Do not create new numbered PASSes — use named cluster convention" was written
into eco's PASS-INDEX without a governing decision, reasoning block, or founder sign-off.
It was agent drift: an AI agent made an architectural call it had no authority to make.
The result is that the current named-cluster-only convention is ungoverned. It has no PASS
record. It cannot be cited. It cannot be audited. It cannot be formally reversed without
a governing PASS to supersede it.

Issue 2 — Portability gap
Named cluster identifiers (ACES.01, OG.02, EDGE.06) are meaningful inside eco and opaque
outside it. An external organization adopting Governance Commons cannot cite "ACES.01" as
a governance reference — it carries no stable meaning without eco context. For Governance
Commons to function as a portable standard, PASS identifiers must be:
  - Universally citable by number, not by internal alias
  - Namespace-safe so multiple organizations can adopt without collision
  - Machine-readable so CI, agents, and tooling can validate PASS references
  - Stable and immutable once assigned

Neither issue can be resolved by a passchangelog entry alone. A governing standard is required.

---

[CLUSTER DECLARATION]

CANON is the Canonical PASS Identifier Standard cluster for Governance Commons.

CANON governs:
- The canonical ID format: <namespace>:<four-digit-id>
- The namespace model: how prefixes are declared; what ownership means; collision avoidance
- The layer band grammar: how namespaces declare semantic layers — not what the layers are
- The alias model: how named cluster identifiers relate to canonical IDs
- The registry standard: schema, governance, write authority, audit trail
- The migration protocol: how existing PASSes gain canonical IDs
- The bootstrap condition: CANON.00 itself is assigned a canonical ID via CANON.03

CANON does not govern:
- The specific layer band assignments for any namespace (eco declares its own; ACME declares its own)
- The content or rules of any PASS (ACES, OG, and domain clusters govern this)
- ONS naming grammar for cluster names (ONS.00 and ONS.01 govern this)
- Any eco-internal PASS implementation (eco adopts CANON; eco does not define it)
- Publication, versioning, or distribution of GC itself (GC REL cluster governs this)

CANON is a GC-level standard. It sits above any single organization's governance system.
eco and GC are first adopters. Other organizations are future adopters.
CANON must be portable to all of them.

---

[CANONICAL ID FORMAT]

The canonical ID format is:

  <NAMESPACE>:<NNNN>

Where:
- NAMESPACE is the organization or ecosystem prefix (e.g., ECO, GC, ACME, CITYX)
- NNNN is a four-digit zero-padded integer (0001 through 9999)
- The colon is the separator; no other separators are valid in a canonical ID

Examples:
  ECO:0001    — eco ecosystem, PASS 0001
  GC:1001     — Governance Commons, PASS 1001
  ACME:1001   — external adopter ACME, PASS 1001

Each namespace is independent. ECO:1001 and GC:1001 and ACME:1001 are three different
PASSes owned by three different organizations. There is no collision.

Flat IDs only. The canonical form is always NAMESPACE:NNNN — never NAMESPACE:NNNN.NN
or NAMESPACE:NNNN.NN.NN. Parent-child relationships between PASSes are expressed in
registry fields (parent, cluster), not in the ID itself. This makes IDs simpler to cite,
simpler to validate, and simpler for tools to consume.

---

[ALIAS MODEL]

Named cluster identifiers (ACES.01, OG.02, EDGE.06, CANON.00) are aliases — ergonomic,
human-readable labels that resolve to a canonical ID.

Rules:
- Aliases are useful for humans; they are never the stable citation target
- Tooling, CI pipelines, and external references MUST use the canonical form
- An alias may change (cluster renamed, reorganized) — the canonical ID never changes
- Every PASS has exactly one canonical ID and zero or more aliases
- Named cluster identifiers in existing PASSes remain valid aliases after migration;
  they do not need to be rewritten in historical documents

The registry is the source of truth for alias resolution:
  ACES.01 → ECO:0001  (example — actual mapping declared in CANON.03)

---

[IMMUTABILITY]

Canonical IDs are immutable. Once assigned:
- The ID never changes
- The ID is never reassigned to a different PASS
- The ID is never reused after a PASS is superseded
- The PASS may be superseded; the ID record remains

If a PASS was assigned to the wrong layer or wrong number, the correction is:
  1. Write a new PASS with the correct content
  2. The old PASS is marked: superseded_by: <new canonical ID>
  3. The old canonical ID remains valid as a historical reference

There is no "move" operation. There is only supersession.

---

[LAYER BAND GRAMMAR]

CANON defines how a namespace declares its layer bands. It does not define what bands
any adopter must use.

Each namespace that adopts CANON declares a layers file (layers.json or layers.yaml)
containing its band assignments. The CANON standard specifies the required fields for
that file; the adopter specifies the values.

Required fields per layer entry:
  - range: the NNNN range this layer covers (e.g., "0000-0999")
  - name: a short identifier for this layer (e.g., "authority")
  - description: one sentence describing what governance concern this layer covers

ECO: namespace declares its own layers file. GC: namespace declares its own. These may
differ. The grammar ensures interoperability; the assignments ensure autonomy.

Reference layer grammar for ECO: (declared in eco's layers file, not locked here):

  0000–0999  authority / constitutional — invariants, agent identity, conduct standards
  1000–1999  operational governance — executable asset governance, pipeline governance
  2000–2999  domain governance — vertical and industry-specific governance
  3000–3999  platform / infrastructure — platform architecture, naming, release
  4000–4999  data / schema / interop — schemas, data contracts, interoperability rules
  9000–9999  reserved — future use, experimental ranges, emergency governance

This is the starter grammar — short enough to be memorized, meaningful enough to be
used by someone unfamiliar with eco. Other organizations may adopt the same bands or
declare different ones.

---

[REGISTRY MODEL]

Every CANON-conformant namespace maintains a PASS registry. The registry is a governed
artifact, not a convenience file.

Minimum required fields per registry entry:

  {
    "id":            "<NAMESPACE>:<NNNN>",
    "alias":         "<named cluster identifier, e.g. ACES.01>",
    "legacy_ids":    ["<prior IDs, e.g. 000.01>"],
    "title":         "<human-readable name>",
    "layer":         "<layer name from namespace layers file>",
    "cluster":       "<cluster name>",
    "parent":        "<canonical ID of parent PASS, or null>",
    "status":        "draft | accepted | sealed | superseded",
    "timestamp":     "<ISO 8601>",
    "path":          "<relative path to PASS document>",
    "supersedes":    ["<canonical IDs this PASS supersedes>"],
    "superseded_by": "<canonical ID, or null>",
    "depends_on":    ["<canonical IDs this PASS depends on — cross-namespace allowed>"]
  }

The depends_on field supports cross-namespace references. An external adopter's PASS may
declare a dependency on an ECO: or GC: PASS:

  "depends_on": ["ECO:0001", "GC:1004"]

This is the mechanism by which external governance builds on GC foundational PASSes
without being inside the ECO: or GC: namespace.

Registry governance requirements (specified in CANON.02):
  - Schema validation: every entry must pass schema validation before being written
  - Append-only changelog: every write produces an audit entry
  - Write authority: declared in a governance document; agents may not write without authority
  - Originating PASS reference: every registry entry must trace to a PASS decision
  - Dependency validation: depends_on entries must resolve to valid, non-superseded records
    (or be explicitly marked as known-superseded dependencies)

---

[EXTERNAL ADOPTER MODEL]

Any organization may adopt the CANON standard without registering with GC. Adoption:

1. Declare a namespace prefix (e.g., ACME:)
   Self-declared. No GC registration required. The adopter is responsible for uniqueness.
   GC recommends: use an organization name or product namespace unlikely to collide.

2. Write a layers declaration file
   Following the CANON.01 layer grammar. Bands may match ECO: reference grammar or differ.

3. Maintain a conformant registry
   Following the CANON.02 schema and governance requirements.

4. Write a migration PASS (if pre-existing governance records exist)
   Following the CANON.03 migration protocol pattern. Each organization produces its own
   migration PASS; CANON.03 is eco's first-adopter migration, not a universal template.

An external adopter does not depend on the ECO: or GC: namespace for their own records.
They may cite ECO: or GC: records via depends_on. Their own records carry their own prefix.

---

[CLUSTER STRUCTURE]

CANON is a four-PASS cluster:

CANON.00 — Cluster Header (this file)
  Declares the problem, cluster identity, canonical ID format, alias model, immutability
  rules, layer grammar, registry model, external adopter model, and cluster invariants.
  Does not assign any canonical IDs. Does not define registry schema fields beyond
  minimum model. Sets scope for CANON.01–03.

CANON.01 — PASS Identifier Governance
  Normative specification for external adopters. Specifies the canonical ID format in
  full detail, namespace declaration rules, layer declaration file format and schema,
  alias resolution rules, immutability enforcement, allocation authority model, and the
  subpass relationship model in the registry.

CANON.02 — Registry Governance
  Normative registry specification. Specifies the full registry schema (all required
  and optional fields), extension model (adopter-specific fields), write authority
  declaration format, schema validation contract, append-only changelog requirement,
  CI integration contract, and the registry-as-governed-artifact declaration with
  provenance requirements.

CANON.03 — Migration Protocol (eco first-adopter)
  Governs retroactive assignment of canonical ECO: IDs to existing PASSes. Answers:
  what happens to legacy 000.xx–0167.xx IDs; which named PASSes become first canonical
  ECO: IDs; how legacy_ids are populated; what the conflict resolution rule is; who holds
  allocation authority for ECO:; and how the unauthorized named-cluster-only rule is
  formally reversed as a governed fix. CANON.03 is eco-specific. Other adopters produce
  their own migration PASSes following the pattern CANON.03 establishes.

---

[BOOTSTRAP ACKNOWLEDGMENT]

CANON.00 defines the canonical ID system. CANON.00 does not yet have a canonical ID.

This is the bootstrap condition: the standard that assigns IDs cannot assign its own ID
before the standard exists.

Resolution: CANON.03 will assign canonical IDs to all existing PASSes, including the
CANON cluster itself. Until CANON.03 is accepted and its assignments take effect:
  - CANON PASSes are identified by their named form (CANON.00, CANON.01, etc.)
  - The named form is valid during this bootstrap period
  - No citation of CANON PASSes by canonical number is valid until CANON.03 declares it
  - Other systems referencing CANON PASSes before CANON.03 should use the named form

---

[RELATIONSHIP TO EXISTING SYSTEMS]

ONS (Ontic Namespace Structure)
CANON depends on ONS for namespace prefix grammar. The NAMESPACE portion of a canonical
ID (e.g., ECO, GC, ACME) must conform to ONS naming rules. CANON does not redefine
naming grammar — it consumes it. CANON.01 will specify the exact ONS conformance rule
for namespace prefixes.

GC passchangelog
Every accepted CANON PASS produces a GC-PASS-NNNN.NN entry in the GC passchangelog.
The passchangelog records the governance decision. The PASS document is the specification.

eco
eco is CANON's first organizational adopter. eco implements CANON by declaring the ECO:
namespace, writing its layers file, maintaining a conformant registry, and completing
CANON.03 migration. eco does not govern CANON; eco implements it.

Governance Commons (GC:)
GC is also a CANON adopter in its own right, using the GC: namespace prefix for
GC-internal governance PASSes. The GC: namespace and ECO: namespace are distinct.
GC: records govern GC-wide standards; ECO: records govern the eco ecosystem.

GC cluster registry (registry/clusters.yaml)
CANON must be registered in the GC cluster registry. This PASS (CANON.00) is the
opening record for the CANON cluster. The cluster registry entry is an output of this PASS.

---

[CLUSTER INVARIANTS]

The following invariants govern all PASSes in the CANON cluster and all registries that
conform to the CANON standard. No CANON PASS may violate them. No amendment may remove
or weaken them.

CANON-CI-1 — IDs are immutable
Once a canonical ID is assigned, it never changes, never moves layers, and is never
reused after supersession. Mistakes are corrected by supersession: a new PASS is written,
the old one is marked superseded_by, and the old ID remains as a permanent historical record.

CANON-CI-2 — Numbers are canonical; names are aliases
The NAMESPACE:NNNN form is the durable, citable, portable identifier. Named identifiers
(ACES.01, OG.02) are ergonomic aliases. External citations, tooling, and CI must use the
canonical form. Aliases are for human readability only and are never stable citation targets.

CANON-CI-3 — IDs are flat
The canonical ID is always NAMESPACE:NNNN. Sub-PASS and parent-PASS relationships are
expressed in registry fields (parent, cluster), not in the ID. No decimal suffixes, no
hierarchical numbering in the canonical ID itself.

CANON-CI-4 — Namespace prefixes are non-transferable
An organization that declares a prefix owns it. ECO: belongs to the eco ecosystem; GC:
belongs to Governance Commons. No external adopter may issue records under a prefix they
do not own. GC does not assign prefixes — organizations self-declare; the CANON standard
provides the grammar and the collision-avoidance guidance.

CANON-CI-5 — The registry is a governed artifact
A PASS registry is not a convenience file. It requires declared write authority, schema
validation, an append-only audit trail, and a traceability requirement linking every entry
to a PASS decision. A registry that does not meet these requirements is not CANON-conformant.

CANON-CI-6 — Layer bands are per-namespace, not global
CANON specifies the layer declaration grammar. It does not mandate what bands any adopter
uses. Each namespace is autonomous in its layer assignments. The grammar ensures that any
adopter's layer structure is readable by a tool that understands CANON; it does not require
bands to match across namespaces.

CANON-CI-7 — Legacy IDs are preserved, not discarded
When existing PASSes receive canonical IDs, prior identifiers become legacy_ids — preserved
aliases in the registry entry. Legacy IDs are never deleted. A PASS with a legacy_id is
fully valid. The canonical form is preferred for new citations; the legacy form remains
resolvable.

CANON-CI-8 — Migration is governed
No canonical ID may be assigned to an existing PASS without a migration PASS that declares
the assignment, the legacy ID mapping, the conflict resolution rule, and the allocation
authority. Casual number assignment outside a migration PASS is a CANON violation and
produces an ungoverned registry entry.

---

[REASONING — 5 QUESTIONS]

1. Why is this a GC standard rather than an eco-internal PASS?
The portability problem is not eco-specific. Any organization adopting GC will face the
same issue: named clusters are opaque to outsiders, and PASS records without canonical IDs
cannot be cited in external standards, compliance mappings, or cross-organization governance.
A GC-level standard means every adopter gets a solution. An eco-internal PASS would solve
eco's problem and leave GC incomplete as a portable standard.

2. Why is the canonical ID NAMESPACE:NNNN rather than just NNNN?
A bare number (0001) collides the moment two organizations both adopt CANON. ECO:0001 and
GC:0001 and ACME:0001 are unambiguous. The namespace prefix is the collision boundary.
It also makes records self-describing in cross-organization contexts: the prefix declares
provenance without a lookup.

3. Why flat IDs rather than hierarchical (NAMESPACE:NNNN.NN)?
Hierarchical IDs embed structure in the identifier itself. When the structure changes —
a sub-pass is promoted, a cluster is reorganized — the ID becomes misleading without being
wrong. Flat IDs are stable because they carry no embedded structure. Relationships live
in the registry where they can be updated without changing the ID.

4. Why is the registry a governed artifact rather than a convenience file?
The registry becomes the single source of truth for PASS citation validity. Agents, CI
pipelines, and external tooling query it to validate dependencies and confirm that a cited
PASS exists, is not superseded, and belongs to the stated layer. A registry that can be
written without authority or validation is an ungoverned artifact — which is exactly the
failure mode the CANON standard exists to prevent.

5. What prevents CANON from drifting the way the numbered PASS system did?
CANON-CI-8 (migration is governed) closes the specific failure mode: an agent cannot
casually assign or remove canonical IDs without a governing PASS. CANON-CI-5 (registry
is a governed artifact) closes the second failure mode: the registry cannot become a
casual file updated without accountability. The bootstrap acknowledgment closes the third:
CANON.00 explicitly declines to assign numbers, preventing premature assignment before
the rules are fully specified in CANON.01–03.

---

[OUTPUTS]
- PASS CANON.00 accepted as the CANON cluster header and founding record
- CANON cluster identity, format, alias model, immutability rules, layer grammar,
  registry model, and cluster invariants (CANON-CI-1 through CANON-CI-8) declared
- CANON cluster entry added to registry/clusters.yaml
- GC-PASS-0006.00 entry added to passchangelog.md

[DELTA SUMMARY]
- Declared CANON cluster: canonical PASS identifier standard for Governance Commons
- Identified and named two governance failures: unauthorized drift (named-cluster-only rule
  without a governing PASS) and portability gap (named identifiers opaque outside eco)
- Declared canonical ID format: NAMESPACE:NNNN — flat, namespace-prefixed, four-digit
- Declared alias model: named cluster IDs (ACES.01) are aliases; NAMESPACE:NNNN is canonical
- Declared immutability rule: IDs never move, change, or are reused; mistakes → supersession
- Declared layer band grammar: per-namespace declaration; ECO: reference grammar published
  (0000s authority, 1000s operational, 2000s domain, 3000s platform, 4000s data/interop,
  9000s reserved) — not locked by CANON, declared by each adopter in their layers file
- Declared registry minimum model: id, alias, legacy_ids, title, layer, cluster, parent,
  status, timestamp, path, supersedes, superseded_by, depends_on (cross-namespace supported)
- Declared external adopter model: self-declared prefix, layers file, conformant registry,
  migration PASS; no GC registration required
- Declared 4-PASS cluster structure: CANON.00 (header), CANON.01 (ID governance),
  CANON.02 (registry governance), CANON.03 (eco migration)
- Declared bootstrap condition: CANON.00 has no canonical ID until CANON.03 assigns it
- Declared 8 cluster invariants (CANON-CI-1 through CANON-CI-8)

[CONSTRAINT VALIDATION]
- AL:2 authority confirmed: this is a GC maintainer-level decision; recorded in passchangelog
- Does not assign canonical IDs: number assignment deferred to CANON.03 per CANON-CI-8
- Does not define registry schema in full: detailed schema deferred to CANON.02
- Does not govern PASS content: explicitly excluded from CANON scope
- Does not modify ONS naming grammar: explicitly excluded; CANON.01 will declare ONS conformance
- Bootstrap acknowledged: CANON.00 named form is valid until CANON.03 assigns canonical IDs
- Cluster invariants do not contradict each other: CI-1 (immutable) + CI-8 (migration governed)
  work together; CI-3 (flat IDs) + CI-6 (layer per-namespace) are independent

[REVERSIBILITY]
Reversing CANON.00 requires a GC-level governance PASS that:
- explicitly supersedes this PASS
- documents why the canonical ID standard is being withdrawn or replaced
- addresses what happens to canonical IDs already assigned under CANON.03
- confirms no governance gap is introduced for organizations that adopted CANON
Until such a PASS exists, CANON.00 is the governing standard for PASS identification.

[HANDOFF]

next_action: Write CANON.01 — PASS Identifier Governance
  Must specify: canonical ID format in full normative detail (RFC 2119 MUST/SHOULD/MAY),
  namespace declaration rules and format, layers declaration file schema, alias resolution
  rules, immutability enforcement, allocation authority model, subpass relationship model
  in the registry, and ONS conformance rule for namespace prefixes.

required_inputs for CANON.01:
  - CANON.00 (this file — invariants, format, scope, adopter model)
  - ONS.00 and ONS.01 (naming grammar — NAMESPACE prefix must conform)
  - eco/passes/PASS-INDEX.md (existing named cluster inventory for alias design)
  - GC registry/clusters.yaml (cluster registry for context)

forbidden_scopes for CANON.01:
  - Do not assign specific ECO: or GC: numbers to existing PASSes — CANON.03 scope
  - Do not define full registry schema — CANON.02 scope
  - Do not govern PASS content
  - Do not modify ONS naming grammar

next_after_CANON.01: Write CANON.02 — Registry Governance
next_after_CANON.02: Write CANON.03 — Migration Protocol (eco first-adopter)

[FINALIZATION]
PASS CANON.00 is ACCEPTED as the CANON cluster header.
The CANON cluster is open. CANON.01 is the next required PASS.
No canonical IDs may be assigned until CANON.01 and CANON.02 are accepted and CANON.03
executes the migration.
CANON cluster invariants CANON-CI-1 through CANON-CI-8 are binding on all CANON PASSes
and on all registries claiming CANON conformance.
