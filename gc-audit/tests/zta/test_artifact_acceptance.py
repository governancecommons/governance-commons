"""Whole-chain acceptance gate tamper and conflict tests."""
import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from zta_artifact_acceptance import screen_artifact_acceptance

class ArtifactAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.policy={"target_id":"app","revision":"rev","build_id":"job",
                     "install_scope":"prod","artifact_digest":"sha256:"+"a"*64,
                     "authorized_builder_keys":["builder"],
                     "authorized_observer_keys":["observer"],
                     "corroborated_execution_ids":["execution"]}
        shared={"control_id":"ZTA-08.02","release_decision":"UNVERIFIED",
                "target_id":"app","revision":"rev","build_id":"job",
                "install_scope":"prod","artifact_digest":self.policy["artifact_digest"]}
        self.chain={**shared,"status":"ARTIFACT_CHAIN_CANDIDATE",
                    "builder_key_id":"builder","observer_key_id":"observer",
                    "build_execution_id":"execution"}
        self.provenance={**shared,"status":"SIGNED_BUILD_PROVENANCE","builder_key_id":"builder"}
        self.execution={**shared,"status":"BUILD_EXECUTION_CORROBORATED","execution_id":"execution"}
        self.installation={**shared,"status":"SIGNED_INSTALLATION_OBSERVATION","observer_key_id":"observer"}
    def check(self):
        return screen_artifact_acceptance(chain=self.chain,provenance=self.provenance,
                                          execution=self.execution,installation=self.installation,
                                          independent_policy=self.policy)
    def test_complete_chain_is_not_pass(self):
        result=self.check()
        self.assertEqual(result["status"],"WHOLE_CHAIN_REVIEW_CANDIDATE")
        self.assertEqual(result["release_decision"],"UNVERIFIED")
    def test_revision_mismatch(self):
        self.provenance["revision"]="old"
        with self.assertRaises(ValueError):self.check()
    def test_wrong_deployment(self):
        self.installation["install_scope"]="test"
        with self.assertRaises(ValueError):self.check()
    def test_wrong_artifact(self):
        self.execution["artifact_digest"]="sha256:"+"b"*64
        with self.assertRaises(ValueError):self.check()
    def test_execution_substitution(self):
        self.chain["build_execution_id"]="untrusted"
        with self.assertRaises(ValueError):self.check()
    def test_unknown_observer(self):
        self.policy["authorized_observer_keys"]=["different"]
        with self.assertRaises(ValueError):self.check()
    def test_wrong_builder(self):
        self.provenance["builder_key_id"]="other"
        with self.assertRaises(ValueError):self.check()
    def test_claimed_pass_rejected(self):
        self.installation["release_decision"]="PASS"
        with self.assertRaises(ValueError):self.check()
    def test_incomplete_policy_rejected(self):
        del self.policy["corroborated_execution_ids"]
        with self.assertRaises(ValueError):self.check()
    def test_missing_component_rejected(self):
        self.provenance={}
        with self.assertRaises(ValueError):self.check()

if __name__=="__main__":
    unittest.main()
