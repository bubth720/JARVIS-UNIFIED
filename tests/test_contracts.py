import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import contracts as c
ROOT=Path(__file__).resolve().parents[1]/'contracts/v1'
NAMES=['capability-manifest','request-envelope','response-envelope','resource-lease','health-status']
class ContractTests(unittest.TestCase):
    def load(self,name):return json.loads((ROOT/'examples'/(name+'.valid.json')).read_text())
    def check(self,name,value):return c.validate_contract(name,value,json.loads((ROOT/(name+'.schema.json')).read_text()))
    def test_five_valid_examples(self):
        for name in NAMES:
            with self.subTest(name=name):self.assertTrue(self.check(name,self.load(name)))
    def test_five_invalid_examples(self):
        for name in NAMES:
            with self.subTest(name=name),self.assertRaises(c.ContractError):self.check(name,json.loads((ROOT/'examples'/(name+'.invalid.json')).read_text()))
    def test_unknown_fields_rejected_for_every_contract(self):
        for name in NAMES:
            v=self.load(name);v['secret_unknown']=True
            with self.subTest(name=name),self.assertRaises(c.ContractError):self.check(name,v)
    def test_boolean_not_integer(self):
        for value in [True,10**700]:
            v=self.load('request-envelope');v['limits']['timeout_ms']=value
            with self.subTest(value_type=type(value).__name__),self.assertRaises(c.ContractError):self.check('request-envelope',v)
    def test_deadline_and_model_identity(self):
        for mutate in [lambda v:v['deadline'].update(expires_at_ms=999),lambda v:v['payload'].pop('model_sha256')]:
            v=self.load('request-envelope');mutate(v)
            with self.assertRaises(c.ContractError):self.check('request-envelope',v)
    def test_voice_binding_is_engine_pack_specific(self):
        v=self.load('request-envelope');v['capability']='speech.synthesize';v['destination']='voice'
        with self.assertRaises(c.ContractError):self.check('request-envelope',v)
        v['payload']['pack_sha256']='b'*64;v['payload']['voice_profile_ref']=v['correlation_id'];self.assertTrue(self.check('request-envelope',v))
    def test_cancellation_does_not_release_residency(self):
        v=self.load('resource-lease');v['release_confirmed']=True
        with self.assertRaises(c.ContractError):self.check('resource-lease',v)
    def test_release_requires_real_end_and_no_model(self):
        v=self.load('resource-lease');v.update(state='released',release_confirmed=True,effective_end=False)
        with self.assertRaises(c.ContractError):self.check('resource-lease',v)
        v.update(effective_end=True,model_resident=False);self.assertTrue(self.check('resource-lease',v))
    def test_unavailable_incompatible_unauthorized_and_expired_responses(self):
        for status,code in [('unavailable','MODULE_ABSENT'),('incompatible','INCOMPATIBLE'),('unauthorized','UNAUTHORIZED'),('interrupted','INTERRUPTED'),('expired','EXPIRED'),('cancelled','CANCELLED'),('refused','INSUFFICIENT_RESOURCES')]:
            v=self.load('response-envelope');v['status']=status;v['error']['code']=code;self.assertTrue(self.check('response-envelope',v))
    def test_correlations_and_responding_identity(self):
        req=self.load('request-envelope');res=self.load('response-envelope');self.assertTrue(c.validate_exchange(req,res))
        res['correlation_id']='00000000-0000-4000-8000-000000000002'
        with self.assertRaises(c.ContractError):c.validate_exchange(req,res)
    def test_schema_unknown_keywords_fail_closed(self):
        with self.assertRaises(c.ContractError):c.validate_schema({'type':'object','made_up_validation':True})
    def test_unavailable_cannot_advertise_available_capability(self):
        v=self.load('capability-manifest');v['capabilities'][0]['available']=True
        with self.assertRaises(c.ContractError):self.check('capability-manifest',v)

if __name__=='__main__':unittest.main()
