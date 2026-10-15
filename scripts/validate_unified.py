#!/usr/bin/env python3
"""Offline delivery checks. No network and no application or model execution."""
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'registry/scripts'))
import update_registry as legacy
from audit_repos import validate_repositories,no_sensitive
from contracts import validate_contract,validate_schema,ContractError

REQUIRED=['README.md','AGENTS.md','registry/repositories.json','registry/modules.json','registry/integrations.json','docs/INVENTAIRE.md','docs/PROUVES.md','docs/MATRICE_INTEGRATION.md','docs/PLAN_INTEGRATION_CORE_LLM.md','docs/ROADMAP.md','docs/RISQUES.md','docs/RUNBOOK.md','docs/COMPTE_RENDU_CENTRAL.md','docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md','.github/workflows/validate-unified.yml']
NAMES=['capability-manifest','request-envelope','response-envelope','resource-lease','health-status']


def validate_delivery(root=ROOT):
    for name in REQUIRED:
        if not (root/name).is_file() or (root/name).stat().st_size==0:raise ValueError('Required delivery missing: '+name)
    repos=legacy.read_json(root/'registry/repositories.json');validate_repositories(repos)
    modules=legacy.read_json(root/'registry/modules.json');missions=legacy.read_json(root/'registry/missions.json');legacy.validate(modules,missions)
    ids={e['id'] for e in repos['repositories']};mids={e['module_id'] for e in modules['modules']}
    if ids!=mids:raise ValueError('Module/repository IDs differ')
    proofs=legacy.read_json(root/'registry/proofs.json')['proofs'];proof_ids=set()
    byid={e['id']:e for e in repos['repositories']}
    for proof in proofs:
        if proof['id'] in proof_ids or proof['repository_id'] not in ids:raise ValueError('Unknown or duplicate proof ID')
        proof_ids.add(proof['id'])
        if proof['type'] not in {'source','CI','hardware','documentation','declaration'}:raise ValueError('Unknown proof type')
        if proof['type']=='source':
            entry=byid[proof['repository_id']]
            if proof['sha']!=entry['observed_commit'] or '/blob/'+proof['sha']+'/' not in proof['url']:raise ValueError('Unbound source proof')
    for e in modules['modules']:
        if e['repository_id'] not in ids or not set(e['consolidation']['target_dependencies'])<=mids:raise ValueError('Unknown module link')
        if not (root/e['consolidation']['evidence_ref'].split('#')[0]).is_file():raise ValueError('Missing evidence')
    integration=legacy.read_json(root/'registry/integrations.json')
    for link in integration['links']:
        if link['from'] not in mids or link['to'] not in mids:raise ValueError('Unknown integration ID')
        if link['integration_test']=='passed' and link['code_link']!='present':raise ValueError('False integration claim')
    for name in NAMES:
        schema=legacy.read_json(root/'contracts/v1'/f'{name}.schema.json');validate_schema(schema)
        valid=legacy.read_json(root/'contracts/v1/examples'/f'{name}.valid.json');validate_contract(name,valid,schema)
        invalid=legacy.read_json(root/'contracts/v1/examples'/f'{name}.invalid.json')
        try:validate_contract(name,invalid,schema)
        except ContractError:pass
        else:raise ValueError('Invalid example accepted: '+name)
    # Source code is scanned for obvious credentials, not printed. Historical
    # documents may mention variable names, which are not credential values.
    for path in root.rglob('*'):
        if not path.is_file() or any(p in {'.git','.audit-cache','__pycache__','.venv'} for p in path.relative_to(root).parts):continue
        if path.suffix not in {'.json','.md','.py','.yml','.yaml','.txt'}:continue
        data=path.read_text()
        from audit_repos import TOKEN
        if TOKEN.search(data):raise ValueError('Obvious credential rejected in '+str(path.relative_to(root)))
        if path.suffix=='.json':legacy.read_json(path)
        if path.suffix=='.md':
            if data.count('```')%2:raise ValueError('Unclosed Markdown fence')
            for target in re.findall(r'\]\(([^)]+)\)',data):
                if target.startswith(('http://','https://','#','/tmp/','/workspace/')):continue
                if not (path.parent/target.split('#')[0]).exists():raise ValueError('Broken local link in '+str(path.relative_to(root)))
    return {'repositories':len(ids),'contracts':len(NAMES),'valid_examples':len(NAMES),'invalid_examples_rejected':len(NAMES)}

if __name__=='__main__':
    try:print(json.dumps(validate_delivery(),sort_keys=True))
    except (ValueError,OSError,KeyError,TypeError) as e:print('Validation failed: '+str(e),file=sys.stderr);raise SystemExit(1)
