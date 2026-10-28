# ADR-002 LOT4 — GitHub recovery / UNIFIED

Base mission: 48a7314a7d14b6b73596a7eaef54da0d5024dca0
Branch: feat/lot4-offline-recovery-20261028
Scope: tooling/integration/adr002_lot4.py and its own 28 negative JUnit-equivalent unittest scenarios, isolated workflow.

The user approved **three principles only**, not runtime transport, durable journal choice or actual consent. The reviewer accepts bounded synthetic two-owner traces and flags invalid epoch, generation, digest, operation, sequences, missing CORE consent, cancellation before commitment, replay, UNKNOWN, missing source preservation and incomplete readback. Even a syntactically good simulation is REVIEW_ONLY, never a permission or durability proof.

No runtime binding/permission/manifest/SDK change. This is not a working two-database transaction or Android E2E. Historical UNIFIED U00/U01 and workspace invariants are part of this workflow. Workflow status must be read at the latest HEAD before claiming pass.

Next: agree with CORE/SERVICES on versioned wire and durable crash recovery, then request separate approval before any real transport/write/merge.
