"""Proposed contracts, checked offline only. No fence, worker, journal or grant implementation."""
from scripts.contracts import validate as schema_validate
from .lock import ROOT,load,LockError


def receipt(value):
    schema_validate(value,load(ROOT/'docs/fusion-02/proposals/operation-receipt.schema.json'))
    state=value['state'];auth=value['authorization_at_commit'];effect=value['effect']
    if auth=='DENIED' and effect!='NONE':raise LockError('Denied decision cannot start an effect')
    if effect in {'STARTED','CONFIRMED'} and not (auth=='GRANTED' and value['confirmation_consumed']):
        raise LockError('Effect without owner decision and exact consumed confirmation')
    if value['readback_verified'] and (not value['output_sha256'] or effect!='CONFIRMED'):
        raise LockError('Readback without exact bytes')
    if state=='PREPARED' and (auth!='NOT_CHECKED' or effect!='NONE' or value['confirmation_consumed']):
        raise LockError('Prepared receipt cannot claim an effect')
    if state=='COMMITTED' and (auth!='GRANTED' or effect!='CONFIRMED' or not value['readback_verified'] or not value['output_sha256'] or value['error'] not in {'NONE','PERMISSION_REVOKED'}):
        raise LockError('COMMITTED requires actual durable decision and readback evidence')
    if value['permission_revoked_after_commit'] and auth!='GRANTED':
        raise LockError('No commit decision before later revocation')
    if value['error']=='ACK_LOST' and state!='UNKNOWN':raise LockError('Missing ACK remains UNKNOWN')
    return value


def transition(previous,current):
    receipt(previous);receipt(current)
    immutable=('session_id','request_id','generation','operation_sha256','destination_ref','confirmation_ref')
    if any(previous[k]!=current[k] for k in immutable):raise LockError('Wrong receipt binding')
    if previous==current:return current  # rereading exact terminal bytes, never permission to re-execute
    if previous['state'] in {'COMMITTED','UNKNOWN'}:raise LockError('Terminal receipt cannot restart automatically')
    if current['sequence']!=previous['sequence']+1:raise LockError('Stale or missing receipt sequence')
    allowed={'PREPARED':{'DISPATCHED','UNKNOWN'},'DISPATCHED':{'DISPATCHED','COMMITTED','UNKNOWN'}}
    if current['state'] not in allowed[previous['state']]:raise LockError('Invalid receipt transition')
    if previous['authorization_at_commit']=='GRANTED' and (current['authorization_at_commit']!='GRANTED' or current['permission_generation']!=previous['permission_generation']):
        raise LockError('Cannot rewrite historical commit decision')
    return current


def capability(value,lock):
    from .v2 import validate
    validate(lock)
    schema_validate(value,load(ROOT/'docs/fusion-02/proposals/capability-status.schema.json'))
    module=next(c for c in lock['components'] if c['id']==value['module'])
    if value['build_commit']!=module['primary']['commit']:raise LockError('Capability belongs to another build')
    proofs={p['id']:p for p in lock['proofs']}
    if any(i not in proofs for i in value['proof_ids']):raise LockError('Unknown capability proof')
    if value['state']=='READY':
        if value['reason']!='VERIFIED_PRODUCT' or module['ci']['status']!='success' or not value['proof_ids']:
            raise LockError('No READY from collector status, failed CI or missing evidence')
        for identifier in value['proof_ids']:
            p=proofs[identifier]
            if p['module']!=value['module'] or p['commit']!=value['build_commit'] or p['target']!=value['target'] or p['result']!='PASS' or value['capability'] not in p['capabilities']:
                raise LockError('Unrelated capability proof')
            if value['target'].startswith('android') and p['driver'] not in {'android_instrumentation','physical_device'}:
                raise LockError('JVM/Robolectric does not prove Android availability')
    elif value['reason']=='VERIFIED_PRODUCT':raise LockError('Unknown capability cannot claim verified product')
    return value


def check_examples(lock):
    directory=ROOT/'docs/fusion-02/proposals'
    for name,validator in [('operation-receipt',receipt),('capability-status',lambda v:capability(v,lock))]:
        validator(load(directory/(name+'.valid.json')))
        try:validator(load(directory/(name+'.invalid.json')))
        except ValueError:pass
        else:raise LockError('Invalid proposed example accepted')
    return {'valid_examples':2,'invalid_examples_rejected':2,'approved':False,'runtime_implemented':False}
