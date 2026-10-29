"""Synthetic documentary lab only: no module calls, persistence or authority."""
import csv
import copy
import hashlib
import io


def document_request(name, content, request_id, session, generation):
    if (not isinstance(name, str) or not name.startswith('synthetic-')
            or not isinstance(content, str) or len(content.encode('utf-8')) > 16384
            or not isinstance(request_id, str) or not request_id
            or not isinstance(session, str) or not session
            or type(generation) is not int or not 1 <= generation <= 2**53 - 1):
        raise ValueError('synthetic input and explicit CORE candidate identity required')
    if name.endswith('.txt'):
        rows = content.splitlines()
    elif name.endswith('.csv'):
        rows = list(csv.reader(io.StringIO(content), strict=True))
    else:
        raise ValueError('TXT/CSV only')
    # Parsing is demonstrated; no invented retrieval result or model output.
    return {'request_id': request_id, 'session': session, 'generation': generation,
            'source_sha256': hashlib.sha256(content.encode('utf-8')).hexdigest(),
            'row_count': len(rows), 'status': 'UNSUPPORTED', 'citations': [],
            'synthetic': True, 'transport': 'OFF', 'write': False}


class Display:
    """Candidate consumer rejects stale identity, replay and asserted readiness."""
    def __init__(self, request):
        self.expected = copy.deepcopy(request)
        self.seen = False

    def receive(self, event):
        if (self.seen or type(event) is not dict or event.keys() != self.expected.keys()
                or any(type(event[key]) is not type(value) or event[key] != value
                       for key, value in self.expected.items())
                or event.get('status') != 'UNSUPPORTED'):
            raise ValueError('untrusted, changed, replayed or unsupported event')
        self.seen = True
        return 'LAB SYNTHETIC — UNSUPPORTED — no documentary answer; transport OFF'
