import unittest
from scripts.contracts import validate
from tooling.integration.lock import ROOT, load
from tooling.integration.proposals import check


class TechnicalObservationTests(unittest.TestCase):
    def setUp(self):
        self.directory=ROOT/'docs/fusion-01/proposals'
        self.schema=load(self.directory/'technical-health.schema.json')
        self.value=load(self.directory/'technical-health.valid.json')

    def test_examples_are_checked_without_approval_or_activation(self):
        result=check()
        self.assertFalse(result['approved']);self.assertFalse(result['runtime_connected'])
        self.assertEqual(result['invalid_examples_rejected'],1)

    def test_free_text_and_personal_data_not_admitted(self):
        for name in ['path','conversation','profile','principal','prompt']:
            value=dict(self.value);value[name]='SYNTHETIC'
            with self.assertRaises(ValueError):validate(value,self.schema)

    def test_unknown_module_and_string_metrics_are_refused(self):
        self.value['module']='external'
        with self.assertRaises(ValueError):validate(self.value,self.schema)
        self.value['module']='core';self.value['metrics']={'queue_size':'1'}
        with self.assertRaises(ValueError):validate(self.value,self.schema)

    def test_invalid_metrics_and_boolean_coercion_are_refused(self):
        for invalid in [-1,257,True]:
            self.value['metrics']={'queue_size':invalid}
            with self.assertRaises(ValueError):validate(self.value,self.schema)
