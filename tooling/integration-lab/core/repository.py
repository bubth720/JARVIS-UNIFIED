"""Only the eight approved public repositories; isolated clones, never worktrees."""
import json, os, re, subprocess
from pathlib import Path
from tooling.contracts.manifest import strict_json
from .policy import MODULES
from .integrity import sha, verify

def read_lock(path):
    p = Path(path)
    if p.stat().st_size > 1024 * 1024: raise ValueError('OVERSIZE_LOCK')
    expected = p.with_suffix('.sha256').read_text().strip()
    if sha(p) != expected: raise ValueError('LOCK_DIGEST_MISMATCH')
    lock = strict_json(p.read_text())
    rows = lock.get('modules', [])
    if len(rows) != 8 or {r['module'] for r in rows} != set(MODULES): raise ValueError('EXACTLY_EIGHT_MODULES_REQUIRED')
    for row in rows:
        if row['repository'] != MODULES[row['module']]: raise ValueError('UNKNOWN_REPOSITORY')
        if any(not re.fullmatch('[0-9a-f]{40}', row[k]) for k in ['commit', 'tree']): raise ValueError('FULL_SHA_REQUIRED')
        if row.get('runtime_enabled') is not False: raise ValueError('RUNTIME_ACTIVATION_REFUSED')
        if not re.fullmatch('[a-zA-Z0-9._/-]+', row['branch']) or '..' in row['branch']: raise ValueError('UNSAFE_BRANCH')
    return lock

def acquire(row, root, offline=False):
    root = Path(root); root.mkdir(parents=True, exist_ok=True); target = root / row['module']
    if target.is_symlink(): raise ValueError('UNSAFE_SOURCE_ROOT')
    if not target.exists():
        if offline: raise FileNotFoundError('OFFLINE_SOURCE_MISSING:' + row['module'])
        # Git verifies object identities. No recursive submodule/model acquisition.
        env = {**os.environ, 'GIT_TERMINAL_PROMPT': '0', 'GIT_CONFIG_NOSYSTEM': '1'}
        q = subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', 'clone', '--no-checkout',
                            'https://github.com/' + row['repository'] + '.git', str(target)],
                           capture_output=True, env=env, timeout=240)
        if q.returncode: raise OSError('REPOSITORY_FETCH_UNAVAILABLE')
        q = subprocess.run(['git', '-C', str(target), '-c', 'core.hooksPath=/dev/null',
                            'checkout', '--detach', row['commit']], capture_output=True, env=env, timeout=60)
        if q.returncode: raise OSError('PINNED_COMMIT_UNAVAILABLE')
        (root/('.'+row['module']+'.lab-source.json')).write_text(json.dumps({'repository':row['repository'],'commit':row['commit'],'isolated_lab_clone':True})+'\n')
    marker=root/('.'+row['module']+'.lab-source.json')
    if not marker.is_file() or marker.is_symlink() or not (target/'.git').is_dir():raise ValueError('ISOLATED_LAB_CLONE_REQUIRED')
    identity=strict_json(marker.read_text())
    if identity!={'repository':row['repository'],'commit':row['commit'],'isolated_lab_clone':True}:raise ValueError('LAB_CLONE_IDENTITY_MISMATCH')
    return target, verify(target, row)
