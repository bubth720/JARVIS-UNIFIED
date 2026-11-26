#!/usr/bin/env python3
"""NEXT-01A / M2 — prepare the V3 build inputs from the UNIFIED monorepo (modules/*), with no external checkout.

Same guarantees as labs/v1/tools/prepare_sources.py and labs/v3/tools/prepare_core_memory.py, which need the historical
Git repositories: every reused file is verified by its Git blob id and size against the FROZEN locks
labs/v1/sources.json (read, never written) and labs/v3/core-memory.lock.json, plus the module pins of the new
independent lock labs/v3/sources.json. The tree of each module is additionally proven unchanged by
tooling/monorepo/import_manifest.py. Writes only into a NEW output directory. No network.
"""
import argparse, hashlib, json, sys
from pathlib import Path

V3 = Path(__file__).resolve().parents[1]
V1_LOCK = V3.parent / 'v1/sources.json'
MEM_LOCK = V3 / 'core-memory.lock.json'
V3_LOCK = V3 / 'sources.json'


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def read_verified(root, rel, sha, size):
    p = (root / rel)
    if p.is_symlink() or not p.is_file(): raise ValueError(f'missing or linked source: {rel}')
    data = p.read_bytes()
    if blob(data) != sha or len(data) != size: raise ValueError(f'blob or size mismatch: {rel}')
    return data


def prepare(monorepo, output):
    v3 = json.loads(V3_LOCK.read_text()); v1 = json.loads(V1_LOCK.read_text()); mem = json.loads(MEM_LOCK.read_text())
    mods = {m['id']: m for m in v3['modules']}
    roots = {k: (monorepo / mods[k]['path']).resolve() for k in ('CORE', 'INTERFACE', 'LLM', 'VOICE', 'NEXUS')}
    # The V3 lock must reproduce exactly the pins of the frozen locks (no silent pin change).
    v1mods = {m['id']: m for m in v1['modules']}
    for k in ('CORE', 'LLM'):
        if mods[k]['sha'] != v1mods[k]['sha']: raise ValueError(f'{k}: V3 lock pin differs from the frozen V1 lock')
    if mods['VOICE']['sha'] != v1['voice']['sha']: raise ValueError('VOICE: V3 lock pin differs from the frozen V1 lock')
    if mods['CORE']['sha'] != mem['commit']: raise ValueError('CORE: V3 lock pin differs from core-memory.lock.json')
    output = output.resolve()
    if output.exists(): raise ValueError('output must be a new directory')
    if any(r == output or r in output.parents for r in roots.values()): raise ValueError('output inside a module')
    kotlin, memory = output / 'kotlin', output / 'core-memory'; n = 0
    for m in v1['modules']:
        if m['id'] == 'LLM':
            for f in m['native']: read_verified(roots['LLM'], f['path'], f['sha'], f['size']); n += 1
            continue
        for f in m['files']:
            data = read_verified(roots[m['id']], f['path'], f['sha'], f['size'])
            dst = kotlin / f['path'].removeprefix('app/src/main/java/'); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(data); n += 1
    for f in mem['files']:
        data = read_verified(roots['CORE'], f['path'], f['blob'], f['size'])
        dst = memory / f['path'].removeprefix('app/src/main/java/'); dst.parent.mkdir(parents=True, exist_ok=True); dst.write_bytes(data); n += 1
    (output / 'provenance.json').write_text(json.dumps({'v3_lock': v3, 'verified_files': n, 'frozen_locks_read_only': [str(V1_LOCK.name), str(MEM_LOCK.name)]}, indent=1) + '\n')
    print(f'PASS: {n} files verified by Git blob id against the frozen V1/V3 locks; build inputs in a new directory; no checkout, no network')
    return n


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--monorepo', type=Path, required=True); ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    try: prepare(a.monorepo.resolve(), a.output)
    except ValueError as e: print('NO-GO:', e); sys.exit(1)
