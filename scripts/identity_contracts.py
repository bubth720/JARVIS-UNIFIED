#!/usr/bin/env python3
"""Offline ID-001B candidate validation. No runtime, permissions, storage writes or prompt composer."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

try:
    from .contracts import validate as schema_validate, validate_schema, ContractError
except ImportError:
    from contracts import validate as schema_validate, validate_schema, ContractError

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT/'docs/IDENTITY/001B'
VERSION = 'jarvis.identity/1'
REVISION = '001B.1-candidate'
MAX_INTEGER = 9007199254740991
KINDS = ('manifest','snapshot','jarvis-preference','personal-preference','consent','change-proposal','decision','application')

class IdentityError(ValueError):
    pass

def fail(code):
    raise IdentityError(code)

def bounded(value,depth=0,counter=None):
    if counter is None:counter=[0]
    counter[0]+=1
    if depth>8 or counter[0]>1024:fail('STRUCTURE_LIMIT')
    if isinstance(value,str):
        try:b=value.encode('utf-8',errors='strict')
        except UnicodeError:fail('INVALID_UTF8')
        if len(b)>8192 or any(ord(c)<32 and c not in '\n\r\t' or ord(c)==127 for c in value):fail('STRING_LIMIT')
    elif type(value) is int:
        if not 0<=value<=MAX_INTEGER:fail('INTEGER_LIMIT')
    elif type(value) is bool or value is None:pass
    elif isinstance(value,list):
        if len(value)>16:fail('LIST_LIMIT')
        for child in value:bounded(child,depth+1,counter)
    elif isinstance(value,dict):
        for key,child in value.items():
            if type(key) is not str or not re.fullmatch('[a-z][a-z0-9_]{0,47}',key):fail('INVALID_KEY')
            bounded(child,depth+1,counter)
    else:fail('TYPE_NOT_SUPPORTED')

def depth_scan(text):
    depth=0;quoted=False;escaped=False
    for c in text:
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c in '[{':
            depth+=1
            if depth>8:fail('STRUCTURE_LIMIT')
        elif c in ']}':depth-=1

def unique_pairs(items):
    d={}
    for k,v in items:
        if k in d:fail('DUPLICATE_FIELD')
        d[k]=v
    return d

def decode(raw):
    if type(raw) is not bytes:fail('BYTES_REQUIRED')
    if len(raw)>32768:fail('WIRE_LIMIT')
    try:
        text=raw.decode('utf-8',errors='strict');depth_scan(text)
        v=json.loads(text,object_pairs_hook=unique_pairs,parse_float=lambda _:fail('FLOAT_FORBIDDEN'),parse_constant=lambda _:fail('NONFINITE_FORBIDDEN'))
    except (UnicodeError,json.JSONDecodeError,RecursionError):fail('MALFORMED_JSON')
    bounded(v)
    if type(v) is not dict:fail('OBJECT_REQUIRED')
    return v

def canonical(value):
    bounded(value)
    raw=json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
    if len(raw)>32768:fail('WIRE_LIMIT')
    return raw

def digest(value):
    return hashlib.sha256(b'jarvis.identity/1:001B.1\0'+canonical(value)).hexdigest()

def utf8_constraints(value,schema):
    if isinstance(value,str) and 'maxLength' in schema and len(value.encode('utf-8'))>schema['maxLength']:fail('UTF8_FIELD_LIMIT')
    if isinstance(value,dict):
        for k,v in value.items():
            if k in schema.get('properties',{}):utf8_constraints(v,schema['properties'][k])
    if isinstance(value,list):
        for v in value:utf8_constraints(v,schema.get('items',{}))
    if 'oneOf' in schema:
        for choice in schema['oneOf']:
            try:schema_validate(value,choice)
            except ContractError:continue
            utf8_constraints(value,choice)

def validate_object(value):
    bounded(value)
    if type(value) is not dict or value.get('kind') not in KINDS:fail('UNSUPPORTED_KIND')
    name=value['kind'];schema=json.loads((SPEC/'schemas'/(name+'.schema.json')).read_text())
    try:validate_schema(schema);schema_validate(value,schema)
    except ContractError:fail('SCHEMA_INVALID')
    utf8_constraints(value,schema)
    raw=canonical(value)
    if name=='manifest' and len(raw)>4096:fail('MANIFEST_LIMIT')
    if 'expires_ms' in value and value['expires_ms']<=value['created_ms']:fail('INVALID_LIFETIME')
    styles=json.loads((SPEC/'STYLE_TABLE.json').read_text())
    if name in ('jarvis-preference','personal-preference') and value['value'] not in styles[value['key']]:fail('STYLE_VALUE_MISMATCH')
    if name=='jarvis-preference':
        if (value['provenance']=='PROGRAMMED') != (value['decision_ref'] is None):fail('PREFERENCE_DECISION_REQUIRED')
    if name=='change-proposal':
        patch=value['patch']
        if not patch or len({x['key'] for x in patch})!=len(patch):fail('PATCH_KEYS')
        for x in patch:
            if x['old_value'] not in styles[x['key']] or x['new_value'] not in styles[x['key']] or x['old_value']==x['new_value']:fail('PATCH_VALUE')
        if (value['target_kind']=='personal-preference') != (value['sensitivity']=='PERSONAL'):fail('SENSITIVITY_MISMATCH')
        if value['sensitivity']=='PERSONAL' and value['storage']!='EPHEMERAL_ONLY':fail('PERSONAL_PERSISTENCE_FORBIDDEN')
    if name=='application':
        state=value['state']
        if state in ('STAGED','FAILED') and value['result_sha256'] is not None:fail('APPLICATION_RESULT')
        if state=='APPLIED' and (value['result_sha256'] is None or value['result_sha256']==value['previous_sha256']):fail('APPLICATION_RESULT')
        if state=='ROLLED_BACK' and (value['rollback_ref'] is None or value['result_sha256']!=value['previous_sha256']):fail('ROLLBACK_PROOF')
    return True

def reference(value):return {'id':value['id'],'revision':value['revision'],'sha256':digest(value)}

def validate_graph(records,now_ms):
    """Check a fully supplied synthetic graph; never authenticate a receipt or grant permission."""
    if type(now_ms) is not int or not 0<=now_ms<=MAX_INTEGER:fail('INVALID_TIME')
    if not isinstance(records,list) or not 1<=len(records)<=16:fail('GRAPH_LIMIT')
    index={}
    for record in records:
        validate_object(record)
        key=(record['id'],record['revision'])
        if key in index or any(x['id']==record['id'] and x['kind']!=record['kind'] for x in index.values()):fail('DUPLICATE_ID')
        index[key]=record
    def resolve(ref,kind=None):
        record=index.get((ref['id'],ref['revision']))
        if record is None or reference(record)!=ref or kind and record['kind']!=kind:fail('REFERENCE_MISMATCH')
        return record
    for r in records:
        kind=r['kind']
        if kind=='snapshot':
            m=resolve(r['manifest_ref'],'manifest')
            if r['composer_revision']!=m['composer_revision'] or r['styles']!=m['styles']:fail('SNAPSHOT_MISMATCH')
            if r['jarvis_preferences'] or r['personal_preferences'] or r['consents']:fail('ID002_READ_ONLY_SCOPE')
            if not r['created_ms']<=now_ms<r['expires_ms']:fail('EXPIRED')
        elif kind=='jarvis-preference' and r['decision_ref'] is not None:
            d=resolve(r['decision_ref'],'decision')
            if d['decision']!='APPROVED':fail('DECISION_NOT_APPROVED')
            p=resolve(d['proposal_ref'],'change-proposal')
            if p['target_kind']!='jarvis-preference' or p['base_ref']['id']!=r['id'] or p['base_ref']['revision']+1!=r['revision']:fail('DECISION_BINDING')
            if len(p['patch'])!=1 or p['patch'][0]['key']!=r['key'] or p['patch'][0]['new_value']!=r['value']:fail('DECISION_BINDING')
        elif kind=='consent':
            target=resolve(r['content_ref'],'personal-preference')
            if target['subject_ref']!=r['subject_ref']:fail('SUBJECT_MISMATCH')
        elif kind=='change-proposal':
            base=resolve(r['base_ref'],r['target_kind'])
            if base['kind']=='manifest' and any(base['styles'][x['key']]!=x['old_value'] for x in r['patch']):fail('BASE_CONFLICT')
            if base['kind'] in ('jarvis-preference','personal-preference') and (len(r['patch'])!=1 or r['patch'][0]['key']!=base['key'] or r['patch'][0]['old_value']!=base['value']):fail('BASE_CONFLICT')
        elif kind=='decision':resolve(r['proposal_ref'],'change-proposal')
        elif kind=='application':
            p=resolve(r['proposal_ref'],'change-proposal');d=resolve(r['decision_ref'],'decision')
            if d['proposal_ref']!=r['proposal_ref'] or r['previous_sha256']!=p['base_ref']['sha256']:fail('DECISION_BINDING')
            if d['decision']!='APPROVED' or not d['created_ms']<=r['created_ms']<d['expires_ms']:fail('DECISION_NOT_APPROVED')
            base=resolve(p['base_ref'],p['target_kind'])
            if base['kind']=='manifest' and r['state']=='APPLIED':
                expected=dict(base);expected['styles']=dict(base['styles']);expected['revision']+=1
                for patch in p['patch']:expected['styles'][patch['key']]=patch['new_value']
                if digest(expected)!=r['result_sha256']:fail('RESULT_DIGEST_MISMATCH')
    return True

def consent_effective(consents,target,subject,now_ms):
    """Synthetic review helper: content matching is not proof of UI authentication."""
    validate_object(target)
    if target['kind']!='personal-preference' or target['subject_ref']!=subject:return False
    if type(now_ms) is not int or not 0<=now_ms<=MAX_INTEGER:fail('INVALID_TIME')
    matching=[]
    for c in consents:
        validate_object(c)
        if c['kind']=='consent' and c['content_ref']==reference(target) and c['subject_ref']==subject:matching.append(c)
    if not target['created_ms']<=now_ms<target['expires_ms']:return False
    if not matching:return False
    latest=max(x['consent_revision'] for x in matching);items=[x for x in matching if x['consent_revision']==latest]
    if len(items)!=1:return False
    c=items[0]
    return c['decision']=='GRANTED' and c['created_ms']<=now_ms<c['expires_ms']

def bundle_paths():
    return sorted(['CONTRACT.md','IdentityPort.md','STYLE_TABLE.json','limits.json','vectors.json','CORPUS_PERSONA.json']+[str(p.relative_to(SPEC)) for p in (SPEC/'schemas').glob('*.schema.json')])

def bundle_material():
    h=hashlib.sha256();entries=[]
    for name in bundle_paths():
        data=(SPEC/name).read_bytes();h.update(name.encode('utf-8')+b'\0'+data+b'\0')
        entries.append({'path':name,'sha256':hashlib.sha256(data).hexdigest()})
    return h.hexdigest(),entries

def check_bundle():
    expected=json.loads((SPEC/'BUNDLE.json').read_text());actual,entries=bundle_material()
    if actual!=expected['bundle_sha256'] or entries!=expected['files']:fail('BUNDLE_MISMATCH')
    if hashlib.sha256(Path(__file__).read_bytes()).hexdigest()!=expected['validator_sha256']:fail('VALIDATOR_MISMATCH')
    return actual

def self_check():
    valid=invalid=0
    for p in sorted((SPEC/'examples').glob('*.valid.json')):validate_object(decode(p.read_bytes()));valid+=1
    for p in sorted((SPEC/'examples').glob('*.invalid.json')):
        try:validate_object(decode(p.read_bytes()))
        except IdentityError:invalid+=1
        else:raise AssertionError('Invalid example accepted: '+p.name)
    validate_graph([decode(p.read_bytes()) for p in sorted((SPEC/'examples').glob('*.valid.json'))],2000)
    vectors=json.loads((SPEC/'vectors.json').read_text())
    for v in vectors['vectors']:
        assert canonical(v['value']).hex()==v['canonical_hex']
        assert digest(v['value'])==v['sha256']
    return {'valid_examples':valid,'invalid_examples_rejected':invalid,'vectors':len(vectors['vectors']),'runtime_or_authentication_proof':False,'candidate_bundle_sha256':check_bundle()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--self-check',action='store_true');parser.add_argument('file',nargs='?');args=parser.parse_args()
    if args.self_check:print(json.dumps(self_check()));return
    if not args.file:parser.error('file or --self-check required')
    value=decode(Path(args.file).read_bytes());validate_object(value);print(json.dumps({'valid':True,'sha256':digest(value),'runtime_or_authentication_proof':False}))
if __name__=='__main__':main()
