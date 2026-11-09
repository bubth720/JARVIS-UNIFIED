"""Admit an already available emulator only. Never boot, grant permissions or touch physical devices."""
import json, os, re, subprocess, time
from pathlib import Path
from .runner import execute
from .integrity import sha, verify

def incident(window, events, crashes):
    # Same conservative system-crash policy as pinned M51-R1, including startup incidents.
    if re.search(r'(Application Not Responding:|ANR in)\s*com\.android\.(systemui|launcher3|settings)',window): return 'SYSTEM_ANR_WINDOW'
    if re.search(r'am_(?:anr|crash).*com\.android\.(?:systemui|launcher3|settings)',events): return 'SYSTEM_ANR_OR_CRASH_EVENT'
    if re.search(r'Process: com\.android\.(?:systemui|launcher3|settings)(?:,|\s)',crashes): return 'SYSTEM_FATAL_EXCEPTION'
    return None

def admit(properties):
    if not re.fullmatch(r'emulator-\d+',properties.get('serial','')) or properties.get('qemu') != '1':
        raise ValueError('PERSONAL_OR_UNKNOWN_DEVICE_REFUSED')
    if properties.get('api') not in (29,35) or 'x86_64' not in properties.get('abi',''):
        raise ValueError('UNQUALIFIED_API_OR_ABI')
    if properties.get('boot') != '1': raise ValueError('ANDROID_NOT_BOOTED')
    if not properties.get('memory_kib') or not properties.get('cpu_online'): raise ValueError('RESOURCES_NOT_OBSERVED')

def preflight(serial, api, output, adb=None, monotonic=time.monotonic, pause=time.sleep):
    out=Path(output);out.mkdir(parents=True,exist_ok=True)
    if not re.fullmatch(r'emulator-\d+',serial or ''): return {'status':'BLOCKED','kind':'EMULATOR','reason':'NO_AUTHORIZED_EMULATOR','app_tests':'NOT_RUN'}
    def real(*args):
        return subprocess.check_output(['adb','-s',serial,*args],stderr=subprocess.PIPE,timeout=20).decode('utf-8')
    call=adb or real
    report={'status':'BLOCKED','kind':'EMULATOR','serial':serial,'api':api,'app_tests':'NOT_RUN','jarvis_installed_by_lab':False,'samples':[]}
    try:
        props={'serial':serial,'qemu':call('shell','getprop','ro.kernel.qemu').strip(),
               'api':int(call('shell','getprop','ro.build.version.sdk').strip()),
               'abi':call('shell','getprop','ro.product.cpu.abilist').strip(),
               'boot':call('shell','getprop','sys.boot_completed').strip(),
               'memory_kib':call('shell','cat','/proc/meminfo').strip(),
               'cpu_online':call('shell','cat','/sys/devices/system/cpu/online').strip()}
        report['properties']=props;admit(props)
        if props['api']!=api: raise ValueError('REQUESTED_API_MISMATCH')
        for package in ['fr.jarvis.v1.lab','fr.jarvis.v1.lab.baseline']:
            # pm path can return 1 for an absent package; request with shell exit normalized,
            # while retaining exactly its stdout. No package is removed by this LAB.
            if call('shell','pm','list','packages',package).strip(): raise ValueError('FRESH_EMULATOR_REQUIRED')
        start=monotonic();pid=None
        for n in range(13):
            if monotonic()-start>120: raise ValueError('PREFLIGHT_WALL_BUDGET_EXCEEDED')
            values={name:call(*args) for name,args in {
                'window':('shell','dumpsys','window'), 'events':('logcat','-d','-b','events'),
                'crashes':('logcat','-d','-b','crash')}.items()}
            for key,value in values.items():(out/f'preflight-{n:02d}-{key}.txt').write_text(value)
            current=call('shell','pidof','com.android.systemui').strip()
            problem=incident(**values)
            if not current or (pid is not None and current!=pid):problem='SYSTEM_UI_PID_CHANGED_OR_MISSING'
            report['samples'].append({'sample':n,'elapsed_s':monotonic()-start,'systemui_pid':current,'incident':problem})
            if problem: raise ValueError(problem)
            pid=current
            if n<12:pause(5)
        report.update(status='PASS',observation_seconds=monotonic()-start,reason=None)
    except (OSError,subprocess.SubprocessError,ValueError) as e:report['reason']=str(e)
    (out/'preflight.json').write_text(json.dumps(report,indent=2)+'\n')
    return report

def qualify(source, row, apks, output, serial, api):
    output=Path(output);verify(source,row)
    result=preflight(serial,api,output/'android')
    if result['status']!='PASS':return result
    if not apks or apks.get('status')!='PASS':return {**result,'status':'BLOCKED','reason':'VERIFIED_APKS_REQUIRED'}
    # Reuse exact original campaign, its 18/24 assertions, package and airplane guards.
    source=Path(source);host=source/'build/m51-host';host.mkdir(parents=True,exist_ok=True)
    (host/'capability.json').write_text(json.dumps({'status':'OBSERVED_EXISTING_EMULATOR',
        'serial':serial,'protections_changed':False,'system_preflight':'PASS','source_commit':row['commit']})+'\n')
    size,density=('1080x1920','420') if api==29 else ('1200x1920','240')
    log=output/'logs/android-campaign.log'
    env={k:v for k,v in os.environ.items() if not any(x in k.upper() for x in ['TOKEN','SECRET','PASSWORD','CREDENTIAL'])}
    env['ANDROID_SERIAL']=serial;env['PYTHONDONTWRITEBYTECODE']='1'
    import sys
    run=execute([sys.executable,'m51/device_campaign.py','--delivery','build/m51-delivery','--output',str((output/'android/full').resolve()),'--api',str(api),'--size',size,'--density',density,'--profile','LAB-01-existing-authorized-emulator'],source,log,2100,env)
    run.update(kind='EMULATOR',log='logs/'+log.name,log_sha256=sha(log),preflight=result,physical='NOT_RUN')
    device=output/'android/full/device.json'
    if not device.is_file():return {**run,'status':'FAIL','reason':'ANDROID_RECEIPT_MISSING'}
    data=json.loads(device.read_text());run['device']=data
    if data.get('source_commit')!=row['commit'] or data.get('status')!='PASS_FUNCTIONAL_UI_BENCHMARKS_RECORDED':
        run.update(status='FAIL',reason='ANDROID_APPLICATION_CAMPAIGN_FAILED',critical=True)
    return run
