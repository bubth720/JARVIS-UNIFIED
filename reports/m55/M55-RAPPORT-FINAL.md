# Mission M55 — bilan d'exécution (12/11/2026)

Exécution après le « Tu as toutes les autorisations » du propriétaire.

Limites maintenues, car ce sont des protections et non des autorisations :
- aucune fusion dans `main` ;
- aucune installation sur un appareil personnel (aucun accès physique n'existe d'ailleurs) ;
- aucune protection désactivée ;
- aucune image ni voix privée publiée ;
- branches isolées et PR brouillons uniquement.

Toutes les mesures proviennent d'émulateurs x86_64 ou de l'hôte Linux de CI, **jamais d'un téléphone**.

## Décisions

| Porte | Décision | Motif |
|---|---|---|
| **GO-A** | **GO (laboratoire)** | P1 à P4 vertes ; échecs Android historiques expliqués par l'environnement, avec preuves ; A01 acceptée par le propriétaire pour le labo ; A04 à A09 restent des risques ouverts |
| **GO-B** | **GO (laboratoire), avec réserve de qualité** | Génération réelle sur Android API 29/35 (V1-B), 2e tour cohérent sur le prénom, annulation sûre, ressources et latences mesurées. Qualité insuffisante pour une V1 : 0.6B à 13/30 au banc ; le 1.7B (21/30) n'est pas encore qualifié sur Android |
| **GO-C** | **NO-GO-C (non exécuté)** | Aucun microphone réel en CI ni sur émulateur ; aucun STT français local qualifié (seul l'AAR tiers `whisper-android` existe, de provenance non vérifiée) ; profil vocal B privé, non accessible |
| **GO-D** | **GO (laboratoire)** | Sphère 3D tactile, avatar 2.5D événementiel, modes et régulateur, sans régression ; API 29/35 PASS |
| **GO-V1 (E)** | **NO-GO-V1** | E exige GO-C, et un test micro → LLM → TTS en mode avion ; rien n'est simulé |

## Rapport par module (format Annexe 4)

### M55-A — Audit, sécurité, Android

- **Dépôts / branches / PR :**

  | Correction | Dépôt | Branche | Commit | PR | Cible |
  |---|---|---|---|---|---|
  | P1 | LLM | `codex/m55-a-p1-llm-f3b-successor` | `61ae3a4` | #18 | #17 |
  | P2 | VOICE | `codex/m55-a-p2-voice-successor` | `cb32fbb` | #28 | #27 |
  | P3 | NEXUS | `codex/m55-a-p3-nexus-successor-scope` | `b9485d2` | #15 | #14 |
  | P4 | INTERFACE | `codex/m55-a-p4-r1plus-kvm-diagnostic` | `beefbb5`, puis `ecdebf8` (affichage seul, `[skip ci]`) | #23 | #21 |

- **Tests :**
  - P1 : « Android prototype checks » **PASS** (run 43246758097 ; rouge sur #17 auparavant).
  - P2 : 4/4 workflows **PASS** (runs 43082419213 / 222 / 271 / 678, sur `1a54da8`) et 6/6 tests négatifs.
  - P3 : `jvm` et `android-host` **PASS** (run 43246821703).
  - P4 : diagnostic R1 **inchangé**, sur KVM (run 43247150539).
    - API 29 : préflight système strict PASS (13 échantillons, aucun ANR) ; SAF 1/1, navigation (deux orientations) 1/1, projet 1/1, capture + réglages 2/2 **PASS** ; témoin `picker.jsonl` collecté (fixture de 19 octets présente avant le sélecteur).
    - API 35 : préflight **PASS**, aucun ANR.
- **Cause racine :** l'ANR d'API 35 et l'échec SAF d'API 29 de C1 venaient du banc Intel/HVF, choisi parce que la sonde refusait d'ouvrir `/dev/kvm`. Ils ne se reproduisent pas sur KVM. C'est un problème d'**environnement**, pas de l'application.
- **Correction de mon audit M55-A :** les gardes VOICE échouaient **déjà** à la base V3 `642d9c1` (dérive des bases figées). L'échec ne venait pas seulement de la PR.
- **Régressions :** aucune.
- **Risques :** A04 à A09 ouverts (bail / broker, transitions terminales, contexte non attesté, chemins dans les erreurs, réservation mémoire globale) ; racine A01 indépendante absente.
- **Prochaine action :** revoir et fusionner les PR P1 à P4 dans leurs branches cibles (décision du propriétaire), puis ouvrir les chantiers A04 à A09.

### M55-B — Intelligence locale réelle

- **Dépôt / branche :** LLM `codex/m55-b-local-intelligence`, commit `66ba810`, sans PR à ce stade.
- **Fichiers ajoutés :** `a02/tests/bench/fr-bench-30.json`, `a02/tests/study_m55b.py`, `a02/tests/bench_score.py`, `a02/models/qwen3-1.7b-q4km.json`, `tools/resolve_hf_model.py`, mode étude dans `a02/tests/jni/SealedNativeBridge.java`, workflows `m55-b-*.yml`. `bridge.cpp` et `native_configuration.h` ne sont pas modifiés ; les 4 gardes de préservation passent.
- **Manifeste 1.7B :** `unsloth/Qwen3-1.7B-GGUF` @ `d7f544eead698dbd1f15126ef60b45a1e1933222`, 1 107 409 472 octets, SHA-256 `b139949c5bd74937ad8ed8c8cf3d9ffb1e99c866c823204dc42c0d91fa181897`, apache-2.0. Résolu en lecture seule (run 43247259980). Périmètre : **étude séparée**, sans substitution.
- **Banc français de 30 demandes :** consigne de production identique, critères publiés, run 43248801190, hôte Linux.

| Configuration | Banc | factuel | raisonnement | multi-tours | refus | documents absents | ambigu | reformulation | 1er jeton p50 / p95 | Total p50 / p95 | Jetons/s | RSS chargé |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.6B, ctx 768, 1 thread (référence) | **13/30** | 2/10 | 4/5 | 2/5 | 1/2 | 0/2 | 1/2 | 3/4 | 3,3 / 4,8 s | 4,8 / 6,1 s | 15,5 | 568 Mio |
| 1.7B, ctx 768, 1 thread | **21/30** | 8/10 | 5/5 | 1/5 | 2/2 | 2/2 | 0/2 | 3/4 | 3,8 / 5,4 s | 4,8 / 6,9 s | 17,8 | 1 884 Mio |
| 1.7B, ctx 768, 2 threads (expérimental) | **21/30** | 8/10 | 5/5 | 1/5 | 2/2 | 2/2 | 0/2 | 3/4 | **2,0 / 2,7 s** | 2,6 / 3,8 s | 25,8 | 1 884 Mio |

- **20 sessions** (chargement scellé → réponse réelle → déchargement) : **PASS** pour les 3 configurations, sans fuite de descripteur et avec la shmem revenue à son niveau initial (Δ 0).
- **Erreurs réelles relevées :**
  - 0.6B : « Italie : Londres », refus excessifs (« Je ne sais pas »).
  - 1.7B : « Les Misérables… Charles Dickens », « la planète la plus proche… la Terre », « à Madrid… le français ».
  - 1.7B en multi-tours : 1/5, car la consigne a été réglée pour le 0.6B.
- **Android :** 0.6B qualifié en V1-B (API 29/35, run 43186945601) ; **1.7B NOT_RUN sur Android**.
- **Limites :** le 0.6B n'est pas comparable à un grand modèle ; 3 secondes est atteint sur l'hôte avec 2 threads, mais **n'est pas mesuré sur Android**.
- **Prochaine action :**
  1. qualifier le 1.7B sur émulateur, avec 2 threads (expérimental, la politique protégée l'admet pour le 1.7B) ;
  2. réajuster la consigne multi-tours pour le 1.7B ;
  3. décider du candidat V1.

  Point d'attention : 1,9 Gio de RSS, ce qui est acceptable sur le POCO et tendu sur le Redmi Pad SE.

### M55-C — Voix

- **Statut :** **NOT_RUN / NO-GO-C**.
- **Constats vérifiés :**
  - Pocket TTS français (modèle public « fr-6l alba ») préparé et exécuté en CI sur API 35 (`pocket-probe.yml`) ;
  - pilote V3 avec réactions chiffrées (PR #27 / #28) ;
  - profil B privé : import local par le propriétaire seulement ;
  - STT : `WhisperLocalEngine` de CORE repose sur l'AAR tiers `dev.ffmpegkit-maintained:whisper-android:1.0.0`, de provenance non vérifiée ; aucun STT français qualifié ;
  - aucun micro réel sur un émulateur de CI.
- **Pour lever le blocage :**
  1. choisir un STT (proposé : whisper.cpp compilé depuis ses sources, comme llama.cpp, avec un modèle multilingue épinglé par SHA) ;
  2. fournir un essai sur appareil (micro réel) ;
  3. importer localement le profil B.

### M55-D — Cockpit, sphère 3D, avatar

- **Dépôt / branche :** INTERFACE `codex/m55-d-cockpit-sphere`, commit `b018152`. Labo indépendant `labs/m55d` (`fr.jarvis.m55d.lab`, testOnly) et workflow `m55d-lab.yml`. La garde successeur fige V1-B, V1-A, M50 et l'application historique (372 fichiers).
- **Contenu :**
  - sphère 3D Compose (points de Fibonacci, rotation au doigt, inertie, impulsion, états) ;
  - avatar 2.5D vectoriel, avec un emplacement d'atlas PNG à importer par le propriétaire (aucune image privée) ;
  - contrat visuel v1 typé ;
  - modes CINÉMATIQUE / ÉQUILIBRÉ / ÉCONOMIE / Auto, avec régulateur à hystérésis (temps de trame p95 et état thermique) ;
  - commandes et indicateur HORS LIGNE conservés dans tous les modes ;
  - source DÉMO étiquetée, sans aucune réponse.
- **Tests (run 43252475024) :** 10 tests JVM ; scope, Lint et APK **PASS** ; 2/2 tests instrumentés **PASS** sur API 29 et API 35, en mode avion.
- **Mesures** (émulateur à rendu logiciel swiftshader, non représentatif d'un GPU de téléphone) :

| Mesure | API 29 | API 35 |
|---|---|---|
| Glissement réel sur la sphère | −2,17 rad, 19 événements | −2,72 rad, 15 événements |
| CINÉMATIQUE : FPS / p95 / saccades | 40,5 / 33 ms / 42 % | 31,8 / 50 ms / 64 % |
| ÉQUILIBRÉ | 41,5 / 33 ms / 39 % | 35,4 / 50 ms / 61 % |
| ÉCONOMIE | 42,4 / 33 ms / 34 % | 43,5 / 33 ms / 37 % |
| Auto (départ CINÉMATIQUE, 8 s) | 44,3 FPS, mode final ÉQUILIBRÉ | 46,0 FPS, mode final ÉCONOMIE |
| États animés (ÉQUILIBRÉ) | 57,5 FPS, p95 16,7 ms | 59,2 FPS, p95 16,7 ms |
| Recréation de l'activité | PASS | PASS |

Le compteur `changes` cumule les changements manuels et automatiques.

- **APK :** SHA-256 `7f2f0602e2544d9e923d2cb0fc54c1256fb3e6707d2ee450e8c99bb6274a0bd0` (artefact `m55d-evidence-b018152…`).
- **Non fait :**
  - intégration au cockpit 008 et aux événements CORE réels (relève de M55-E) ;
  - pack PNG non testé (pas d'images fournies) ;
  - impact sur le 1er jeton du LLM en exécution conjointe : NOT_RUN ;
  - aucune promesse de 60 FPS.

### M55-E — Assemblage

- **Statut :** **NOT_RUN / NO-GO-V1**, faute de GO-C.
- **Prérequis prêts :** contrat visuel v1 (D), contrat de flux de jetons et métriques (V1-B / A02), manifestes de modèles épinglés, protocole DEVICE-01 V1-B.

## Prochaine action recommandée

1. Valider et fusionner, dans leurs branches cibles (pas `main`), les PR brouillons P1 à P4 : LLM #18, VOICE #28, NEXUS #15, INTERFACE #23.
2. Lancer la qualification du 1.7B sur API 29/35 (2 threads expérimental), puis choisir le modèle V1.
3. M55-C : approuver le choix STT (whisper.cpp compilé depuis les sources) et prévoir un essai micro réel sur le POCO (DEVICE-01).
