"""Source fingerprint and scope review. No producer invocation or runtime adapter."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[2]
BASE='6539b444b5d65154088b8a2722212c0c16bbf257'
PREFIXES=('docs/nexus-n01-a2/','tooling/nexus_n01_a2/')
WORKFLOW='.github/workflows/nexus-n01-a2.yml'

def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args])

def scope_check():
    subprocess.run(['git','-C',str(ROOT),'merge-base','--is-ancestor',BASE,'HEAD'],check=True)
    frozen={}
    for entry in git(ROOT,'ls-tree','-rz',BASE).split(b'\0'):
        if not entry:continue
        meta,name=entry.split(b'\t',1);mode,kind,oid=meta.decode().split();name=name.decode()
        if kind!='blob':raise ValueError('Unsupported base object: '+name)
        frozen[name]=mode
        p=ROOT/name
        if p.is_symlink() or not p.is_file():raise ValueError('Missing/non-regular historical file: '+name)
        if p.read_bytes()!=git(ROOT,'cat-file','--filters',BASE+':'+name):raise ValueError('Historical bytes changed: '+name)
        if bool(p.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('Historical mode changed: '+name)
    actual=set(git(ROOT,'ls-files','--cached','--others','--exclude-standard','-z').decode().split('\0'))-{''}
    if not set(frozen)<=actual:raise ValueError('Historical files missing')
    added=sorted(actual-set(frozen))
    for name in added:
        p=ROOT/name
        if not (name.startswith(PREFIXES) or name==WORKFLOW):raise ValueError('Unexpected addition: '+name)
        if p.is_symlink() or not p.is_file() or p.stat().st_mode&0o111:raise ValueError('Unsafe addition: '+name)
        if p.suffix not in {'.py','.md','.json','.txt','.patch','.yml'}:raise ValueError('Unexpected artifact: '+name)
        p.read_text(encoding='utf-8')
    return {'result':'PASS','base':BASE,'historical_files_unchanged':len(frozen),'additions':added,'contracts_changed':False,'runtime_authorized':False}

def source_check(checkouts):
    manifest=json.loads((ROOT/'docs/nexus-n01-a2/evidence/five-repository-source-check.json').read_text())
    verified=[]
    for item in manifest['records']:
        repo=Path(checkouts[item['checkout']]).resolve()
        candidate=repo/item['path']
        if candidate.is_symlink():raise ValueError('Unsafe source symlink')
        p=candidate.resolve()
        if not p.is_relative_to(repo):raise ValueError('Unsafe source path')
        data=p.read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual!=item['git_blob_sha']:raise ValueError('Source differs from reviewed GitHub blob: '+item['repository'])
        subprocess.run(['git','-C',str(repo),'merge-base','--is-ancestor',item['commit'],'HEAD'],check=True)
        verified.append({k:item[k] for k in ('repository','commit','path','git_blob_sha')})
    return {'result':'PASS','source_level_only':True,'repositories':verified,'production_integration':'NOT_RUN','network_transport':'NOT_IMPLEMENTED'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources-root',type=Path)
    parser.add_argument('--local-workspace',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result={'scope':scope_check()}
    if args.sources_root:
        result['sources']=source_check({name:args.sources_root/name for name in ('core','services','nexus','unified','interface')})
    if args.local_workspace:
        result['sources']=source_check({name:args.local_workspace/repo for name,repo in {'core':'JAVIS-Local-v2','services':'JARVIS-SERVICES','nexus':'JARVIS-NEXUS','unified':'JARVIS-UNIFIED','interface':'JARVIS-INTERFACE'}.items()})
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
