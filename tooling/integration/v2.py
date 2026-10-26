"""FUSION-02 evidence admission. No Android orchestration or permission authority."""
import copy
import hashlib
import json
from .lock import ROOT, REPOSITORIES, LockError, load, safe_path, validate as validate_v1, verify_sources
from scripts.contracts import validate as schema_validate

PILOT = {'core','nexus','services'}
SCENARIOS = tuple('ABCDEFGHIJ')


def projection(value):
    """Reuse F0 source admission, not its old gate decisions or runtime verdicts."""
    return {'format':'jarvis.integration-lock/1','mission':'FUSION-01/F0',
            'composition':'CANDIDATE_NOT_INTEGRATED','observed_at':value['observed_at'],
            'components':value['components'],'conflicts':[],
            'gates':[{'id':f'F{i}','depends_on':[] if i==0 else ['F0'],
                      'status':'VERIFIED' if i==0 else 'NOT_RUN','blockers':[],
                      'basis':'Source inventory projection only; not an integration gate.'} for i in range(9)],
            'frozen_contracts':value['frozen_contracts']}


def validate(value, baseline=None):
    schema_validate(value,load(ROOT/'tooling/integration/lock-v2.schema.json'))
    validate_v1(projection(value))
    baseline_bytes=(ROOT/'integration-lock.json').read_bytes() if baseline is None else (json.dumps(baseline,ensure_ascii=False,indent=2)+'\n').encode()
    if hashlib.sha256(baseline_bytes).hexdigest()!=value['baseline_sha256']:
        raise LockError('FUSION-01 baseline changed')
    if {v['module'] for v in value['versions']}!=set(REPOSITORIES):
        raise LockError('Exactly eight version profiles required')
    profiles={v['module']:v for v in value['versions']}
    if profiles['core']['min_sdk']!=24:
        raise LockError('CORE API24 must remain supported')
    components={c['id']:c for c in value['components']}
    for consumed in value['consumed']:
        if consumed['consumer']==consumed['dependency']:
            raise LockError('Self dependency')
        dependency=components[consumed['dependency']]
        if consumed['commit'] not in {r['commit'] for r in [dependency['primary'],*dependency['alternatives']]}:
            raise LockError('Consumed SHA absent from locked inventory')
        safe_path(consumed['binding_path'])
        if consumed['binding_path'] not in {f['path'] for f in components[consumed['consumer']]['primary']['files']}:
            raise LockError('Dependency binding itself must be fingerprinted')
    by_proof={}
    for p in value['proofs']:
        if p['id'] in by_proof:raise LockError('Duplicate proof ID')
        by_proof[p['id']]=p
        module=components[p['module']]
        ref=next((r for r in [module['primary'],*module['alternatives']] if r['commit']==p['commit']),None)
        if ref is None or p['evidence'] not in ref['files']:
            raise LockError('Proof must bind exact locked Git bytes')
        if p['result']=='PASS' and (not p['tests'] or p['failed'] or p['skipped']):
            raise LockError('Missing, failed or skipped tests cannot be a complete PASS')
        if p['level']=='JVM_PASS' and p['driver'] not in {'jvm','robolectric'}:
            raise LockError('Wrong JVM proof driver')
        if p['level']=='ANDROID_EMULATOR_PASS' and p['driver']!='android_instrumentation':
            raise LockError('Robolectric is not instrumentation')
        if p['level']=='ANDROID_DEVICE_PASS' and p['driver']!='physical_device':
            raise LockError('Emulator is not a personal device proof')
        if p['target']=='linux' and p['level']!='JVM_PASS':
            raise LockError('Linux cannot prove Android E2E')
        if p['target'].startswith('android') and p['level'] in {'ANDROID_EMULATOR_PASS','END_TO_END_PASS','ANDROID_DEVICE_PASS'}:
            if p['driver'] not in {'android_instrumentation','physical_device'}:
                raise LockError('Android runtime proof requires actual runtime driver')
    result=_assess(value)
    if value['status']=='READY' and result['blockers']:
        raise LockError('READY cannot reference missing Android proof or failed selected CI')
    return value


def _assess(value):
    components={c['id']:c for c in value['components']}
    blockers=list(value['blockers'])
    for module in sorted(PILOT):
        if components[module]['ci']['status']!='success':blockers.append('CI_NOT_SUCCESS:'+module)
    for module in ('nexus','services'):
        bindings=[c for c in value['consumed'] if c['consumer']=='core' and c['dependency']==module and c['role'] in {'runtime','build_library'}]
        if not bindings or any(c['commit']!=components[module]['primary']['commit'] for c in bindings):
            blockers.append('CORE_NOT_CONSUMING_PRIMARY:'+module)
    requirements={'nexus':{'document.search','citation.resolve'},
                  'services':{'csv.transform','csv.export','permission.fence'}}
    for target in value['required_targets']:
        for module,caps in requirements.items():
            available=set()
            for p in value['proofs']:
                if p['module']==module and p['target']==target and p['commit']==components[module]['primary']['commit'] and p['result']=='PASS' and p['level']=='ANDROID_EMULATOR_PASS':
                    available.update(p['capabilities'])
            if not caps<=available:blockers.append('ANDROID_PRODUCER_PROOF_MISSING:'+module+':'+target)
        for scenario in SCENARIOS:
            if not any(p['module']=='core' and p['target']==target and p['commit']==components['core']['primary']['commit'] and p['result']=='PASS' and p['level']=='END_TO_END_PASS' and p['scenario']==scenario for p in value['proofs']):
                blockers.append('ANDROID_E2E_MISSING:'+target+':'+scenario)
    return {'verdict':'BLOCKED' if blockers else 'READY',
            'android_multi_module_go':not blockers,'blockers':sorted(set(blockers)),
            'authorization_granted':False,'physical_device_qualified':False,
            'scope':'recorded evidence review only; not an installation or runtime permission'}


def assess(value):
    validate(value)
    return _assess(value)


def verify(value,repositories):
    validate(value)
    return verify_sources(projection(value),repositories)


def compare_to_v1(value,baseline=None):
    validate(value,baseline)
    baseline=load(ROOT/'integration-lock.json') if baseline is None else baseline
    old={c['id']:c for c in baseline['components']}
    return {'format':'jarvis.integration-diff/2','components':[
        {'module':c['id'],'before':old[c['id']]['primary']['commit'],'after':c['primary']['commit'],
         'changed':old[c['id']]['primary']['commit']!=c['primary']['commit'],
         'ci_before':old[c['id']]['ci']['status'],'ci_after':c['ci']['status'],
         'versions':next(v for v in value['versions'] if v['module']==c['id'])}
        for c in value['components']], 'consumed':copy.deepcopy(value['consumed']),
        'assessment':assess(value),'automatic_migration':False}


def report(value):
    validate(value)
    result=assess(value)
    lines=['# FUSION-02 — candidature Android-first', '',
           'Verdict : '+result['verdict']+'. Aucun droit d’installation ou activation accordé.', '',
           '| Module | Primaire | CI exacte | Android minSdk |', '|---|---|---|---|']
    profiles={v['module']:v for v in value['versions']}
    for c in value['components']:
        lines.append('| '+ ' | '.join([c['id'],c['primary']['commit'],c['ci']['status'],str(profiles[c['id']]['min_sdk'])+' (0 = hors Android)'])+' |')
    lines += ['', '## Prérequis Android24/25 manquants', '']
    lines += ['- '+b for b in result['blockers']]
    lines += ['', '## Preuves enregistrées, non réexécutées par ce rapport', '',
              '| Preuve | Module | Niveau | Cible | Verdict |', '|---|---|---|---|---|']
    for p in value['proofs']:
        lines.append('| '+' | '.join(p[k] for k in ['id','module','level','target','result'])+' |')
    return '\n'.join(lines)+'\n'
