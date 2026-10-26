"""UNI-08/U01, offline compatibility *review* of proposed CORE/SERVICES receipts.

Never translates historical states into authorization, activates a runtime, or
asserts that an input came from a trusted CORE process. Pure standard library.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

MAX_GENERATION = 2**53 - 1
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
OPERATIONS = frozenset(("export.csv", "export.docx"))
LOCAL_STATES = frozenset(("PREPARED", "COMMIT_STARTED", "COMMITTED", "REFUSED", "UNKNOWN"))
WIRE_STATES = frozenset(("PREPARED", "DISPATCHED", "COMMITTED", "UNKNOWN"))


@dataclass(frozen=True)
class Review:
    disposition: str
    blockers: tuple[str, ...]
    runtime_authorized: bool = False
    wire_receipt_created: bool = False


def _valid_uuid(value: object) -> bool:
    return type(value) is str and UUID.fullmatch(value) is not None


def _valid_digest(value: object) -> bool:
    return type(value) is str and DIGEST.fullmatch(value) is not None


def review(proposal: object) -> Review:
    """Conservative U01 review. Input is untrusted even when syntactically valid.

    Deliberately does not recognize COMMITTED as a wire receipt: the host must
    independently attest durable close, exact readback and consent at commit.
    No translation exists between COMMIT_STARTED and DISPATCHED.
    """
    if type(proposal) is not dict:
        return Review("BLOCKED", ("MALFORMED_INPUT",))
    required = {"format", "session", "request", "generation", "operation",
                "source_digest", "content_digest", "destination", "local_state",
                "wire_state", "host_grant_attested", "readback_attested"}
    if set(proposal) != required or proposal.get("format") != "jarvis.uni08-u01-review/1":
        return Review("BLOCKED", ("MALFORMED_INPUT",))
    blockers: list[str] = []
    if not _valid_uuid(proposal["session"]) or not _valid_uuid(proposal["request"]):
        blockers.append("INVALID_CORRELATION")
    generation = proposal["generation"]
    if type(generation) is not int or generation < 1 or generation > MAX_GENERATION:
        blockers.append("GENERATION_NOT_WIRE_SAFE")
    if type(proposal["operation"]) is not str or proposal["operation"] not in OPERATIONS:
        blockers.append("OPERATION_NOT_ALLOWLISTED")
    if not _valid_digest(proposal["source_digest"]) or not _valid_digest(proposal["content_digest"]):
        blockers.append("DIGEST_INVALID")
    destination = proposal["destination"]
    if (type(destination) is not str or not 1 <= len(destination) <= 4096
            or "\x00" in destination or any(0xD800 <= ord(c) <= 0xDFFF for c in destination)
            or len(destination.encode("utf-8", errors="replace")) > 4096):
        blockers.append("DESTINATION_INVALID")
    local_state, wire_state = proposal["local_state"], proposal["wire_state"]
    if (type(local_state) is not str or type(wire_state) is not str
            or local_state not in LOCAL_STATES or wire_state not in WIRE_STATES):
        blockers.append("UNKNOWN_STATE")
    elif local_state == "COMMIT_STARTED" and wire_state == "DISPATCHED":
        blockers.append("NON_EQUIVALENT_COMMIT_STATES")
    elif local_state == "REFUSED":
        blockers.append("REFUSAL_HAS_NO_WIRE_STATE")
    elif local_state != wire_state:
        blockers.append("STATE_TRANSITION_UNPROVEN")
    if proposal["host_grant_attested"] is not True:
        blockers.append("CORE_AUTHORITY_NOT_ATTESTED")
    if local_state == "COMMITTED" and proposal["readback_attested"] is not True:
        blockers.append("DURABLE_READBACK_NOT_ATTESTED")
    if not blockers:
        blockers.append("HUMAN_REVIEW_AND_RUNTIME_INTEGRATION_NOT_APPROVED")
    return Review("BLOCKED", tuple(sorted(set(blockers))))
