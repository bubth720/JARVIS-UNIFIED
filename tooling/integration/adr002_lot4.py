"""ADR-002 lot 4: pure, OFF-by-default review of synthetic two-owner trace.

No IO, no IPC, no consent issuance, no token validation against real CORE,
no promotion of an UNKNOWN journal, and no Android runtime permission.
"""
from __future__ import annotations

from dataclasses import dataclass
import re

UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
WIRE_MAX_GENERATION = (1 << 53) - 1
EXPECTED = frozenset({"format", "epoch", "session", "request", "generation",
                      "operation", "source_digest", "content_digest", "destination",
                      "events", "readback"})
EVENT_KEYS = frozenset({"owner", "sequence", "state"})
READBACK_KEYS = frozenset({"closed", "acknowledged", "source_unchanged",
                           "destination_digest", "destination_identity"})
CORE_EVENTS = frozenset({"PREPARED", "CONSENT_CONSUMED", "REVOKED", "CANCELLED"})
SERVICES_EVENTS = frozenset({"DISPATCHED", "COMMIT_STARTED", "COMMITTED", "UNKNOWN"})
OPERATIONS = frozenset({"export.csv", "export.docx"})
MAX_EVENTS = 32


@dataclass(frozen=True)
class Verdict:
    state: str
    blockers: tuple[str, ...]
    runtime_authorized: bool = False
    issued_token: bool = False
    remote_identity_verified: bool = False
    durable_two_journal_commit_proven: bool = False
    allow_retry: bool = False
    allow_mutation: bool = False


def _is_uuid(value: object) -> bool:
    return type(value) is str and UUID.fullmatch(value) is not None


def _is_sha(value: object) -> bool:
    return type(value) is str and SHA256.fullmatch(value) is not None


def review(candidate: object) -> Verdict:
    """Review a small *untrusted* fixture and never return an execution grant."""
    blockers: set[str] = set()
    if type(candidate) is not dict or set(candidate) != EXPECTED:
        return Verdict("BLOCKED", ("SCHEMA_INVALID",))
    if candidate["format"] != "jarvis.adr002.lot4.synthetic-trace/1":
        blockers.add("VERSION_UNSUPPORTED")
    if not all(_is_uuid(candidate[k]) for k in ("epoch", "session", "request")):
        blockers.add("IDENTITY_INVALID")
    g = candidate["generation"]
    if type(g) is not int or g < 1 or g > WIRE_MAX_GENERATION:
        blockers.add("GENERATION_INCOMPATIBLE")
    if type(candidate["operation"]) is not str or candidate["operation"] not in OPERATIONS:
        blockers.add("OPERATION_INVALID")
    if not all(_is_sha(candidate[k]) for k in ("source_digest", "content_digest")):
        blockers.add("DIGEST_INVALID")
    d = candidate["destination"]
    if (type(d) is not str or len(d) == 0 or len(d) > 512
            or any(ord(c) < 32 or 0xD800 <= ord(c) <= 0xDFFF for c in d)):
        blockers.add("DESTINATION_INVALID")
    events = candidate["events"]
    if type(events) is not list or not 1 <= len(events) <= MAX_EVENTS:
        return Verdict("BLOCKED", tuple(sorted(blockers | {"EVENTS_INVALID"})))
    counters = {"CORE": 0, "SERVICES": 0}
    phase = {"CORE": None, "SERVICES": None}
    prepared = consent = dispatched = started = terminal = False
    cancelled = False
    for e in events:
        if type(e) is not dict or set(e) != EVENT_KEYS:
            blockers.add("EVENT_SCHEMA_INVALID")
            continue
        owner, sequence, state = e["owner"], e["sequence"], e["state"]
        if type(owner) is not str or owner not in counters:
            blockers.add("JOURNAL_OWNER_INVALID")
            continue
        if type(sequence) is not int or sequence != counters[owner] + 1:
            blockers.add("SEQUENCE_INVALID")
            continue
        counters[owner] += 1
        if type(state) is not str or state not in (CORE_EVENTS if owner == "CORE" else SERVICES_EVENTS):
            blockers.add("EVENT_STATE_INVALID")
            continue
        if terminal:
            blockers.add("AFTER_TERMINAL")
            continue
        if owner == "CORE":
            if state == "PREPARED":
                if prepared: blockers.add("REPLAY_PREPARE")
                prepared = True
            elif state == "CONSENT_CONSUMED":
                if not prepared or consent or cancelled:
                    blockers.add("CONSENT_UNAUTHORIZED")
                consent = True
            else:
                # Revocation/cancellation before engagement must block any effect.
                if not prepared: blockers.add("CANCEL_WITHOUT_PREPARE")
                if not started: cancelled = True
            phase[owner] = state
        elif state == "DISPATCHED":
            if not prepared or dispatched or cancelled or started:
                blockers.add("DISPATCH_INVALID")
            dispatched = True
        elif state == "COMMIT_STARTED":
            if not dispatched or not consent or started or cancelled:
                blockers.add("COMMIT_BARRIER_FAILED")
            started = True
        elif state == "COMMITTED":
            if not started or phase["SERVICES"] == "COMMITTED":
                blockers.add("COMMITTED_UNPROVEN")
            terminal = True
        elif state == "UNKNOWN":
            terminal = True
        phase[owner] = state
    rb = candidate["readback"]
    if type(rb) is not dict or set(rb) != READBACK_KEYS:
        blockers.add("READBACK_SCHEMA_INVALID")
    elif phase["SERVICES"] == "COMMITTED":
        if (rb["closed"] is not True or rb["acknowledged"] is not True
                or rb["source_unchanged"] is not True
                or rb["destination_digest"] != candidate["content_digest"]
                or rb["destination_identity"] != d):
            blockers.add("COMMITTED_LACKS_FULL_READBACK")
    if phase["SERVICES"] == "UNKNOWN":
        blockers.add("UNKNOWN_STICKY_NO_RETRY")
    if not blockers:
        # Syntactic trace only: no filesystem persistence, Android UID or actual grant.
        blockers.add("REVIEW_ONLY_NO_REAL_CORE_OR_DURABILITY")
    return Verdict("BLOCKED" if blockers != {"REVIEW_ONLY_NO_REAL_CORE_OR_DURABILITY"} else "REVIEW_ONLY",
                   tuple(sorted(blockers)))
