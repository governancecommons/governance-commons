"""Release catalog authorization never derives its trust anchor from fixtures."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from zta_catalog_authority import authorize_catalog, CatalogAuthorityError, canonical
from test_evaluator import records

class CatalogAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.catalog,_,_=records()
        self.expected={c["control_id"]:c["objective"] for c in self.catalog["controls"]}
        self.pin="sha256:"+hashlib.sha256(canonical(self.catalog)).hexdigest()
    def check(self):
        return authorize_catalog(self.catalog,approved_catalog_digest=self.pin,
                                 expected_objectives=self.expected)
    def test_pinned_complete_policy(self):
        self.assertEqual(self.check()["status"],"CATALOG_AUTHORIZED")
    def test_placeholder_catalog_rejected_against_real_policy(self):
        self.expected["ZTA-02.01"]="Authorization enforcement"
        with self.assertRaises(CatalogAuthorityError):self.check()
    def test_tamper_rejected_even_if_objectives_unchanged(self):
        self.catalog["controls"][0]["fail_predicate"]="changed"
        with self.assertRaises(CatalogAuthorityError):self.check()
    def test_incomplete_independent_catalog_rejected(self):
        del self.expected["ZTA-02.01"]
        with self.assertRaises(CatalogAuthorityError):self.check()
    def test_digest_cannot_come_from_untrusted_target(self):
        self.pin="sha256:"+"0"*64
        with self.assertRaises(CatalogAuthorityError):self.check()

if __name__=="__main__":unittest.main()
