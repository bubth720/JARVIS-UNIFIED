# AUD-00 — Chemin critique V1

## P0 — V1-A : chat texte Android, vrai GGUF, A02, mode avion

| # | Tâche | Dépôt / base | Dépend de | État 11/11 |
|---|---|---|---|---|
| P0.1 | LLM-01 : CI « Android prototype checks » verte sans affaiblir F3B | JARVIS-LLM `claude/repos-folders-analysis-sr65sg` (`59ce4d4`, sur R02 `0ef3635`) | — | **FAIT** run 43073699901 SUCCESS ; à reporter sur la branche de PR #17 |
| P0.2 | Décision moteur unique V1 : moteur JARVIS-LLM (JNI épinglé, A02) **ou** llama-android de CORE | UNIFIED (décision utilisateur) | P0.1 | **À DÉCIDER** — recommandation : moteur JARVIS-LLM ; llama-android ne peut pas porter A02 |
| P0.3 | LLM-02 : `load` depuis FD scellé ; réservation RAM avant copie ; tests adversariaux JNI | JARVIS-LLM `mission/llm-a02-native-android` depuis P0.1 | P0.1 | Prototype Linux seulement |
| P0.4 | LLM-03 : génération réelle Qwen3-0.6B sur émulateur ARM64 puis appareil ; TTFT/tok/s/PSS | JARVIS-LLM | P0.3 (pour la livraison), P0.1 (pour mesurer) | Linux x86_64 seulement |
| P0.5 | CORE-01 : adaptateur `LocalLanguageModel` → `LlamaNative` dans l'hôte minSdk29 (labo M50-S1 INTERFACE), sans réponse synthétique | JARVIS-INTERFACE (labo) + sources CORE `SessionCoordinator` | P0.2, P0.3 | SessionCoordinator + client INTERFACE qualifiés API29/35 en SYNTHETIC |
| P0.6 | INTERFACE : diagnostic borné du crash Compose API29 / ANR API35 (M51) | JARVIS-INTERFACE `codex/m51-v1-foundation` | — (parallélisable) | FAIL |
| P0.7 | APK V1-A signée + manifeste modèle + SHA + guide ; GO-LAB-ONLY tant que DEVICE-01 absent | INTERFACE/UNIFIED | P0.4, P0.5, P0.6 | ABSENT |

## P1 — modules par lots indépendants (après P0.5)

- VOICE-01 PocketTTS Android (`feat/voice-expressive-v3-android`) ; d'abord isoler ses deux CI rouges (gardes VOICE-02/005J sur toutes les PR).
- VOICE-02 STT : réutiliser Whisper de CORE (seul STT existant), push-to-talk.
- AVATAR-01 : manifeste événement→pose sur `feature/avatar-png-001`, PNG hors dépôt.
- NEXUS-01 : corriger la portée de `nex-07.yml` (le « quota preflight » n'est pas en défaut), puis adaptateur lecture seule non bloquant.
- SERVICES-01 / ZIM : chemin local, jamais dans l'APK ni GitHub.
- EVOLUTION-01 : hôte Android minimal, désactivable, sans mutation.

## P2

- UNIFIED-01 lockfile SHA + APK testOnly intégrée ; DEVICE-01 sur POCO (action humaine) ; GO / GO-LAB-ONLY / NO-GO.

## Parallélisation sûre (surfaces disjointes)

P0.3 (LLM natif) ∥ P0.6 (INTERFACE Compose) ∥ correctifs de portée CI VOICE/NEXUS. P0.5 attend P0.2 et P0.3.

## Actions humaines requises

1. Arbitrer P0.2 (moteur unique).
2. Autoriser la source/licence exacte du GGUF Android (l'autorisation Qwen3-0.6B antérieure couvrait le cloud-lab ; le workflow Linux a un repli Unsloth à valider).
3. DEVICE-01 : l'essai sur POCO ne peut être fait que par toi.
