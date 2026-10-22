# JARVIS — Index général de la campagne de développement intensif

**Date :** 22 octobre 2026 · **Statut :** PRÉPARÉ / AUCUN AGENT DÉMARRÉ
**Dépôt :** `bubth720/JARVIS-UNIFIED`, branche `plan/intensive-2026-10-22`, commit de base `8ddac8fe8a1861a27d3abeca81eb4ab8f110c3a9`.
La liste est exhaustive **pour les développements actuellement identifiables** ; de nouveaux besoins pourront émerger pendant l'implémentation. **31 missions substantielles**, aucune fusion.

## État initial vérifié
- CORE : Qwen3-0.6B-Q4_K_M GGUF vérifié intégralement par MVP004C, commit `a6f13dd` ; génération JNI Android encore NON QUALIFIÉE. MVP005-007 restent des gates distincts.
- LLM : Kotlin/C++ llama.cpp, profil Android, catalogue, fixtures P2, patch F3B non appliqué ; pas de connexion native CORE de production.
- VOICE : Studio005J, expression, identités et Binder pilote V1 opt-in ; génération par Binder non autorisée.
- INTERFACE : Dashboard Compose/DataStore et avatar 2.5D vectoriel avec IDLE/BLINK/HEAD_TILT, pas de lip-sync.
- SERVICES : huit bibliothèques développées, BRIDGE transport réel absent.
- NEXUS et EVOLUTION : README initial uniquement, leurs fondations sont à créer.
- IDENTITY et MEMORY : composants existants partiellement dans CORE, **aucun dépôt distinct**.
- UNIFIED : outils/registre et contrats, pas de runtime.

## Dossiers réellement déposés dans les dépôts propriétaires
| Dépôt | Missions | Commit de planification | Index du dépôt |
|---|---:|---|---|
| JAVIS-Local-v2 | 7 | `1b7ac9b35b` | [INDEX](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/INDEX.md) |
| JARVIS-LLM | 3 | `fdb71605d9` | [INDEX](https://github.com/bubth720/JARVIS-LLM/blob/fdb71605d91b69484a38fcf0df283365a2493f38/docs/intensive-2026-10-22/INDEX.md) |
| JARVIS-VOICE | 3 | `31a0087381` | [INDEX](https://github.com/bubth720/JARVIS-VOICE/blob/31a0087381db14a9d2256e6e64373ef45b38b616/docs/intensive-2026-10-22/INDEX.md) |
| JARVIS-INTERFACE | 4 | `50f5f61708` | [INDEX](https://github.com/bubth720/JARVIS-INTERFACE/blob/50f5f61708d5ce6b141dec98fe0c73d89eaf00e3/docs/intensive-2026-10-22/INDEX.md) |
| JARVIS-SERVICES | 3 | `67e7f798b8` | [INDEX](https://github.com/bubth720/JARVIS-SERVICES/blob/67e7f798b8bbcb8391e0d57ea5b886a2a9edf4db/docs/intensive-2026-10-22/INDEX.md) |
| JARVIS-NEXUS | 5 | `e4b2018383` | [INDEX](https://github.com/bubth720/JARVIS-NEXUS/blob/e4b2018383a35106cd326848fab597ef07a50157/docs/intensive-2026-10-22/INDEX.md) |
| JARVIS-VOLUTION- | 4 | `36d09339aa` | [INDEX](https://github.com/bubth720/JARVIS-VOLUTION-/blob/36d09339aa93869c36c0981800918cde818637ac/docs/intensive-2026-10-22/INDEX.md) |
| JARVIS-UNIFIED | 2 | Présente branche | [Fiches UNI](./UNI-01.md) |

## Inventaire des 31 missions
| Mission | Priorité | Vague indicative | Dépendances | Document immuable |
|---|---|---:|---|---|
| CORE-01 | P0 | 0 | Aucune | [CORE-01](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/CORE-01.md) |
| CORE-02 | P1 | 2 | CORE-01,UNI-01 | [CORE-02](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/CORE-02.md) |
| CORE-03 | P2 | 4 | CORE-01,CORE-02,NEX-03,SERV-01,UNI-01 | [CORE-03](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/CORE-03.md) |
| ID-01 | P1 | 2 | CORE-01 | [ID-01](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/ID-01.md) |
| ID-02 | P2 | 3 | ID-01,MEM-01 | [ID-02](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/ID-02.md) |
| MEM-01 | P1 | 2 | CORE-01 | [MEM-01](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/MEM-01.md) |
| MEM-02 | P2 | 4 | MEM-01,NEX-03 | [MEM-02](https://github.com/bubth720/JAVIS-Local-v2/blob/1b7ac9b35b5e6e133167fcaf1873e58b9db7288e/docs/intensive-2026-10-22/MEM-02.md) |
| LLM-01 | P0 | 0 | Aucune | [LLM-01](https://github.com/bubth720/JARVIS-LLM/blob/fdb71605d91b69484a38fcf0df283365a2493f38/docs/intensive-2026-10-22/LLM-01.md) |
| LLM-02 | P1 | 1 | LLM-01 | [LLM-02](https://github.com/bubth720/JARVIS-LLM/blob/fdb71605d91b69484a38fcf0df283365a2493f38/docs/intensive-2026-10-22/LLM-02.md) |
| LLM-03 | P2 | 3 | LLM-01,LLM-02,UNI-01 | [LLM-03](https://github.com/bubth720/JARVIS-LLM/blob/fdb71605d91b69484a38fcf0df283365a2493f38/docs/intensive-2026-10-22/LLM-03.md) |
| VOICE-01 | P0 | 0 | Aucune | [VOICE-01](https://github.com/bubth720/JARVIS-VOICE/blob/31a0087381db14a9d2256e6e64373ef45b38b616/docs/intensive-2026-10-22/VOICE-01.md) |
| VOICE-02 | P1 | 3 | VOICE-01,ID-01 | [VOICE-02](https://github.com/bubth720/JARVIS-VOICE/blob/31a0087381db14a9d2256e6e64373ef45b38b616/docs/intensive-2026-10-22/VOICE-02.md) |
| VOICE-03 | P2 | 4 | VOICE-01,VOICE-02,CORE-02,UNI-01 | [VOICE-03](https://github.com/bubth720/JARVIS-VOICE/blob/31a0087381db14a9d2256e6e64373ef45b38b616/docs/intensive-2026-10-22/VOICE-03.md) |
| UI-01 | P1 | 3 | CORE-02 | [UI-01](https://github.com/bubth720/JARVIS-INTERFACE/blob/50f5f61708d5ce6b141dec98fe0c73d89eaf00e3/docs/intensive-2026-10-22/UI-01.md) |
| UI-02 | P1 | 3 | ID-01,MEM-01 | [UI-02](https://github.com/bubth720/JARVIS-INTERFACE/blob/50f5f61708d5ce6b141dec98fe0c73d89eaf00e3/docs/intensive-2026-10-22/UI-02.md) |
| AVA-01 | P0 | 0 | Aucune | [AVA-01](https://github.com/bubth720/JARVIS-INTERFACE/blob/50f5f61708d5ce6b141dec98fe0c73d89eaf00e3/docs/intensive-2026-10-22/AVA-01.md) |
| AVA-02 | P1 | 4 | AVA-01,VOICE-02,CORE-02 | [AVA-02](https://github.com/bubth720/JARVIS-INTERFACE/blob/50f5f61708d5ce6b141dec98fe0c73d89eaf00e3/docs/intensive-2026-10-22/AVA-02.md) |
| SERV-01 | P0 | 0 | Aucune | [SERV-01](https://github.com/bubth720/JARVIS-SERVICES/blob/67e7f798b8bbcb8391e0d57ea5b886a2a9edf4db/docs/intensive-2026-10-22/SERV-01.md) |
| SERV-02 | P1 | 1 | SERV-01 | [SERV-02](https://github.com/bubth720/JARVIS-SERVICES/blob/67e7f798b8bbcb8391e0d57ea5b886a2a9edf4db/docs/intensive-2026-10-22/SERV-02.md) |
| SERV-03 | P2 | 3 | SERV-01,SERV-02,UNI-01 | [SERV-03](https://github.com/bubth720/JARVIS-SERVICES/blob/67e7f798b8bbcb8391e0d57ea5b886a2a9edf4db/docs/intensive-2026-10-22/SERV-03.md) |
| NEX-01 | P0 | 0 | Aucune | [NEX-01](https://github.com/bubth720/JARVIS-NEXUS/blob/e4b2018383a35106cd326848fab597ef07a50157/docs/intensive-2026-10-22/NEX-01.md) |
| NEX-02 | P0 | 1 | NEX-01 | [NEX-02](https://github.com/bubth720/JARVIS-NEXUS/blob/e4b2018383a35106cd326848fab597ef07a50157/docs/intensive-2026-10-22/NEX-02.md) |
| NEX-03 | P1 | 2 | NEX-02 | [NEX-03](https://github.com/bubth720/JARVIS-NEXUS/blob/e4b2018383a35106cd326848fab597ef07a50157/docs/intensive-2026-10-22/NEX-03.md) |
| NEX-04 | P2 | 3 | NEX-01,NEX-03 | [NEX-04](https://github.com/bubth720/JARVIS-NEXUS/blob/e4b2018383a35106cd326848fab597ef07a50157/docs/intensive-2026-10-22/NEX-04.md) |
| NEX-05 | P2 | 2 | NEX-01,NEX-02 | [NEX-05](https://github.com/bubth720/JARVIS-NEXUS/blob/e4b2018383a35106cd326848fab597ef07a50157/docs/intensive-2026-10-22/NEX-05.md) |
| EVOL-01 | P0 | 0 | Aucune | [EVOL-01](https://github.com/bubth720/JARVIS-VOLUTION-/blob/36d09339aa93869c36c0981800918cde818637ac/docs/intensive-2026-10-22/EVOL-01.md) |
| EVOL-02 | P1 | 1 | EVOL-01 | [EVOL-02](https://github.com/bubth720/JARVIS-VOLUTION-/blob/36d09339aa93869c36c0981800918cde818637ac/docs/intensive-2026-10-22/EVOL-02.md) |
| EVOL-03 | P2 | 3 | EVOL-02,UNI-01 | [EVOL-03](https://github.com/bubth720/JARVIS-VOLUTION-/blob/36d09339aa93869c36c0981800918cde818637ac/docs/intensive-2026-10-22/EVOL-03.md) |
| EVOL-04 | P2 | 4 | EVOL-03 | [EVOL-04](https://github.com/bubth720/JARVIS-VOLUTION-/blob/36d09339aa93869c36c0981800918cde818637ac/docs/intensive-2026-10-22/EVOL-04.md) |
| UNI-01 | P0 | 0 | Aucune | [UNI-01](./UNI-01.md) |
| UNI-02 | P1 | 1 | UNI-01 | [UNI-02](./UNI-02.md) |

## Ordre et parallélisme contrôlé
**Vague 0 :** CORE-01, LLM-01, VOICE-01, AVA-01, SERV-01, NEX-01, EVOL-01, UNI-01. Huit dépôts indépendants ; leur attribution exige une commande individuelle.
**Vague 1 :** LLM-02, SERV-02, NEX-02, EVOL-02, UNI-02 après chaque prérequis.
**Vagues 2 à 4 :** uniquement après livraison des interfaces requises, jamais simultanément si fichiers communs CORE `JarvisCore.kt`, LLM `LlamaBackend.kt`, INTERFACE `DashboardGrid.kt`.
Le numéro de vague est une proposition d'ordre, **pas une preuve que les dépendances ont été réalisées**.

## Accès aux agents
[Guide d'attribution Codex](./ASSIGNATION-CODEX.md) · [Dépendances et propriétaires](./DEPENDANCES.md) · [Manifeste machine](./MISSIONS.json).

## Interdictions permanentes
La présence d'un dossier ne lance jamais Codex. Aucun merge `main`, installation sur POCO/Redmi, migration/effacement, contournement de sécurité, nouveau poids non approuvé, activation Binder/native ou exécution de patch hors sandbox approuvé. Toute intervention sensible fera l'objet d'une décision explicite.
