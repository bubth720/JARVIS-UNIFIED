"""Validate pinned sources, claims, gates and score without giving permission to execute them."""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[2]
REPORTS=ROOT/'reports/v1-acceleration'
MODULES={'CORE','LLM','INTERFACE','NEXUS','SERVICES','VOICE','AVATAR','EVOLUTION','UNIFIED'}
STATES={'ABSENT','PREPARED','AVAILABLE_OFF','LAB_ONLY','ACTIVE_VERIFIED','BLOCKED','ERROR','UNKNOWN'}
GATES={'G-A','G-ROOT','G-B','G-C','G-DOC','G-VOICE','G-V1','G-MERGE'}
WEIGHTS={'CHAT':25,'COCKPIT':20,'NEXUS':15,'SERVICES':15,'VOICE':10,'AVATAR':5,'EVOLUTION':5,'STABILITY':5}
SENSITIVE={'merge','root_provision','native_patch','personal_device_install','real_data_migration','model_acquisition','external_write','cloud_purchase'}
CRITERIA_SHA256='05851201deee722aaa5c4e5ab78ab9390b222c0d470e532d1ea7f0d86ee6c8b1'
ALLOWED_PREPARATION={'source_audit','unit_tests','cloud_emulator_test','lab_apk_build','draft_pr_publish','synthetic_fixture'}

class InvalidEvidence(ValueError): pass

def need(value,code):
    if not value:raise InvalidEvidence(code)

def digest(value,n=64):return isinstance(value,str) and re.fullmatch('[0-9a-f]{'+str(n)+'}',value) is not None

def no_duplicates(pairs):
    out={}
    for key,value in pairs:
        need(key not in out,'DUPLICATE_JSON_KEY');out[key]=value
    return out

def read(path):
    raw=Path(path).read_bytes();need(len(raw)<=2*1024*1024,'REPORT_SIZE_LIMIT')
    return json.loads(raw,object_pairs_hook=no_duplicates)

def check_lock(lock):
    need(lock.get('schema')=='jarvis.v1.baseline-lock/1','LOCK_VERSION')
    need(digest(lock.get('coordination_base'),40),'COORDINATION_BASE')
    need(digest(lock.get('mission_document',{}).get('sha256')),'MISSION_DOCUMENT_HASH')
    modules=lock.get('modules',[]);ids=[m.get('module_id') for m in modules]
    need(len(ids)==len(set(ids)) and set(ids)==MODULES,'MODULE_SET')
    need(lock['composition']['runtime_modules']==[] and lock['composition']['composition_code_present'] is False,'UNIFIED_MUST_NOT_BECOME_RUNTIME')
    for m in modules:
        for name in ('source_sha','source_tree','default_sha','default_tree'):need(digest(m.get(name),40),'BAD_GIT_'+name)
        need(isinstance(m.get('repository'),str) and m['repository'].startswith('bubth720/'),'REPOSITORY_ID')
        need(m.get('source_branch') and m.get('default_branch'),'BRANCH_REQUIRED')
        need(m.get('reference_tree_truncated') is False,'TRUNCATED_REFERENCE_TREE')
        for doc in m.get('source_documents',[]):
            need(digest(doc.get('git_blob_sha'),40) and digest(doc.get('sha256')),'SOURCE_FINGERPRINT')
            need(isinstance(doc.get('bytes'),int) and doc['bytes']>0,'EMPTY_SOURCE')
            need('/'+m['source_sha']+'/' in doc.get('url',''),'SOURCE_URL_NOT_PINNED')
        for run in m.get('ci_observed',[]):
            need(run.get('head_sha')==m['source_sha'],'CI_AT_WRONG_COMMIT')
            need(run.get('conclusion') in ('success','failure','cancelled','skipped','timed_out','action_required',None),'CI_CONCLUSION')
    return {m['module_id']:m for m in modules}

def evidence_ref(ref,commit,module,evidence,modules,kinds=None):
    need(ref in evidence,'MISSING_EVIDENCE')
    e=evidence[ref]
    need(e.get('module_id')==module and e.get('tested_commit')==commit,'EVIDENCE_BINDING')
    need(commit==modules[module]['source_sha'],'CLAIM_AT_WRONG_SOURCE')
    need(e.get('status')=='PASS','EVIDENCE_NOT_PASS')
    need(e.get('url','').startswith('https://github.com/bubth720/'),'UNTRUSTED_EVIDENCE_LINK')
    if kinds:need(e.get('kind') in kinds,'WRONG_PROOF_LAYER')
    return e

def check_capabilities(data,modules):
    need(data.get('schema')=='jarvis.v1.capability-evidence/1','CAPABILITY_VERSION')
    rows=data.get('capabilities',[]);ids=[x.get('module_id') for x in rows]
    need(len(ids)==len(set(ids)) and set(ids)==MODULES,'CAPABILITY_MODULE_SET')
    evidence=data.get('evidence',{})
    for row in rows:
        mid=row['module_id'];need(row.get('source_sha')==modules[mid]['source_sha'],'CAPABILITY_SOURCE')
        need(row.get('availability') in STATES,'CAPABILITY_STATE')
        for field in ('code_present','connected','enabled','runtime_ready','user_approved','device_qualified'):
            need(type(row.get(field)) is bool,'CAPABILITY_BOOLEAN')
        need(set(row.get('dimensions',{}))=={'implemented','tested','integrated','experienced'},'DIMENSION_SET')
        for field,claim in row.get('dimensions',{}).items():
            need(field in ('implemented','tested','integrated','experienced') and type(claim.get('value')) is bool,'DIMENSION_TYPE')
            if claim['value']:
                allowed={'SOURCE'} if field=='implemented' else {'EXECUTION','ANDROID_EMULATOR','ANDROID_PHYSICAL','HUMAN_RECEPTION'}
                e=evidence_ref(claim.get('evidence_ref'),claim.get('tested_commit'),mid,evidence,modules,allowed)
                if field=='integrated':need('INTEGRATION' in e.get('operation_ids',[]),'INTEGRATION_PROOF_REQUIRED')
                if field=='experienced':need(e.get('platform') in ('ANDROID_EMULATOR','ANDROID_PHYSICAL','HUMAN_RECEPTION'),'USER_EXPERIENCE_PROOF_REQUIRED')
        if row['code_present']:evidence_ref('source_'+mid,row['source_sha'],mid,evidence,modules,{'SOURCE'})
        # This coordination branch carries no approved runtime composition or authority.
        need(not any(row[f] for f in ('connected','enabled','runtime_ready','user_approved','device_qualified')),'RUNTIME_PROOF_NOT_RECEIVED')
        need(row['availability']!='ACTIVE_VERIFIED','NO_APPROVED_RUNTIME_COMPOSITION')
    metrics=data.get('metrics',{});n=metrics.get('comparable_trials')
    need(type(n) is int and n>=0,'TRIAL_COUNT')
    if n<20:need(metrics.get('ttft_p95_ms') is None,'P95_REQUIRES_20_COMPARABLE_TRIALS')
    if n==0:need(all(metrics.get(k) is None for k in ('ttft_p50_ms','ttft_p95_ms','ttft_max_ms')),'ABSENT_MEASURE_IS_NOT_ZERO')
    return len(rows)

def check_gates(data):
    need(data.get('schema')=='jarvis.v1.gates/1','GATE_VERSION')
    rows=data.get('gates',[]);ids=[x.get('gate_id') for x in rows]
    need(len(ids)==len(set(ids)) and set(ids)==GATES,'GATE_SET')
    need(data.get('sensitive_execution_authorized') is False,'NO_BLANKET_SENSITIVE_APPROVAL')
    for row in rows:
        need(row.get('status') in {'BLOCKED','NOT_RUN','PARTIAL','UNKNOWN'},'GATE_CANNOT_PASS_FROM_PREPARATION')
        need(row.get('approved') is False and row.get('crossed') is False and row.get('approval_ref') is None,'HUMAN_GATE_NOT_GRANTED')
    need(data['lab_patch']['state']=='UNAPPLIED' and data['lab_patch']['root']=='CLOSED','LAB_SCOPE_CANNOT_OPEN_FROM_M51')
    need(digest(data['lab_patch']['sha256']),'PATCH_FINGERPRINT')
    return len(rows)

def permitted(action):
    """This validator can label permitted preparation; it cannot approve sensitive actions."""
    return action in ALLOWED_PREPARATION and action not in SENSITIVE

def check_score(data,modules,evidence):
    need(data.get('schema')=='jarvis.v1.score/1','SCORE_VERSION')
    need(data.get('domain_weights')==WEIGHTS and sum(WEIGHTS.values())==100,'SCORE_DOMAIN_WEIGHTS')
    rows=data.get('criteria',[]);ids=[r.get('criterion_id') for r in rows]
    need(len(ids)==len(set(ids)),'SCORE_CRITERION_DUPLICATE')
    frozen_fields=('criterion_id','domain','weight','required_platform','module_id','operation_id')
    spec=[{k:r.get(k) for k in frozen_fields} for r in rows]
    need(hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(',',':')).encode()).hexdigest()==CRITERIA_SHA256,'SCORE_CRITERIA_SPEC')
    total=0;by={k:0 for k in WEIGHTS}
    for row in rows:
        domain=row.get('domain');need(domain in WEIGHTS,'SCORE_DOMAIN')
        weight=row.get('weight');need(type(weight) is int and weight>0,'SCORE_WEIGHT')
        by[domain]+=weight
        need(row.get('module_id') in modules,'SCORE_MODULE')
        need(row.get('state') in {'UNASSESSED','BLOCKED','NOT_RUN','PASS','FAIL'},'SCORE_STATE')
        if row['state']=='PASS':
            e=evidence_ref(row.get('evidence_ref'),row.get('tested_commit'),row['module_id'],evidence,modules,{'EXECUTION','ANDROID_EMULATOR','ANDROID_PHYSICAL','HUMAN_RECEPTION'})
            need(e.get('platform')==row.get('required_platform'),'SCORE_WRONG_PLATFORM')
            need(row.get('operation_id') in e.get('operation_ids',[]),'SCORE_WRONG_OPERATION')
            need(digest(e.get('artifact_sha256')),'EXECUTION_ARTIFACT_HASH_REQUIRED')
            total+=weight
        else:need(row.get('evidence_ref') is None and row.get('tested_commit') is None,'UNASSESSED_CLAIM_MUST_NOT_AWARD')
    need(by==WEIGHTS,'SCORE_CRITERIA_TOTALS')
    need(data.get('qualified_points')==total and data.get('unassessed_or_blocked_points')==100-total,'SCORE_TOTAL')
    need(data.get('prepared_points_earned')==0,'NO_POINTS_FOR_DOCUMENTS')
    return total

def check_artifact(name,digest_sha256):
    need(isinstance(name,str) and Path(name).name==name and '/' not in name and '\\' not in name,'ARTIFACT_NAME')
    need(Path(name).suffix.lower() in {'.zip','.json','.txt','.md','.log','.apk','.svg'},'PRIVATE_OR_MODEL_ARTIFACT_FORBIDDEN')
    need(digest(digest_sha256),'ARTIFACT_SHA256')

def validate(directory=REPORTS):
    directory=Path(directory)
    modules=check_lock(read(directory/'BASELINE-LOCK.json'))
    capabilities=read(directory/'CAPABILITY-EVIDENCE.json');n=check_capabilities(capabilities,modules)
    gates=check_gates(read(directory/'GATES.json'))
    points=check_score(read(directory/'SCORE.json'),modules,capabilities['evidence'])
    return {'status':'PASS','scope':'OFFLINE_COORDINATION_ONLY','modules':len(modules),'source_documents':sum(len(m['source_documents']) for m in modules.values()),'capabilities':n,'gates':gates,'qualified_points':points,'runtime_activated':False,'models_acquired':False}

def graph_svg(score):
    """Deterministic static score graphic; unknown is not earned and is labelled explicitly."""
    by={k:0 for k in WEIGHTS}
    for r in score['criteria']:
        if r['state']=='PASS':by[r['domain']]+=r['weight']
    rows=['<svg xmlns="http://www.w3.org/2000/svg" width="820" height="420" viewBox="0 0 820 420" role="img" aria-labelledby="title desc">',
          '<title id="title">Grille V1 préenregistrée — nouvelle composition M51</title>',
          '<desc id="desc">Les barres grises sont des points non attribués. Aucun document ou test isolé ne vaut capacité intégrée.</desc>',
          '<rect width="820" height="420" fill="#101b2c"/>',
          '<text x="20" y="30" fill="white" font-size="18">Nouvelle composition M51 : points non encore attribués</text>']
    y=65
    for domain,maximum in WEIGHTS.items():
        earned=by[domain];rows+=[f'<text x="20" y="{y+15}" fill="white" font-size="14">{domain}</text>',f'<rect x="160" y="{y}" width="{maximum*20}" height="22" fill="#64748b"/>',f'<rect x="160" y="{y}" width="{earned*20}" height="22" fill="#22d3ee"/>',f'<text x="690" y="{y+15}" fill="white" font-size="14">{earned}/{maximum}</text>'];y+=38
    rows+=['<text x="20" y="390" fill="#cbd5e1" font-size="13">Gris : non évalué/bloqué. Cyan : acquis par preuve. Ce n’est pas le % historique du projet.</text>','</svg>']
    return '\n'.join(rows)+'\n'

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--reports',type=Path,default=REPORTS);p.add_argument('--output',type=Path);p.add_argument('--svg',type=Path);a=p.parse_args()
    result=validate(a.reports)
    result['tested_commit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    result['tested_tree']=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=ROOT,text=True).strip()
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    if a.svg:a.svg.write_text(graph_svg(read(a.reports/'SCORE.json')))
    print(json.dumps(result,sort_keys=True))
