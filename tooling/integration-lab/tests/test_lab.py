"""Laboratory safety fixtures. These are not Android or model qualification."""
import copy,hashlib,importlib.util,json,os,signal,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[1];ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE));sys.path.insert(0,str(ROOT))
from core import repository,integrity,policy,runner,android,evidence,reporting,campaign,dependencies,contracts,builder

class LockTests(unittest.TestCase):
    def setUp(self):self.value=repository.read_lock(HERE/'config/modules.lock.json')
    def load(self,value,bad_digest=False):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'modules.lock.json';p.write_text(json.dumps(value));p.with_suffix('.sha256').write_text('0'*64 if bad_digest else integrity.sha(p))
            return repository.read_lock(p)
    def test_eight_exact_modules(self):self.assertEqual(set(policy.MODULES),{r['module'] for r in self.value['modules']})
    def test_invalid_commit(self):
        self.value['modules'][0]['commit']='5da98383'
        with self.assertRaisesRegex(ValueError,'FULL_SHA'):self.load(self.value)
    def test_wrong_lock_fingerprint(self):
        with self.assertRaisesRegex(ValueError,'DIGEST'):self.load(self.value,True)
    def test_unknown_or_external_repository(self):
        self.value['modules'][0]['repository']='other/private'
        with self.assertRaisesRegex(ValueError,'UNKNOWN_REPOSITORY'):self.load(self.value)
    def test_disabled_module_never_silently_activated(self):
        self.value['modules'][0]['runtime_enabled']=True
        with self.assertRaisesRegex(ValueError,'ACTIVATION'):self.load(self.value)
    def test_duplicate_and_missing_modules(self):
        self.value['modules'][-1]=copy.deepcopy(self.value['modules'][0])
        with self.assertRaisesRegex(ValueError,'EIGHT'):self.load(self.value)
    def test_untrusted_command_refused(self):
        for name in ['curl https://x','sudo','download-model','llm-admit','']:
            with self.assertRaisesRegex(ValueError,'UNAPPROVED'):policy.command_owner(name)
    def test_no_runtime_authority_from_lab(self):
        self.assertEqual(['INTERFACE_LOCAL_ONLY'],policy.runtime_selection(['INTERFACE_LOCAL_ONLY']))
        for names in [[],['LLM'],['CORE','INTERFACE_LOCAL_ONLY']]:
            with self.assertRaises(ValueError):policy.runtime_selection(names)
    def test_failure_not_successful_aggregate(self):
        self.assertEqual('FAIL',policy.aggregate(['PASS','FAIL','BLOCKED']))
        self.assertEqual('BLOCKED',policy.aggregate(['PASS','BLOCKED']))
    def test_path_escape(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):policy.child(d,'../private')

class GitTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        subprocess.run(['git','init','-q',str(self.root)],check=True)
        (self.root/'protected.txt').write_text('historical fixture\n')
        subprocess.run(['git','-C',str(self.root),'add','.'],check=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=LAB fixture','-c','user.email=lab@example.invalid','commit','-qm','fixture'],check=True)
        self.row={'commit':integrity.git(self.root,'rev-parse','HEAD').decode().strip(),'tree':integrity.git(self.root,'rev-parse','HEAD^{tree}').decode().strip()}
    def tearDown(self):self.temp.cleanup()
    def test_valid_commit_and_tree(self):self.assertEqual('PASS',integrity.verify(self.root,self.row)['status'])
    def test_missing_commit_is_refused(self):
        self.row['commit']='0'*40
        with self.assertRaisesRegex(ValueError,'COMMIT'):integrity.verify(self.root,self.row)
    def test_wrong_tree(self):
        self.row['tree']='0'*40
        with self.assertRaisesRegex(ValueError,'TREE'):integrity.verify(self.root,self.row)
    def test_protected_bytes_modified(self):
        (self.root/'protected.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError,'DRIFT'):integrity.verify(self.root,self.row)
    def test_malicious_index_does_not_hide_protected_change(self):
        (self.root/'protected.txt').write_text('changed');subprocess.run(['git','-C',str(self.root),'add','.'],check=True)
        with self.assertRaisesRegex(ValueError,'DRIFT'):integrity.verify(self.root,self.row)
    def test_protected_fingerprint_wrong(self):
        self.row['protected']={'protected.txt':'0'*64}
        with self.assertRaisesRegex(ValueError,'PREIMAGE'):integrity.verify(self.root,self.row)
    def test_symlink_refused(self):
        (self.root/'protected.txt').unlink();(self.root/'protected.txt').symlink_to('/etc/passwd')
        with self.assertRaisesRegex(ValueError,'UNSAFE'):integrity.verify(self.root,self.row)
    def test_repository_offline_unavailable(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaisesRegex(FileNotFoundError,'OFFLINE_SOURCE'):repository.acquire({'module':'CORE'},d,True)
    def test_nonisolated_existing_checkout_refused(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'CORE').mkdir()
            with self.assertRaisesRegex(ValueError,'ISOLATED'):repository.acquire({'module':'CORE'},d,True)

class ExecutionTests(unittest.TestCase):
    def call(self,code,timeout=2,max_bytes=1024*1024):
        with tempfile.TemporaryDirectory() as d:
            return runner.execute([sys.executable,'-c',code],d,Path(d)/'test.log',timeout,max_bytes=max_bytes)
    def test_successful_real_process(self):self.assertEqual('PASS',self.call('print("ok")')['status'])
    def test_failed_real_process(self):
        r=self.call('raise SystemExit(7)');self.assertEqual(('FAIL',7),(r['status'],r['exit_code']))
    def test_process_interrupted(self):
        r=self.call('import os,signal;os.kill(os.getpid(),signal.SIGTERM)');self.assertEqual('PROCESS_SIGNAL',r['reason'])
    def test_timeout(self):self.assertEqual('TIMEOUT',self.call('import time;time.sleep(10)',.1)['reason'])
    def test_truncated_output_is_failure(self):
        r=self.call('print("x"*100000)',max_bytes=1024);self.assertEqual(('FAIL',True),(r['status'],r['truncated']))
    def test_zero_tests_not_success(self):self.assertEqual('FAIL',self.call('print("Ran 0 tests in 0.000s\\n\\nOK")')['status'])
    def test_missing_executable_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            r=runner.execute(['/nonexistent/lab-tool'],d,Path(d)/'missing.log',1);self.assertEqual('BLOCKED',r['status'])
    def test_gradle_versions_not_globally_replaced(self):
        with patch.dict(os.environ,{'LAB_GRADLE_8_10_2':'/tool/g810','LAB_GRADLE_8_13':'/tool/g813'}):
            self.assertEqual('/tool/g810',builder.command('nexus-jvm',Path('.'))[0][0])
            self.assertEqual('/tool/g813',builder.command('interface-m51',Path('.'))[0][0])

class AndroidTests(unittest.TestCase):
    def props(self):return {'serial':'emulator-5554','qemu':'1','api':29,'abi':'x86_64','boot':'1','memory_kib':'MemTotal: 2048000 kB','cpu_online':'0-1'}
    def test_physicals_and_unknown_devices_refused(self):
        for serial in ['POCO','Redmi','192.168.1.1:5555','']:
            p=self.props();p['serial']=serial
            with self.assertRaisesRegex(ValueError,'DEVICE_REFUSED'):android.admit(p)
    def test_no_device_does_not_call_adb(self):
        with tempfile.TemporaryDirectory() as d:
            fake=unittest.mock.Mock();r=android.preflight('',29,d,adb=fake);fake.assert_not_called();self.assertEqual('BLOCKED',r['status'])
    def test_unbooted_android_refused(self):
        p=self.props();p['boot']='0'
        with self.assertRaisesRegex(ValueError,'NOT_BOOTED'):android.admit(p)
    def test_wrong_api_and_abi_refused(self):
        for key,value in [('api',24),('abi','arm64-v8a')]:
            p=self.props();p[key]=value
            with self.assertRaisesRegex(ValueError,'API_OR_ABI'):android.admit(p)
    def test_real_m51_r1_crash_signature_blocks_environment(self):
        self.assertEqual('SYSTEM_ANR_OR_CRASH_EVENT',android.incident('','I am_crash: [2104,0,com.android.systemui,818429453,java.util.ConcurrentModificationException,NULL,HashMap.java,1441]',''))
    def test_systemui_anr_and_fatal(self):
        self.assertIsNotNone(android.incident('Application Not Responding: com.android.systemui','',''))
        self.assertIsNotNone(android.incident('','','Process: com.android.systemui, PID: 2'))
    def fake_adb(self,crash=False):
        def f(*args):
            if args==('shell','getprop','ro.kernel.qemu'):return '1'
            if args==('shell','getprop','ro.build.version.sdk'):return '29'
            if args==('shell','getprop','ro.product.cpu.abilist'):return 'x86_64'
            if args==('shell','getprop','sys.boot_completed'):return '1'
            if args[:2]==('shell','cat'):return 'observed'
            if args[:4]==('shell','pm','list','packages'):return ''
            if args==('shell','pidof','com.android.systemui'):return '7'
            if args==('logcat','-d','-b','events') and crash:return 'am_crash: [2,0,com.android.systemui,0]'
            return ''
        return f
    def test_stable_fixture_can_be_admitted_but_not_qualified(self):
        clock=[0.0]
        def pause(n):clock[0]+=n
        with tempfile.TemporaryDirectory() as d:
            r=android.preflight('emulator-5554',29,d,adb=self.fake_adb(),monotonic=lambda:clock[0],pause=pause)
            self.assertEqual('PASS',r['status']);self.assertEqual(13,len(r['samples']));self.assertEqual('NOT_RUN',r['app_tests'])
    def test_critical_system_crash_stops_at_first_sample(self):
        with tempfile.TemporaryDirectory() as d:
            r=android.preflight('emulator-5554',29,d,adb=self.fake_adb(True),pause=lambda n:None)
            self.assertEqual('BLOCKED',r['status']);self.assertEqual(1,len(r['samples']));self.assertFalse(r['jarvis_installed_by_lab'])

class EvidenceTests(unittest.TestCase):
    def receipt(self):
        return {'id':'fixture-campaign','profile':'safe','status':'FAIL','lab_commit':'a'*40,'lab_tree':'b'*40,'modules':[],
                'commands':[{'id':'fixture','module':'NEXUS','kind':'UNIT','status':'FAIL','reason':'fixture assertion'}],'android':{'status':'NOT_RUN'},'apks':{'status':'NOT_RUN'}}
    def test_report_and_dashboard_regenerated_from_same_receipt(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            reporting.render(self.receipt(),a);reporting.render(self.receipt(),b)
            for n in ['report.json','REPORT.md','dashboard.html']:self.assertEqual((Path(a)/n).read_bytes(),(Path(b)/n).read_bytes())
    def test_html_escaping_and_no_network_dependency(self):
        r=self.receipt();r['id']='</script><img src="https://invalid/x">'
        with tempfile.TemporaryDirectory() as d:
            reporting.render(r,d);s=(Path(d)/'dashboard.html').read_text();self.assertNotIn('<img src=',s);self.assertNotIn('fetch(',s);self.assertIn("script-src 'none'",s)
    def test_export_and_verify(self):
        with tempfile.TemporaryDirectory() as d:
            reporting.render(self.receipt(),d);r=evidence.export(d);self.assertEqual('PASS',evidence.verify_archive(Path(d)/r['path'])['status'])
    def test_corrupted_archive_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            reporting.render(self.receipt(),d);evidence.export(d);p=Path(d)/'corrupt.zip'
            with zipfile.ZipFile(Path(d)/'evidence.zip') as src,zipfile.ZipFile(p,'w') as z:
                for name in src.namelist():z.writestr(name,b'changed' if name=='REPORT.md' else src.read(name))
            with self.assertRaisesRegex(ValueError,'DIGEST'):evidence.verify_archive(p)
    def test_missing_archive_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):evidence.verify_archive(Path(d)/'absent.zip')
    def test_untrusted_metadata_path_refused(self):
        for name in ['../secret.txt','/etc/passwd','apks/other.apk','x.gguf','x.key','sources/key.json','a\\b.json']:self.assertFalse(evidence.allowed(name),name)
    def test_private_payload_export_refused(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'fixture.gguf').write_bytes(b'GGUF')
            with self.assertRaisesRegex(ValueError,'UNAUTHORIZED_EXPORT'):evidence.export(d)
    def test_interrupted_campaign_recovers_without_retry(self):
        with tempfile.TemporaryDirectory() as d:
            r=self.receipt();r.update(status='RUNNING',lab_commit=campaign.identity()['lab_commit'],lock_sha256=integrity.sha(HERE/'config/modules.lock.json'),commands=[])
            evidence.write(Path(d)/'campaign.json',r)
            with patch.object(builder,'run') as run:
                after=campaign.recover(d);run.assert_not_called();self.assertEqual('UNKNOWN',after['status'])
    def test_comparison_does_not_invent_speedup(self):
        a=self.receipt();b=self.receipt();r=reporting.compare(a,b);self.assertFalse(r['performance_comparable']);self.assertIsNone(r['performance_delta'])
    def test_unexecuted_regression_is_not_cleared_by_inventory_pass(self):
        a=self.receipt();a['modules']=[{'module':'NEXUS','commit':'a'*40,'status':'FAIL'}]
        b=copy.deepcopy(a);b['commands']=[];b['modules'][0]['status']='PASS'
        r=reporting.compare(a,b)['modules'][0]
        self.assertEqual('NOT_RUN',r['after_status']);self.assertEqual(['fixture'],r['prior_failures_not_reexecuted'])
        self.assertFalse(r['coverage_comparable']);self.assertEqual('OPTIMISER',r['recommendation'])
    def test_unknown_dependency_is_not_compatible(self):
        r=dependencies.compare({'facts':{}},{'facts':{}});self.assertEqual('UNKNOWN',r['status'])
    def test_incompatible_toolchain(self):
        r=dependencies.compare({'facts':{'gradle':['8.10.2']}},{'facts':{'gradle':['8.13']}});self.assertEqual('INCOMPATIBLE',r['status'])
    def test_historical_contracts_checked_without_runtime_activation(self):
        r=contracts.inspect({'UNIFIED':ROOT});self.assertEqual(5,len(r['schema_tests']));self.assertFalse(r['runtime_integration_proven'])

if __name__=='__main__':unittest.main()
