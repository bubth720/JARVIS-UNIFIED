"""Additive B0 scope and unchanged pinned producers; never edits an old guard."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
BASE='1834472161ff961b6c7a20a766d0e255d545ab44'
NEXUS='5f10193440972ba25b30645d2811537418eface5'
V1='9599d99147f9c9baaccdd07b4d5a6359d558b4c6'
ALLOWED=('tooling/research_b0/','docs/research-b0/')
WORKFLOW='.github/workflows/research-b0.yml'


def git(root,*args):
    return subprocess.check_output(['git','-C',str(root),*args])


def freeze(root,base,allowed=(),workflow=None,check_additions=True):
    root=Path(root)
    subprocess.run(['git','-C',str(root),'merge-base','--is-ancestor',base,'HEAD'],check=True,capture_output=True)
    frozen=set()
    for row in git(root,'ls-tree','-rz',base).split(b'\0'):
        if not row:continue
        meta,name=row.split(b'\t',1);mode,kind,oid=meta.decode().split();name=name.decode();path=root/name
        if kind!='blob' or path.is_symlink() or not path.is_file():raise ValueError('Historical path: '+name)
        if path.read_bytes()!=git(root,'cat-file','--filters',base+':'+name):raise ValueError('Historical bytes: '+name)
        if bool(path.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('Historical mode: '+name)
        frozen.add(name)
    actual=set(git(root,'ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0'))-{''}
    added=actual-frozen
    if not frozen<=actual:raise ValueError('Historical deletion')
    if check_additions:
        for name in sorted(added):
            p=root/name
            if not (name.startswith(allowed) or name==workflow):raise ValueError('Unexpected addition: '+name)
            if p.is_symlink() or not p.is_file() or p.stat().st_mode&0o111:raise ValueError('Unsafe addition: '+name)
            if p.suffix not in ('.py','.md','.json','.yml','.txt') or not p.read_text().strip():raise ValueError('Invalid addition: '+name)
    return dict(base=base,source_commit=git(root,'rev-parse','HEAD').decode().strip(),
                historical_files_unchanged=len(frozen),additions=sorted(added),result='PASS')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace',type=Path,default=ROOT.parent)
    p.add_argument('--output',type=Path)
    p.add_argument('--run-v1-chain',action='store_true')
    p.add_argument('--v1-log',type=Path)
    args=p.parse_args()
    result={'unified':freeze(ROOT,BASE,ALLOWED,WORKFLOW)}
    nexus=args.workspace/'JARVIS-NEXUS';ui=args.workspace/'JARVIS-INTERFACE'
    result['nexus']=freeze(nexus,NEXUS)
    result['interface_v1']=freeze(ui,V1,check_additions=False)
    if result['unified']['historical_files_unchanged']!=525:raise ValueError('Unexpected UNIFIED base')
    if result['nexus']['historical_files_unchanged']!=342:raise ValueError('Unexpected NEXUS base')
    if result['interface_v1']['historical_files_unchanged']!=430:raise ValueError('Unexpected V1 base')
    subprocess.run([sys.executable,'reuse-r1plus/n01-a3/check_routing_scope.py'],cwd=nexus,check=True)
    from tooling.nexus_n01_a2.review import source_check
    result['contracts']=source_check({key:args.workspace/name for key,name in {
      'core':'JAVIS-Local-v2','services':'JARVIS-SERVICES','nexus':'JARVIS-NEXUS',
      'unified':'JARVIS-UNIFIED','interface':'JARVIS-INTERFACE'}.items()})
    if args.run_v1_chain:
        # The unchanged historical test itself uses disposable worktrees internally.
        # Run it in a disposable clone, without changing the actual UI checkout.
        with tempfile.TemporaryDirectory(prefix='b0-v1-chain-') as tmp:
            clone=Path(tmp)/'interface'
            subprocess.run(['git','clone','--shared','--quiet','--no-checkout',str(ui),str(clone)],check=True)
            subprocess.run(['git','-C',str(clone),'checkout','--quiet','--detach',result['interface_v1']['source_commit']],check=True)
            r=subprocess.run([sys.executable,'labs/v3/tools/check_scope.py','--interface',str(clone)],cwd=clone,
                             stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180)
            if args.v1_log:args.v1_log.parent.mkdir(parents=True,exist_ok=True);args.v1_log.write_text(r.stdout)
            if r.returncode:raise ValueError('Historical V1 guard chain refused; inspect retained log')
            result['v1_guard_chain']={'result':'PASS','source_commit':result['interface_v1']['source_commit'],'summary':r.stdout.splitlines()[-1]}
    result.update(contracts_changed=False,production_connected=False,collection=False)
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
