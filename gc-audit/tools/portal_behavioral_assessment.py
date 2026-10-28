"""Record a bounded Portal application test as local observations, never ZTA PASS."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from zta_cli import make_report, verify, canonical
from zta_evaluator import AssessmentInputError, digest

PROBE = Path(__file__).with_name("portal_behavioral_probe.mjs")
SOURCES = ("src/local-server.mjs", "src/auth/sqlite-auth-store.mjs",
           "src/auth/http-request-guards.mjs", "src/storage/editorial-store.mjs")
EXPECTED_IDS = {"http.anonymous.dashboard", "http.anonymous.import", "http.owner.dashboard",
                "http.disabled-membership.dashboard", "http.import.missing-csrf",
                "http.import.wrong-origin", "http.reviewer.import-denied",
                "http.revoked-session.dashboard", "store.author-cannot-review",
                "store.reviewer-cannot-approve", "store.independent-approver"}


def sha256(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def assess(root: Path) -> dict:
    report = make_report(root, "governance-commons-portal")
    source_entries = {entry["path"]: entry for entry in report["manifest"]["entries"]}
    if any(path not in source_entries for path in SOURCES):
        raise AssessmentInputError("required Portal implementation source is absent from exact Git revision")
    node = shutil.which("node")
    if not node:
        raise AssessmentInputError("Node.js 22 or later is required")
    env = {key: os.environ[key] for key in ("PATH", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT") if key in os.environ}
    try:
        run = subprocess.run([node, str(PROBE), str(root)], cwd=PROBE.parents[2], env=env,
                             capture_output=True, timeout=30, check=False)
    except subprocess.TimeoutExpired as exc:
        raise AssessmentInputError("isolated Portal probe timed out") from exc
    if run.returncode:
        raise AssessmentInputError("isolated Portal probe failed: " + run.stderr.decode("utf-8", "replace")[-2000:])
    try:
        payload = json.loads(run.stdout)
        rows = payload["observations"]
    except (ValueError, KeyError, TypeError) as exc:
        raise AssessmentInputError("invalid Portal probe output") from exc
    if payload.get("schema") != "gc-audit.portal-observations.v1" or not isinstance(rows, list):
        raise AssessmentInputError("unsupported Portal probe output")
    if {row.get("id") for row in rows} != EXPECTED_IDS or len(rows) != len(EXPECTED_IDS):
        raise AssessmentInputError("incomplete Portal observations")
    controls = {item["control_id"] for item in report["catalog"]["controls"]}
    if any(row.get("observed") != row.get("expected") or row.get("verification") != "LOCAL_ASSERTION"
           or not set(row.get("control_ids", [])) <= controls for row in rows):
        raise AssessmentInputError("failed or unsupported Portal observation")
    report["application_pilot"] = {
        "schema": "gc-audit.application-pilot.v1", "target_type": "application",
        "surface": "local loopback HTTP server and in-memory editorial store",
        "environment": payload["environment"],
        "method": "fixed Node.js probe against actual Portal request handlers and EditorialStore",
        "probe_source_sha256": sha256(PROBE.read_bytes()),
        "portal_sources": [{"path": path, "git_blob_oid": source_entries[path]["git_blob_oid"]} for path in SOURCES],
        "observation_digest": digest(rows), "observations": rows,
        "verification": "LOCAL_ASSERTION_ONLY", "authority": "UNVERIFIED",
        "network_scope": "127.0.0.1 only; no OAuth callback or external release fetch",
        "limitations": ["Synthetic local sessions are not production GitHub OAuth evidence.",
                        "Local HTTP and store assertions do not establish full control coverage or trusted host authority.",
                        "No deployed service, production database, keys, credentials, release or publication route was tested."]}
    report["limitations"].append("Application observations are local assertions; all ZTA controls remain UNVERIFIED.")
    report["report_digest"] = digest({k: v for k, v in report.items() if k != "report_digest"})
    verify(report, root)
    return report


def verify_pilot(report: dict, root: Path | None = None) -> None:
    verify(report, root)
    pilot = report.get("application_pilot")
    if not isinstance(pilot, dict) or pilot.get("schema") != "gc-audit.application-pilot.v1":
        raise AssessmentInputError("missing application pilot")
    rows = pilot.get("observations")
    if not isinstance(rows, list) or pilot.get("observation_digest") != digest(rows):
        raise AssessmentInputError("observation digest mismatch")
    if pilot.get("authority") != "UNVERIFIED" or any(item["status"] != "UNVERIFIED" for item in report["result"]["control_results"]):
        raise AssessmentInputError("local observations cannot authorize control PASS")
    if pilot.get("probe_source_sha256") != sha256(PROBE.read_bytes()):
        raise AssessmentInputError("probe source mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("assess")
    run.add_argument("--target", required=True, type=Path)
    run.add_argument("--authorize-local-test", action="store_true", required=True)
    run.add_argument("--output", required=True, type=Path)
    check = sub.add_parser("verify")
    check.add_argument("--report", required=True, type=Path)
    check.add_argument("--target", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "assess":
            root = args.target.resolve(strict=True)
            output = args.output.resolve()
            if output == root or root in output.parents:
                raise AssessmentInputError("output must be outside the assessed Portal repository")
            report = assess(root)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(canonical(report) + b"\n")
            print(json.dumps({"status": "VALID_LOCAL_TEST", "report": str(output),
                              "digest": report["report_digest"], "revision": report["target"]["revision"],
                              "observations": len(report["application_pilot"]["observations"])}))
        else:
            report = json.loads(args.report.read_text(encoding="utf-8"))
            verify_pilot(report, args.target.resolve(strict=True) if args.target else None)
            print(json.dumps({"status": "VALID_LOCAL_TEST", "digest": report["report_digest"]}))
        return 0
    except (AssessmentInputError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "EVALUATION_ERROR", "reason": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
