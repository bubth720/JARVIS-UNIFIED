"""Private synthetic ledger; restart-safe counters and content-addressed copies.

No production database is opened. The exclusive owner lock prevents recovery
while another laboratory process can still publish. Files never carry authority.
"""
from contextlib import contextmanager
from dataclasses import asdict
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import stat
import time
import uuid
from .contracts import Refused

MARKER = 'jarvis.research-b0-private-store/1\n'


def file_hash(path):
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, 'rb') as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise Refused('NON_REGULAR_OBJECT')
            h = hashlib.sha256()
            for chunk in iter(lambda: source.read(65536), b''):
                h.update(chunk)
            return h.hexdigest()
    except OSError:
        raise Refused('UNSAFE_OR_MISSING_OBJECT') from None


class Ledger:
    def __init__(self, root, limits):
        self.root = Path(root).absolute()
        if any(p.is_symlink() for p in [self.root, *self.root.parents]):
            raise Refused('STORE_SYMLINK')
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        marker = self.root/'B0-ONLY'
        if list(self.root.iterdir()) and (marker.is_symlink() or not marker.is_file() or marker.read_text() != MARKER):
            raise Refused('UNOWNED_STORE')
        if not marker.exists():
            marker.write_text(MARKER)
        self.root.chmod(0o700)
        self.limits = limits
        self.lock = os.open(self.root/'owner.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(self.lock)
            self.lock = None
            raise Refused('STORE_OWNER_ACTIVE') from None
        try:
            for name in ('tmp', 'objects'):
                p = self.root/name
                if p.is_symlink():
                    raise Refused('STORE_SYMLINK')
                p.mkdir(exist_ok=True, mode=0o700)
            self.db = self.root/'ledger.sqlite'
            if self.db.is_symlink():
                raise Refused('STORE_SYMLINK')
            with self.connection() as c:
                c.executescript('''
                  CREATE TABLE IF NOT EXISTS mission(id TEXT PRIMARY KEY, limits TEXT NOT NULL,
                    created REAL NOT NULL, requests INTEGER NOT NULL, received INTEGER NOT NULL,
                    temporary INTEGER NOT NULL, active INTEGER NOT NULL, state TEXT NOT NULL);
                  CREATE TABLE IF NOT EXISTS documents(id TEXT PRIMARY KEY, metadata TEXT NOT NULL);
                  CREATE TABLE IF NOT EXISTS events(sequence INTEGER PRIMARY KEY, event TEXT NOT NULL, code TEXT NOT NULL);
                ''')
                row = c.execute('SELECT * FROM mission').fetchone()
                config = json.dumps(asdict(limits), sort_keys=True)
                if row is None:
                    c.execute('INSERT INTO mission VALUES(?,?,?,0,0,0,0,?)', (uuid.uuid4().hex, config, time.time(), 'READY'))
                elif row['limits'] != config:
                    raise Refused('RESUME_LIMITS_CHANGED')
                elif any(type(row[k]) is not int or row[k] < 0 for k in ('requests', 'received', 'temporary', 'active')):
                    raise Refused('CORRUPT_LEDGER')
                # A new exclusive owner may clean only its own uncommitted parts.
                for p in (self.root/'tmp').iterdir():
                    if p.is_symlink() or not p.is_file() or not re.fullmatch(r'[0-9a-f]{32}\.part', p.name):
                        raise Refused('UNSAFE_TEMPORARY_FILE')
                    p.unlink()
                c.execute("UPDATE mission SET temporary=0, active=0, state=CASE WHEN state='RUNNING' THEN 'INTERRUPTED' ELSE state END")
            self.db.chmod(0o600)
        except BaseException:
            self.close()
            raise

    @contextmanager
    def connection(self):
        if self.lock is None:
            raise Refused('STORE_CLOSED')
        c = sqlite3.connect(self.db, timeout=1)
        c.row_factory = sqlite3.Row
        try:
            c.execute('BEGIN IMMEDIATE')
            yield c
            c.commit()
        except BaseException:
            c.rollback()
            raise
        finally:
            c.close()

    def close(self):
        if self.lock is not None:
            os.close(self.lock)
            self.lock = None

    def snapshot(self):
        with self.connection() as c:
            row = dict(c.execute('SELECT * FROM mission').fetchone())
        row.pop('limits')
        return row

    def event(self, name, code='', *, strict=True):
        with self.connection() as c:
            if c.execute('SELECT count(*) FROM events').fetchone()[0] >= self.limits.events:
                if strict:raise Refused('EVENT_QUOTA')
                return False
            c.execute('INSERT INTO events(event,code) VALUES(?,?)', (name, code))
        return True

    def state(self, value):
        with self.connection() as c:
            if value in ('COMPLETED', 'FAILED') and c.execute('SELECT active FROM mission').fetchone()[0] > 1:
                value = 'RUNNING'
            c.execute('UPDATE mission SET state=?', (value,))

    def remaining_time(self):
        age = time.time() - self.snapshot()['created']
        if age < 0 or age >= self.limits.duration_seconds:
            raise Refused('MISSION_DEADLINE')
        return self.limits.duration_seconds - age

    def enter(self):
        self.remaining_time()
        with self.connection() as c:
            m = c.execute('SELECT * FROM mission').fetchone()
            if m['active'] >= self.limits.connections:
                raise Refused('CONNECTION_QUOTA')
            if m['received'] >= self.limits.mission_bytes:
                raise Refused('MISSION_BYTES')
            if shutil.disk_usage(self.root).free < min(self.limits.document_bytes, self.limits.temporary_bytes):
                raise Refused('DISK_CAPACITY')
            c.execute("UPDATE mission SET active=active+1, state='RUNNING'")

    def leave(self):
        with self.connection() as c:
            c.execute('UPDATE mission SET active=active-1 WHERE active>0')

    def request(self):
        with self.connection() as c:
            row = c.execute('SELECT requests FROM mission').fetchone()
            if row[0] >= self.limits.requests:
                raise Refused('REQUEST_QUOTA')
            c.execute('UPDATE mission SET requests=requests+1')

    def charge(self, size):
        with self.connection() as c:
            c.execute('UPDATE mission SET received=received+?, temporary=temporary+?', (size, size))
            row = c.execute('SELECT received,temporary FROM mission').fetchone()
        if row['received'] > self.limits.mission_bytes:
            return 'MISSION_BYTES'
        if row['temporary'] > self.limits.temporary_bytes:
            return 'TEMPORARY_QUOTA'
        return None

    def release(self, size):
        with self.connection() as c:
            c.execute('UPDATE mission SET temporary=temporary-? WHERE temporary>=?', (size, size))

    def cached(self, plan):
        with self.connection() as c:
            row = c.execute('SELECT metadata FROM documents WHERE id=?', (plan.key,)).fetchone()
        if row is None:
            return None
        data = json.loads(row[0])
        path = self.root/'objects'/plan.sha256
        if (set(data) != {'format','document_id','source_id','origin_url','final_url','retrieved_at',
                         'date_kind','content_type','size_bytes','sha256','validation','transformations'} or
                data.get('format') != 'jarvis.research-b0-document/1' or
                data.get('source_id') != plan.source_id or data.get('origin_url') != plan.url or
                data.get('date_kind') != 'SIMULATED' or data.get('retrieved_at') != '2030-01-01T00:00:00Z' or
                data.get('content_type') != plan.content_type or
                type(data.get('size_bytes')) is not int or not 0 <= data['size_bytes'] <= self.limits.document_bytes or
                data.get('document_id') != plan.key or data.get('sha256') != plan.sha256 or
                data.get('validation') != 'VERIFIED_SYNTHETIC' or
                data.get('transformations') != [dict(operation='identity-stream-copy', tool='research-b0/1',
                     input_sha256=plan.sha256, output_sha256=plan.sha256)] or
                path.is_symlink() or not path.is_file() or path.stat().st_size != data.get('size_bytes') or
                file_hash(path) != plan.sha256):
            raise Refused('CACHE_INTEGRITY')
        return data

    def publish(self, part, plan, metadata):
        if file_hash(part) != plan.sha256:
            raise Refused('HASH_MISMATCH')
        target = self.root/'objects'/plan.sha256
        try:
            os.link(part, target, follow_symlinks=False)
        except FileExistsError:
            if file_hash(target) != plan.sha256:
                raise Refused('ORIGINAL_CONFLICT')
        with self.connection() as c:
            c.execute('INSERT OR IGNORE INTO documents VALUES(?,?)', (plan.key, json.dumps(metadata, sort_keys=True)))
        return self.cached(plan)

    def document_count(self):
        with self.connection() as c:
            return c.execute('SELECT count(*) FROM documents').fetchone()[0]
