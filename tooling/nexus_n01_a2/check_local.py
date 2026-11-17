"""Run authorized existing/offline checks and write evidence only to --output."""
import argparse
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from tooling.nexus_n01_a2.review import ROOT,scope_check,source_check

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--workspace',type=Path,default=Path('/workspace'))
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    if out.is_relative_to(ROOT):raise ValueError('Evidence output must stay outside checkout')
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    suites=[('validator',ROOT,['scripts/validate_unified.py']),
      ('unified',ROOT,['-m','unittest','discover','-s','tests','-v']),
      ('registry',ROOT,['-m','unittest','discover','-s','registry/tests','-v']),
      ('backup',ROOT,['-m','unittest','discover','-s','backup_prototype/tests','-v']),
      ('u01',ROOT,['-m','unittest','discover','-s','tooling/integration/uni08_u01_tests','-v']),
      ('a2',ROOT,['-m','unittest','discover','-s','tooling/nexus_n01_a2/tests','-v']),
      ('nexus-scope',args.workspace/'JARVIS-NEXUS',['-m','unittest','discover','-s','reuse-r1plus/n01-a2/tests','-v']),
      ('nexus-final',args.workspace/'JARVIS-NEXUS',['-m','unittest','discover','-s','tests/final','-v'])]
    results=[]
    for name,cwd,cmd in suites:
        p=subprocess.run([sys.executable,*cmd],cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=180)
        (out/(name+'.txt')).write_text(p.stdout)
        counts=re.search(r'Ran (\d+) tests?',p.stdout)
        result={'name':name,'command':'python3 '+' '.join(cmd),'repository':cwd.name,'exit_code':p.returncode,'tests':int(counts.group(1)) if counts else None,'summary':p.stdout.splitlines()[-4:]}
        results.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
    ui=args.workspace/'JARVIS-INTERFACE';v1='9599d99147f9c9baaccdd07b4d5a6359d558b4c6';frozen=0
    def git(*a):return subprocess.check_output(['git','-C',str(ui),*a])
    for record in git('ls-tree','-rz',v1).split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);name=name.decode();mode=meta.decode().split()[0];p=ui/name
        if p.is_symlink() or p.read_bytes()!=git('cat-file','--filters',v1+':'+name):raise ValueError('V1 content changed: '+name)
        if bool(p.stat().st_mode&0o111)!=(mode=='100755'):raise ValueError('V1 mode changed: '+name)
        frozen+=1
    assert frozen==430
    checks={k:args.workspace/v for k,v in {'core':'JAVIS-Local-v2','services':'JARVIS-SERVICES','nexus':'JARVIS-NEXUS','unified':'JARVIS-UNIFIED','interface':'JARVIS-INTERFACE'}.items()}
    report={'platform':platform.platform(),'python':sys.version,'suites':results,'total_python_tests':sum(x['tests'] or 0 for x in results),'scope':scope_check(),'five_sources':source_check(checks),'frozen_v1_files_unchanged':frozen,'result':'PASS' if all(x['exit_code']==0 for x in results) else 'FAIL'}
    (out/'local-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    if report['result']!='PASS':raise SystemExit(1)

if __name__=='__main__':main()
