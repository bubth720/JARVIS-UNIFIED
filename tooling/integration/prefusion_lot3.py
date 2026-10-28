"""Synthetic, fail-closed document transcript reviewer. No runtime adapter."""
import argparse
import hashlib
import json
from pathlib import Path
from uuid import UUID


class TranscriptError(ValueError):
    pass


def review(value):
    fields = {'format', 'origin', 'runtime_enabled', 'source', 'session', 'request',
              'epoch', 'generation', 'events'}
    if type(value) is not dict or set(value) != fields:
        raise TranscriptError('closed transcript fields required')
    if (value['format'] != 'jarvis.prefusion.lot3.transcript/1' or
            value['origin'] != 'LABORATORY' or value['runtime_enabled'] is not False):
        raise TranscriptError('laboratory only')
    for key in ('session', 'request', 'epoch'):
        try:
            if str(UUID(value[key])) != value[key]:
                raise ValueError()
        except (ValueError, TypeError, AttributeError):
            raise TranscriptError('canonical correlation required') from None
    if type(value['generation']) is not int or not 1 <= value['generation'] <= 2**53 - 1:
        raise TranscriptError('invalid generation')
    source = value['source']
    if type(source) is not dict or set(source) != {'kind', 'text', 'sha256'}:
        raise TranscriptError('closed source required')
    if type(source['kind']) is not str or source['kind'] not in ('TXT', 'CSV') or type(source['text']) is not str:
        raise TranscriptError('invalid source')
    try:
        raw = source['text'].encode('utf-8')
    except UnicodeError:
        raise TranscriptError('invalid UTF-8') from None
    if not 1 <= len(raw) <= 2048 or hashlib.sha256(raw).hexdigest() != source['sha256']:
        raise TranscriptError('source integrity or size')
    events = value['events']
    expected = [('CORE', 'SUBMITTED'), ('CORE', 'ACK_UNTRUSTED'),
                ('NEXUS', 'UNSUPPORTED'), ('INTERFACE', 'DISPLAY_UNAVAILABLE')]
    if type(events) is not list or len(events) != len(expected):
        raise TranscriptError('incomplete transcript')
    for seq, (event, (module, state)) in enumerate(zip(events, expected), 1):
        fields = {'sequence', 'module', 'state', 'session', 'request', 'epoch', 'generation'}
        if type(event) is not dict or set(event) != fields:
            raise TranscriptError('closed event required; no fabricated response or citation')
        if type(event['sequence']) is not int or event['sequence'] != seq:
            raise TranscriptError('replay or sequence gap')
        if event['module'] != module or event['state'] != state:
            raise TranscriptError('unsupported routing or positive readiness')
        if any(type(event[k]) is not type(value[k]) or event[k] != value[k]
               for k in ('session', 'request', 'epoch', 'generation')):
            raise TranscriptError('stale or foreign event')
    return {'status': 'UNSUPPORTED', 'display': 'UNAVAILABLE', 'trusted': False,
            'runtime_link_enabled': False, 'mutation_performed': False,
            'source_sha256': source['sha256'], 'review_only': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('transcript', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(review(json.loads(args.transcript.read_text(encoding='utf-8'))), indent=2))
        return 0
    except (TranscriptError, OSError, UnicodeError, ValueError):
        print('REJECTED: invalid laboratory transcript')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
