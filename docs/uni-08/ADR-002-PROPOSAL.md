# UNI-08/U01 — ADR-002 proposal (NOT APPROVED)

**Status:** REVIEW_REQUIRED. This file has no authority to change UNIFIED v1/v2, CORE, SERVICES, or Android production behavior.

## Conflict verified

- SERVICES `CommitAuthorization.Preview` proposal/1 accepts generation **>=0** and its desktop fixture starts at generation 0.
- UNIFIED OperationReceipt/2-draft expects generation **1..2^53-1**. A direct cast is impossible for generation 0 or an oversized Java long.
- SERVICES local `COMMIT_STARTED` and UNIFIED draft `DISPATCHED` are **not equivalent** without agreement on the durable decision point. Historical CORE `COMPLETED` is not `COMMITTED`.
- An in-memory host `ConsentToken` and a synthetic SAF laboratory cannot attest a production CORE signature, revoke barrier or persisted consent.

## Nonbinding resolution for review

1. Keep existing local generation 0 fixtures and the old proposal/1 intact. Propose a future *versioned adapter*, which explicitly refuses generation 0 and >2^53-1 at the wire boundary. **Never silently add 1**.
2. CORE exclusively owns session, request, generation, cancellation, consent issuance, revoke serialization, and the single heavy-resource admission. No new registry, scheduler or memory owner in UNIFIED.
3. `COMMIT_STARTED` denotes SERVICES' durable start, not a general wire `DISPATCHED`. Define a future receipt with both fields if accepted. UNKNOWN is sticky on absent ACK; no implicit retry or rollback.
4. On confirmed user consent, a future CORE implementation must atomically validate preview/session/generation/deadline/revocation, consume a single-use token and persist its commit decision *before* calling the effect. SERVICES persists an effect-started marker before provider mutation. Readback of the full output and digest are required for a committed result. Fail closed on disagreement.
5. In the current U01 artifact, `uni08_u01.review` only classifies candidate mismatches on synthetic data. It **always returns BLOCKED** and has no host grant verification, state migration or runtime side effects.

## Human decisions before implementation

- Exact wire version and max generation boundary; whether local generation zero is retained for fixtures only.
- Definition of `DISPATCHED`, durable receipt fields, an explicit permission-revoked-after-commit indicator, and how UNKNOWN is restored after process death.
- Binding of UID/signature/grant, sources and provider destination; rotation, force-stop, cancellation and readback tests on an authorized emulator before first production activation.

## Acceptance for U01 (software review only)

- Python tests cover generation 0, negative/overflow, bool, altered source/destination, distinct receipt states, missing consent/readback and malformed payloads.
- No edits to `contracts/v1`, FUSION-01/02 manifests, runtime or other repositories; no GO claim.
- CI must be observed at exact code SHA; no production endorsement even on green CI.

Rollback: remove the additive U01 files on its isolated branch; no migration or private content exists.
