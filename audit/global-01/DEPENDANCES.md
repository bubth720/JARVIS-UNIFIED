# Cartographie réelle des dépendances (14/11/2026)

L'application unifiée est **INTERFACE `labs/v3`** (paquet `fr.jarvis.v3`), branche `ccr-5cf17ed2-phgk00`.

**Construction :** elle compile des sources **épinglées** des autres dépôts. Aucune dépendance binaire maison.
Les épinglages se trouvent dans `.github/workflows/v3-cockpit.yml` ; un test JVM vérifie qu'ils correspondent
au SYSTEM BLUEPRINT de l'application.

```
                      ┌──────────────────────── INTERFACE labs/v3 (application) ─────────────────────────┐
                      │  CockpitActivity / CockpitScene / CommandCenter / PaletteSheet / AvatarView        │
                      │  conv/ : ConvApp → ConvSession → ConversationContext (Persona, WorkingMemory,      │
                      │          ActionGuard, KnowledgePlanner, Provenance) ; ConversationJournal          │
                      └───────┬───────────────┬──────────────────┬────────────────┬───────────────────────┘
                              │               │                  │                │
           V1-B transport (inchangé)   STT whisper.cpp     Pocket TTS        NEXUS (sources)   CORE mémoire (6 fichiers)
           V1bCoreTransport            v1.8.4 (épinglé)    VOICE 92d0745     06ccf98           5da9838 (lock blob+taille)
                 │                                                            │                    │
        CORE SessionCoordinator (5da9838,                         BundledNexusStorage       ConfirmedMemoryStore
        sources V1 verrouillées)                                  → androidx.sqlite          (SQLite plateforme,
                 │                                                   bundled 2.5.2           noBackupFilesDir)
        ConvLanguageModel (dérivé A02LanguageModel)                  (FTS5, SQLite 3.46.0)
                 │
        LLM A02 natif (JARVIS-LLM 2e01177) — llama.cpp épinglé — modèle Qwen3-0.6B (SHA ac2d9771, importé par l'utilisateur)
```

## Tableau

| Module | Dépôt @ commit | Mode d'intégration | Garde |
|---|---|---|---|
| CORE (session, contrats) | JAVIS-Local-v2 @ 5da9838 | 6 sources via `labs/v1/tools/prepare_sources.py` | Verrou `labs/v1/sources.json` |
| CORE (mémoire consentie) | JAVIS-Local-v2 @ 5da9838 | 6 sources via `labs/v3/tools/prepare_core_memory.py` | Verrou `labs/v3/core-memory.lock.json` |
| LLM A02 | JARVIS-LLM @ 2e01177 | Arbre natif vérifié + JNI | Verrou natif, commit et arbre exacts |
| Étude modèle | JARVIS-LLM @ 3e2560e (données seulement) | Banc et manifestes | SHA des poids contrôlés |
| VOICE | JARVIS-VOICE @ 92d0745 | Modules `:pocket` (et règles de réaction reprises en code) | `check_reuse.py` ; ⚠ A-003 |
| STT | whisper.cpp v1.8.4 | Module `:stt` | Source épinglée |
| NEXUS | JARVIS-NEXUS @ 06ccf98 | Sources `nexus-core` + `nexus-android-store` | Inchangées ; stockage adapté par l'application |
| SQLite embarqué | androidx.sqlite:sqlite-bundled-android 2.5.2 | Dépendance Maven (Google) | Accord du propriétaire (14/11) |
| V1, V1-A, V1-B, M55-D, historique | INTERFACE (gelés) | Sources compilées inchangées | `labs/v3/tools/check_scope.py` (430 fichiers gelés) |
| SERVICES | JARVIS-SERVICES | **Non intégré** | — |
| EVOLUTION | JARVIS-VOLUTION- | **Non intégré** (désactivé) | — |
| ARCH-01 (contrats PC/Android) | JARVIS-UNIFIED (PR #26 brouillon) | Contrats Python simulés, **non branchés** dans l'application | Tests `tooling/arch01` |

## Incompatibilités et écarts constatés

1. **Politique A02.** Contexte 768, 1 thread, sortie 128 et 3 échanges relus au plus. Elle limite mécaniquement
   la longueur des réponses et du contexte. Toute évolution relève de LLM et d'une décision explicite.
2. **Deux SQLite dans le même processus.**
   - La plateforme : CORE mémoire.
   - L'embarqué : NEXUS.

   C'est un choix assumé : les bases ne sont jamais partagées entre les deux.
3. **VOICE 92d0745.** Ce commit échoue à ses propres gardes historiques (A-003).
4. **ARCH-01.** Le contrat `ModelBackend` n'est pas encore le chemin réel de l'application (l'application
   appelle `ConvLanguageModel` directement). L'alignement est à prévoir lors d'un éventuel changement de modèle.
5. **Portes CI historiques UNIFIED et LLM.** Elles sont rouges pour des raisons externes au code (A-001, A-002).
