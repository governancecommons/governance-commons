"""Adversarial signed scope review tests: signature does not grant N/A."""
import base64
import copy
import sys
import unittest
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"tools"))
from zta_scope_approvals import DOMAIN,canonical,verify_scope_approval

def scenario():
    sk=Ed25519PrivateKey.generate()
    pub=sk.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
    p={"domain":DOMAIN,"target_id":"app","revision":"rev1","control_id":"ZTA-06.02",
       "capability":"remote_access","required_scopes":["deployment","integrations"],
       "observation_ids":["o1","o2"],"decision":"APPROVE_ABSENCE_REVIEW",
       "approver_key_id":"reviewer"}
    env={"payload":p,"signature":base64.b64encode(sk.sign(canonical(p))).decode()}
    args={"target_id":"app","revision":"rev1","control_id":"ZTA-06.02",
          "capability":"remote_access","required_scopes":["deployment","integrations"],
          "verified_screen":{"status":"ABSENCE_CANDIDATE","verified_scopes":["deployment","integrations"]},
          "verified_observation_ids":{"o1","o2"},
          "authorized_approvers":{"reviewer":pub}}
    return env,args,sk

class ScopeApprovalTests(unittest.TestCase):
    def test_valid_signature_still_unverified(self):
        env,args,_=scenario()
        r=verify_scope_approval(env,**args)
        self.assertEqual(r["status"],"SIGNED_SCOPE_REVIEW")
        self.assertEqual(r["release_decision"],"UNVERIFIED")
    def test_tampering_rejected(self):
        for key,value in (("revision","new"),("control_id","ZTA-01.01"),
                          ("required_scopes",["deployment"]),("approver_key_id","rogue")):
            with self.subTest(key=key):
                env,args,_=scenario()
                env["payload"][key]=value
                with self.assertRaises(ValueError):verify_scope_approval(env,**args)
    def test_wrong_signature_rejected(self):
        env,args,_=scenario()
        env["signature"]=base64.b64encode(b"x"*64).decode()
        with self.assertRaises(ValueError):verify_scope_approval(env,**args)
    def test_missing_independent_coverage_rejected(self):
        env,args,_=scenario()
        args["verified_screen"]["verified_scopes"]=["deployment"]
        with self.assertRaises(ValueError):verify_scope_approval(env,**args)
    def test_observation_set_mismatch_rejected(self):
        env,args,_=scenario()
        args["verified_observation_ids"]={"o1"}
        with self.assertRaises(ValueError):verify_scope_approval(env,**args)
    def test_verified_presence_blocks_approval(self):
        env,args,_=scenario()
        args["verified_screen"]["status"]="APPLICABLE"
        with self.assertRaises(ValueError):verify_scope_approval(env,**args)
    def test_untrusted_reviewer_rejected(self):
        env,args,_=scenario()
        args["authorized_approvers"]={}
        with self.assertRaises(ValueError):verify_scope_approval(env,**args)

if __name__=="__main__":unittest.main()
