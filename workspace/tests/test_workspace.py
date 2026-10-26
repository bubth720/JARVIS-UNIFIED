"""Safety regressions for proposal only: cannot make a monolith or auto-merge."""
from copy import deepcopy
from pathlib import Path
import unittest
from workspace.check_plan import PlanError, check, load

FILE = Path(__file__).resolve().parents[1] / "modular-workspace.proposed.json"

class WorkspacePlanTests(unittest.TestCase):
    def setUp(self):
        self.plan=deepcopy(load(FILE))

    def reject(self):
        with self.assertRaises(PlanError):
            check(self.plan)

    def test_proposed_manifest_valid_but_never_authorized(self):
        x=check(self.plan)
        self.assertEqual(x["validated_modules"],8)
        self.assertEqual(x["runtime_links_enabled"],0)
        self.assertFalse(x["merge_authorized"])
        self.assertFalse(x["remote_shas_reverified_now"])

    def test_activation_refused(self):
        self.plan["runtime_enabled"]=True
        self.reject()

    def test_approval_refused(self):
        self.plan["approved"]=True
        self.reject()

    def test_checkout_refused(self):
        self.plan["automated_checkout_enabled"]=True
        self.reject()

    def test_qualified_apk_refused(self):
        self.plan["unified_apk_qualified"]=True
        self.reject()

    def test_global_android_go_refused(self):
        self.plan["android_multi_module_go"]=True
        self.reject()

    def test_default_main_disallowed(self):
        self.plan["modules"][0]["branch"]="main"
        self.reject()

    def test_commit_is_full_sha(self):
        self.plan["modules"][0]["commit"]="f6a3b2d"
        self.reject()

    def test_wrong_repo_refused(self):
        self.plan["modules"][0]["repository"]="bubth720/not-real"
        self.reject()

    def test_android_version_cannot_be_faked(self):
        self.plan["modules"][1]["min_sdk"]=24
        self.reject()

    def test_duplicate_module_refused(self):
        self.plan["modules"][1]=deepcopy(self.plan["modules"][0])
        self.reject()

    def test_unknown_module_refused(self):
        self.plan["modules"][1]["id"]="extra"
        self.reject()

    def test_enabled_edge_refused(self):
        self.plan["proposed_dependencies"][0]["enabled"]=True
        self.reject()

    def test_cross_owner_unified_runtime_refused(self):
        self.plan["proposed_dependencies"][0]["provider"]="unified"
        self.reject()

    def test_cycle_refused(self):
        self.plan["proposed_dependencies"].append({
            "consumer":"voice","provider":"core","role":"speech","enabled":False})
        self.reject()

    def test_self_edge_refused(self):
        self.plan["proposed_dependencies"][0]["provider"]="interface"
        self.reject()

    def test_invented_go_gate_refused(self):
        self.plan["gates"][0]["state"]="PASS"
        self.reject()

    def test_missing_gate_refused(self):
        self.plan["gates"].pop()
        self.reject()

    def test_extra_field_refused(self):
        self.plan["auto_merge"]=True
        self.reject()

    def test_unknown_role_refused(self):
        self.plan["proposed_dependencies"][0]["role"]="delete_storage"
        self.reject()

if __name__ == "__main__":
    unittest.main()
