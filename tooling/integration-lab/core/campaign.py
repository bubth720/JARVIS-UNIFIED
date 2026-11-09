"""Persist each observation, continue independent modules after errors, never retry a command."""
import datetime,json,os,platform,subprocess,sys,uuid
from pathlib import Path
from . import repository,integrity,policy,builder,dependencies,contracts,android,evidence,reporting

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[1]

def identity():
    return {'lab_commit':integrity.git(ROOT,'rev-parse','HEAD').decode().strip(),
            'lab_tree':integrity.git(ROOT,'rev-parse','HEAD^{tree}').decode().strip(),
            'lab_dirty':bool(integrity.git(ROOT,'status','--porcelain').strip()),
            'lab_files_sha256':{p.relative_to(HERE).as_posix():integrity.sha(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.suffix in {'.py','.json','.sha256','.html','.txt','.md'}}}

def recover(output):
    p=Path(output)/'campaign.json';r=json.loads(p.read_text())
    if r['lock_sha256']!=integrity.sha(HERE/'config/modules.lock.json'):raise ValueError('RESUME_LOCK_MISMATCH')
    if r['lab_commit']!=identity()['lab_commit']:raise ValueError('RESUME_CODE_MISMATCH')
    for c in r.get('commands',[]):
        if c.get('log'):
            p=policy.child(output,c['log'])
            if integrity.sha(p)!=c['log_sha256']:raise ValueError('RESUME_EVIDENCE_DRIFT')
        for artifact in c.get('junit_evidence',[]):
            if integrity.sha(policy.child(output,artifact['path']))!=artifact['sha256']:raise ValueError('RESUME_JUNIT_DRIFT')
    for artifact in r.get('apks',{}).get('artifacts',[]):
        if integrity.sha(policy.child(output,artifact['path']))!=artifact['sha256']:raise ValueError('RESUME_APK_DRIFT')
    if r.get('status')=='RUNNING':
        r.update(status='UNKNOWN',interruption='INCOMPLETE_COMMAND_NOT_RETRIED',active=None)
    evidence.write(Path(output)/'campaign.json',r);reporting.render(r,output);evidence.export(output)
    return r

def run(args,phase='run'):
    out=Path(args.output).resolve()
    if args.resume:return recover(out)
    if (out/'campaign.json').exists():raise ValueError('EXISTING_CAMPAIGN_USE_NEW_OUTPUT_OR_RESUME')
    if out==ROOT or out in ROOT.parents:raise ValueError('PROTECTED_OUTPUT_DIRECTORY')
    if out.is_relative_to(ROOT) and integrity.git(ROOT,'ls-files','--',out.relative_to(ROOT).as_posix()).strip():raise ValueError('PROTECTED_OUTPUT_DIRECTORY')
    if out.exists() and any(out.iterdir()):raise ValueError('NONEMPTY_OUTPUT_DIRECTORY')
    lock=repository.read_lock(HERE/'config/modules.lock.json');out.mkdir(parents=True,exist_ok=True)
    from tooling.contracts.manifest import strict_json
    selected_profile=strict_json((HERE/'config/profiles'/(args.profile+'.json')).read_text())
    policy.runtime_selection(selected_profile['runtime_modules'])
    if any(selected_profile.get(k) is not False for k in ['model_acquisition','core_llm_admission','physical_devices','emulator_boot']):raise ValueError('UNAUTHORIZED_PROFILE')
    capabilities=strict_json((HERE/'config/capabilities.json').read_text())
    if capabilities['module_runtime_states']!={m:'DISABLED' for m in policy.MODULES} or capabilities['authority_roots'] or capabilities['scope']!='DEVELOPMENT_TOOL_ONLY':raise ValueError('UNAUTHORIZED_CAPABILITY_REGISTRY')
    sources_root=Path(args.source_root).resolve() if args.source_root else out/'workspace/sources'
    # Never build in the LAB itself or in its preserved parent checkout.
    if sources_root==ROOT or sources_root in ROOT.parents:raise ValueError('ORIGINAL_SOURCE_DIRECTORY_REFUSED')
    r={**identity(),'schema':'jarvis.integration-lab.receipt/1','id':str(uuid.uuid4()),
       'date_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'profile':args.profile,
       'phase':phase,'status':'RUNNING','active':None,'modules':[],'commands':[],
       'environment':{'system':platform.system(),'machine':platform.machine(),'python':platform.python_version(),
                      'runner_image':os.environ.get('ImageVersion','UNKNOWN')},
       'github':{'run_id':os.environ.get('GITHUB_RUN_ID'),'run_attempt':os.environ.get('GITHUB_RUN_ATTEMPT'),
                 'repository':os.environ.get('GITHUB_REPOSITORY'),'ref':os.environ.get('GITHUB_REF')},
       'lock_sha256':integrity.sha(HERE/'config/modules.lock.json'),'build_cache_state':'UNKNOWN',
       'android':{'status':'NOT_RUN','kind':'EMULATOR','reason':'SAFE_PROFILE' if args.profile=='safe' else 'PENDING'},
       'apks':{'status':'NOT_RUN','ready_to_install':False},'runtime_modules':['INTERFACE_LOCAL_ONLY'],
       'capabilities':capabilities,'selected_profile':selected_profile,
       'sensitive_gates':'CLOSED','llm_generation':'NOT_RUN','physical':'NOT_RUN'}
    def save():evidence.write(out/'campaign.json',r)
    save();sources={};rows={m['module']:m for m in lock['modules']}
    try:
        for row in lock['modules']:
            item={k:row[k] for k in ['module','repository','branch','commit','tree','contract_version']};item['runtime_enabled']=False
            r['active']='VERIFY_'+row['module'];save()
            try:
                source,proof=repository.acquire(row,sources_root,args.offline);sources[row['module']]=source
                item.update(status='PASS',integrity=proof,dependencies=dependencies.inspect(source))
            except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as e:item.update(status='BLOCKED',reason=str(e))
            r['modules'].append(item);save()
        r['compatibility']=[]
        available={m['module']:m for m in r['modules'] if m['status']=='PASS'}
        for a in rows:
            for b in rows:
                if a==b:continue
                result=dependencies.compare(available[a]['dependencies'],available[b]['dependencies']) if a in available and b in available else {'status':'BLOCKED','scope':'SHARED_TOOLCHAIN_NOT_RUNTIME','mismatches':[],'unknown':['SOURCE_UNAVAILABLE'],'runtime_connected':False}
                r['compatibility'].append({'from':a,'to':b,**result})
        try:r['contracts']=contracts.inspect(sources)
        except (OSError,ValueError) as e:r['contracts']={'status':'FAIL','reason':str(e),'links':[]}
        requested=[]
        if phase in ['run','test']:requested+=policy.TEST_IDS
        if phase in ['run','build']:requested+=policy.BUILD_IDS
        if phase=='android':requested+=['interface-m51']
        failed_modules=set()
        for identifier in requested:
            owner=policy.command_owner(identifier);r['active']=identifier;save()
            if owner not in sources or owner in failed_modules:
                result={'id':identifier,'module':owner,'kind':'STATIC','status':'NOT_RUN','reason':'SOURCE_UNAVAILABLE_OR_CRITICAL_STOP'}
            else:
                try:
                    result=builder.run(identifier,rows[owner],sources[owner],out,offline=args.offline)
                    if result.get('critical'):failed_modules.add(owner)
                except (OSError,ValueError,RuntimeError,subprocess.SubprocessError) as e:result={'id':identifier,'module':owner,'kind':'STATIC','status':'BLOCKED','reason':str(e)}
            r['commands'].append(result);print(json.dumps({k:result.get(k) for k in ['id','module','status','reason','test_invocations','unique_test_cases']}),flush=True);save()
        if phase in ['run','build','android'] and 'INTERFACE' in sources:
            done=next((x for x in r['commands'] if x['id']=='interface-m51'),None)
            if done and done['status']=='PASS':
                try:r['apks']=builder.collect_apks(sources['INTERFACE'],rows['INTERFACE'],out)
                except (OSError,ValueError) as e:r['apks']={'status':'FAIL','reason':str(e),'ready_to_install':False}
        if phase=='android' or (phase=='run' and args.profile=='android_lab'):
            if args.profile!='android_lab':raise ValueError('ANDROID_LAB_PROFILE_REQUIRED')
            if 'INTERFACE' not in sources:r['android']={'status':'BLOCKED','reason':'INTERFACE_SOURCE_UNAVAILABLE'}
            else:r['android']=android.qualify(sources['INTERFACE'],rows['INTERFACE'],r['apks'],out,args.serial,args.api)
        for m in r['modules']:
            if m['module'] in sources:
                try:m['integrity_after']=integrity.verify(sources[m['module']],rows[m['module']])
                except (ValueError,OSError) as e:m.update(status='FAIL',reason=str(e))
                states=[c['status'] for c in r['commands'] if c['module']==m['module']]
                if states:m['status']=policy.aggregate([m['status'],*states])
        required=[m['status'] for m in r['modules']]+[r['contracts']['status']]
        if phase in ['run','build']:required.append(r['apks']['status'])
        if args.profile=='android_lab' or phase=='android':required.append(r['android']['status'])
        r.update(status=policy.aggregate(required),active=None)
    except BaseException:
        r.update(status='UNKNOWN',interruption='INTERRUPTED_NO_AUTO_RETRY');raise
    finally:
        save();reporting.render(r,out);evidence.export(out)
    return r
