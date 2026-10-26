import copy
import unittest
from tooling.integration.lock import ROOT,load,LockError
from tooling.integration.v2 import validate,assess,compare_to_v1
from tooling.integration.contracts_v2 import receipt,transition,capability,check_examples


class EvidenceV2Tests(unittest.TestCase):
    def setUp(self):self.lock=load(ROOT/'integration-lock-v2.json')

    def test_current_candidate_is_blocked_and_v1_intact(self):
        result=assess(self.lock)
        self.assertFalse(result['android_multi_module_go'])
        self.assertTrue(any('CORE_NOT_CONSUMING_PRIMARY' in b for b in result['blockers']))
        self.assertEqual(len(compare_to_v1(self.lock)['components']),8)

    def test_ready_without_instrumentation_or_successful_ci_refused(self):
        self.lock['status']='READY'
        with self.assertRaises(LockError):validate(self.lock)

    def test_rag_reconciliation_is_not_misreported_as_old_v3(self):
        profile=next(x for x in self.lock['versions'] if x['module']=='nexus')
        self.assertTrue(any('version4' in x for x in profile['data_schemas']))
        self.assertEqual(next(x for x in self.lock['components'] if x['id']=='nexus')['primary']['commit'],'9d6928cd8651f83fa5091bdb474b33761d366412')

    def test_robolectric_cannot_be_promoted_to_emulator(self):
        self.lock['proofs'][0].update(level='ANDROID_EMULATOR_PASS',driver='robolectric',target='android24')
        with self.assertRaises(LockError):validate(self.lock)

    def test_api26_proof_cannot_satisfy_api24_or_25(self):
        p=self.lock['proofs'][0]
        p.update(level='END_TO_END_PASS',driver='android_instrumentation',target='android26',scenario='A')
        result=assess(self.lock)
        self.assertIn('ANDROID_E2E_MISSING:android24:A',result['blockers'])
        self.assertIn('ANDROID_E2E_MISSING:android25:A',result['blockers'])

    def test_failed_skipped_empty_and_unbound_proofs_refused(self):
        for key,value in [('failed',1),('skipped',1),('tests',0),('commit','f'*40)]:
            x=copy.deepcopy(self.lock);x['proofs'][0][key]=value
            with self.assertRaises(LockError):validate(x)
        self.lock['proofs'][0]['evidence']['sha256']='0'*64
        with self.assertRaises(LockError):validate(self.lock)

    def test_consumed_unknown_dependency_sha_is_rejected(self):
        self.lock['consumed'][0]['commit']='0'*40
        with self.assertRaises(LockError):validate(self.lock)

    def test_core_min_sdk_and_fusion01_baseline_cannot_be_changed(self):
        x=copy.deepcopy(self.lock);next(v for v in x['versions'] if v['module']=='core')['min_sdk']=26
        with self.assertRaises(LockError):validate(x)
        self.lock['baseline_sha256']='0'*64
        with self.assertRaises(LockError):validate(self.lock)

    def test_independent_lanes_do_not_add_pilot_ci_blockers(self):
        result=assess(self.lock)
        for owner in ['llm','voice','interface','evolution','unified']:
            self.assertNotIn('CI_NOT_SUCCESS:'+owner,result['blockers'])


class ContractV2Tests(unittest.TestCase):
    def setUp(self):
        self.lock=load(ROOT/'integration-lock-v2.json')
        self.r=load(ROOT/'docs/fusion-02/proposals/operation-receipt.valid.json')
        self.c=load(ROOT/'docs/fusion-02/proposals/capability-status.valid.json')

    def test_examples_remain_unapproved_and_runtime_absent(self):
        self.assertEqual(check_examples(self.lock),{'valid_examples':2,'invalid_examples_rejected':2,'approved':False,'runtime_implemented':False})

    def test_old_completed_never_becomes_committed(self):
        self.r['state']='COMPLETED'
        with self.assertRaises(ValueError):receipt(self.r)

    def test_denial_before_commit_never_claims_effect(self):
        denied={**self.r,'sequence':2,'state':'UNKNOWN','authorization_at_commit':'DENIED','error':'PERMISSION_REVOKED'}
        self.assertEqual(transition(self.r,denied)['effect'],'NONE')
        denied['effect']='STARTED'
        with self.assertRaises(LockError):receipt(denied)

    def test_revocation_after_commit_preserves_honest_effect(self):
        dispatched={**self.r,'sequence':2,'state':'DISPATCHED'}
        started={**dispatched,'sequence':3,'authorization_at_commit':'GRANTED','confirmation_consumed':True,'effect':'STARTED'}
        committed={**started,'sequence':4,'state':'COMMITTED','effect':'CONFIRMED','readback_verified':True,'output_sha256':'b'*64,'permission_revoked_after_commit':True,'error':'PERMISSION_REVOKED'}
        transition(self.r,dispatched);transition(dispatched,started);transition(started,committed)
        self.assertEqual(receipt(committed)['state'],'COMMITTED')

    def test_ack_lost_and_unknown_never_auto_retry(self):
        dispatched={**self.r,'state':'DISPATCHED','sequence':2}
        unknown={**dispatched,'state':'UNKNOWN','sequence':3,'error':'ACK_LOST','effect':'UNKNOWN'}
        transition(self.r,dispatched);transition(dispatched,unknown)
        with self.assertRaises(LockError):transition(unknown,{**dispatched,'sequence':4})
        unknown['state']='COMMITTED'
        with self.assertRaises(LockError):receipt(unknown)

    def test_operation_destination_generation_and_sequence_bound(self):
        for key,value in [('operation_sha256','c'*64),('destination_ref','00000000-0000-4000-8000-000000000009'),('generation',2),('sequence',4)]:
            changed={**self.r,'state':'DISPATCHED','sequence':2,key:value}
            with self.assertRaises(LockError):transition(self.r,changed)

    def test_commit_requires_confirmation_and_exact_readback(self):
        self.r.update(state='COMMITTED',authorization_at_commit='GRANTED',effect='CONFIRMED',output_sha256='b'*64,readback_verified=True,confirmation_consumed=True)
        receipt(self.r)
        for key,value in [('confirmation_consumed',False),('readback_verified',False),('output_sha256','')]:
            with self.assertRaises(LockError):receipt({**self.r,key:value})

    def test_collector_ready_or_missing_capability_proof_is_not_product_ready(self):
        capability(self.c,self.lock)
        self.c.update(state='READY',reason='VERIFIED_PRODUCT')
        with self.assertRaises(LockError):capability(self.c,self.lock)
        self.c['proof_ids']=['nexus-jvm-linux']
        with self.assertRaises(LockError):capability(self.c,self.lock)

    def test_wrong_build_and_personal_fields_refused(self):
        self.c['build_commit']='0'*40
        with self.assertRaises(LockError):capability(self.c,self.lock)
        self.r['prompt']='SYNTHETIC_FORBIDDEN_FIELD'
        with self.assertRaises(ValueError):receipt(self.r)
