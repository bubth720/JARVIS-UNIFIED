"""Independent Gradle versions, selected pinned commands and original M51 APK verifier."""
import os, shutil, sys
from pathlib import Path
from . import policy, runner
from .integrity import verify, sha

def command(identifier, root):
    module = policy.command_owner(identifier)
    if identifier in policy.PYTHON:
        _, argv, kind, timeout = policy.PYTHON[identifier]
        return [sys.executable, *argv], kind, timeout
    if identifier == 'llm-native-helpers': return ['bash', 'perf03/tests/run.sh'], 'NATIVE', 180
    _, argv, kind, timeout, version = policy.GRADLE[identifier]
    configured = os.environ.get('LAB_GRADLE_'+version.replace('.', '_'))
    prefix = [configured] if configured else ['bash', 'gradlew']
    return [*prefix, *argv, '--rerun-tasks', '--no-daemon', '--max-workers=2', '--console=plain', '-Pkotlin.compiler.execution.strategy=in-process'], kind, timeout

def run(identifier, row, root, output, offline=False):
    verify(root, row)
    argv, kind, timeout = command(identifier, root)
    if offline and identifier in policy.GRADLE:
        version=policy.GRADLE[identifier][-1]
        if not os.environ.get('LAB_GRADLE_'+version.replace('.', '_')):
            raise ValueError('OFFLINE_GRADLE_TOOLCHAIN_REQUIRED:'+version)
        argv.append('--offline')
    env = {k: v for k, v in os.environ.items() if not any(t in k.upper() for t in ['TOKEN', 'SECRET', 'PASSWORD', 'CREDENTIAL'])}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    # JVM/SDK caches may be shared; source snapshots never are.
    jdk = os.environ.get('LAB_JAVA_HOME_21' if row['module'] == 'SERVICES' else 'LAB_JAVA_HOME_17')
    if jdk: env.update(JAVA_HOME=jdk, PATH=str(Path(jdk)/'bin')+os.pathsep+env.get('PATH',''))
    log = Path(output)/'logs'/(identifier+'.log')
    result = runner.execute(argv, root, log, timeout, env)
    result.update(id=identifier, module=row['module'], kind=kind, commit=row['commit'], tree=row['tree'],
                  log='logs/'+log.name, log_sha256=sha(log), physical='NOT_RUN')
    if identifier in policy.GRADLE:
        counts = runner.junit(root); result.update(counts)
        copied=[]
        for p in sorted(Path(root).glob('**/build/test-results/**/TEST-*.xml')):
            name=p.relative_to(root).as_posix();dest=Path(output)/'results'/identifier/name
            dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
            copied.append({'path':dest.relative_to(output).as_posix(),'sha256':sha(dest)})
        result['junit_evidence']=copied
        result['binary_inventory']=[{'source_relative_path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size}
                                    for p in sorted(Path(root).glob('**/build/libs/*.jar')) if p.is_file() and not p.is_symlink()]
        if result['status'] == 'PASS' and (not counts['test_invocations'] or counts['failures'] or counts['skipped']):
            result.update(status='FAIL', reason='MISSING_OR_FAILED_JUNIT')
        if result['status']=='FAIL':
            text=log.read_text(errors='replace')
            if 'UnknownHostException' in text:result['failure_phase']='ENVIRONMENT_DNS'
            elif 'Could not resolve' in text or 'could not resolve plugin artifact' in text:result['failure_phase']='DEPENDENCY_RESOLUTION'
    try: result['integrity_after'] = verify(root, row)
    except ValueError as e: result.update(status='FAIL', reason=str(e), critical=True)
    return result

def collect_apks(root, row, output):
    # This historical verifier checks testOnly, all permissions, native helper identities,
    # certificates, test results and absence of models/private media before staging.
    root = Path(root); log = Path(output)/'logs/m51-apk-verifier.log'
    result = runner.execute([sys.executable, 'm51/collect_build.py'], root, log, 120)
    result.update(kind='STATIC', log='logs/'+log.name, log_sha256=sha(log))
    if result['status'] != 'PASS': return result
    import json
    receipt = json.loads((root/'build/m51-delivery/build.json').read_text())
    if receipt['source_commit'] != row['commit'] or receipt['source_tree'] != row['tree']:
        raise ValueError('APK_BUILD_SOURCE_MISMATCH')
    target = Path(output)/'apks'; target.mkdir(exist_ok=True); artifacts = []
    for item in receipt['apks']:
        for name, digest in [(item['apk'],item['sha256']), (item['test_apk'],item['test_sha256'])]:
            p = root/'build/m51-delivery'/name
            if Path(name).name != name or p.is_symlink() or sha(p) != digest: raise ValueError('APK_DIGEST_MISMATCH')
            shutil.copyfile(p, target/name); artifacts.append({'path':'apks/'+name,'sha256':digest,'bytes':p.stat().st_size})
    for p in (root/'build/m51-delivery').iterdir():
        if p.suffix in {'.json', '.txt'}: shutil.copyfile(p, target/p.name)
    return {**result, 'artifacts':artifacts, 'receipt':receipt, 'qualification':'NOT_RUN', 'ready_to_install':False}
