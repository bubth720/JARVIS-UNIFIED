# AUD-00 — Contrats d'intégration, versions et risques de régression

Observé le 11/11/2026 en lecture seule. « Implémenté » ne veut pas dire « raccordé » : aucun appel runtime intermodule n'est actif dans une APK de production.

## 1. Frontières réellement présentes dans le code

| Appelant → appelé | Contrat / type | Où | Transport | État |
|---|---|---|---|---|
| CORE UI → CORE session | `SessionCoordinator` (`SessionPhase`, `SessionState`, `SessionActions`) | JAVIS-Local-v2 `codex/m50-s1-core-ci-20261029` | in-process | Testé JVM + labo API29/35 |
| CORE session → moteur | `LocalLanguageModel` (`warmUp/generate/infer/requestStop/unload/openSession`) | idem `LocalLanguageModel.kt` | in-process | Seule implémentation : `LlamaLocalEngine` (llama-android 0.1.1) |
| CORE → événements | `CoreEventBus`, `ConversationEventPublisher`, `ModuleConnector` | `events/` | in-process | Opt-in, testé JVM |
| INTERFACE → CORE | `CoreConversationTransport` / `CoreConversationClientAdapter` / `CoreEventUiPort` | JARVIS-INTERFACE `codex/m50-s1b-android-20261104` | in-process (labo `labs/m50-s1`, `fr.jarvis.lab.m50s1`, minSdk 29) | Réponses LAB/SYNTHETIC uniquement |
| LLM app → natif | `LlamaNative` : `create/begin/cancel/load(path)/generate/generateP2/generateStream/allocations/unload/destroy` | JARVIS-LLM `LlamaBackend.kt` + `app/src/main/cpp/bridge.cpp` | JNI | Linux réel testé ; Android génération NOT_RUN |
| LLM ↔ CORE (P2) | contrat P2 SHA `3deeaf35…ef8` | JARVIS-LLM `fixtures/p2-contract` | Binder entre APK fixtures | Fixtures uniquement ; `androidCrossApkExecuted=false` |
| VOICE ↔ CORE | 005K contrats, pilote Binder authentifié | JARVIS-VOICE `feat/voice-core-bridge-005k`, `feat/voice-bridge-pilot` | Binder | Génération bloquée, non activé |
| NEXUS ← hôte | `KnowledgeCatalogService` + `AccessPolicy`, `KnowledgeReadPort`, `ReadOnlyConsultationAdapter` | JARVIS-NEXUS | bibliothèque JVM | Hôte Android absent |
| SERVICES ← CORE | catalogue 17 outils, approbations durables, BRIDGE fichiers | JARVIS-SERVICES `feat/services-final-01` | aucun transport | Volontairement non raccordé |
| EVOLUTION ← hôte | `EventSink`, `Sanitizer`, scheduler piloté par l'hôte | JARVIS-VOLUTION- | bibliothèque JVM | Aucun hôte |
| Tous | Contrats v1 UNIFIED (schémas + Java/Kotlin générés) | JARVIS-UNIFIED `contracts/v1` | indépendant du transport | Non exercés par un runtime réel |

## 2. Incompatibilités à arbitrer avant CORE-01

1. **Deux moteurs LLM distincts.** CORE embarque `dev.ffmpegkit-maintained:llama-android:0.1.1` (AAR tiers, minSdk 24) ; JARVIS-LLM embarque un llama.cpp épinglé avec JNI propre, garde-fous ressources, P2 et A02 (minSdk 29). A02 n'est applicable qu'au moteur JARVIS-LLM. Garder les deux crée une copie divergente du même rôle (risque « Éviter les copies divergentes » d'UNIFIED-01).
2. **minSdk.** CORE app 24, INTERFACE app 26, labo M50-S1 29, LLM 29, VOICE 26. Importer le moteur LLM dans l'app CORE historique exigerait de monter son minSdk : interdit par `JAVIS-Local-v2/AGENTS.md` sans autorisation. Le labo M50-S1 (29) est compatible sans changement.
3. **Chargement par chemin.** `LlamaNative.load(handle, path: ByteArray, …)` prend un chemin ; A02 exige que le moteur consomme le FD scellé (directement, ou `/proc/self/fd/N` seulement après vérification du FD). Changement d'ABI JNI → fichier protégé par les gardes historiques (`app/src/main/cpp/bridge.cpp`).
4. **Prompt système.** `LocalLanguageModel.generate(prompt, systemPrompt, …)` ↔ `generateP2(..., system)` : mapping documenté comme décision ouverte dans UNIFIED D4-02.
5. **Annulation / libération.** CORE `requestStop()` par défaut `UNSUPPORTED`, `unload()` `UNKNOWN` ; le moteur LLM expose `cancel/unload/destroy`. L'adaptateur doit remonter des états vérifiés, pas des succès supposés.

## 3. Versions observées

| Module | Kotlin / AGP / Gradle | SDK | Notes |
|---|---|---|---|
| CORE | Kotlin 2.0.21, AGP 8.7.3, Gradle 8.10.2 (CI) | min24/target35, arm64 | pas de wrapper sur main |
| LLM | wrapper Gradle 8.11.1, JDK 21, NDK 28.1.13356709, CMake 3.22.1 | min29/target36, arm64 | llama.cpp épinglé via `tools/prepare-native.sh` |
| INTERFACE | Compose, wrapper | min26/target35 (app), min29 (labo M50) | |
| NEXUS | Java 17, Gradle 8.10.2 | JVM + adaptateur API24 | |
| EVOLUTION | Kotlin 2.1.20, Gradle 8.13 | JVM | |

## 4. Risques de régression d'intégration

- Gardes de préservation **portées sur une base figée** déclenchées sur toutes les PR (`pull_request:` sans filtre) : VOICE `check_style_preservation.py` (base `99d4073`), NEXUS `nex-07.yml` → `check-prefusion.py`, LLM F3B `verify.py` (corrigé par `59ce4d4`). Elles rendent les CI rouges sans défaut produit ; les corriger en exécutant la garde dans son contexte historique, jamais en la supprimant.
- Fichiers protégés touchés par toute intégration native : `bridge.cpp`, `LlamaBackend.kt` (LLM), `SessionCoordinator.kt` (CORE). Chaque modification doit déclarer son successeur de garde, comme `tools/check-f3b-successor-r02.py`.
- ~120 PR brouillon ouvertes sur 8 dépôts ; aucune base commune de livraison. UNIFIED-01 doit geler un lockfile de SHA avant tout assemblage.
