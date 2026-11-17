import copy
import json
from pathlib import Path
import tempfile
import unittest

from tooling.gpu_forge.build_corpus import build, serialize
from tooling.gpu_forge.preparation import ROOT, estimated_cents, fits_budget, review, score_reply, validate_cases


POLICY = {'monthly_cap_cents': 4900, 'compute_cap_cents': 4000, 'ancillary_cap_cents': 400, 'reserve_cents': 500}


class PreparationTests(unittest.TestCase):
    def test_generated_corpus_matches_committed_bytes(self):
        self.assertEqual(serialize(build()), (ROOT / 'datasets/gpu-forge/g03-calibration.jsonl').read_text())
        self.assertEqual(100, sum(validate_cases(build()).values()))

    def test_duplicate_is_visible(self):
        rows = build(); rows[-1] = rows[0]
        with self.assertRaises(ValueError): validate_cases(rows)

    def test_empty_corpus_cannot_pass(self):
        with self.assertRaises(ValueError): validate_cases([])

    def test_exact_oracle_rejects_wrong_answer_and_extra_text(self):
        case = build()[0]
        self.assertTrue(score_reply(case, case['oracle']['expected']))
        self.assertFalse(score_reply(case, '999999'))
        self.assertFalse(score_reply(case, 'La réponse est ' + case['oracle']['expected']))

    def test_json_oracle_rejects_extra_keys_and_bool_number_substitution(self):
        case = {'oracle': {'kind': 'json_exact', 'expected': {'enabled': True}}}
        self.assertTrue(score_reply(case, '{"enabled":true}'))
        self.assertFalse(score_reply(case, '{"enabled":1}'))
        self.assertFalse(score_reply(case, '{"enabled":true,"extra":0}'))
        self.assertFalse(score_reply(case, '```json\n{"enabled":true}\n```'))

    def test_billing_rounds_up_and_reserves_shutdown(self):
        self.assertEqual(62, estimated_cents(600000, 3600, 60, 120))
        self.assertEqual(2, estimated_cents(600000, 61, 60, 0))
        self.assertEqual(1, estimated_cents(1, 1, 1, 0))

    def test_full_49_eur_envelope_including_reserve_is_valid(self):
        self.assertTrue(fits_budget(POLICY, 3990, 390, 10, 10))
        self.assertFalse(fits_budget(POLICY, 3990, 390, 11, 10))
        self.assertFalse(fits_budget(POLICY, 3990, 390, 10, 11))

    def test_50_eur_or_negative_or_boolean_amounts_are_refused(self):
        with self.assertRaises(ValueError): fits_budget({**POLICY, 'monthly_cap_cents': 5000}, 0, 0, 0, 0)
        with self.assertRaises(ValueError): fits_budget(POLICY, -1, 0, 0, 0)
        with self.assertRaises(ValueError): estimated_cents(True, 3600, 60, 0)

    def test_corrupt_dataset_hash_cannot_pass(self):
        manifest = json.loads((ROOT / 'docs/gpu-forge/g03/campaign.json').read_text())
        manifest['dataset']['sha256'] = '0' * 64
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'campaign.json'; path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError): review(path)

    def test_preparation_cannot_be_used_to_enable_provisioning(self):
        source = json.loads((ROOT / 'docs/gpu-forge/g03/campaign.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'campaign.json'
            for key in ('launch_authorized', 'provisioning_enabled'):
                manifest = copy.deepcopy(source); manifest[key] = True
                path.write_text(json.dumps(manifest))
                with self.assertRaises(ValueError): review(path)

    def test_review_does_not_claim_model_or_android_execution(self):
        report = review(ROOT / 'docs/gpu-forge/g03/campaign.json')
        self.assertEqual('NOT_AUTHORIZED', report['gpu_execution'])
        self.assertFalse(report['inference_executed'])
