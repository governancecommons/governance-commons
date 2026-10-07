"""Validate umbrella pins against immutable component compatibility artifacts.

This command checks evidence and never edits manifests, publishes, or activates RFCs.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SPECS = {"agent-dossier", "agent-matrix", "ons"}


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args],
        text=True,
        encoding="utf-8",
        stderr=subprocess.PIPE,
    ).strip()


def version(value: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value):
        raise ValueError(f"invalid release version: {value!r}")
    return tuple(map(int, value.split(".")))


def check_compatibility(manifest: dict, matrix: dict) -> list[str]:
    """Check only specification pins; runtime observations do not determine releases."""
    errors = []
    pins = {}
    for entry in manifest.get("specs", []):
        name = entry["spec"]
        if name not in SPECS:
            # The immutable historical train included APO as a spec.
            if (
                name == "agent-project-orchestrator"
                and manifest.get("release_id") == "GC-v1.2.0"
            ):
                continue
            errors.append(
                f"{name}: reference tooling/runtime cannot be a specification pin"
            )
            continue
        if name in pins:
            errors.append(f"duplicate specification pin: {name}")
        pins[name] = entry
        pin = entry.get("pinned_version")
        if pin is None:
            errors.append(
                f"{name}: exact pinned_version required for compatibility verification"
            )
        elif version(pin) < version(entry["min_version"]):
            errors.append(f"{name}: pinned_version is below min_version")
        if entry["compat_status"] != "ok":
            errors.append(f"{name}: compatibility hold remains")
    if set(pins) != SPECS:
        errors.append(
            "release must name Agent Dossier, Agent Matrix, and ONS exactly once"
        )
        return errors
    if manifest.get("compat_hold_items"):
        errors.append("release has unresolved compat_hold_items")
    if any(not p.get("pinned_version") for p in pins.values()):
        return errors

    rows = matrix["versioning"].get("normative_compatibility")
    if not rows:
        errors.append("Matrix source lacks RFC-0001 normative_compatibility data")
        return errors
    selected = [
        r for r in rows if r["matrix_version"] == pins["agent-matrix"]["pinned_version"]
    ]
    if len(selected) != 1:
        errors.append(
            "Matrix pin must resolve to exactly one normative compatibility row"
        )
        return errors
    row = selected[0]
    if row["status"] not in {"current", "supported"}:
        errors.append("Matrix normative row is not current or supported")
    alignment = row.get("dossier_specification_alignment")
    if alignment != pins["agent-dossier"]["pinned_version"]:
        errors.append(
            f"Dossier pin {pins['agent-dossier']['pinned_version']} "
            f"differs from Matrix declared alignment {alignment}; "
            "coordinated compatibility evidence required"
        )
    return errors


def validate_release(manifest_path: Path, components: Path, matrix_ref: str) -> dict:
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    schema = json.loads(
        (ROOT / "schemas/gc-release-manifest.schema.json").read_text(encoding="utf-8")
    )
    errors = [
        f"manifest schema: {e.message}"
        for e in Draft202012Validator(schema).iter_errors(manifest)
    ]
    evidence = {}
    try:
        matrix_commit = git(
            components / "agent-matrix", "rev-parse", f"{matrix_ref}^{{commit}}"
        )
        matrix = yaml.safe_load(
            git(
                components / "agent-matrix",
                "show",
                f"{matrix_commit}:agent-matrix.yaml",
            )
        )
        evidence["compatibility_source"] = {
            "repo": "governancecommons/agent-matrix",
            "commit": matrix_commit,
            "path": "agent-matrix.yaml",
            "section": "versioning.normative_compatibility",
        }
        # Compatibility checks still run when historical schema defects exist.
        errors.extend(check_compatibility(manifest, matrix))
        for entry in manifest["specs"]:
            name = entry["spec"]
            if name not in SPECS:
                continue
            if entry["repo"] != f"governancecommons/{name}":
                errors.append(f"{name}: unexpected repository identity")
                continue
            pin = entry.get("pinned_version")
            if not pin:
                continue
            version(pin)
            tag = f"v{pin}"
            commit = git(components / name, "rev-parse", f"refs/tags/{tag}^{{commit}}")
            evidence[name] = {"repo": entry["repo"], "tag": tag, "commit": commit}
        if "agent-dossier" in evidence:
            dossier = evidence["agent-dossier"]
            row = next(
                (
                    r
                    for r in matrix["versioning"].get("normative_compatibility", [])
                    if r["matrix_version"]
                    == next(
                        e["pinned_version"]
                        for e in manifest["specs"]
                        if e["spec"] == "agent-matrix"
                    )
                ),
                None,
            )
            if row and row.get("min_dossier_schema_version"):
                content = json.loads(
                    git(
                        components / "agent-dossier",
                        "show",
                        f"{dossier['commit']}:schemas/agent-dossier-instance.schema.json",
                    )
                )
                match = re.search(
                    r"/v/([0-9]+\.[0-9]+\.[0-9]+)/", content.get("$id", "")
                )
                if not match or version(match[1]) < version(
                    row["min_dossier_schema_version"]
                ):
                    errors.append(
                        "Dossier release schema identity is below "
                        "Matrix's schema minimum"
                    )
    except (
        subprocess.CalledProcessError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        StopIteration,
    ) as exc:
        errors.append(f"component evidence unavailable or malformed: {exc}")
    return {
        "release_id": manifest.get("release_id"),
        "passed": not errors,
        "errors": errors,
        "evidence": evidence,
        "limits": [
            "Git tags prove source availability, not package publication or adoption.",
            "ONS pin availability is checked; "
            "no undeclared ONS compatibility is inferred.",
            "Runtime/tooling versions do not decide specification compatibility.",
            "Validation does not activate RFC-0001 or mark a release ready.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--components", type=Path, default=ROOT)
    parser.add_argument(
        "--matrix-ref",
        default="HEAD",
        help="Compatibility source commit/ref; report records resolved SHA",
    )
    args = parser.parse_args()
    report = validate_release(args.manifest, args.components, args.matrix_ref)
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
