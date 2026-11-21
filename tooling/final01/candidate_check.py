"""F01 — is a candidate producer commit a drop-in replacement for the pinned one, for what the APK really compiles?

Reads the frozen V1 lock (INTERFACE labs/v1/sources.json) WITHOUT modifying it, and checks, at the candidate commit:
  * LLM: every locked native file has the exact locked git blob and size (what prepare_sources.verify_llm demands);
  * VOICE: the whole `pocketRuntime` module tree (compiled unchanged by labs/v1/pocket) is byte-identical to the pin;
  * any module: the candidate descends from the pin (no rewritten history).
A candidate is DROP_IN only if every check passes; otherwise the exact differing paths are listed. DROP_IN proves the
APK would compile the same bytes; it does not replace a build and an emulator run before a pin change, and changing
the pin in the frozen lock still requires the owner's exception (labs/v1 is preserved byte-identical).
"""
import argparse, json, subprocess, sys


def git(repo, *a, check=True):
    return subprocess.run(['git', '-C', repo, *a], capture_output=True, text=True, check=check).stdout.strip()


def blob_at(repo, sha, path):
    r = subprocess.run(['git', '-C', repo, 'rev-parse', f'{sha}:{path}'], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def check_llm(lock, repo, candidate):
    m = next(x for x in lock['modules'] if x['id'] == 'LLM'); diffs = []
    for f in m['native']:
        b = blob_at(repo, candidate, f['path'])
        size = int(git(repo, 'cat-file', '-s', b)) if b else None
        if b != f['sha'] or size != f['size']:
            diffs.append({'path': f['path'], 'locked_blob': f['sha'], 'candidate_blob': b})
    return m['sha'], len(m['native']), diffs


def check_tree(repo, pin, candidate, path):
    a, b = blob_at(repo, pin, path), blob_at(repo, candidate, path)
    if a == b: return []
    return [x for x in git(repo, 'diff', '--name-only', pin, candidate, '--', path).split('\n') if x]


def run(lock_path, module, repo, candidate):
    lock = json.load(open(lock_path)); candidate = git(repo, 'rev-parse', candidate + '^{commit}')
    if module == 'LLM':
        pin, n, diffs = check_llm(lock, repo, candidate); what = f'{n} locked native files (blob + size)'
    elif module == 'VOICE':
        pin = lock['voice']['sha']; diffs = check_tree(repo, pin, candidate, lock['voice']['module']); what = f"tree {lock['voice']['module']}"
    else:
        raise SystemExit(f'{module}: not in the V1 lock (use a build test)')
    descends = subprocess.run(['git', '-C', repo, 'merge-base', '--is-ancestor', pin, candidate]).returncode == 0
    status = 'DROP_IN' if descends and not diffs else 'NOT_DROP_IN'
    return {'module': module, 'pin': pin, 'candidate': candidate, 'checked': what, 'candidate_descends_from_pin': descends,
            'differences': diffs, 'status': status}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--lock', required=True); ap.add_argument('--module', required=True, choices=['LLM', 'VOICE'])
    ap.add_argument('--repo', required=True); ap.add_argument('--candidate', required=True)
    a = ap.parse_args(); r = run(a.lock, a.module, a.repo, a.candidate)
    json.dump(r, sys.stdout, indent=1); print(); sys.exit(0 if r['status'] == 'DROP_IN' else 1)
