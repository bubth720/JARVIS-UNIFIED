"""Validate the deliberately bounded JSON Schema subset used by contracts/v1.

Not a general JSON Schema implementation; unsupported keywords fail closed.
All schema documents remain portable draft2020-12 documents.
"""
from datetime import datetime
import math
import re
import uuid


class ContractError(ValueError): pass

KEYWORDS={'$schema','$id','title','description','type','properties','required','additionalProperties','items','minItems','maxItems','uniqueItems','minLength','maxLength','minimum','maximum','pattern','enum','const','oneOf','allOf','format'}


def validate_schema(schema):
    if not isinstance(schema,dict) or set(schema)-KEYWORDS:raise ContractError('Unsupported schema keyword')
    if 'format' in schema and schema['format'] not in {'uuid','date-time'}:raise ContractError('Unsupported format')
    for sub in schema.get('properties',{}).values():validate_schema(sub)
    if isinstance(schema.get('items'),dict):validate_schema(schema['items'])
    for k in ['oneOf','allOf']:
        for sub in schema.get(k,[]):validate_schema(sub)


def validate(value,schema):
    validate_schema(schema)
    def check(v,s):
        if 'type' in s:
            t=s['type'];ok={'object':isinstance(v,dict),'array':isinstance(v,list),'string':isinstance(v,str),'integer':type(v) is int,'number':type(v) is int or type(v) is float and math.isfinite(v),'boolean':type(v) is bool,'null':v is None}.get(t,False)
            if not ok:raise ContractError('Type mismatch')
        if 'const' in s and (type(v) is not type(s['const']) or v!=s['const']):raise ContractError('Constant mismatch')
        if 'enum' in s and not any(type(v) is type(x) and v==x for x in s['enum']):raise ContractError('Unknown value')
        if isinstance(v,dict):
            if not set(s.get('required',[]))<=set(v):raise ContractError('Missing field')
            if s.get('additionalProperties') is False and set(v)-set(s.get('properties',{})):raise ContractError('Unknown field')
            for key,child in s.get('properties',{}).items():
                if key in v:check(v[key],child)
        if isinstance(v,list):
            if not s.get('minItems',0)<=len(v)<=s.get('maxItems',len(v)):raise ContractError('Array limit')
            if s.get('uniqueItems') and any(v[i]==v[j] for i in range(len(v)) for j in range(i)):raise ContractError('Duplicate item')
            for item in v:
                if 'items' in s:check(item,s['items'])
        if isinstance(v,str):
            if not s.get('minLength',0)<=len(v)<=s.get('maxLength',len(v)):raise ContractError('String limit')
            if 'pattern' in s and not re.search(s['pattern'],v):raise ContractError('Pattern mismatch')
            if s.get('format')=='uuid':
                try:
                    if str(uuid.UUID(v))!=v:raise ValueError()
                except ValueError:raise ContractError('Canonical UUID required') from None
            if s.get('format')=='date-time':
                try:
                    if datetime.fromisoformat(v.replace('Z','+00:00')).utcoffset().total_seconds()!=0:raise ValueError()
                except (ValueError,AttributeError):raise ContractError('UTC date-time required') from None
        if type(v) in (int,float):
            if type(v) is float and not math.isfinite(v) or not s.get('minimum',v)<=v<=s.get('maximum',v):raise ContractError('Numeric limit')
        for child in s.get('allOf',[]):check(v,child)
        if 'oneOf' in s:
            count=0
            for child in s['oneOf']:
                try:check(v,child);count+=1
                except ContractError:pass
            if count!=1:raise ContractError('Exactly one alternative required')
    check(value,schema)
    return True


def validate_contract(name,value,schema):
    validate(value,schema)
    if name=='request-envelope':
        d=value['deadline'];duration=d['expires_at_ms']-d['sent_at_ms']
        if duration<=0 or duration>value['limits']['timeout_ms']:raise ContractError('Invalid remaining deadline')
        p=value['payload']
        if value['capability']=='text.generate' and 'model_sha256' not in p:raise ContractError('Model fingerprint required')
        if value['capability']=='speech.synthesize' and not {'voice_profile_ref','pack_sha256'}<=set(p):raise ContractError('Exact voice binding required')
    if name=='resource-lease':
        v=value
        if v['state']=='released' and not (v['effective_end'] and v['release_confirmed'] and not v['model_resident']):raise ContractError('Release before effective end')
        if v['state']!='released' and v['release_confirmed']:raise ContractError('Release is not confirmed')
        if v['state']=='stop_requested' and not v['cancellation_requested']:raise ContractError('Cancellation state inconsistent')
        if v['decision']=='refused' and (v['model_resident'] or v['state']!='idle'):raise ContractError('Refusal cannot own a resident model')
    if name=='capability-manifest':
        ids=[x['id'] for x in value['capabilities']]
        if len(ids)!=len(set(ids)):raise ContractError('Duplicate capability')
        if value['state']!='available' and any(c['available'] for c in value['capabilities']):raise ContractError('Unavailable module advertises available capability')
    if name=='health-status' and value['state']=='unknown' and value['reason_code']=='OK':raise ContractError('Unknown health cannot be OK')
    return True


def validate_exchange(request,response):
    if request['correlation_id']!=response['correlation_id']:raise ContractError('Unmatched response')
    if request['destination']!=response['provenance']['module_id']:raise ContractError('Wrong responding module')
    return True
