import json,subprocess,collections,csv,sys
GIT={'JAVIS-Local-v2':'/home/user/bubth720/javis-local-v2.git'}
for r in ['JARVIS-LLM','JARVIS-VOICE','JARVIS-INTERFACE','JARVIS-NEXUS','JARVIS-VOLUTION-','JARVIS-SERVICES','JARVIS-UNIFIED']: GIT[r]='/home/user/'+r
def g(r,*a):
    p=subprocess.run(['git','-C',GIT[r],*a],capture_output=True,text=True); return p.returncode,p.stdout.strip()
def anc(r,a,b): return g(r,'merge-base','--is-ancestor',a,b)[0]==0
P=[json.loads(l) for l in open('prs.jsonl')]; C={(c['repo'],c['number']):c for c in map(json.loads,open('ci.jsonl'))}
B=collections.defaultdict(list)
for b in map(json.loads,open('branches.jsonl')): B[b['repo']].append(b)
REF={'JAVIS-Local-v2':['5da98383ed12','49ad428e94ed'],'JARVIS-LLM':['61ae3a4b7e5e'],'JARVIS-VOICE':['cb32fbbd60c7'],'JARVIS-INTERFACE':['e6489bf011c8'],'JARVIS-NEXUS':['5f1019344097'],'JARVIS-VOLUTION-':['c4abfb035e3e','84ebc2e2b55d'],'JARVIS-SERVICES':['8d80d09d6aab'],'JARVIS-UNIFIED':['f1f30dc3cef2','0af322c1e353']}
def date(r,s): return g(r,'log','-1','--format=%cI',s)[1]
rows=[]; open_=[p for p in P if p['state']=='open']
for p in P:
    r=p['repo']; h=p['head_sha']; c=C.get((r,p['number']),{})
    row={k:p[k] for k in ['repo','number','title','state','draft','created_at','updated_at','head_ref','head_sha','base_ref','base_sha','url']}
    row['labels']=';'.join(p['labels']); row['merged']=bool(p.get('merged_at'))
    row['ci_at_head']=c.get('ci','N/A (fermée)' if p['state']!='open' else 'UNKNOWN')
    row['failing_checks']=';'.join(sorted({x['name'] for x in (c.get('runs') or []) if x['conclusion'] in ('failure','timed_out')}))[:300]
    row['mergeable_state']=c.get('mergeable_state') or 'UNKNOWN'
    ok=g(r,'cat-file','-e',h+'^{commit}')[0]==0 if h!='UNKNOWN' else False
    row['in_main']=anc(r,h,'origin/main') if ok else 'UNKNOWN'
    cont=[]
    if ok and p['state']=='open':
        for q in open_:
            if q['repo']==r and q['number']!=p['number'] and q['head_sha']!=h and anc(r,h,q['head_sha']): cont.append(f"#{q['number']}")
    row['contained_in_open_prs']=' '.join(cont)
    refs=[x for x in REF.get(r,[]) if ok and g(r,'cat-file','-e',x+'^{commit}')[0]==0 and anc(r,h,x)]
    row['contained_in_mission_refs']=' '.join(refs)
    br=[b['name'] for b in B[r] if ok and b['sha']!=h and anc(r,h,b['sha'])] if ok else []
    row['contained_in_branches_count']=len(br)
    row['stacked_on_pr']=' '.join(f"#{q['number']}" for q in P if q['repo']==r and q['head_ref']==p['base_ref'] and q['state']=='open')
    row['commits_ahead_of_base']=g(r,'rev-list','--count',f"{p['base_sha']}..{h}")[1] if ok and p['base_sha']!='UNKNOWN' and g(r,'cat-file','-e',p['base_sha'])[0]==0 else 'UNKNOWN'
    ev='CI_PASS_AT_HEAD' if row['ci_at_head']=='PASS' else ('CI_FAIL_AT_HEAD' if row['ci_at_head']=='FAIL' else ('NO_CI' if row['ci_at_head']=='NO_CI' else 'UNKNOWN'))
    names=' '.join(x['name'] for x in (c.get('runs') or []))
    if any(k in names for k in ['API29','API35','API 29','emulator','Emulator']): ev+='+EMULATOR_JOB'
    row['evidence_level']=ev
    if p['state']!='open': dec='FERMÉE/FUSIONNÉE — historique'
    elif row['in_main'] is True: dec='RÉSOLUE: tête déjà dans main — fermeture = décision propriétaire'
    elif cont: dec='CONTENUE dans '+' '.join(cont)+' (code préservé plus loin) — SUPERSEDED candidate, revue requise'
    elif refs: dec='CONTENUE dans la référence de mission '+' '.join(refs)+' — SUPERSEDED candidate'
    elif row['ci_at_head']=='FAIL': dec='BLOQUÉE: CI rouge au SHA ('+row['failing_checks'][:80]+')'
    elif row['ci_at_head']=='PASS': dec='ENCORE UTILE / REVIEW_REQUIRED (CI verte au SHA)'
    elif row['ci_at_head']=='NO_CI': dec='NON PROUVÉE: aucune CI au SHA'
    else: dec='UNKNOWN: '+row['ci_at_head']
    row['proposed_decision']=dec
    rows.append(row)
with open(sys.argv[1],'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
json.dump(rows,open('rows.json','w'),ensure_ascii=False)
print(collections.Counter(r['proposed_decision'].split(':')[0].split(' dans')[0] for r in rows))
