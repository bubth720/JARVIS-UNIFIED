# Mission P0 — A02 et intégration V1-A : état vérifié (11/11/2026, ~20:50 UTC)

**Décision : NON TERMINÉE — GO-LAB-ONLY non atteint.** Les phases A et B (code) sont livrées. Il manque la preuve finale de la phase C : la conversation réelle sur émulateur via l'APK V1-A n'a pas encore réussi. Le dernier échec (run 43093246716) n'est pas diagnostiqué : les journaux et artefacts GitHub renvoient HTTP 502, et le run suivant (43095604469) reste en file d'attente.

## Branches et commits (aucune fusion dans `main`, aucune installation sur appareil)

| Dépôt | Branche | Commit | Rôle |
|---|---|---|---|
| bubth720/JARVIS-LLM | `claude/repos-folders-analysis-sr65sg` | `216ca0d6636fbbac28b75a54fb8df736c986c8d2` | A02 (`a02/`), streaming, modèle autorisé épinglé |
| bubth720/JARVIS-INTERFACE | idem | `5340d6328cdc5cc078808b3586dffe401adcfad7` | Labo V1-A (`labs/v1a/`) : CORE + A02 + INTERFACE |
| bubth720/JARVIS-VOICE | idem | `1a54da86337394ab702ae35c45c57574cef130cb` | VOICE-00 (portée des gardes historiques) |
| bubth720/JARVIS-NEXUS | idem | `d2b59e07c329f7d0bfd458a440f831bdc989c4b3` | NEXUS-00 (portée des gardes historiques, quotas préservés) |

Modèle autorisé par l'utilisateur : `unsloth/Qwen3-0.6B-GGUF` @ `50968a4468ef4233ed78cd7c3de230dd1d61a56b`, 396 705 472 o, SHA-256 `ac2d97712095a558e31573f62f466a3f9d93990898b0ec79d7c974c1780d524a`, licence déclarée apache-2.0 (vérifiée en CI). Il n'est ni commité, ni embarqué dans l'APK.

## Phase A — A02 (JARVIS-LLM)

| Test | Environnement | Résultat | Preuve |
|---|---|---|---|
| 6 gardes historiques de préservation | CI Linux | **PASS** | run 43089256668 |
| Suite adversariale native (34 cas : SHA, taille, budget, FD, TOCTOU, annulation, 100 cycles, concurrence) | Linux hôte | **PASS** | run 43089256668 |
| Suite JNI synthétique (10 cas, chargeur par chemin non exporté) | Linux hôte | **PASS** | run 43089256668 |
| Vrai GGUF via memfd scellé : génération, multi-tour, source tronquée après scellement | Linux hôte, modèle autorisé | **PASS** | run 43089256668 (24/24) |
| Streaming réel (48 fragments → COMPLETED), arrêt après 2 fragments (CANCELLED), moteur réutilisable | Linux hôte | **PASS** | idem |
| 10 cycles chargement/déchargement réels : aucune fuite de FD, shmem libérée (Δ 0 kB) | Linux hôte | **PASS** | idem |
| Build NDK arm64-v8a : ELF aarch64, alignement 16 KiB, chargeur par chemin absent | CI | **PASS** | runs 43088370615, 43089256668 |
| Suite adversariale exécutée via `adb shell` sur Android | Émulateurs API 29 et 35 | **PASS** | runs 43088370615, 43089256668 |

Mesures Linux (x86_64, **pas Android**) : RSS 59,7 → 579,8 Mo une fois chargé ; shmem scellée 381,6 Mo puis 0 après déchargement ; llama.cpp : poids 390,8 Mo, contexte 88,1 Mo, calcul 0,8 Mo.

Politique protégée du moteur respectée, sans contournement : pour Qwen3 0.6B, contexte 512 ou 768, **un seul thread**, ≤ 96 jetons générés. Le premier essai avec 2 threads avait été refusé (« Configuration native refusée », run 43088370615).

## Phase B — CORE + LLM + INTERFACE (labo M50, API 29)

| Test | Environnement | Résultat | Preuve |
|---|---|---|---|
| Garde M50 d'origine exécutée sur son commit `b9a6c19` + garde successeur (322 fichiers figés) + 5 tests Python, dont 2 négatifs | CI + local | **PASS** | runs V1-A 43089259775, 43092086007, 43093246716 |
| 9 sources Kotlin CORE/INTERFACE extraites par blob et compilées sans modification | CI | **PASS** | idem |
| Tests unitaires (12) : moteur réel derrière `LocalLanguageModel`, multi-tour, erreurs visibles, Stop, streaming ordonné, terminaux | CI + JVM locale | **PASS** | run 43092086007 (étape Gradle verte) ; 12/12 en local |
| Lint, APK arm64 + x86_64, APK de test | CI | **PASS** | idem |
| Vérification de l'APK : testOnly, aucune permission, moteur unique, aucun modèle embarqué, 16 KiB, aucun chargeur par chemin | CI | **PASS** | run 43092086007 |
| A02 dans le bac à sable applicatif (`untrusted_app`) + refus visibles + session CORE sans modèle | Émulateur API 29 | **PASS** (4/5 tests) | run 43092086007 |
| Conversation réelle CORE → A02 → INTERFACE avec le modèle autorisé (3 tours, streaming, Stop, déchargement) | Émulateur API 29 | **FAIL** | run 43092086007 : ENOENT (corrigé `5d4bea3`) ; run 43093246716 : échec, cause non lue (journaux 502) |
| Idem sur API 35 | Émulateur API 35 | **NOT_RUN** | ignoré après l'échec API 29 |

## Phase C — APK

APK testOnly construite et vérifiée en CI. Elle n'est pas publiée comme artefact : la publication n'a lieu qu'après réussite des émulateurs. Aucun SHA-256 d'APK qualifiée n'est donc déclaré. Le protocole POCO est prêt : [DEVICE-01-PROTOCOL.md](DEVICE-01-PROTOCOL.md). DEVICE-01 : **NOT_RUN**, attend ton autorisation.

## Blocages restants

1. Lire la cause de l'échec API 29 du run 43093246716, puis faire passer le run 43095604469 (en file d'attente). Blocage : indisponibilité de GitHub (HTTP 502).
2. Performances Android (TTFT, débit, PSS, température) : **NOT_RUN**. Seules des mesures Linux existent.
3. A01 (racine d'autorité opérateur) reste fermée ; A02 garantit l'intégrité des octets, pas l'autorisation.
4. Report des correctifs sur les branches des PR existantes (#17 LLM, #27 VOICE, #14 NEXUS) : nécessite ton accord.
