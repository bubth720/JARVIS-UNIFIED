"""Exact owned fixture endpoint, double answer check, pinned IP and TLS name."""
import re
import ssl
from urllib.parse import urlsplit
from .contracts import Refused
from .fixtures import HOST, SyntheticServer


class LabPolicy:
    def __init__(self, fixture, resolver=None, tls=None):
        if not isinstance(fixture, SyntheticServer) or not fixture.port or fixture.server.is_serving() is not True:
            raise Refused('OWNED_LIVE_FIXTURE_REQUIRED')
        self.fixture = fixture
        self.port = fixture.port
        self.ip = '127.0.0.1'
        self.tls = tls if tls is not None else fixture.tls.client
        if not self.tls.check_hostname or self.tls.verify_mode != ssl.CERT_REQUIRED:
            raise Refused('TLS_VERIFICATION_REQUIRED')
        self.resolver = resolver

    def validate(self, url):
        if self.ip != '127.0.0.1':
            raise Refused('PINNED_ADDRESS_CHANGED')
        if type(url) is not str or not url.isascii() or len(url) > 2048 or any(ord(c) <= 32 or ord(c) == 127 for c in url) or '\\' in url:
            raise Refused('MALFORMED_URL')
        try:
            p = urlsplit(url)
            if p.scheme != 'https' or p.username is not None or p.password is not None or p.fragment or p.query:
                raise Refused('URL_COMPONENT_REFUSED')
            if p.hostname != HOST or p.netloc != f'{HOST}:{self.port}' or p.port != self.port:
                raise Refused('DESTINATION_REFUSED')
            if not re.fullmatch(r'/[a-z-]{1,40}', p.path):
                raise Refused('PATH_REFUSED')
        except (ValueError, UnicodeError):
            raise Refused('MALFORMED_URL') from None
        if self.fixture.port != self.port or not self.fixture.server.is_serving():
            raise Refused('FIXTURE_CHANGED')
        if not self.tls.check_hostname or self.tls.verify_mode != ssl.CERT_REQUIRED:
            raise Refused('TLS_VERIFICATION_REQUIRED')
        return p.path

    async def resolve(self):
        answers = await self.resolver(HOST) if self.resolver else (self.ip,)
        if type(answers) not in (tuple, list) or not answers or any(a != self.ip for a in answers):
            raise Refused('DNS_DESTINATION_CHANGED')
        return self.ip
