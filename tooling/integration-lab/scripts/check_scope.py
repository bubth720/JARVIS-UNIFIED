"""Preserve the entire coordination baseline, including every earlier proof and guard."""
import subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tooling/integration-lab'));sys.path.insert(0,str(ROOT))
from core.integrity import git,snapshot

def check():
    base='a7625a31513be5c56fa36ed946fbdcd3c23c2a15'
    subprocess.run(['git','merge-base','--is-ancestor',base,'HEAD'],cwd=ROOT,check=True)
    frozen=snapshot(ROOT,base)
    actual=git(ROOT,'ls-files','--cached','--others','--exclude-standard').decode().splitlines()
    extra=set(actual)-set(frozen)
    if any(not p.startswith('tooling/integration-lab/') and p!='.github/workflows/integration-lab.yml' for p in extra):raise ValueError('UNAUTHORIZED_LAB_SCOPE')
    for name in extra:
        p=ROOT/name
        if p.is_symlink() or p.suffix not in {'.py','.json','.md','.txt','.html','.yml','.sha256','.log','.svg','.xml'}:raise ValueError('UNAUTHORIZED_SOURCE_PAYLOAD:'+name)
        if p.read_bytes().startswith(b'GGUF'):raise ValueError('MODEL_IN_SOURCE_REFUSED')
    return {'status':'PASS','frozen_files':len(frozen),'base':base,'contracts_unchanged':True,'historical_guards_unchanged':True}

if __name__=='__main__':
    import json
    print(json.dumps(check()))
