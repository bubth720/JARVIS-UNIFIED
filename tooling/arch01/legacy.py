"""Adapter from the EXISTING CORE engine contract (LocalLanguageModel, pinned 5da9838) to ModelBackend.

The current Android engine is not replaced nor modified: it is wrapped. In Kotlin the adapter will live in
CORE (later, authorised mission) and delegate 1:1; here a Python Protocol mirrors the Kotlin signatures so
the mapping can be tested with simulated engines.
"""
from __future__ import annotations

from typing import Callable, Optional, Protocol

from .backend import (Availability, BackendDescriptor, Capabilities, Health, Location, ModelBackend, ModelIdentity,
                      Qualification, Refusal, Rejected, ReleaseResult, StopResult, GenerationRequest, GenerationResult,
                      Performance, validate)


class LocalLanguageModel(Protocol):
    """Mirror of com.stark.jarvislocal.LocalLanguageModel (methods listed in core_contract_5da9838.json)."""
    def warmUp(self, settings: dict) -> None: ...
    def generate(self, prompt: str, systemPrompt: str, settings: dict) -> str: ...
    def isLoaded(self) -> bool: ...
    def prepare(self, settings: dict) -> dict: ...
    def infer(self, request: dict) -> dict: ...
    def requestStop(self) -> str: ...            # StopResult name
    def unload(self) -> str: ...                 # UnloadResult name
    def openSession(self, sessionId: str) -> None: ...


class LegacyLocalModelBackend(ModelBackend):
    """ON_DEVICE backend over the historical engine. Defaults = CORE InferenceCapabilities (2048 / 256).
    The historical engine has no streaming: the whole text is delivered as one chunk."""

    def __init__(self, engine: LocalLanguageModel, model: ModelIdentity, backend_id: str = "android-local",
                 max_context: int = 2048, max_output: int = 256, memory_available_bytes: Optional[int] = None,
                 qualification: Qualification = Qualification.NOT_CHECKED):
        self.engine = engine
        self._d = BackendDescriptor(backend_id, Location.ON_DEVICE, "android", model,
                                    Capabilities(max_context, max_output, memory_available_bytes, streaming=False),
                                    Performance(), qualification)
        self._running: Optional[str] = None
        self.release_confirmed = True

    def descriptor(self) -> BackendDescriptor:
        return self._d

    def health(self, now_ms: int) -> Health:
        if not self.release_confirmed:
            return Health(Availability.DEGRADED, now_ms, "RELEASE_UNCONFIRMED")
        return Health(Availability.AVAILABLE if self.engine.isLoaded() else Availability.UNAVAILABLE, now_ms,
                      "OK" if self.engine.isLoaded() else "NOT_LOADED")

    def generate(self, request: GenerationRequest, on_text: Callable[[str], None]) -> GenerationResult:
        validate(request, self._d.capabilities)
        if self._running is not None:
            raise Rejected(Refusal.BUSY)
        self._running = request.request_id
        try:
            self.engine.openSession(request.session_id)
            settings = {"systemPrompt": request.system_prompt, "contextSize": request.context_tokens, "maxTokens": request.max_output_tokens}
            text = self.engine.generate(request.prompt(), request.system_prompt, settings)   # system prompt stays separate
            on_text(text)
            return GenerationResult(request.session_id, request.request_id, self._d.backend_id, text)
        finally:
            self._running = None

    def request_stop(self, request_id: str) -> StopResult:
        if self._running != request_id:
            return StopResult.NOT_RUNNING
        return StopResult(self.engine.requestStop())

    def release(self) -> ReleaseResult:
        r = ReleaseResult(self.engine.unload())
        # CORE rule: an implementation without a confirmed release must never authorise switching.
        self.release_confirmed = r == ReleaseResult.CONFIRMED
        return r
