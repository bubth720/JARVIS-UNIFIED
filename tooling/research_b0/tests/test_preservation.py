"""Actual Git sources, negative temporary clones; no production adapters."""
from pathlib import Path
import subprocess
import tempfile
import sys
import unittest
from tooling.research_b0.check_preservation import ROOT,BASE,ALLOWED,WORKFLOW,V1,freeze


class PreservationTest(unittest.TestCase):
    def clone(self):
        tmp=tempfile.TemporaryDirectory(prefix='b0-preservation-');self.addCleanup(tmp.cleanup)
        root=Path(tmp.name)/'repo'
        subprocess.run(['git','clone','--shared','--quiet','--no-checkout',str(ROOT),str(root)],check=True)
        subprocess.run(['git','-C',str(root),'checkout','--quiet','--detach',BASE],check=True)
        return root

    def test_all_525_old_files_and_contracts_unchanged(self):
        self.assertEqual(525,freeze(ROOT,BASE,ALLOWED,WORKFLOW)['historical_files_unchanged'])

    def test_production_contract_mutation_refused(self):
        root=self.clone();p=root/'contracts/v1/request-envelope.schema.json';p.write_text(p.read_text()+' ')
        with self.assertRaisesRegex(ValueError,'Historical bytes'):freeze(root,BASE)

    def test_historical_guard_mutation_refused(self):
        root=self.clone();p=root/'tooling/nexus_n01_a2/review.py';p.write_text(p.read_text()+'\n# mutation\n')
        with self.assertRaisesRegex(ValueError,'Historical bytes'):freeze(root,BASE)

    def test_historical_mode_mutation_refused(self):
        root=self.clone();p=root/'README.md';p.chmod(0o755)
        with self.assertRaisesRegex(ValueError,'Historical mode'):freeze(root,BASE)

    def test_addition_outside_lab_refused(self):
        root=self.clone();(root/'UNDECLARED.txt').write_text('synthetic')
        with self.assertRaisesRegex(ValueError,'Unexpected addition'):freeze(root,BASE,ALLOWED,WORKFLOW)

    def test_unchanged_v1_guard_still_refuses_historical_mutation(self):
        ui=ROOT.parent/'JARVIS-INTERFACE'
        tmp=tempfile.TemporaryDirectory(prefix='b0-v1-negative-');self.addCleanup(tmp.cleanup)
        clone=Path(tmp.name)/'interface'
        subprocess.run(['git','clone','--shared','--quiet','--no-checkout',str(ui),str(clone)],check=True)
        subprocess.run(['git','-C',str(clone),'checkout','--quiet','--detach',V1],check=True)
        p=clone/'README.md';p.write_text(p.read_text()+'\nSynthetic unauthorized mutation\n')
        result=subprocess.run([sys.executable,'labs/v1/tools/check_scope.py','--interface',str(clone)],cwd=clone,
                              stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=90)
        self.assertNotEqual(0,result.returncode,result.stdout)
        self.assertIn('README.md',result.stdout)
