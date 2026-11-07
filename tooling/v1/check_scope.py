"""Freeze the complete UNIFIED baseline; no runtime source or historical proof is rewritten."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASE='a73c1571f3e1dd0acd50e87b9742fbe2214a93d2'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def check():
 subprocess.run(['git','merge-base','--is-ancestor',BASE,'HEAD'],cwd=ROOT,check=True)
 frozen={}
 for line in git('ls-tree','-r',BASE).decode().splitlines():
  meta,name=line.split('\t',1);mode,kind,blob=meta.split();assert kind=='blob';frozen[name]=(mode,git('cat-file','--filters',BASE+':'+name))
 actual=set(git('ls-files','--cached','--others','--exclude-standard').decode().splitlines())
 assert set(frozen)<=actual
 assert all(n.startswith(('tooling/v1/','reports/v1-acceleration/')) or n=='.github/workflows/m51-unified.yml' for n in actual-set(frozen))
 modes={l.split('\t',1)[1]:l.split()[0] for l in git('ls-files','--stage').decode().splitlines()}
 for n in actual:
  p=ROOT/n;assert p.is_file() and not p.is_symlink();assert all(not a.is_symlink() for a in p.parents if a!=ROOT)
  if n in frozen:assert p.read_bytes()==frozen[n][1],n
  else:
   assert p.suffix.lower() in ('.py','.json','.md','.yml','.yaml','.svg','.log','.txt'),n
   p.read_bytes().decode('utf-8');assert not p.read_bytes().startswith(b'GGUF')
  assert modes.get(n)==(frozen[n][0] if n in frozen else '100644'),n
 return {'status':'PASS','base':BASE,'commit':git('rev-parse','HEAD').decode().strip(),'tree':git('rev-parse','HEAD^{tree}').decode().strip(),'worktree_dirty':bool(git('status','--porcelain')),'frozen_files':len(frozen),'source_changed':False,'contracts_v1_changed':False,'runtime_activation':False}
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args();r=check()
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
