"""Owned loopback HTTPS fixture; ephemeral keys, fictitious bytes, no DNS."""
import asyncio
import hashlib
from pathlib import Path
import ssl
import subprocess
import tempfile
from . import fence
from .contracts import Plan

HOST = 'lab.synthetic.test'
DATA = b'Fictional research document. No personal data.\n'
SLOW = b'synthetic-block\n' * 8192


class TLSMaterial:
    def __init__(self, hostname=HOST):
        self.temp = tempfile.TemporaryDirectory(prefix='research-b0-tls-')
        root = Path(self.temp.name)
        commands = [
            ['req', '-x509', '-newkey', 'rsa:2048', '-nodes', '-keyout', 'ca.key',
             '-out', 'ca.pem', '-days', '1', '-subj', '/CN=B0 ephemeral laboratory CA',
             '-addext', 'basicConstraints=critical,CA:TRUE'],
            ['req', '-newkey', 'rsa:2048', '-nodes', '-keyout', 'server.key',
             '-out', 'server.csr', '-subj', '/CN=' + hostname],
            ['x509', '-req', '-in', 'server.csr', '-CA', 'ca.pem', '-CAkey', 'ca.key',
             '-CAcreateserial', '-out', 'server.pem', '-days', '1', '-extfile', 'extensions.txt'],
        ]
        (root/'extensions.txt').write_text('subjectAltName=DNS:' + hostname + '\nbasicConstraints=critical,CA:FALSE\nextendedKeyUsage=serverAuth\n')
        for command in commands:
            subprocess.run(['openssl', *command], cwd=root, check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
        for p in root.glob('*.key'):
            p.chmod(0o600)
        self.server = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.server.minimum_version = ssl.TLSVersion.TLSv1_2
        self.server.load_cert_chain(root/'server.pem', root/'server.key')
        self.client = ssl.create_default_context(cafile=str(root/'ca.pem'))
        self.client.minimum_version = ssl.TLSVersion.TLSv1_2

    def close(self):
        self.temp.cleanup()


class SyntheticServer:
    def __init__(self, tls):
        self.tls = tls
        self.server = None
        self.port = None
        self.tasks = set()
        self.requests = []
        self.first_chunk = asyncio.Event()

    async def __aenter__(self):
        self.server = await asyncio.start_server(self.handle, '127.0.0.1', 0,
                                                ssl=self.tls.server, ssl_handshake_timeout=1,
                                                limit=8192)
        self.port = self.server.sockets[0].getsockname()[1]
        if fence.ACTIVE:
            fence.ACTIVE.ports.add(self.port)
        return self

    async def __aexit__(self, *args):
        self.server.close()
        await self.server.wait_closed()
        for task in list(self.tasks):
            task.cancel()
        await asyncio.gather(*list(self.tasks), return_exceptions=True)
        if fence.ACTIVE:
            fence.ACTIVE.ports.discard(self.port)
        self.port = None

    def url(self, path='/ok'):
        return f'https://{HOST}:{self.port}{path}'

    def plan(self, path='/ok', source_id='fixture', **kwargs):
        body = SLOW if path in ('/slow', '/stream') else DATA
        return Plan(source_id, self.url(path), hashlib.sha256(body).hexdigest(), **kwargs)

    async def handle(self, reader, writer):
        task = asyncio.current_task()
        self.tasks.add(task)
        try:
            header = await asyncio.wait_for(reader.readuntil(b'\r\n\r\n'), 2)
            first = header.split(b'\r\n', 1)[0].decode('ascii')
            method, path, version = first.split(' ')
            self.requests.append(path)
            status, headers, body = '200 OK', {}, DATA
            if path == '/error':
                status = '503 Service Unavailable'
            elif path in ('/redirect', '/external', '/private', '/chain'):
                status, body = '302 Found', b''
                headers['Location'] = {'/redirect': '/ok', '/external': 'https://outside.synthetic.test/ok',
                                       '/private': 'https://127.0.0.1/ok', '/chain': '/chain'}[path]
            elif path in ('/slow', '/stream'):
                body = SLOW
            elif path == '/corrupt':
                body = b'corrupt fictional bytes'
            elif path == '/invalid-text':
                body = b'\xff\xfe'
            elif path == '/encoding':
                headers['Content-Encoding'] = 'gzip'
            elif path == '/chunked':
                headers['Transfer-Encoding'] = 'chunked'
            elif path == '/huge-header':
                headers['X-Synthetic'] = 'x' * 20000
            elif path not in ('/ok', '/stall', '/persistent', '/extra', '/incomplete', '/disconnect', '/huge'):
                status = '404 Not Found'
            length = 4194304 if path == '/huge' else len(body)
            headers.update({'Content-Length': str(length), 'Content-Type': 'text/plain', 'Connection': 'close'})
            writer.write(('HTTP/1.1 ' + status + '\r\n' + ''.join(k + ': ' + v + '\r\n' for k, v in headers.items()) + '\r\n').encode())
            await writer.drain()
            if path == '/stall':
                await asyncio.sleep(2)
            if path in ('/incomplete', '/disconnect'):
                writer.write(body[:len(body)//2])
                await writer.drain()
                if path == '/disconnect':
                    writer.transport.abort()
                return
            for start in range(0, len(body), 4096):
                writer.write(body[start:start+4096])
                await writer.drain()
                self.first_chunk.set()
                if path == '/slow':
                    await asyncio.sleep(.015)
            if path == '/extra':
                writer.write(b'undeclared-body')
                await writer.drain()
            if path == '/persistent':
                await asyncio.sleep(2)
        except (ConnectionError, asyncio.TimeoutError, asyncio.IncompleteReadError,
                asyncio.LimitOverrunError, ValueError):
            pass
        finally:
            writer.close()
            try:
                await asyncio.wait_for(writer.wait_closed(), .3)
            except (Exception, asyncio.CancelledError):
                pass
            self.tasks.discard(task)
