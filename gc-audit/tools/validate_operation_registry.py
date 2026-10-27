"""Read-only semantic self-audit of the GC-AUDIT operation allowlist.

This is a static contract validator, not an execution sandbox. Repository-owned
policy must be separately pinned/reviewed before production use.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path, PureWindowsPath
import re
import sys
import yaml

class RegistryError(ValueError):
    pass

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str) or key in result:
            raise RegistryError("duplicate or non-string YAML mapping key")
        result[key] = loader.construct_object(value_node, deep=True)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
ROOT_NAME = "governance-commons"
SAFE_SCRIPT = re.compile(r"^governance-commons/gc-audit/tools/[A-Za-z0-9_-]+[.]ps1$")
# Conservatively reject direct shell spawning/evaluation in registered scripts.
# This is a source-level alarm, not proof of runtime confinement.
DIRECT_SHELL = re.compile(
    r'(?im)^\s*(?:Invoke-Expression\b|iex\b|Start-Process\s+[\x27"]?(?:pwsh|powershell|cmd|bash|sh)\b|&\s+[\x27"]?(?:pwsh|powershell|cmd|bash|sh)\b)'
)
INDIRECT_PROCESS = re.compile(r"(?im)^\\s*(?:return\\s+)?&\\s+\\$[A-Za-z_][A-Za-z0-9_]*\\s+@?[A-Za-z_\\$]")
WRITE_SWITCH = re.compile(r"\[switch\]\s*\$(?:Fix\w*|Apply\w*|Write\w*|Repair\w*)\b", re.I)

def contained_script(path, portfolio_root):
    if not isinstance(path, str) or not SAFE_SCRIPT.fullmatch(path):
        raise RegistryError("nonallowlisted script path")
    if "\\" in path or ":" in path or PureWindowsPath(path).is_absolute():
        raise RegistryError("platform-specific script path escape")
    root = portfolio_root.resolve(strict=True)
    candidate = root.joinpath(*path.split("/"))
    try:
        physical = candidate.resolve(strict=True)
        physical.relative_to((root / ROOT_NAME / 'gc-audit' / 'tools').resolve(strict=True))
    except (ValueError, OSError) as exc:
        raise RegistryError("script unavailable or escapes containment root") from exc
    if not physical.is_file():
        raise RegistryError("script is not a file")
    return physical

def validate_registry(registry_text, portfolio_root):
    try:
        registry = yaml.load(registry_text, Loader=UniqueLoader)
    except yaml.YAMLError as exc:
        raise RegistryError("malformed registry YAML") from exc
    if not isinstance(registry, dict) or registry.get("schema") != "gc-audit.registry.v1":
        raise RegistryError("unsupported registry authority")
    sec = registry.get("security")
    if not isinstance(sec, dict) or sec.get("execution_model") != "allowlist" or sec.get("shell") != "forbidden":
        raise RegistryError("unsafe registry security declaration")
    if not isinstance(registry.get("tools"), list):
        raise RegistryError("missing operation allowlist")
    ids, scripts, internal = set(), set(), set()
    delegation_findings = []
    for item in sec.get("internalScripts", []):
        if not isinstance(item, dict) or item.get("internal") is not True:
            raise RegistryError("invalid internal script exemption")
        path = item.get("script")
        physical = contained_script(path, portfolio_root)
        if physical in internal:
            raise RegistryError("duplicate internal exemption")
        internal.add(physical)
    for op in registry["tools"]:
        if not isinstance(op, dict) or not isinstance(op.get("id"), str) or op["id"] in ids:
            raise RegistryError("duplicate or malformed operation ID")
        ids.add(op["id"])
        steps = op.get("steps")
        if not isinstance(steps, list):
            raise RegistryError("missing operation steps")
        if op.get("status") == "planned":
            if steps:
                raise RegistryError("planned operation is executable")
            continue
        if op.get("status") != "active" or not steps:
            raise RegistryError("unknown status or empty active operation")
        mutable = op.get("mutates")
        if type(mutable) is not bool:
            raise RegistryError("missing mutation contract")
        if mutable and op.get("requiresExplicitApply") is not True:
            raise RegistryError("mutating operation lacks explicit apply")
        for step in steps:
            if not isinstance(step, dict):
                raise RegistryError("invalid executable step")
            physical = contained_script(step.get("script"), portfolio_root)
            if physical in internal:
                raise RegistryError("internal helper exposed as operation")
            scripts.add(physical)
            code = physical.read_text(encoding="utf-8-sig")
            if INDIRECT_PROCESS.search(code):
                delegation_findings.append(physical.name)
            if DIRECT_SHELL.search(code):
                raise RegistryError("direct shell spawning or expression evaluation requires explicit review")
            if not mutable and WRITE_SWITCH.search(code):
                raise RegistryError("read-only operation exposes mutating switch")
            if mutable and not re.search(r"\[switch\]\s*\$Apply\b", code, re.I):
                raise RegistryError("mutating operation has no explicit -Apply")
    if not ids or not scripts:
        raise RegistryError("empty operation allowlist")
    return {"status":"REGISTRY_CONTRACT_VALID", "delegation_review":"REQUIRED" if delegation_findings else "NOT_DETECTED",
            "indirect_delegation_scripts":sorted(set(delegation_findings)),
            "operations":len(ids),"scripts":len(scripts)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--registry",type=Path,required=True)
    p.add_argument("--portfolio-root",type=Path,required=True)
    args=p.parse_args()
    try:
        outcome=validate_registry(args.registry.read_text(encoding="utf-8-sig"), args.portfolio_root)
    except (RegistryError, OSError, UnicodeError) as exc:
        print(json.dumps({"status":"FAIL","reason":str(exc)}))
        return 1
    print(json.dumps(outcome,sort_keys=True))
    return 0

if __name__=="__main__":
    sys.exit(main())
