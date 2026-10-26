"""Independent CI runner. Fixed local checks, recorded counts, no remote reads or runtime code."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import re
import subprocess
import sys
from .lock import ROOT

SUITES=(('audit_contracts','tests',41),('registry','registry/tests',23),
        ('campaign','tooling/campaign/tests',32),('backup','backup_prototype/tests',30),
        ('fusion01','tooling/integration/tests',21),('fusion02','tooling/integration/fusion02_tests',1))
CHECKS=(('unified_validator',['scripts/validate_unified.py']),
        ('v1_lock',['-m','tooling.integration.cli','validate']),
        ('v1_proposal',['-m','tooling.integration.cli','proposals']),
        ('v2_lock',['-m','tooling.integration.cli_v2','validate']),
        ('v2_comparison',['-m','tooling.integration.cli_v2','compare']),
        ('v2_contracts',['-m','tooling.integration.check_v2_contracts']))


def unittest_result(output,returncode,minimum=1):
    runs=re.findall(r'^Ran (\d+) tests? in ',output,re.M)
    counts={k:sum(map(int,re.findall(r'\b'+k+r'=(\d+)',output))) for k in ['failures','errors','skipped']}
    tests=int(runs[-1]) if runs else 0
    return {'tests':tests,'failed':counts['failures'],'errors':counts['errors'],'skipped':counts['skipped'],
            'passed':max(0,tests-counts['failures']-counts['errors']-counts['skipped']),
            'exit_code':returncode,'ok':returncode==0 and tests>=minimum and not any(counts.values())}


def execute(command):
    try:
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=180)
        return result.returncode,result.stdout+result.stderr
    except subprocess.TimeoutExpired:
        return 124,'Timeout: partial run is not counted as passed.\n'
    except OSError:
        return 127,'Local command unavailable.\n'


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    results=[]
    for name,directory,minimum in SUITES:
        command=[sys.executable,'-m','unittest','discover','-s',directory,'-v']
        code,text=execute(command)
        (output/(name+'.log')).write_text(text)
        results.append({'name':name,'command':['python3',*command[1:]],'kind':'unittest',**unittest_result(text,code,minimum)})
    for name,args in CHECKS:
        code,text=execute([sys.executable,*args]);(output/(name+'.log')).write_text(text)
        results.append({'name':name,'command':['python3',*args],'kind':'validation','exit_code':code,'ok':code==0})
    ok=all(r['ok'] for r in results)
    totals={k:sum(r.get(k,0) for r in results if r['kind']=='unittest') for k in ['tests','passed','failed','errors','skipped']}
    summary={'format':'jarvis.fusion02.ci/1','observed_at':datetime.now(timezone.utc).isoformat(),
             'platform':sys.platform,'python':sys.version.split()[0],
             'results':results,'totals':totals,'ok':ok,'android_instrumentation_executed':False,
             'runtime_authorization_granted':False}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'ok':ok,**totals,'checks':len(results)}))
    return 0 if ok else 1


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True)
    return run(p.parse_args(argv).output)


if __name__=='__main__':raise SystemExit(main())
