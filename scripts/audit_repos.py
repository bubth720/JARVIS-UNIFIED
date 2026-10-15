#!/usr/bin/env python3
"""Read-only audit: source snapshots != declarations != CI != hardware evidence."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'registry/scripts'))
import update_registry as legacy


class AuditError(ValueError): pass
class RetrievalError(AuditError):
    def __init__(self,reason,http_status=None):self.reason,self.http_status=reason,http_status;super().__init__(reason)

SENSITIVE={'password','passwd','secret','token','access_token','authorization','private_key','credentials','prompt','personal_notes','audio_base64'}
TOKEN=re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}|(?:AKIA|ASIA)[A-Z0-9]{16})\b|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----|https?://[^\s/]+:[^\s/@]+@')


def no_sensitive(value):
    if isinstance(value,dict):
        for key,child in value.items():
            if key.lower() in SENSITIVE:raise AuditError('sensitive_data_rejected')
            no_sensitive(child)
    elif isinstance(value,list):
        for child in value:no_sensitive(child)
    elif isinstance(value,str) and TOKEN.search(value):raise AuditError('sensitive_data_rejected')


def validate_repositories(document):
    if document.get('schema_version')!=1 or not isinstance(document.get('repositories'),list):raise AuditError('invalid_registry')
    entries=document['repositories'];names=[e.get('name') for e in entries];ids=[e.get('id') for e in entries]
    if set(names)!=set(legacy.REPOSITORIES) or len(names)!=9 or len(set(ids))!=9:raise AuditError('duplicate_or_unknown_repository')
    for e in entries:
        if not re.fullmatch(r'[a-z0-9-]+',e['id']):raise AuditError('invalid_id')
        legacy.branch_name(e['inspection_branch'])
        sha=e.get('observed_commit')
        if sha is not None and not re.fullmatch('[0-9a-f]{40}',sha):raise AuditError('invalid_sha')
    no_sensitive(document)
    return True


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args):raise RetrievalError('redirect_refused')


class Api:
    def __init__(self,token_env=None,opener=None):
        if token_env not in (None,'GH_TOKEN','GITHUB_TOKEN'):raise AuditError('invalid_token_variable')
        self.token_env=token_env;self.opener=opener or urllib.request.build_opener(NoRedirect());self.requests=[]
    def _get(self,path,token=None):
        if not path.startswith('/repos/bubth720/'):raise AuditError('endpoint_forbidden')
        headers={'Accept':'application/vnd.github+json','User-Agent':'jarvis-consolidation-audit/1','X-GitHub-Api-Version':'2022-11-28'}
        if token:headers['Authorization']='Bearer '+token
        request=urllib.request.Request('https://api.github.com'+path,headers=headers,method='GET')
        try:
            with self.opener.open(request,timeout=15) as response:
                data=response.read(4*1024*1024+1)
                if len(data)>4*1024*1024:raise RetrievalError('response_too_large')
                value=legacy.loads(data);no_sensitive(value);return value
        except urllib.error.HTTPError as error:
            code=error.code
            reason='rate_limit' if code==429 or code==403 and error.headers.get('X-RateLimit-Remaining')=='0' else {401:'unauthorized',403:'forbidden',404:'not_found_or_inaccessible'}.get(code,'http_error')
            raise RetrievalError(reason,code) from None
        except urllib.error.URLError as error:
            reason='timeout' if isinstance(error.reason,(TimeoutError,socket.timeout)) else 'proxy_forbidden' if 'Tunnel connection failed: 403' in str(error.reason) else 'network_error'
            raise RetrievalError(reason) from None
        except (TimeoutError,socket.timeout):raise RetrievalError('timeout') from None
    def get(self,path):
        try:
            try:value=self._get(path)
            except RetrievalError as error:
                token=os.environ.get(self.token_env) if self.token_env and error.reason in {'unauthorized','forbidden','rate_limit'} else None
                if not token:raise
                value=self._get(path,token)
            self.requests.append({'method':'GET','url':'https://api.github.com'+path,'outcome':'retrieved','response_sha256':hashlib.sha256(legacy.dumps(value)).hexdigest()})
            return value
        except RetrievalError as error:
            self.requests.append({'method':'GET','url':'https://api.github.com'+path,'outcome':error.reason,'http_status':error.http_status});raise
    def pages(self,path,key=None):
        items=[]
        for page in range(1,11):
            data=self.get(path+('&' if '?' in path else '?')+'per_page=100&page='+str(page))
            value=data[key] if key else data
            if not isinstance(value,list):raise RetrievalError('invalid_api_data')
            items.extend(value)
            if len(value)<100:return items
        raise RetrievalError('pagination_limit')


def online_record(api,entry):
    repo=entry['name'];base='/repos/'+repo;branch=entry['inspection_branch']
    result={'repository_id':entry['id'],'repository':repo,'branch':branch,'source':'github_api','proof_type':'source','commit':None,'commit_date_utc':None,'retrieval':'not_checked','files':None,'main_relation':'unknown','ci':{'status':'not_checked'},'prs':{'status':'not_checked'},'hardware':'not_checked'}
    try:
        meta=api.get(base)
        if meta.get('full_name')!=repo:raise RetrievalError('identity_mismatch')
        result['visibility']='private' if meta.get('private') is True else 'public' if meta.get('private') is False else 'unknown'
        data=api.get(base+'/branches/'+urllib.parse.quote(branch,safe=''));sha=data['commit']['sha']
        if not isinstance(sha,str) or not re.fullmatch('[0-9a-f]{40}',sha):raise RetrievalError('invalid_sha')
        result['commit']=sha
        commit=api.get(base+'/commits/'+sha);result['commit_date_utc']=commit['commit']['committer']['date']
        result['retrieval']='confirmed';result['url']='https://github.com/'+repo+'/tree/'+sha
    except RetrievalError as error:
        result['retrieval']=error.reason;result['http_status']=error.http_status;return result
    except (KeyError,TypeError,AttributeError):result['retrieval']='invalid_api_data';return result
    try:
        branches=api.pages(base+'/branches');result['branches']=[{'name':b['name'],'sha':b['commit']['sha']} for b in branches]
        if meta.get('default_branch')=='main' or any(b['name']=='main' for b in branches):
            compare=api.get(base+'/compare/'+urllib.parse.quote(branch,safe='')+'...main')
            result['main_relation']='included' if compare['status'] in {'ahead','identical'} else 'not_included' if compare['status'] in {'behind','diverged'} else 'unknown'
    except (RetrievalError,KeyError,TypeError) as error:result['branch_detail_error']=error.reason if isinstance(error,RetrievalError) else 'invalid_api_data'
    try:
        pulls=api.pages(base+'/pulls?state=all')
        result['prs']={'status':'confirmed','items':[{'number':p['number'],'state':p['state'],'draft':p.get('draft'),'merged_at':p.get('merged_at'),'url':legacy.safe_url(p.get('html_url'))} for p in pulls]}
    except (RetrievalError,KeyError,TypeError) as error:result['prs']={'status':'unknown','reason':error.reason if isinstance(error,RetrievalError) else 'invalid_api_data'}
    try:
        runs=api.pages(base+'/actions/runs?head_sha='+sha,'workflow_runs');result['ci']=legacy.action_summary(runs,sha)
    except (RetrievalError,KeyError,TypeError,AttributeError) as error:result['ci']={'status':'unknown','reason':error.reason if isinstance(error,RetrievalError) else 'invalid_api_data'}
    return result


def normalize(record,baseline,at,max_age_days=7):
    no_sensitive(record);r=copy.deepcopy(record)
    sha=r.get('commit');stamp=r.get('captured_at',at)
    if r.get('proof_type')=='declaration':r['evidence_state']='declaration'
    elif r.get('retrieval')!='confirmed':
        r['evidence_state']='retrieval_error'
        r['main_relation']='unknown'
        r['ci']={'status':'not_checked','reason':'retrieval_failed'}
        r['prs']={'status':'not_checked','reason':'retrieval_failed'}
    elif not sha:
        r['evidence_state']='unknown_missing_sha'
        r['ci']={'status':'unknown','reason':'missing_sha'}
    else:
        if not isinstance(sha,str) or not re.fullmatch('[0-9a-f]{40}',sha):raise AuditError('invalid_sha')
        try:
            observed=datetime.fromisoformat(stamp.replace('Z','+00:00'));captured=datetime.fromisoformat(at.replace('Z','+00:00'))
            if observed.utcoffset() is None or captured.utcoffset() is None:raise ValueError()
            age=(captured-observed).total_seconds()
            if age<0:raise ValueError()
            r['evidence_state']='stale' if age>max_age_days*86400 else 'confirmed'
        except (ValueError,TypeError):r['evidence_state']='unknown_timestamp'
    r['captured_at']=stamp;r.setdefault('hardware','not_checked');r.setdefault('ci',{'status':'unknown'});r.setdefault('prs',{'status':'unknown'})
    old=baseline.get(r['repository_id'],{}).get('observed_commit')
    r['ref_change']={'previous':old,'observed':sha,'state':'unknown' if sha is None or old is None else 'unchanged' if old==sha else 'changed'}
    r['runtime_integration']='not_demonstrated_by_audit'
    return r


def run_audit(registry,fixture=None,api=None,baseline=None):
    validate_repositories(registry)
    previous={e['id']:e for e in (baseline or registry)['repositories']}
    if fixture is not None:
        no_sensitive(fixture)
        if fixture.get('synthetic') is not True:raise AuditError('synthetic_marker_required')
        records=fixture['records'];at=fixture['captured_at'];source='synthetic_fixture'
        allowed={e['id']:e['name'] for e in registry['repositories']};seen=set()
        for rec in records:
            rid=rec['repository_id']
            if rid not in allowed or rid in seen or rec['repository']!=allowed[rid]:raise AuditError('duplicate_or_ambiguous_identity')
            seen.add(rid)
        if seen!=set(allowed):raise AuditError('missing_fixture_repository')
    else:
        at=datetime.now(timezone.utc).isoformat(timespec='seconds');source='github_api'
        records=[online_record(api,e) for e in registry['repositories']]
    results=[normalize(rec,previous,at) for rec in records]
    report={'schema_version':1,'captured_at':at,'source':source,'synthetic':source=='synthetic_fixture','repositories':results,'requests':api.requests if api else [],'runtime_qualification':False}
    no_sensitive(report)
    return report


def markdown(report):
    lines=['# Audit JARVIS — '+report['source'],'','Capture UTC : '+report['captured_at']+'. Aucune qualification runtime ou matérielle déduite.','', '| Dépôt | Preuve | SHA | Relation main | CI | Changement ref |','|---|---|---|---|---|---|']
    for r in report['repositories']:
        lines.append('| '+' | '.join(legacy.md(x) for x in [r['repository'],r['evidence_state']+' / '+r.get('retrieval','unknown'),r.get('commit') or 'unknown',r.get('main_relation','unknown'),r['ci']['status'],r['ref_change']['state']])+' |')
    return '\n'.join(lines)+'\n'


def write_report(report,output):
    # Validate everything, including unexpected fields, before any output write.
    no_sensitive(report);data=legacy.dumps(report);summary=markdown(report).encode();output.mkdir(parents=True,exist_ok=True)
    for name,content in [('audit.json',data),('SUMMARY.md',summary)]:
        fd,temp=tempfile.mkstemp(prefix='.audit-',dir=output)
        try:
            with os.fdopen(fd,'wb') as f:f.write(content);f.flush();os.fsync(f.fileno())
            os.replace(temp,output/name)
        finally:
            if os.path.exists(temp):os.unlink(temp)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);m=p.add_mutually_exclusive_group(required=True);m.add_argument('--online',action='store_true');m.add_argument('--offline',action='store_true')
    p.add_argument('--registry',type=Path,default=ROOT/'registry/repositories.json');p.add_argument('--baseline',type=Path)
    p.add_argument('--fixtures',type=Path,default=ROOT/'tests/fixtures/audit.json');p.add_argument('--output-dir',type=Path)
    p.add_argument('--token-env',choices=['GH_TOKEN','GITHUB_TOKEN']);a=p.parse_args(argv)
    try:
        registry=legacy.read_json(a.registry);baseline=legacy.read_json(a.baseline) if a.baseline else registry
        if a.offline and a.token_env:raise AuditError('offline_credentials_forbidden')
        report=run_audit(registry,legacy.read_json(a.fixtures) if a.offline else None,None if a.offline else Api(a.token_env),baseline)
        output=a.output_dir or ROOT/'reports'/('offline' if a.offline else 'online')
        if output.resolve()==ROOT/'registry' or ROOT/'registry' in output.resolve().parents:raise AuditError('registry_output_forbidden')
        write_report(report,output);print(markdown(report))
        return 0 if a.offline or all(r['evidence_state']=='confirmed' for r in report['repositories']) else 2
    except (AuditError,legacy.RegistryError,OSError,ValueError,TypeError,KeyError) as error:
        print('Audit refusé : '+(str(error) if isinstance(error,AuditError) else type(error).__name__),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
