"""Validate that a ZTA catalog is approved for substantive decisions.

Schema fixtures are deliberately synthetic. Structural validity is not a
claim that the catalog represents the 24 normative acceptance-contract controls.
"""
from __future__ import annotations
import hashlib
import json

class CatalogAuthorityError(ValueError):
    pass

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def authorize_catalog(catalog, *, approved_catalog_digest, expected_objectives):
    if not isinstance(expected_objectives,dict) or len(expected_objectives)!=24:
        raise CatalogAuthorityError("complete independent control objectives required")
    actual={c["control_id"]:c["objective"] for c in catalog["controls"]}
    if len(actual)!=24 or actual!=expected_objectives:
        raise CatalogAuthorityError("catalog objectives differ from approved normative controls")
    measured="sha256:"+hashlib.sha256(canonical(catalog)).hexdigest()
    if measured!=approved_catalog_digest:
        raise CatalogAuthorityError("catalog does not match externally pinned release digest")
    return {"status":"CATALOG_AUTHORIZED","catalog_digest":measured,
            "controls_checked":24}
