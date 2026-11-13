"""ModelBackend: the abstract contract every AI engine implements (Android on-device or PC local).

Services never talk to a backend: they talk to CORE, which routes to a backend through this contract.
The semantics extend, without changing, the CORE inference contract pinned at 5da9838
(LocalLanguageModel / InferenceRequest / InferenceCapabilities / InferenceRefusal / StopResult / UnloadResult).
"""
from __future__ import annotations

import abc
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, FrozenSet, Optional

CONTRACT_VERSION = "2.0.0-draft"     # v1 schemas are closed (contracts/v1/SEMANTICS.md): v2 must be negotiated
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class Location(Enum):
    ON_DEVICE = "on_device"      # Android phone/tablet, offline, no network permission
    PC_LOCAL = "pc_local"        # JARVIS CENTRAL on the owner's PC, reached only through the paired local link
    # There is deliberately no CLOUD value: a remote/cloud backend cannot be expressed by this contract.


class Availability(Enum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"          # never treated as available (v1 health-status rule)


class Modality(Enum):
    TEXT_IN = "text_in"
    TEXT_OUT = "text_out"
    IMAGE_IN = "image_in"
    AUDIO_IN = "audio_in"
    TOOL_CALLS = "tool_calls"
    EMBEDDINGS = "embeddings"


class Qualification(Enum):       # same closed values as contracts/v1 capability-manifest
    UNKNOWN = "unknown"
    NOT_CHECKED = "not_checked"
    CODE_VERIFIED = "code_verified"
    FIXTURE_TESTED = "fixture_tested"
    SIMULATED_ANDROID = "simulated_android"
    PHYSICAL_VERIFIED = "physical_verified"


class MeasurementOrigin(Enum):
    MEASURED = "measured"        # measured on this device with this model, with a sample count
    DECLARED = "declared"        # announced by the backend, not measured: never used to rank
    UNKNOWN = "unknown"


class DataClass(Enum):
    """Sensitivity of a request; the owner decides which classes may leave the phone for the PC."""
    PUBLIC = "public"
    PERSONAL = "personal"            # conversation, memories
    SENSITIVE = "sensitive"          # health, identity, voice profile references…


# Same values as CORE (pinned): these are the shared vocabulary, not new semantics.
class StopResult(Enum):
    REQUESTED = "REQUESTED"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_RUNNING = "NOT_RUNNING"


class ReleaseResult(Enum):       # = CORE UnloadResult
    CONFIRMED = "CONFIRMED"
    UNKNOWN = "UNKNOWN"
    FAILED = "FAILED"


class Refusal(Enum):             # CORE InferenceRefusal + routing/link refusals (prefixed by meaning)
    BUSY = "BUSY"
    CONTRACT = "CONTRACT"
    SYSTEM_PROMPT = "SYSTEM_PROMPT"
    BUDGET = "BUDGET"
    STALE_RESPONSE = "STALE_RESPONSE"
    STOP_REQUESTED = "STOP_REQUESTED"
    RELEASE_UNCONFIRMED = "RELEASE_UNCONFIRMED"
    DELEGATE_DISABLED = "DELEGATE_DISABLED"
    PROCESS_ENGINE_HELD = "PROCESS_ENGINE_HELD"
    NO_ELIGIBLE_BACKEND = "NO_ELIGIBLE_BACKEND"
    MODALITY = "MODALITY"


CORE_REFUSALS = {r.value for r in Refusal} - {"NO_ELIGIBLE_BACKEND", "MODALITY"}


class Rejected(Exception):
    def __init__(self, reason: Refusal, detail: str = ""):
        super().__init__(f"{reason.value}: {detail}")
        self.reason = reason


@dataclass(frozen=True)
class ModelIdentity:
    sha256: str                  # exact weights; a name never identifies a model
    family: str                  # e.g. "qwen3"
    parameters: str              # e.g. "0.6B"
    quantization: str            # e.g. "Q4_K_M"
    license: str

    def __post_init__(self):
        if not SHA256.match(self.sha256):
            raise ValueError("model sha256 must be 64 lowercase hex characters")


@dataclass(frozen=True)
class Performance:
    origin: MeasurementOrigin = MeasurementOrigin.UNKNOWN
    first_token_ms_p50: Optional[int] = None
    first_token_ms_p95: Optional[int] = None
    tokens_per_second: Optional[float] = None
    sample_count: int = 0
    measured_on: Optional[str] = None    # free label of the device ("POCO X8 Pro"), never an identifier

    @property
    def usable_for_ranking(self) -> bool:
        return self.origin == MeasurementOrigin.MEASURED and self.sample_count >= 5 and self.first_token_ms_p95 is not None


@dataclass(frozen=True)
class Capabilities:
    max_context_tokens: int
    max_output_tokens: int
    memory_available_bytes: Optional[int]          # None = unknown (not "unlimited")
    modalities: FrozenSet[Modality] = frozenset({Modality.TEXT_IN, Modality.TEXT_OUT})
    tools: FrozenSet[str] = frozenset()            # tool ids the backend can call (SERVICES tool.invoke)
    separate_system_prompt: bool = True            # CORE requires it (Refusal.SYSTEM_PROMPT otherwise)
    streaming: bool = True
    cancellation: bool = True


@dataclass(frozen=True)
class BackendDescriptor:
    backend_id: str
    location: Location
    platform: str                    # "android" | "linux" | "windows" | "macos" (v2: windows/macos added)
    model: ModelIdentity
    capabilities: Capabilities
    performance: Performance = Performance()
    qualification: Qualification = Qualification.NOT_CHECKED
    contract_version: str = CONTRACT_VERSION

    def __post_init__(self):
        if self.platform not in {"android", "linux", "windows", "macos"}:
            raise ValueError("unknown platform")
        if self.location == Location.ON_DEVICE and self.platform != "android":
            raise ValueError("an on-device backend runs on Android")


@dataclass(frozen=True)
class Health:
    availability: Availability
    checked_at_ms: int                     # receiver-side monotonic clock of the registry
    code: str = "OK"                       # closed codes in the doc; never a path, prompt or content


@dataclass(frozen=True)
class GenerationRequest:
    """Same fields as CORE InferenceRequest (v1) + routing requirements (v2)."""
    session_id: str
    request_id: str
    system_prompt: str
    question: str
    context: str = ""
    context_tokens: int = 2048
    max_output_tokens: int = 256
    required_modalities: FrozenSet[Modality] = frozenset({Modality.TEXT_IN, Modality.TEXT_OUT})
    required_tools: FrozenSet[str] = frozenset()
    data_class: DataClass = DataClass.PERSONAL
    contract_version: int = 1

    def prompt(self) -> str:                # identical rendering to CORE renderPrompt()
        return self.context + f"UTILISATEUR: {self.question}\nASSISTANT:"


@dataclass(frozen=True)
class GenerationResult:
    session_id: str
    request_id: str
    backend_id: str
    text: str
    native_done: bool = True               # an exception alone does not prove the backend stopped
    stopped: bool = False


def validate(request: GenerationRequest, caps: Capabilities) -> None:
    """Mirror of CORE validateInference (5da9838): same refusals, same byte budget rule."""
    if request.contract_version != 1 or not request.session_id.strip() or not request.request_id.strip():
        raise Rejected(Refusal.CONTRACT, "contract version or identifiers")
    if not caps.separate_system_prompt:
        raise Rejected(Refusal.SYSTEM_PROMPT)
    if not request.required_modalities <= caps.modalities or not request.required_tools <= caps.tools:
        raise Rejected(Refusal.MODALITY, "required modality or tool not offered")
    used = len(request.prompt().encode("utf-8")) + len(request.system_prompt.encode("utf-8"))
    if (not 1 <= request.context_tokens <= caps.max_context_tokens or not 1 <= request.max_output_tokens <= caps.max_output_tokens
            or used + request.max_output_tokens + 128 > request.context_tokens):
        raise Rejected(Refusal.BUDGET)


class ModelBackend(abc.ABC):
    """The only surface CORE uses to reach an engine. Implementations: Android A02 (existing, through the
    legacy adapter), future PC engines (llama.cpp server, vLLM, …) behind the paired local link."""

    @abc.abstractmethod
    def descriptor(self) -> BackendDescriptor: ...

    @abc.abstractmethod
    def health(self, now_ms: int) -> Health: ...

    @abc.abstractmethod
    def generate(self, request: GenerationRequest, on_text: Callable[[str], None]) -> GenerationResult:
        """Validates (validate()), streams text chunks to on_text in order, returns the full result.
        Raises Rejected for refusals; never returns success with an error."""

    @abc.abstractmethod
    def request_stop(self, request_id: str) -> StopResult:
        """Idempotent. A stop REQUEST is not the end of native work, nor a release."""

    @abc.abstractmethod
    def release(self) -> ReleaseResult:
        """Unload the model. Only CONFIRMED authorises loading another heavy backend in the same process."""
