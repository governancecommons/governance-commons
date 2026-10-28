"""Disposable same-principal host demonstration and offline report verification."""
from __future__ import annotations

import argparse
import base64
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from local_evidence_host import LocalEvidenceHost
from trusted_evidence import HostEvidenceVerifier, ReplayLedger
from zta_authenticated_packages import canonical_bytes
from zta_evaluator import canonical, digest

BASE = Path(__file__).resolve().parents[1]
CATALOG = json.loads((BASE / "catalogs" / "gc-audit.zta-controls.v1.draft.json").read_text(encoding="utf-8"))
AS_OF = "2026-10-28T12:00:00Z"


def _child(host: Path, pin: str, package: Path) -> dict:
    run = subprocess.run([sys.executable, __file__, "--child", str(host), pin, str(package)],
                         capture_output=True, text=True, check=True, timeout=60)
    return json.loads(run.stdout)


def demonstrate() -> dict:
    sys.path.insert(0, str(BASE / "tests" / "zta"))
    from test_local_evidence_host import LocalHostTests, public_key
    fixture = LocalHostTests()
    fixture.setUp()
    try:
        original_pin = digest(fixture.config)
        accepted = _child(fixture.host_dir, original_pin, fixture.package_path)
        replay = _child(fixture.host_dir, original_pin, fixture.package_path)
        tampered_package = copy.deepcopy(fixture.package)
        tampered_package["envelopes"][0]["payload"]["observation"]["observed_status"] = 200
        fixture.write_package(tampered_package)
        tampered = _child(fixture.host_dir, original_pin, fixture.package_path)
        fixture.write_package(fixture.package)
        substituted = copy.deepcopy(fixture.config)
        substituted["root_keys"][0]["public_key_b64"] = public_key(fixture.producer)
        fixture.write_private("config.json", substituted)
        replaced_config = _child(fixture.host_dir, original_pin, fixture.package_path)
        fixture.write_private("config.json", fixture.config)
        revoked = copy.deepcopy(fixture.config)
        revoked["revoked_policy_ids"] = ["local-host-pilot"]
        fixture.write_private("config.json", revoked)
        revoked_policy = _child(fixture.host_dir, digest(revoked), fixture.package_path)
        results = {"authenticated": accepted, "replay_after_restart": replay,
                   "tampered_observation": tampered, "replaced_configuration": replaced_config,
                   "revoked_policy": revoked_policy}
        if accepted["status"] != "AUTHENTICATED" or any(
                item["status"] != "REJECTED" for name, item in results.items() if name != "authenticated"):
            raise ValueError("host demonstration outcomes unexpected")
        if any(item["control_status"] != "UNVERIFIED" or
               item["host_authority"] != "CONFIGURED_ROOT_ONLY" for item in results.values()):
            raise ValueError("host demonstration exceeded authority boundary")
        report = {"schema": "gc-audit.local-host-demo.v1", "assessed_at": AS_OF,
                  "host_config": fixture.config, "signed_authority": fixture.policy,
                  "evidence_package": fixture.package, "catalog_digest": digest(CATALOG),
                  "results": results,
                  "provenance": {"host_principal": fixture.config["host_principal"],
                                 "target_revision": fixture.revision,
                                 "host_directory": str(fixture.host_dir),
                                 "ledger": "host-owned persistent SQLite file, reopened by each child process",
                                 "keys": "ephemeral synthetic keys; private material discarded"},
                  "limitations": ["host and target fixture ran under the same OS principal",
                                  "configuration pin was supplied by the demo harness, not an independent deployment source",
                                  "temporary host and target directories are removed after demonstration",
                                  "fixed assessment time and synthetic observations are test-only",
                                  "no ZTA control PASS or operational assurance"]}
        report["report_digest"] = digest(report)
        return report
    finally:
        fixture.doCleanups()


def verify_report(report: dict) -> None:
    claimed = report.get("report_digest")
    if claimed != digest({k: v for k, v in report.items() if k != "report_digest"}):
        raise ValueError("report digest mismatch")
    config, authority, package = report["host_config"], report["signed_authority"], report["evidence_package"]
    if digest(config) != report["results"]["authenticated"]["config_digest"]:
        raise ValueError("configuration provenance mismatch")
    if digest(authority) != config["policy_digest"] or digest(CATALOG) != config["catalog_digest"]:
        raise ValueError("policy or catalog provenance mismatch")
    root = config["root_keys"][0]
    Ed25519PublicKey.from_public_bytes(base64.b64decode(root["public_key_b64"], validate=True)).verify(
        base64.b64decode(authority["signature"], validate=True), canonical_bytes(authority["payload"]))
    with tempfile.TemporaryDirectory(prefix="gc-evidence-offline-") as directory:
        ledger = ReplayLedger(Path(directory) / "receipts.sqlite")
        try:
            offline = HostEvidenceVerifier(root_keys={root["key_id"]: base64.b64decode(root["public_key_b64"])},
                replay_ledger=ledger).verify(authority=authority, envelopes=package["envelopes"], catalog=CATALOG,
                target_id=config["target_id"], revision=config["revision"], environment=config["environment"],
                expected_control_ids=set(config["control_ids"]), as_of=report["assessed_at"])
            if offline["status"] != "AUTHENTICATED" or offline["control_status"] != "UNVERIFIED":
                raise ValueError("offline signature verification failed")
        finally:
            ledger.close()
    for name, item in report["results"].items():
        if item["receipt_digest"] != digest({k: v for k, v in item.items() if k != "receipt_digest"}):
            raise ValueError(f"{name} receipt digest mismatch")
        if item["control_status"] != "UNVERIFIED" or item["host_authority"] != "CONFIGURED_ROOT_ONLY":
            raise ValueError(f"{name} exceeded authority boundary")
    if report["results"]["authenticated"]["status"] != "AUTHENTICATED" or any(
            item["status"] != "REJECTED" for name, item in report["results"].items() if name != "authenticated"):
        raise ValueError("demonstration outcome mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    parser.add_argument("--child", nargs=3, metavar=("HOST_DIR", "PIN", "PACKAGE"))
    args = parser.parse_args()
    if args.child:
        host, pin, package = args.child
        print(json.dumps(LocalEvidenceHost(host, expected_config_digest=pin).verify(package, CATALOG, assessed_at=AS_OF)))
        return 0
    report = json.loads(args.verify.read_text(encoding="utf-8")) if args.verify else demonstrate()
    verify_report(report)
    if args.output:
        args.output.write_bytes(canonical(report) + b"\n")
    print(json.dumps({"status": "VERIFIED", "report_digest": report["report_digest"],
                      "outcomes": {name: item["status"] for name, item in report["results"].items()}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
