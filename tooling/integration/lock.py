"""Validate an immutable candidate BOM without running any repository's code.

Git evidence authenticates local objects, not the remote identity or hardware.
Network observations are dated declarations, checked separately from local hashes.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from scripts.contracts import validate as validate_schema_value
from tooling.contracts.manifest import strict_json
from tooling.campaign.status import EvidenceGateEvaluator

ROOT = Path(__file__).resolve().parents[2]
REPOSITORIES = {name: 'bubth720/' + repo for name, repo in {
    'core': 'JAVIS-Local-v2', 'llm': 'JARVIS-LLM', 'voice': 'JARVIS-VOICE',
    'interface': 'JARVIS-INTERFACE', 'nexus': 'JARVIS-NEXUS',
    'services': 'JARVIS-SERVICES', 'evolution': 'JARVIS-VOLUTION-',
    'unified': 'JARVIS-UNIFIED'}.items()}
PLATFORMS = {'android24', 'android25', 'android26', 'android29_arm64', 'linux'}
CONTRACTS = {f'contracts/v1/{n}.schema.json' for n in (
    'request-envelope', 'response-envelope', 'resource-lease', 'health-status', 'capability-manifest')}
MAX_BYTES = 2 * 1024 * 1024
GATE_OWNERS = {
    'F1': {'core', 'nexus', 'services'}, 'F2': {'core', 'nexus', 'services'},
    'F3': {'core', 'llm'}, 'F4': {'core', 'interface'},
    'F5': {'core', 'llm', 'voice', 'interface'}, 'F6': {'core', 'nexus', 'services'},
    'F7': {'core', 'evolution'}, 'F8': set(REPOSITORIES),
}


class LockError(ValueError):
    pass


def load(path):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise LockError('Input exceeds 2 MiB')
    return strict_json(path.read_text(encoding='utf-8'))


def safe_path(path):
    EvidenceGateEvaluator.safe_path(path)
    if any(p in {'', '.'} for p in path.split('/')) or path.startswith('-'):
        raise LockError('Unsafe source path')
    return path


def waves(gates):
    pending = {g['id']: set(g['depends_on']) for g in gates}
    done, result = set(), []
    while pending:
        ready = sorted(k for k, deps in pending.items() if deps <= done)
        if not ready:
            raise LockError('Dependency cycle')
        result.append(ready)
        for k in ready:
            del pending[k]
            done.add(k)
    return result


def validate(lock):
    validate_schema_value(lock, load(Path(__file__).with_name('lock.schema.json')))
    components = lock['components']
    if {c['id'] for c in components} != set(REPOSITORIES):
        raise LockError('Exactly eight unique owners required')
    for c in components:
        if c['repository'] != REPOSITORIES[c['id']]:
            raise LockError('Repository identity mismatch')
        if c['owner'] != c['id']:
            raise LockError('One declared owner per resource domain')
        if {p['target'] for p in c['platforms']} != PLATFORMS:
            raise LockError('Unique complete platform matrix required')
        commits, branches = set(), set()
        for ref in [c['primary'], *c['alternatives']]:
            if ref['commit'] in commits or ref['branch'] in branches:
                raise LockError('Duplicate reference')
            commits.add(ref['commit']); branches.add(ref['branch'])
            # git-check-ref-format rules for the bounded branch-only subset used here.
            b = ref['branch']
            if not re.fullmatch(r'[A-Za-z0-9._/-]+', b) or '..' in b or b.endswith(('/', '.')) or any(
                    not p or p.startswith('.') or p.endswith('.lock') for p in b.split('/')):
                raise LockError('Unsafe branch name')
            if len(set(ref['parents'])) != len(ref['parents']) or ref['commit'] in ref['parents']:
                raise LockError('Invalid commit parents')
            paths = [safe_path(f['path']) for f in ref['files']]
            if len(paths) != len(set(paths)):
                raise LockError('Duplicate evidence path')
        if c['ci']['status'] in {'success', 'failure', 'pending'}:
            url = c['ci']['url']
            if c['ci']['commit'] != c['primary']['commit'] or not re.fullmatch(
                    re.escape('https://github.com/' + c['repository'] + '/actions/runs/') + r'[0-9]+', url):
                raise LockError('CI must bind the selected SHA and exact repository run')
        if c['license']['status'] == 'UNKNOWN' and c['license']['expression'] != 'UNKNOWN':
            raise LockError('Unknown license cannot invent an SPDX identifier')
    ids = [g['id'] for g in lock['gates']]
    if set(ids) != {f'F{i}' for i in range(9)} or len(ids) != len(set(ids)):
        raise LockError('Unique F0-F8 gates required')
    gate_by_id = {g['id']: g for g in lock['gates']}
    for g in lock['gates']:
        if set(g['depends_on']) - set(ids) or g['id'] in g['depends_on']:
            raise LockError('Unknown/self dependency')
        if g['id'] != 'F0' and 'F0' not in ancestors(g['id'], gate_by_id):
            raise LockError('F0 inventory must precede every integration gate')
        if g['status'] == 'VERIFIED':
            if g['blockers'] or any(gate_by_id[d]['status'] != 'VERIFIED' for d in g['depends_on']):
                raise LockError('Verified gate has blockers or unverified dependencies')
            if g['id'] != 'F0' and any(c['ci']['status'] != 'success' for c in components
                                      if c['id'] in GATE_OWNERS[g['id']]):
                raise LockError('No integrated GO with missing/failed selected CI')
        elif g['status'] == 'BLOCKED' and not g['blockers']:
            raise LockError('Blocked gate needs a reason')
    waves(lock['gates'])
    conflicts = lock['conflicts']
    if len({c['id'] for c in conflicts}) != len(conflicts):
        raise LockError('Duplicate conflict ID')
    for conflict in conflicts:
        if not set(conflict['components']) <= set(REPOSITORIES):
            raise LockError('Unknown conflict owner')
        if any(gate_by_id[gate]['status'] == 'VERIFIED' for gate in conflict['blocks']):
            raise LockError('Candidate conflicts cannot silently become integrated GO')
    if {f['path'] for f in lock['frozen_contracts']} != CONTRACTS:
        raise LockError('Exactly five frozen v1 schemas required')
    return lock


def ancestors(identifier, by_id, visiting=None):
    visiting = set() if visiting is None else visiting
    if identifier in visiting:
        raise LockError('Dependency cycle')
    if identifier not in by_id:
        raise LockError('Unknown dependency')
    result = set()
    for dep in by_id[identifier]['depends_on']:
        result.add(dep)
        result.update(ancestors(dep, by_id, visiting | {identifier}))
    return result


def git(path, *args):
    try:
        # Fixed Git readers only. No shell, hooks, checkout, fetch, build or patch execution.
        # Partial-clone readers must not lazily fetch objects or modify their source repository.
        env = dict(os.environ, GIT_NO_LAZY_FETCH='1', GIT_ALLOW_PROTOCOL='', GIT_OPTIONAL_LOCKS='0')
        return subprocess.check_output(['git', '--no-replace-objects', '-C', str(path), *args],
                                       stderr=subprocess.PIPE, timeout=20, env=env)
    except (OSError, subprocess.SubprocessError) as exc:
        raise LockError('Git evidence inaccessible') from exc


def verify_sources(lock, repositories, root=ROOT):
    validate(lock)
    if set(repositories) != set(REPOSITORIES.values()):
        raise LockError('Explicit paths for all eight repositories required')
    references, files = 0, 0
    for c in lock['components']:
        path = repositories[c['repository']]
        for ref in [c['primary'], *c['alternatives']]:
            commit = ref['commit']
            if git(path, 'rev-parse', commit + '^{commit}').decode().strip() != commit:
                raise LockError('Wrong Git object type')
            parents = git(path, 'show', '-s', '--format=%P', commit).decode().split()
            if parents != ref['parents']:
                raise LockError('Commit parent mismatch: ' + c['id'])
            for item in ref['files']:
                file = safe_path(item['path'])
                spec = commit + ':' + file
                if int(git(path, 'cat-file', '-s', spec)) > MAX_BYTES:
                    raise LockError('Evidence blob exceeds limit')
                mode = git(path, 'ls-tree', commit, '--', file).split(b' ', 1)[0]
                if mode not in {b'100644', b'100755'}:
                    raise LockError('Evidence must be a regular tracked file')
                if hashlib.sha256(git(path, 'show', spec)).hexdigest() != item['sha256']:
                    raise LockError('Source fingerprint mismatch: ' + c['id'] + '/' + file)
                files += 1
            references += 1
    for item in lock['frozen_contracts']:
        # Fixed allowlist prevents traversal, arbitrary file reads or replacement of schema scope.
        if hashlib.sha256((Path(root) / item['path']).read_bytes()).hexdigest() != item['sha256']:
            raise LockError('Frozen contract changed')
    return {'mode': 'local_git_objects', 'references': references, 'source_files': files,
            'frozen_contracts': 5, 'remote_ci_reexecuted': False, 'hardware_qualified': False}


def plan(lock):
    validate(lock)
    by_id = {g['id']: g for g in lock['gates']}
    return [{'id': g['id'], 'status': g['status'], 'waiting_for': [d for d in g['depends_on']
             if by_id[d]['status'] != 'VERIFIED'], 'blockers': g['blockers']}
            for wave in waves(lock['gates']) for g in [by_id[k] for k in wave]]


def compare(before, after):
    validate(before); validate(after)
    old = {c['id']: c for c in before['components']}
    return [{'component': c['id'], 'before': old[c['id']]['primary']['commit'],
             'after': c['primary']['commit'], 'ci_before': old[c['id']]['ci']['status'],
             'ci_after': c['ci']['status']}
            for c in after['components'] if c['primary']['commit'] != old[c['id']]['primary']['commit']
            or c['ci'] != old[c['id']]['ci']]


def markdown(lock):
    validate(lock)
    def cell(s): return str(s).replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;')
    lines = ['# FUSION-01 — composition candidate, non intégrée', '',
             'Observation : ' + lock['observed_at'] + '. Contrôle documentaire, jamais autorisation runtime.', '',
             '| Module | SHA sélectionné | CI exacte | android24 | android25 | android26 | android29 ARM64 | Linux |',
             '|---|---|---|---|---|---|---|---|']
    for c in lock['components']:
        platforms = {p['target']: p['status'] for p in c['platforms']}
        lines.append('| ' + ' | '.join(map(cell, [c['id'], c['primary']['commit'], c['ci']['status'],
            *[platforms[k] for k in ['android24','android25','android26','android29_arm64','linux']]])) + ' |')
    lines += ['', 'SUPPORTED décrit seulement la surface logicielle indiquée dans le verrou, pas un appareil qualifié.', '',
              '| Phase | État | Dépendances non vérifiées | Blocages |', '|---|---|---|---|']
    for g in plan(lock):
        lines.append('| ' + ' | '.join(map(cell, [g['id'], g['status'], ', '.join(g['waiting_for']), '; '.join(g['blockers'])])) + ' |')
    lines += ['', '## Conflits à porter, sans fusion automatique', '']
    for c in lock['conflicts']:
        lines += ['- ' + cell(c['id']) + ' (' + ', '.join(c['blocks']) + ') : ' + cell(c['reason']) + ' Action : ' + cell(c['required_action'])]
    return '\n'.join(lines) + '\n'
