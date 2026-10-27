"""Negative fixtures for prerelease consolidation; pure standard library."""
import unittest
from copy import deepcopy
from pathlib import Path
from tooling.prefusion.check_lot2 import check,load,EvidenceError

PATH=Path(__file__).resolve().parents[3]/"docs/prefusion/LOT2-EVIDENCE.json"

class Lot2EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.data=deepcopy(load(PATH))
    def bad(self):
        with self.assertRaises(EvidenceError):check(self.data)
    def test_valid_is_still_review_only(self):
        x=check(self.data)
        self.assertEqual(x["candidate_prs"],6)
        self.assertFalse(x["android_go"])
        self.assertFalse(x["tested_at_combined_commit"])
    def test_no_main(self):
        self.data["merge_main_allowed"]=True; self.bad()
    def test_no_run(self):
        self.data["runtime_activation_allowed"]=True; self.bad()
    def test_no_approval(self):
        self.data["approved"]=True; self.bad()
    def test_no_monolith_claim(self):
        self.data["code_combined"]=True; self.bad()
    def test_no_physical_claim(self):
        self.data["physical_device_qualified"]=True; self.bad()
    def test_no_android_go(self):
        self.data["release_gates"][0]["status"]="PASS";self.bad()
    def test_no_fake_device_pass(self):
        self.data["release_gates"][4]["status"]="BLOCKED";self.bad()
    def test_no_removed_gate(self):
        self.data["release_gates"].pop();self.bad()
    def test_no_missing_module(self):
        self.data["modules"].pop();self.bad()
    def test_no_duplicate_module(self):
        self.data["modules"][1]["module"]="CORE";self.bad()
    def test_no_duplicate_pr(self):
        self.data["modules"][0]["prs"][1]["number"]=20;self.bad()
    def test_no_fake_sha(self):
        self.data["modules"][0]["prs"][0]["sha"]="abcd";self.bad()
    def test_no_duplicate_run(self):
        self.data["modules"][0]["prs"][1]["run"]=40563102521;self.bad()
    def test_overlapping_file_must_be_reviewed(self):
        p=self.data["modules"][0]["prs"][0]["files"][0]
        self.data["modules"][0]["prs"][1]["files"].append(p);self.bad()
    def test_directory_traversal_not_permitted(self):
        self.data["modules"][0]["prs"][0]["files"].append("../main");self.bad()
    def test_unknown_field_refused(self):
        self.data["auto_merge"]=False;self.bad()
    def test_wrong_repo_refused(self):
        self.data["modules"][2]["repo"]="example/repo";self.bad()
    def test_bad_baseline_refused(self):
        self.data["source_baseline"]["branch"]="main";self.bad()
    def test_zero_ci_refused(self):
        self.data["modules"][0]["prs"][0]["run"]=0;self.bad()

if __name__=="__main__":unittest.main()
