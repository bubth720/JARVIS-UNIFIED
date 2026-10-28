import copy
import unittest
from tooling.integration.adr002_lot4 import review, WIRE_MAX_GENERATION

U = lambda n: f"00000000-0000-4000-8000-{n:012x}"
H = "a" * 64


def fixture():
    return {
        "format": "jarvis.adr002.lot4.synthetic-trace/1",
        "epoch": U(1), "session": U(2), "request": U(3),
        "generation": 1, "operation": "export.csv",
        "source_digest": "b" * 64, "content_digest": H,
        "destination": "fixture://new.csv",
        "events": [
            {"owner": "CORE", "sequence": 1, "state": "PREPARED"},
            {"owner": "SERVICES", "sequence": 1, "state": "DISPATCHED"},
            {"owner": "CORE", "sequence": 2, "state": "CONSENT_CONSUMED"},
            {"owner": "SERVICES", "sequence": 2, "state": "COMMIT_STARTED"},
            {"owner": "SERVICES", "sequence": 3, "state": "COMMITTED"},
        ],
        "readback": {"closed": True, "acknowledged": True,
                     "source_unchanged": True, "destination_digest": H,
                     "destination_identity": "fixture://new.csv"},
    }


class SafetyTests(unittest.TestCase):
    def assertDenied(self, x, reason):
        v = review(x)
        self.assertIn(reason, v.blockers)
        self.assertFalse(v.runtime_authorized)
        self.assertFalse(v.issued_token)
        self.assertFalse(v.remote_identity_verified)
        self.assertFalse(v.durable_two_journal_commit_proven)
        self.assertFalse(v.allow_retry)
        self.assertFalse(v.allow_mutation)

    def test_valid_synthetic_remains_review_only(self):
        v = review(fixture())
        self.assertEqual(v.state, "REVIEW_ONLY")
        self.assertDenied(fixture(), "REVIEW_ONLY_NO_REAL_CORE_OR_DURABILITY")

    def test_unknown_is_not_success_or_retry(self):
        x = fixture()
        x["events"][-1]["state"] = "UNKNOWN"
        self.assertDenied(x, "UNKNOWN_STICKY_NO_RETRY")

    def test_gen_zero(self):
        x = fixture(); x["generation"] = 0
        self.assertDenied(x, "GENERATION_INCOMPATIBLE")

    def test_gen_over_limit(self):
        x = fixture(); x["generation"] = WIRE_MAX_GENERATION + 1
        self.assertDenied(x, "GENERATION_INCOMPATIBLE")

    def test_gen_bool(self):
        x = fixture(); x["generation"] = True
        self.assertDenied(x, "GENERATION_INCOMPATIBLE")

    def test_unrecognized_format(self):
        x = fixture(); x["format"] = "old"
        self.assertDenied(x, "VERSION_UNSUPPORTED")

    def test_forged_authority_field(self):
        x = fixture(); x["authorized"] = True
        self.assertDenied(x, "SCHEMA_INVALID")

    def test_invalid_epoch(self):
        x = fixture(); x["epoch"] = "not-authenticated"
        self.assertDenied(x, "IDENTITY_INVALID")

    def test_invalid_digest(self):
        x = fixture(); x["source_digest"] = "x"
        self.assertDenied(x, "DIGEST_INVALID")

    def test_invalid_operation(self):
        x = fixture(); x["operation"] = "delete.document"
        self.assertDenied(x, "OPERATION_INVALID")

    def test_dangerous_destination(self):
        x = fixture(); x["destination"] = "path\n../file"
        self.assertDenied(x, "DESTINATION_INVALID")

    def test_core_prepared_missing(self):
        x = fixture(); x["events"].pop(0)
        self.assertDenied(x, "DISPATCH_INVALID")

    def test_consent_missing(self):
        x = fixture(); x["events"].pop(2)
        x["events"][2]["sequence"] = 2
        self.assertDenied(x, "COMMIT_BARRIER_FAILED")

    def test_revoked_before_commit(self):
        x = fixture()
        x["events"].insert(3, {"owner": "CORE", "sequence": 3, "state": "REVOKED"})
        self.assertDenied(x, "COMMIT_BARRIER_FAILED")

    def test_cancelled_before_commit(self):
        x = fixture()
        x["events"].insert(3, {"owner": "CORE", "sequence": 3, "state": "CANCELLED"})
        self.assertDenied(x, "COMMIT_BARRIER_FAILED")

    def test_duplicate_consent(self):
        x = fixture()
        x["events"].insert(3, {"owner": "CORE", "sequence": 3, "state": "CONSENT_CONSUMED"})
        self.assertDenied(x, "CONSENT_UNAUTHORIZED")

    def test_reordered_journal(self):
        x = fixture(); x["events"][2]["sequence"] = 3
        self.assertDenied(x, "SEQUENCE_INVALID")

    def test_comitted_without_start(self):
        x = fixture(); x["events"].pop(3)
        x["events"][-1]["sequence"] = 2
        self.assertDenied(x, "COMMITTED_UNPROVEN")

    def test_no_close(self):
        x = fixture(); x["readback"]["closed"] = False
        self.assertDenied(x, "COMMITTED_LACKS_FULL_READBACK")

    def test_no_ack(self):
        x = fixture(); x["readback"]["acknowledged"] = False
        self.assertDenied(x, "COMMITTED_LACKS_FULL_READBACK")

    def test_changed_source(self):
        x = fixture(); x["readback"]["source_unchanged"] = False
        self.assertDenied(x, "COMMITTED_LACKS_FULL_READBACK")

    def test_truncated_readback(self):
        x = fixture(); x["readback"]["destination_digest"] = "c" * 64
        self.assertDenied(x, "COMMITTED_LACKS_FULL_READBACK")

    def test_wrong_destination(self):
        x = fixture(); x["readback"]["destination_identity"] = "fixture://other.csv"
        self.assertDenied(x, "COMMITTED_LACKS_FULL_READBACK")

    def test_unknown_followed_by_success_is_rejected(self):
        x = fixture()
        x["events"][-1]["state"] = "UNKNOWN"
        x["events"].append({"owner": "SERVICES", "sequence": 4, "state": "COMMITTED"})
        self.assertDenied(x, "AFTER_TERMINAL")

    def test_missing_readback_field(self):
        x = fixture(); del x["readback"]["closed"]
        self.assertDenied(x, "READBACK_SCHEMA_INVALID")

    def test_empty_history(self):
        x = fixture(); x["events"] = []
        self.assertDenied(x, "EVENTS_INVALID")

    def test_duplicate_prepared(self):
        x = fixture()
        x["events"].insert(1, {"owner": "CORE", "sequence": 2, "state": "PREPARED"})
        x["events"][3]["sequence"] = 3
        self.assertDenied(x, "REPLAY_PREPARE")

    def test_external_owner(self):
        x = fixture(); x["events"][1]["owner"] = "LLM"
        self.assertDenied(x, "JOURNAL_OWNER_INVALID")


if __name__ == "__main__":
    unittest.main()
