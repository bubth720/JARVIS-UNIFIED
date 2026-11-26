#!/usr/bin/env python3
"""Offline, fail-closed validation of the JARVIS monorepo source manifest."""
import argparse
import json
import re
import sys
from pathlib import Path

REPOSITORIES = {
    "core": "bubth720/JAVIS-Local-v2",
    "llm": "bubth720/JARVIS-LLM",
    "voice": "bubth720/JARVIS-VOICE",
    "interface": "bubth720/JARVIS-INTERFACE",
    "nexus": "bubth720/JARVIS-NEXUS",
    "services": "bubth720/JARVIS-SERVICES",
    "evolution": "bubth720/JARVIS-VOLUTION-",
}
REQUIRED_POLICY = {
    "one_core": True,
    "one_local_llm": True,
    "android_offline": True,
    "never_merge_main_without_owner_approval": True,
    "model_weights_excluded": True,
    "source_repos_remain_archived_only_after_verified_migration": True,
}
SHA = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_STATUS = {
    "BASELINE",
    "BASELINE_S04",
    "BASELINE_CANDIDATE_NO_GO",
    "ISOLATED_OFF",
    "DIAGNOSTIC_ONLY_SANDBOX_BLOCKED",
}
DEFAULT_MANIFEST = Path(__file__).with_name("sources.lock.json")


def load_and_validate(path):
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("type") != "unified_source_snapshot_proposal":
        raise ValueError("Invalid source manifest schema/type")
    coordinator = manifest.get("coordinator", {})
    if coordinator.get("repository") != "bubth720/JARVIS-UNIFIED" or not SHA.fullmatch(str(coordinator.get("base_sha", ""))):
        raise ValueError("Invalid coordinator")
    policy = manifest.get("policy", {})
    for key, value in REQUIRED_POLICY.items():
        if policy.get(key) is not value:
            raise ValueError("Required safety policy missing: " + key)
    modules = manifest.get("modules")
    if not isinstance(modules, list) or len(modules) != len(REPOSITORIES):
        raise ValueError("Exactly seven modules required")
    seen = set()
    for module in modules:
        if not isinstance(module, dict):
            raise ValueError("Module must be object")
        ident = module.get("id")
        if ident not in REPOSITORIES or ident in seen:
            raise ValueError("Unexpected/duplicate module: " + str(ident))
        seen.add(ident)
        if module.get("repository") != REPOSITORIES[ident]:
            raise ValueError("Repository mismatch: " + ident)
        if module.get("target") != "modules/" + ident:
            raise ValueError("Unsafe module path: " + ident)
        for key in ("source_sha", "candidate_sha"):
            value = module.get(key)
            if value is not None and not SHA.fullmatch(str(value)):
                raise ValueError("Invalid " + key + ": " + ident)
        if not SHA.fullmatch(str(module.get("source_sha", ""))):
            raise ValueError("Missing source_sha: " + ident)
        if type(module.get("embedded_in_s04")) is not bool:
            raise ValueError("Invalid embedded flag: " + ident)
        if module.get("status") not in ALLOWED_STATUS:
            raise ValueError("Invalid status: " + ident)
        if module.get("candidate_sha") and module.get("status") != "BASELINE_CANDIDATE_NO_GO":
            raise ValueError("Candidate must remain NO-GO: " + ident)
        if ident in ("services", "evolution") and module["embedded_in_s04"]:
            raise ValueError("Optional module cannot claim S04 integration")
    if seen != set(REPOSITORIES):
        raise ValueError("Missing module")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    args = parser.parse_args()
    try:
        manifest = load_and_validate(args.manifest)
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as exc:
        print("NO-GO: " + str(exc), file=sys.stderr)
        return 2
    print("PASS: seven module source SHAs and required safety policies validated.")
    print("SOURCE-ONLY: no APK build, integration, or physical qualification is implied.")
    for m in manifest["modules"]:
        print("{} {} {}".format(m["id"], m["source_sha"][:12], m["status"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
