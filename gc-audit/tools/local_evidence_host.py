"""Local host adapter for the existing GC-AUDIT evidence verifier.

The host deployment supplies a directory and a separately pinned configuration
digest. Evidence may supply envelopes only. This module never grants ZTA PASS.
"""
from __future__ import annotations

import base64
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import subprocess

from trusted_evidence import EvidenceVerificationError, HostEvidenceVerifier, ReplayLedger, _validate
from zta_evaluator import digest


class HostConfigurationError(EvidenceVerificationError):
    pass


def _windows_acl(path: Path) -> dict:
    script = r"""
$ErrorActionPreference = 'Stop'
$acl = Get-Acl -LiteralPath $env:GC_AUDIT_ACL_PATH
$sid = [Security.Principal.WindowsIdentity]::GetCurrent().User.Value
$rules = @($acl.Access | ForEach-Object {
  @{sid=$_.IdentityReference.Translate([Security.Principal.SecurityIdentifier]).Value;
    type=$_.AccessControlType.ToString()}
})
@{principal=$sid;owner=$acl.GetOwner([Security.Principal.SecurityIdentifier]).Value;
  protected=$acl.AreAccessRulesProtected;rules=$rules} | ConvertTo-Json -Compress -Depth 5
"""
    env = dict(os.environ, GC_AUDIT_ACL_PATH=str(path))
    run = subprocess.run(["pwsh", "-NoProfile", "-NonInteractive", "-Command", script],
                         capture_output=True, text=True, env=env, timeout=15, check=False)
    if run.returncode:
        raise HostConfigurationError(f"host ACL inspection failed: {run.stderr.strip()[:240]}")
    try:
        return json.loads(run.stdout)
    except ValueError as exc:
        raise HostConfigurationError("host ACL inspection malformed") from exc


def host_principal() -> str:
    if os.name == "nt":
        run = subprocess.run(["pwsh", "-NoProfile", "-NonInteractive", "-Command",
                              "[Security.Principal.WindowsIdentity]::GetCurrent().User.Value"],
                             capture_output=True, text=True, timeout=15, check=False)
        if run.returncode or not run.stdout.strip():
            raise HostConfigurationError("host principal inspection failed")
        return run.stdout.strip()
    return f"uid:{os.geteuid()}"


def _checked_path(path: Path, *, directory: bool, private: bool) -> os.stat_result:
    if not path.is_absolute() or ".." in path.parts:
        raise HostConfigurationError("absolute path without traversal required")
    for part in (path, *path.parents):
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or (getattr(info, "st_file_attributes", 0) & 0x400):
            raise HostConfigurationError("filesystem link or reparse point forbidden")
    info = path.lstat()
    if directory and not stat.S_ISDIR(info.st_mode) or not directory and not stat.S_ISREG(info.st_mode):
        raise HostConfigurationError("unexpected host filesystem object")
    if private and not directory and info.st_nlink != 1:
        raise HostConfigurationError("host file has multiple hard links")
    if private:
        if os.name == "nt":
            acl = _windows_acl(path)
            if acl["owner"] != acl["principal"]:
                raise HostConfigurationError("host resource owner differs from current principal")
            allowed = {acl["principal"], "S-1-5-18", "S-1-5-32-544"}
            if any(rule["sid"] not in allowed for rule in acl["rules"] if rule["type"] == "Allow"):
                raise HostConfigurationError("host resource grants access to untrusted principal")
            if directory and not acl["protected"]:
                raise HostConfigurationError("host directory inherits ACL")
        elif info.st_uid != os.geteuid() or info.st_mode & 0o077:
            raise HostConfigurationError("host resource owner or permissions invalid")
    return info


def _read_json(path: Path, *, private: bool) -> dict:
    before = _checked_path(path, directory=False, private=private)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_CLOEXEC", 0)
    fd = os.open(path, flags)
    try:
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino) or not stat.S_ISREG(after.st_mode):
            raise HostConfigurationError("host file changed during open")
        with os.fdopen(fd, "rb", closefd=False) as stream:
            raw = stream.read(1_048_577)
        if len(raw) > 1_048_576:
            raise HostConfigurationError("host file exceeds size limit")
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise HostConfigurationError(f"invalid JSON in {path.name}: {exc}") from exc
        if not isinstance(value, dict):
            raise HostConfigurationError("JSON object required")
        return value
    finally:
        os.close(fd)


def _separate(a: Path, b: Path) -> None:
    left, right = a.resolve(strict=True), b.resolve(strict=True)
    if left == right or left in right.parents or right in left.parents:
        raise HostConfigurationError("host and target paths overlap")


class LocalEvidenceHost:
    """Host-owned loading and receipts; caller must protect deployment inputs."""

    def __init__(self, host_dir: str | Path, *, expected_config_digest: str):
        self.host_dir = Path(host_dir)
        self.expected_config_digest = expected_config_digest
        if not isinstance(expected_config_digest, str) or not re.fullmatch(r"sha256:[a-f0-9]{64}", expected_config_digest):
            raise HostConfigurationError("deployment configuration pin required")

    def verify(self, package_path: str | Path, catalog: dict, *, assessed_at: str | None = None) -> dict:
        try:
            principal = host_principal()
        except (OSError, HostConfigurationError, subprocess.SubprocessError):
            principal = "UNAVAILABLE"
        receipt = {"schema": "gc-audit.local-host-receipt.v1", "status": "REJECTED",
                   "reason": "host verification did not complete", "host_authority": "CONFIGURED_ROOT_ONLY",
                   "control_status": "UNVERIFIED", "host_principal": principal,
                   "host_id": None, "config_digest": None, "authority_digest": None,
                   "package_digest": None, "catalog_digest": None, "verifier_result": None,
                   "limitations": ["same-principal or deployment-source separation is not proven by this adapter",
                                   "signature authentication does not establish ZTA control PASS"]}
        try:
            if principal == "UNAVAILABLE":
                raise HostConfigurationError("host principal unavailable")
            _checked_path(self.host_dir, directory=True, private=True)
            config = _read_json(self.host_dir / "config.json", private=True)
            _validate("local-host-config", config)
            receipt["host_id"] = config["host_id"]
            receipt["config_digest"] = digest(config)
            if receipt["config_digest"] != self.expected_config_digest:
                raise HostConfigurationError("host configuration differs from deployment pin")
            if config["host_principal"] != receipt["host_principal"]:
                raise HostConfigurationError("host principal differs from configuration")
            target = Path(config["target_root"])
            _checked_path(target, directory=True, private=False)
            _separate(self.host_dir, target)
            git_env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
                           GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
            git_command = ["git", "-c", "core.fsmonitor=false", "-C", str(target)]
            revision = subprocess.run([*git_command, "rev-parse", "HEAD"], env=git_env,
                capture_output=True, text=True, timeout=15, check=True).stdout.strip()
            if revision != config["revision"]:
                raise HostConfigurationError("target revision differs from host configuration")
            if subprocess.run([*git_command, "status", "--porcelain"], env=git_env,
                capture_output=True, text=True, timeout=15, check=True).stdout.strip():
                raise HostConfigurationError("target worktree is not clean")
            receipt["catalog_digest"] = digest(catalog)
            if receipt["catalog_digest"] != config["catalog_digest"]:
                raise HostConfigurationError("catalog differs from host configuration")
            authority = _read_json(self.host_dir / "authority.json", private=True)
            receipt["authority_digest"] = digest(authority)
            if receipt["authority_digest"] != config["policy_digest"]:
                raise HostConfigurationError("authority policy differs from host configuration")
            package = _read_json(Path(package_path), private=False)
            if set(package) != {"schema", "envelopes"} or package["schema"] != "gc-audit.local-evidence-package.v1":
                raise HostConfigurationError("evidence package may contain envelopes only")
            receipt["package_digest"] = digest(package)
            keys = {}
            for entry in config["root_keys"]:
                if entry["key_id"] in keys:
                    raise HostConfigurationError("duplicate host root identifier")
                keys[entry["key_id"]] = base64.b64decode(entry["public_key_b64"], validate=True)
            ledger_path = self.host_dir / "replay.sqlite"
            _checked_path(ledger_path, directory=False, private=True)
            ledger = ReplayLedger(ledger_path)
            try:
                if ledger.db.execute("PRAGMA integrity_check").fetchone() != ("ok",):
                    raise HostConfigurationError("replay ledger integrity check failed")
                verifier = HostEvidenceVerifier(root_keys=keys,
                    revoked_root_ids=config["revoked_root_ids"],
                    revoked_policy_ids=config["revoked_policy_ids"],
                    revoked_producer_key_ids=config["revoked_producer_key_ids"], replay_ledger=ledger)
                from datetime import datetime, timezone
                as_of = assessed_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                outcome = verifier.verify(authority=authority, envelopes=package["envelopes"],
                    catalog=catalog, target_id=config["target_id"], revision=config["revision"],
                    environment=config["environment"], expected_control_ids=set(config["control_ids"]),
                    as_of=as_of)
                receipt["verifier_result"] = outcome
                receipt["status"] = outcome["status"]
                receipt["reason"] = outcome["reason"]
            finally:
                ledger.close()
        except (OSError, ValueError, KeyError, sqlite3.Error, subprocess.SubprocessError) as exc:
            receipt["reason"] = f"host rejected: {type(exc).__name__}: {exc}"
        receipt["receipt_digest"] = digest(receipt)
        _validate("local-host-receipt", receipt)
        return receipt
