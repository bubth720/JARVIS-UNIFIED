"""Capability registry: what each backend can do, measured performance and freshness of its availability."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from .backend import Availability, BackendDescriptor, Health


@dataclass(frozen=True)
class Entry:
    descriptor: BackendDescriptor
    health: Health
    effective: Availability          # health downgraded to UNKNOWN when stale
    age_ms: int


class CapabilityRegistry:
    """Single source of truth for CORE routing. A backend must refresh its health (heartbeat) within
    ttl_ms; after that its availability is UNKNOWN, which is never eligible. Clock injected (monotonic,
    registry side only: remote timestamps are never compared with local ones)."""

    def __init__(self, ttl_ms: int = 15_000):
        if ttl_ms <= 0:
            raise ValueError("ttl")
        self.ttl_ms = ttl_ms
        self._d: Dict[str, BackendDescriptor] = {}
        self._h: Dict[str, Health] = {}

    def register(self, descriptor: BackendDescriptor, health: Health) -> None:
        old = self._d.get(descriptor.backend_id)
        if old is not None and old.model.sha256 != descriptor.model.sha256:
            # A different model under the same id is a different backend: previous measurements are void.
            self.withdraw(descriptor.backend_id)
        self._d[descriptor.backend_id] = descriptor
        self._h[descriptor.backend_id] = health

    def heartbeat(self, backend_id: str, health: Health) -> bool:
        if backend_id not in self._d:
            return False                 # unknown backends cannot appear through a heartbeat
        if health.checked_at_ms < self._h[backend_id].checked_at_ms:
            return False                 # stale/out-of-order heartbeat ignored
        self._h[backend_id] = health
        return True

    def withdraw(self, backend_id: str) -> None:
        self._d.pop(backend_id, None)
        self._h.pop(backend_id, None)

    def get(self, backend_id: str, now_ms: int) -> Optional[Entry]:
        d = self._d.get(backend_id)
        if d is None:
            return None
        h = self._h[backend_id]
        age = now_ms - h.checked_at_ms
        effective = h.availability if 0 <= age <= self.ttl_ms else Availability.UNKNOWN
        return Entry(d, h, effective, age)

    def snapshot(self, now_ms: int) -> List[Entry]:
        return [e for e in (self.get(i, now_ms) for i in sorted(self._d)) if e is not None]
