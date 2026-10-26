import json
import unittest
from tooling.integration.ci import unittest_result
from tooling.integration.lock import ROOT

class CiEvidenceTests(unittest.TestCase):
    def test_failed_empty_skipped_and_missing_results_do_not_become_pass(self):
        for text,code in [('Ran 0 tests in 0.001s\nOK',0),('Ran 3 tests in 1s\nOK (skipped=1)',0),('Ran 3 tests in 1s\nFAILED (failures=1, errors=1)',1),('command died',0)]:
            self.assertFalse(unittest_result(text,code)['ok'])
        self.assertTrue(unittest_result('Ran 3 tests in 1.2s\nOK',0)['ok'])

    def test_independent_workflow_is_parseable_without_yaml_dependency(self):
        data=json.loads((ROOT/'.github/workflows/fusion-02.yml').read_text())
        self.assertIn('push',data['on']);self.assertIn('pull_request',data['on'])
        self.assertEqual(data['permissions'],{'contents':'read'})
        steps=data['jobs']['independent-validation']['steps']
        python=next(s for s in steps if s.get('uses','').startswith('actions/setup-python'))
        self.assertEqual(python['with']['python-version'],'3.12.12')
        self.assertTrue(any(s.get('if')=='always()' and s.get('uses','').startswith('actions/upload-artifact') for s in steps))

