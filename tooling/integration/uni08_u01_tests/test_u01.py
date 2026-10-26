"""Isolated tests; no Android or producer claim."""
import unittest
from copy import deepcopy
from tooling.integration.uni08_u01 import MAX_GENERATION, review

BASE = dict(format="jarvis.uni08-u01-review/1",
    session="123e4567-e89b-42d3-a456-426614174000",
    request="123e4567-e89b-42d3-a456-426614174001", generation=1,
    operation="export.csv", source_digest="a"*64, content_digest="b"*64,
    destination="tree:synthetic/new.csv", local_state="PREPARED", wire_state="PREPARED",
    host_grant_attested=True, readback_attested=False)

class TestU01(unittest.TestCase):
    def case(self, field=None, value=None):
        p=deepcopy(BASE)
        if field: p[field]=value
        return review(p)
    def test_never_grants_authority(self):
        x=self.case(); self.assertEqual(x.disposition,"BLOCKED"); self.assertFalse(x.runtime_authorized); self.assertFalse(x.wire_receipt_created)
    def test_zero_generation_refused(self): self.assertIn("GENERATION_NOT_WIRE_SAFE",self.case("generation",0).blockers)
    def test_negative_generation_refused(self): self.assertIn("GENERATION_NOT_WIRE_SAFE",self.case("generation",-1).blockers)
    def test_bool_generation_refused(self): self.assertIn("GENERATION_NOT_WIRE_SAFE",self.case("generation",True).blockers)
    def test_out_of_range_generation_refused(self): self.assertIn("GENERATION_NOT_WIRE_SAFE",self.case("generation",MAX_GENERATION+1).blockers)
    def test_max_generation_not_authority(self): self.assertEqual(self.case("generation",MAX_GENERATION).disposition,"BLOCKED")
    def test_commit_started_is_not_dispatched(self):
        p=dict(BASE,local_state="COMMIT_STARTED",wire_state="DISPATCHED"); self.assertIn("NON_EQUIVALENT_COMMIT_STATES",review(p).blockers)
    def test_refusal_never_mapped_to_wire(self):
        p=dict(BASE,local_state="REFUSED",wire_state="UNKNOWN"); self.assertIn("REFUSAL_HAS_NO_WIRE_STATE",review(p).blockers)
    def test_legacy_completed_unknown(self): self.assertIn("UNKNOWN_STATE",self.case("local_state","COMPLETED").blockers)
    def test_durable_readback_required(self):
        p=dict(BASE,local_state="COMMITTED",wire_state="COMMITTED"); self.assertIn("DURABLE_READBACK_NOT_ATTESTED",review(p).blockers)
    def test_even_attested_readback_not_release(self):
        p=dict(BASE,local_state="COMMITTED",wire_state="COMMITTED",readback_attested=True)
        self.assertIn("HUMAN_REVIEW_AND_RUNTIME_INTEGRATION_NOT_APPROVED",review(p).blockers)
    def test_no_grant_refused(self): self.assertIn("CORE_AUTHORITY_NOT_ATTESTED",self.case("host_grant_attested",False).blockers)
    def test_invalid_uuid_refused(self): self.assertIn("INVALID_CORRELATION",self.case("request","not-a-uuid").blockers)
    def test_digest_refused(self): self.assertIn("DIGEST_INVALID",self.case("source_digest","FF"*32).blockers)
    def test_unknown_operation_refused(self): self.assertIn("OPERATION_NOT_ALLOWLISTED",self.case("operation","delete.all").blockers)
    def test_destination_null_refused(self): self.assertIn("DESTINATION_INVALID",self.case("destination","x\x00y").blockers)
    def test_extra_field_refused(self):
        p=dict(BASE,enabled=True); self.assertEqual(review(p).blockers,("MALFORMED_INPUT",))
    def test_missing_field_refused(self):
        p=dict(BASE);del p["request"];self.assertEqual(review(p).blockers,("MALFORMED_INPUT",))
    def test_wrong_type_refused(self): self.assertEqual(review([]).blockers,("MALFORMED_INPUT",))
    def test_unhashable_operation_refused(self): self.assertIn("OPERATION_NOT_ALLOWLISTED",self.case("operation",[]).blockers)
    def test_unhashable_state_refused(self): self.assertIn("UNKNOWN_STATE",self.case("local_state",{}).blockers)
    def test_ill_formed_unicode_refused(self): self.assertIn("DESTINATION_INVALID",self.case("destination","\ud800").blockers)
    def test_timestamp_or_replay_not_validated(self):
        self.assertIn("HUMAN_REVIEW_AND_RUNTIME_INTEGRATION_NOT_APPROVED", self.case().blockers)

if __name__=='__main__':unittest.main()
