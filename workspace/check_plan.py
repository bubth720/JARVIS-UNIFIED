"""Offline, fail-closed validation of a *proposed* modular JARVIS workspace.

This does NOT clone repositories, verify remote commits, build an APK, resolve
licences, activate IPC, migrate databases, modify main, or approve integration.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

MODULES = {
    "core": ("bubth720/JAVIS-Local-v2", 24),
    "llm": ("bubth720/JARVIS-LLM", 29),
    "voice": ("bubth720/JARVIS-VOICE", 26),
    "interface": ("bubth720/JARVIS-INTERFACE", 26),
    "nexus": ("bubth720/JARVIS-NEXUS", 24),
    "services": ("bubth720/JARVIS-SERVICES", 24),
    "evolution": ("bubth720/JARVIS-VOLUTION-", 0),
    "unified": ("bubth720/JARVIS-UNIFIED", 0),
}
SHA = re.compile(r"[0-9a-f]{40}\Z")
BRANCH = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,159}\Z")
ROOT_KEYS = {
    "format", "observed_date", "purpose", "approved", "runtime_enabled",
    "automated_checkout_enabled", "unified_apk_qualified",
    "android_multi_module_go", "layout", "distribution", "modules",
    "proposed_dependencies", "gates"
}
MOD_KEYS = {"id", "repository", "branch", "commit", "min_sdk"}
DEP_KEYS = {"consumer", "provider", "role", "enabled"}
GATE_KEYS = {"id", "state", "reason"}
REQUIRED_GATES = {"contracts", "nexus_android", "services_android", "runtime_e2e", "physical"}
ALLOWED_ROLES = {"ui_events", "inference", "speech", "document_retrieval", "tools"}


class PlanError(ValueError):
    pass


def _unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise PlanError("duplicate JSON key")
        out[key] = value
    return out


def _reject_constant(_):
    raise PlanError("nonfinite JSON number")


def load(path):
    p = Path(path)
    if p.stat().st_size > 128 * 1024:
        raise PlanError("oversized proposal")
    return json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=_unique_pairs,
                      parse_constant=_reject_constant)


def _exact(value, keys):
    if type(value) is not dict or set(value) != keys:
        raise PlanError("unknown or missing fields")


def _valid_branch(branch):
    return (type(branch) is str and BRANCH.fullmatch(branch) is not None
            and ".." not in branch and "//" not in branch and not branch.endswith(("/", ".")))


def check(value):
    _exact(value, ROOT_KEYS)
    if value["format"] != "jarvis.modular-workspace/1" or value["purpose"] != "PROPOSED_ONLY":
        raise PlanError("unapproved workspace format")
    if value["layout"] != "single-project-modular" or value["distribution"] != "independent-modules-until-qualified":
        raise PlanError("unapproved topology")
    for field in ("approved", "runtime_enabled", "automated_checkout_enabled",
                  "unified_apk_qualified", "android_multi_module_go"):
        if value[field] is not False:
            raise PlanError("deployment/approval cannot be granted by a proposal")
    if type(value["observed_date"]) is not str or re.fullmatch(r"20[0-9]{2}-[0-9]{2}-[0-9]{2}", value["observed_date"]) is None:
        raise PlanError("invalid observation date")
    modules = value["modules"]
    if type(modules) is not list or len(modules) != 8:
        raise PlanError("eight pinned modules required")
    seen = set()
    for m in modules:
        _exact(m, MOD_KEYS)
        key = m["id"]
        if type(key) is not str or key not in MODULES or key in seen:
            raise PlanError("duplicate/unknown module")
        seen.add(key)
        repo, sdk = MODULES[key]
        if m["repository"] != repo or type(m["min_sdk"]) is not int or m["min_sdk"] != sdk:
            raise PlanError("invalid module owner/platform")
        if not _valid_branch(m["branch"]) or m["branch"] in {"main", "master"}:
            raise PlanError("unsafe release/default branch")
        if type(m["commit"]) is not str or SHA.fullmatch(m["commit"]) is None:
            raise PlanError("unpinned module")
    if seen != set(MODULES):
        raise PlanError("missing module")
    dependencies = value["proposed_dependencies"]
    if type(dependencies) is not list or len(dependencies) > 20:
        raise PlanError("invalid dependency plan")
    edges = set()
    graph = {module: set() for module in MODULES}
    for dep in dependencies:
        _exact(dep, DEP_KEYS)
        consumer, provider = dep["consumer"], dep["provider"]
        if type(consumer) is not str or type(provider) is not str or consumer not in MODULES or provider not in MODULES:
            raise PlanError("foreign dependency")
        if consumer == provider or (consumer, provider) in edges or dep["role"] not in ALLOWED_ROLES:
            raise PlanError("duplicate/self/unknown relation")
        if dep["enabled"] is not False:
            raise PlanError("runtime edges cannot be enabled")
        if provider == "unified" or consumer == "unified":
            raise PlanError("UNIFIED is not a runtime dependency")
        edges.add((consumer, provider))
        graph[consumer].add(provider)
    visited = set()
    visiting = set()
    def visit(node):
        if node in visiting:
            raise PlanError("dependency cycle")
        if node in visited:
            return
        visiting.add(node)
        for sub in graph[node]:
            visit(sub)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)
    gates = value["gates"]
    if type(gates) is not list or len(gates) != len(REQUIRED_GATES):
        raise PlanError("missing safety gates")
    seen_gates = set()
    for g in gates:
        _exact(g, GATE_KEYS)
        name = g["id"]
        if type(name) is not str or name not in REQUIRED_GATES or name in seen_gates:
            raise PlanError("duplicate/unknown gate")
        seen_gates.add(name)
        if g["state"] not in ("BLOCKED", "NOT_RUN") or type(g["reason"]) is not str or not (15 <= len(g["reason"]) <= 500):
            raise PlanError("invalid positive/empty gate")
    if seen_gates != REQUIRED_GATES:
        raise PlanError("missing gates")
    return {"status": "REVIEW_ONLY", "validated_modules": len(modules),
            "proposed_links": len(dependencies), "runtime_links_enabled": 0,
            "remote_shas_reverified_now": False, "all_source_code_combined": False,
            "unified_apk_qualified": False, "android_multi_module_go": False,
            "merge_authorized": False, "missing_gates": sorted(seen_gates)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", type=Path)
    args = ap.parse_args(argv)
    try:
        print(json.dumps(check(load(args.manifest)), indent=2, sort_keys=True))
        return 0
    except (PlanError, OSError, UnicodeError, ValueError, TypeError, RecursionError):
        print("WORKSPACE PROPOSAL REJECTED")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
