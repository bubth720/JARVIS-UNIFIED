import json, shutil, tempfile, unittest
from pathlib import Path
import tooling.monorepo.import_manifest as im

class ImportManifest(unittest.TestCase):
    def test_imported_tree_matches_manifest(self):
        self.assertEqual([], im.check())

    def _fake(self):
        root = Path(tempfile.mkdtemp()); (root / 'tooling/monorepo/import').mkdir(parents=True)
        (root / 'tooling/monorepo/sources.lock.json').write_text(json.dumps({'modules': [{'id': 'core', 'source_sha': 'a' * 40, 'target': 'modules/core'}]}))
        (root / 'modules/core').mkdir(parents=True); (root / 'modules/core/A.kt').write_text('class A')
        old = (im.ROOT, im.LOCK, im.MANIFEST)
        im.ROOT, im.LOCK, im.MANIFEST = root, root / 'tooling/monorepo/sources.lock.json', root / 'tooling/monorepo/import/IMPORT-MANIFEST.json'
        self.addCleanup(lambda: setattr(im, 'ROOT', old[0]) or setattr(im, 'LOCK', old[1]) or setattr(im, 'MANIFEST', old[2]))
        got, problems = im.compute(); self.assertEqual([], problems)
        im.MANIFEST.write_text(json.dumps({'modules': got})); return root

    def test_changed_extra_missing_and_forbidden_files_are_no_go(self):
        root = self._fake(); self.assertEqual([], im.check())
        (root / 'modules/core/A.kt').write_text('class A2'); self.assertTrue(any('tree_sha256' in p for p in im.check()))
        (root / 'modules/core/A.kt').write_text('class A'); (root / 'modules/core/model.gguf').write_bytes(b'x')
        self.assertTrue(any('forbidden' in p for p in im.check())); (root / 'modules/core/model.gguf').unlink()
        (root / 'modules/extra').mkdir(); self.assertTrue(any('unexpected module' in p for p in im.check())); (root / 'modules/extra').rmdir()
        shutil.rmtree(root / 'modules/core'); self.assertTrue(any('missing' in p for p in im.check()))

if __name__ == '__main__': unittest.main()
