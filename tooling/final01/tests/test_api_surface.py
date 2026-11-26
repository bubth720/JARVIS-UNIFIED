import subprocess, tempfile, unittest
from pathlib import Path
from tooling.final01.api_surface import compare, declarations

class Decl(unittest.TestCase):
    def test_visibility_rules(self):
        src = """package a.b
/** doc fun hidden() */
class Port(val x: Int) {
    fun open(path: String): Result
    private fun secret() = 1
    internal val inner = 2
    // fun commented()
}
internal class Hidden { fun notPublic() }
fun top(a: Int = 3): Int = a
private fun priv() {}
"""
        d = declarations('A.kt', src)
        self.assertIn('a.b :: class Port(val x: Int)', d)
        self.assertIn('a.b.Port :: fun open(path: String): Result', d)
        self.assertIn('a.b :: fun top(a: Int = 3): Int', d)
        d2 = declarations('B.kt', 'package q\nfun on(cb: (Int) -> Unit = {}): Map<String, Int> = emptyMap()\nval h: (String) -> Int = { 1 }\n')
        self.assertIn('q :: fun on(cb: (Int) -> Unit', d2[0]); self.assertNotIn('emptyMap', d2[0]); self.assertEqual('q :: val h: (String) -> Int', d2[1])
        for bad in ('secret', 'inner', 'commented', 'Hidden', 'notPublic', 'priv', 'hidden()'):
            self.assertFalse(any(bad in x for x in d), bad)

class Compare(unittest.TestCase):
    def repo(self, versions):
        t = tempfile.mkdtemp(); g = lambda *a: subprocess.run(['git', '-C', t, *a], check=True, capture_output=True, text=True).stdout.strip()
        g('init', '-q'); g('config', 'user.email', 't@invalid'); g('config', 'user.name', 't'); shas = []
        for v in versions:
            Path(t, 'src').mkdir(exist_ok=True); Path(t, 'src/P.kt').write_text(v); g('add', '-A'); g('commit', '-q', '-m', 'v'); shas.append(g('rev-parse', 'HEAD'))
        return t, shas

    def test_identical_additive_and_breaking(self):
        base = 'package p\ninterface Port {\n    fun read(id: String): Data\n}\n'
        t, (a, b, c, d) = self.repo([base, base + '// comment only\n', base.replace('}', '    fun list(): List<Data>\n}'), base.replace('id: String', 'id: Long')])
        self.assertEqual('IDENTICAL', compare(t, a, b, ['src'])['status'])
        self.assertEqual('ADDITIVE', compare(t, a, c, ['src'])['status'])
        r = compare(t, a, d, ['src']); self.assertEqual('BREAKING_CANDIDATE', r['status'])
        self.assertIn('p.Port :: fun read(id: String): Data', r['removed_or_changed'])

    def test_visibility_reduction_is_breaking(self):
        t, (a, b) = self.repo(['package p\nfun api(): Int = 1\n', 'package p\ninternal fun api(): Int = 1\n'])
        self.assertEqual('BREAKING_CANDIDATE', compare(t, a, b, ['src'])['status'])

if __name__ == '__main__': unittest.main()
