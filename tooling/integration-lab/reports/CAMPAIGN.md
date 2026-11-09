# JARVIS INTEGRATION LAB — FAIL

Campagne : `fa4db0c6-75b6-47ca-8e69-940413456fd2` ; mode safe.
LAB commit : `1a10328459a71578a6e56427b848cb6467fba57d` ; tree `b37563981c7fb2db0a236c48cda6adcfa016aff4`.
Les tests hôte, schémas et APK compilées ne prouvent ni Android ni une intégration runtime.

| Module | Source | État | Blocage |
|---|---|---|---|
| CORE | `5da98383ed12cb5a54e896fbe57560bacc432fb5` | PASS |  |
| LLM | `08fbda527d187f324d94e0adafbca76fa955a343` | FAIL |  |
| VOICE | `fe57452fcb33f5b6870070f30ba6c5f1d349c4ba` | FAIL |  |
| INTERFACE | `b9a9506785b8851f55789ed4329c9394a3937447` | PASS |  |
| NEXUS | `eae61fb62a9ccd4073b96d71454f89e5a943eae9` | PASS |  |
| SERVICES | `8d80d09d6aabf6eac00a7bc6bb4930862bd72812` | PASS |  |
| UNIFIED | `a7625a31513be5c56fa36ed946fbdcd3c23c2a15` | PASS |  |
| EVOLUTION | `84ebc2e2b55d48306247fc9045a712294abaf457` | PASS |  |

## Commandes exécutées

| ID | Module / type | État | Invocations / uniques | Durée hôte (s) |
|---|---|---|---|---|
| core-scope | CORE / UNIT | PASS | 20 / None | 0.803 |
| llm-perf02 | LLM / UNIT | PASS | 34 / None | 0.603 |
| llm-historical-guard | LLM / STATIC | FAIL | None / None | 0.653 |
| llm-manifest-guard | LLM / STATIC | FAIL | None / None | 0.051 |
| interface-host | INTERFACE / UNIT | PASS | 17 / None | 0.151 |
| nexus-sqlite | NEXUS / INTEGRATION | PASS | 10 / None | 0.653 |
| unified-validator | UNIFIED / STATIC | PASS | None / None | 0.302 |
| unified-tests | UNIFIED / UNIT | PASS | 41 / None | 0.402 |
| unified-registry | UNIFIED / UNIT | PASS | 23 / None | 0.904 |
| unified-backup | UNIFIED / UNIT | PASS | 30 / None | 15.505 |
| unified-campaign | UNIFIED / UNIT | PASS | 32 / None | 1.605 |
| unified-integration | UNIFIED / UNIT | PASS | 21 / None | 0.653 |
| unified-v1 | UNIFIED / UNIT | PASS | 51 / None | 0.201 |
| llm-native-helpers | LLM / NATIVE | PASS | None / None | 10.94 |
| voice-jvm | VOICE / UNIT | FAIL | 52 / 52 | 137.103 |
| services-jvm | SERVICES / UNIT | PASS | 134 / 134 | 24.991 |
| evolution-jvm | EVOLUTION / UNIT | PASS | 40 / 40 | 59.528 |
| nexus-jvm | NEXUS / UNIT | PASS | 100 / 100 | 138.3 |
| interface-m51 | INTERFACE / UNIT | PASS | 36 / 15 | 259.383 |

## Android

{"status": "NOT_RUN", "kind": "EMULATOR", "reason": "SAFE_PROFILE"}

## APK

Toutes les APK restent NON QUALIFIÉES tant que la réception Android du même build ne passe pas.

## Décisions

CORE/LLM, racine LAB_CLOUD, JNI, modèles, appareils personnels et fusion : non autorisés par ce laboratoire.

## Non exécuté

Génération réelle LLM, matériel personnel, nouvelles connexions runtime : NOT_RUN.

Rapports complets : report.json, logs/, APK et manifeste SHA256. Durées de build : horloge monotone hôte, pas latence Android.

Artefacts Actions conservés 90 jours ; télécharger evidence.zip avant expiration. Ce dashboard ne déclenche aucun build.
