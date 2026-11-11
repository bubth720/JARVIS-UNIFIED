# R02 — Security remediation and offline Android V1 coordination (2026-11-11)

Status: **BLOCKED — security remediation not yet demonstrated**. This is a coordination-only document, not a claim of implemented fixes, executed tests, or APK delivery.

## Verified source inputs
- JARVIS-LLM branch `codex/m51-lab-cloud-audit`, commit `08fbda527d187f324d94e0adafbca76fa955a343`: `m51review/SECURITY-REVIEW.md`. M51.07 verdict NO-GO; admission patch `8df826451e501a107305f8fcaee5ca3d5334e22de23246d32cc7fd5312da21e8` not applied.
- JARVIS-UNIFIED branch `codex/v1-first-run-recovery-20261110`, commit `093c30637093ad829dbd3643747ec5cb52499695`: `reports/v1-acceleration/MISSION-51/SECURITY-REVIEW.md` and `docs/v1-first-run/PLAN.md`.
- R01 original report/evidence bundle: **not located**. M51 observations must not be misrepresented as the R01 report.

## Three remediation workstreams
A. **Authority/integrity**: A01 missing independent operator root, A02 pathname / writable-FD / mtime restoration, A06 self-declared unattested context. Require independent trusted root, run/job/commit/artifact binding, immutable content or FD receipt, and exact license/hash/model authorization. Never synthesize a signed authority or treat local signer as independent.
B. **Concurrency/lifecycle**: A03 watcher exception blocks subsequent notifications, A04 blocking monitor delays shared deadline, A07 terminal transitions unsealed, A08 watcher under lease lock but outside broker. Isolate callback failure, bound deadline independently, make terminal state idempotent, ensure lease/broker ordering.
C. **Errors/resources**: A05 filesystem exception leaks paths, A09 memory peak unbounded atomically and not exercised with resident model. Sanitize errors, enforce atomic reservation and thermal/RAM gates; test cancellation/backpressure/cleanup.

## Hard gates
G0: verify historical guard implementations, preimages, contracts, source commits and R01 provenance; snapshot baselines.
G1: produce *new* LLM security diff on isolated LLM branch and adversarial tests; security review must approve exact diff and independent authority provisioning.
G2: real JNI generation only after G1; no fake tokens, no synthetic fallback; cloud model authorization is not Android model authorization. If weights are absent, report BLOCKED.
G3: Android integration only after G2: reuse CORE SessionCoordinator + INTERFACE client; text input, streamed output, visible errors, local session, interruption recovery; no VOICE/avatar/services.
G4: emulator API29/API35 + offline proof + APK signature/SHA256 + RAM, startup, tokens/s, battery, thermal measurements. A compiled APK is not sufficient.

## Restrictions
No merge into main, no personal-device installation, no additional model download, no security bypass, no destructive operations. Do not claim G-A/G-ROOT/G-B/G-C passed without independent evidence. All failed prerequisites stop dependent work.

## Deliverable ledger
Module: UNIFIED (coordination). Mission: R02. Branch: `mission/r02-security-v1-coordination-20261111`. Tests: NOT_RUN. Security fixes: NOT_APPLIED. Real generation: NOT_RUN. Android APK: NOT_PRODUCED. Next action: obtain exact security source/preimages and implement separate LLM remediation diff with isolated tests, then review before admission.
