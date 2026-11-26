import json, subprocess, tempfile, unittest
from pathlib import Path
from tooling.final01.candidate_check import run

def repo():
    t = tempfile.mkdtemp(); g = lambda *a: subprocess.run(['git', '-C', t, *a], check=True, capture_output=True, text=True).stdout.strip()
    g('init', '-q'); g('config', 'user.email', 't@invalid'); g('config', 'user.name', 't'); return t, g

def commit(t, g, files):
    for p, c in files.items(): Path(t, p).parent.mkdir(parents=True, exist_ok=True); Path(t, p).write_text(c)
    g('add', '-A'); g('commit', '-q', '-m', 'c'); return g('rev-parse', 'HEAD')

class CandidateCheck(unittest.TestCase):
    def setUp(self):
        self.t, self.g = repo()
        self.pin = commit(self.t, self.g, {'a02/native/engine.cpp': 'v1', 'pocketRuntime/src/P.kt': 'p1', 'docs/x.md': 'd'})
        self.lock = Path(tempfile.mkdtemp(), 'sources.json')
        blob = self.g('rev-parse', f'{self.pin}:a02/native/engine.cpp')
        self.lock.write_text(json.dumps({'modules': [{'id': 'LLM', 'sha': self.pin, 'native': [{'path': 'a02/native/engine.cpp', 'sha': blob, 'size': 2}]}],
                                         'voice': {'sha': self.pin, 'module': 'pocketRuntime'}}))

    def test_docs_and_ci_only_change_is_drop_in(self):
        c = commit(self.t, self.g, {'docs/x.md': 'changed', '.github/workflows/w.yml': 'ci'})
        self.assertEqual('DROP_IN', run(str(self.lock), 'LLM', self.t, c)['status'])
        self.assertEqual('DROP_IN', run(str(self.lock), 'VOICE', self.t, c)['status'])

    def test_locked_native_change_is_not_drop_in(self):
        c = commit(self.t, self.g, {'a02/native/engine.cpp': 'v2'})
        r = run(str(self.lock), 'LLM', self.t, c); self.assertEqual('NOT_DROP_IN', r['status']); self.assertEqual('a02/native/engine.cpp', r['differences'][0]['path'])

    def test_runtime_tree_change_is_not_drop_in(self):
        c = commit(self.t, self.g, {'pocketRuntime/src/New.kt': 'n'})
        r = run(str(self.lock), 'VOICE', self.t, c); self.assertEqual('NOT_DROP_IN', r['status']); self.assertIn('pocketRuntime/src/New.kt', r['differences'])

    def test_divergent_history_is_not_drop_in_even_with_same_bytes(self):
        self.g('checkout', '-q', '--orphan', 'other'); c = commit(self.t, self.g, {'a02/native/engine.cpp': 'v1', 'pocketRuntime/src/P.kt': 'p1', 'unrelated.txt': 'rewritten history'})
        self.assertEqual('NOT_DROP_IN', run(str(self.lock), 'LLM', self.t, c)['status'])

if __name__ == '__main__': unittest.main()
