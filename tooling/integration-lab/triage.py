#!/usr/bin/env python3
"""Read-only LAB-02 triage of a genuine LAB-01 receipt (never grants runtime authority)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

STATUSES = frozenset({'PASS', 'FAIL', 'BLOCKED', 'NOT_RUN', 'UNKNOWN', 'PARTIAL'})
MODULES = frozenset({'CORE', 'LLM', 'VOICE', 'INTERFACE', 'NEXUS', 'SERVICES', 'UNIFIED', 'EVOLUTION'})
RULES = {
    'llm-manifest-guard': ('P0', 'HISTORICAL_GUARD',
        'Compare the precise manifest preimage and guard contract at the pinned LLM commit; propose a separately reviewed minimal correction. Never relax the guard.'),
    'llm-historical-guard': ('P1', 'HISTORICAL_GUARD',
        'Audit the prefusion scope changes against their original baseline; retain all historical violations and submit a minimal reviewable diff.'),
    'voice-jvm': ('P1', 'RESOURCE_QUALIFICATION',
        'Qualify the skipped public reference test only with approved licensed FP32 resources, or retain NOT_QUALIFIED. Do not use private voice data or count a skip as PASS.'),
}
FALLBACK = {
    'FAIL': ('P1', 'FAILED_COMMAND', 'Inspect the precise failing log and rerun only on a controlled branch; do not relax assertions.'),
    'BLOCKED': ('P1', 'BLOCKED_COMMAND', 'Resolve the documented prerequisite without bypassing protections; then rerun the same pinned test.'),
    'UNKNOWN': ('P1', 'UNKNOWN_EXECUTION', 'Recover an exact receipt and investigate the interruption; do not claim PASS.'),
    'NOT_RUN': ('P2', 'NOT_EXECUTED', 'Check whether the step is in scope and has an authorized environment before executing it.'),
    'PARTIAL': ('P1', 'PARTIAL_COVERAGE', 'Identify missing cases and qualify them separately; retain the partial status.'),
}

def _text(value, limit=500):
    if value is None:
        return ''
    return re.sub(r'[\x00-\x1f\x7f]+', ' ', str(value))[:limit]


def _markdown(value):
    return _text(value).replace('\\', '\\\\').replace('|', '\\|').replace('`', "'").replace('<', '&lt;').replace('>', '&gt;')


def _validated_command(item):
    if not isinstance(item, dict):
        raise ValueError('INVALID_COMMAND')
    module, ident, state = item.get('module'), item.get('id'), item.get('status')
    if module not in MODULES or not isinstance(ident, str) or not re.fullmatch('[A-Za-z0-9_-]{1,96}', ident) or state not in STATUSES:
        raise ValueError('INVALID_COMMAND_ID_MODULE_OR_STATUS')
    return module, ident, state


def _evidence(item, root):
    name, digest = item.get('log'), item.get('log_sha256')
    if not isinstance(name, str) or not isinstance(digest, str) or not re.fullmatch('[a-f0-9]{64}', digest):
        return {'status': 'NOT_CHECKED', 'reason': 'NO_VERIFIABLE_LOG_REFERENCE'}
    if root is None:
        return {'status': 'NOT_CHECKED', 'log': name, 'sha256_declared': digest}
    base = Path(root).resolve()
    candidate = base / name
    if candidate.is_symlink() or not candidate.resolve().is_relative_to(base):
        return {'status': 'INVALID', 'reason': 'UNSAFE_EVIDENCE_PATH'}
    if not candidate.is_file():
        return {'status': 'UNAVAILABLE', 'log': name}
    if candidate.stat().st_size > 16 * 1024 * 1024:
        return {'status': 'INVALID', 'reason': 'EVIDENCE_TOO_LARGE'}
    actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
    return {'status': 'VERIFIED' if actual == digest else 'MISMATCH', 'log': name, 'sha256_declared': digest, 'sha256_actual': actual}


def triage(receipt, source_sha256, evidence_root=None):
    if not isinstance(receipt, dict) or not isinstance(receipt.get('commands'), list):
        raise ValueError('INVALID_LAB_RECEIPT')
    commands = receipt['commands']
    if len(commands) > 500:
        raise ValueError('TOO_MANY_COMMANDS')
    findings, seen = [], set()
    for command in commands:
        module, ident, status = _validated_command(command)
        identity = (module, ident)
        if identity in seen:
            raise ValueError('DUPLICATE_COMMAND')
        seen.add(identity)
        if status == 'PASS':
            continue
        if ident in RULES and (ident.startswith('llm-') and module == 'LLM' or ident == 'voice-jvm' and module == 'VOICE'):
            priority, classification, next_action = RULES[ident]
        else:
            priority, classification, next_action = FALLBACK[status]
        # A skip is a missing qualification, not a failing synthesis inference.
        if module == 'VOICE' and status == 'FAIL' and command.get('skipped', 0) and command.get('failures', 1) == 0:
            priority, classification = 'P1', 'RESOURCE_QUALIFICATION'
        findings.append({'module': module, 'command': ident, 'status': status,
                         'classification': classification, 'priority': priority,
                         'reason': _text(command.get('reason') or 'NO_TYPED_REASON'),
                         'commit': _text(command.get('commit') or 'UNKNOWN', 48),
                         'next_action': next_action,
                         'evidence': _evidence(command, evidence_root)})
    android = receipt.get('android_safe', receipt.get('android', {}))
    if not isinstance(android, dict):
        raise ValueError('INVALID_ANDROID_STATUS')
    if android.get('status') != 'PASS':
        findings.append({'module': 'INTERFACE', 'command': 'android-qualification',
                         'status': android.get('status', 'UNKNOWN'),
                         'classification': 'ANDROID_NOT_QUALIFIED', 'priority': 'P0',
                         'reason': _text(android.get('reason') or 'NO_VALID_ANDROID_RECEIPT'),
                         'commit': 'UNKNOWN',
                         'next_action': 'Admit a stable, explicitly authorized Android emulator; perform API29/35 baseline first, then candidate. Do not install on personal devices.',
                         'evidence': {'status': 'NOT_CHECKED', 'reason': 'NO_ANDROID_EXECUTION_PROOF'}})
    if receipt.get('runtime_integration_proven') is False:
        findings.append({'module': 'UNIFIED', 'command': 'runtime-integration',
                         'status': 'NOT_RUN', 'classification': 'INTEGRATION_UNPROVEN',
                         'priority': 'P1', 'reason': 'NO_PRODUCT_RUNTIME_CONNECTION_QUALIFIED',
                         'commit': 'UNKNOWN',
                         'next_action': 'Qualify one read-only contract connection using real implementations, separate from CORE/LLM authority gates.',
                         'evidence': {'status': 'NOT_CHECKED', 'reason': 'NO_RUNTIME_PROOF'}})
    findings.sort(key=lambda row: ({'P0': 0, 'P1': 1, 'P2': 2}[row['priority']], row['module'], row['command']))
    result = {'schema': 'jarvis.integration-lab.triage/1',
              'source_sha256': source_sha256,
              'source_campaign_status': receipt.get('campaign_status', receipt.get('status', 'UNKNOWN')),
              'status': 'ACTION_REQUIRED' if findings else 'NO_RECORDED_BLOCKER_NOT_A_GO',
              'source_run_id': receipt.get('run_id'),
              'source_commit': receipt.get('source_commit'),
              'runtime_authority_granted': False, 'product_qualified': False,
              'finding_count': len(findings), 'findings': findings}
    return result


def markdown(result):
    parts = ['# JARVIS — LAB-02 Read-only triage', '',
             'Source receipt SHA256: `' + result['source_sha256'] + '`',
             'Campaign status: **' + _markdown(result['source_campaign_status']) + '**',
             'Result: **' + result['status'] + '**', '',
             'This is a recommendation from recorded evidence, not a new test, a correction, or authorization. No module is granted GO.', '',
             '| Priority | Module | Step | Observed | Diagnosis | Evidence |',
             '|---|---|---|---|---|---|']
    for row in result['findings']:
        parts.append('| ' + ' | '.join(_markdown(v) for v in [row['priority'], row['module'], row['command'], row['status'], row['classification'], row['evidence']['status']]) + ' |')
    parts.extend(['', '## Short independent next missions', ''])
    for row in result['findings']:
        parts.extend(['### ' + row['priority'] + ' — ' + row['module'] + ' / ' + row['command'],
                      'Observed: `' + row['status'] + '` · commit `' + _markdown(row['commit']) + '` · reason: ' + _markdown(row['reason']),
                      'Action: ' + row['next_action'],
                      'Acceptance: same-step evidence at an exact commit, failure retained until retested; no implicit merge, installation, acquisition, or gate opening.', ''])
    return '\n'.join(parts)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--evidence-root')
    args = parser.parse_args(argv)
    source = Path(args.receipt)
    if source.stat().st_size > 10 * 1024 * 1024:
        raise ValueError('RECEIPT_TOO_LARGE')
    data = source.read_bytes()
    report = triage(json.loads(data), hashlib.sha256(data).hexdigest(), args.evidence_root)
    output = Path(args.output).resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError('NONEMPTY_OUTPUT_DIRECTORY')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'TRIAGE.json').write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    (output / 'TRIAGE.md').write_text(markdown(report), encoding='utf-8')
    print(json.dumps({'status': report['status'], 'findings': report['finding_count'], 'output': str(output)}))
    return 0  # The triage generator succeeded; original FAIL status is unchanged in the report.

if __name__ == '__main__':
    raise SystemExit(main())
