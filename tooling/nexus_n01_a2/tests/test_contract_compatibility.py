"""Real existing validators, synthetic candidate messages. No contract edits."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from scripts.contracts import ContractError,validate_contract
from tooling.integration.uni08_u01 import review,MAX_GENERATION

ROOT=Path(__file__).resolve().parents[3]
SCHEMA=json.loads((ROOT/'contracts/v1/request-envelope.schema.json').read_text())
VALID=json.loads((ROOT/'contracts/v1/examples/request-envelope.valid.json').read_text())

def receipt():
    return dict(format='jarvis.uni08-u01-review/1',session='00000000-0000-4000-8000-000000000001',request='00000000-0000-4000-8000-000000000002',generation=1,operation='export.csv',source_digest='a'*64,content_digest='b'*64,destination='synthetic-empty-destination',local_state='PREPARED',wire_state='PREPARED',host_grant_attested=True,readback_attested=True)

class ContractCompatibilityTest(unittest.TestCase):
    def test_historical_valid_request_still_validates(self):
        self.assertTrue(validate_contract('request-envelope',deepcopy(VALID),SCHEMA))
    def test_existing_document_retrieve_shape_is_retained(self):
        request=deepcopy(VALID);request.update(destination='nexus',capability='document.retrieve')
        self.assertTrue(validate_contract('request-envelope',request,SCHEMA))
    def test_research_is_not_an_existing_wire_module(self):
        request=deepcopy(VALID);request['destination']='research'
        with self.assertRaises(ContractError):validate_contract('request-envelope',request,SCHEMA)
    def test_profiles_and_vault_are_not_existing_wire_modules(self):
        for module in ('profiles','data_vault'):
            with self.subTest(module=module):
                request=deepcopy(VALID);request['destination']=module
                with self.assertRaises(ContractError):validate_contract('request-envelope',request,SCHEMA)
    def test_research_collect_is_not_an_existing_wire_capability(self):
        request=deepcopy(VALID);request['capability']='research.collect'
        with self.assertRaises(ContractError):validate_contract('request-envelope',request,SCHEMA)
    def test_n01_metadata_cannot_be_appended_to_closed_payload(self):
        for key,value in {'mission_id':'synthetic','policy_revision':1,'raw_sha256':'a'*64,'licence':'CC0','authority_ref':'synthetic'}.items():
            with self.subTest(key=key):
                request=deepcopy(VALID);request['payload'][key]=value
                with self.assertRaises(ContractError):validate_contract('request-envelope',request,SCHEMA)
    def test_top_level_mission_cannot_be_added(self):
        request=deepcopy(VALID);request['mission_id']='synthetic'
        with self.assertRaises(ContractError):validate_contract('request-envelope',request,SCHEMA)
    def test_generation_zero_and_long_overflow_have_no_automatic_mapping(self):
        for generation in (0,-1,MAX_GENERATION+1,True):
            with self.subTest(generation=generation):
                candidate=receipt();candidate['generation']=generation
                self.assertIn('GENERATION_NOT_WIRE_SAFE',review(candidate).blockers)
    def test_commit_started_is_not_dispatched(self):
        candidate=receipt();candidate.update(local_state='COMMIT_STARTED',wire_state='DISPATCHED')
        self.assertIn('NON_EQUIVALENT_COMMIT_STATES',review(candidate).blockers)
    def test_completed_is_not_committed(self):
        candidate=receipt();candidate.update(local_state='COMPLETED',wire_state='COMMITTED')
        self.assertIn('UNKNOWN_STATE',review(candidate).blockers)
    def test_missing_host_grant_is_blocked(self):
        candidate=receipt();candidate['host_grant_attested']=False
        self.assertIn('CORE_AUTHORITY_NOT_ATTESTED',review(candidate).blockers)
    def test_valid_synthetic_receipt_does_not_authorize_runtime(self):
        verdict=review(receipt())
        self.assertEqual('BLOCKED',verdict.disposition)
        self.assertFalse(verdict.runtime_authorized);self.assertFalse(verdict.wire_receipt_created)
    def test_oversized_v1_timeout_is_not_a_long_mission_extension(self):
        request=deepcopy(VALID);request['limits']['timeout_ms']=3_600_000
        with self.assertRaises(ContractError):validate_contract('request-envelope',request,SCHEMA)

if __name__=='__main__':unittest.main()
