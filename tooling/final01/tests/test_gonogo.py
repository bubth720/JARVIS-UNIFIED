import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from tooling.final01.gonogo import decide

A = 'a' * 40; B = 'b' * 40
REQ = {'lot': 'FX', 'required': [{'id': 't1', 'sha': A}, {'id': 't2', 'sha': A}]}

def ev(i, r, sha=A, source='run 1'):
    return {'id': i, 'sha': sha, 'result': r, 'source': source}


class Gate(unittest.TestCase):
    def test_all_pass_is_go(self):
        self.assertEqual('GO', decide(REQ, [ev('t1', 'PASS'), ev('t2', 'PASS')])['verdict'])

    def test_every_non_pass_result_is_no_go(self):
        for bad in ['FAIL', 'BLOCKED', 'BLOCKED_DEVICE', 'NOT_RUN', 'UNKNOWN', 'SKIPPED', 'pass', 'Pass', 'PASSED', 'OK', '', None, True, 1]:
            out = decide(REQ, [ev('t1', 'PASS'), ev('t2', bad)])
            self.assertEqual('NO-GO', out['verdict'], bad)

    def test_missing_evidence_is_no_go(self):
        out = decide(REQ, [ev('t1', 'PASS')])
        self.assertEqual('NO-GO', out['verdict']); self.assertIn('t2: no evidence', out['reasons'][0])

    def test_evidence_at_another_commit_is_no_go(self):
        out = decide(REQ, [ev('t1', 'PASS'), ev('t2', 'PASS', sha=B)])
        self.assertEqual('NO-GO', out['verdict']); self.assertIn('only at', out['reasons'][0])

    def test_branch_name_or_short_sha_requirement_is_no_go(self):
        for sha in ['main', 'aaaaaaa', A.upper(), A + 'a', None]:
            self.assertEqual('NO-GO', decide({'required': [{'id': 't1', 'sha': sha}]}, [ev('t1', 'PASS', sha=sha)])['verdict'], sha)

    def test_contradictory_evidence_is_no_go(self):
        self.assertEqual('NO-GO', decide(REQ, [ev('t1', 'PASS'), ev('t1', 'FAIL'), ev('t2', 'PASS')])['verdict'])

    def test_unsourced_evidence_is_no_go(self):
        self.assertEqual('NO-GO', decide(REQ, [ev('t1', 'PASS', source=''), ev('t2', 'PASS')])['verdict'])

    def test_empty_requirements_is_no_go(self):
        self.assertEqual('NO-GO', decide({'lot': 'FX', 'required': []}, [ev('t1', 'PASS')])['verdict'])
        self.assertEqual('NO-GO', decide({}, [])['verdict'])

    def test_extra_passing_evidence_cannot_hide_a_missing_test(self):
        self.assertEqual('NO-GO', decide(REQ, [ev('t1', 'PASS'), ev('t3', 'PASS'), ev('t2x', 'PASS')])['verdict'])

    def test_cli_exit_code(self):
        d = Path(tempfile.mkdtemp()); (d / 'r.json').write_text(json.dumps(REQ))
        (d / 'e.json').write_text(json.dumps([ev('t1', 'PASS'), ev('t2', 'NOT_RUN')]))
        p = subprocess.run([sys.executable, '-m', 'tooling.final01.gonogo', str(d / 'r.json'), str(d / 'e.json')], capture_output=True, text=True)
        self.assertEqual(1, p.returncode); self.assertEqual('NO-GO', json.loads(p.stdout)['verdict'])
        (d / 'e.json').write_text(json.dumps([ev('t1', 'PASS'), ev('t2', 'PASS')]))
        p = subprocess.run([sys.executable, '-m', 'tooling.final01.gonogo', str(d / 'r.json'), str(d / 'e.json')], capture_output=True, text=True)
        self.assertEqual(0, p.returncode)


if __name__ == '__main__': unittest.main()
