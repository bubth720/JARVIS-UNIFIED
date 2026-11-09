"""LAB-02 read-only triage tests: synthetic receipts, never product qualification."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'triage.py'
spec = importlib.util.spec_from_file_location('lab02_triage', SCRIPT)
triage_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triage_mod)

class TriageTests(unittest.TestCase):
    def receipt(self):
        return {
            'schema': 'jarvis.integration-lab.delivery/1', 'campaign_status': 'FAIL',
            'runtime_integration_proven': False, 'android_safe': {'status': 'NOT_RUN', 'reason': 'SAFE_PROFILE'},
            'commands': [
                {'module': 'LLM', 'id': 'llm-manifest-guard', 'status': 'FAIL', 'kind': 'STATIC', 'commit': 'a'*40},
                {'module': 'VOICE', 'id': 'voice-jvm', 'status': 'FAIL', 'skipped': 1, 'failures': 0},
                {'module': 'NEXUS', 'id': 'nexus-jvm', 'status': 'PASS'}]}

    def result(self, **changes):
        data = self.receipt();data.update(changes)
        return triage_mod.triage(data, 'f'*64)

    def test_realistic_blockers_are_not_cleared(self):
        r = self.result()
        self.assertEqual('ACTION_REQUIRED', r['status'])
        self.assertEqual(4, r['finding_count'])
        self.assertEqual({'HISTORICAL_GUARD', 'RESOURCE_QUALIFICATION', 'ANDROID_NOT_QUALIFIED', 'INTEGRATION_UNPROVEN'}, {f['classification'] for f in r['findings']})
        self.assertFalse(r['runtime_authority_granted'])
        self.assertFalse(r['product_qualified'])

    def test_all_green_is_not_product_go(self):
        r = self.result(commands=[{'module': 'NEXUS', 'id': 'nexus-jvm', 'status': 'PASS'}], android_safe={'status': 'PASS'}, runtime_integration_proven=True)
        self.assertEqual('NO_RECORDED_BLOCKER_NOT_A_GO', r['status'])
        self.assertEqual(0, r['finding_count'])
        self.assertFalse(r['product_qualified'])

    def test_unknown_step_not_hidden(self):
        r = self.result(commands=[{'module': 'NEXUS', 'id': 'new-readonly-test', 'status': 'UNKNOWN'}])
        self.assertEqual('UNKNOWN_EXECUTION', next(f['classification'] for f in r['findings'] if f['module'] == 'NEXUS'))

    def test_duplicate_command_rejected(self):
        d = self.receipt();d['commands'] *= 2
        with self.assertRaisesRegex(ValueError, 'DUPLICATE_COMMAND'): triage_mod.triage(d, 'f'*64)

    def test_malformed_receipt_rejected(self):
        for item in [None, {}, {'commands': 'no'}, {'commands': [{'module': 'LLM', 'id': 'oops', 'status': 'GREEN'}]}, {'commands': [{'module': 'OTHER', 'id': 'bad', 'status': 'PASS'}]}]:
            with self.assertRaises(ValueError):triage_mod.triage(item, 'f'*64)

    def test_log_verified_and_detects_tampering(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'log.txt';p.write_text('correct')
            item={'log': 'log.txt', 'log_sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
            self.assertEqual('VERIFIED', triage_mod._evidence(item, d)['status'])
            p.write_text('changed')
            self.assertEqual('MISMATCH', triage_mod._evidence(item, d)['status'])

    def test_path_traversal_and_symlink_refused(self):
        with tempfile.TemporaryDirectory() as d:
            item={'log':'../private.txt', 'log_sha256':'a'*64}
            self.assertEqual('INVALID', triage_mod._evidence(item,d)['status'])
            (Path(d)/'link.txt').symlink_to('/etc/passwd')
            item['log']='link.txt'
            self.assertEqual('INVALID', triage_mod._evidence(item,d)['status'])

    def test_no_false_log_verification(self):
        self.assertEqual('NOT_CHECKED', triage_mod._evidence({'log':'log.txt','log_sha256':'a'*64},None)['status'])

    def test_markdown_escapes_table_controls(self):
        r = self.result(commands=[{'module':'NEXUS','id':'search','status':'FAIL','reason':'<script>|some-text'}])
        md = triage_mod.markdown(r)
        self.assertNotIn('<script>',md)
        self.assertIn('\\|', md)
        self.assertIn('No module is granted GO',md)

    def test_output_deterministic(self):
        r = self.result()
        self.assertEqual(triage_mod.markdown(r),triage_mod.markdown(r))
        self.assertEqual(json.dumps(r,sort_keys=True),json.dumps(self.result(),sort_keys=True))

    def test_cli_writes_two_files_without_mutating_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            inp=Path(d)/'receipt.json';inp.write_text(json.dumps(self.receipt()))
            before=inp.read_bytes()
            target=Path(d)/'output'
            self.assertEqual(0,triage_mod.main(['--receipt',str(inp),'--output',str(target)]))
            self.assertEqual(before,inp.read_bytes())
            self.assertTrue((target/'TRIAGE.json').exists())
            self.assertTrue((target/'TRIAGE.md').exists())

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            inp=Path(d)/'receipt.json';inp.write_text(json.dumps(self.receipt()))
            target=Path(d)/'output';target.mkdir();(target/'protected.txt').write_text('keep')
            with self.assertRaisesRegex(ValueError,'NONEMPTY_OUTPUT_DIRECTORY'):
                triage_mod.main(['--receipt',str(inp),'--output',str(target)])
            self.assertEqual('keep',(target/'protected.txt').read_text())

if __name__ == '__main__':unittest.main()
