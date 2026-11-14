"""ARCH-01 contract tests. SIMULATED engines only: no model, no network, no Android, no PC.
A passing test proves the contract logic, never that a real backend works (that needs a device/PC)."""
import ast
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tooling.arch01.backend import (Availability, BackendDescriptor, Capabilities, DataClass, GenerationRequest,
                                    GenerationResult, Health, Location, MeasurementOrigin, Modality, ModelBackend,
                                    ModelIdentity, Performance, Refusal, Rejected, ReleaseResult, StopResult,
                                    CORE_REFUSALS, validate)
from tooling.arch01.legacy import LegacyLocalModelBackend, LocalLanguageModel
from tooling.arch01.link import (Kind, LinkEndpoint, LinkError, LoopbackTransport, Message, PROTOCOL, Role,
                                 open_network_transport)
from tooling.arch01.memory_sync import Confirmation, MobileMemoryAuthority, Proposal, State, SyncError, digest
from tooling.arch01.registry import CapabilityRegistry
from tooling.arch01.router import Router, RoutingPolicy

FIXTURE = json.loads((ROOT / "tooling/arch01/core_contract_5da9838.json").read_text())
SHA_06B = "ac2d97712095a558e31573f62f466a3f9d93990898b0ec79d7c974c1780d524a"   # Qwen3-0.6B Q4_K_M (V1)
SHA_PC = "b" * 64                                                                 # placeholder: no PC model chosen


class FakeBackend(ModelBackend):
    """Simulated engine: returns a fixed text in chunks; records calls."""

    def __init__(self, d: BackendDescriptor, availability=Availability.AVAILABLE, text="réponse simulée"):
        self._d, self.availability, self.text, self.calls, self.stops = d, availability, text, [], 0

    def descriptor(self): return self._d
    def health(self, now_ms): return Health(self.availability, now_ms)

    def generate(self, request, on_text):
        validate(request, self._d.capabilities)
        self.calls.append(request.request_id)
        for w in self.text.split(" "):
            on_text(w)
        return GenerationResult(request.session_id, request.request_id, self._d.backend_id, self.text)

    def request_stop(self, request_id): self.stops += 1; return StopResult.REQUESTED
    def release(self): return ReleaseResult.CONFIRMED


def android(**caps):
    c = dict(max_context_tokens=2048, max_output_tokens=256, memory_available_bytes=6 << 30)
    c.update(caps)
    return BackendDescriptor("android-local", Location.ON_DEVICE, "android", ModelIdentity(SHA_06B, "qwen3", "0.6B", "Q4_K_M", "apache-2.0"),
                             Capabilities(**c), Performance(MeasurementOrigin.MEASURED, 13_000, 16_000, 15.5, 20, "emulator API 35"))


def pc(backend_id="pc-central", tools=frozenset(), ctx=32_768, perf=Performance()):
    return BackendDescriptor(backend_id, Location.PC_LOCAL, "windows", ModelIdentity(SHA_PC, "simulated", "70B", "Q4_K_M", "n/a"),
                             Capabilities(ctx, 4096, 48 << 30, frozenset({Modality.TEXT_IN, Modality.TEXT_OUT, Modality.TOOL_CALLS}), tools), perf)


def req(rid="r1", **kw):
    base = dict(session_id="s1", request_id=rid, system_prompt="Tu es JARVIS.", question="Bonjour ?", context_tokens=2048, max_output_tokens=128)
    base.update(kw)
    return GenerationRequest(**base)


class CoreContractPreservedTests(unittest.TestCase):
    """The existing CORE engine contract (5da9838) is wrapped, not changed."""

    def test_adapter_covers_every_core_method_and_value(self):
        mirrored = {n for n, v in vars(LocalLanguageModel).items() if callable(v) and not n.startswith("_")}
        self.assertEqual(set(FIXTURE["LocalLanguageModel.methods"]), mirrored)
        self.assertEqual(FIXTURE["enums"]["StopResult"], [s.value for s in StopResult])
        self.assertEqual(FIXTURE["enums"]["UnloadResult"], [s.value for s in ReleaseResult])
        self.assertEqual(set(FIXTURE["enums"]["InferenceRefusal"]), CORE_REFUSALS)
        self.assertEqual(FIXTURE["InferenceCapabilities.defaults"]["maxContextSize"], "2048")
        self.assertEqual(FIXTURE["InferenceCapabilities.defaults"]["maxGenerationTokens"], "256")

    @unittest.skipUnless(os.environ.get("ARCH01_CORE_REPO"), "set ARCH01_CORE_REPO to re-verify against the CORE git history")
    def test_fixture_matches_core_git_blobs(self):
        repo, src = os.environ["ARCH01_CORE_REPO"], FIXTURE["source"]
        for f, blob in src["blobs"].items():
            got = subprocess.check_output(["git", "-C", repo, "rev-parse", f"{src['commit']}:app/src/main/java/com/stark/jarvislocal/{f}"]).decode().strip()
            self.assertEqual(blob, got, f)

    def test_validation_mirrors_core_refusals(self):
        caps = android().capabilities
        validate(req(), caps)
        for bad, reason in [(req(request_id=" "), Refusal.CONTRACT), (req(contract_version=2), Refusal.CONTRACT),
                            (req(context_tokens=4096), Refusal.BUDGET), (req(max_output_tokens=512), Refusal.BUDGET),
                            (req(context="x" * 4000), Refusal.BUDGET)]:
            with self.subTest(reason=reason), self.assertRaises(Rejected) as e:
                validate(bad, caps)
            self.assertEqual(reason, e.exception.reason)
        with self.assertRaises(Rejected) as e:
            validate(req(), Capabilities(2048, 256, None, separate_system_prompt=False))
        self.assertEqual(Refusal.SYSTEM_PROMPT, e.exception.reason)
        self.assertEqual("Bonjour ?", req().question)
        self.assertEqual("UTILISATEUR: Bonjour ?\nASSISTANT:", req().prompt())   # same rendering as CORE renderPrompt()


class SimulatedLegacyEngine:
    """Python stand-in for the current Android engine through the CORE contract."""
    def __init__(self, unload="CONFIRMED"):
        self.loaded, self.unload_result, self.seen = True, unload, []
    def warmUp(self, settings): self.loaded = True
    def generate(self, prompt, systemPrompt, settings): self.seen.append((prompt, systemPrompt)); return "Bonjour !"
    def isLoaded(self): return self.loaded
    def prepare(self, settings): return {"nativeDone": True, "modelUnloaded": False}
    def infer(self, request): raise AssertionError("the adapter uses generate() with a separate system prompt")
    def requestStop(self): return "UNSUPPORTED"
    def unload(self): self.loaded = False; return self.unload_result
    def openSession(self, sessionId): pass


class LegacyAdapterTests(unittest.TestCase):
    def test_current_engine_keeps_its_behaviour_behind_the_contract(self):
        eng = SimulatedLegacyEngine()
        b = LegacyLocalModelBackend(eng, android().model)
        out = []
        r = b.generate(req(), out.append)
        self.assertEqual("Bonjour !", r.text); self.assertEqual(["Bonjour !"], out)
        self.assertEqual([("UTILISATEUR: Bonjour ?\nASSISTANT:", "Tu es JARVIS.")], eng.seen)   # system prompt separate
        self.assertEqual(Location.ON_DEVICE, b.descriptor().location)
        self.assertEqual(StopResult.NOT_RUNNING, b.request_stop("r1"))

    def test_unconfirmed_release_blocks_switching(self):
        reg = CapabilityRegistry()
        b = LegacyLocalModelBackend(SimulatedLegacyEngine(unload="UNKNOWN"), android().model)
        self.assertEqual(ReleaseResult.UNKNOWN, b.release())
        reg.register(b.descriptor(), b.health(0))
        self.assertTrue(Router(reg).select(req(), 1).refused)         # DEGRADED/unloaded: never routed


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.reg = CapabilityRegistry(ttl_ms=10_000)
        self.reg.register(android(), Health(Availability.AVAILABLE, 0))

    def test_pc_absent_uses_android_offline(self):
        d = Router(self.reg, RoutingPolicy(pc_authorized=True)).select(req(), 100)
        self.assertEqual(("android-local", Location.ON_DEVICE), (d.backend_id, d.location))

    def test_pc_present_but_not_authorised_stays_on_phone(self):
        self.reg.register(pc(), Health(Availability.AVAILABLE, 0))
        d = Router(self.reg).select(req(), 100)                         # default policy: PC not authorised
        self.assertEqual("android-local", d.backend_id)
        self.assertIn("pc-central: excluded, PC not authorised by the owner", d.reasons)

    def test_pc_available_and_authorised_is_preferred(self):
        self.reg.register(pc(), Health(Availability.AVAILABLE, 0))
        self.assertEqual("pc-central", Router(self.reg, RoutingPolicy(pc_authorized=True)).select(req(), 100).backend_id)

    def test_stale_or_unknown_pc_falls_back_to_android(self):
        self.reg.register(pc(), Health(Availability.AVAILABLE, 0))
        self.reg.heartbeat("android-local", Health(Availability.AVAILABLE, 20_000))
        d = Router(self.reg, RoutingPolicy(pc_authorized=True)).select(req(), 20_000)   # PC heartbeat 20 s old
        self.assertEqual("android-local", d.backend_id)
        self.assertIn("pc-central: excluded, availability unknown", d.reasons)
        self.reg.register(pc(), Health(Availability.UNKNOWN, 20_000))
        self.assertEqual("android-local", Router(self.reg, RoutingPolicy(pc_authorized=True)).select(req(), 20_000).backend_id)

    def test_sensitive_data_never_leaves_the_phone(self):
        self.reg.register(pc(), Health(Availability.AVAILABLE, 0))
        d = Router(self.reg, RoutingPolicy(pc_authorized=True)).select(req(data_class=DataClass.SENSITIVE), 100)
        self.assertEqual("android-local", d.backend_id)

    def test_big_context_needs_the_pc_and_is_refused_without_it(self):
        big = req(context_tokens=16_000, max_output_tokens=1000)
        self.assertTrue(Router(self.reg, RoutingPolicy(pc_authorized=True)).select(big, 100).refused)
        self.reg.register(pc(), Health(Availability.AVAILABLE, 0))
        self.assertEqual("pc-central", Router(self.reg, RoutingPolicy(pc_authorized=True)).select(big, 100).backend_id)
        self.assertTrue(Router(self.reg).select(big, 100).refused)      # unauthorised: explicit refusal, no downgrade

    def test_services_tool_requests_go_only_to_backends_declaring_the_tool(self):
        self.reg.register(pc(tools=frozenset({"services.calendar.read"})), Health(Availability.AVAILABLE, 0))
        tool = req(required_modalities=frozenset({Modality.TEXT_IN, Modality.TEXT_OUT, Modality.TOOL_CALLS}),
                   required_tools=frozenset({"services.calendar.read"}))
        self.assertEqual("pc-central", Router(self.reg, RoutingPolicy(pc_authorized=True)).select(tool, 100).backend_id)
        self.assertTrue(Router(self.reg).select(tool, 100).refused)

    def test_only_measured_performance_ranks_backends(self):
        self.reg.register(pc("pc-a", perf=Performance(MeasurementOrigin.DECLARED, 10, 20, 999.0, 0)), Health(Availability.AVAILABLE, 0))
        self.reg.register(pc("pc-b", perf=Performance(MeasurementOrigin.MEASURED, 900, 1200, 40.0, 30, "PC")), Health(Availability.AVAILABLE, 0))
        self.assertEqual("pc-b", Router(self.reg, RoutingPolicy(pc_authorized=True)).select(req(), 100).backend_id)

    def test_running_request_is_never_rerouted_nor_replayed(self):
        self.reg.register(pc(), Health(Availability.AVAILABLE, 0))
        r = Router(self.reg, RoutingPolicy(pc_authorized=True)); q = req()
        d = r.select(q, 100); r.begin(q, d)
        self.reg.withdraw("pc-central")                                  # PC disappears during the turn
        self.assertEqual("pc-central", r.select(q, 200).backend_id)      # same request stays pinned
        self.assertEqual(["r1"], r.on_backend_lost("pc-central"))         # reported interrupted, not replayed
        self.assertEqual("android-local", r.select(req("r2"), 300).backend_id)   # next turn: phone, offline

    def test_a_new_pc_engine_plugs_in_at_runtime_without_rebuilding(self):
        """Theoretical criterion of ARCH-01: a more powerful engine is only a new descriptor + implementation."""
        class FuturePcEngine(FakeBackend):
            pass
        eng = FuturePcEngine(pc("pc-future", ctx=131_072))
        self.reg.register(eng.descriptor(), eng.health(0))
        r = Router(self.reg, RoutingPolicy(pc_authorized=True)); q = req(context_tokens=100_000, max_output_tokens=2000)
        d = r.select(q, 10); self.assertEqual("pc-future", d.backend_id)
        chunks = []; res = eng.generate(q, chunks.append)
        self.assertEqual(res.text, " ".join(chunks)); self.assertEqual(["r1"], eng.calls)

    def test_nothing_eligible_is_an_explicit_refusal(self):
        self.reg.register(android(), Health(Availability.UNAVAILABLE, 0))
        d = Router(self.reg, RoutingPolicy(pc_authorized=True)).select(req(), 100)
        self.assertTrue(d.refused); self.assertEqual(Refusal.NO_ELIGIBLE_BACKEND.value, d.reasons[-1])
        with self.assertRaises(Rejected):
            Router(self.reg).begin(req(), d)


class RegistryTests(unittest.TestCase):
    def test_heartbeat_rules_and_model_change(self):
        reg = CapabilityRegistry(ttl_ms=1000)
        self.assertFalse(reg.heartbeat("ghost", Health(Availability.AVAILABLE, 0)))
        reg.register(pc(), Health(Availability.AVAILABLE, 500))
        self.assertFalse(reg.heartbeat("pc-central", Health(Availability.AVAILABLE, 400)))   # out of order
        self.assertEqual(Availability.UNKNOWN, reg.get("pc-central", 2000).effective)
        self.assertEqual(Availability.UNKNOWN, reg.get("pc-central", 100).effective)          # clock before check: unknown
        other = BackendDescriptor("pc-central", Location.PC_LOCAL, "linux", ModelIdentity("c" * 64, "x", "8B", "Q8_0", "mit"), pc().capabilities)
        reg.register(other, Health(Availability.AVAILABLE, 600))
        self.assertEqual("c" * 64, reg.get("pc-central", 700).descriptor.model.sha256)

    def test_descriptor_rules(self):
        with self.assertRaises(ValueError):
            ModelIdentity("not-a-sha", "x", "1B", "q", "l")
        with self.assertRaises(ValueError):
            BackendDescriptor("x", Location.ON_DEVICE, "windows", android().model, android().capabilities)
        self.assertNotIn("CLOUD", Location.__members__)


class LinkTests(unittest.TestCase):
    def setUp(self):
        self.phone = LinkEndpoint(Role.MOBILE, paired=True)
        self.t = LoopbackTransport(self.phone)
        self.t.send(Message(PROTOCOL, Role.CENTRAL, "L1", 0, Kind.HELLO, {"role": "central"}))

    def m(self, seq, kind, body, sender=Role.CENTRAL, **kw):
        return Message(PROTOCOL, sender, "L1", seq, kind, body, **kw)

    def assertLink(self, code, msg, endpoint=None):
        with self.assertRaises(LinkError) as e:
            (endpoint or self.phone).accept(msg)
        self.assertEqual(code, e.exception.code)

    def test_pairing_version_hello_and_roles(self):
        self.assertLink("NOT_PAIRED", self.m(0, Kind.HELLO, {}), LinkEndpoint(Role.MOBILE, paired=False))
        self.assertLink("VERSION_MAJOR", Message((3, 0), Role.CENTRAL, "L1", 5, Kind.HEARTBEAT, {}))
        self.assertLink("NO_HELLO", self.m(0, Kind.HEARTBEAT, {}), LinkEndpoint(Role.MOBILE, paired=True))
        self.assertLink("KIND_NOT_ALLOWED", self.m(1, Kind.GENERATE, {"request_id": "r"}, remaining_ms=1000))   # a PC never drives the phone
        self.assertLink("KIND_NOT_ALLOWED", self.m(1, Kind.MEMORY_SNAPSHOT, {}))                                 # nor sends memories as truth

    def test_replay_size_forbidden_fields_and_deadline(self):
        self.t.send(self.m(1, Kind.HEARTBEAT, {"availability": "available"}))
        self.assertLink("REPLAY", self.m(1, Kind.HEARTBEAT, {}))
        self.assertLink("TOO_LARGE", self.m(2, Kind.CHUNK, {"request_id": "r", "index": 0, "text": "x" * 70_000}))
        self.assertLink("FORBIDDEN_FIELD", self.m(3, Kind.CAPABILITIES, {"endpoint": "x"}))
        central = LinkEndpoint(Role.CENTRAL, paired=True)
        central.accept(Message(PROTOCOL, Role.MOBILE, "L1", 0, Kind.HELLO, {}))
        self.assertLink("DEADLINE", Message(PROTOCOL, Role.MOBILE, "L1", 1, Kind.GENERATE, {"request_id": "r"}), central)
        self.assertLink("DEADLINE", Message(PROTOCOL, Role.MOBILE, "L1", 2, Kind.GENERATE, {"request_id": "r"}, remaining_ms=10**9), central)
        central.accept(Message(PROTOCOL, Role.MOBILE, "L1", 3, Kind.GENERATE, {"request_id": "r"}, remaining_ms=60_000))

    def test_chunks_are_ordered_and_cancel_is_idempotent(self):
        self.t.send(self.m(1, Kind.CHUNK, {"request_id": "r", "index": 0, "text": "Bon"}))
        self.assertLink("CHUNK_ORDER", self.m(2, Kind.CHUNK, {"request_id": "r", "index": 2, "text": "!"}))
        central = LinkEndpoint(Role.CENTRAL, paired=True)
        central.accept(Message(PROTOCOL, Role.MOBILE, "L1", 0, Kind.HELLO, {}))
        for s in (1, 2):
            central.accept(Message(PROTOCOL, Role.MOBILE, "L1", s, Kind.CANCEL, {"request_id": "r"}))
        self.assertEqual({"r"}, central.cancelled)
        self.phone.cancelled.add("r")
        self.t.send(self.m(3, Kind.CHUNK, {"request_id": "r", "index": 1, "text": "jour"}))   # late chunk: ignored
        self.assertEqual(["Bon"], self.phone.chunks["r"])

    def test_no_network_transport_exists(self):
        with self.assertRaises(LinkError) as e:
            open_network_transport("192.168.1.10", 8080)
        self.assertEqual("NETWORK_DISABLED", e.exception.code)


class MemorySyncTests(unittest.TestCase):
    def test_pc_proposes_phone_confirms_with_exact_content(self):
        a = MobileMemoryAuthority("s1")
        a.receive(Proposal("p1", None, "m1", "Je préfère le thé."))
        self.assertEqual({}, a.memories)                                  # a proposal is not a memory
        with self.assertRaises(SyncError):
            a.confirm(Confirmation("p1", digest("Je préfère le café."), "s1"))
        with self.assertRaises(SyncError):
            a.confirm(Confirmation("p1", digest("Je préfère le thé."), "other-session"))
        m = a.confirm(Confirmation("p1", digest("Je préfère le thé."), "s1"))
        self.assertEqual((1, State.CONFIRMED), (m.revision, m.state))
        self.assertEqual([], a.snapshot_for_pc())                         # not shared unless the owner allows it
        a.share("m1", True); self.assertEqual(["m1"], [x.memory_id for x in a.snapshot_for_pc()])

    def test_conflicts_rejections_and_deletion_win(self):
        a = MobileMemoryAuthority("s1")
        a.receive(Proposal("p1", None, "m1", "A")); a.confirm(Confirmation("p1", digest("A"), "s1"))
        with self.assertRaises(SyncError) as e:
            a.receive(Proposal("p2", 0, "m1", "B"))
        self.assertEqual("CONFLICT", e.exception.code)
        a.receive(Proposal("p3", 1, "m1", "B")); a.reject("p3"); self.assertEqual({}, a.pending)
        a.delete("m1")
        with self.assertRaises(SyncError) as e:
            a.receive(Proposal("p4", 2, "m1", "C"))
        self.assertEqual("DELETED_WINS", e.exception.code)
        self.assertEqual(State.DELETED, a.snapshot_for_pc()[0].state)


class NoActivationTests(unittest.TestCase):
    def test_package_has_no_network_process_or_model_access(self):
        banned = {"socket", "urllib", "http", "requests", "subprocess", "ssl", "asyncio"}
        for f in (ROOT / "tooling/arch01").glob("*.py"):
            tree = ast.parse(f.read_text())
            names = {a.name.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
            names |= {n.module.split(".")[0] for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module and n.level == 0}
            self.assertFalse(names & banned, f"{f.name}: {names & banned}")
            self.assertIsNone(re.search(r"\.gguf|huggingface|https?://", f.read_text()), f.name)


if __name__ == "__main__":
    unittest.main()
