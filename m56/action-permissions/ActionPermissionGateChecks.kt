package jarvis.unified.actions

/**
 * Self-contained policy smoke checks, runnable without Android or JUnit.
 * These are source-level checks only until executed in a real Kotlin toolchain.
 */
object ActionPermissionGateChecks {
    @JvmStatic fun main(args: Array<String>) {
        val now = 1000L
        val read = ActionRequest("r1", ActionKind.READ_LOCAL, "notes/a", "hash1", true)
        val grant = CapabilityGrant(ActionKind.READ_LOCAL, "notes", 2000L)
        check(!ActionPermissionGate.decide(read, emptyList(), emptyList(), now).allowed)
        check(ActionPermissionGate.decide(read, listOf(grant), emptyList(), now).allowed)
        check(!ActionPermissionGate.decide(read, listOf(grant.copy(expiresAtEpochMs = now)), emptyList(), now).allowed)
        check(!ActionPermissionGate.decide(read.copy(resource = "notes-private/a"), listOf(grant), emptyList(), now).allowed)

        val send = ActionRequest("s1", ActionKind.SEND_MESSAGE, "mail/outbox/1", "sha256:a", true)
        val sendGrant = CapabilityGrant(ActionKind.SEND_MESSAGE, "mail/outbox", 2000L)
        val approval = ExplicitApproval("s1", ActionKind.SEND_MESSAGE, "mail/outbox/1", "sha256:a", 2000L)
        check(!ActionPermissionGate.decide(send, listOf(sendGrant), emptyList(), now).allowed)
        check(!ActionPermissionGate.decide(send, listOf(sendGrant), listOf(approval.copy(payloadDigest = "sha256:b")), now).allowed)
        check(ActionPermissionGate.decide(send, listOf(sendGrant), listOf(approval), now).allowed)
        check(!ActionPermissionGate.decide(send, listOf(sendGrant), listOf(approval.copy(expiresAtEpochMs = now)), now).allowed)

        val pay = ActionRequest("p1", ActionKind.PAYMENT, "bank/transfer", "sha256:p", true)
        check(!ActionPermissionGate.decide(pay, emptyList(), emptyList(), now).allowed)
    }
}
