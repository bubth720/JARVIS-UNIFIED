package jarvis.unified.actions

/**
 * M56: deterministic, fail-closed policy boundary for assistant tool calls.
 * No LLM-generated text can grant permission. An adapter must check this
 * decision immediately before execution, not just when planning an action.
 *
 * This file is deliberately dependency-free and has no Android permissions.
 * Integration into CORE/SERVICES is NOT implied by its presence.
 */
enum class ActionKind {
    READ_LOCAL, READ_REMOTE, CREATE_LOCAL_REMINDER, WRITE_LOCAL,
    SEND_MESSAGE, DELETE_DATA, EXPORT_PRIVATE_DATA,
    MODIFY_CODE, INSTALL_PACKAGE, PAYMENT
}

data class ActionRequest(
    val actionId: String,
    val kind: ActionKind,
    val resource: String,
    val payloadDigest: String,
    val initiatedByUser: Boolean
)

data class CapabilityGrant(
    val kind: ActionKind,
    val resourcePrefix: String,
    val expiresAtEpochMs: Long
)

data class ExplicitApproval(
    val actionId: String,
    val kind: ActionKind,
    val resource: String,
    val payloadDigest: String,
    val expiresAtEpochMs: Long
)

enum class DecisionReason {
    ALLOW_SCOPED_READ, ALLOW_USER_REQUESTED_REMINDER, ALLOW_EXPLICIT_APPROVAL,
    DENY_INVALID_REQUEST, DENY_NO_CAPABILITY, DENY_EXPLICIT_APPROVAL_REQUIRED,
    DENY_PAYMENT, DENY_EXPIRED
}

data class ActionDecision(val allowed: Boolean, val reason: DecisionReason)

object ActionPermissionGate {
    private val sensitive = setOf(
        ActionKind.WRITE_LOCAL, ActionKind.SEND_MESSAGE, ActionKind.DELETE_DATA,
        ActionKind.EXPORT_PRIVATE_DATA, ActionKind.MODIFY_CODE,
        ActionKind.INSTALL_PACKAGE
    )

    /**
     * nowEpochMs must come from a trusted monotonic/clock abstraction in CORE.
     * Approval records must come from a trusted UI approval store, never the LLM.
     * The caller must atomically consume one-shot approvals before execution.
     */
    fun decide(
        request: ActionRequest,
        grants: Collection<CapabilityGrant>,
        approvals: Collection<ExplicitApproval>,
        nowEpochMs: Long
    ): ActionDecision {
        if (request.actionId.isBlank() || request.resource.isBlank() ||
            request.payloadDigest.isBlank() || nowEpochMs < 0L
        ) return ActionDecision(false, DecisionReason.DENY_INVALID_REQUEST)

        if (request.kind == ActionKind.PAYMENT) {
            return ActionDecision(false, DecisionReason.DENY_PAYMENT)
        }

        val scoped = grants.any {
            it.kind == request.kind &&
                it.expiresAtEpochMs > nowEpochMs &&
                (request.resource == it.resourcePrefix ||
                    request.resource.startsWith(it.resourcePrefix.trimEnd('/') + "/"))
        }

        if (request.kind == ActionKind.READ_LOCAL || request.kind == ActionKind.READ_REMOTE) {
            return if (scoped) ActionDecision(true, DecisionReason.ALLOW_SCOPED_READ)
            else ActionDecision(false, DecisionReason.DENY_NO_CAPABILITY)
        }

        if (request.kind == ActionKind.CREATE_LOCAL_REMINDER &&
            request.initiatedByUser && scoped
        ) return ActionDecision(true, DecisionReason.ALLOW_USER_REQUESTED_REMINDER)

        if (request.kind in sensitive || request.kind == ActionKind.CREATE_LOCAL_REMINDER) {
            val matching = approvals.any {
                it.actionId == request.actionId &&
                    it.kind == request.kind &&
                    it.resource == request.resource &&
                    it.payloadDigest == request.payloadDigest &&
                    it.expiresAtEpochMs > nowEpochMs
            }
            return if (scoped && matching) {
                ActionDecision(true, DecisionReason.ALLOW_EXPLICIT_APPROVAL)
            } else {
                ActionDecision(false, DecisionReason.DENY_EXPLICIT_APPROVAL_REQUIRED)
            }
        }

        return ActionDecision(false, DecisionReason.DENY_NO_CAPABILITY)
    }
}
