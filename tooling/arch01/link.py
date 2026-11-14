"""PC ↔ Android link contract (JARVIS MOBILE ↔ JARVIS CENTRAL). Messages and validation rules only.

NO network transport exists in this package: the only transport is an in-memory loopback for tests, and
constructing anything else is refused. The real transport (LAN only, mutually authenticated, encrypted,
no cloud relay, no automatic discovery) belongs to a separate, explicitly authorised mission and to a
SEPARATE Android variant: the local Android variant keeps no network permission (ARCHITECTURE.md).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple

PROTOCOL = (2, 0)                 # major, minor; v1 envelopes stay valid inside CORE, the link speaks v2
MAX_BODY_BYTES = 64 * 1024        # a text chunk / request; documents travel by reference, never inline
MAX_REMAINING_MS = 300_000
NETWORK_TRANSPORT_ENABLED = False # architectural guard: flipped only by a future authorised mission


class Kind(Enum):
    HELLO = "hello"                       # versions, role, pairing proof reference
    CAPABILITIES = "capabilities"         # BackendDescriptor list of the PC
    HEARTBEAT = "heartbeat"               # health, sequence
    GENERATE = "generate"                 # GenerationRequest + remaining delay (never an absolute deadline)
    CHUNK = "chunk"                       # streamed text, ordered by index
    COMPLETE = "complete"
    CANCEL = "cancel"                     # idempotent
    ERROR = "error"                       # closed codes
    MEMORY_PROPOSAL = "memory_proposal"   # PC → phone only: proposals, never confirmed memories
    MEMORY_SNAPSHOT = "memory_snapshot"   # phone → PC: confirmed memories the owner allowed to share


class Role(Enum):
    MOBILE = "mobile"     # authority for session, history and memories (CORE on Android)
    CENTRAL = "central"   # PC engine host; never authority for memories


class LinkError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class Message:
    version: Tuple[int, int]
    sender: Role
    session: str          # link session established after pairing (opaque id)
    seq: int              # strictly increasing per sender and link session (replay protection)
    kind: Kind
    body: Dict
    remaining_ms: Optional[int] = None   # GENERATE only: bounded remaining delay, applied with the receiver clock

    def size(self) -> int:
        return len(repr(self.body).encode("utf-8"))


FORBIDDEN_BODY_KEYS = {"url", "uri", "path", "file", "api_key", "token", "password", "endpoint"}
ALLOWED = {Role.MOBILE: {Kind.HELLO, Kind.HEARTBEAT, Kind.GENERATE, Kind.CANCEL, Kind.MEMORY_SNAPSHOT, Kind.ERROR},
           Role.CENTRAL: {Kind.HELLO, Kind.CAPABILITIES, Kind.HEARTBEAT, Kind.CHUNK, Kind.COMPLETE, Kind.ERROR, Kind.MEMORY_PROPOSAL}}


class LinkEndpoint:
    """Receiving side state machine: version negotiation, pairing gate, replay protection, size limits."""

    def __init__(self, me: Role, paired: bool):
        self.me = me
        self.paired = paired              # result of an out-of-band, owner-confirmed pairing (not modelled here)
        self.peer_version: Optional[Tuple[int, int]] = None
        self.last_seq: Dict[Tuple[Role, str], int] = {}
        self.cancelled: set = set()
        self.chunks: Dict[str, List[str]] = {}

    def accept(self, m: Message) -> None:
        if m.sender == self.me:
            raise LinkError("LOOP")
        if m.version[0] != PROTOCOL[0]:
            raise LinkError("VERSION_MAJOR")          # major mismatch: explicit refusal, never a guess
        if not self.paired:
            raise LinkError("NOT_PAIRED")             # nothing, not even HELLO, is processed before pairing
        if m.kind != Kind.HELLO and self.peer_version is None:
            raise LinkError("NO_HELLO")
        if m.kind not in ALLOWED[m.sender]:
            raise LinkError("KIND_NOT_ALLOWED")       # e.g. a PC cannot send GENERATE or MEMORY_SNAPSHOT
        key = (m.sender, m.session)
        if m.seq <= self.last_seq.get(key, -1):
            raise LinkError("REPLAY")
        if m.size() > MAX_BODY_BYTES:
            raise LinkError("TOO_LARGE")
        if FORBIDDEN_BODY_KEYS & {k.lower() for k in m.body}:
            raise LinkError("FORBIDDEN_FIELD")
        if m.kind == Kind.GENERATE and not (m.remaining_ms is not None and 0 < m.remaining_ms <= MAX_REMAINING_MS):
            raise LinkError("DEADLINE")
        if m.kind != Kind.GENERATE and m.remaining_ms is not None:
            raise LinkError("DEADLINE")
        self.last_seq[key] = m.seq
        if m.kind == Kind.HELLO:
            self.peer_version = (m.version[0], min(m.version[1], PROTOCOL[1]))
        elif m.kind == Kind.CANCEL:
            self.cancelled.add(m.body["request_id"])  # idempotent
        elif m.kind == Kind.CHUNK:
            rid = m.body["request_id"]
            if rid in self.cancelled:
                return                                 # late chunks after cancel are ignored, not shown
            got = self.chunks.setdefault(rid, [])
            if m.body["index"] != len(got):
                raise LinkError("CHUNK_ORDER")
            got.append(m.body["text"])


class LoopbackTransport:
    """In-memory transport for contract tests ONLY."""

    def __init__(self, receiver: LinkEndpoint):
        self.receiver = receiver

    def send(self, m: Message) -> None:
        self.receiver.accept(m)


def open_network_transport(*_args, **_kwargs):
    """There is no network transport in ARCH-01. Any attempt is refused by design."""
    if not NETWORK_TRANSPORT_ENABLED:
        raise LinkError("NETWORK_DISABLED")
    raise NotImplementedError
