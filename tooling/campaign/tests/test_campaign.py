import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from tooling.campaign.manifest import CampaignManifestReader, CampaignError
from tooling.campaign.dag import MissionDAGResolver
from tooling.campaign.ownership import OwnershipConflictDetector, OwnershipPolicy
from tooling.campaign.status import EvidenceGateEvaluator, MissionStatusMachine
from tooling.campaign.cli import report, main

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "docs/intensive-2026-10-22/MISSIONS.json"


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.value = json.loads(MANIFEST.read_text())
        self.manifest = CampaignManifestReader(copy.deepcopy(self.value))

    def test_real_31_mission_graph(self):
        waves = MissionDAGResolver(self.manifest).waves()
        self.assertEqual(sum(map(len, waves)), 31)
        self.assertEqual(set(waves[0]), {"CORE-01", "LLM-01", "VOICE-01", "AVA-01", "SERV-01", "NEX-01", "EVOL-01", "UNI-01"})
        done = set()
        for wave in waves:
            for mission in wave:
                self.assertTrue(set(self.manifest.nodes[mission].dependencies) <= done)
            done.update(wave)

    def test_duplicate_and_missing_ids_rejected(self):
        for modify in (lambda x: x["missions"].append(x["missions"][0]), lambda x: x["missions"].pop()):
            value = copy.deepcopy(self.value)
            modify(value)
            with self.assertRaises(CampaignError):
                CampaignManifestReader(value)

    def test_unknown_dependency_rejected(self):
        self.value["missions"][0]["dependencies"] = ["UNKNOWN-01"]
        with self.assertRaises(CampaignError):
            CampaignManifestReader(self.value)

    def test_changed_owner_and_replacement_id_rejected(self):
        value = copy.deepcopy(self.value)
        value["missions"][0]["repository"] = "bubth720/JARVIS-LLM"
        with self.assertRaises(CampaignError):
            CampaignManifestReader(value)
        value = copy.deepcopy(self.value)
        value["missions"][0]["id"] = "CORE-99"
        value["missions"][0]["path"] = "docs/intensive-2026-10-22/CORE-99.md"
        with self.assertRaises(CampaignError):
            CampaignManifestReader(value)

    def test_cycle_rejected(self):
        self.value["missions"][0]["dependencies"] = ["CORE-02"]
        with self.assertRaises(CampaignError):
            MissionDAGResolver(CampaignManifestReader(self.value)).waves()

    def test_unknown_version_repository_and_path_rejected(self):
        for key, value in (("version", 99), ("version", True)):
            modified = copy.deepcopy(self.value)
            modified[key] = value
            with self.assertRaises(CampaignError):
                CampaignManifestReader(modified)
        self.value["missions"][0]["repository"] = "bubth720/UNKNOWN"
        with self.assertRaises(CampaignError):
            CampaignManifestReader(self.value)

    def test_shared_repository_collision_even_different_files(self):
        assignments = [{"mission": "CORE-01", "owner": "one", "branch": "feat/core-01"},
                       {"mission": "MEM-01", "owner": "two", "branch": "feat/memory"}]
        with self.assertRaises(CampaignError):
            OwnershipConflictDetector.check(self.manifest, assignments)

    def test_independent_repositories_accepted(self):
        assignments = [{"mission": "CORE-01", "owner": "one", "branch": "feat/core-01"},
                       {"mission": "LLM-01", "owner": "two", "branch": "feat/llm-01"}]
        self.assertTrue(OwnershipConflictDetector.check(self.manifest, assignments))

    def test_main_and_branch_traversal_rejected(self):
        for branch in ("main", "feat/../main", "feat/a.lock", "feat/a b", "feat/a.lock/b", "feat/.hidden"):
            with self.assertRaises(CampaignError):
                OwnershipConflictDetector.check(self.manifest, [{"mission": "CORE-01", "owner": "one", "branch": branch}])

    def test_sensitive_changes_require_separate_authorization(self):
        with self.assertRaises(CampaignError):
            OwnershipPolicy.check_changes(["jni"], [])
        OwnershipPolicy.check_changes(["jni"], ["jni"])
        with self.assertRaises(CampaignError):
            OwnershipPolicy.check_changes(["unknown"], [])

    def test_missing_proof_never_delivered(self):
        machine = MissionStatusMachine(self.manifest, EvidenceGateEvaluator(self.manifest, {}))
        with self.assertRaises(CampaignError):
            machine.transition("CORE-01", "DELIVERED")
        machine.transition("CORE-01", "ASSIGNED", owner="one", branch="feat/core-01")
        machine.transition("CORE-01", "IN_PROGRESS")
        with self.assertRaises(CampaignError):
            machine.transition("CORE-01", "DELIVERED", evidence={})
        self.assertEqual(machine.status("CORE-01"), "IN_PROGRESS")

    def test_dependency_not_delivered_blocks_assignment(self):
        machine = MissionStatusMachine(self.manifest, EvidenceGateEvaluator(self.manifest, {}))
        with self.assertRaises(CampaignError):
            machine.transition("CORE-02", "ASSIGNED", owner="one", branch="feat/core-02")

    def test_manual_blockers_and_decisions_preserved(self):
        machine = MissionStatusMachine(self.manifest, EvidenceGateEvaluator(self.manifest, {}))
        machine.transition("CORE-01", "BLOCKED", blockers=["Hardware not qualified"], decisions=["No JNI authorization"])
        machine.transition("CORE-01", "ASSIGNED", owner="one", branch="feat/core-01")
        machine.transition("CORE-01", "IN_PROGRESS")
        self.assertEqual(machine.records["CORE-01"]["blockers"], ["Hardware not qualified"])
        self.assertEqual(machine.records["CORE-01"]["decisions"], ["No JNI authorization"])

    def test_repeated_reporting_has_no_duplicates_or_mutation(self):
        state = {"CORE-01": {"status": "BLOCKED", "blockers": ["Await qualification"], "decisions": ["No installation"]}}
        before = copy.deepcopy(state)
        first = report(self.manifest, state, {})
        self.assertEqual(first, report(self.manifest, state, {}))
        self.assertEqual(state, before)
        self.assertNotIn("CORE-01", first["ready"])
        self.assertEqual(first["manual_decisions"]["CORE-01"], ["No installation"])

    def test_cli_commands_execute_without_connection(self):
        for args in (["list-ready"], ["list-blocked"], ["export-wave", "--wave", "0"],
                     ["explain-mission", "--mission", "CORE-03"], ["report", "--markdown"]):
            completed = subprocess.run(["python3", "-m", "tooling.campaign.cli", *args], cwd=ROOT, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stdout)


class GitEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="jarvis-campaign-test-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Synthetic Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.path / "code.txt").write_text("Synthetic fixture, not an application\n")
        self.commit("base")
        self.base = self.git("rev-parse", "HEAD").strip()
        value = json.loads(MANIFEST.read_text())
        for repo in value["repositories"]:
            if repo["repository"] == "bubth720/JAVIS-Local-v2":
                repo["planning_commit"] = self.base
        self.manifest = CampaignManifestReader(value)
        self.evaluator = EvidenceGateEvaluator(self.manifest, {"bubth720/JAVIS-Local-v2": self.path})
        self.receipt = {"format": "jarvis.campaign-validation/1", "mission": "CORE-01", "base_commit": self.base,
                        "qualification": "software_tested", "capabilities": ["fixture.lookup"],
                        "checks": [{"command": ["synthetic-fixture-test"], "exit_code": 0, "passed": 1, "failed": 0, "skipped": 0}]}
        self.write_evidence()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.path), *args], stderr=subprocess.PIPE).decode()

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-q", "-m", message)

    def write_evidence(self):
        (self.path / "REPORT.md").write_text("Synthetic test evidence; not a real module delivery.\n")
        (self.path / "VALIDATION.json").write_text(json.dumps(self.receipt))
        self.commit("fixture evidence")
        self.evidence = {"commit": self.git("rev-parse", "HEAD").strip(), "report": "REPORT.md", "receipt": "VALIDATION.json",
                         "report_sha256": hashlib.sha256((self.path / "REPORT.md").read_bytes()).hexdigest(),
                         "receipt_sha256": hashlib.sha256((self.path / "VALIDATION.json").read_bytes()).hexdigest()}

    def test_commit_report_receipt_and_ancestry_verified(self):
        capability = self.evaluator.verify("CORE-01", self.evidence)
        self.assertEqual(capability.capabilities, ("fixture.lookup",))
        machine = MissionStatusMachine(self.manifest, self.evaluator)
        machine.transition("CORE-01", "ASSIGNED", owner="one", branch="feat/core-01")
        machine.transition("CORE-01", "IN_PROGRESS")
        machine.transition("CORE-01", "DELIVERED", evidence=self.evidence)
        self.assertEqual(machine.delivered(), {"CORE-01"})

    def test_wrong_hash_and_nonexistent_commit_rejected(self):
        for key, value in (("commit", "f" * 40), ("report_sha256", "0" * 64), ("receipt_sha256", "0" * 64)):
            evidence = {**self.evidence, key: value}
            with self.assertRaises(CampaignError):
                self.evaluator.verify("CORE-01", evidence)

    def test_failed_skipped_zero_or_boolean_check_rejected(self):
        for key, value in (("failed", 1), ("skipped", 1), ("passed", 0), ("passed", True), ("exit_code", 1)):
            receipt = copy.deepcopy(self.receipt)
            receipt["checks"][0][key] = value
            self.receipt = receipt
            self.write_evidence()
            with self.assertRaises(CampaignError):
                self.evaluator.verify("CORE-01", self.evidence)
            self.receipt["checks"][0].update(exit_code=0, passed=1, failed=0, skipped=0)

    def test_physical_claim_and_wrong_mission_rejected(self):
        self.receipt["qualification"] = "physical_verified"
        self.write_evidence()
        with self.assertRaises(CampaignError):
            self.evaluator.verify("CORE-01", self.evidence)

    def test_successful_build_and_demo_are_not_fabricated_test_counts(self):
        self.receipt["checks"].extend([
            {"command": ["synthetic-build"], "exit_code": 0, "passed": 0, "failed": 0, "skipped": 0, "kind": "build_lint", "lint_errors": 0},
            {"command": ["synthetic-demo"], "exit_code": 0, "passed": 0, "failed": 0, "skipped": 0, "kind": "functional_demo", "observed": ["Synthetic fixture output inspected"]}])
        self.write_evidence()
        self.assertEqual(self.evaluator.verify("CORE-01", self.evidence).mission, "CORE-01")

    def test_build_only_receipt_does_not_unlock_mission(self):
        self.receipt["checks"] = [{"command": ["synthetic-build"], "exit_code": 0, "passed": 0, "failed": 0, "skipped": 0, "kind": "build_lint", "lint_errors": 0}]
        self.write_evidence()
        with self.assertRaises(CampaignError):
            self.evaluator.verify("CORE-01", self.evidence)

    def test_partial_receipt_does_not_unlock_dependencies(self):
        self.receipt["status"] = "PARTIAL"
        self.receipt["blocking_limitations"] = ["Native tokenizer unavailable"]
        self.write_evidence()
        with self.assertRaises(CampaignError):
            self.evaluator.verify("CORE-01", self.evidence)

    def test_derived_base_is_accepted_only_with_verified_ancestry(self):
        self.receipt["base_commit"] = self.evidence["commit"]
        self.write_evidence()
        self.assertEqual(self.evaluator.verify("CORE-01", self.evidence).mission, "CORE-01")

    def test_sibling_branch_delivery_rejected_without_mutating_state(self):
        machine = MissionStatusMachine(self.manifest, self.evaluator)
        machine.transition("CORE-01", "ASSIGNED", owner="one", branch="feat/core-01")
        machine.transition("CORE-01", "IN_PROGRESS")
        machine.transition("CORE-01", "DELIVERED", evidence=self.evidence)
        self.git("checkout", "-q", "-b", "sibling", self.base)
        self.receipt["mission"] = "MEM-01"
        self.write_evidence()
        machine.transition("MEM-01", "ASSIGNED", owner="one", branch="feat/mem-01")
        machine.transition("MEM-01", "IN_PROGRESS")
        before = copy.deepcopy(machine.records)
        with self.assertRaises(CampaignError):
            machine.transition("MEM-01", "DELIVERED", evidence=self.evidence)
        self.assertEqual(machine.records, before)
        self.assertEqual(machine.delivered(), {"CORE-01"})

    def test_unsafe_evidence_path_rejected(self):
        for path in ("../secret", "/secret", "C:\\secret", "HEAD:secret"):
            with self.assertRaises(CampaignError):
                self.evaluator.verify("CORE-01", {**self.evidence, "report": path})

    def test_repository_inaccessible_rejected(self):
        evaluator = EvidenceGateEvaluator(self.manifest, {})
        with self.assertRaises(CampaignError):
            evaluator.verify("CORE-01", self.evidence)

    def test_docs_only_planning_child_preserves_technical_base(self):
        self.git("checkout", "-q", "-b", "planning", self.base)
        doc = self.path / "docs/intensive-2026-10-22/CORE-01.md"
        doc.parent.mkdir(parents=True)
        doc.write_text("Synthetic mission sheet\n")
        self.commit("planning only")
        planning = self.git("rev-parse", "HEAD").strip()
        value = copy.deepcopy(self.manifest.value)
        value["repositories"][0]["planning_commit"] = planning
        manifest = CampaignManifestReader(value)
        evaluator = EvidenceGateEvaluator(manifest, {"bubth720/JAVIS-Local-v2": self.path})
        self.assertEqual(evaluator.verify("CORE-01", self.evidence).mission, "CORE-01")

    def test_non_documentary_planning_child_cannot_bypass_base(self):
        self.git("checkout", "-q", "-b", "planning", self.base)
        (self.path / "code.txt").write_text("Different implementation\n")
        self.commit("not documentation")
        value = copy.deepcopy(self.manifest.value)
        value["repositories"][0]["planning_commit"] = self.git("rev-parse", "HEAD").strip()
        evaluator = EvidenceGateEvaluator(CampaignManifestReader(value), {"bubth720/JAVIS-Local-v2": self.path})
        with self.assertRaises(CampaignError):
            evaluator.verify("CORE-01", self.evidence)

    def test_verification_does_not_modify_git_or_files(self):
        before = (self.git("show-ref"), self.git("status", "--porcelain")) if self.git("branch", "--list").strip() else None
        files = {str(p.relative_to(self.path)): p.read_bytes() for p in self.path.rglob("*") if p.is_file() and ".git" not in p.parts}
        self.evaluator.verify("CORE-01", self.evidence)
        self.assertEqual(before, (self.git("show-ref"), self.git("status", "--porcelain")))
        self.assertEqual(files, {str(p.relative_to(self.path)): p.read_bytes() for p in self.path.rglob("*") if p.is_file() and ".git" not in p.parts})

    def central_receipt(self):
        source = copy.deepcopy(self.evidence)
        receipt = {**self.receipt, "validated_repository": "bubth720/JAVIS-Local-v2",
                   "validated_commit": source["commit"], "source_report_sha256": source["report_sha256"],
                   "source_receipt": {"path": "VALIDATION.json", "sha256": source["receipt_sha256"]}}
        target = self.path / "NORMALIZED.json"
        target.write_text(json.dumps(receipt))
        self.commit("coordinator normalizes historical fixture")
        source.update(receipt="NORMALIZED.json", receipt_sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                      receipt_origin={"repository": "bubth720/JARVIS-UNIFIED", "commit": self.git("rev-parse", "HEAD").strip()})
        value = copy.deepcopy(self.manifest.value)
        value["central_base"] = self.base
        evaluator = EvidenceGateEvaluator(CampaignManifestReader(value), {
            "bubth720/JAVIS-Local-v2": self.path, "bubth720/JARVIS-UNIFIED": self.path})
        return evaluator, source

    def test_central_normalization_preserves_original_source_commit(self):
        evaluator, evidence = self.central_receipt()
        self.assertNotEqual(evidence["commit"], evidence["receipt_origin"]["commit"])
        self.assertEqual(evaluator.verify("CORE-01", evidence).mission, "CORE-01")

    def test_foreign_receipt_origin_and_wrong_subject_rejected(self):
        evaluator, evidence = self.central_receipt()
        bad_origin = copy.deepcopy(evidence)
        bad_origin["receipt_origin"]["repository"] = "bubth720/JARVIS-LLM"
        with self.assertRaises(CampaignError):
            evaluator.verify("CORE-01", bad_origin)
        target = self.path / "NORMALIZED.json"
        receipt = json.loads(target.read_text())
        receipt["validated_commit"] = self.base
        target.write_text(json.dumps(receipt))
        self.commit("invalid subject fixture")
        evidence["receipt_origin"]["commit"] = self.git("rev-parse", "HEAD").strip()
        evidence["receipt_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        with self.assertRaises(CampaignError):
            evaluator.verify("CORE-01", evidence)

    def test_normalized_receipt_checks_original_receipt_digest_too(self):
        evaluator, evidence = self.central_receipt()
        target = self.path / "NORMALIZED.json"
        receipt = json.loads(target.read_text())
        receipt["source_receipt"]["sha256"] = "0" * 64
        target.write_text(json.dumps(receipt))
        self.commit("wrong historical receipt hash fixture")
        evidence["receipt_origin"]["commit"] = self.git("rev-parse", "HEAD").strip()
        evidence["receipt_sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
        with self.assertRaises(CampaignError):
            evaluator.verify("CORE-01", evidence)


if __name__ == "__main__":
    unittest.main()
