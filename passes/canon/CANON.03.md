PASS CANON.03 — Migration Protocol (eco and GC First-Adopter)

[NP-METADATA]
- PASS ID: CANON.03
- Canonical ID: GC:2004 — assigned by this PASS (bootstrap resolution)
- Name: Migration Protocol — eco and GC First-Adopter
- Domain: governance.pass.identity
- Role: CREATE + FIX
- Predecessor: CANON.02
- Actor: Jess Ervin (GC founder) + Claude (claude-sonnet-4-6)
- Date: 2026-06-20
- time.loc: 2026-06-20T00:00:00Z
- Authority: AL:2 — GC maintainer decision
- Status: ACCEPTED

[PREDECESSOR IMPORT]
This PASS operates under all invariants declared in CANON.00 (CANON-CI-1 through CANON-CI-8)
and all normative rules declared in CANON.01 (R-ID through R-IM) and CANON.02 (R-RF through R-GA).
No CANON invariant or normative rule is waived or modified by this PASS.

[INTENT]
Govern the migration of existing governance records in the eco and Governance Commons ecosystems
into the CANON canonical identifier system. This PASS:

- Formally reverses the unauthorized named-cluster-only rule (the drift fix)
- Declares the ECO: namespace, its allocation authority, and its layer bands
- Declares the GC: namespace, its allocation authority, and its layer bands
- Declares the canonical ID assignment algorithm for existing PASSes
- Declares the legacy ID mapping rules
- Declares the conflict resolution rules
- Assigns canonical IDs to the CANON cluster (GC:2001–GC:2004)
- Assigns canonical IDs to the ACES cluster (ECO:0001–ECO:0007)
- Assigns canonical IDs to the OG cluster (ECO:1001–ECO:1003)
- Assigns canonical IDs to the RT/EV/OPS/REM operational PASSes (ECO:1004–ECO:1007)
- Declares the follow-on implementation task for remaining eco PASSes
- Resolves the CANON bootstrap condition: CANON cluster PASSes now have canonical IDs
- Produces companion artifacts: namespace.yaml, layers.yaml, and initial passes.registry.json
  for both the ECO: and GC: namespaces

[BOUNDARIES]
INCLUDES:
- Drift reversal: formal governance record of the unauthorized rule and its reversal
- ECO: namespace declaration and layer band assignments
- GC: namespace declaration and layer band assignments
- Assignment algorithm: rules for mapping existing PASSes to NAMESPACE:NNNN
- Legacy ID mapping rules: how numbered and prior-named PASSes become legacy_ids
- Conflict resolution rules: what to do when ambiguity or collision exists
- Initial canonical ID assignments: CANON, ACES, OG, RT, EV, OPS, REM clusters
- Follow-on task declaration: scope and rules for migrating remaining eco PASSes
- Bootstrap resolution: CANON cluster canonical IDs assigned here
- Companion artifacts: namespace.yaml and layers.yaml for ECO: and GC:;
  initial passes.registry.json for ECO: (ACES + OG) and GC: (CANON + ONS + GC core)
  with corresponding .jsonl changelog files

EXCLUDES:
- Canonical ID assignments for eco domain PASSes beyond those listed above
  (PLAT, ONS, DEVX, CK, HELM, LENS, EDGE, AGRI, AIRP, SUBP, etc. — follow-on task)
- Canonical ID assignments for legacy numbered PASSes (000.xx through 0167.xx) —
  follow-on task except where explicitly listed here
- Any modification to PASS content
- Any change to the CANON.00–CANON.02 normative rules

DEPENDS ON:
- CANON.01 (R-ID grammar, namespace declaration, alias model, R-AA rules)
- CANON.02 (entry schema, status values, write authority, changelog requirements)
- CANON.00 (invariants, bootstrap acknowledgment)
- eco/passes/PASS-INDEX.md (inventory of existing named cluster PASSes)
- eco/passes/core/ACES.00–06.md (timestamp and dependency data)
- eco/passes/OG.00–02.md (timestamp and dependency data)

MUST NOT TOUCH:
- CANON.00, CANON.01, CANON.02 (sealed upon acceptance)
- Any existing PASS document content

---

[DRIFT REVERSAL]

Problem of record

On or before 2026-04-12T21:52:02Z, an agent (operating without explicit founder instruction)
wrote the following rule into eco's PASS-INDEX.md:

  "Do not create new numbered PASSes — use named cluster convention."

This rule was:
  - Never proposed as a governance decision
  - Never recorded in any passchangelog
  - Never reviewed or signed off by the eco founder or GC maintainer
  - Not traceable to any PASS decision record
  - A violation of ACES.01 Invariant #6 (No Drift) and ACES.01 Invariant #14 (No Scope Drift)

The rule was also incorrect as governance: the named cluster convention was introduced
as a complement to the numbered system (ACES.06 explicitly reserved 0100.00 for the
Execution Path using a numbered form), not a replacement for it. The agent's inference
that "named clusters are better, therefore no more numbers" was unauthorized extrapolation.

Formal reversal

The rule "Do not create new numbered PASSes — use named cluster convention" is hereby
declared:

  UNAUTHORIZED — produced by agent drift without governance authority
  REVERSED — no longer in effect as of the acceptance of this PASS
  SUPERSEDED — replaced by the CANON canonical identifier system declared in
               CANON.00, CANON.01, and CANON.02

The PASS-INDEX.md note is a historical artifact of the drift. It is not authoritative.
It SHOULD be updated to reference this PASS as the governing replacement.

Governed replacement

The governed replacement for the unauthorized rule is:
  All new PASSes MUST be assigned a canonical ID conforming to CANON.01 R-ID-1
  before or at the time of acceptance. Named cluster identifiers (CLUSTER.SEQ)
  remain valid and are the alias for the canonical ID. Both coexist: the number
  is canonical; the name is ergonomic.

---

[ECO: NAMESPACE DECLARATION]

Namespace prefix:   ECO
Owner:              eco ecosystem — Jess Ervin (jj-ervin)
Description:        Governance records for the eco AI governance platform and ecosystem.
Allocation authority: eco project maintainer — jj-ervin
Registry file:      passes/passes.registry.json
Layers file:        passes/layers.yaml
Namespace file:     passes/namespace.yaml
Canon version:      CANON.01
Created:            2026-06-20T00:00:00Z

Layer bands for ECO:

  0000–0999  authority
    Agent identity, conduct standards, global invariants, foundational governance.
    Cluster: ACES and its amendments.

  1000–1999  operational
    Executable asset governance, pipeline governance, runtime, events, operations,
    remediation. Clusters: OG, RT, EV, OPS, REM.

  2000–2999  domain
    Vertical and industry-specific governance; eco surface governance; cognitive
    and orchestration governance; design system governance; hardware governance.
    Clusters: CK, HELM, LENS, JAG, AI, TRX, CAPS, PKE, NEHI, LASSO, JAEGER,
    UI, UIH, EDGE, AGRI, AIRP, SUBP, ECOHW, GOALIE.

  3000–3999  platform
    Platform architecture, naming, licensing, graduation, release, DevX.
    Clusters: PLAT, ONS, LIC, GRAD, DEVX, REL.

  4000–4999  data-interop
    Schemas, data contracts, interoperability rules. Currently unallocated.

  9000–9999  reserved
    Future use, experimental ranges, emergency governance.

---

[GC: NAMESPACE DECLARATION]

Namespace prefix:   GC
Owner:              Governance Commons — Jess Ervin (jj-ervin)
Description:        Governance records for the Governance Commons portable standards ecosystem.
Allocation authority: GC project maintainer — jj-ervin
Registry file:      passes/passes.registry.json
Layers file:        passes/layers.yaml
Namespace file:     passes/namespace.yaml
Canon version:      CANON.01
Created:            2026-06-20T00:00:00Z

Layer bands for GC:

  0000–0999  authority
    GC charter, ecosystem invariants, agent authority constraints, core governance.
    Cluster: GC (ecosystem-level decisions).

  1000–1999  operational
    Agent protocol governance, multi-agent coordination standards.
    Clusters: APO, ATP.

  2000–2999  standards
    Portable governance standards published by GC for external adopters.
    Clusters: ONS, CANON.

  3000–3999  platform
    GC registry, release, distribution, SDK governance. Currently unallocated.

  9000–9999  reserved
    Future use, experimental ranges, emergency governance.

---

[ASSIGNMENT ALGORITHM]

The following rules govern how existing PASSes are assigned ECO: or GC: canonical IDs.
These rules apply to the initial migration and to all future assignments under CANON.

Rule A-1 — Layer band determines the thousands digit
  A PASS is assigned a canonical ID whose NNNN falls in the range declared for its
  layer in the namespace layers file. Authority PASSes get ECO:0001–0999;
  operational PASSes get ECO:1001–1999; domain PASSes get ECO:2001–2999; etc.

Rule A-2 — Within a band, cluster headers are assigned first
  The cluster header (CLUSTER.00) is assigned the lowest available number in the
  band before any sub-PASSes in that cluster are assigned.

Rule A-3 — Within a cluster, sub-PASSes are assigned in chronological order
  Sub-PASSes (CLUSTER.01, CLUSTER.02, etc.) are assigned the next sequential
  numbers after the cluster header, in order of their time.loc timestamp.
  A PASS with an earlier timestamp gets a lower NNNN.

Rule A-4 — Clusters are ordered by their cluster header timestamp
  When multiple clusters share a band, the cluster with the earliest .00 timestamp
  is assigned the lowest block of numbers within the band.

Rule A-5 — Legacy numbered PASSes that have been superseded by named PASSes
  receive no new canonical ID. Their legacy form (e.g., 000.01) becomes a
  legacy_id in the superseding named PASS's registry entry.
  Determination: if a named PASS explicitly declares it "supersedes" a numbered
  PASS in its document, that numbered PASS is treated as superseded.

Rule A-6 — Legacy numbered PASSes that have NOT been superseded by named PASSes
  receive their own ECO: canonical IDs in the appropriate layer band, with their
  legacy numbered form in legacy_ids. The assignment follows Rules A-1 through A-4
  applied to their document content and timestamp.

Rule A-7 — Numbers are assigned sequentially with gaps permitted
  There is no requirement to fill every number in a band. Gaps are permitted and
  expected. Reservations (CANON.01 range reservation mechanism) are used to block
  ranges for known future clusters.

Rule A-8 — 2100.00 and 2200.00
  These non-sequential legacy PASSes (outside the 0001–0167 range) are assigned
  ECO: IDs in the follow-on implementation task. They are noted here as requiring
  review to determine their layer placement.

---

[LEGACY ID MAPPING RULES]

When a named PASS supersedes a legacy numbered PASS, the legacy form becomes a
legacy_id in the named PASS's registry entry.

  Example:
    ACES.01 supersedes PASS 000.01.
    ECO:0002 (ACES.01) registry entry: legacy_ids: ["000.01"]

When a legacy numbered PASS has no named successor, its own legacy numbered form
becomes its own legacy_id in its new ECO: canonical ID entry.

  Example:
    PASS 0006.05 has no named successor.
    ECO:XXXX (assigned in follow-on task) registry entry: legacy_ids: ["0006.05"]

The legacy_id value is always the string form of the prior identifier exactly as
it appears in the document's PASS ID field.

Supersession determination

A named PASS supersedes a legacy numbered PASS if and only if:
  (a) The named PASS's document explicitly states it supersedes the numbered PASS, OR
  (b) The numbered PASS's document explicitly states it is superseded by the named PASS.

Supersession MUST NOT be inferred from content similarity alone. When in doubt,
treat the legacy PASS as unsuperseded (assign it its own ECO: ID) and note it as
a candidate for manual review.

---

[CONFLICT RESOLUTION RULES]

C-1 — Earlier timestamp wins
  When two PASSes compete for the same canonical ID (should not occur under strict
  sequential allocation, but may arise during migration), the PASS with the earlier
  time.loc timestamp takes the lower number. The other PASS takes the next available.

C-2 — Named PASS takes precedence over legacy numbered PASS
  When a named PASS and a legacy numbered PASS cover the same governance topic,
  the named PASS is treated as the canonical record. The legacy PASS receives
  superseded status with superseded_by pointing to the named PASS's canonical ID.

C-3 — Ambiguous supersession is resolved conservatively
  When it is unclear whether a legacy PASS is superseded by a named PASS,
  both receive their own canonical IDs. A note is added to both registry entries
  declaring the ambiguity and flagging for manual review.

C-4 — Alias collisions within a namespace are not permitted
  If two PASSes would receive the same alias string, the later PASS (by timestamp)
  takes a modified alias or is assigned an alias with a disambiguation suffix.
  The modification must be recorded in the migration PASS or its follow-on task notes.

---

[CANONICAL ID ASSIGNMENTS — GC: NAMESPACE]

The following assignments are made by this PASS and are immediately binding.

GC: standards band (2000–2999) — CANON cluster

  GC:2001  alias: CANON.00  title: Canonical PASS Identifier Standard — Cluster Header
           status: accepted  timestamp: 2026-06-20T00:00:00Z
           path: passes/canon/CANON.00.md
           layer: standards  cluster: CANON  parent: null
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: []  originating_pass: CANON.03

  GC:2002  alias: CANON.01  title: PASS Identifier Governance — Normative Specification
           status: accepted  timestamp: 2026-06-20T00:00:00Z
           path: passes/canon/CANON.01.md
           layer: standards  cluster: CANON  parent: GC:2001
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: [GC:2001]  originating_pass: CANON.03

  GC:2003  alias: CANON.02  title: Registry Governance — Normative Specification
           status: accepted  timestamp: 2026-06-20T00:00:00Z
           path: passes/canon/CANON.02.md
           layer: standards  cluster: CANON  parent: GC:2001
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: [GC:2001, GC:2002]  originating_pass: CANON.03

  GC:2004  alias: CANON.03  title: Migration Protocol — eco and GC First-Adopter
           status: accepted  timestamp: 2026-06-20T00:00:00Z
           path: passes/canon/CANON.03.md
           layer: standards  cluster: CANON  parent: GC:2001
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: [GC:2001, GC:2002, GC:2003]  originating_pass: CANON.03

GC: standards band (2000–2999) — ONS cluster

  GC:2005  alias: ONS.00  title: Ontic Namespace Structure — Canonical Naming Grammar
           status: accepted  timestamp: 2026-04-11T00:00:00Z
           path: passes/ons/ (in eco repo; GC reference)
           layer: standards  cluster: ONS  parent: null
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: []  originating_pass: CANON.03

  GC:2006  alias: ONS.01  title: ONS Lint Rule Catalog and Naming Enforcement
           status: accepted  timestamp: 2026-06-03T16:34:47Z
           path: passes/ons/ (in eco repo; GC reference)
           layer: standards  cluster: ONS  parent: GC:2005
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: [GC:2005]  originating_pass: CANON.03

  GC:2007  alias: ONS.02  title: ONS Python AST Naming Enforcement
           status: accepted  timestamp: 2026-06-04T03:42:30Z
           path: passes/ons/ (in eco repo; GC reference)
           layer: standards  cluster: ONS  parent: GC:2005
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: [GC:2005, GC:2006]  originating_pass: CANON.03

GC: authority band (0000–0999) — GC ecosystem charter

  GC:0001  alias: GC.00  title: Governance Commons Ecosystem Charter
           status: accepted  timestamp: 2026-06-05T00:00:00Z
           path: docs/charter.md
           layer: authority  cluster: GC  parent: null
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: []  originating_pass: CANON.03

GC: operational band (1000–1999) — agent protocol clusters

  GC:1001  alias: APO.00  title: Agent Project Orchestrator — Cluster Header
           status: accepted  timestamp: 2026-06-05T00:00:00Z
           path: agent-project-orchestrator/DEV-PATH.md (cluster header reference)
           layer: operational  cluster: APO  parent: null
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: []  originating_pass: CANON.03

  GC:1002  alias: ATP.00  title: Agent Team Protocol — Cluster Header
           status: accepted  timestamp: 2026-06-05T00:00:00Z
           path: agent-team-protocol/
           layer: operational  cluster: ATP  parent: null
           legacy_ids: []  supersedes: []  superseded_by: null
           depends_on: []  originating_pass: CANON.03

---

[CANONICAL ID ASSIGNMENTS — ECO: NAMESPACE]

The following assignments are made by this PASS and are immediately binding.

ECO: authority band (0000–0999) — ACES cluster

  ECO:0001  alias: ACES.00  title: ACES Cluster Header
            status: sealed  timestamp: 2026-03-29T00:33:46Z
            path: passes/core/ACES.00.md
            layer: authority  cluster: ACES  parent: null
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: []  originating_pass: CANON.03

  ECO:0002  alias: ACES.01  title: Global Invariants (16)
            status: sealed  timestamp: 2026-03-29T00:46:53Z
            path: passes/core/ACES.01.md
            layer: authority  cluster: ACES  parent: ECO:0001
            legacy_ids: ["000.01"]
            supersedes: []  superseded_by: null
            depends_on: [ECO:0001]  originating_pass: CANON.03

  ECO:0003  alias: ACES.02  title: Construction Interface Specification
            status: sealed  timestamp: 2026-03-29T00:58:49Z
            path: passes/core/ACES.02.md
            layer: authority  cluster: ACES  parent: ECO:0001
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0001, ECO:0002]  originating_pass: CANON.03

  ECO:0004  alias: ACES.03  title: Role and Context Filter
            status: sealed  timestamp: 2026-03-29T02:04:01Z
            path: passes/core/ACES.03.md
            layer: authority  cluster: ACES  parent: ECO:0001
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0001, ECO:0002, ECO:0003]  originating_pass: CANON.03

  ECO:0005  alias: ACES.04  title: Agent Onboarding Protocol
            status: sealed  timestamp: 2026-03-29T02:11:35Z
            path: passes/core/ACES.04.md
            layer: authority  cluster: ACES  parent: ECO:0001
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0001, ECO:0002, ECO:0003, ECO:0004]  originating_pass: CANON.03

  ECO:0006  alias: ACES.05  title: Modularity and Licensing Boundary
            status: sealed  timestamp: 2026-03-29T02:20:25Z
            path: passes/core/ACES.05.md
            layer: authority  cluster: ACES  parent: ECO:0001
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0001, ECO:0002, ECO:0003, ECO:0004, ECO:0005]
            originating_pass: CANON.03

  ECO:0007  alias: ACES.06  title: ACES-1.0 Sealing and Forward References
            status: sealed  timestamp: 2026-03-29T04:23:12Z
            path: passes/core/ACES.06.md
            layer: authority  cluster: ACES  parent: ECO:0001
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0001, ECO:0002, ECO:0003, ECO:0004, ECO:0005, ECO:0006]
            originating_pass: CANON.03

ECO: operational band (1000–1999) — OG, RT, EV, OPS, REM clusters

  ECO:1001  alias: OG.00  title: Operational Governance — Cluster Header
            status: sealed  timestamp: 2026-03-29T05:28:06Z
            path: passes/OG.00.md
            layer: operational  cluster: OG  parent: null
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0007]  originating_pass: CANON.03

  ECO:1002  alias: OG.01  title: Compound Pass Specification
            status: sealed  timestamp: 2026-03-29T05:42:44Z
            path: passes/OG.01.md
            layer: operational  cluster: OG  parent: ECO:1001
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:1001]  originating_pass: CANON.03

  ECO:1003  alias: OG.02  title: Pipeline Integration
            status: sealed  timestamp: 2026-03-29T05:49:43Z
            path: passes/OG.02.md
            layer: operational  cluster: OG  parent: ECO:1001
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:1001, ECO:1002]  originating_pass: CANON.03

  ECO:1004  alias: RT.00  title: Runtime Cluster Header
            status: accepted  timestamp: 2026-03-30T18:10:07Z
            path: passes/rt/RT.00.md
            layer: operational  cluster: RT  parent: null
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0002]  originating_pass: CANON.03

  ECO:1005  alias: EV.00  title: Event Cluster Header
            status: accepted  timestamp: 2026-03-30T18:10:07Z
            path: passes/EV.00.md
            layer: operational  cluster: EV  parent: null
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0002]  originating_pass: CANON.03

  ECO:1006  alias: OPS.00  title: Operations Cluster Header
            status: accepted  timestamp: 2026-03-30T18:10:07Z
            path: passes/OPS.00.md
            layer: operational  cluster: OPS  parent: null
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0002]  originating_pass: CANON.03

  ECO:1007  alias: REM.00  title: Remediation Cluster Header — Auto-Fix and Violation Memory
            status: accepted  timestamp: 2026-06-04T01:47:57Z
            path: passes/rem/REM.00.md
            layer: operational  cluster: REM  parent: null
            legacy_ids: []  supersedes: []  superseded_by: null
            depends_on: [ECO:0002, ECO:1001]  originating_pass: CANON.03

---

[FOLLOW-ON IMPLEMENTATION TASK]

The assignments declared above cover the CANON, ONS, ACES, OG, RT, EV, OPS, and REM
clusters. Approximately 150+ additional PASSes in the eco namespace require canonical
ID assignment. These are governed by the rules declared in this PASS and are delegated
to a follow-on implementation task.

Scope of follow-on task

  ECO: domain band (2000–2999) — to be assigned:
    JAG.00, AI.00, AI.01, TRX.00, CAPS.00, GRAD.01, PKE.00,
    CK.00–02, HELM.00–02, LENS.00–01,
    NEHI.00–01, LASSO.00–03, JAEGER.00,
    UI.00–02, UIH.00–03,
    EDGE.00–15, AGRI.00–03, AIRP.00–01, SUBP.00–01, ECOHW.00,
    GOALIE cluster (if any PASSes exist)

  ECO: platform band (3000–3999) — to be assigned:
    PLAT.00–03, ONS.00–02 (eco copies), LIC.00, GRAD.01,
    DEVX.00, REL.00, REL-EDGE.00

  ECO: legacy numbered PASSes — to be assigned:
    000.01 through 000.34 (unsuperseded ones)
    0001.00 through 0167.xx (unsuperseded ones)
    2100.00, 2200.00 (require layer review)

Governing rules for follow-on task

  1. Apply Rules A-1 through A-8 from [ASSIGNMENT ALGORITHM]
  2. Apply legacy ID mapping rules from [LEGACY ID MAPPING RULES]
  3. Apply conflict resolution rules from [CONFLICT RESOLUTION RULES]
  4. Each assignment block must be recorded as a PASS decision (or a sub-PASS of a
     migration continuation PASS) and must produce corresponding registry entries
     and changelog entries per CANON.02
  5. The allocation authority for ECO: (jj-ervin) must authorize each assignment block

The follow-on task is not blocked on any further governance approval. The rules
declared in this PASS are sufficient to execute the remaining migration.

---

[BOOTSTRAP RESOLUTION]

CANON.00 acknowledged the bootstrap condition: the CANON cluster could not have
canonical IDs until CANON.03 existed. This PASS resolves that condition.

As of acceptance of this PASS:
  CANON.00 → GC:2001 (ACCEPTED)
  CANON.01 → GC:2002 (ACCEPTED)
  CANON.02 → GC:2003 (ACCEPTED)
  CANON.03 → GC:2004 (ACCEPTED, self-assigned — the bootstrap resolution)

The self-assignment of GC:2004 to CANON.03 is the intentional resolution of the
bootstrap: this PASS assigns its own canonical ID in the same action that establishes
the assignment authority. This is the one permitted case of self-referential assignment.
It is documented here so any future audit can confirm it was deliberate and authorized.

After this PASS is accepted, the originating_pass field for GC:2001–GC:2004 in the
registry is "CANON.03" (named form, accepted during bootstrap). Once GC:2004 is written
to the registry, future references may use the canonical form GC:2004.

---

[COMPANION ARTIFACTS]

This PASS produces the following files:

ECO: namespace
  eco/passes/namespace.yaml        — ECO: namespace declaration
  eco/passes/layers.yaml           — ECO: layer band assignments
  eco/passes/passes.registry.json  — initial ECO: registry (ACES + OG + RT/EV/OPS/REM)
  eco/passes/passes.registry.changelog.jsonl  — initial changelog

GC: namespace
  governance-commons/passes/namespace.yaml        — GC: namespace declaration
  governance-commons/passes/layers.yaml           — GC: layer band assignments
  governance-commons/passes/passes.registry.json  — initial GC: registry (CANON + ONS + GC + APO + ATP)
  governance-commons/passes/passes.registry.changelog.jsonl  — initial changelog

eco/passes/PASS-INDEX.md
  Should be updated to note that canonical IDs are now assigned and to reference
  CANON.03 as the governing migration PASS. The unauthorized "no numbered passes"
  note should be replaced with a reference to CANON.03.

---

[REASONING — 5 QUESTIONS]

1. Why does this PASS assign its own canonical ID (GC:2004)?
   The bootstrap condition is a genuine governance problem: no canonical ID exists until
   this PASS assigns one, but the PASS itself needs a canonical ID. The resolution is
   self-assignment, explicitly authorized and documented. This is preferable to leaving
   CANON.03 in the named-form-only state permanently (which would mean the migration
   PASS that established the ID system was itself unindexed), and preferable to waiting
   for a CANON.04 that does nothing except assign an ID to CANON.03.

2. Why assign only ACES, OG, RT/EV/OPS, REM, CANON, ONS, GC, APO, and ATP here rather
   than all PASSes?
   A complete assignment of 150+ PASSes in a single governance PASS would produce an
   unwieldy document and increase the risk of assignment errors. The foundational clusters
   (ACES, OG) are assigned here because they are the highest-dependency PASSes in the
   ecosystem — every other PASS depends on them. Assigning them correctly first lets the
   follow-on task reference them in depends_on without using named forms. The remaining
   clusters are governed by clear rules that an authorized agent can execute without
   additional governance decisions.

3. Why are the drift reversal and the migration in the same PASS?
   The drift reversal and the migration are causally linked: the drift created the
   condition (no canonical IDs for named PASSes) that the migration resolves. Separating
   them would require referencing a prior PASS for the reversal and a later PASS for the
   fix — which is circular in this case because the fix IS the reversal. Combining them
   in the final CANON PASS creates a single authoritative record that says: the unauthorized
   rule is gone, and here is the governed replacement in full.

4. Why are ECO: and GC: declared in the same PASS rather than separate migration PASSes?
   Both namespaces need to be established together because they are interdependent:
   GC:2001–GC:2004 (CANON cluster) are the governance authority for the ECO: migration.
   The ECO: registry entries reference GC: canonical IDs in their originating_pass field.
   Establishing both in the same PASS ensures there are no circular reference gaps
   between the two namespaces at the moment of first registry write.

5. Why is the follow-on task governed by rules declared here rather than by a future PASS?
   A future PASS for each remaining cluster would be correct governance but prohibitively
   expensive — it would require 10+ PASSes to complete the migration. The assignment
   algorithm (Rules A-1 through A-8) is deterministic given the existing PASS documents.
   An authorized agent can execute the algorithm without further governance decisions.
   The only governance gate is allocation authority: the eco maintainer must authorize
   each assignment block, and that authorization is recorded in the registry's
   originating_pass field referencing the migration continuation artifact.

---

[OUTPUTS]
- PASS CANON.03 accepted as the Migration Protocol for eco and GC first-adopter
- Drift reversal: unauthorized named-cluster-only rule formally reversed and superseded
- ECO: namespace declared: allocation authority, layer bands (5 active + reserved)
- GC: namespace declared: allocation authority, layer bands (4 active + reserved)
- Assignment algorithm declared: 8 rules (A-1 through A-8)
- Legacy ID mapping rules declared
- Conflict resolution rules declared: 4 rules (C-1 through C-4)
- CANON cluster canonical IDs assigned: GC:2001–GC:2004
- ONS cluster canonical IDs assigned: GC:2005–GC:2007
- GC ecosystem charter assigned: GC:0001
- APO, ATP cluster headers assigned: GC:1001–GC:1002
- ACES cluster canonical IDs assigned: ECO:0001–ECO:0007
- OG cluster canonical IDs assigned: ECO:1001–ECO:1003
- RT, EV, OPS, REM cluster headers assigned: ECO:1004–ECO:1007
- Bootstrap condition resolved: CANON.03 = GC:2004
- Follow-on implementation task declared and governed
- Companion artifacts produced: namespace.yaml, layers.yaml, passes.registry.json,
  passes.registry.changelog.jsonl for both ECO: and GC: namespaces

[DELTA SUMMARY]
- Drift reversal: documented unauthorized rule origin (agent, no governance record,
  ACES.01 Inv#6 and Inv#14 violated), declared rule reversed and superseded, declared
  governed replacement (canonical IDs required at acceptance; names are aliases)
- ECO: namespace: prefix ECO, owner jj-ervin, 5 active layer bands plus reserved,
  companion files at eco/passes/
- GC: namespace: prefix GC, owner jj-ervin, 4 active layer bands plus reserved,
  companion files at governance-commons/passes/
- Assignment algorithm: 8 rules covering layer-band mapping, chronological ordering,
  cluster-header priority, legacy supersession determination, and gap permission
- 8 rules: A-1 (layer band = NNNN thousands digit), A-2 (headers first), A-3
  (sub-PASSes chronological), A-4 (clusters ordered by header timestamp), A-5
  (superseded legacy → legacy_id), A-6 (unsuperseded legacy → own ECO: ID),
  A-7 (gaps permitted), A-8 (2100.00/2200.00 require review)
- 4 conflict resolution rules: C-1 (timestamp wins), C-2 (named over numbered),
  C-3 (ambiguous → conservative, two IDs + review note), C-4 (alias collision
  → disambiguation suffix)
- GC: assignments: GC:0001 (GC.00), GC:1001-1002 (APO.00, ATP.00),
  GC:2001-2004 (CANON.00-03), GC:2005-2007 (ONS.00-02)
- ECO: assignments: ECO:0001-0007 (ACES.00-06), ECO:1001-1003 (OG.00-02),
  ECO:1004-1007 (RT.00, EV.00, OPS.00, REM.00)
- Bootstrap resolved: GC:2004 = CANON.03 (self-assigned, explicitly authorized)
- Follow-on task: ~150+ remaining eco PASSes; governed by A-1 through A-8 and
  legacy ID mapping rules; requires allocation authority authorization per block;
  no additional governance PASS required

[CONSTRAINT VALIDATION]
- CANON-CI-1 (immutable): all assignments above are permanent; GC:2004 self-assignment
  is the bootstrap exception and is explicitly documented
- CANON-CI-7 (legacy IDs preserved): ACES.01 (ECO:0002) carries legacy_id "000.01";
  all future assignments carry legacy_ids per the legacy ID mapping rules
- CANON-CI-8 (migration governed): this PASS IS the migration governance record;
  R-AA-1 satisfied for all assignments above (originating_pass = CANON.03)
- Drift reversal is a FIX-type governance action: problem of record documented,
  rule reversed, governed replacement installed; ACES.01 Inv#6 and Inv#14 compliance
  restored
- Does not assign remaining eco PASSes: confirmed; follow-on task declared with
  governing rules; no additional PASS required for follow-on execution
- Does not modify any PASS content: confirmed; assignments are registry metadata only

[REVERSIBILITY]
Reversing CANON.03 would require:
- A new CANON amendment PASS that supersedes this PASS
- A declaration of what happens to canonical IDs already assigned (GC:0001–GC:2004,
  ECO:0001–ECO:1007) — these IDs are immutable; reversal cannot unassign them
- A declaration of what replaces the drift reversal (i.e., whether the unauthorized
  named-cluster-only rule would be reinstated — which would require ACES.01 Inv#6
  compliance)
In practice, CANON.03 is irreversible in its core effect: the canonical IDs assigned
here are permanent. The drift reversal is also irreversible: the unauthorized rule
cannot be reinstated without producing a new governance violation.

[HANDOFF]

next_action: Write companion artifacts
  1. eco/passes/namespace.yaml
  2. eco/passes/layers.yaml
  3. eco/passes/passes.registry.json (ACES + OG + RT/EV/OPS/REM entries)
  4. eco/passes/passes.registry.changelog.jsonl (initial write entries)
  5. governance-commons/passes/namespace.yaml
  6. governance-commons/passes/layers.yaml
  7. governance-commons/passes/passes.registry.json (CANON + ONS + GC + APO/ATP entries)
  8. governance-commons/passes/passes.registry.changelog.jsonl (initial write entries)

next_action_after_artifacts: Update eco/passes/PASS-INDEX.md
  Add canonical ID column to existing PASS-INDEX tables.
  Replace unauthorized "no numbered passes" note with reference to CANON.03 and GC:2004.

next_action_after_pass_index: Execute follow-on migration task
  Assign ECO: canonical IDs to remaining domain, platform, and legacy PASSes.
  Follow Rules A-1 through A-8. Record each assignment block as an authorized registry
  write with originating_pass referencing a follow-on migration artifact.

[FINALIZATION]
PASS CANON.03 is ACCEPTED as the Migration Protocol for eco and GC first-adopter.
The CANON cluster is complete. CANON.00–CANON.03 are accepted and assigned canonical IDs.
The ECO: and GC: namespaces are declared and their initial canonical ID assignments are binding.
The bootstrap condition declared in CANON.00 is resolved.
The unauthorized named-cluster-only rule is formally reversed and superseded by the
CANON canonical identifier system.
