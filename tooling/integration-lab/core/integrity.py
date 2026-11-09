"""Hash actual tracked files against commit blobs, independently of the mutable index."""
import hashlib, os, subprocess
from pathlib import Path

def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE, timeout=30)

def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''): h.update(chunk)
    return h.hexdigest()

def snapshot(root, commit):
    data = git(root, 'ls-tree', '-rz', commit)
    result = {}
    for entry in data.split(b'\0'):
        if not entry: continue
        info, name = entry.split(b'\t', 1); mode, kind, oid = info.decode().split()
        name = name.decode('utf-8')
        if kind == 'commit':
            result[name] = {'mode': mode, 'blob': oid, 'submodule': True}; continue
        if mode not in {'100644', '100755'}: raise ValueError('UNSUPPORTED_SOURCE_MODE:' + name)
        p = Path(root) / name
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(Path(root).resolve()):
            raise ValueError('MISSING_OR_UNSAFE_SOURCE:' + name)
        data = p.read_bytes(); actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual != oid:
            # Preserve repository-declared checkout attributes (notably Windows .bat CRLF).
            expected=git(root,'cat-file','--filters',commit+':'+name)
            if data != expected: raise ValueError('PROTECTED_SOURCE_DRIFT:' + name)
        if os.name != 'nt' and bool(p.stat().st_mode & 0o111) != (mode == '100755'):
            raise ValueError('SOURCE_MODE_DRIFT:' + name)
        result[name] = {'mode': mode, 'blob': oid, 'sha256': hashlib.sha256(data).hexdigest()}
    return result

def verify(root, row):
    if git(root, 'rev-parse', 'HEAD').decode().strip() != row['commit']: raise ValueError('COMMIT_DRIFT')
    if git(root, 'rev-parse', 'HEAD^{tree}').decode().strip() != row['tree']: raise ValueError('TREE_DRIFT')
    files = snapshot(root, row['commit'])
    for path, expected in row.get('protected', {}).items():
        if files.get(path, {}).get('sha256') != expected: raise ValueError('PREIMAGE_DRIFT:' + path)
    return {'status': 'PASS', 'commit': row['commit'], 'tree': row['tree'], 'tracked_files': len(files),
            'submodules_initialized': False, 'sources_preserved': True}
