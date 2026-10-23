"""Validated campaign domain types, with no runtime module ownership."""
from dataclasses import dataclass
from pathlib import Path
import re
from tooling.contracts.manifest import strict_json


class CampaignError(ValueError):
    pass


EXPECTED_OWNERS = {
    f"{prefix}-{number:02}": "bubth720/" + repository
    for prefix, count, repository in (
        ("CORE", 3, "JAVIS-Local-v2"), ("ID", 2, "JAVIS-Local-v2"), ("MEM", 2, "JAVIS-Local-v2"),
        ("LLM", 3, "JARVIS-LLM"), ("VOICE", 3, "JARVIS-VOICE"), ("UI", 2, "JARVIS-INTERFACE"),
        ("AVA", 2, "JARVIS-INTERFACE"), ("SERV", 3, "JARVIS-SERVICES"), ("NEX", 5, "JARVIS-NEXUS"),
        ("EVOL", 4, "JARVIS-VOLUTION-"), ("UNI", 2, "JARVIS-UNIFIED"))
    for number in range(1, count + 1)
}


@dataclass(frozen=True)
class MissionNode:
    id: str
    repository: str
    dependencies: tuple
    priority: str
    wave: int
    path: str


@dataclass(frozen=True)
class RepoReference:
    repository: str
    planning_commit: str


class CampaignManifestReader:
    def __init__(self, value):
        if value.get("version") != 1 or type(value.get("version")) is not int:
            raise CampaignError("Unknown campaign version")
        self.value = value
        self.references = {}
        for item in value.get("repositories", []):
            self.add_reference(item["repository"], item["planning_commit"])
        self.add_reference(value["central_repo"], value["central_base"])
        self.nodes = {}
        for item in value["missions"]:
            mission = item["id"]
            if not isinstance(mission, str) or not re.fullmatch(r"[A-Z]+-[0-9]{2}", mission):
                raise CampaignError("Invalid mission ID")
            if mission in self.nodes:
                raise CampaignError("Duplicate mission: " + mission)
            deps = item["dependencies"]
            if not isinstance(deps, list) or any(not isinstance(x, str) for x in deps) or len(set(deps)) != len(deps):
                raise CampaignError("Invalid dependencies")
            if item["repository"] not in self.references:
                raise CampaignError("Unknown repository")
            if EXPECTED_OWNERS.get(mission) != item["repository"]:
                raise CampaignError("Campaign v1 mission ownership mismatch: " + mission)
            if item["priority"] not in {"P0", "P1", "P2"} or type(item["wave"]) is not int or item["wave"] < 0:
                raise CampaignError("Invalid priority or wave")
            path = item["path"]
            if path != "docs/intensive-2026-10-22/" + mission + ".md":
                raise CampaignError("Mission path mismatch")
            self.nodes[mission] = MissionNode(mission, item["repository"], tuple(deps), item["priority"], item["wave"], path)
        if set(self.nodes) != set(EXPECTED_OWNERS):
            raise CampaignError("Campaign v1 requires its 31 explicit missions")
        for node in self.nodes.values():
            if set(node.dependencies) - self.nodes.keys():
                raise CampaignError("Unknown dependency: " + node.id)
        self.references = dict(self.references)

    def add_reference(self, repository, commit):
        if not isinstance(repository, str) or not re.fullmatch(r"bubth720/[A-Za-z0-9_-]+", repository):
            raise CampaignError("Invalid repository")
        if repository in self.references or not isinstance(commit, str) or not re.fullmatch("[0-9a-f]{40}", commit):
            raise CampaignError("Ambiguous repository or invalid SHA")
        self.references[repository] = RepoReference(repository, commit)

    @classmethod
    def read(cls, path):
        return cls(strict_json(Path(path).read_text(encoding="utf-8")))


RepoReferenceCatalog = dict
