import copy
from pathlib import Path
import unittest

from tooling.reuse_r1plus.verify import REPORT, check
from tooling.v1.validate import InvalidEvidence, read


class ReuseReceptionTests(unittest.TestCase):
    def setUp(self):
        self.receipt = read(REPORT / 'RECEIPT.json')

    def row(self, name):
        return next(r for r in self.receipt['modules'] if r['module'] == name)

    def test_real_receipts_pass_only_documentary_check(self):
        result = check(self.receipt)
        self.assertEqual('PASS_DOCUMENTARY_CHECK_ONLY', result['status'])
        self.assertFalse(result['can_activate'])

    def test_green_jvm_cannot_promote_any_runtime_capability(self):
        for flag in ('can_activate', 'productive_connection', 'android_qualified', 'real_llm_qualified', 'vertical_integrated'):
            with self.subTest(flag=flag):
                forged = copy.deepcopy(self.receipt); forged[flag] = True
                with self.assertRaisesRegex(InvalidEvidence, 'UNSUPPORTED_PROMOTION'):
                    check(forged)

    def test_voice_skips_cannot_be_reported_as_passes(self):
        row = self.row('VOICE'); row['passed'] += row['junit']['skipped']
        with self.assertRaisesRegex(InvalidEvidence, 'PASS_COUNTS'): check(self.receipt)

    def test_other_snapshot_cannot_inherit_fresh_core_tests(self):
        self.row('CORE')['tested_source'] = '0' * 40
        with self.assertRaisesRegex(InvalidEvidence, 'SOURCE_BINDING'): check(self.receipt)

    def test_llm_tests_reproducing_defects_do_not_mean_safety_pass(self):
        self.row('LLM')['safety_verdict'] = 'PASS'
        with self.assertRaisesRegex(InvalidEvidence, 'LLM_NO_GO_HIDDEN'): check(self.receipt)

    def test_nexus_host_adapter_is_not_a_runtime_connection(self):
        self.row('NEXUS')['test_source_set_only'] = False
        with self.assertRaisesRegex(InvalidEvidence, 'NEXUS_PROMOTION'): check(self.receipt)

    def test_apk_build_cannot_replace_android_reception(self):
        self.row('INTERFACE')['android_status'] = 'PASS'
        with self.assertRaisesRegex(InvalidEvidence, 'ANDROID_BUILD_PROMOTION'): check(self.receipt)

    def test_raw_preflight_contradicted_by_anr_is_not_accepted(self):
        self.receipt['api29_raw_preflight_accepted'] = True
        with self.assertRaisesRegex(InvalidEvidence, 'CONTRADICTORY_PREFLIGHT'): check(self.receipt)

    def test_closed_campaign_cannot_be_reported_as_new_attempt(self):
        self.receipt['campaign_attempt'] = 2
        with self.assertRaisesRegex(InvalidEvidence, 'CAMPAIGN_ID'): check(self.receipt)


if __name__ == '__main__': unittest.main()
