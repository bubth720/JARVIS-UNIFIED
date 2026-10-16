import copy
import io
import json
from pathlib import Path
import socket
import sys
import tempfile
import unittest
from unittest import mock
import urllib.error
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import audit_repos as a

ROOT=Path(__file__).resolve().parents[1]
class AuditTests(unittest.TestCase):
    def setUp(self):
        self.reg=a.legacy.read_json(ROOT/'registry/repositories.json');self.fixture=a.legacy.read_json(ROOT/'tests/fixtures/audit.json')
    def report(self):return a.run_audit(self.reg,self.fixture)
    def test_readme_only_is_not_runtime(self):
        item=self.report()['repositories'][4]
        self.assertEqual(item['files'],['README.md']);self.assertEqual(item['runtime_integration'],'not_demonstrated_by_audit')
    def test_main_behind_mission_and_ci_does_not_qualify_hardware(self):
        item=self.report()['repositories'][1]
        self.assertEqual(item['main_relation'],'not_included');self.assertEqual(item['ci']['status'],'success');self.assertEqual(item['hardware'],'not_checked')
    def test_http403_404_separate_from_absence(self):
        records=self.report()['repositories'];self.assertEqual(records[6]['retrieval'],'not_found_or_inaccessible');self.assertEqual(records[7]['retrieval'],'forbidden')
        self.assertTrue(all(r['evidence_state']=='retrieval_error' for r in records[6:8]))
    def test_rate_limit_and_timeout(self):
        for status,headers,expected in [(403,{'X-RateLimit-Remaining':'0'},'rate_limit'),(403,{},'forbidden'),(404,{},'not_found_or_inaccessible'),(429,{},'rate_limit')]:
            opener=mock.Mock();opener.open.side_effect=urllib.error.HTTPError('https://api.github.com/repos/bubth720/JARVIS-LLM',status,'mock',headers,None)
            with self.assertRaises(a.RetrievalError) as caught:a.Api(opener=opener).get('/repos/bubth720/JARVIS-LLM')
            self.assertEqual(caught.exception.reason,expected)
        opener.open.side_effect=urllib.error.URLError(socket.timeout())
        with self.assertRaises(a.RetrievalError) as caught:a.Api(opener=opener).get('/repos/bubth720/JARVIS-LLM')
        self.assertEqual(caught.exception.reason,'timeout')
    def test_duplicate_repositories_and_alias_not_unified(self):
        self.reg['repositories'][4]['name']=self.reg['repositories'][3]['name']
        with self.assertRaises(a.AuditError):a.validate_repositories(self.reg)
    def test_missing_sha_stale_and_unknown_timestamp(self):
        rec=self.fixture['records'][0];rec['commit']=None;self.assertEqual(self.report()['repositories'][0]['evidence_state'],'unknown_missing_sha')
        rec['commit']='a'*40;rec['captured_at']='2020-01-01T00:00:00Z';self.assertEqual(self.report()['repositories'][0]['evidence_state'],'stale')
        rec['captured_at']='not-a-time';self.assertEqual(self.report()['repositories'][0]['evidence_state'],'unknown_timestamp')
    def test_declaration_not_confirmed_source(self):
        self.fixture['records'][0]['proof_type']='declaration';self.assertEqual(self.report()['repositories'][0]['evidence_state'],'declaration')
    def test_sensitive_unexpected_field_never_published(self):
        self.fixture['records'][0]['unexpected']={'token':'synthetic-only'}
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'not-created'
            with self.assertRaises(a.AuditError):a.write_report(self.report(),out)
            self.assertFalse(out.exists())
    def test_hidden_credential_value_is_rejected(self):
        with self.assertRaises(a.AuditError):a.no_sensitive({'unexpected':'ghp_'+'X'*36})
    def test_changed_sha_between_captures(self):
        rec=self.fixture['records'][0];self.reg['repositories'][0]['observed_commit']=rec['commit']
        self.assertEqual(self.report()['repositories'][0]['ref_change']['state'],'unchanged')
        rec['commit']='f'*40;self.assertEqual(self.report()['repositories'][0]['ref_change']['state'],'changed')
    def test_offline_deterministic_and_network_forbidden(self):
        with mock.patch('urllib.request.OpenerDirector.open',side_effect=AssertionError('network')),mock.patch('os.environ.get',side_effect=AssertionError('credential')):
            self.assertEqual(a.legacy.dumps(self.report()),a.legacy.dumps(self.report()))
    def test_no_ci_is_unknown(self):
        rec=self.report()['repositories'][0];self.assertEqual(rec['ci']['status'],'unknown')
    def test_http_transport_only_get_and_no_auth_for_public_success(self):
        response=mock.MagicMock();response.__enter__.return_value=response;response.read.return_value=b'{"full_name":"bubth720/JARVIS-LLM"}'
        opener=mock.Mock();opener.open.return_value=response
        api=a.Api(opener=opener);api.get('/repos/bubth720/JARVIS-LLM')
        req=opener.open.call_args.args[0];self.assertEqual(req.get_method(),'GET');self.assertIsNone(req.get_header('Authorization'))
    def test_read_error_never_removes_repository(self):
        api=mock.Mock();api.get.side_effect=a.RetrievalError('proxy_forbidden');api.requests=[]
        report=a.run_audit(self.reg,api=api);self.assertEqual(len(report['repositories']),9);self.assertTrue(all(r['evidence_state']=='retrieval_error' for r in report['repositories']))
    def test_output_json_and_markdown(self):
        with tempfile.TemporaryDirectory() as d:
            a.write_report(self.report(),Path(d));self.assertEqual(len(json.loads((Path(d)/'audit.json').read_text())['repositories']),9);self.assertIn('synthetic_fixture',(Path(d)/'SUMMARY.md').read_text())

if __name__=='__main__':unittest.main()
