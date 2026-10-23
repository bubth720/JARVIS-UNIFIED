"""A repository-wide single-writer rule includes all shared-file collisions."""
import re
from .manifest import CampaignError


class OwnershipPolicy:
    SENSITIVE = frozenset({"jni", "native_admission", "critical_permissions", "signatures", "inter_apk_activation",
                           "personal_data_migration", "personal_device", "untrusted_patch_execution", "main_merge"})
    SHARED = {
        "bubth720/JAVIS-Local-v2": ("JarvisCore.kt", "LocalDatabase.kt", "PromptBuilder.kt"),
        "bubth720/JARVIS-LLM": ("LlamaBackend.kt", "bridge.cpp"),
        "bubth720/JARVIS-INTERFACE": ("DashboardGrid.kt", "AvatarAnimationController.kt"),
    }

    @classmethod
    def check_changes(cls, changes, authorizations):
        if set(changes) - cls.SENSITIVE:
            raise CampaignError("Unknown sensitive change category")
        missing = set(changes) - set(authorizations)
        if missing:
            raise CampaignError("Explicit authorization required: " + ", ".join(sorted(missing)))


class OwnershipConflictDetector:
    @staticmethod
    def check(manifest, assignments):
        repositories, owners = {}, set()
        for assignment in assignments:
            mission, owner = assignment["mission"], assignment["owner"]
            if mission not in manifest.nodes or not isinstance(owner, str) or not owner.strip():
                raise CampaignError("Invalid assignment")
            repository = manifest.nodes[mission].repository
            branch = assignment["branch"]
            if not isinstance(branch, str) or not re.fullmatch(r"feat/[A-Za-z0-9._/-]+", branch) or ".." in branch or "//" in branch or branch.endswith(("/", ".lock", ".")):
                raise CampaignError("Unsafe campaign branch")
            if any(part.startswith(".") or part.endswith((".lock", ".")) for part in branch.split("/")):
                raise CampaignError("Unsafe campaign branch component")
            if repository in repositories:
                raise CampaignError("Repository ownership collision: " + repository)
            if owner in owners:
                raise CampaignError("Owner already assigned")
            repositories[repository] = assignment
            owners.add(owner)
        return True
