"""Fail-closed UNI-08 candidate audits. Fixtures are synthetic copies."""
import copy
import tempfile
import unittest
from pathlib import Path

from tooling.integration.uni08_candidate import CandidateError, MODULES, load_file, validate

HERE = Path(__file__).resolve().parents[3]
CANDIDATE = HERE / "docs" / "uni-08" / "BOM-PROPOSED.json"


class CandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = load_file(CANDIDATE)

    def value(self):
        return copy.deepcopy(self.source)

    def rejected(self, mutate):
        d = self.value()
        mutate(d)
        with self.assertRaises(CandidateError):
            validate(d)

    def test_eight_real_repositories_are_identified(self):
        v = validate(self.value())
        self.assertEqual(len(v["modules"]), len(MODULES))
        self.assertEqual({m["id"] for m in v["modules"]}, set(MODULES))

    def test_never_grants_release_or_runtime(self):
        v = validate(self.value())
        self.assertEqual(v["verdict"], "BLOCKED")
        self.assertFalse(v["android_multi_module_go"])
        self.assertFalse(v["authorization_granted"])
        self.assertFalse(v["github_bytes_verified_now"])

    def test_real_success_not_global_success(self):
        v = {m["id"]: m for m in validate(self.value())["modules"]}
        self.assertEqual(v["core"]["ci_review"], "SOFTWARE_CI_SUCCESS_ONLY")
        self.assertEqual(v["services"]["ci_review"], "FAILED")
        self.assertEqual(v["voice"]["ci_review"], "MIXED")
        self.assertEqual(v["nexus"]["ci_review"], "UNKNOWN")
        self.assertEqual(v["llm"]["ci_review"], "STALE_ONLY")

    def test_forbid_claim_ready(self):
        self.rejected(lambda d: d.__setitem__("decision", "READY"))

    def test_forbid_claimed_lower_sdk(self):
        self.rejected(lambda d: d["modules"][1].__setitem__("min_sdk", 24))

    def test_forbid_duplicate_module(self):
        self.rejected(lambda d: d["modules"][1].__setitem__("id", d["modules"][0]["id"]))

    def test_forbid_duplicate_run_id(self):
        def f(d):
            d["modules"][0]["ci_observations"].append(copy.deepcopy(d["modules"][0]["ci_observations"][0]))
        self.rejected(f)

    def test_forbid_emulator_e2e_claim(self):
        self.rejected(lambda d: d["modules"][0].__setitem__("android_e2e_attested", True))

    def test_forbid_false_android_go(self):
        self.rejected(lambda d: d.__setitem__("android_multi_module_go", True))

    def test_forbid_false_approval(self):
        self.rejected(lambda d: d.__setitem__("human_approved", True))

    def test_forbid_main_as_candidate(self):
        self.rejected(lambda d: d["modules"][0].__setitem__("candidate_branch", "main"))

    def test_forbid_missing_module(self):
        self.rejected(lambda d: d["modules"].pop())

    def test_forbid_module_runtime_claim(self):
        self.rejected(lambda d: d["modules"][0].__setitem__("runtime_link_attested", True))

    def test_forbid_physical_claim(self):
        self.rejected(lambda d: d["modules"][0].__setitem__("physical_attested", True))

    def test_forbid_run_of_another_repo(self):
        def f(d):
            d["modules"][0]["ci_observations"][0]["url"] = "https://github.com/other/repo/actions/runs/40287287330"
        self.rejected(f)

    def test_forbid_wrong_repo(self):
        self.rejected(lambda d: d["modules"][0].__setitem__("repository", "bubth720/FAKE"))

    def test_forbid_wrong_sha_length(self):
        self.rejected(lambda d: d["modules"][0].__setitem__("candidate_sha", "f6a3b2d"))

    def test_do_not_count_parent_ci_as_candidate_ci(self):
        d = self.value()
        llm = next(m for m in d["modules"] if m["id"] == "llm")
        self.assertNotEqual(llm["candidate_sha"], llm["ci_observations"][0]["commit"])
        v = {m["id"]: m for m in validate(d)["modules"]}
        self.assertEqual(v["llm"]["ci_review"], "STALE_ONLY")

    def test_do_not_count_same_sha_mixed_ci_as_green(self):
        d = self.value()
        v = {m["id"]: m for m in validate(d)["modules"]}
        self.assertEqual(v["voice"]["ci_review"], "MIXED")

    def test_refuse_unknown_json_keys(self):
        self.rejected(lambda d: d.__setitem__("automatic_merge", True))

    def test_strict_duplicate_json_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"a":1,"a":2}')
            with self.assertRaises(CandidateError):
                load_file(path)

    def test_refuse_nan(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"x": NaN}')
            with self.assertRaises(CandidateError):
                load_file(path)

    def test_refuse_oversized_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "large.json"
            path.write_bytes(b' ' * (1024 * 1024 + 1))
            with self.assertRaises(CandidateError):
                load_file(path)


if __name__ == "__main__":
    unittest.main()
