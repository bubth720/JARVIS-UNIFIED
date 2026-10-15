"""Offline tests: fabricated API data, no writes to GitHub or other repositories."""
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.request
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import update_registry as r

ROOT = Path(__file__).resolve().parents[1]


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.modules = r.read_json(ROOT / 'modules.json')
        self.missions = r.read_json(ROOT / 'missions.json')
        self.client = r.Demo(ROOT / 'demo/github.json')

    def run_demo(self):
        return r.update(self.modules, self.missions, self.client, checked_at='2026-10-15T12:00:00+00:00', generation='1' * 32)

    def module(self, modules, name):
        return next(m for m in modules['modules'] if m['repository'] == 'bubth720/' + name)

    def test_read_valid_registry(self):
        self.assertTrue(r.validate(self.modules, self.missions))
        self.assertEqual(len(self.modules['modules']), 9)
        self.assertEqual(len(self.missions['missions']), 16)

    def test_inaccessible_repository_no_invention(self):
        modules, _ = self.run_demo()
        m = self.module(modules, 'JARVIS-SERVICES')
        self.assertEqual(m['state'], 'unknown')
        self.assertEqual(m['observation']['repository']['status'], 'failure')
        self.assertEqual(m['observation']['repository']['reason'], 'inaccessible_or_missing')
        self.assertEqual(m['observation']['ci']['status'], 'not_checked')

    def test_missing_branch_is_not_ci_failure(self):
        modules, _ = self.run_demo()
        m = self.module(modules, 'JARVIS-INTERFACE-')
        self.assertEqual(m['state'], 'failure')
        self.assertEqual(m['observation']['branch']['reason'], 'branch_not_found')
        self.assertEqual(m['observation']['ci']['status'], 'not_checked')

    def test_no_ci_results_is_unknown(self):
        modules, _ = self.run_demo()
        m = self.module(modules, 'JARVIS-NEXUS')
        self.assertEqual(m['observation']['ci']['status'], 'unknown')
        self.assertEqual(m['observation']['ci']['reason'], 'no_actions_runs_for_sha')
        self.assertEqual(m['observation']['ci']['runs'], [])

    def test_manual_blockers_decisions_and_unknown_fields_preserved(self):
        self.modules['modules'][0]['manual'].update(blockers=['Waiting for owner'], decisions=['Keep data'], extra_note={'nested': ['unchanged']})
        before_m, before_t = copy.deepcopy(self.modules), copy.deepcopy(self.missions)
        modules, missions = self.run_demo()
        for before, after in [(before_m['modules'], modules['modules']), (before_t['missions'], missions['missions'])]:
            self.assertEqual([e['manual'] for e in before], [e['manual'] for e in after])
        self.assertEqual(self.modules, before_m)
        self.assertEqual(self.missions, before_t)

    def test_repeated_update_no_duplicate_modules_missions_or_prs(self):
        modules, missions = self.run_demo()
        again_m, again_t = r.update(modules, missions, self.client, checked_at='2026-10-15T12:00:00+00:00', generation='1' * 32)
        self.assertEqual(modules, again_m); self.assertEqual(missions, again_t)
        self.assertEqual(len(again_m['modules']), 9)
        self.assertEqual(len({e['id'] for e in again_t['missions']}), len(again_t['missions']))

    def test_api_only_get_requests_and_no_remote_git_operations(self):
        # Full fake HTTP transport records every method, URL and header.
        fixture = self.client.responses
        requests = []
        class Response:
            def __init__(self, request, entry): self.request, self.entry = request, entry
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def geturl(self): return self.request.full_url
            def read(self, limit): return r.dumps(self.entry['body'])[:limit]
        class Opener:
            def open(self, request, timeout):
                requests.append(request)
                path = request.full_url.removeprefix(r.API)
                entry = fixture[path]
                if entry['http_status'] != 200:
                    raise urllib.error.HTTPError(request.full_url, entry['http_status'], 'synthetic', {}, io.BytesIO())
                return Response(request, entry)
        with mock.patch.object(subprocess, 'run', side_effect=AssertionError('No Git command permitted in API mode')):
            r.update(self.modules, self.missions, r.GitHub(opener=Opener()))
        self.assertTrue(requests)
        self.assertEqual({req.get_method() for req in requests}, {'GET'})
        self.assertTrue(all(req.full_url.startswith('https://api.github.com/repos/bubth720/') for req in requests))
        self.assertTrue(all(req.get_header('Authorization') is None for req in requests))

    def test_git_mode_uses_only_ls_remote(self):
        calls = []
        def command(args, **kwargs):
            calls.append(args)
            return subprocess.CompletedProcess(args, 0, 'ref: refs/heads/main\tHEAD\n' + 'a' * 40 + '\trefs/heads/main\n', '')
        with mock.patch.object(subprocess, 'run', side_effect=command):
            client = r.GitRefs()
            client.observe('bubth720/JARVIS-NEXUS', 'main')
            client.observe('bubth720/JARVIS-NEXUS', 'missing')
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], ['git', '-c', 'credential.interactive=false', 'ls-remote', '--symref', 'https://github.com/bubth720/JARVIS-NEXUS.git', 'HEAD', 'refs/heads/*'])

    def test_pending_failure_unknown_and_sha_filter(self):
        sha = 'a' * 40
        def run(id, status, conclusion, head=sha, workflow=1):
            return dict(id=id, head_sha=head, workflow_id=workflow, event='push', run_number=id, run_attempt=1, status=status, conclusion=conclusion)
        self.assertEqual(r.action_summary([run(1, 'completed', 'success')], sha)['status'], 'success')
        self.assertEqual(r.action_summary([run(1, 'in_progress', None)], sha)['status'], 'pending')
        self.assertEqual(r.action_summary([run(1, 'completed', 'success'), run(2, 'completed', 'failure')], sha)['status'], 'failure')
        self.assertEqual(r.action_summary([run(1, 'completed', 'skipped')], sha)['status'], 'unknown')
        self.assertEqual(r.action_summary([run(1, 'completed', 'success', head='b' * 40)], sha)['status'], 'unknown')
        self.assertIsNone(r.action_summary([], sha)['tests_count'])

    def test_api_failures_preserve_historical_commit_and_date(self):
        entry = self.module(self.modules, 'JARVIS-SERVICES')
        old = copy.deepcopy(entry['last_verified_commit'])
        self.assertIsNotNone(old)
        modules, _ = self.run_demo()
        after = self.module(modules, 'JARVIS-SERVICES')
        self.assertEqual(after['last_verified_commit'], old)
        self.assertEqual(after['verified_at'], entry['verified_at'])
        self.assertNotEqual(after['checked_at'], old['verified_at'])

    def test_demo_no_network_no_git_no_secret_read(self):
        with mock.patch.object(urllib.request.OpenerDirector, 'open', side_effect=AssertionError('Network forbidden')), mock.patch.object(subprocess, 'run', side_effect=AssertionError('Git forbidden')), mock.patch.object(os.environ, 'get', side_effect=AssertionError('Secret read forbidden')):
            modules, _ = self.run_demo()
        self.assertEqual(modules['modules'][0]['observation']['source'], 'demo')

    def test_duplicate_ids_and_confusing_repository_names_refused(self):
        self.missions['missions'].append(copy.deepcopy(self.missions['missions'][0]))
        with self.assertRaises(r.RegistryError): r.validate(self.modules, self.missions)
        self.missions['missions'].pop()
        self.modules['modules'][4]['repository'] = 'bubth720/JARVIS-INTERFACE'
        with self.assertRaises(r.RegistryError): r.validate(self.modules, self.missions)

    def test_duplicate_prs_deduplicated_and_head_identity_filtered(self):
        repo = 'bubth720/JARVIS-NEXUS'
        endpoint = '/repos/' + repo + '/pulls?state=all&head=bubth720%3Amain&per_page=100&page=1'
        pull = {'number': 7, 'state': 'open', 'draft': True, 'merged_at': None,
                'head': {'ref': 'main', 'sha': 'a' * 40, 'repo': {'full_name': repo}},
                'base': {'ref': 'main'}, 'html_url': 'https://github.com/' + repo + '/pull/7'}
        wrong = copy.deepcopy(pull); wrong['number'] = 8; wrong['head']['repo']['full_name'] = 'different/repo'
        self.client.responses[endpoint]['body'] = [pull, pull, wrong]
        modules, _ = self.run_demo()
        records = self.module(modules, 'JARVIS-NEXUS')['observation']['pull_requests']['items']
        self.assertEqual([p['number'] for p in records], [7])

    def test_missing_ci_endpoint_does_not_become_success(self):
        repo = 'bubth720/JARVIS-NEXUS'
        prefix = '/repos/' + repo + '/actions/runs?'
        self.client.responses = {p: v for p, v in self.client.responses.items() if not p.startswith(prefix)}
        modules, _ = self.run_demo()
        ci = self.module(modules, 'JARVIS-NEXUS')['observation']['ci']
        self.assertEqual(ci['status'], 'unknown')
        self.assertEqual(ci['reason'], 'demo_endpoint_not_provided')

    def test_mixed_generation_refused(self):
        self.missions['generation'] = 'other'
        with self.assertRaises(r.RegistryError): r.validate(self.modules, self.missions)

    def test_local_snapshots_traceable_and_manual_preserved(self):
        modules, missions = self.run_demo()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snapshot = r.publish_local(root, modules, missions, self.client.evidence)
            self.assertEqual(r.read_json(root/'modules.json'), modules)
            self.assertEqual(r.read_json(snapshot/'missions.json'), missions)
            self.assertIn('observations', r.read_json(snapshot/'evidence.json'))
            self.assertTrue((root/'SUMMARY.md').is_file())
            self.assertFalse((root/'.update.lock').exists())

    def test_demo_requires_separate_output_and_leaves_registry_unchanged(self):
        before = (ROOT/'modules.json').read_bytes()
        with mock.patch('sys.stderr', new_callable=io.StringIO):
            self.assertEqual(r.main(['--registry-dir', str(ROOT), '--mode', 'demo']), 1)
        self.assertEqual(before, (ROOT/'modules.json').read_bytes())

    def test_redirect_rejected_even_to_github(self):
        req = urllib.request.Request(r.API+'/repos/bubth720/JARVIS-UNIFIED')
        with self.assertRaises(r.ReadError):
            r.NoRedirect().redirect_request(req, None, 302, '', {}, 'https://example.invalid/')

    def test_token_only_after_anonymous_denial_and_never_in_evidence(self):
        secret = uuid.uuid4().hex
        paths, headers = [], []
        def transport(path, token=None):
            paths.append(path); headers.append(token)
            if token is None: raise r.ReadError('http_401', 401)
            return {'ok': True}
        client = r.GitHub('GH_TOKEN')
        with mock.patch.dict(os.environ, {'GH_TOKEN': secret}), mock.patch.object(client, '_read', side_effect=transport):
            client.get('/repos/bubth720/JARVIS-NEXUS')
        self.assertEqual(headers, [None, secret])
        self.assertNotIn(secret, json.dumps(client.evidence))
        self.assertNotIn(secret, json.dumps(client.cache))
        client = r.GitHub('GH_TOKEN')
        with mock.patch.dict(os.environ, {'GH_TOKEN': secret}), mock.patch.object(client, '_read', return_value={'ok': True}) as read:
            client.get('/repos/bubth720/JARVIS-NEXUS')
            read.assert_called_once_with('/repos/bubth720/JARVIS-NEXUS')

    def test_proxy_failure_does_not_trigger_token_retry(self):
        client = r.GitHub('GH_TOKEN')
        with mock.patch.object(os.environ, 'get', side_effect=AssertionError('No token read')), mock.patch.object(client, '_read', side_effect=r.ReadError('network_unavailable')) as read:
            with self.assertRaises(r.ReadError): client.get('/repos/bubth720/JARVIS-NEXUS')
        self.assertEqual(read.call_count, 1)

    def test_markdown_escapes_manual_content(self):
        self.modules['modules'][0]['manual']['phase'] = 'blocked'
        self.missions['missions'][0]['manual']['blockers'] = ['<script>|bad\nrow']
        modules, missions = self.run_demo()
        report = r.summary(modules, missions)
        self.assertNotIn('<script>', report)
        self.assertIn('&lt;script&gt;&#124;bad row', report)

    def test_pagination_limit_is_unknown_not_partial_green(self):
        client = r.GitHub()
        with mock.patch.object(client, 'get', return_value=[{}] * 100):
            with self.assertRaises(r.ReadError) as error: client.pages('/repos/bubth720/JARVIS-NEXUS/pulls?state=all')
        self.assertEqual(error.exception.reason, 'pagination_limit')

    def test_branch_with_slash_encoded_exactly(self):
        modules, _ = self.run_demo()
        self.assertEqual(self.module(modules, 'JARVIS-INTERFACE')['observation']['branch']['status'], 'success')
        paths = [e['url'] for e in self.client.evidence]
        self.assertTrue(any('/branches/development%2Fmission-002' in path for path in paths))


if __name__ == '__main__': unittest.main()
