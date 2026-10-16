#!/usr/bin/env python3
"""Read-only GitHub observations; stdlib only. No API writes or remote Git writes."""
from __future__ import annotations
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import uuid

REPOSITORIES = tuple('bubth720/' + name for name in (
    'JAVIS-Local-v2', 'JARVIS-LLM', 'JARVIS-VOICE', 'JARVIS-INTERFACE',
    'JARVIS-INTERFACE-', 'JARVIS-NEXUS', 'JARVIS-VOLUTION-', 'JARVIS-SERVICES', 'JARVIS-UNIFIED'))
STATES = {'success', 'failure', 'pending', 'unknown', 'not_checked'}
PHASES = {'proposed', 'in_progress', 'completed', 'blocked', 'unknown'}
SHA = re.compile(r'[0-9a-f]{40}')
MAX_BYTES = 4 * 1024 * 1024
MAX_PAGES = 10
API = 'https://api.github.com'


class RegistryError(Exception):
    pass


class ReadError(RegistryError):
    def __init__(self, reason, http_status=None):
        super().__init__(reason)
        self.reason, self.http_status = reason, http_status


def need(condition, message):
    if not condition:
        raise RegistryError(message)


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dumps(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result


def loads(data):
    try:
        return json.loads(data, object_pairs_hook=no_duplicates,
                          parse_constant=lambda _: (_ for _ in ()).throw(RegistryError('Non-finite JSON')))
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise RegistryError('Invalid JSON') from exc


def read_json(path):
    need(path.is_file() and not path.is_symlink() and path.stat().st_size <= MAX_BYTES, 'Missing/oversized or linked JSON file')
    return loads(path.read_bytes())


def branch_name(value):
    need(isinstance(value, str) and 0 < len(value) <= 200 and not value.startswith(('-', '/', '.'))
         and not value.endswith(('/', '.', '.lock')) and '..' not in value and '@{' not in value
         and not any(c.isspace() or ord(c) < 32 or c in '~^:?*[\\' for c in value)
         and '//' not in value, 'Invalid branch name')


def result(status, reason=None, **fields):
    need(status in STATES, 'Invalid observation status')
    return {'status': status, 'reason': reason, **fields}


def timestamp(value):
    try:
        need(isinstance(value, str) and datetime.fromisoformat(value).utcoffset().total_seconds() == 0, 'UTC timestamp required')
    except (ValueError, AttributeError) as exc:
        raise RegistryError('UTC timestamp required') from exc


def validate(modules, missions):
    for doc, key in [(modules, 'modules'), (missions, 'missions')]:
        need(isinstance(doc, dict) and doc.get('schema_version') == 1 and type(doc['schema_version']) is int, 'Unsupported schema')
        need(isinstance(doc.get('generation'), str) and isinstance(doc.get(key), list), 'Invalid registry root')
    need(modules['generation'] == missions['generation'], 'Mixed generations: restore a complete saved snapshot')
    repos = [m.get('repository') for m in modules['modules']]
    need(len(repos) == len(REPOSITORIES) and set(repos) == set(REPOSITORIES), 'Exactly the nine requested repositories must be preserved')
    ids = set()
    for entry in modules['modules'] + missions['missions']:
        need(isinstance(entry, dict) and entry.get('repository') in REPOSITORIES, 'Unknown repository')
        branch_name(entry.get('reference_branch') if 'reference_branch' in entry else entry.get('branch'))
        need(isinstance(entry.get('manual'), dict), 'Missing manual fields')
        manual = entry['manual']
        need(manual.get('phase') in PHASES and isinstance(manual.get('blockers'), list)
             and isinstance(manual.get('decisions'), list) and isinstance(manual.get('next_action'), str), 'Invalid manual state')
        need(all(isinstance(text, str) for text in manual['blockers'] + manual['decisions']), 'Manual decisions/blockers must be text')
        need(entry.get('state') in STATES, 'Invalid entry state')
        commit = entry.get('last_verified_commit')
        if commit is not None:
            need(isinstance(commit, dict) and SHA.fullmatch(commit.get('sha', '')) is not None, 'Invalid verified commit')
            need(commit.get('source') in {'git', 'api', 'demo', 'local_git'}, 'Missing commit source')
            timestamp(commit.get('verified_at'))
        if entry.get('verified_at') is not None:
            timestamp(entry['verified_at'])
        observation = entry.get('observation')
        if observation is not None:
            need(isinstance(observation, dict) and observation.get('source') in {'api', 'git', 'demo'}, 'Invalid observation')
            timestamp(observation.get('checked_at'))
            need(isinstance(observation.get('evidence_id'), str), 'Missing evidence ID')
            for key in ['repository', 'branch', 'ci', 'pull_requests']:
                need(isinstance(observation.get(key), dict) and observation[key].get('status') in STATES, 'Invalid observation component')
    for entry in missions['missions']:
        need(isinstance(entry.get('id'), str) and re.fullmatch(r'[A-Za-z0-9._-]+', entry['id']) and entry['id'] not in ids, 'Duplicate/invalid mission ID')
        ids.add(entry['id'])
    return True


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        # Never forward authentication or silently rename a repository.
        raise ReadError('redirect_refused', code)


class GitHub:
    source = 'api'

    def __init__(self, token_env=None, opener=None):
        need(token_env in (None, 'GH_TOKEN', 'GITHUB_TOKEN'), 'Unsupported token variable name')
        self.token_env = token_env
        self.opener = opener or urllib.request.build_opener(NoRedirect())
        self.cache = {}
        self.evidence = []

    def _read(self, path, token=None):
        need(path.startswith('/repos/') and not path.startswith('//') and '#' not in path, 'Unexpected API endpoint')
        headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'jarvis-central-registry/1', 'X-GitHub-Api-Version': '2022-11-28'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        request = urllib.request.Request(API + path, headers=headers, method='GET')
        try:
            with self.opener.open(request, timeout=15) as response:
                body = response.read(MAX_BYTES + 1)
                need(len(body) <= MAX_BYTES, 'API response too large')
                need(response.geturl().startswith(API + '/repos/'), 'Unexpected response host')
                # Response headers/body (which could contain sensitive content) are not logged.
                return loads(body)
        except urllib.error.HTTPError as exc:
            raise ReadError('http_' + str(exc.code), exc.code) from None
        except (urllib.error.URLError, TimeoutError, OSError):
            raise ReadError('network_unavailable') from None

    def get(self, path):
        if path in self.cache:
            value = self.cache[path]
            if isinstance(value, ReadError):
                raise value
            return copy.deepcopy(value)
        authenticated = False
        try:
            try:
                value = self._read(path)
            except ReadError as exc:
                # Explicit opt-in, only after anonymous HTTP auth/rate refusal.
                # Proxy connection errors never trigger token usage.
                token = os.environ.get(self.token_env) if self.token_env and exc.http_status in (401, 403, 429) else None
                if not token:
                    raise
                authenticated = True
                value = self._read(path, token)
            self.cache[path] = copy.deepcopy(value)
            self.evidence.append({'method': 'GET', 'url': API + path, 'status': 'success', 'authenticated_retry': authenticated, 'response_sha256': digest(dumps(value))})
            return value
        except ReadError as exc:
            self.cache[path] = exc
            self.evidence.append({'method': 'GET', 'url': API + path, 'status': 'failure', 'reason': exc.reason, 'http_status': exc.http_status, 'authenticated_retry': authenticated})
            raise
        except RegistryError:
            exc = ReadError('invalid_api_response')
            self.cache[path] = exc
            self.evidence.append({'method': 'GET', 'url': API + path, 'status': 'failure', 'reason': exc.reason, 'authenticated_retry': authenticated})
            raise exc from None

    def pages(self, path, key=None):
        items = []
        for page in range(1, MAX_PAGES + 1):
            separator = '&' if '?' in path else '?'
            data = self.get(path + separator + 'per_page=100&page=' + str(page))
            values = data.get(key) if key and isinstance(data, dict) else data
            need(isinstance(values, list), 'Invalid paginated API response')
            items.extend(values)
            if len(values) < 100:
                return items
        raise ReadError('pagination_limit')


class Demo(GitHub):
    source = 'demo'

    def __init__(self, path):
        super().__init__()
        document = read_json(path)
        need(document.get('synthetic') is True and isinstance(document.get('responses'), dict), 'Synthetic demo marker required')
        self.responses = document['responses']

    def _read(self, path, token=None):
        # No URL opener, Git command or credentials in demo mode.
        entry = self.responses.get(path)
        if entry is None:
            raise ReadError('demo_endpoint_not_provided')
        if entry.get('http_status') != 200:
            raise ReadError('http_' + str(entry['http_status']), entry['http_status'])
        return copy.deepcopy(entry['body'])


def repository_path(repo):
    need(repo in REPOSITORIES, 'Repository is outside the exact requested allowlist')
    return '/repos/' + repo


def safe_url(url):
    if isinstance(url, str) and url.startswith('https://github.com/') and '\n' not in url and '\r' not in url:
        return url
    return None


def action_summary(runs, sha):
    # Exact SHA only, latest run/attempt for each workflow+event. Older green
    # runs cannot conceal a more recent red run of the same workflow/event.
    latest = {}
    for run in runs:
        if run.get('head_sha') != sha:
            continue
        key = (run.get('workflow_id'), run.get('event'))
        previous = latest.get(key)
        order = (run.get('run_number', 0), run.get('run_attempt', 1), run.get('id', 0))
        if previous is None or order > previous[0]:
            latest[key] = (order, run)
    selected = []
    for _, run in latest.values():
        state, conclusion = run.get('status'), run.get('conclusion')
        status = 'pending' if state in {'queued', 'in_progress', 'waiting', 'requested', 'pending'} else (
            'success' if state == 'completed' and conclusion == 'success' else
            'failure' if state == 'completed' and conclusion in {'failure', 'cancelled', 'timed_out', 'action_required', 'startup_failure', 'stale'} else 'unknown')
        selected.append({'id': run['id'], 'workflow_id': run.get('workflow_id'), 'event': run.get('event'),
                         'head_sha': sha, 'run_number': run.get('run_number'), 'run_attempt': run.get('run_attempt', 1),
                         'status': status, 'github_status': state, 'conclusion': conclusion, 'url': safe_url(run.get('html_url'))})
    selected.sort(key=lambda item: item['id'])
    states = {run['status'] for run in selected}
    status = 'failure' if 'failure' in states else 'pending' if 'pending' in states else 'unknown' if not selected or 'unknown' in states else 'success'
    return result(status, 'no_actions_runs_for_sha' if not selected else 'observed_actions_workflows_only', runs=selected, scope='exact_sha_actions_only', required_workflows_known=False, tests_count=None)


def observe_api(client, repo, branch):
    base = repository_path(repo)
    observation = {
        'repository': result('not_checked'), 'branch': result('not_checked'),
        'ci': result('not_checked'), 'pull_requests': result('not_checked'),
    }
    try:
        metadata = client.get(base)
        need(metadata.get('full_name') == repo, 'Remote identity changed; no automatic rename')
        observation['repository'] = result('success', url=safe_url(metadata.get('html_url')), default_branch=metadata.get('default_branch'))
    except ReadError as exc:
        observation['repository'] = result('failure', 'inaccessible_or_missing' if exc.http_status == 404 else exc.reason, http_status=exc.http_status)
        return observation
    except (RegistryError, AttributeError, TypeError):
        observation['repository'] = result('unknown', 'invalid_repository_metadata')
        return observation
    try:
        data = client.get(base + '/branches/' + urllib.parse.quote(branch, safe=''))
        sha = data['commit']['sha']
        need(data.get('name') == branch and isinstance(sha, str) and SHA.fullmatch(sha), 'Invalid branch data')
        observation['branch'] = result('success', name=branch, sha=sha, url=f'https://github.com/{repo}/tree/' + urllib.parse.quote(branch, safe=''))
    except ReadError as exc:
        observation['branch'] = result('failure', 'branch_not_found' if exc.http_status == 404 else exc.reason, http_status=exc.http_status)
    except (RegistryError, KeyError, TypeError, AttributeError):
        observation['branch'] = result('unknown', 'invalid_branch_response')
    # PRs remain useful even when a historical branch has been removed.
    try:
        pulls = client.pages(base + '/pulls?state=all&head=' + urllib.parse.quote(repo.split('/')[0] + ':' + branch, safe=''))
        records = {}
        for pull in pulls:
            if pull.get('head', {}).get('ref') != branch or pull.get('head', {}).get('repo', {}).get('full_name') != repo:
                continue
            records[pull['number']] = {'number': pull['number'], 'state': pull.get('state'), 'draft': pull.get('draft'),
                                     'merged_at': pull.get('merged_at'), 'head_sha': pull['head'].get('sha'),
                                     'base_branch': pull.get('base', {}).get('ref'), 'url': safe_url(pull.get('html_url'))}
        observation['pull_requests'] = result('success', items=sorted(records.values(), key=lambda item: item['number']), scope='same_repository_head_branch')
    except ReadError as exc:
        observation['pull_requests'] = result('unknown', exc.reason, items=[])
    except (RegistryError, KeyError, AttributeError, TypeError):
        observation['pull_requests'] = result('unknown', 'invalid_pr_response', items=[])
    if observation['branch']['status'] == 'success':
        try:
            runs = client.pages(base + '/actions/runs?head_sha=' + sha, 'workflow_runs')
            observation['ci'] = action_summary(runs, sha)
        except ReadError as exc:
            observation['ci'] = result('unknown', exc.reason, runs=[])
        except (RegistryError, KeyError, TypeError, AttributeError):
            observation['ci'] = result('unknown', 'invalid_actions_response', runs=[])
    return observation


class GitRefs:
    source = 'git'

    def __init__(self):
        self.cache, self.evidence = {}, []

    def observe(self, repo, branch):
        repository_path(repo); branch_name(branch)
        if repo not in self.cache:
            url = 'https://github.com/' + repo + '.git'
            try:
                # Fixed, read-only Git operation, no fetch/checkout/push/remote changes.
                command = ['git', '-c', 'credential.interactive=false', 'ls-remote', '--symref', url, 'HEAD', 'refs/heads/*']
                process = subprocess.run(command, capture_output=True, text=True, timeout=30,
                                         env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'})
                need(len(process.stdout.encode()) <= MAX_BYTES, 'Git response too large')
                if process.returncode:
                    self.cache[repo] = None
                    self.evidence.append({'method': 'git ls-remote', 'url': url, 'status': 'failure', 'reason': 'git_read_failed', 'exit_code': process.returncode})
                else:
                    refs, default = {}, None
                    for line in process.stdout.splitlines():
                        value, name = line.split('\t', 1)
                        if name == 'HEAD' and value.startswith('ref: refs/heads/'):
                            default = value[len('ref: refs/heads/'):]
                        elif name.startswith('refs/heads/'):
                            need(SHA.fullmatch(value) is not None, 'Invalid Git SHA')
                            refs[name[len('refs/heads/'):]] = value
                    self.cache[repo] = (refs, default)
                    self.evidence.append({'method': 'git ls-remote', 'url': url, 'status': 'success', 'default_branch': default, 'branches': refs})
            except (OSError, subprocess.TimeoutExpired, RegistryError, ValueError):
                self.cache[repo] = None
                self.evidence.append({'method': 'git ls-remote', 'url': url, 'status': 'failure', 'reason': 'git_unavailable_or_invalid'})
        data = self.cache[repo]
        observation = {'repository': result('failure', 'git_read_failed'), 'branch': result('not_checked'),
                       'ci': result('not_checked', 'git_does_not_expose_ci'),
                       'pull_requests': result('not_checked', 'git_does_not_expose_prs')}
        if data is not None:
            refs, default = data
            observation['repository'] = result('success', default_branch=default)
            observation['branch'] = result('success', name=branch, sha=refs[branch]) if branch in refs else result('failure', 'branch_not_advertised_by_git')
        return observation


def update(modules, missions, client, checked_at=None, generation=None):
    validate(modules, missions)
    modules, missions = copy.deepcopy(modules), copy.deepcopy(missions)
    checked_at, generation = checked_at or now(), generation or uuid.uuid4().hex
    timestamp(checked_at)
    cache = {}
    for entry in modules['modules'] + missions['missions']:
        repo = entry['repository']
        branch = entry.get('reference_branch', entry.get('branch'))
        key = (repo, branch)
        if key not in cache:
            if isinstance(client, GitRefs):
                cache[key] = client.observe(repo, branch)
            else:
                cache[key] = observe_api(client, repo, branch)
        observation = copy.deepcopy(cache[key])
        observation.update(source=client.source, checked_at=checked_at, evidence_id=generation)
        entry['observation'] = observation
        branch_observation = observation['branch']
        entry['state'] = branch_observation['status'] if observation['repository']['status'] == 'success' else 'unknown'
        entry['checked_at'] = checked_at
        if branch_observation['status'] == 'success':
            entry['last_verified_commit'] = {'sha': branch_observation['sha'], 'branch': branch, 'verified_at': checked_at, 'source': client.source, 'scope': 'remote_branch' if client.source != 'demo' else 'synthetic', 'evidence_id': generation}
            entry['verified_at'] = checked_at
        # Failed/not-checked attempts preserve the historical verified commit,
        # its timestamp and the entirety of user-managed manual data.
    for doc in [modules, missions]:
        doc['generation'] = generation
    validate(modules, missions)
    return modules, missions


def md(value):
    return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', ' ').replace('\r', ' ').replace('`', '&#96;')


def summary(modules, missions):
    validate(modules, missions)
    sources = sorted({e['observation']['source'] for e in modules['modules'] if e.get('observation')})
    lines = ['# Registre central JARVIS', '', 'Génération : ' + modules['generation'] + '. Sources : ' + ', '.join(sources) + '.', '',
             '**success désigne une observation réussie, pas une mission terminée ni une application validée.**', '',
             'Une valeur conservée après un échec est historique ; vérifier checked_at, verified_at et les preuves.', '',
             '| Dépôt | Branche de référence | État observation | Dernier SHA vérifié (source) | CI courante | Phase manuelle |', '|---|---|---|---|---|---|']
    for entry in modules['modules']:
        commit, obs = entry.get('last_verified_commit'), entry.get('observation') or {}
        text = commit['sha'] + ' (' + commit['source'] + ')' if commit else 'unknown'
        lines.append('| ' + ' | '.join(md(v) for v in [entry['repository'], entry['reference_branch'], entry['state'], text, obs.get('ci', {}).get('status', 'not_checked'), entry['manual']['phase']]) + ' |')
    lines += ['', '## Missions', '', '| ID | Dépôt / branche | SHA distant vérifié | Observation / CI | Phase manuelle | Blocages manuels | Prochaine action |', '|---|---|---|---|---|---|---|']
    for entry in missions['missions']:
        ci = (entry.get('observation') or {}).get('ci', {}).get('status', 'not_checked')
        commit = entry.get('last_verified_commit')
        lines.append('| ' + ' | '.join(md(v) for v in [entry['id'], entry['repository'] + ' / ' + entry['branch'], commit['sha'] if commit else 'unknown (voir preuves locales)', entry['state'] + ' / ' + ci, entry['manual']['phase'], '; '.join(entry['manual']['blockers']) or 'aucun renseigné', entry['manual']['next_action']]) + ' |')
    lines += ['', '## Limites', '', '- Les états manuels, décisions et preuves locales ne sont jamais remplacés par GitHub.',
              '- CI : GitHub Actions au SHA exact, derniers essais par workflow/événement ; pas de certification des tests ni de lecture des logs.',
              '- PR : recherche limitée aux branches du même dépôt ; pas de découverte de missions ou branches automatique.',
              '- Mode git : PR/CI not_checked. Mode demo : données synthétiques, aucune preuve GitHub réelle.', '']
    return '\n'.join(lines)


def publish_local(output, modules, missions, evidence):
    """Local artifacts only. Immutable snapshot first, then checked working copies."""
    output.mkdir(parents=True, exist_ok=True)
    need(not output.is_symlink(), 'Linked output directory forbidden')
    lock = output / '.update.lock'
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise RegistryError('Update lock exists: another writer or interrupted update; review before removing') from exc
    try:
        os.close(fd)
        generation = modules['generation']
        need(re.fullmatch(r'[0-9a-f]{32}', generation), 'Invalid snapshot ID')
        directory = output / 'evidence' / generation
        directory.mkdir(parents=True, exist_ok=False)
        files = {'modules.json': dumps(modules), 'missions.json': dumps(missions),
                 'evidence.json': dumps({'schema_version': 1, 'generation': generation,
                                        'checked_at': modules['modules'][0].get('checked_at'),
                                        'collector_sha256': digest(Path(__file__).read_bytes()), 'observations': evidence}),
                 'SUMMARY.md': summary(modules, missions).encode('utf-8')}
        for name, data in files.items():
            with (directory / name).open('xb') as stream:
                stream.write(data); stream.flush(); os.fsync(stream.fileno())
        for name in ['modules.json', 'missions.json', 'SUMMARY.md']:
            fd, temp_name = tempfile.mkstemp(prefix='.registry-', dir=output)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(files[name]); stream.flush(); os.fsync(stream.fileno())
            os.replace(temp_name, output / name)
        return directory
    finally:
        lock.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--registry-dir', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--mode', choices=['api', 'git', 'demo'], default='api')
    parser.add_argument('--demo-file', type=Path)
    parser.add_argument('--token-env', choices=['GH_TOKEN', 'GITHUB_TOKEN'], help='Optional retry only after anonymous HTTP 401/403/429; token is never saved')
    parser.add_argument('--validate-only', action='store_true')
    args = parser.parse_args(argv)
    try:
        root = args.registry_dir.resolve()
        modules, missions = read_json(root / 'modules.json'), read_json(root / 'missions.json')
        validate(modules, missions)
        if args.validate_only:
            print('Registre valide : ' + str(len(modules['modules'])) + ' dépôts, ' + str(len(missions['missions'])) + ' missions.')
            return 0
        output = args.output_dir.resolve() if args.output_dir else root
        if args.mode == 'demo':
            need(output != root and args.output_dir is not None, 'Demo requires a separate --output-dir; real registry will not be overwritten')
            need(args.token_env is None, 'Demo must not use credentials')
            client = Demo(args.demo_file or root / 'demo' / 'github.json')
        elif args.mode == 'git':
            need(args.token_env is None, 'Git uses the existing HTTPS proxy; no API token required')
            client = GitRefs()
        else:
            client = GitHub(args.token_env)
        updated_modules, updated_missions = update(modules, missions, client)
        snapshot = publish_local(output, updated_modules, updated_missions, client.evidence)
        print(summary(updated_modules, updated_missions))
        print('Snapshot local : ' + str(snapshot))
        complete = all(e['state'] == 'success' and (args.mode != 'api' or all(e['observation'][k]['status'] != 'unknown' for k in ['pull_requests', 'ci'])) for e in updated_modules['modules'] + updated_missions['missions'])
        # 2 = partial observations saved, not a clean all-success network run.
        return 0 if complete else 2
    except (RegistryError, OSError, KeyError, TypeError, ValueError) as exc:
        print('Échec local : ' + (str(exc) if isinstance(exc, RegistryError) else type(exc).__name__), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
