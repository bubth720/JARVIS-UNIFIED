"""Verify preserved-source receipts without changing historical gates or scores."""
import hashlib
import json
from pathlib import Path
import subprocess

from tooling.v1.validate import InvalidEvidence, need, read

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'reports/reuse-first-r1plus'
BASE = 'a7625a31513be5c56fa36ed946fbdcd3c23c2a15'
ADDITIONS = ('reports/reuse-first-r1plus/', 'tooling/reuse_r1plus/')
WORKFLOWS = {'.github/workflows/reuse-r1plus-baselines.yml', '.github/workflows/reuse-r1plus-coordination.yml'}


def preservation():
    historical = subprocess.check_output(['git', 'ls-tree', '-r', BASE], cwd=ROOT, text=True).splitlines()
    names = set()
    for line in historical:
        meta, name = line.split('\t', 1)
        names.add(name)
        p = ROOT / name
        mode, kind, blob = meta.split()
        need(kind == 'blob' and p.is_file() and not p.is_symlink(), 'HISTORICAL_FILE_MISSING:' + name)
        actual = subprocess.check_output(['git', 'hash-object', '--', name], cwd=ROOT, text=True).strip()
        need(actual == blob, 'HISTORICAL_CONTENT_CHANGED:' + name)
        need(bool(p.stat().st_mode & 0o111) == (mode == '100755'), 'HISTORICAL_MODE_CHANGED:' + name)
    files = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    for name in files:
        need(name in names or name in WORKFLOWS or name.startswith(ADDITIONS), 'UNDECLARED_ADDITION:' + name)
    return len(historical)


def check(receipt, evidence_root=REPORT):
    need(receipt.get('schema') == 'jarvis.reuse.reception/1', 'SCHEMA')
    need(receipt.get('scope') == 'DOCUMENTARY_ONLY', 'DOCUMENTARY_SCOPE')
    for key in ('can_activate', 'productive_connection', 'android_qualified', 'real_llm_qualified', 'vertical_integrated'):
        need(receipt.get(key) is False, 'UNSUPPORTED_PROMOTION:' + key)
    need(receipt.get('historical_coordination_base') == BASE, 'HISTORICAL_BASE')
    manifest = read(evidence_root / 'EVIDENCE-SHA256.json')
    for name, expected in manifest.items():
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts, 'EVIDENCE_PATH')
        path = evidence_root / p
        need(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'EVIDENCE_HASH:' + name)
    inventory = read(evidence_root / 'INVENTORY.json')
    inventory_sources = {r['module']: r['audit_commit'] for r in inventory['repositories']}
    rows = receipt.get('modules', [])
    need(len(rows) == 8 and {m.get('module') for m in rows} == set(inventory_sources), 'MODULE_SET')
    for row in rows:
        mid = row['module']
        need(row.get('status') in {'PASS', 'FAIL', 'SKIP', 'BLOCKED', 'NON_QUALIFIE'}, 'STATUS')
        need(row.get('scope') == 'HOST_TESTS_ONLY', 'HOST_SCOPE')
        need(row.get('runtime_qualified') is False, 'RUNTIME_PROMOTION')
        ev = read(evidence_root / row['evidence']) if row.get('evidence') else None
        source = row.get('tested_source')
        if mid in {'CORE', 'VOICE', 'SERVICES', 'EVOLUTION'}:
            need(source == inventory_sources[mid] == ev['source'] == ev['expected_source'], 'SOURCE_BINDING')
            stats = {k: sum(s[k] for s in ev['junit']) for k in ('tests', 'failures', 'errors', 'skipped')}
            need(stats == row['junit'] and stats['tests'] > 0, 'JUNIT_COUNTS')
            need(row['passed'] == stats['tests'] - stats['skipped'] - stats['failures'] - stats['errors'], 'PASS_COUNTS')
            need(not stats['failures'] and not stats['errors'], 'BASELINE_FAILURE')
        elif mid == 'LLM':
            need(source == inventory_sources[mid] == ev['commit'], 'LLM_SOURCE')
            need(ev['audit_verdict'] == row['safety_verdict'] == 'NO_GO', 'LLM_NO_GO_HIDDEN')
            need(ev['patch_applied'] is False and ev['jni_loaded'] is False and ev['weights_acquired'] is False, 'LLM_STATE')
        elif mid == 'NEXUS':
            need(source == ev['source_commit'] and row['junit'] == ev['junit'], 'NEXUS_BINDING')
            need(ev['production_connected'] is False and row['test_source_set_only'] is True, 'NEXUS_PROMOTION')
        elif mid == 'INTERFACE':
            need(source == ev['source_commit'], 'UI_BUILD_BINDING')
            need(row['android_status'] == 'BLOCKED' and row['device_tests_after_fix'] == 'NOT_RUN', 'ANDROID_BUILD_PROMOTION')
        else:
            need(source == BASE and row['runtime_qualified'] is False, 'COORDINATION_SOURCE')
    for api in (29, 35):
        raw = read(evidence_root / f'evidence/C1-api{api}-RECEPTION.json')
        need(raw['android_qualified'] is False and raw['source_commit'] == receipt['campaign_source'], 'CAMPAIGN_PROMOTION')
    review = read(evidence_root / 'evidence/C1-api29-offline-review.json')
    need(receipt['api29_raw_preflight_accepted'] is False, 'CONTRADICTORY_PREFLIGHT')
    need(receipt['campaign_run'] == '42524234101' and receipt['campaign_attempt'] == 1, 'CAMPAIGN_ID')
    return {'status': 'PASS_DOCUMENTARY_CHECK_ONLY', 'can_activate': False, 'module_receipts': len(rows), 'hashed_files': len(manifest)}


def main():
    result = check(read(REPORT / 'RECEIPT.json'))
    result['historical_files_preserved'] = preservation()
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
