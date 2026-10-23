"""Verify local Git evidence without network, checkout, fetch or test execution."""
from dataclasses import dataclass
import hashlib
from pathlib import Path, PurePosixPath
import re
import subprocess
from tooling.contracts.manifest import strict_json
from .manifest import CampaignError


@dataclass(frozen=True)
class CapabilityManifest:
    mission: str
    capabilities: tuple
    qualification: str


class EvidenceGateEvaluator:
    def __init__(self, manifest, repository_paths):
        self.manifest = manifest
        self.paths = repository_paths

    @staticmethod
    def git(path, *args):
        try:
            return subprocess.check_output(["git", "-C", str(path), *args], stderr=subprocess.PIPE, timeout=15)
        except (OSError, subprocess.SubprocessError) as exc:
            raise CampaignError("Local Git evidence unavailable") from exc

    @staticmethod
    def safe_path(path):
        if not isinstance(path, str) or not path or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts or "\\" in path or ":" in path:
            raise CampaignError("Unsafe evidence path")
        return path

    def verify(self, mission, evidence):
        node = self.manifest.nodes[mission]
        fields = {"commit", "report", "report_sha256", "receipt", "receipt_sha256"}
        if set(evidence) not in (fields, fields | {"receipt_origin"}):
            raise CampaignError("Invalid evidence fields")
        commit = evidence["commit"]
        if not isinstance(commit, str) or not re.fullmatch("[0-9a-f]{40}", commit):
            raise CampaignError("Full commit SHA required")
        if node.repository not in self.paths:
            raise CampaignError("Repository not mounted: " + node.repository)
        path = Path(self.paths[node.repository])
        actual = self.git(path, "rev-parse", commit + "^{commit}").decode().strip()
        if actual != commit:
            raise CampaignError("Commit mismatch")
        receipt_path, receipt_commit = path, commit
        if "receipt_origin" in evidence:
            origin = evidence["receipt_origin"]
            central = self.manifest.value["central_repo"]
            if not isinstance(origin, dict) or set(origin) != {"repository", "commit"} or origin["repository"] != central:
                raise CampaignError("Only the central registry can normalize historical receipts")
            if central not in self.paths or not isinstance(origin["commit"], str) or not re.fullmatch("[0-9a-f]{40}", origin["commit"]):
                raise CampaignError("Central receipt repository or full commit missing")
            receipt_path, receipt_commit = Path(self.paths[central]), origin["commit"]
            self.git(receipt_path, "merge-base", "--is-ancestor", self.manifest.references[central].planning_commit, receipt_commit)
        receipt_bytes = self.git(receipt_path, "show", receipt_commit + ":" + self.safe_path(evidence["receipt"]))
        if hashlib.sha256(receipt_bytes).hexdigest() != evidence["receipt_sha256"]:
            raise CampaignError("Receipt digest mismatch")
        receipt = strict_json(receipt_bytes.decode("utf-8"))
        if "receipt_origin" in evidence:
            if receipt.get("validated_repository") != node.repository or receipt.get("validated_commit") != commit or receipt.get("source_report_sha256") != evidence["report_sha256"]:
                raise CampaignError("Central receipt is not bound to the exact source evidence")
            if "source_receipt" in receipt:
                source = receipt["source_receipt"]
                if not isinstance(source, dict) or set(source) != {"path", "sha256"}:
                    raise CampaignError("Invalid historical receipt reference")
                original = self.git(path, "show", commit + ":" + self.safe_path(source["path"]))
                if hashlib.sha256(original).hexdigest() != source["sha256"]:
                    raise CampaignError("Historical receipt digest mismatch")
        planning = self.manifest.references[node.repository].planning_commit
        # Mission sheets may live on a docs-only child of the technical base.
        # Accept that parent only after verifying the exact Git diff; never
        # choose an unrelated newer main or infer ancestry from a branch name.
        allowed_bases = {planning}
        parents = self.git(path, "rev-list", "--parents", "-n", "1", planning).decode().split()
        if len(parents) == 2:
            changes = self.git(path, "diff", "--name-status", parents[1], planning).decode().splitlines()
            if changes and all(line.startswith("A\tdocs/intensive-2026-10-22/") for line in changes):
                allowed_bases.add(parents[1])
        base = receipt.get("base_commit")
        if not isinstance(base, str) or not re.fullmatch("[0-9a-f]{40}", base):
            raise CampaignError("Full base SHA required")
        anchored = False
        for anchor in allowed_bases:
            try:
                self.git(path, "merge-base", "--is-ancestor", anchor, base)
                anchored = True
                break
            except CampaignError:
                pass
        if not anchored:
            raise CampaignError("Unverified technical base")
        self.git(path, "merge-base", "--is-ancestor", base, commit)
        report = self.git(path, "show", commit + ":" + self.safe_path(evidence["report"]))
        if not report.strip() or hashlib.sha256(report).hexdigest() != evidence["report_sha256"] or hashlib.sha256(receipt_bytes).hexdigest() != evidence["receipt_sha256"]:
            raise CampaignError("Evidence digest mismatch")
        if receipt.get("format") != "jarvis.campaign-validation/1" or receipt.get("mission") != mission:
            raise CampaignError("Wrong validation receipt")
        if receipt.get("status", "DELIVERED") != "DELIVERED" or receipt.get("blocking_limitations"):
            raise CampaignError("Partial or blocked mission is not delivered")
        if receipt.get("base_commit") != base:
            raise CampaignError("Receipt base mismatch")
        checks = receipt.get("checks")
        if not isinstance(checks, list) or not checks:
            raise CampaignError("Missing executed checks")
        for check in checks:
            if not isinstance(check, dict) or not isinstance(check.get("command"), list) or not check["command"] or any(not isinstance(s, str) for s in check["command"]):
                raise CampaignError("Invalid validation command")
            if any(type(check.get(k)) is not int for k in ("exit_code", "passed", "failed", "skipped")) or check["exit_code"] != 0 or check["passed"] <= 0 or check["failed"] != 0 or check["skipped"] != 0:
                raise CampaignError("Failed, skipped or unexecuted checks block delivery")
        capabilities = receipt.get("capabilities")
        if not isinstance(capabilities, list) or not capabilities or any(not isinstance(x, str) or not x for x in capabilities) or len(set(capabilities)) != len(capabilities):
            raise CampaignError("Missing or duplicate capabilities")
        # This tool verifies recorded software evidence. Native and physical claims
        # require independent qualification; a receipt can never upgrade this level.
        if receipt.get("qualification") != "software_tested":
            raise CampaignError("Unsupported qualification claim")
        return CapabilityManifest(mission, tuple(capabilities), "software_tested")


class MissionStatusMachine:
    TRANSITIONS = {"PREPARED": {"ASSIGNED", "BLOCKED"}, "ASSIGNED": {"IN_PROGRESS", "BLOCKED"},
                   "IN_PROGRESS": {"DELIVERED", "BLOCKED"}, "BLOCKED": {"ASSIGNED"}, "DELIVERED": set()}

    def __init__(self, manifest, evaluator, records=None):
        self.manifest = manifest
        self.evaluator = evaluator
        self.records = dict(records or {})
        if set(self.records) - manifest.nodes.keys():
            raise CampaignError("Unknown mission record")
        for record in self.records.values():
            if record.get("status") not in self.TRANSITIONS:
                raise CampaignError("Unknown mission status")

    def status(self, mission):
        if mission not in self.manifest.nodes:
            raise CampaignError("Unknown mission")
        return self.records.get(mission, {}).get("status", "PREPARED")

    def delivered(self):
        verified = set()
        for mission in self.records:
            if self.status(mission) == "DELIVERED":
                self.evaluator.verify(mission, self.records[mission].get("evidence", {}))
                verified.add(mission)
        for mission in verified:
            if not set(self.manifest.nodes[mission].dependencies) <= verified:
                raise CampaignError("Delivered dependency missing: " + mission)
            node = self.manifest.nodes[mission]
            for dependency in node.dependencies:
                if self.manifest.nodes[dependency].repository == node.repository:
                    path = self.evaluator.paths[node.repository]
                    self.evaluator.git(path, "merge-base", "--is-ancestor",
                                       self.records[dependency]["evidence"]["commit"],
                                       self.records[mission]["evidence"]["commit"])
        return verified

    def transition(self, mission, status, *, evidence=None, owner=None, branch=None, blockers=None, decisions=None):
        current = self.status(mission)
        if status not in self.TRANSITIONS[current]:
            raise CampaignError("Forbidden status transition")
        delivered = self.delivered()
        if status in {"ASSIGNED", "IN_PROGRESS", "DELIVERED"} and not set(self.manifest.nodes[mission].dependencies) <= delivered:
            raise CampaignError("Dependencies not delivered")
        record = {**self.records.get(mission, {}), "status": status}
        for key, value in (("owner", owner), ("branch", branch), ("blockers", blockers), ("decisions", decisions)):
            if value is not None:
                record[key] = value
        if status in {"ASSIGNED", "IN_PROGRESS"} and (not record.get("owner") or not record.get("branch")):
            raise CampaignError("Owner and branch required")
        if status == "BLOCKED" and not record.get("blockers"):
            raise CampaignError("Blocker reason required")
        if status == "DELIVERED":
            self.evaluator.verify(mission, evidence or {})
            record["evidence"] = evidence
        from .ownership import OwnershipConflictDetector
        trial = {**self.records, mission: record}
        assignments = [{"mission": key, "owner": value.get("owner"), "branch": value.get("branch")}
                       for key, value in trial.items() if value["status"] in {"ASSIGNED", "IN_PROGRESS"}]
        OwnershipConflictDetector.check(self.manifest, assignments)
        # Validate the proposed complete state before publishing it. In
        # particular, a sibling branch must not pretend to include its same-repo
        # dependency just because both commits descend from the campaign base.
        MissionStatusMachine(self.manifest, self.evaluator, trial).delivered()
        self.records = trial
        return record
