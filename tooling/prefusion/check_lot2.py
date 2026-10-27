"""Fail-closed validator for snapshot of LOT2 branches; no GitHub queries or merge.

This is a historical offline manifest check; it does not confirm remote CI.
Fetch live PR/Actions refs separately before any subsequent action.
"""
import json
import re
import sys
from pathlib import Path

SHA = re.compile(r"[a-f0-9]{40}\Z")
REPOS = {
    "CORE": "bubth720/JAVIS-Local-v2",
    "INTERFACE": "bubth720/JARVIS-INTERFACE",
    "EVOLUTION": "bubth720/JARVIS-VOLUTION-",
}
REQUIRED_BLOCKS = {
    "ANDROID_FTS5", "CORE_SERVICES_ADR002", "JNI_UNLOAD",
    "VOICE_EMOTIONS", "PHYSICAL_DEVICE", "SIGNED_CORE_UI",
    "EVOLUTION_SANDBOX",
}

class EvidenceError(ValueError):
    pass

def unique_pairs(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise EvidenceError("duplicate JSON key")
        result[k] = v
    return result

def load(path):
    p = Path(path)
    if p.stat().st_size > 32768:
        raise EvidenceError("oversized manifest")
    return json.loads(p.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)

def check(x):
    keys={"format", "observed_date", "status", "approved", "merge_main_allowed",
          "runtime_activation_allowed", "code_combined", "physical_device_qualified",
          "source_baseline", "modules", "release_gates"}
    if type(x) is not dict or set(x)!=keys:
        raise EvidenceError("unexpected manifest structure")
    if x["format"] != "jarvis.uni08.lot2-evidence/1" or x["status"] != "REVIEW_ONLY":
        raise EvidenceError("false approval format")
    for k in ("approved","merge_main_allowed","runtime_activation_allowed","code_combined","physical_device_qualified"):
        if x[k] is not False:
            raise EvidenceError("unapproved runtime/release promotion")
    if x["observed_date"] != "2026-10-27":
        raise EvidenceError("unexpected observation date")
    baseline=x["source_baseline"]
    if (type(baseline) is not dict or set(baseline)!={"repo","branch","sha"}
        or baseline["repo"]!="bubth720/JARVIS-UNIFIED"
        or baseline["branch"]!="codex/prefusion-20261026-lot1"
        or type(baseline["sha"]) is not str or not SHA.fullmatch(baseline["sha"])):
        raise EvidenceError("unverified baseline")
    modules=x["modules"]
    if type(modules) is not list or len(modules)!=3:
        raise EvidenceError("must have exactly three modules")
    seen_modules=set()
    for m in modules:
        if type(m) is not dict or set(m)!={"module","repo","prs"}:
            raise EvidenceError("invalid module")
        name=m["module"]
        if type(name) is not str or name in seen_modules or name not in REPOS or m["repo"]!=REPOS[name]:
            raise EvidenceError("duplicate/foreign module")
        seen_modules.add(name)
        prs=m["prs"]
        if type(prs) is not list or len(prs)!=2:
            raise EvidenceError("two distinct candidate PRs per owner required")
        seen_paths=set()
        seen_prs=set()
        seen_runs=set()
        for pr in prs:
            if type(pr) is not dict or set(pr)!={"number","sha","run","files"}:
                raise EvidenceError("invalid PR entry")
            num, sha, run=pr["number"],pr["sha"],pr["run"]
            if type(num) is not int or num < 1 or num in seen_prs:
                raise EvidenceError("duplicate/invalid PR number")
            if type(run) is not int or run < 1 or run in seen_runs:
                raise EvidenceError("duplicate/invalid CI run")
            if type(sha) is not str or not SHA.fullmatch(sha):
                raise EvidenceError("missing full commit sha")
            seen_prs.add(num)
            seen_runs.add(run)
            files=pr["files"]
            if type(files) is not list or not files or len(files)>50:
                raise EvidenceError("empty/oversized delta")
            if len(files)!=len(set(files)):
                raise EvidenceError("duplicate path in PR")
            for p in files:
                if (type(p) is not str or not p or p.startswith("/")
                        or ".." in Path(p).parts or "\\" in p
                        or p in seen_paths):
                    raise EvidenceError("invalid path or overlapping PR writes")
                seen_paths.add(p)
    if seen_modules!=set(REPOS):
        raise EvidenceError("missing module")
    gates=x["release_gates"]
    if type(gates) is not list or len(gates)!=len(REQUIRED_BLOCKS):
        raise EvidenceError("missing gates")
    names=set()
    for g in gates:
        if type(g) is not dict or set(g)!={"name","status"}:
            raise EvidenceError("invalid gate")
        name=g["name"]
        if type(name) is not str or name not in REQUIRED_BLOCKS or name in names:
            raise EvidenceError("unknown/duplicate gate")
        names.add(name)
        if g["status"] != ("NOT_RUN" if name=="PHYSICAL_DEVICE" else "BLOCKED"):
            raise EvidenceError("gate illegally promoted")
    return {
        "verdict": "REVIEW_ONLY",
        "module_owners":len(modules),
        "candidate_prs":sum(len(m["prs"]) for m in modules),
        "source_write_overlap":False,
        "merges_performed_by_validator":0,
        "tested_at_combined_commit":False,
        "remote_ci_reverified_by_validator":False,
        "android_go":False,
        "release_gates":sorted(names),
    }

if __name__=="__main__":
    try:
        result=check(load(sys.argv[1]))
        print(json.dumps(result,indent=2,sort_keys=True))
    except (IndexError, OSError, ValueError, TypeError, RecursionError) as exc:
        print(f"BLOCKED: {type(exc).__name__}: {exc}",file=sys.stderr)
        raise SystemExit(1)
