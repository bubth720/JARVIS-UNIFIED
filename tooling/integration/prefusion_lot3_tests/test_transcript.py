import copy
import json
from pathlib import Path
import unittest
from tooling.integration.prefusion_lot3 import review, TranscriptError


ROOT = Path(__file__).resolve().parents[3]


class TranscriptTests(unittest.TestCase):
    def setUp(self):
        self.value = json.loads((ROOT / 'docs/prefusion/lot3/txt.json').read_text())

    def reject(self, mutate):
        value = copy.deepcopy(self.value)
        mutate(value)
        with self.assertRaises(TranscriptError):
            review(value)

    def test_txt_reports_only_unavailable(self):
        result = review(self.value)
        self.assertEqual(result['display'], 'UNAVAILABLE')
        self.assertFalse(result['runtime_link_enabled'])
        self.assertNotIn('text', result)

    def test_csv(self):
        self.assertEqual(review(json.loads((ROOT / 'docs/prefusion/lot3/csv.json').read_text()))['status'], 'UNSUPPORTED')

    def test_digest_mismatch(self):
        self.reject(lambda v: v['source'].update(text='changed'))

    def test_large_source(self):
        self.reject(lambda v: v['source'].update(text='x' * 2049))

    def test_fabricated_citation(self):
        self.reject(lambda v: v['events'][2].update(citation='invented'))

    def test_fabricated_ready(self):
        self.reject(lambda v: v['events'][2].update(state='READY'))

    def test_replay(self):
        self.reject(lambda v: v['events'][1].update(sequence=1))

    def test_gap(self):
        self.reject(lambda v: v['events'][1].update(sequence=3))

    def test_wrong_session(self):
        self.reject(lambda v: v['events'][1].update(session=v['request']))

    def test_old_epoch(self):
        self.reject(lambda v: v['events'][1].update(epoch=v['request']))

    def test_generation_zero_and_boolean(self):
        for generation in (0, True, -1, 2**53):
            with self.subTest(generation=generation):
                self.reject(lambda v: v.update(generation=generation))

    def test_payload_uid_not_identity(self):
        self.reject(lambda v: v.update(uid=1000))

    def test_runtime_activation(self):
        self.reject(lambda v: v.update(runtime_enabled=True))

    def test_partial_transcript(self):
        self.reject(lambda v: v['events'].pop())

    def test_invalid_utf8(self):
        self.reject(lambda v: v['source'].update(text='\ud800'))

    def test_foreign_generation(self):
        self.reject(lambda v: v['events'][1].update(generation=2))

    def test_wrong_producer(self):
        self.reject(lambda v: v['events'][2].update(module='LLM'))

    def test_no_mutation(self):
        old = copy.deepcopy(self.value)
        self.assertFalse(review(self.value)['mutation_performed'])
        self.assertEqual(old, self.value)
