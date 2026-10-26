# FUSION-02 — candidature Android-first

Verdict : BLOCKED. Aucun droit d’installation ou activation accordé.

| Module | Primaire | CI exacte | Android minSdk |
|---|---|---|---|
| core | 36761cea101b5f88b87cd4136dc075d28a1adb96 | success | 24 (0 = hors Android) |
| evolution | c0180181804338d21f3bf9d4b537b709595902f7 | success | 0 (0 = hors Android) |
| interface | 1d0a89f3d92cba64122db08cc7b326239f85c08d | success | 26 (0 = hors Android) |
| llm | e0b781442b21034a251f6af450396faabc5f667d | unknown | 29 (0 = hors Android) |
| nexus | 9d6928cd8651f83fa5091bdb474b33761d366412 | unknown | 24 (0 = hors Android) |
| services | f00091a639612b91eca1a301580c8f531249f1e3 | failure | 24 (0 = hors Android) |
| unified | 3caa57d91ce0dba31043e7cb6373a5e2df8b9fa4 | failure | 0 (0 = hors Android) |
| voice | fe57452fcb33f5b6870070f30ba6c5f1d349c4ba | unknown | 26 (0 = hors Android) |

## Prérequis Android24/25 manquants

- ANDROID_E2E_MISSING:android24:A
- ANDROID_E2E_MISSING:android24:B
- ANDROID_E2E_MISSING:android24:C
- ANDROID_E2E_MISSING:android24:D
- ANDROID_E2E_MISSING:android24:E
- ANDROID_E2E_MISSING:android24:F
- ANDROID_E2E_MISSING:android24:G
- ANDROID_E2E_MISSING:android24:H
- ANDROID_E2E_MISSING:android24:I
- ANDROID_E2E_MISSING:android24:J
- ANDROID_E2E_MISSING:android25:A
- ANDROID_E2E_MISSING:android25:B
- ANDROID_E2E_MISSING:android25:C
- ANDROID_E2E_MISSING:android25:D
- ANDROID_E2E_MISSING:android25:E
- ANDROID_E2E_MISSING:android25:F
- ANDROID_E2E_MISSING:android25:G
- ANDROID_E2E_MISSING:android25:H
- ANDROID_E2E_MISSING:android25:I
- ANDROID_E2E_MISSING:android25:J
- ANDROID_PRODUCER_PROOF_MISSING:nexus:android24
- ANDROID_PRODUCER_PROOF_MISSING:nexus:android25
- ANDROID_PRODUCER_PROOF_MISSING:services:android24
- ANDROID_PRODUCER_PROOF_MISSING:services:android25
- CI_NOT_SUCCESS:nexus
- CI_NOT_SUCCESS:services
- CORE production Android AppGraph/SessionCoordinator does not compose the selected primary ports.
- CORE_NOT_CONSUMING_PRIMARY:nexus
- CORE_NOT_CONSUMING_PRIMARY:services
- NEXUS real Android FTS5/citation and API24/25 instrumentation missing.
- SERVICES live authorizeAtCommit fence and SAF readback export not qualified.

## Preuves enregistrées, non réexécutées par ce rapport

| Preuve | Module | Niveau | Cible | Verdict |
|---|---|---|---|---|
| core-jvm-linux | core | JVM_PASS | linux | PASS |
| llm-jvm-linux | llm | JVM_PASS | linux | PASS |
| nexus-jvm-linux | nexus | JVM_PASS | linux | PASS |
| services-jvm-linux | services | JVM_PASS | linux | PASS |
| interface-jvm-linux | interface | JVM_PASS | linux | PASS |
| evolution-jvm-linux | evolution | JVM_PASS | linux | PASS |
