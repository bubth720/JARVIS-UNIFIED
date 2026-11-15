"""Routing policy of CORE: Android model when the PC is absent, PC model when available AND authorised."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Tuple

from .backend import Availability, DataClass, GenerationRequest, Location, Rejected, Refusal, validate
from .registry import CapabilityRegistry, Entry


@dataclass(frozen=True)
class RoutingPolicy:
    """Owner's decision. Default: the PC is NOT authorised (nothing leaves the phone)."""
    pc_authorized: bool = False
    pc_data_classes: FrozenSet[DataClass] = frozenset({DataClass.PUBLIC, DataClass.PERSONAL})
    prefer_pc: bool = True                      # when both are eligible, the more capable PC wins
    accept_degraded: bool = False


@dataclass(frozen=True)
class Decision:
    backend_id: Optional[str]
    location: Optional[Location]
    reasons: Tuple[str, ...]                    # why each candidate was kept or excluded (auditable)

    @property
    def refused(self) -> bool:
        return self.backend_id is None


class Router:
    def __init__(self, registry: CapabilityRegistry, policy: RoutingPolicy = RoutingPolicy()):
        self.registry = registry
        self.policy = policy
        self._inflight: Dict[str, str] = {}       # request_id -> backend_id (no switch while generating)

    def _eligible(self, e: Entry, request: GenerationRequest, reasons: List[str]) -> bool:
        bid = e.descriptor.backend_id
        ok = {Availability.AVAILABLE} | ({Availability.DEGRADED} if self.policy.accept_degraded else set())
        if e.effective not in ok:
            reasons.append(f"{bid}: excluded, availability {e.effective.value}"); return False
        if e.descriptor.location == Location.PC_LOCAL:
            if not self.policy.pc_authorized:
                reasons.append(f"{bid}: excluded, PC not authorised by the owner"); return False
            if request.data_class not in self.policy.pc_data_classes:
                reasons.append(f"{bid}: excluded, data class {request.data_class.value} stays on the phone"); return False
        try:
            validate(request, e.descriptor.capabilities)
        except Rejected as r:
            reasons.append(f"{bid}: excluded, {r.reason.value}"); return False
        reasons.append(f"{bid}: eligible")
        return True

    def select(self, request: GenerationRequest, now_ms: int) -> Decision:
        if request.request_id in self._inflight:          # same request: same backend, never re-routed
            bid = self._inflight[request.request_id]
            e = self.registry.get(bid, now_ms)
            return Decision(bid, e.descriptor.location if e else None, ("in flight: pinned to " + bid,))
        reasons: List[str] = []
        eligible = [e for e in self.registry.snapshot(now_ms) if self._eligible(e, request, reasons)]
        if not eligible:
            return Decision(None, None, tuple(reasons + [Refusal.NO_ELIGIBLE_BACKEND.value]))

        def rank(e: Entry):
            pc_first = 0 if (self.policy.prefer_pc and e.descriptor.location == Location.PC_LOCAL) else 1
            p = e.descriptor.performance                     # only MEASURED performance may rank
            latency = p.first_token_ms_p95 if p.usable_for_ranking else 10**9
            return (pc_first, 0 if e.effective == Availability.AVAILABLE else 1, latency, e.descriptor.backend_id)

        best = sorted(eligible, key=rank)[0]
        return Decision(best.descriptor.backend_id, best.descriptor.location, tuple(reasons + ["selected " + best.descriptor.backend_id]))

    def begin(self, request: GenerationRequest, decision: Decision) -> None:
        if decision.refused:
            raise Rejected(Refusal.NO_ELIGIBLE_BACKEND)
        self._inflight[request.request_id] = decision.backend_id

    def end(self, request_id: str) -> None:
        self._inflight.pop(request_id, None)

    def on_backend_lost(self, backend_id: str) -> List[str]:
        """The PC disappeared: running requests are reported as interrupted (never silently replayed on
        another backend: a partial answer and side effects may already exist). Next turns route again."""
        lost = [r for r, b in self._inflight.items() if b == backend_id]
        for r in lost:
            self._inflight.pop(r)
        return lost
