"""Execute exact-source offline checks once. No retries, model, APK installation or sensitive operation."""
import json,platform,re,subprocess,sys
from pathlib import Path
from tooling.v1.validate import ROOT,validate,graph_svg,read,REPORTS
from tooling.v1.check_scope import check

def main():
 out=ROOT/'.audit-cache/m51-ci/raw';out.mkdir(parents=True,exist_ok=True)
 identity={'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,text=True).strip(),'platform':platform.platform(),'python':platform.python_version()}
 (out/'preservation.json').write_text(json.dumps(check(),indent=2)+'\n')
 suites=[('historical-validator',['scripts/validate_unified.py']),('historical-tests',['-m','unittest','discover','-s','tests','-v']),('historical-registry',['-m','unittest','discover','-s','registry/tests','-v']),('historical-backup',['-m','unittest','discover','-s','backup_prototype/tests','-v']),('historical-campaign',['-m','unittest','discover','-s','tooling/campaign/tests','-v']),('historical-integration',['-m','unittest','discover','-s','tooling/integration/tests','-v']),('m51-v1',['-m','unittest','discover','-s','tooling/v1/tests','-v'])]
 results=[]
 for name,args in suites:
  run=subprocess.run([sys.executable]+args,cwd=ROOT,capture_output=True,text=True,timeout=180)
  log=run.stdout+run.stderr;(out/(name+'.log')).write_text(log)
  count=re.search(r'(?m)^Ran (\d+) tests? ',log)
  result={'suite':name,'status':'PASS' if run.returncode==0 else 'FAIL','command':['python3']+args,'exit_code':run.returncode,'tests':int(count[1]) if count else None}
  results.append(result);print(json.dumps(result),flush=True)
  if run.returncode:break
 failed=any(r['status']!='PASS' for r in results)
 report={**identity,'suites':results,'all_requested_suites_executed':len(results)==len(suites),'status':'FAIL' if failed else 'PASS','runtime_activated':False,'model_acquired':False,'android':'NOT_RUN','physical_android':'NOT_RUN','llm_generation':'NOT_RUN','ttft_p95_ms':None}
 (out/'test-results.json').write_text(json.dumps(report,indent=2)+'\n')
 if not failed:
  (out/'validation.json').write_text(json.dumps({**validate(),**identity},indent=2)+'\n')
  (out/'SCORE.svg').write_text(graph_svg(read(REPORTS/'SCORE.json')))
  (out/'preservation.json').write_text(json.dumps(check(),indent=2)+'\n')
 return 1 if failed else 0
if __name__=='__main__':raise SystemExit(main())
