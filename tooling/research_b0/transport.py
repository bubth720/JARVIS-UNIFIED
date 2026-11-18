"""Asynchronous bounded HTTPS to an owned fixture, never Internet research."""
import asyncio
import codecs
from dataclasses import dataclass
import hashlib
import os
import socket
import ssl
import time
from urllib.parse import urljoin
import uuid
from .contracts import Refused


@dataclass(frozen=True, eq=False)
class LabPermit:
    """Opaque in-memory fixture authority; not serializable CORE authorization."""
    plan_key: str
    generation: int
    expires: float


class LabResearch:
    def __init__(self, policy, ledger, *, enabled=False):
        self.policy, self.ledger = policy, ledger
        self.enabled = enabled is True
        self.generation = 0
        self.permits = set()
        self.consumed = set()
        self.tasks = set()
        self.connection_attempts = 0
        self.requested_stop = None

    def enable_lab(self):
        self.enabled = True

    def approve(self, plan):
        if not self.enabled:
            raise Refused('LAB_DISABLED')
        self.policy.validate(plan.url)
        if plan.depth > self.ledger.limits.depth:
            raise Refused('DEPTH_QUOTA')
        self.ledger.remaining_time()
        permit = LabPermit(plan.key, self.generation, time.monotonic() + self.ledger.limits.duration_seconds)
        self.ledger.event('APPROVED')
        self.permits.add(permit)
        return permit

    def check(self, plan, permit):
        if not self.enabled or not isinstance(permit, LabPermit) or permit not in self.permits:
            raise Refused('LAB_AUTHORITY_REQUIRED')
        if permit.plan_key != plan.key or permit.generation != self.generation or time.monotonic() >= permit.expires:
            raise Refused('STALE_OR_WRONG_PERMIT')
        if plan.depth > self.ledger.limits.depth:
            raise Refused('DEPTH_QUOTA')
        self.ledger.remaining_time()

    def start(self, plan, permit):
        self.check(plan, permit)
        task = asyncio.create_task(self._download(plan, permit))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return task

    async def stop(self, *, pause=False):
        self.requested_stop = 'PAUSED' if pause else 'CANCELLED'
        self.generation += 1
        self.permits.clear()
        tasks = list(self.tasks)
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        if self.ledger.snapshot()['state'] == 'COMPLETED':
            self.ledger.event('STOP_AFTER_COMPLETION', strict=False)
            return dict(state='COMPLETED', stop_observed=True, documents_preserved=self.ledger.document_count())
        self.ledger.state(self.requested_stop)
        self.ledger.event(self.requested_stop, strict=False)
        return dict(state=self.requested_stop, stop_observed=True, documents_preserved=self.ledger.document_count())

    async def _download(self, plan, permit):
        self.check(plan, permit)
        if permit in self.consumed:
            raise Refused('PERMIT_ALREADY_USED')
        self.consumed.add(permit)
        self.requested_stop = None
        cached = self.ledger.cached(plan)
        if cached is not None:
            self.policy.validate(cached['final_url'])
            self.ledger.event('CACHE_VERIFIED')
            self.ledger.state('COMPLETED')
            return cached
        self.ledger.enter()
        part = self.ledger.root/'tmp'/(uuid.uuid4().hex + '.part')
        reserved = 0
        try:
            self.ledger.event('STARTED')
            limit = min(self.ledger.limits.timeout_seconds, self.ledger.remaining_time())
            async with asyncio.timeout(limit):
                url = plan.url
                visited = set()
                for hops in range(self.ledger.limits.redirects + 1):
                    self.check(plan, permit)
                    path = self.policy.validate(url)
                    if url in visited:
                        raise Refused('REDIRECT_CYCLE')
                    visited.add(url)
                    await self.policy.resolve()
                    # A changed answer cannot influence the pinned connection.
                    ip = await self.policy.resolve()
                    self.policy.validate(url)
                    self.check(plan, permit)
                    self.ledger.request()
                    self.connection_attempts += 1
                    reader, writer = await asyncio.open_connection(
                        ip, self.policy.port, family=socket.AF_INET, ssl=self.policy.tls,
                        server_hostname='lab.synthetic.test', limit=self.ledger.limits.header_bytes,
                        ssl_handshake_timeout=limit, ssl_shutdown_timeout=.2)
                    try:
                        if writer.get_extra_info('peername')[:2] != (ip, self.policy.port):
                            raise Refused('PEER_CHANGED')
                        writer.write((f'GET {path} HTTP/1.1\r\nHost: lab.synthetic.test:{self.policy.port}\r\nConnection: close\r\nAccept-Encoding: identity\r\n\r\n').encode('ascii'))
                        await writer.drain()
                        try:
                            raw = await reader.readuntil(b'\r\n\r\n')
                        except (asyncio.LimitOverrunError, asyncio.IncompleteReadError):
                            raise Refused('INVALID_OR_OVERSIZED_HEADER') from None
                        if len(raw) > self.ledger.limits.header_bytes:
                            raise Refused('HEADER_QUOTA')
                        status, headers = self.parse_header(raw)
                        if 300 <= status < 400:
                            if status not in (301, 302, 303, 307, 308) or 'location' not in headers:
                                raise Refused('INVALID_REDIRECT')
                            if hops == self.ledger.limits.redirects:
                                raise Refused('REDIRECT_QUOTA')
                            target = urljoin(url, headers['location'])
                            self.policy.validate(target)
                            self.ledger.event('REDIRECT')
                            url = target
                            continue
                        if status != 200:
                            raise Refused('HTTP_' + str(status))
                        if 'transfer-encoding' in headers or headers.get('content-encoding', 'identity') != 'identity':
                            raise Refused('ENCODING_REFUSED')
                        length = headers.get('content-length', '')
                        if not length.isascii() or not length.isdecimal() or len(length) > 10:
                            raise Refused('CONTENT_LENGTH_REQUIRED')
                        length = int(length)
                        if length > self.ledger.limits.document_bytes:
                            raise Refused('DOCUMENT_QUOTA')
                        if headers.get('content-type', '').split(';')[0] != plan.content_type:
                            raise Refused('CONTENT_TYPE_MISMATCH')
                        h = hashlib.sha256()
                        decoder = codecs.getincrementaldecoder('utf-8')() if plan.content_type == 'text/plain' else None
                        received = 0
                        with part.open('xb') as output:
                            while received < length:
                                self.check(plan, permit)
                                left = self.ledger.snapshot()
                                allowance = min(self.ledger.limits.chunk_bytes, length-received,
                                                max(1, self.ledger.limits.mission_bytes-left['received']+1),
                                                max(1, self.ledger.limits.temporary_bytes-left['temporary']+1))
                                chunk = await reader.read(allowance)
                                if not chunk:
                                    raise Refused('TRUNCATED_RESPONSE')
                                self.check(plan, permit)
                                code = self.ledger.charge(len(chunk))
                                reserved += len(chunk)
                                if code:
                                    raise Refused(code)
                                received += len(chunk)
                                h.update(chunk)
                                if decoder:
                                    decoder.decode(chunk)
                                output.write(chunk)
                            if decoder:
                                decoder.decode(b'', final=True)
                            tail = await reader.read(1)
                            if tail:
                                self.ledger.charge(len(tail))
                                reserved += len(tail)
                                raise Refused('EXCESS_BODY')
                            output.flush()
                            os.fsync(output.fileno())
                        if h.hexdigest() != plan.sha256:
                            raise Refused('HASH_MISMATCH')
                        self.check(plan, permit)
                        self.ledger.event('VALIDATED')
                        metadata = dict(format='jarvis.research-b0-document/1', document_id=plan.key,
                            source_id=plan.source_id, origin_url=plan.url, final_url=url,
                            retrieved_at='2030-01-01T00:00:00Z', date_kind='SIMULATED',
                            content_type=plan.content_type, size_bytes=received, sha256=h.hexdigest(),
                            validation='VERIFIED_SYNTHETIC', transformations=[dict(operation='identity-stream-copy',
                            tool='research-b0/1', input_sha256=h.hexdigest(), output_sha256=h.hexdigest())])
                        # Bounded synchronous commit in this test worker: cancellation
                        # cannot interleave the authority check and publication.
                        result = self.ledger.publish(part, plan, metadata)
                        self.ledger.state('COMPLETED')
                        return result
                    finally:
                        writer.close()
                        try:
                            await asyncio.wait_for(writer.wait_closed(), .3)
                        except (Exception, asyncio.CancelledError):
                            pass
                raise Refused('REDIRECT_QUOTA')
        except asyncio.CancelledError:
            self.ledger.state(self.requested_stop or 'INTERRUPTED')
            raise
        except (TimeoutError, ssl.SSLError, ConnectionError, OSError, UnicodeError, Refused) as error:
            self.ledger.state('FAILED')
            code = error.code if isinstance(error, Refused) else (
                'TIMEOUT' if isinstance(error, TimeoutError) else 'TLS_REFUSED' if isinstance(error, ssl.SSLError)
                else 'INVALID_TEXT' if isinstance(error, UnicodeError) else 'TRANSPORT_IO')
            self.ledger.event('FAILED', code, strict=False)
            raise Refused(code) from None
        finally:
            if part.exists():
                part.unlink()
            self.ledger.release(reserved)
            self.ledger.leave()

    @staticmethod
    def parse_header(raw):
        try:
            lines = raw.decode('ascii').split('\r\n')
            version, code, reason = lines[0].split(' ', 2)
            if version != 'HTTP/1.1' or len(code) != 3 or not code.isdecimal():
                raise ValueError()
            headers = {}
            for line in lines[1:-2]:
                key, value = line.split(':', 1)
                if not key or not all(c.isalnum() or c == '-' for c in key) or key.lower() in headers or any(ord(c) < 32 for c in value):
                    raise ValueError()
                headers[key.lower()] = value.strip()
            return int(code), headers
        except (ValueError, UnicodeError):
            raise Refused('INVALID_HTTP_HEADER') from None
