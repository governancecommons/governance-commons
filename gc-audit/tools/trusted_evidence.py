"""Bounded Ed25519 evidence authentication against host-configured roots.

This module authenticates producers relative to a host-supplied root and a
durable replay ledger. It does not establish the root's independent provenance,
evaluate control sufficiency, or authorize a ZTA PASS.
"""
from __future__ import annotations

import base64
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jsonschema import Draft202012Validator, FormatChecker

from zta_authenticated_packages import canonical_bytes
from zta_evaluator import digest

SCHEMAS = Path(__file__).resolve().parents[1] / "schemas" / "evidence"


class EvidenceVerificationError(ValueError):
    pass


def _validate(name: str, value: dict) -> None:
    schema = json.loads((SCHEMAS / f"gc-audit.{name}.v1.schema.json").read_text(encoding="utf-8"))
    error = next(iter(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(value)), None)
    if error:
        raise EvidenceVerificationError(f"invalid {name}: {error.message}")


def _time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError, AttributeError) as exc:
        raise EvidenceVerificationError("invalid timestamp") from exc
    if parsed.tzinfo is None:
        raise EvidenceVerificationError("timezone-bound timestamp required")
    return parsed.astimezone(timezone.utc)


def _verify_signature(payload: dict, signature: str, key_bytes: bytes) -> None:
    try:
        if not isinstance(key_bytes, bytes) or len(key_bytes) != 32:
            raise ValueError("invalid public key")
        Ed25519PublicKey.from_public_bytes(key_bytes).verify(
            base64.b64decode(signature, validate=True), canonical_bytes(payload))
    except (InvalidSignature, ValueError, TypeError) as exc:
        raise EvidenceVerificationError("signature invalid") from exc


class ReplayLedger:
    """Host-owned SQLite receipt store; use a persistent path in real hosts."""

    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(str(path), timeout=10, isolation_level=None)
        try:
            self.db.execute("CREATE TABLE IF NOT EXISTS receipts (evidence_id TEXT PRIMARY KEY, nonce TEXT UNIQUE NOT NULL, envelope_digest TEXT NOT NULL)")
        except sqlite3.Error:
            self.db.close()
            raise

    def accept(self, receipts: list[tuple[str, str, str]]) -> None:
        try:
            self.db.execute("BEGIN IMMEDIATE")
            self.db.executemany("INSERT INTO receipts(evidence_id,nonce,envelope_digest) VALUES(?,?,?)", receipts)
            self.db.execute("COMMIT")
        except sqlite3.IntegrityError as exc:
            self.db.execute("ROLLBACK")
            raise EvidenceVerificationError("replayed evidence identifier or nonce") from exc
        except Exception:
            self.db.execute("ROLLBACK")
            raise

    def close(self) -> None:
        self.db.close()


class HostEvidenceVerifier:
    """Host creates this with roots and ledger from configuration outside target data.

    The evidence envelope has no trust-root field. A caller able to replace this
    host object or its configuration is outside this library's trust boundary;
    results therefore say CONFIGURED_ROOT_ONLY, never independent authority.
    """

    def __init__(self, *, root_keys: dict[str, bytes], revoked_root_ids=(),
                 revoked_policy_ids=(), revoked_producer_key_ids=(), replay_ledger: ReplayLedger):
        if not isinstance(root_keys, dict) or not root_keys or not isinstance(replay_ledger, ReplayLedger):
            raise EvidenceVerificationError("host roots and replay ledger required")
        if any(not isinstance(k, str) or not k or not isinstance(v, bytes) or len(v) != 32
               for k, v in root_keys.items()):
            raise EvidenceVerificationError("invalid configured host root")
        self._roots = dict(root_keys)
        self._revoked = frozenset(revoked_root_ids)
        self._revoked_policies = frozenset(revoked_policy_ids)
        self._revoked_producers = frozenset(revoked_producer_key_ids)
        self._ledger = replay_ledger

    def verify(self, *, authority: dict, envelopes: list[dict], catalog: dict,
               target_id: str, revision: str, environment: str,
               expected_control_ids: set[str], as_of: str) -> dict:
        try:
            policy_digest = digest(authority)
        except (TypeError, ValueError):
            policy_digest = digest({"invalid": True})
        try:
            envelope_digest = digest(envelopes)
        except (TypeError, ValueError):
            envelope_digest = digest({"invalid": True})
        context = {"target_id": target_id, "revision": revision,
                   "environment": environment,
                   "control_ids": sorted(expected_control_ids) if isinstance(expected_control_ids, set) else [],
                   "assessed_at": as_of}
        try:
            evidence_ids, receipts = self._check(authority, envelopes, catalog,
                target_id, revision, environment, expected_control_ids, as_of)
            self._ledger.accept(receipts)
            result = {"schema": "gc-audit.evidence-verification.v1", "status": "AUTHENTICATED",
                      "reason": "signatures, bindings, freshness and replay acceptance verified against configured root",
                      **context,
                      "evidence_ids": sorted(evidence_ids), "policy_digest": policy_digest,
                      "envelope_digest": envelope_digest,
                      "producer_authentication": "SIGNATURE_VERIFIED",
                      "host_authority": "CONFIGURED_ROOT_ONLY", "control_status": "UNVERIFIED"}
        except (EvidenceVerificationError, sqlite3.Error, TypeError, KeyError, ValueError) as exc:
            result = {"schema": "gc-audit.evidence-verification.v1", "status": "REJECTED",
                      "reason": str(exc), "evidence_ids": [], "policy_digest": policy_digest,
                      **context,
                      "envelope_digest": envelope_digest,
                      "producer_authentication": "UNVERIFIED",
                      "host_authority": "CONFIGURED_ROOT_ONLY", "control_status": "UNVERIFIED"}
        _validate("evidence-verification", result)
        return result

    def _check(self, authority, envelopes, catalog, target_id, revision,
               environment, expected_control_ids, as_of):
        if not all(isinstance(v, str) and v for v in (target_id, revision, environment)):
            raise EvidenceVerificationError("host target context required")
        if not isinstance(expected_control_ids, set) or not expected_control_ids:
            raise EvidenceVerificationError("host control scope required")
        now = _time(as_of)
        _validate("host-authority", authority)
        policy = authority["payload"]
        root_id = policy["root_key_id"]
        if root_id in self._revoked or root_id not in self._roots:
            raise EvidenceVerificationError("unknown or revoked host root")
        _verify_signature(policy, authority["signature"], self._roots[root_id])
        if policy["policy_id"] in self._revoked_policies:
            raise EvidenceVerificationError("host authority policy revoked")
        if (policy["target_id"], policy["revision"], policy["environment"]) != (target_id, revision, environment):
            raise EvidenceVerificationError("host target, revision or environment mismatch")
        issued, expires = _time(policy["issued_at"]), _time(policy["expires_at"])
        if not issued <= now < expires or (policy.get("revoked_at") and now >= _time(policy["revoked_at"])):
            raise EvidenceVerificationError("host authority expired or revoked")
        if policy["catalog_digest"] != digest(catalog):
            raise EvidenceVerificationError("catalog differs from signed authority")
        catalog_controls = {c["control_id"]: c["objective"] for c in catalog["controls"]}
        if len(catalog_controls) != len(catalog["controls"]):
            raise EvidenceVerificationError("duplicate catalog control")
        control_policy = {c["control_id"]: c for c in policy["controls"]}
        if len(control_policy) != len(policy["controls"]) or not expected_control_ids <= control_policy.keys():
            raise EvidenceVerificationError("control scope missing or duplicated")
        for cid in expected_control_ids:
            if cid not in catalog_controls or control_policy[cid]["objective_digest"] != digest(catalog_controls[cid]):
                raise EvidenceVerificationError("control objective differs from signed authority")
        producers = {p["key_id"]: p for p in policy["producers"]}
        if len(producers) != len(policy["producers"]):
            raise EvidenceVerificationError("duplicate producer key identifier")
        if not isinstance(envelopes, list) or not envelopes:
            raise EvidenceVerificationError("missing evidence envelope")
        seen_ids, seen_nonces, seen_pairs, receipts = set(), set(), set(), []
        for envelope in envelopes:
            _validate("evidence-envelope", envelope)
            item = envelope["payload"]
            eid, nonce, cid = item["evidence_id"], item["nonce"], item["control_id"]
            if eid in seen_ids or nonce in seen_nonces:
                raise EvidenceVerificationError("duplicate evidence identifier or nonce")
            seen_ids.add(eid); seen_nonces.add(nonce)
            if eid in policy["revoked_evidence_ids"]:
                raise EvidenceVerificationError("evidence identifier revoked")
            if (item["policy_id"], item["target_id"], item["revision"], item["environment"]) != (
                    policy["policy_id"], target_id, revision, environment):
                raise EvidenceVerificationError("evidence target, revision or environment mismatch")
            if cid not in expected_control_ids:
                raise EvidenceVerificationError("evidence control outside host scope")
            approved = control_policy[cid]
            if (item["objective_digest"] != approved["objective_digest"]
                    or item["method"] not in approved["methods"] or item["scope"] not in approved["scopes"]):
                raise EvidenceVerificationError("objective, method or collection scope unauthorized")
            pair = (cid, item["scope"])
            if pair in seen_pairs:
                raise EvidenceVerificationError("duplicate control and collection scope")
            seen_pairs.add(pair)
            if item["observation_digest"] != digest(item["observation"]):
                raise EvidenceVerificationError("observation content digest mismatch")
            observed, item_expires = _time(item["collected_at"]), _time(item["expires_at"])
            if not issued <= observed <= now < item_expires or (now - observed).total_seconds() > policy["max_evidence_age_seconds"]:
                raise EvidenceVerificationError("evidence expired, stale or future-dated")
            signer = producers.get(item["producer_key_id"])
            if signer is None or item["producer_key_id"] in self._revoked_producers:
                raise EvidenceVerificationError("producer not authorized by signed host policy")
            if (not _time(signer["valid_from"]) <= observed
                    or not now < _time(signer["valid_until"])
                    or signer.get("revoked_at") and now >= _time(signer["revoked_at"])):
                raise EvidenceVerificationError("producer key expired or revoked")
            try:
                key_bytes = base64.b64decode(signer["public_key_b64"], validate=True)
            except (ValueError, TypeError) as exc:
                raise EvidenceVerificationError("invalid producer key encoding") from exc
            _verify_signature(item, envelope["signature"], key_bytes)
            receipts.append((eid, nonce, digest(envelope)))
        expected_pairs = {(cid, scope) for cid in expected_control_ids for scope in control_policy[cid]["scopes"]}
        if seen_pairs != expected_pairs:
            raise EvidenceVerificationError("requested control or collection scope evidence incomplete")
        return seen_ids, receipts
