"""GC-AUDIT-ZTA-001C: conservative, read-only assessment evaluator.

No execution of target code; no network or filesystem writes. This module only
evaluates supplied, schema-valid JSON records. A machine-readable PASS requires
separately specified proof semantics: this baseline deliberately cannot emit PASS.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas" / "zta"
KINDS = ("controls", "profile", "target", "evidence", "result")
class AssessmentInputError(ValueError):
    """Invalid assessment data, not a security finding."""

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def digest(value):
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()

def validate(kind, value):
    if kind not in KINDS:
        raise AssessmentInputError("unsupported record kind")
    schema = json.loads((SCHEMA_DIR / f"gc-audit.zta-{kind}.v1.schema.json").read_text(encoding="utf-8"))
    error = next(iter(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value)), None)
    if error:
        raise AssessmentInputError(f"invalid {kind}: {error.message}")

def require_unique(values, key, description):
    ids = [v[key] for v in values]
    if len(set(ids)) != len(ids):
        raise AssessmentInputError(f"duplicate {description}")

def verify_evidence_bytes(evidence, source_bytes):
    """Verify exact content bytes, not identity or control sufficiency.

    One declared source reference per record is supported in this increment.
    Absent bytes or ambiguous/multiple references are rejected, never assumed valid.
    """
    validate("evidence", evidence)
    references = evidence["source_refs"]
    if len(references) != 1:
        raise AssessmentInputError("evidence must reference exactly one source for byte verification")
    reference = references[0]
    if reference not in source_bytes:
        raise AssessmentInputError("evidence source bytes not supplied")
    payload = source_bytes[reference]
    if not isinstance(payload, bytes):
        raise AssessmentInputError("evidence source payload must be bytes")
    measured = "sha256:" + hashlib.sha256(payload).hexdigest()
    if measured != evidence["source_digest"]:
        raise AssessmentInputError("evidence source digest mismatch")
    return {"evidence_id": evidence["evidence_id"], "source_ref": reference,
            "digest": measured, "integrity": "VERIFIED",
            "producer_identity": "UNVERIFIED", "control_sufficiency": "UNVERIFIED"}

def resolve_profile(profile, known_profiles):
    """Validate the entire inheritance DAG without silently dropping overrides."""
    profiles = {p["profile_id"]: p for p in known_profiles}
    profiles[profile["profile_id"]] = profile
    for p in profiles.values():
        validate("profile", p)
    ordered, visiting, visited = [], set(), set()
    def visit(pid):
        if pid in visiting:
            raise AssessmentInputError("profile inheritance cycle")
        if pid in visited:
            return
        if pid not in profiles:
            raise AssessmentInputError("missing inherited profile")
        visiting.add(pid)
        parent = profiles[pid]
        if parent["catalog_digest"] != profile["catalog_digest"]:
            raise AssessmentInputError("profile catalog mismatch")
        if parent["policy_version"] != profile["policy_version"]:
            raise AssessmentInputError("profile policy mismatch")
        for ancestor in parent["inherits"]:
            visit(ancestor)
        visiting.remove(pid)
        visited.add(pid)
        ordered.append(parent)
    visit(profile["profile_id"])
    mandatory = set()
    for p in ordered:
        mandatory.update(p["mandatory_control_ids"])
    return {"lineage": [p["profile_id"] for p in ordered],
            "mandatory_control_ids": sorted(mandatory)}

def evaluate(catalog, profile, target, evidence_records=(), *, as_of=None,
             evidence_sources=None, inherited_profiles=()):
    for kind, record in (("controls", catalog), ("profile", profile), ("target", target)):
        validate(kind, record)
    for evidence in evidence_records:
        validate("evidence", evidence)
    controls = catalog["controls"]
    require_unique(controls, "control_id", "control IDs")
    expected = {f"ZTA-{domain:02d}.0{number}" for domain in range(1, 13) for number in (1, 2)}
    if {c["control_id"] for c in controls} != expected:
        raise AssessmentInputError("catalog must contain exactly 24 approved controls")
    if profile["catalog_digest"] != digest(catalog):
        raise AssessmentInputError("profile catalog digest mismatch")
    if target["profile_id"] != profile["profile_id"]:
        raise AssessmentInputError("target/profile mismatch")
    resolved = resolve_profile(profile, inherited_profiles)
    known = {c["control_id"] for c in controls}
    for control_id in resolved["mandatory_control_ids"]:
        if control_id not in known:
            raise AssessmentInputError("unknown mandatory control")
    for r in profile["conditional_rules"] + profile["exclusion_rules"]:
        if r["control_id"] not in known:
            raise AssessmentInputError("unknown profile control")
    if profile["conditional_rules"] or profile["exclusion_rules"]:
        raise AssessmentInputError("conditional rules not yet executable; cannot safely evaluate")
    require_unique(target["resources"], "id", "resource IDs")
    require_unique(target["actors"], "id", "actor IDs")
    require_unique(target["components"], "id", "component IDs")
    require_unique(target["trust_boundaries"], "id", "trust boundary IDs")
    comp = {c["id"] for c in target["components"]}
    resource = {r["id"] for r in target["resources"]}
    for b in target["trust_boundaries"]:
        if b["source_component"] not in comp or b["destination_component"] not in comp or not set(b["resource_ids"]) <= resource:
            raise AssessmentInputError("invalid trust boundary reference")
    require_unique(target["control_responsibilities"], "control_id", "control responsibility IDs")
    for r in target["control_responsibilities"]:
        if r["control_id"] not in known or r["component_id"] not in comp:
            raise AssessmentInputError("invalid control responsibility reference")
    require_unique(evidence_records, "evidence_id", "evidence IDs")
    verified_evidence = []
    for e in evidence_records:
        if evidence_sources is not None:
            verified_evidence.append(verify_evidence_bytes(e, evidence_sources))
        if e["target_id"] != target["target_id"] or e["revision"] != target["revision"]:
            raise AssessmentInputError("cross-target or stale-revision evidence")
        if not set(e["control_ids"]) <= known:
            raise AssessmentInputError("evidence references unknown control")
        # SHA-256 strings alone do not prove source contents, identity or behavior.
        # The assessor must never promote such declarations to verified evidence.
    if as_of is not None:
        raise AssessmentInputError("freshness policy not implemented: cannot accept as_of")
    entries = [{"control_id":cid, "status":"UNVERIFIED",
                "reason":"proof sufficiency, applicability and evidence integrity not independently established",
                "evidence_ids":[]} for cid in sorted(known)]
    core = {"schema":"gc-audit.zta-result.v1","version":"1.0.0",
            "id":f"assessment-{target['id']}","target_id":target["target_id"],
            "revision":target["revision"],"profile_id":target["profile_id"],
            "catalog_digest":digest(catalog),"policy_version":profile["policy_version"],
            "control_results":entries,"findings":[],"assessment_state":"VALID",
            "release_eligibility":"BLOCKED"}
    core["normalized_digest"] = digest(core)
    validate("result", core)
    return core
