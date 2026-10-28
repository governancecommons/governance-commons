"""Reproduce the synthetic signed-evidence fixture without private keys."""
from __future__ import annotations

import argparse
import base64
import copy
import json
from pathlib import Path
import tempfile

from trusted_evidence import HostEvidenceVerifier, ReplayLedger
from zta_evaluator import canonical, digest

BASE = Path(__file__).resolve().parents[1]
REPORTS = BASE / "reports"


def run_demo() -> dict:
    roots = json.loads((REPORTS / "evidence-001-demo-root.json").read_text(encoding="utf-8"))
    package = json.loads((REPORTS / "evidence-001-demo-package.json").read_text(encoding="utf-8"))
    catalog = json.loads((BASE / "catalogs" / "gc-audit.zta-controls.v1.draft.json").read_text(encoding="utf-8"))
    expected = package["expected"]
    if roots["provenance"] != "SYNTHETIC_TEST_ONLY_NOT_INDEPENDENT_AUTHORITY":
        raise ValueError("demo root provenance changed")
    with tempfile.TemporaryDirectory(prefix="gc-audit-evidence-demo-") as directory:
        ledger = ReplayLedger(Path(directory) / "receipts.sqlite")
        try:
            verifier = HostEvidenceVerifier(root_keys={roots["key_id"]: base64.b64decode(roots["public_key_b64"], validate=True)},
                                            replay_ledger=ledger)
            kwargs = dict(authority=package["authority"], envelopes=package["envelopes"], catalog=catalog,
                          target_id=expected["target_id"], revision=expected["revision"],
                          environment=expected["environment"],
                          expected_control_ids=set(expected["control_ids"]), as_of=expected["as_of"])
            accepted = verifier.verify(**kwargs)
            replay = verifier.verify(**kwargs)
            changed = copy.deepcopy(package["envelopes"])
            changed[0]["payload"]["observation"]["observed"] = "ALLOWED"
            tampered = verifier.verify(**{**kwargs, "envelopes": changed})
            wrong_target = verifier.verify(**{**kwargs, "target_id": "other-app"})
            missing = verifier.verify(**{**kwargs, "envelopes": []})
            substituted = HostEvidenceVerifier(root_keys={roots["key_id"]: bytes(32)}, replay_ledger=ledger).verify(**kwargs)
        finally:
            ledger.close()
    results = {"authenticated": accepted, "replay": replay, "tampered_observation": tampered,
               "wrong_target": wrong_target, "missing_evidence": missing, "substituted_root": substituted}
    if accepted["status"] != "AUTHENTICATED" or any(r["status"] != "REJECTED" for name, r in results.items() if name != "authenticated"):
        raise ValueError("demo verification outcome changed")
    if any(r["control_status"] != "UNVERIFIED" or r["host_authority"] != "CONFIGURED_ROOT_ONLY" for r in results.values()):
        raise ValueError("demo exceeded authority boundary")
    report = {"schema": "gc-audit.evidence-demo-result.v1", "root_digest": digest(roots),
              "package_digest": digest(package), "catalog_digest": digest(catalog),
              "as_of": expected["as_of"], "results": results,
              "limitations": ["synthetic self-signed root is test-only and is not independent host authority",
                              "replay ledger is disposable for this reproducible demonstration",
                              "authenticated producer signature does not establish observation truth or ZTA control PASS"]}
    report["report_digest"] = digest(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    expected = run_demo()
    if args.verify:
        supplied = json.loads(args.verify.read_text(encoding="utf-8"))
        if supplied != expected:
            raise SystemExit("demo report mismatch")
    if args.output:
        args.output.write_bytes(canonical(expected) + b"\n")
    print(json.dumps({"status": "DEMO_VERIFIED", "report_digest": expected["report_digest"],
                      "outcomes": {name: r["status"] for name, r in expected["results"].items()}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
