"""Offline, read-only repository pilot for the existing ZTA evaluator."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

from zta_evaluator import AssessmentInputError, canonical, digest, evaluate

CATALOG = Path(__file__).resolve().parents[1] / "catalogs" / "gc-audit.zta-controls.v1.draft.json"
PROFILE = "zta.library.v1"


def git(root: Path, *args: str) -> bytes:
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_NO_LAZY_FETCH="1")
    process = subprocess.run(["git", "-C", str(root), *args], env=env,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if process.returncode:
        raise AssessmentInputError(f"local git {args[0]} failed: {process.stderr.decode('utf-8', 'replace').strip()}")
    return process.stdout


def collect(root: Path) -> tuple[str, list[dict]]:
    if not root.is_dir() or root.resolve() != Path(os.fsdecode(git(root, "rev-parse", "--show-toplevel")).strip()).resolve():
        raise AssessmentInputError("target must be an existing Git repository root")
    if git(root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise AssessmentInputError("target working tree is not clean; exact revision assessment requires a clean tree")
    revision = git(root, "rev-parse", "HEAD").decode("ascii").strip()
    entries = []
    for row in git(root, "ls-tree", "-r", "-z", "HEAD").split(b"\0"):
        if not row:
            continue
        metadata, name = row.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split()
        if kind != "blob":
            raise AssessmentInputError("unsupported Git tree entry")
        entries.append({"path": name.decode("utf-8", "surrogateescape"),
                        "mode": mode, "git_blob_oid": oid})
    entries.sort(key=lambda e: e["path"])
    return revision, entries


def make_report(root: Path, target_id: str) -> dict:
    revision, entries = collect(root)
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    profile = {"schema": "gc-audit.zta-profile.v1", "version": "1.0.0",
               "id": "gc-audit-zta-library-pilot", "catalog_digest": digest(catalog),
               "profile_id": PROFILE, "inherits": [],
               "mandatory_control_ids": [c["control_id"] for c in catalog["controls"]],
               "conditional_rules": [], "exclusion_rules": [], "policy_version": "gc-audit-product-001-gate1"}
    manifest = {"method": "local git ls-tree -r HEAD; tracked blobs only",
                "revision": revision, "entries": entries}
    target = {"schema": "gc-audit.zta-target.v1", "version": "1.0.0",
              "id": target_id, "target_id": target_id, "revision": revision,
              "profile_id": PROFILE, "resources": [], "actors": [],
              "trust_boundaries": [], "components": [], "capabilities": [],
              "control_responsibilities": [], "evidence_manifest_digest": digest(manifest)}
    result = evaluate(catalog, profile, target)
    report = {"schema": "gc-audit.repository-report.v1", "version": "1.0.0",
              "target": target, "profile": profile, "catalog": catalog,
              "catalog_source": "gc-audit/catalogs/gc-audit.zta-controls.v1.draft.json",
              "manifest": manifest, "result": result,
              "verified_repository_facts": ["Git repository root resolved", "working tree clean",
                                            "HEAD revision resolved", "tracked blob inventory collected"],
              "limitations": ["Repository metadata and source inventory do not prove runtime ZTA controls.",
                              "No host-owned trust roots, signed control proof, production behavior, or deployment evidence supplied.",
                              "Git blob IDs bind tracked content; the manifest does not include untracked, ignored, submodule, or external files.",
                              "Report digest detects changes to this file; it is not a signature or independent authority."],
              "next_action": "Obtain independently authenticated, revision-bound control evidence and host authority before considering any PASS."}
    report["report_digest"] = digest(report)
    return report


def verify(report: dict, root: Path | None = None) -> None:
    if report.get("schema") != "gc-audit.repository-report.v1":
        raise AssessmentInputError("unsupported report schema")
    body = {k: v for k, v in report.items() if k != "report_digest"}
    if report.get("report_digest") != digest(body):
        raise AssessmentInputError("report digest mismatch")
    if report["target"]["evidence_manifest_digest"] != digest(report["manifest"]):
        raise AssessmentInputError("manifest digest mismatch")
    if report["profile"]["catalog_digest"] != digest(report["catalog"]):
        raise AssessmentInputError("catalog digest mismatch")
    if report["profile"]["profile_id"] != PROFILE:
        raise AssessmentInputError("unsupported profile")
    if report["result"] != evaluate(report["catalog"], report["profile"], report["target"]):
        raise AssessmentInputError("evaluator result mismatch")
    if root is not None:
        revision, entries = collect(root)
        if revision != report["target"]["revision"] or entries != report["manifest"]["entries"]:
            raise AssessmentInputError("local target does not match report")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    assess = sub.add_parser("assess", help="assess an explicitly authorized local Git root")
    assess.add_argument("--target", type=Path, required=True)
    assess.add_argument("--target-id", required=True)
    assess.add_argument("--profile", required=True, choices=[PROFILE])
    assess.add_argument("--authorize-local-read", action="store_true", required=True)
    assess.add_argument("--output", type=Path, required=True)
    check = sub.add_parser("verify", help="reopen and integrity-check an exported report")
    check.add_argument("--report", type=Path, required=True)
    check.add_argument("--target", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "assess":
            if not args.authorize_local_read:
                raise AssessmentInputError("explicit local read authorization required")
            root = args.target.resolve(strict=True)
            output = args.output.resolve()
            if output == root or root in output.parents:
                raise AssessmentInputError("output must be outside the assessed repository")
            report = make_report(root, args.target_id)
            verify(report, root)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(canonical(report) + b"\n")
            print(json.dumps({"status": "VALID", "report": str(output),
                              "digest": report["report_digest"], "revision": report["target"]["revision"]}))
        else:
            report = json.loads(args.report.read_text(encoding="utf-8"))
            verify(report, args.target.resolve(strict=True) if args.target else None)
            print(json.dumps({"status": "VALID", "digest": report["report_digest"]}))
        return 0
    except (AssessmentInputError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "EVALUATION_ERROR", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
