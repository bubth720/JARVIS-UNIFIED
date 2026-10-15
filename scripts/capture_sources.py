#!/usr/bin/env python3
"""Inspect prepared bare Git snapshots without executing or modifying their code."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

CHOICES = {
 'core': ('JAVIS-Local-v2','main'), 'llm':('JARVIS-LLM','mission-003b-resources'),
 'voice':('JARVIS-VOICE','feat/voice-expression-005i'), 'interface':('JARVIS-INTERFACE','development/mission-002'),
 'interface-placeholder':('JARVIS-INTERFACE-','main'), 'nexus':('JARVIS-NEXUS','main'),
 'evolution-candidate':('JARVIS-VOLUTION-','main'), 'services':('JARVIS-SERVICES','main'),
 'unified':('JARVIS-UNIFIED','main')}


def capture(cache):
    stamp=datetime.now(timezone.utc).isoformat(timespec='seconds'); entries=[]
    for rid,(name,selected) in CHOICES.items():
        gitdir=cache/(name+'.git')
        def git(*args):
            return subprocess.check_output(['git','--git-dir='+str(gitdir),*args],text=True)
        default=git('symbolic-ref','HEAD').strip().removeprefix('refs/heads/')
        refs={line.split(' ',1)[0]:line.split(' ',1)[1] for line in git('for-each-ref','--format=%(refname:short) %(objectname)','refs/heads').splitlines()}
        branches=[]
        for branch,sha in refs.items():
            date=git('show','-s','--format=%cI',sha).strip()
            date=datetime.fromisoformat(date).astimezone(timezone.utc).isoformat()
            merged=None
            if 'main' in refs:
                operation=subprocess.run(['git','--git-dir='+str(gitdir),'merge-base','--is-ancestor',sha,refs['main']],capture_output=True)
                if operation.returncode not in (0,1):raise RuntimeError('Ancestry check failed')
                merged=operation.returncode==0
            counts=None
            if 'main' in refs:counts=list(map(int,git('rev-list','--left-right','--count',refs['main']+'...'+sha).split()))
            branches.append({'name':branch,'sha':sha,'commit_date_utc':date,'merged_into_main':merged,'main_only_commits':counts[0] if counts else None,'branch_only_commits':counts[1] if counts else None,'url':'https://github.com/bubth720/'+name+'/tree/'+sha})
        files=git('ls-tree','-r','--name-only',selected).splitlines()
        main_files=git('ls-tree','-r','--name-only','main').splitlines() if 'main' in refs else None
        manifests=[];sdk=[];interfaces=[];ipc=[];fingerprints={}
        patterns=re.compile(r'bindService\(|startService\(|class\s+\w+\s*:\s*(?:Service|ContentProvider)|\.aidl$|Messenger\(')
        for f in files:
            if not f.endswith(('.kt','.kts','.xml','.cpp','.h','.py','.md','.yml','.yaml','.json','.aidl')):continue
            size=int(git('cat-file','-s',refs[selected]+':'+f))
            if size>256*1024:continue
            text=git('show',selected+':'+f)
            if f.endswith(('AndroidManifest.xml','build.gradle.kts','settings.gradle.kts')) or ('src/main/' in f and f.endswith(('.kt','.cpp','.h','.aidl'))):
                fingerprints[f]=hashlib.sha256(text.encode()).hexdigest()
            if f.endswith('AndroidManifest.xml'):
                manifests.append({'path':f,'packages':re.findall(r'android:name="([^\"]+)"',text),'services':re.findall(r'<service\b[^>]*',text),'internet_declared':bool(re.search(r'<uses-permission[^>]*android.permission.INTERNET',text)),'network_removal_directive':'tools:node="remove"' in text})
            if f.endswith('build.gradle.kts'):
                sdk.append({'path':f,'min_sdk':re.findall(r'minSdk\s*=\s*(\d+)',text),'compile_sdk':re.findall(r'compileSdk\s*=\s*(\d+)',text),'application_id':re.findall(r'applicationId\s*=\s*"([^\"]+)"',text)})
            if '/src/main/' in f and f.endswith(('.kt','.aidl')):
                interfaces.extend({'path':f,'name':n} for n in re.findall(r'\binterface\s+(\w+)',text))
                if patterns.search(text) or f.endswith('.aidl'):ipc.append(f)
        history=[]
        if 'main' in refs:
            for line in git('log','--first-parent','--max-count=12','--format=%H|%P|%cI|%s','main').splitlines():
                sha,parents,date,subject=line.split('|',3)
                history.append({'sha':sha,'parents':parents.split(),'date_utc':datetime.fromisoformat(date).astimezone(timezone.utc).isoformat(),'subject':subject})
        entries.append({'id':rid,'name':'bubth720/'+name,'access':{'status':'success','method':'https_git_bare_snapshot','visibility':'unknown'},'captured_at':stamp,'default_branch':default,'inspection_branch':selected,'observed_commit':refs[selected],'main_commit':refs.get('main'),'branches':branches,'main_first_parent_history':history,'files':files,'main_files':main_files,'languages':sorted({Path(f).suffix for f in files if Path(f).suffix in ['.kt','.java','.cpp','.h','.py']}),'manifests':manifests,'gradle':sdk,'interfaces':interfaces,'ipc_pattern_hits':ipc,'source_sha256':fingerprints,'tests':[f for f in files if '/test/' in f or '/androidTest/' in f or '/tests/' in f],'workflows':[f for f in files if f.startswith('.github/workflows/')],'prs':{'status':'unknown','reason':'api_unavailable'},'ci':{'status':'unknown','reason':'api_unavailable'},'hardware':{'status':'not_checked'},'proof_type':'source','scope':'files_and_git_graph_only'})
    return {'schema_version':1,'captured_at':stamp,'repositories':entries,'naming_probes':[]}



def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--cache',type=Path,default=Path('.audit-cache'));p.add_argument('--output',type=Path,required=True);p.add_argument('--naming-probes',type=Path);a=p.parse_args()
    data=capture(a.cache)
    if a.naming_probes:data['naming_probes']=json.loads(a.naming_probes.read_text())['probes']
    a.output.parent.mkdir(parents=True,exist_ok=True)
    # No raw source, author email, credential, binary or private data is copied.
    a.output.write_text(json.dumps(data,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    print('Captured',len(data['repositories']),'Git snapshots; no runtime validation.')
if __name__=='__main__':main()
