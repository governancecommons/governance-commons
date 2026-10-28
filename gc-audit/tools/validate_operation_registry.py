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
SAFE_SCRIPT = re.compile(r"^governance-commons/gc-audit/tools/[A-Za-z0-9_-]+[.]ps1$")
SAFE_ID = re.compile(r"^gc-audit\.[a-z][a-z0-9-]*$")
ROOT_FIELDS = {"schema", "authority", "updated", "description", "security", "categories", "tools", "docs"}
SECURITY_FIELDS = {"execution_model", "shell", "path_policy", "mutation_policy", "owner",
                   "evidenceBundles", "contracts", "playValidationProfiles", "internalScripts"}
OP_FIELDS = {"id", "verb", "category", "status", "title", "description", "mutates",
             "requiresExplicitApply", "previewContract", "machineReadableDiffRequired",
             "outputContract", "zeroTrust", "mode", "recordSchema", "activeProviders", "steps"}
STEP_FIELDS = {"script", "projectArg", "targetArg", "containmentArg", "requiresFile",
               "portfolioOnly", "supportsDryRun", "fixedArgs", "supportsHours",
               "supportsSummary", "supportsProfile", "profiles", "supportsStrict",
               "supportsFilePath", "supportsText", "supportsMode", "supportsPaths",
               "supportsProject", "supportsJson"}
AUTH_CLAIMS = {"normalization-apply", "schema-authority-change", "git-branch-or-remote-split"}
ARG_FIELDS = {"projectArg": "Project", "targetArg": "TargetPath",
              "containmentArg": "PortfolioRoot", "requiresFile": "PLAY.jsonl"}
# Conservatively reject direct shell spawning/evaluation in registered scripts.
# This is a source-level alarm, not proof of runtime confinement.
DIRECT_SHELL = re.compile(
    r'(?im)^\s*(?:Invoke-Expression\b|iex\b|Start-Process\s+[\x27"]?(?:pwsh|powershell|cmd|bash|sh)\b|&\s+[\x27"]?(?:pwsh|powershell|cmd|bash|sh)\b)'
)
INDIRECT_PROCESS = re.compile(r"(?im)^\s*(?:return\s+)?&\s+\$[A-Za-z_][A-Za-z0-9_]*\s+@?[A-Za-z_\$]")
COMPUTED_PROCESS = re.compile(r"(?im)^\s*(?:return\s+)?&\s*\(")
WRITE_COMMAND = re.compile(r"(?im)(?<![\w-])(?:Set-Content|Add-Content|Out-File|New-Item|Remove-Item|Copy-Item|Move-Item|Rename-Item)\b")
WRITE_SWITCH = re.compile(r"\[switch\]\s*\$(?:Fix\w*|Apply\w*|Write\w*|Repair\w*)\b", re.I)

def contained_script(path, portfolio_root, repo_root):
    if not isinstance(path, str) or not SAFE_SCRIPT.fullmatch(path):
        raise RegistryError("nonallowlisted script path")
    if "\\" in path or ":" in path or PureWindowsPath(path).is_absolute():
        raise RegistryError("platform-specific script path escape")
    root = portfolio_root.resolve(strict=True)
    try:
        repository = repo_root.resolve(strict=True)
        repository.relative_to(root)
        tools_root = repository / 'gc-audit' / 'tools'
        physical_tools = tools_root.resolve(strict=True)
        physical_tools.relative_to(repository)
        candidate = repository.joinpath(*path.split("/")[1:])
        physical = candidate.resolve(strict=True)
        physical.relative_to(physical_tools)
    except (ValueError, OSError) as exc:
        raise RegistryError("script unavailable or escapes containment root") from exc
    if not physical.is_file():
        raise RegistryError("script is not a file")
    return physical

def validate_registry(registry_text, portfolio_root, repo_root, *, require_self_audit=False,
                      require_runtime_assurance=False):
    try:
        registry = yaml.load(registry_text, Loader=UniqueLoader)
    except (yaml.YAMLError, RegistryError) as exc:
        raise RegistryError("malformed registry YAML") from exc
    if not isinstance(registry, dict) or registry.get("schema") != "gc-audit.registry.v1":
        raise RegistryError("unsupported registry authority")
    if set(registry) != ROOT_FIELDS or registry["authority"] != "DEV-ACCORD.05":
        raise RegistryError("missing or unknown registry authority field")
    sec = registry.get("security")
    if not isinstance(sec, dict) or sec.get("execution_model") != "allowlist" or sec.get("shell") != "forbidden":
        raise RegistryError("unsafe registry security declaration")
    if set(sec) != SECURITY_FIELDS or sec["owner"] != "GC-AUDIT":
        raise RegistryError("missing or unknown security authority field")
    if sec["path_policy"] != "scripts must resolve under the portfolio root":
        raise RegistryError("unsafe path policy")
    if not isinstance(sec["internalScripts"], list):
        raise RegistryError("invalid internal script list")
    if not isinstance(registry.get("tools"), list):
        raise RegistryError("missing operation allowlist")
    categories = registry["categories"]
    if not isinstance(categories, dict) or not categories or any(
            not isinstance(name, str) or not isinstance(value, dict) or
            set(value) != {"label", "description"} for name, value in categories.items()):
        raise RegistryError("missing category definitions")
    ids, scripts, internal = set(), set(), set()
    delegation_findings, write_findings = [], []
    self_audit_ready = set()
    for item in sec.get("internalScripts", []):
        if not isinstance(item, dict) or set(item) != {"script", "internal", "reason"} or item.get("internal") is not True or not isinstance(item.get("reason"), str) or not item["reason"].strip():
            raise RegistryError("invalid internal script exemption")
        path = item.get("script")
        physical = contained_script(path, portfolio_root, repo_root)
        if physical in internal:
            raise RegistryError("duplicate internal exemption")
        internal.add(physical)
    for op in registry["tools"]:
        if not isinstance(op, dict) or not set(op) <= OP_FIELDS or not isinstance(op.get("id"), str) or not SAFE_ID.fullmatch(op["id"]) or op["id"] in ids:
            raise RegistryError("duplicate or malformed operation ID")
        ids.add(op["id"])
        if (not isinstance(op.get("verb"), str) or not op["verb"].strip() or
                not isinstance(op.get("category"), str) or op["category"] not in categories):
            raise RegistryError("missing or unknown operation verb/category")
        steps = op.get("steps")
        if not isinstance(steps, list):
            raise RegistryError("missing operation steps")
        if op.get("status") == "planned":
            if steps or type(op.get("mutates")) is not bool:
                raise RegistryError("planned operation is executable")
            if op["id"] in {"gc-audit.registry", "gc-audit.zerotrust"} and op.get("zeroTrust") is not None:
                raise RegistryError("planned self-audit claims active zero-trust assurance")
            continue
        if op.get("status") != "active" or not steps:
            raise RegistryError("unknown status or empty active operation")
        mutable = op.get("mutates")
        if type(mutable) is not bool:
            raise RegistryError("missing mutation contract")
        if mutable and op.get("requiresExplicitApply") is not True:
            raise RegistryError("mutating operation lacks explicit apply")
        if not mutable and op.get("requiresExplicitApply") is True:
            raise RegistryError("read-only operation declares apply")
        zt = op.get("zeroTrust")
        if op["id"] in {"gc-audit.registry", "gc-audit.zerotrust"} and zt is None:
            raise RegistryError("active self-audit lacks zero-trust declaration")
        if zt is not None:
            if not isinstance(zt, dict) or op["id"] not in {"gc-audit.registry", "gc-audit.zerotrust"}:
                raise RegistryError("unauthorized zero-trust declaration")
            claims = zt.get("explicitAuthorizationRequired")
            if op["id"] == "gc-audit.registry" and (zt.get("failClosed") is not True or
                    set(zt) != {"failClosed", "networkRegistryFetch", "pathContainment",
                                "schemaInference", "explicitAuthorizationRequired"} or
                    zt.get("networkRegistryFetch") != "forbidden" or
                    zt.get("pathContainment") != "portfolio-root-for-registry-paths" or
                    zt.get("schemaInference") != "forbidden" or
                    not isinstance(claims, list) or
                    any(not isinstance(claim, str) for claim in claims) or
                    set(claims) != AUTH_CLAIMS or len(claims) != len(AUTH_CLAIMS)):
                raise RegistryError("incomplete registry authorization boundary")
            if op["id"] == "gc-audit.zerotrust" and zt != {"selfApplying": True}:
                raise RegistryError("invalid zero-trust self-audit declaration")
        for step in steps:
            if not isinstance(step, dict) or not set(step) <= STEP_FIELDS:
                raise RegistryError("invalid executable step")
            for key, value in step.items():
                if key in ARG_FIELDS and value != ARG_FIELDS[key]:
                    raise RegistryError("unsafe step argument mapping")
                if key.startswith("supports") or key == "portfolioOnly":
                    if type(value) is not bool and not (key == "supportsMode" and isinstance(value, list) and all(isinstance(x, str) and x for x in value)):
                        raise RegistryError("invalid step capability declaration")
            if "profiles" in step and (not isinstance(step["profiles"], list) or
                    not step["profiles"] or any(not isinstance(p, str) or not p for p in step["profiles"]) or
                    len(set(step["profiles"])) != len(step["profiles"])):
                raise RegistryError("invalid step profiles")
            if "fixedArgs" in step and (not isinstance(step["fixedArgs"], list) or
                    len(step["fixedArgs"]) % 2 or
                    any(not isinstance(arg, str) or not re.fullmatch(r"(?:-[A-Za-z][A-Za-z0-9]*|[0-9]+)", arg) for arg in step["fixedArgs"])):
                raise RegistryError("unsafe fixed arguments")
            physical = contained_script(step.get("script"), portfolio_root, repo_root)
            expected_self_audit = {"gc-audit.registry": "validate-registry.ps1",
                                   "gc-audit.zerotrust": "validate-zero-trust.ps1"}
            if op["id"] in expected_self_audit and (
                    len(steps) != 1 or physical.name != expected_self_audit[op["id"]]):
                raise RegistryError("self-audit operation redirected")
            if op["id"] in expected_self_audit:
                self_audit_ready.add(op["id"])
            if physical in internal:
                raise RegistryError("internal helper exposed as operation")
            scripts.add(physical)
            code = physical.read_text(encoding="utf-8-sig")
            if INDIRECT_PROCESS.search(code) or COMPUTED_PROCESS.search(code):
                delegation_findings.append(physical.name)
            if not mutable and WRITE_COMMAND.search(code):
                write_findings.append(physical.name)
            if DIRECT_SHELL.search(code):
                raise RegistryError("direct shell spawning or expression evaluation requires explicit review")
            if not mutable and WRITE_SWITCH.search(code):
                raise RegistryError("read-only operation exposes mutating switch")
            if mutable and not re.search(r"\[switch\]\s*\$Apply\b", code, re.I):
                raise RegistryError("mutating operation has no explicit -Apply")
    if not ids or not scripts:
        raise RegistryError("empty operation allowlist")
    readiness = "READY" if {"gc-audit.registry", "gc-audit.zerotrust"} <= self_audit_ready else "UNAVAILABLE"
    if require_self_audit and readiness != "READY":
        raise RegistryError("required self-audit assurance unavailable")
    if require_runtime_assurance:
        raise RegistryError("runtime confinement requires independently verified trusted-host enforcement")
    return {"status":"REGISTRY_CONTRACT_VALID", "delegation_review":"REQUIRED" if delegation_findings else "NOT_DETECTED",
            "indirect_delegation_scripts":sorted(set(delegation_findings)),
            "read_only_write_scripts":sorted(set(write_findings)),
            "self_audit_readiness":readiness,
            "runtime_security_assurance":"UNVERIFIED",
            "operations":len(ids),"scripts":len(scripts)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--registry",type=Path,required=True)
    p.add_argument("--portfolio-root",type=Path,required=True)
    p.add_argument("--repo-root",type=Path)
    p.add_argument("--require-self-audit",action="store_true")
    p.add_argument("--require-runtime-assurance",action="store_true")
    args=p.parse_args()
    try:
        outcome=validate_registry(args.registry.read_text(encoding="utf-8-sig"), args.portfolio_root,
            args.repo_root or args.registry.resolve(strict=True).parent.parent,
            require_self_audit=args.require_self_audit,
            require_runtime_assurance=args.require_runtime_assurance)
    except (RegistryError, OSError, UnicodeError) as exc:
        print(json.dumps({"status":"FAIL","reason":str(exc)}))
        return 1
    print(json.dumps(outcome,sort_keys=True))
    return 0

if __name__=="__main__":
    sys.exit(main())
