"""Applicability screening cannot issue NOT_APPLICABLE from absence claims."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from zta_applicability import screen_applicability

class ApplicabilityTests(unittest.TestCase):
    def setUp(self):
        self.base={"control_id":"ZTA-06.02","target_id":"target","revision":"rev1",
                   "capability":"remote_access","trusted_capability_policy":{"ZTA-06.02":"remote_access"}}
        self.absent={"id":"obs1","target_id":"target","revision":"rev1",
                     "capability":"remote_access","outcome":"ABSENT",
                     "scope":"deployment","inventory_complete":True}
        self.trust={"obs1":("target","rev1","remote_access","ABSENT","deployment",True)}
    def screen(self,items=None,trust=None):
        return screen_applicability(**self.base,observations=[self.absent] if items is None else items,
             independently_verified_observations=self.trust if trust is None else trust)
    def test_independent_absence_is_only_candidate(self):
        result=self.screen()
        self.assertEqual(result["status"],"ABSENCE_CANDIDATE")
        self.assertNotEqual(result["status"],"NOT_APPLICABLE")
    def test_target_claim_without_verifier_rejected(self):
        with self.assertRaises(ValueError):
            self.screen(trust={})
    def test_unknown_policy_rejected(self):
        self.base["trusted_capability_policy"]={}
        with self.assertRaises(ValueError):self.screen()
    def test_revision_substitution_rejected(self):
        self.absent["revision"]="rev2"
        with self.assertRaises(ValueError):self.screen()
    def test_incomplete_inventory_not_a_candidate(self):
        self.absent["inventory_complete"]=False
        self.trust["obs1"]=("target","rev1","remote_access","ABSENT","deployment",False)
        self.assertEqual(self.screen()["status"],"UNVERIFIED")
    def test_verified_presence_overrides_absence(self):
        present=dict(self.absent,id="obs2",outcome="PRESENT")
        trust=dict(self.trust,obs2=("target","rev1","remote_access","PRESENT","deployment",True))
        self.assertEqual(self.screen([self.absent,present],trust)["status"],"APPLICABLE")
    def test_unknown_blocks_absence_candidate(self):
        unknown=dict(self.absent,id="obs2",outcome="UNKNOWN")
        trust=dict(self.trust,obs2=("target","rev1","remote_access","UNKNOWN","deployment",True))
        self.assertEqual(self.screen([self.absent,unknown],trust)["status"],"UNVERIFIED")
    def test_duplicate_observation_rejected(self):
        with self.assertRaises(ValueError):
            self.screen([self.absent,self.absent])
    def test_no_observations_remains_unverified(self):
        self.assertEqual(self.screen([])["status"],"UNVERIFIED")

if __name__=="__main__":unittest.main()
