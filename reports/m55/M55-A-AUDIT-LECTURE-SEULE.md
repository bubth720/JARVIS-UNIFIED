# M55-A — Audit, sécurité et remise à niveau Android (lecture seule)

**Date :** 12/11/2026. **Mode :** lecture seule stricte. Aucun commit, aucun push, aucune PR, aucune CI déclenchée, aucune installation pendant M55-A. Les résultats cités sont ceux des runs datés, identifiés par leur SHA.

**Décision : NO-GO-A, levable.** Les protections d'intégrité du modèle sont actives et prouvées sur Android. En revanche, trois critères de la porte ne sont pas remplis :
1. un échec Android historique n'est pas expliqué (assertion SAF sur API 29) ;
2. trois PR d'entrée ont une CI rouge, à cause de gardes historiques non migrées en mode successeur ;
3. la racine d'autorité opérateur (A01) reste ouverte.

Quatre corrections minimales, présentées au §8, lèveraient les deux premiers points. Le troisième relève de ta décision.

## 1. Les 8 modules : état réel

| Module | Dépôt | Branche de référence | SHA | PR (brouillon) | Dernière CI | Tests | Statut M55-A |
|---|---|---|---|---|---|---|---|
| CORE | JAVIS-Local-v2 | `codex/m50-s1-core-ci-20261029` | `5da9838` | #27 (clean) | 2 × `regression` SUCCESS (runs 41731949559 / 41731937156, 03/11) | Gardes M50, lot3, lot2, FUSION02 ; 20 tests Python ; Gradle / Android NOT_RUN dans cette PR | Réutilisable : 6 sources compilées **sans modification** dans V1-A et V1-B |
| LLM | JARVIS-LLM | `codex/jarvis-v1b-conversation-performance` | `2e01177` | #17 (unstable), #16, #14 | V1-B : NDK, Linux sans modèle, émulateurs API 29/35 SUCCESS ; Linux avec modèle : 37 PASS, porte de dialogue 3/4 (run 43186877283). PR #17 : `verify` FAIL (§4) | 34 tests natifs adversariaux, 12 JNI synthétiques, 37 avec le modèle réel | Génération réelle prouvée ; sécurité A02 PASS ; A01, A04 à A09 ouverts |
| VOICE | JARVIS-VOICE | `feat/voice-expressive-v3-android` | `92d0745` | #27 (unstable), #26 | `compile-and-tests`, `android-keystore`, `android-library-crypto-playback`, `build` SUCCESS ; `test-and-build` et `build-and-audit` FAIL (§4) | 14 JVM de politique, 6 AndroidKeyStore instrumentés | Pocket TTS réel non qualifié sur appareil ; profil B absent du labo |
| INTERFACE | JARVIS-INTERFACE | `feature/interface-cockpit-v2-008` ; `labs/v1b` | `22c2493` ; `d592505` | #22 (clean), #21, #19, #18 | #22 : 66 JVM, Lint 0 erreur, 27 tests Android par profil (runs 42995632626 / 42995632542) ; V1-B : 5/5 instrumentés sur API 29 et 35 (run 43186945601) | Voir à gauche | Cockpit V2 statique (sphère 2D) ; V1-B PASS sur la mécanique |
| UNIFIED | JARVIS-UNIFIED | `codex/jarvis-v1b-conversation-performance` | `1733386` | #25 (coordination), #23 | Aucune CI de code | — | Pilote documentaire ; portes G0 à G4 définies |
| NEXUS | JARVIS-NEXUS | `codex/reuse-first-r1plus-20261108` | `b7d9d88` | #14 (unstable), #13 | CI dédiée SUCCESS : 108 JVM + 10 Python (run 42523712059) ; NEX-07 FAIL (§4) | Voir à gauche | Labo uniquement ; aucune écriture, aucune migration |
| SERVICES | JARVIS-SERVICES | `mission/m50-integrated-beta-20261029` | `8d80d09` | #12 (clean, documentaire) | Historique | — | Écriture OFF par contrat ; hors chemin critique V1 |
| EVOLUTION | JARVIS-VOLUTION- | `mission/m50-integrated-beta-20261029` | `84ebc2e` | #6 (clean, documentaire) | Historique | — | Diagnostic sans auto-réparation ; hors chemin critique |

## 2. Matrice des protections historiques

| Protection | Où elle vit | Preuve exécutée | État |
|---|---|---|---|
| Intégrité du modèle (A02) : memfd scellé, 4 sceaux, SHA re-haché, identité inode, aucun chemin hôte | LLM `a02/` | Linux + Android, bac à sable de l'app, API 29/35 (runs 43186877283, 43186945601) | **ACTIVE — PASS** |
| Chargeur par chemin non exporté | LLM `a02_bridge.cpp` | `nm` (NDK) + `verify_apk.py` | **ACTIVE — PASS** |
| Politique moteur 0.6B (contexte 512 ou 768, 1 thread, sortie bornée) | `native_configuration.h` (inchangé) | gardes 003e, 003f, f3a, f3b ; refus 129/257 | **ACTIVE — PASS** |
| Annulation (Stop) | `generate()` protégé + CORE `SessionCoordinator` | Stop en flux : 4 à 5 ms sur API 29/35 ; Linux CANCELLED | **ACTIVE — PASS** |
| Révocation, isolation des observateurs (A03) | LLM PR #17 (candidat) | 2 tests de régression **NOT_RUN** (la CI s'arrête avant, §4) | **OUVERTE** |
| Autorité opérateur indépendante (A01) | — | Seulement un diagnostic Keystore (M51) | **OUVERTE — décision requise (G-ROOT)** |
| Lease / broker, échéance partagée (A04, A08) | LLM M51 | Constat d'audit M51 seulement | **OUVERTE** |
| Transitions terminales scellées (A07) | LLM M51 | Constat M51 | **OUVERTE** |
| Contexte non attesté (A06) | LLM M51 | Constat M51 | **OUVERTE** |
| Fuite de chemins dans les erreurs (A05) | LLM | Trace A02 sans chemin (vérifiée) ; erreurs historiques non revues | **PARTIELLE** |
| Pic mémoire borné (A09) | A02 `require_budget` | Refus `A02_MEMORY_BUDGET_REFUSED` PASS ; réservation atomique globale non prouvée | **PARTIELLE** |
| Refus du replay | VOICE `PilotAuthorization` ; NEXUS #14 | Tests JVM (replay, bail expiré, octroi) ; 108 JVM NEXUS PASS | **ACTIVE en labo** (pas de fil réel) |
| Consentement mémoire | CORE `feat/mem-02` (labo opt-in) ; V1-B : mémoire en RAM seulement | Labo JVM | **ACTIVE** : rien de durable n'est stocké |
| Écriture OFF | SERVICES #12 (contrat) ; NEXUS sans écriture | Garde NEXUS (non-mutation SQLite) PASS | **ACTIVE** |
| Isolation LAB_CLOUD | LLM #16 (NO-GO LAB_CLOUD) | Constat ; non relu en détail dans M55-A | **À confirmer** |
| testOnly, aucune permission, aucun réseau | V1-A, V1-B, cockpit 008 | `verify_apk.py` ; APK 008 sans INTERNET ni RECORD_AUDIO | **ACTIVE — PASS** |

## 3. Contrats réels inspectés (sans supposer leur remplacement)

- **CORE** : `SessionCoordinator` (`send` → `begin` → `actions.chat`, phases READY / THINKING / ERROR, `prepared` conservé après une erreur), `LocalLanguageModel`, `InferenceContract.validateInference` (budget **en octets** : `octets + maxTokens + 128 ≤ contexte`), `CoreEventBus`.
- **LLM** : `NativeBridge` protégé (`generate` P2, `SynchronousStream`, `onNativePrepared`, `onNativeEvent`), plus les ajouts A02 et V1-B (`loadSealedFd`, `generateStreamTurns`, `countTurnsTokens`, `setOutputCeiling`).
- **INTERFACE** : `CoreConversationTransport` / `CoreConversationClientAdapter` (ACK, drainage, UNKNOWN, Stop) ; cockpit 008 : `HomeViewModel` (session en RAM), DataStore JSON v1 (13 fichiers protégés).
- **VOICE** : `PilotAuthorization` / `PilotWire` (hello, request, status ; refus `NATIVE_AUTHORITY_UNAVAILABLE`), `LocalProxy`, `PcmPlayer`. Aucun pont CORE ↔ VOICE activé.

## 4. Échecs Android et CI : causes racines

| # | Échec | Cause racine | Classe | Correctif minimal |
|---|---|---|---|---|
| E1 | Labo V1-A, API 29 : « Métadonnées GGUF invalides » | SELinux interdit la réouverture `/proc/self/fd` du memfd | Application | **Corrigé** (`168f562`, ouverture servie depuis le fd scellé) |
| E2 | Labo V1-A, API 29 : `mmap` EPERM | Un noyau antérieur à 6.7 refuse `MAP_SHARED` sur un memfd scellé en écriture | Application | **Corrigé** (`c00035b`, `MAP_PRIVATE` en lecture seule) |
| E3 | M51-R1, API 35 : ANR `com.android.phone` / SystemUI **avant** l'installation de JARVIS | Banc Intel/HVF sans KVM | **Environnement** | Ne se reproduit pas sur ubuntu-24.04 + KVM : API 35 démarre et passe 5/5 dans V1-A et V1-B |
| E4 | M51-R1, API 29 : assertion SAF de référence FAIL | **INCONNUE** : `picker.jsonl` jamais collecté pendant le test | Inconnue | Proposé : collecte en lecture seule du témoin SAF sur banc KVM (§8, P4) |
| E5 | M51 : crash Compose (SnapshotStateObserver) sur API 29 | Non reproduit depuis ; cockpit 008 : 27 tests Android PASS sur API 34 | Inconnue sur API 29 | Inclus dans P4 (rejouer le scénario sur API 29 et 35) |
| E6 | LLM #17 `verify` FAIL | `docs/mission-003f-f3b/verify.py` exige que `SENSITIVE.patch` s'applique à `bridge.cpp` ; la branche du candidat a modifié `bridge.cpp` | Garde historique en mode préimage | P1 : brancher la garde successeur `check-f3b-successor-r02.py` (`59ce4d4`), sans toucher la garde d'origine |
| E7 | VOICE #27 `test-and-build` / `build-and-audit` FAIL | `check_style_preservation.py` refuse la modification de `voiceStudio/build.gradle.kts` (fichier protégé : `applicationId` du pilote) | **Défaut réel de la PR** ; la garde a raison | P2 : sortir le pilote dans un module ou une variante qui ne touche aucun fichier protégé (ou appliquer le successeur `1a54da8` si tu le valides) |
| E8 | NEXUS #14, NEX-07 FAIL | La garde de périmètre exacte refuse les ajouts | Garde historique en mode préimage | P3 : garde successeur `d2b59e0`, sans assouplir NEX-07 |
| E9 | CI V1-B, porte de dialogue 3/4 | Connaissances du 0.6B (« Italie : Lione ») | Limite du modèle | Hors M55-A (M55-B) |

## 5. Matrice de compatibilité (relevée sur les fichiers de build, au SHA indiqué)

| Module @ SHA | AGP | Kotlin | Gradle | NDK | minSdk / target / compile | ABI | Compose |
|---|---|---|---|---|---|---|---|
| CORE @ `5da9838` | 8.7.3 | 2.0.21 | — | — | 24 (app), 29 / 35 / 35 | arm64-v8a | — |
| LLM @ `2e01177` | 8.10.1 | — | 8.11.1 | 28.1.13356709 | 29 / 35–36 / 36 | arm64-v8a (+ x86_64 labo) | — |
| INTERFACE V1-B @ `d592505` | 8.9.2 | 2.1.20 | 8.13 | 28.1.13356709 | 29 / 35 / 35 | arm64-v8a + x86_64 | — |
| INTERFACE cockpit @ `22c2493` | 8.9.2 | 2.1.20 | 8.13 | — | 26 / 35 / 35 | — | oui |
| INTERFACE R1+ @ `d569ce8` | 8.9.2 | 2.1.20 | 8.13 | — | 26 / 35 / 35 | — | BOM 2025.04.01 |
| VOICE @ `92d0745` | 8.9.2 | 2.1.20 | 8.13 | — | 26 / 35 / 35 | arm64-v8a (x86_64 en test) | — |
| NEXUS @ `b7d9d88` | 8.7.3 | — | 8.10.2 | — | 24 / 35 / 35 | — | — |
| SERVICES / EVOLUTION | — | — | 8.13 | — | — | — | — |

Points d'attention :
- **CORE** est en Kotlin 2.0.21 / AGP 8.7.3, mais ses sources compilent sans modification sous 2.1.20 / 8.9.2 dans V1-A et V1-B (prouvé).
- **LLM** utilise compileSdk 36 et AGP 8.10.1, alors que l'hôte est en 35 / 8.9.2. Seule la bibliothèque native est consommée (via CMake), donc ce n'est pas un conflit aujourd'hui.
- **L'assemblage M55-E** devra fixer une seule chaîne d'outils, a priori AGP 8.9.2, Kotlin 2.1.20, Gradle 8.13, NDK 28.1, compile/target 35, minSdk 29. VOICE et le cockpit (minSdk 26) remontent alors à 29.

## 6. État de référence figé et plan de retour arrière

- **Référence reproductible** : les SHA du §1, plus `4ed3f99` (V1-A) et `2e01177` / `d592505` (V1-B), avec le modèle `ac2d9771…524a`.
- **Retour arrière** : toutes les branches sont additives. Aucun `main` n'a été modifié, aucune migration ni donnée persistante n'a été créée. Un retour consiste à abandonner une branche ou une PR brouillon. Les APK sont testOnly, avec des paquets distincts (`fr.jarvis.v1a.lab`, `fr.jarvis.v1b.lab`, `com.jarvis.voice.studio.expressivev3`) : aucune n'écrase une application installée.

## 7. Journal des risques

| Risque | Gravité | Réponse |
|---|---|---|
| A01 ouverte : l'autorisation du modèle repose sur ta déclaration, pas sur une racine signée | Élevée pour une V1, acceptable en labo | Décision G-ROOT ; à ne jamais simuler |
| Budget CORE en octets, trop conservateur (questions de 47 à 312 octets) | Moyenne | Extension du contrat CORE à revoir (M55-B), sans modifier CORE sans accord |
| Latence de 11 à 21 s avant le 1er jeton sur émulateur, 1 thread | Élevée pour la voix (M55-C/E) | Seuls leviers : modifier la politique protégée ou changer de modèle (décision) |
| Fichiers de voix B et PNG d'avatar privés | Élevée (confidentialité) | Jamais dans GitHub ; import local par le propriétaire |
| Secrets dans les journaux | Moyenne | Traces A02/V1-B sans chemin ni contenu ; à vérifier pour VOICE et NEXUS |
| Banc HVF/ANR trompeur | Moyenne | Utiliser exclusivement le banc ubuntu-24.04 + KVM |

## 8. Plan de corrections minimales proposé (à valider, rien n'est exécuté)

| ID | Dépôt / PR | Changement | Fichiers touchés | Protections |
|---|---|---|---|---|
| P1 | LLM #17 | Brancher la garde successeur F3B (`check-f3b-successor-r02.py`) dans son workflow ; laisser la garde d'origine intacte ; exécuter enfin les 2 tests A03 | workflow + script successeur (déjà écrit) | inchangées |
| P2 | VOICE #27 | Sortir l'`applicationId` du pilote du fichier protégé (module ou variante séparée) | `voiceStudio/build.gradle.kts` **restauré**, nouveau module | garde de préservation inchangée, redevient verte |
| P3 | NEXUS #14 | Garde de périmètre successeur (`d2b59e0`) pour les ajouts du labo | workflow + script successeur | NEX-07 inchangé |
| P4 | INTERFACE | Rejouer la référence M51-R1+ sur API 29 et 35 (banc KVM), en lecture seule, avec collecte du témoin SAF et des journaux Compose | nouveau workflow de diagnostic seulement | aucune modification applicative |

Après P1 à P4 : GO-A si les CI redeviennent vertes et si E4/E5 sont expliqués (ou classés environnement, preuves à l'appui). Chaque correctif serait livré sur une branche isolée, avec une PR brouillon et des preuves au SHA exact. Aucune fusion.

## 9. Décision GO / NO-GO-A

**NO-GO-A** à ce SHA :
- E4 n'est pas expliqué ;
- les CI d'entrée #17, #27 et #14 sont rouges ;
- A01 est ouverte.

Ce qui est déjà acquis pour M55-B : la génération réelle locale sur Android (API 29/35), l'annulation, le déchargement, les rechargements et l'intégrité du modèle. M55-B partirait donc de V1-B, sans repartir de zéro.

### Validations demandées

1. Autoriser l'exécution de P1 à P4 : branches isolées, CI et PR brouillons.
2. Pour A01 : accepter un GO-A « labo » sans racine indépendante, avec ton autorisation de modèle comme seule source, ou exiger d'abord la racine G-ROOT.
3. Pour la suite de M55-B : garder le 0.6B seul, ou ouvrir l'étude séparée du 1.7B, comme le dossier le permet « après accord ».
