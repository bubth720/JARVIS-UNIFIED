"""Synthetic receipt mutations; none of these fixtures qualifies a real device."""
import copy
import unittest
from tooling.v1 import reception as r, validate as v


class ReceivedComposition(unittest.TestCase):
    def setUp(self):
        self.modules = v.check_lock(v.read(v.REPORTS/'BASELINE-LOCK.json'))
        self.score = copy.deepcopy(v.read(v.REPORTS/'SCORE.json'))
        self.base_score = copy.deepcopy(self.score)
        self.receipt = {
            'schema': 'jarvis.v1.receipts/1', 'scored_source': 'a'*40,
            'score_claims_allowed': True,
            'receipts': [{
                'receipt_id': 'fixture-build', 'kind': 'APK_BUILD',
                'module_id': 'INTERFACE', 'repository': r.HOST_REPOSITORY,
                'status': 'PASS', 'source_commit': 'a'*40, 'source_tree': 'b'*40,
                'ui_base_commit': self.modules['INTERFACE']['source_sha'],
                'artifact_zip_sha256': 'c'*64, 'ci_run': 123,
                'ci_url': 'https://github.com/'+r.HOST_REPOSITORY+'/actions/runs/123',
                'ci_job_conclusion': 'success',
                'runtime_connections': ['INTERFACE_LOCAL_ONLY'],
                'physical_android': 'NOT_RUN', 'llm_generation': 'NOT_RUN',
                'apk': {'package': 'fr.jarvis.v1.lab', 'variant': 'candidate',
                        'test_only': True, 'allow_backup': False,
                        'sha256': 'd'*64, 'test_sha256': '9'*64, 'certificate_sha256': 'e'*64,
                        'permissions': ['fr.jarvis.v1.lab.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION']},
            }],
        }
        for api in (29, 35):
            self.receipt['receipts'].append({
                'receipt_id': 'fixture-api'+str(api), 'kind': 'ANDROID_EMULATOR',
                'module_id': 'INTERFACE', 'repository': r.HOST_REPOSITORY,
                'status': 'PASS', 'build_receipt_id': 'fixture-build',
                'source_commit': 'a'*40, 'source_tree': 'b'*40, 'apk_sha256': 'd'*64,
                'test_apk_sha256': '9'*64, 'package': 'fr.jarvis.v1.lab',
                'ci_run': 123, 'ci_job': api, 'ci_job_conclusion': 'success',
                'ci_url': 'https://github.com/'+r.HOST_REPOSITORY+'/actions/runs/123',
                'platform': 'ANDROID_EMULATOR', 'api': api, 'abi': 'x86_64',
                'emulation': 'TCG', 'protections_changed': False,
                'physical_android': 'NOT_RUN', 'llm_generation': 'NOT_RUN',
                'artifact_zip_sha256': 'f'*64,
                'proof_review': 'RAW_LOGS_HASHES_AND_OUTPUTS_INSPECTED',
                'evidence_files': {'fixture-functional.txt': '1'*64},
                'qualified_operations': sorted(r.OPERATIONS),
            })
        for row in self.score['criteria']:
            if row['domain'] == 'COCKPIT' and row['operation_id'] in r.OPERATIONS:
                row.update(state='PASS', evidence_ref='fixture-api29', tested_commit='a'*40)
        self.score.update(qualified_points=12, unassessed_or_blocked_points=88)

    def check(self):
        return r.check(self.receipt, self.score, self.modules)

    def test_real_receipt_and_score_validate_without_authority(self):
        result=r.validate()
        self.assertFalse(result['runtime_authority_granted'])
        self.assertEqual('NOT_RUN',result['llm_generation'])

    def test_synthetic_valid_receipt_preserves_baseline_mapping(self):
        before=copy.deepcopy(self.modules)
        self.assertEqual(12,self.check()['qualified_points'])
        self.assertEqual(before,self.modules)

    def test_device_source_mismatch_rejected(self):
        self.receipt['receipts'][1]['source_commit']='2'*40
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_GIT_BINDING'):self.check()

    def test_device_tree_mismatch_rejected(self):
        self.receipt['receipts'][1]['source_tree']='2'*40
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_GIT_BINDING'):self.check()

    def test_apk_digest_mismatch_rejected(self):
        self.receipt['receipts'][1]['apk_sha256']='2'*64
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_APK_BINDING'):self.check()

    def test_ci_from_another_run_rejected(self):
        self.receipt['receipts'][1]['ci_run']=124
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_CI_BINDING'):self.check()

    def test_different_test_apk_or_package_cannot_certify_candidate(self):
        self.receipt['receipts'][1]['test_apk_sha256']='2'*64
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_TEST_APK_BINDING'):self.check()
        self.receipt['receipts'][1]['test_apk_sha256']='9'*64
        self.receipt['receipts'][1]['package']='fr.jarvis.v1.lab.baseline'
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_PACKAGE_SCOPE'):self.check()

    def test_provenance_link_cannot_point_elsewhere(self):
        self.receipt['receipts'][0]['ci_url']='https://github.com/bubth720/other/actions/runs/123'
        with self.assertRaisesRegex(v.InvalidEvidence,'BUILD_PROVENANCE'):self.check()

    def test_score_scope_cannot_be_extended_to_real_chat(self):
        row=self.score['criteria'][3];row.update(state='PASS',evidence_ref='fixture-api29',tested_commit='a'*40)
        with self.assertRaisesRegex(v.InvalidEvidence,'SCORE_RECEIPT_SCOPE'):self.check()

    def test_false_physical_claim_rejected(self):
        self.receipt['receipts'][1]['platform']='ANDROID_PHYSICAL'
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_PLATFORM'):self.check()

    def test_build_count_never_qualifies_an_android_operation(self):
        self.receipt['receipts'][1].pop('proof_review')
        self.receipt['receipts'][1]['tests_passed']=10000
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_PROOF_REVIEW_REQUIRED'):self.check()

    def test_job_failure_cannot_be_overwritten_by_receipt_pass(self):
        self.receipt['receipts'][1]['ci_job_conclusion']='failure'
        with self.assertRaisesRegex(v.InvalidEvidence,'DEVICE_JOB_NOT_SUCCESS'):self.check()

    def test_android_matrix_must_include_both_received_apis(self):
        self.receipt['receipts'].pop()
        with self.assertRaisesRegex(v.InvalidEvidence,'ANDROID_MATRIX_NOT_RECEIVED'):self.check()

    def test_one_api_without_crud_proof_does_not_award_crud(self):
        self.receipt['receipts'][2]['qualified_operations'].remove('CRUD_PERSISTENCE')
        with self.assertRaisesRegex(v.InvalidEvidence,'OPERATION_NOT_RECEIVED_ON_ALL_APIS'):self.check()

    def test_two_different_builds_of_same_commit_do_not_form_one_matrix(self):
        other=copy.deepcopy(self.receipt['receipts'][0])
        other['receipt_id']='fixture-other-build'
        other['apk']['sha256']='2'*64
        self.receipt['receipts'].append(other)
        self.receipt['receipts'][2]['build_receipt_id']='fixture-other-build'
        self.receipt['receipts'][2]['apk_sha256']='2'*64
        with self.assertRaisesRegex(v.InvalidEvidence,'ANDROID_MATRIX_ARTIFACT_MISMATCH'):self.check()

    def test_sensitive_permission_and_runtime_connections_rejected(self):
        self.receipt['receipts'][0]['apk']['permissions'].append('android.permission.INTERNET')
        with self.assertRaisesRegex(v.InvalidEvidence,'APK_PERMISSION_SCOPE'):self.check()
        self.receipt['receipts'][0]['apk']['permissions'].pop()
        self.receipt['receipts'][0]['runtime_connections'].append('CORE')
        with self.assertRaisesRegex(v.InvalidEvidence,'BUILD_RUNTIME_SCOPE'):self.check()

    def test_failed_device_cannot_carry_qualified_operations(self):
        self.receipt['receipts'][1]['status']='FAIL'
        with self.assertRaisesRegex(v.InvalidEvidence,'FAILED_DEVICE_CANNOT_SCORE'):self.check()

    def test_raw_file_digest_and_duplicate_receipt_id_rejected(self):
        self.receipt['receipts'][1]['evidence_files']['fixture-functional.txt']='UNKNOWN'
        with self.assertRaisesRegex(v.InvalidEvidence,'ARTIFACT_SHA256'):self.check()
        self.receipt['receipts'][1]['evidence_files']['fixture-functional.txt']='1'*64
        self.receipt['receipts'][2]['receipt_id']='fixture-api29'
        with self.assertRaisesRegex(v.InvalidEvidence,'RECEIPT_IDS'):self.check()

    def test_old_validator_is_still_strict_and_cannot_promote_new_source(self):
        evidence={'fixture-api29': {'module_id':'INTERFACE','tested_commit':'a'*40,'status':'PASS'}}
        with self.assertRaisesRegex(v.InvalidEvidence,'CLAIM_AT_WRONG_SOURCE'):
            v.check_score(self.score,self.modules,evidence)


if __name__ == '__main__':
    unittest.main()
