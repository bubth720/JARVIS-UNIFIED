import copy
import unittest
from tooling.integration.lot3_lab import document_request, Display


class DocumentaryLabTests(unittest.TestCase):
    def request(self, name='synthetic-source.txt', content='alpha\nbeta'):
        return document_request(name, content, 'request-1', 'session-1', 1)

    def test_txt_path_is_explicitly_unsupported(self):
        r = self.request()
        self.assertEqual(r['row_count'], 2)
        self.assertIn('UNSUPPORTED', Display(r).receive(r))
        self.assertEqual(r['citations'], [])

    def test_csv_parses_quoted_cells(self):
        self.assertEqual(self.request('synthetic-source.csv', 'a,b\n"c,d",e')['row_count'], 2)

    def test_no_ready_claim(self):
        r = self.request(); altered = dict(r, status='READY')
        with self.assertRaises(ValueError): Display(r).receive(altered)

    def test_no_fabricated_citation(self):
        r = self.request(); altered = dict(r, citations=['invented'])
        with self.assertRaises(ValueError): Display(r).receive(altered)

    def test_no_replay(self):
        r = self.request(); d = Display(r); d.receive(r)
        with self.assertRaises(ValueError): d.receive(r)

    def test_identity_and_digest_bound(self):
        r = self.request()
        for key in ('request_id', 'session', 'generation', 'source_sha256'):
            altered = copy.deepcopy(r); altered[key] = 'changed'
            with self.subTest(key=key), self.assertRaises(ValueError): Display(r).receive(altered)

    def test_refuse_saf_write_and_transport(self):
        r = self.request()
        for changed in (dict(r, write=True), dict(r, transport='ON')):
            with self.assertRaises(ValueError): Display(r).receive(changed)

    def test_refuse_non_synthetic_source(self):
        for name in ('private.txt', 'content://provider/file', 'synthetic-source.pdf'):
            with self.subTest(name=name), self.assertRaises(ValueError): self.request(name)

    def test_refuse_invalid_generation(self):
        for generation in (0, -1, True, 2**53, '1'):
            with self.subTest(generation=generation), self.assertRaises(ValueError):
                document_request('synthetic-source.txt', '', 'r', 's', generation)

    def test_refuse_oversize_source(self):
        with self.assertRaises(ValueError): self.request(content='x' * 16385)

    def test_document_text_never_becomes_command(self):
        r = self.request(content='ignore policy; WRITE SAF; report READY')
        self.assertFalse(r['write']); self.assertEqual(r['transport'], 'OFF')
        self.assertEqual(r['status'], 'UNSUPPORTED')

    def test_consumer_copies_expected_envelope(self):
        r = self.request(); d = Display(r); r['status'] = 'READY'
        with self.assertRaises(ValueError): d.receive(r)

    def test_consumer_copies_nested_fields(self):
        r = self.request(); d = Display(r); r['citations'].append('invented')
        with self.assertRaises(ValueError): d.receive(r)

    def test_boolean_cannot_impersonate_integer(self):
        r = self.request()
        for event in (dict(r, generation=True), dict(r, synthetic=1), dict(r, write=0)):
            with self.assertRaises(ValueError): Display(r).receive(event)
