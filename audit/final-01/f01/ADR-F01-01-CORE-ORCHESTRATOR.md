# ADR-F01-01 — CORE, orchestrateur central et autorité unique

**Statut :** ACCEPTÉ par le propriétaire le 21/11/2026 (décision R-03). Aucun code de production n'est déplacé tant que les contrats ci-dessous ne sont pas validés.

## Contexte (vérifié sur les SHA)

- **APK V3** : INTERFACE `e6489bf011c804fcbb699f41416e4b389e50d66a`.
- **Fichiers CORE compilés** : CORE `5da98383ed12cb5a54e896fbe57560bacc432fb5`, verrou V1 et `labs/v3/core-memory.lock.json`.
  - `SessionCoordinator`, `InferenceContract`, `LocalLanguageModel`, `Models` ;
  - `CoreEventBus`, `CoreSessionEvents` ;
  - mémoire : `MemoryApprovalWorkflow`, `ConfirmedMemoryStore`, `MemoryContextAssembler`, `MemoryRecallIndex`, `MemoryExportService` ;
  - `IdentityCodec`.
- **CORE contient déjà**, sans que l'APK les utilise : `orchestration/IntentRouter`, `orchestration/TaskCoordinator` et `orchestration/CoreCapabilities`.
- **INTERFACE contient un orchestrateur de fait** : `labs/v3/app/src/main/java/fr/jarvis/v3/conv/`.

| Rôle | Fichiers | Dépendances |
|---|---|---|
| Orchestration (état du tour, voix, LLM, documents, mémoire) | `ConvSession.kt` (380 lignes), `ConvApp.kt` | Android, CORE, VOICE, INTERFACE V1 |
| Adaptateurs de producteurs | `ConvLanguageModel.kt`, `LocalKnowledge.kt`, `BundledNexusStorage.kt`, `ConsentedMemory.kt`, `ConversationContext.kt` | CORE, NEXUS, AndroidX SQLite |
| **Politique pure** (sans Android) | `KnowledgePlanner`, `DocumentaryAnswer`, `ActionGuard`, `RepetitionGuard`, `SpeechGuard`, `WorkingMemory`, `Persona`, `Provenance`, `QuickReaction`, `MemoryIntent`, `ConversationJournal` (≈ 840 lignes) | aucune |

## Décision

1. **CORE** est l'unique autorité sur les points suivants :
   - le cycle de vie d'un tour (accepter, refuser, annuler, terminer) ;
   - les politiques (documents, actions, mémoire, persona) ;
   - le contexte envoyé au modèle ;
   - toute écriture durable : mémoire confirmée, journal, permissions.
2. **INTERFACE** garde l'affichage, l'avatar, la sphère, la navigation, les gestes, l'accessibilité et la présentation des notices. Elle ne décide plus d'aucune politique.
3. La couche `fr.jarvis.v3.conv` actuelle reste en place comme **adaptateur de compatibilité**, derrière un drapeau, jusqu'à la preuve de parité.
4. **Un seul moteur LLM actif** : CORE choisit le backend derrière `InferenceContract` / `ModelBackend` ; aucun second orchestrateur n'est créé.

## Migration progressive

Chaque étape est réversible.

| Étape | Contenu | Preuve exigée (porte GO/NO-GO stricte, `tooling/final01/gonogo.py`) | Retour arrière |
|---|---|---|---|
| **M0** (F01, fait) | Contrats décrits ; diff d'API outillé ; versions candidates testées | `api_surface`, `candidate_check`, tests 17/17 | Sans objet |
| **M1** | Contrat `ConversationTurnPort` (CORE, version 1, additif). Entrée : texte ou transcription, voix oui/non, identifiant de session. Sortie : réponse finale, notices, sources, provenance (« Pourquoi ? »), état (`ACCEPTED`, `REFUSED`, `CANCELLED`, `FAILED`, `UNKNOWN`). | Diff d'API CORE `ADDITIVE` (jamais `BREAKING_CANDIDATE`) ; tests de contrat positifs et négatifs | Ne pas consommer le port |
| **M2** | Copie **byte-identique** des 11 fichiers de politique pure dans un module CORE `core-policy` (JVM pur). INTERFACE continue d'utiliser sa propre copie. | Les 37 tests JVM actuels passent **contre les deux copies** ; garde d'identité d'octets entre les copies | Supprimer le module CORE neuf (jamais de données touchées) |
| **M3** | Implémentation CORE du port, en réutilisant `SessionCoordinator`, `TaskCoordinator` et la mémoire CORE. Adaptateur INTERFACE `CoreTurnAdapter` derrière le drapeau `coreOrchestrator` (désactivé par défaut). | **Parité** : corpus fixe de tours rejoué par les deux chemins avec un modèle simulé déterministe ; réponse, notices, sources et état identiques ; puis audits émulateur (f, g, h, i, c8, F2, Q, R, S, T, j, m) verts dans les deux positions du drapeau | Drapeau désactivé (aucune migration de données) |
| **M4** | Drapeau activé par défaut sur une branche candidate ; ancien chemin conservé une version | Campagne complète API 29/35 verte ; ensuite seulement, DEVICE-01 | Drapeau désactivé |
| **M5** | Retrait de l'ancien chemin INTERFACE | Accord du propriétaire, spécifique au SHA | Revert du commit |

## Invariants de non-régression

Ce sont les tests de parité M3.

- Aucune écriture durable sans CORE.
- La mémoire durable n'est écrite qu'après confirmation du texte exact (b3, h, g6).
- Un document n'est jamais une consigne (F4, L, Q) ; une valeur absente ou contradictoire n'est jamais inventée (c8, F2, R).
- Fermeture idempotente et libération confirmée du moteur (j, h4).
- Le journal tolère les lignes tronquées (S) ; le stockage plein est géré proprement (T).
- Mode avion ; aucune permission nouvelle ; `allowBackup=false` et `dataExtractionRules`.
- La sphère et l'avatar ne dépendent jamais de l'orchestrateur (K, P).

## Hors périmètre de cette ADR

- Migration de données utilisateur : aucune, les formats restent identiques.
- Changement de modèle : aucun.
- Toute fusion vers `main`.
