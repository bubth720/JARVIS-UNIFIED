"""Offline review of a GPU experiment proposal. Contains no cloud or model execution path."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[2]


def natural(value):
    if type(value) is not int or value < 0:
        raise ValueError('NONNEGATIVE_INTEGER_REQUIRED')
    return value


def estimated_cents(rate_microeur_per_hour, duration_seconds, billing_quantum_seconds, shutdown_seconds):
    rate, duration, quantum, shutdown = map(natural, (rate_microeur_per_hour, duration_seconds, billing_quantum_seconds, shutdown_seconds))
    if not quantum or not duration:
        raise ValueError('POSITIVE_DURATION_AND_QUANTUM_REQUIRED')
    billed = ((duration + shutdown + quantum - 1) // quantum) * quantum
    # Integer ceiling: 1 cent = 10,000 micro-EUR; 1 hour = 3,600 seconds.
    return (rate * billed + 36_000_000 - 1) // 36_000_000


def fits_budget(policy, committed_compute, committed_ancillary, task_compute, task_ancillary):
    values = list(map(natural, (committed_compute, committed_ancillary, task_compute, task_ancillary)))
    compute, ancillary = values[0] + values[2], values[1] + values[3]
    cap, reserve = natural(policy['monthly_cap_cents']), natural(policy['reserve_cents'])
    if cap >= 5000 or not reserve:
        raise ValueError('STRICT_SUB_50_EUR_CAP_AND_RESERVE_REQUIRED')
    return (compute <= natural(policy['compute_cap_cents']) and ancillary <= natural(policy['ancillary_cap_cents'])
            and compute + ancillary + reserve <= cap)


def score_reply(case, reply):
    oracle = case['oracle']
    if oracle['kind'] == 'json_exact':
        try:
            parsed = json.loads(reply)
        except (ValueError, TypeError):
            return False
        # Canonical JSON distinguishes true from 1, unlike Python's equality for those values.
        return json.dumps(parsed, sort_keys=True, ensure_ascii=False) == json.dumps(oracle['expected'], sort_keys=True, ensure_ascii=False)
    if oracle['kind'] == 'exact_text':
        def normal(text): return ' '.join(unicodedata.normalize('NFC', text).split()).casefold()
        return isinstance(reply, str) and normal(reply) == normal(oracle['expected'])
    raise ValueError('UNKNOWN_ORACLE')


def validate_cases(rows):
    if len(rows) != 100:
        raise ValueError('EXPECTED_100_CALIBRATION_CASES')
    ids, prompts = set(), set()
    for case in rows:
        identity = hashlib.sha256(json.dumps([case['history'], case['prompt']], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        if case['id'] in ids or identity in prompts:
            raise ValueError('DUPLICATE_CASE')
        ids.add(case['id']); prompts.add(identity)
        if case['provenance'] != 'synthetic' or case['split'] != 'calibration_public' or not case['prompt'].strip():
            raise ValueError('SYNTHETIC_PUBLIC_CALIBRATION_ONLY')
        if case['oracle']['kind'] not in {'exact_text', 'json_exact'}:
            raise ValueError('UNKNOWN_ORACLE')
        if case['oracle']['kind'] == 'exact_text' and not isinstance(case['oracle']['expected'], str):
            raise ValueError('TEXT_ORACLE_REQUIRES_TEXT')
        for turn in case['history']:
            if turn['role'] not in {'user', 'assistant'} or not isinstance(turn['content'], str):
                raise ValueError('INVALID_HISTORY')
    counts = dict(Counter(r['category'] for r in rows))
    if counts != {'arithmetic': 30, 'logic': 10, 'factual': 10, 'structured': 10, 'documents': 20, 'context': 10, 'security': 10}:
        raise ValueError('COVERAGE_CHANGED')
    return counts


def review(manifest_path):
    manifest = json.loads(Path(manifest_path).read_text())
    if manifest['launch_authorized'] is not False or manifest['provisioning_enabled'] is not False:
        raise ValueError('PREPARATION_MUST_NOT_AUTHORIZE_EXECUTION')
    corpus = ROOT / manifest['dataset']['path']
    raw = corpus.read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest['dataset']['sha256']:
        raise ValueError('CORPUS_HASH_MISMATCH')
    rows = [json.loads(line) for line in raw.decode().splitlines()]
    counts = validate_cases(rows)
    if {m['parameters_billion'] for m in manifest['models']} != {0.6, 1.7}:
        raise ValueError('ONLY_PLANNED_06B_AND_17B_MODELS')
    for model in manifest['models']:
        digest = model['sha256']
        if len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('MODEL_DIGEST_REQUIRED')
    if not fits_budget(manifest['budget'], 0, 0, 0, 0):
        raise ValueError('INVALID_BUDGET')
    return {'status': 'READY_FOR_REVIEW', 'gpu_execution': 'NOT_AUTHORIZED', 'cases': len(rows),
            'categories': counts, 'dataset_sha256': manifest['dataset']['sha256'],
            'model_weights_downloaded': False, 'inference_executed': False,
            'limitations': ['Public calibration set; no blind holdout supplied', 'No live provider quote or shutdown qualification',
                            'Model outputs do not qualify Android memory, UI, voice or energy']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=ROOT / 'docs/gpu-forge/g03/campaign.json')
    args = parser.parse_args()
    print(json.dumps(review(args.manifest), ensure_ascii=False, indent=2))
