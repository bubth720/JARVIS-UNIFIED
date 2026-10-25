import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tooling.integration.lock import (ROOT, LockError, load, validate, verify_sources,
                                      waves, plan, compare, markdown)
from tooling.integration.cli import main


class LockTests(unittest.TestCase):
    def setUp(self):
        self.lock = load(ROOT / 'integration-lock.json')

    def rejected(self, value):
        with self.assertRaises(ValueError): validate(value)

    def test_complete_candidate_validates_without_granting_runtime(self):
        self.assertEqual(validate(self.lock)['composition'], 'CANDIDATE_NOT_INTEGRATED')
        self.assertEqual([g['id'] for g in plan(self.lock) if g['status'] == 'VERIFIED'], ['F0'])

    def test_duplicate_repository_identity_or_owner_rejected(self):
        self.lock['components'][0]['repository'] = 'bubth720/JARVIS-LLM'
        self.rejected(self.lock)

    def test_duplicate_component_cannot_hide_missing_one(self):
        self.lock['components'][-1] = copy.deepcopy(self.lock['components'][0])
        self.rejected(self.lock)

    def test_branch_commit_and_evidence_path_admission(self):
        for kind, bad in [('branch', 'feat/../../main'), ('commit', '374ea2e')]:
            x = copy.deepcopy(self.lock); x['components'][0]['primary'][kind] = bad
            self.rejected(x)
        for path in ['../private', '/tmp/private', 'a//b', 'a/./b', 'a\\b', 'a:b']:
            x = copy.deepcopy(self.lock);x['components'][0]['primary']['files'][0]['path'] = path
            self.rejected(x)

    def test_ci_cannot_inherit_another_commit_or_repository_success(self):
        c = self.lock['components'][0]
        c['ci'].update(status='success', commit='a'*40,
                       url='https://github.com/'+c['repository']+'/actions/runs/1')
        self.rejected(self.lock)
        c['ci']['commit'] = c['primary']['commit']
        c['ci']['url'] = 'https://github.com/bubth720/JARVIS-LLM/actions/runs/1'
        self.rejected(self.lock)

    def test_unknown_ci_remains_unknown_in_report(self):
        self.assertIn('| unknown |', markdown(self.lock))
        self.assertIn('candidate', markdown(self.lock))

    def test_no_go_with_unresolved_conflicts_or_missing_dependencies(self):
        for phase in ['F1', 'F2', 'F3', 'F8']:
            x=copy.deepcopy(self.lock)
            g=next(g for g in x['gates'] if g['id']==phase)
            g['status']='VERIFIED';g['blockers']=[]
            self.rejected(x)

    def test_missing_f0_unknown_dependency_and_cycles_refused(self):
        for deps in [[], ['F9'], ['F8']]:
            x=copy.deepcopy(self.lock);x['gates'][1]['depends_on']=deps
            self.rejected(x)

    def test_boolean_not_integer_and_unknown_field_refused(self):
        x=copy.deepcopy(self.lock);x['components'][0]['primary']['files'][0]['sha256']=True
        self.rejected(x)
        self.lock['activate_native']=True;self.rejected(self.lock)

    def test_duplicate_json_nonfinite_and_huge_file_refused(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'input.json'
            for s in ['{"x":1,"x":2}', '{"x":NaN}', '{"x":"\\ud800"}', ' '* (2*1024*1024+1)]:
                p.write_text(s)
                with self.assertRaises(ValueError): load(p)

    def test_exact_platform_inventory_required(self):
        self.lock['components'][0]['platforms'][-1] = copy.deepcopy(self.lock['components'][0]['platforms'][0])
        self.rejected(self.lock)

    def test_compare_no_duplicate_or_implicit_mutation(self):
        before=copy.deepcopy(self.lock)
        self.assertEqual(compare(before,self.lock),[])
        c=self.lock['components'][0];c['ci']['reason']='Fresh observation differs, no inferred success.'
        self.assertEqual(len(compare(before,self.lock)),1)
        self.assertEqual(before,load(ROOT/'integration-lock.json'))

    def test_blockers_are_preserved_in_plan_and_markdown(self):
        p=plan(self.lock)
        f2=next(g for g in p if g['id']=='F2')
        self.assertEqual(f2['waiting_for'],['F1'])
        self.assertIn('FTS5',markdown(self.lock))
        self.assertEqual(next(g for g in p if g['id']=='F3')['status'],'BLOCKED')

    def test_independent_jvm_gate_does_not_depend_on_native_voice_or_llm(self):
        # Synthetic policy-only scenario, never a claim that F1 actually ran.
        self.lock['conflicts']=[c for c in self.lock['conflicts'] if 'F1' not in c['blocks']]
        for c in self.lock['components']:
            if c['id'] in {'core','nexus','services'}:
                c['ci']={'status':'success','commit':c['primary']['commit'],
                         'url':'https://github.com/'+c['repository']+'/actions/runs/1',
                         'reason':'Synthetic test observation only.'}
        phase=next(g for g in self.lock['gates'] if g['id']=='F1')
        phase['status']='VERIFIED';phase['blockers']=[]
        self.assertEqual(validate(self.lock)['gates'][1]['status'],'VERIFIED')
        self.assertEqual(next(g for g in self.lock['gates'] if g['id']=='F3')['status'],'BLOCKED')

    def test_only_readonly_git_objects_are_used(self):
        with tempfile.TemporaryDirectory() as d:
            repo=Path(d)/'repo';repo.mkdir()
            def git(*a):return subprocess.check_output(['git','-C',str(repo),*a],stderr=subprocess.DEVNULL).decode().strip()
            git('init','-q');git('config','user.name','Synthetic test');git('config','user.email','synthetic@example.invalid')
            (repo/'evidence.md').write_text('Synthetic tracked evidence only.\n')
            git('add','evidence.md');git('commit','-qm','fixture')
            sha=git('rev-parse','HEAD');before=git('show-ref')
            x=copy.deepcopy(self.lock)
            for c in x['components']:
                c['primary']={'branch':'fixture','commit':sha,'parents':[],
                              'files':[{'path':'evidence.md','sha256':hashlib.sha256((repo/'evidence.md').read_bytes()).hexdigest()}]}
                c['alternatives']=[]
                c['ci']={'status':'not_checked','commit':sha,'url':'NOT_OBSERVED','reason':'Synthetic local evidence, not GitHub.'}
            mapping={c['repository']:str(repo) for c in x['components']}
            result=verify_sources(x,mapping)
            self.assertEqual((result['references'],result['source_files']),(8,8))
            self.assertFalse(result['hardware_qualified'])
            self.assertEqual(git('show-ref'),before)
            self.assertEqual(git('status','--porcelain'),'')
            # Reading committed bytes never substitutes a dirty checkout's content.
            (repo/'evidence.md').write_text('uncommitted alteration')
            self.assertEqual(verify_sources(x,mapping)['source_files'],8)
            x['components'][0]['primary']['files'][0]['sha256']='0'*64
            with self.assertRaises(LockError):verify_sources(x,mapping)

    def test_missing_repository_map_fails_closed(self):
        with self.assertRaises(LockError): verify_sources(self.lock,{})

    def test_cli_fails_closed_without_echoing_sensitive_error_details(self):
        with patch('sys.stderr') as stderr:
            self.assertEqual(main(['compare']),1)
            self.assertNotIn('/workspace',str(stderr.write.call_args_list))


if __name__=='__main__':unittest.main()
