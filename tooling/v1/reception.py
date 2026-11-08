"""Validate a separately received lab composition without rewriting the source audit.

This is evidence bookkeeping, not an authority or runtime switch. Device counts
never award points: an inspected operation must be named in an exact receipt.
"""
import copy
import json
from pathlib import Path
from tooling.v1 import validate as v

OPERATIONS = {'NAVIGATION', 'CRUD_PERSISTENCE', 'OFFLINE'}
HOST_REPOSITORY = 'bubth720/JARVIS-INTERFACE'


def check(receipt, score, baseline_modules):
    v.need(receipt.get('schema') == 'jarvis.v1.receipts/1', 'RECEIPT_VERSION')
    rows = receipt.get('receipts', [])
    v.need(isinstance(rows, list), 'RECEIPT_LIST')
    ids = [r.get('receipt_id') for r in rows]
    v.need(all(isinstance(i, str) and i for i in ids) and len(ids) == len(set(ids)), 'RECEIPT_IDS')
    builds = {}
    for row in rows:
        if row.get('kind') != 'APK_BUILD':
            continue
        v.need(row.get('module_id') == 'INTERFACE' and row.get('status') == 'PASS', 'BUILD_SCOPE')
        v.need(row.get('repository') == HOST_REPOSITORY, 'BUILD_REPOSITORY')
        v.need(v.digest(row.get('source_commit'), 40) and v.digest(row.get('source_tree'), 40), 'BUILD_GIT_IDENTITY')
        v.need(row.get('ui_base_commit') == baseline_modules['INTERFACE']['source_sha'], 'BUILD_BASELINE_BINDING')
        v.need(v.digest(row.get('artifact_zip_sha256')), 'BUILD_ARTIFACT_DIGEST')
        v.need(row.get('ci_job_conclusion') == 'success' and type(row.get('ci_run')) is int, 'BUILD_CI')
        v.need(row.get('ci_url') == f"https://github.com/{HOST_REPOSITORY}/actions/runs/{row['ci_run']}", 'BUILD_PROVENANCE')
        apk = row.get('apk', {})
        v.need(apk.get('package') == 'fr.jarvis.v1.lab' and apk.get('variant') == 'candidate', 'APK_SCOPE')
        v.need(apk.get('test_only') is True and apk.get('allow_backup') is False, 'APK_ISOLATION')
        v.need(v.digest(apk.get('sha256')) and v.digest(apk.get('test_sha256')) and v.digest(apk.get('certificate_sha256')), 'APK_DIGEST')
        v.need(apk.get('permissions') == ['fr.jarvis.v1.lab.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION'], 'APK_PERMISSION_SCOPE')
        v.need(row.get('runtime_connections') == ['INTERFACE_LOCAL_ONLY'], 'BUILD_RUNTIME_SCOPE')
        v.need(row.get('physical_android') == 'NOT_RUN' and row.get('llm_generation') == 'NOT_RUN', 'BUILD_QUALIFICATION_SCOPE')
        builds[row['receipt_id']] = row
    evidence = {}
    scored_source = receipt.get('scored_source')
    for row in rows:
        if row.get('kind') != 'ANDROID_EMULATOR':
            continue
        v.need(row.get('module_id') == 'INTERFACE', 'DEVICE_MODULE_SCOPE')
        v.need(row.get('status') in {'PASS', 'FAIL', 'NOT_RUN'}, 'DEVICE_STATUS')
        v.need(row.get('build_receipt_id') in builds, 'DEVICE_BUILD_MISSING')
        build = builds[row['build_receipt_id']]
        v.need(row.get('source_commit') == build['source_commit'] and row.get('source_tree') == build['source_tree'], 'DEVICE_GIT_BINDING')
        v.need(row.get('apk_sha256') == build['apk']['sha256'], 'DEVICE_APK_BINDING')
        v.need(row.get('test_apk_sha256') == build['apk']['test_sha256'], 'DEVICE_TEST_APK_BINDING')
        v.need(row.get('package') == build['apk']['package'], 'DEVICE_PACKAGE_SCOPE')
        v.need(row.get('repository') == HOST_REPOSITORY and row.get('ci_run') == build['ci_run'], 'DEVICE_CI_BINDING')
        v.need(row.get('ci_url') == build['ci_url'], 'DEVICE_PROVENANCE')
        v.need(row.get('platform') == 'ANDROID_EMULATOR' and row.get('api') in (29, 35), 'DEVICE_PLATFORM')
        v.need(row.get('abi') == 'x86_64' and row.get('emulation') in ('TCG', 'KVM'), 'DEVICE_ENVIRONMENT')
        v.need(row.get('protections_changed') is False, 'DEVICE_PROTECTION_SCOPE')
        v.need(row.get('physical_android') == 'NOT_RUN' and row.get('llm_generation') == 'NOT_RUN', 'DEVICE_QUALIFICATION_SCOPE')
        v.need(v.digest(row.get('artifact_zip_sha256')), 'DEVICE_ARTIFACT_DIGEST')
        ops = row.get('qualified_operations', [])
        v.need(isinstance(ops, list) and len(ops) == len(set(ops)) and set(ops) <= OPERATIONS, 'DEVICE_OPERATION_SCOPE')
        if row['status'] != 'PASS':
            v.need(not ops, 'FAILED_DEVICE_CANNOT_SCORE')
            continue
        # PASS requires an explicitly inspected receipt, never an aggregate count.
        v.need(type(row.get('ci_job')) is int and row['ci_job'] > 0 and row.get('ci_job_conclusion') == 'success', 'DEVICE_JOB_NOT_SUCCESS')
        v.need(row.get('proof_review') == 'RAW_LOGS_HASHES_AND_OUTPUTS_INSPECTED', 'DEVICE_PROOF_REVIEW_REQUIRED')
        v.need(isinstance(row.get('evidence_files'), dict) and bool(row['evidence_files']), 'DEVICE_RAW_FILES_REQUIRED')
        for name, digest in row['evidence_files'].items():
            v.check_artifact(name, digest)
        if row['source_commit'] == scored_source:
            evidence[row['receipt_id']] = {
                'module_id': 'INTERFACE', 'tested_commit': row['source_commit'],
                'kind': 'ANDROID_EMULATOR', 'status': 'PASS', 'platform': 'ANDROID_EMULATOR',
                'url': row['ci_url'], 'artifact_sha256': row['artifact_zip_sha256'],
                'operation_ids': ops,
            }
    modules = copy.deepcopy(baseline_modules)
    if scored_source is not None:
        v.need(v.digest(scored_source, 40) and evidence, 'SCORED_SOURCE_NOT_RECEIVED')
        received = [r for r in rows if r.get('kind') == 'ANDROID_EMULATOR' and r.get('status') == 'PASS' and r.get('source_commit') == scored_source]
        v.need({r['api'] for r in received} == {29, 35}, 'ANDROID_MATRIX_NOT_RECEIVED')
        v.need(len({(r['source_tree'], r['apk_sha256'], r['test_apk_sha256'], r['ci_run'], builds[r['build_receipt_id']]['artifact_zip_sha256']) for r in received}) == 1, 'ANDROID_MATRIX_ARTIFACT_MISMATCH')
        modules['INTERFACE']['source_sha'] = scored_source
    for criterion in score.get('criteria', []):
        if criterion.get('state') == 'PASS':
            v.need(criterion.get('module_id') == 'INTERFACE' and criterion.get('operation_id') in OPERATIONS, 'SCORE_RECEIPT_SCOPE')
            v.need(all(criterion['operation_id'] in e['operation_ids'] for e in evidence.values()), 'OPERATION_NOT_RECEIVED_ON_ALL_APIS')
    points = v.check_score(score, modules, evidence)
    v.need(receipt.get('score_claims_allowed') is (points > 0), 'SCORE_RECEPTION_DECISION')
    return {
        'status': 'PASS', 'scope': 'RECEIVED_LOCAL_INTERFACE_ONLY',
        'qualified_points': points, 'scored_source': scored_source,
        'runtime_authority_granted': False, 'physical_android': 'NOT_RUN',
        'llm_generation': 'NOT_RUN', 'source_audit_lock_changed': False,
    }


def validate(directory=v.REPORTS):
    directory = Path(directory)
    return check(v.read(directory/'MISSION-51/RECEPTION.json'),
                 v.read(directory/'RECEPTION-SCORE.json'),
                 v.check_lock(v.read(directory/'BASELINE-LOCK.json')))


def graph_svg(score):
    return v.graph_svg(score).replace(
        'Nouvelle composition M51 : points non encore attribués',
        f"Nouvelle composition M51 : {score['qualified_points']}/100 points reçus")


if __name__ == '__main__':
    print(json.dumps(validate(), sort_keys=True))
