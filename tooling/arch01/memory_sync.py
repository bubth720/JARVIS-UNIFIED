"""Memory synchronisation contract between JARVIS MOBILE (authority) and JARVIS CENTRAL (replica).

Rules from ARCHITECTURE.md "Politique de mémorisation durable", extended to two machines:
- the phone's CORE stays the single authority for confirmed memories;
- the PC may only PROPOSE (e.g. after a long analysis); a proposal becomes a memory only after the owner's
  explicit confirmation bound to proposal id + revision + content hash, on the phone;
- the phone sends the PC only memories the owner allowed to share; deletion on the phone wins.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class State(Enum):
    PROPOSED = "proposed"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"
    DELETED = "deleted"


@dataclass(frozen=True)
class Memory:
    memory_id: str
    revision: int
    text_sha256: str
    state: State
    shareable_with_pc: bool = False


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    base_revision: Optional[int]      # revision the PC saw; None = new memory
    memory_id: str
    text: str
    origin: str = "central"


@dataclass(frozen=True)
class Confirmation:
    """Produced ONLY by an owner gesture on the phone UI (never by a model output)."""
    proposal_id: str
    text_sha256: str
    session_id: str


class SyncError(Exception):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class MobileMemoryAuthority:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.memories: Dict[str, Memory] = {}
        self.pending: Dict[str, Proposal] = {}

    def receive(self, p: Proposal) -> None:
        cur = self.memories.get(p.memory_id)
        if cur is not None and cur.state == State.DELETED:
            raise SyncError("DELETED_WINS")
        if cur is not None and p.base_revision != cur.revision:
            raise SyncError("CONFLICT")             # PC worked on an outdated version: owner must review again
        self.pending[p.proposal_id] = p             # stays a proposal: nothing is stored yet

    def confirm(self, c: Confirmation) -> Memory:
        p = self.pending.get(c.proposal_id)
        if p is None:
            raise SyncError("UNKNOWN_PROPOSAL")
        if c.session_id != self.session_id or c.text_sha256 != digest(p.text):
            raise SyncError("CONFIRMATION_MISMATCH")   # edited text / other session: confirm again
        cur = self.memories.get(p.memory_id)
        m = Memory(p.memory_id, (cur.revision + 1) if cur else 1, digest(p.text), State.CONFIRMED)
        self.memories[p.memory_id] = m
        del self.pending[c.proposal_id]
        return m

    def reject(self, proposal_id: str) -> None:
        self.pending.pop(proposal_id, None)            # nothing durable is created

    def share(self, memory_id: str, allowed: bool) -> None:
        """Owner's explicit choice, per memory; default is not shared."""
        cur = self.memories[memory_id]
        self.memories[memory_id] = Memory(cur.memory_id, cur.revision, cur.text_sha256, cur.state, allowed)

    def delete(self, memory_id: str) -> None:
        cur = self.memories[memory_id]
        self.memories[memory_id] = Memory(memory_id, cur.revision + 1, cur.text_sha256, State.DELETED)

    def snapshot_for_pc(self):
        """Only confirmed memories the owner marked shareable; deletions are propagated as tombstones."""
        return [m for m in self.memories.values() if (m.state == State.CONFIRMED and m.shareable_with_pc) or m.state == State.DELETED]
