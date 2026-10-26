"""UNI-08/U00: offline, fail-closed review of a *proposed* GitHub BOM.

This does not fetch GitHub, attest CI, authorize runtime connections, or promote
an integration candidate. The observed inputs require independent verification.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

MAX_SIZE = 1024 * 1024
SHA = re.compile(r"[0-9a-f]{40}\\Z")
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
ROOT_KEYS = {"format", "observation_date", "scope", "decision", "human_approved", "android_multi_module_go", "modules"}
MODULE_KEYS = {"id", "repository", "default_branch", "candidate_branch", "candidate_sha", "min_sdk", "ci_observations", "android_e2e_attested", "physical_attested", "runtime_link_attested", "risk"}
RUN_KEYS = {"workflow", "run_id", "commit", "conclusion", "url"}
CONCLUSIONS = {"success", "failure", "cancelled", "pending"}

class CandidateError(ValueError):
    pass


def _pairs_unique(pairs):
    out = {}
    for key, val in pairs:
        if key in out:
            raise CandidateError("duplicate JSON key")
        out[key] = val
    return out


def _bad_constant(_):
    raise CandidateError("non-finite JSON number")


def load_file(path: str | Path):
    p = Path(path)
    if p.stat().st_size > MAX_SIZE:
        raise CandidateError("candidate exceeds one MiB")
    return json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=_pairs_unique,
                      parse_constant=_bad_constant)


def _exact(obj, keys, where):
    if type(obj) is not dict or set(obj) != keys:
        raise CandidateError(f"unexpected keys at {where}")


def _sha(value, where):
    if type(value) is not str or not SHA.fullmatch(value):
        raise CandidateError(f"invalid full commit SHA at {where}")


def _github_run(url, repo, run_id):
    if type(url) is not str or type(run_id) is not int or run_id < 1:
        raise CandidateError("invalid CI run URL/ID")
    if url != f"https://github.com/{repo}/actions/runs/{run_id}":
        raise CandidateError("CI URL does not identify the selected repository and run")
    parsed = urlparse(url)
    if parsed.hostname != "github.com" or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise CandidateError("untrusted CI URL")


def validate(candidate):
    """Validate structure, referential consistency, and fail-closed claims only.

    The underlying GitHub observations are *not* re-attested here. A CI success
    on an ancestor never qualifies the selected candidate commit.
    """
    _exact(candidate, ROOT_KEYS, "root")
    if candidate["format"] != "jarvis.uni08-candidate/1" or candidate["scope"] != "AUDIT_ONLY":
        raise CandidateError("unapproved candidate format/scope")
    if (candidate["decision"] != "BLOCKED" or candidate["human_approved"] is not False
            or candidate["android_multi_module_go"] is not False):
        raise CandidateError("audit candidate cannot authorize release")
    if type(candidate["observation_date"]) is not str or not re.fullmatch(r"20\\d\\d-\\d\\d-\\d\\d", candidate["observation_date"]):
        raise CandidateError("invalid observation date")
    entries = candidate["modules"]
    if type(entries) is not list or len(entries) != 8:
        raise CandidateError("exactly eight module entries required")
    seen = set()
    results = []
    for item in entries:
        _exact(item, MODULE_KEYS, "module")
        name = item["id"]
        if type(name) is not str or name not in MODULES or name in seen:
            raise CandidateError("unknown/duplicate module")
        seen.add(name)
        repo, sdk = MODULES[name]
        if item["repository"] != repo or type(item["min_sdk"]) is not int or item["min_sdk"] != sdk:
            raise CandidateError("repository or baseline minSdk mismatch")
        branch = item["candidate_branch"]
        default = item["default_branch"]
        if any(type(b) is not str or not b or len(b) > 160 or any(c.isspace() for c in b) or ".." in b for b in (branch, default)):
            raise CandidateError("invalid branch")
        if branch == default:
            raise CandidateError("candidate must not be the default production branch")
        _sha(item["candidate_sha"], "module")
        for key in ("android_e2e_attested", "physical_attested", "runtime_link_attested"):
            if item[key] is not False:
                raise CandidateError("unauthorized evidence escalation")
        if type(item["risk"]) is not str or not 5 <= len(item["risk"]) <= 500:
            raise CandidateError("risk rationale required")
        runs = item["ci_observations"]
        if type(runs) is not list or len(runs) > 20:
            raise CandidateError("invalid CI observations")
        ids = set()
        matching = []
        stale = False
        for run in runs:
            _exact(run, RUN_KEYS, "ci")
            if type(run["workflow"]) is not str or not 1 <= len(run["workflow"]) <= 150:
                raise CandidateError("invalid workflow")
            if run["conclusion"] not in CONCLUSIONS:
                raise CandidateError("invalid CI conclusion")
            _sha(run["commit"], "ci")
            _github_run(run["url"], repo, run["run_id"])
            if run["run_id"] in ids:
                raise CandidateError("duplicate CI run")
            ids.add(run["run_id"])
            if run["commit"] == item["candidate_sha"]:
                matching.append(run["conclusion"])
            else:
                stale = True
        if not matching:
            ci = "STALE_ONLY" if stale else "UNKNOWN"
        elif all(s == "success" for s in matching):
            ci = "SOFTWARE_CI_SUCCESS_ONLY"
        elif "success" in matching:
            ci = "MIXED"
        elif "failure" in matching:
            ci = "FAILED"
        else:
            ci = "UNQUALIFIED"
        results.append({"id": name, "candidate_sha": item["candidate_sha"], "ci_review": ci,
                        "runtime_qualified": False, "physical_qualified": False})
    if seen != set(MODULES):
        raise CandidateError("missing module")
    return {"verdict": "BLOCKED", "authorization_granted": False,
            "github_bytes_verified_now": False, "android_multi_module_go": False,
            "modules": sorted(results, key=lambda r: r["id"])}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("candidate", type=Path)
    args = ap.parse_args(argv)
    try:
        value = load_file(args.candidate)
        print(json.dumps(validate(value), indent=2, ensure_ascii=False, sort_keys=True))
        return 0
    except (CandidateError, OSError, UnicodeError, ValueError, TypeError, KeyError, OverflowError) as exc:
        print("REJECTED:", type(exc).__name__, str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
