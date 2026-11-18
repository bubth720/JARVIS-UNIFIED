"""Laboratory-only types; none is a production v1 carrier or CORE permission."""
from dataclasses import asdict, dataclass
import hashlib
import json
import math
import re


class Refused(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


@dataclass(frozen=True)
class Limits:
    requests: int = 12
    document_bytes: int = 262144
    mission_bytes: int = 1048576
    connections: int = 1
    timeout_seconds: float = 2.0
    duration_seconds: float = 30.0
    depth: int = 2
    temporary_bytes: int = 524288
    redirects: int = 3
    header_bytes: int = 8192
    chunk_bytes: int = 4096
    events: int = 128

    def __post_init__(self):
        caps = dict(requests=100, document_bytes=4194304, mission_bytes=16777216,
                    connections=4, depth=5, temporary_bytes=16777216,
                    redirects=5, header_bytes=16384, chunk_bytes=65536, events=1024)
        for name, cap in caps.items():
            value = getattr(self, name)
            minimum = 0 if name in ('depth', 'redirects') else 1
            if type(value) is not int or not minimum <= value <= cap:
                raise Refused('INVALID_LIMIT_' + name.upper())
        for name, cap in [('timeout_seconds', 10), ('duration_seconds', 120)]:
            value = getattr(self, name)
            if type(value) not in (int, float) or not math.isfinite(value) or not 0 < value <= cap:
                raise Refused('INVALID_LIMIT_' + name.upper())

    @classmethod
    def profile(cls, name):
        if name == 'android':
            return cls()
        if name == 'mini-pc':
            return cls(connections=2, document_bytes=1048576, mission_bytes=4194304,
                       temporary_bytes=2097152)
        raise Refused('UNKNOWN_PROFILE')


@dataclass(frozen=True)
class Plan:
    source_id: str
    url: str
    sha256: str
    content_type: str = 'text/plain'
    depth: int = 0

    def __post_init__(self):
        if not isinstance(self.source_id, str) or not re.fullmatch(r'[a-z][a-z0-9_-]{0,39}', self.source_id):
            raise Refused('INVALID_SOURCE_ID')
        if not isinstance(self.url, str) or len(self.url) > 2048:
            raise Refused('INVALID_URL')
        if not isinstance(self.sha256, str) or not re.fullmatch('[0-9a-f]{64}', self.sha256):
            raise Refused('EXPECTED_HASH_REQUIRED')
        if self.content_type not in ('text/plain', 'application/octet-stream'):
            raise Refused('UNREVIEWED_CONTENT_TYPE')
        if type(self.depth) is not int or self.depth < 0:
            raise Refused('INVALID_DEPTH')

    @property
    def key(self):
        return digest(asdict(self))
