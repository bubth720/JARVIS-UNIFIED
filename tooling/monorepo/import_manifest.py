"""M1 — offline integrity of the imported modules/ tree (no network, no source repository needed).

`python3 tooling/monorepo/import_manifest.py --write` records, per module of sources.lock.json, the file count, the
byte count and a tree digest (sha256 over sorted "path\\0sha256(content)" lines). Without --write it recomputes and
compares: any missing module, extra or changed file, or forbidden artefact (model weights, APK, keystore, database,
native binary) is NO-GO. The digest proves the tree is unchanged since import; provenance to the original commits is
in import/SOURCE-SNAPSHOT-REPORT.json (git-archive SHA-256 of each pinned commit).
"""
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCK = ROOT / 'tooling/monorepo/sources.lock.json'
MANIFEST = ROOT / 'tooling/monorepo/import/IMPORT-MANIFEST.json'
FORBIDDEN = ('.gguf', '.onnx', '.apk', '.aab', '.jks', '.keystore', '.p12', '.db', '.sqlite', '.so', '.dylib', '.dll', '.tflite', '.safetensors', '.pt', '.ckpt')


def tree(module_dir):
    lines, n, size, bad = [], 0, 0, []
    for p in sorted(module_dir.rglob('*')):
        if p.is_symlink(): bad.append(str(p.relative_to(ROOT)) + ' (symlink)'); continue
        if not p.is_file(): continue
        rel = p.relative_to(module_dir).as_posix(); data = p.read_bytes()
        if rel.lower().endswith(FORBIDDEN) or (rel.lower().endswith('.bin') and len(data) > 1_000_000): bad.append(rel)
        lines.append(rel + '\0' + hashlib.sha256(data).hexdigest()); n += 1; size += len(data)
    return {'files': n, 'bytes': size, 'tree_sha256': hashlib.sha256('\n'.join(lines).encode()).hexdigest()}, bad


def compute():
    lock = json.loads(LOCK.read_text()); out, problems = {}, []
    for m in lock['modules']:
        d = ROOT / m['target']
        if not d.is_dir(): problems.append(f"{m['id']}: module directory missing"); continue
        t, bad = tree(d); out[m['id']] = {'source_sha': m['source_sha'], 'target': m['target'], **t}
        problems += [f"{m['id']}: forbidden artefact {b}" for b in bad]
    extra = sorted(p.name for p in (ROOT / 'modules').iterdir() if p.is_dir() and p.name not in {m['target'].split('/')[-1] for m in lock['modules']}) if (ROOT / 'modules').is_dir() else []
    problems += [f'unexpected module directory {e}' for e in extra]
    return out, problems


def check():
    got, problems = compute()
    want = json.loads(MANIFEST.read_text())['modules']
    for k in sorted(set(want) | set(got)):
        if k not in got: problems.append(f'{k}: missing'); continue
        if k not in want: problems.append(f'{k}: not in manifest'); continue
        for f in ('source_sha', 'files', 'bytes', 'tree_sha256'):
            if want[k][f] != got[k][f]: problems.append(f'{k}: {f} {want[k][f]} != {got[k][f]}')
    return problems


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--write', action='store_true'); a = ap.parse_args()
    if a.write:
        got, problems = compute()
        if problems: print('NO-GO:', *problems, sep='\n  '); sys.exit(1)
        MANIFEST.write_text(json.dumps({'schema': 'jarvis.monorepo.import-manifest/1', 'modules': got}, indent=1) + '\n'); print('written', {k: v['files'] for k, v in got.items()})
    else:
        p = check(); print('GO: modules/ identical to the import manifest' if not p else 'NO-GO:\n  ' + '\n  '.join(p)); sys.exit(1 if p else 0)
