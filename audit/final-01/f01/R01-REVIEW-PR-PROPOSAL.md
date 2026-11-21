# R-01 — PR de revue proposées (aucune n'est créée)

Toutes seraient des PR **brouillons**, sans fusion, sans fermeture d'une autre PR et sans modification de branche.
- La **tête** est le SHA exact qualifié.
- La **base** est l'ancêtre le plus proche qui a un sens pour la revue. Elle est calculée par généalogie Git le 21/11/2026.

| # | Dépôt | Tête (branche @ SHA) | Base proposée @ SHA | Delta | Dépendances / remarques | Preuve au SHA de tête |
|---|---|---|---|---|---|---|
| P1 | INTERFACE | `codex/global-01-s04-20261119` @ `e6489bf011c804fcbb699f41416e4b389e50d66a` | `codex/jarvis-v1-delivery` @ `de59e2b0c7b79fc604fb94f057809175e44219e4` (V1 livrée) | +67 commits, 940 fichiers (en majorité `labs/v3/` et captures) | V3 entier : A-031 à A-040 et S04. Garde V1 : 430 fichiers figés intacts. Alternative : base `development/mission-002` (branche par défaut, +127 commits). | Run 44638538519 : 11/11 et 30/30 sur API 29 et 35 |
| P2 | UNIFIED | `ccr-e05fe51e-ycqubx` @ `a9098df22148f96d8f22dd80f6d28b46697c73ba` (+ F01) | `codex/research-n01-b0-lab-20261118` @ `f1f30dc3cef2043ccfc68347c2cdc9b4e732de88` (tête de la PR #28) | +7 commits avant F01 | **Empilée sur #28.** Contient S04 UNIFIED `0af322c`, A-037 et F00 ; F01 s'ajoutera. | Tests locaux UNIFIED 222 PASS ; B0 63/63 sous 3.12 à `f1f30dc` |
| P3 | UNIFIED | `codex/m56-action-permission-core` @ `323a79b26b96486055ea9a9d2ed2fc273981dfe8` | `main` @ `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b` | +2 commits, 2 fichiers (`m56/action-permissions`) | Indépendante, aucun fichier commun avec P2. Entrée de F07. | CI à vérifier au SHA (`UNKNOWN`) |
| P4 | LLM | `ccr-5cf17ed2-phgk00` @ `9c3fc500ea74a40c4bfe9d3c3ffd66d09848fc71` | `codex/m55-b-local-intelligence` @ `ec9cbc2275d1eba202a0c829ebf7a9f5ed8c67d6` | +6 commits, 9 fichiers (workflows, `a02/tests`, `tools`) | A-002 successeur d'intégrité. **DROP_IN** pour l'APK (8 fichiers natifs identiques, API 302/302). Recoupe la PR #18 (2 fichiers communs, lignes divergentes). | Run 43625706542 PASS |
| P5 | VOICE | `ccr-5cf17ed2-phgk00` @ `58907351324b5a86385b08a2b61595efedb28357` | `feat/voice-expressive-v3-android` @ `92d07453260553466c92196454b56929b7494b2f` (= tête de la PR #27, épinglage APK) | +1 commit, 4 fichiers (gardes) | A-003. **DROP_IN** (`pocketRuntime` identique, API 445/445). Recoupe la PR #28 (1 fichier commun) : garder une seule des deux lignes. | Run 43625576432 PASS |
| P6 | EVOLUTION | `feat/evolution-final-01` @ `c4abfb035e3e99cc52840b04af06e3cea818c7a0` | `feat/evol-03-atelier-de-correctifs-isoles-e` @ `c0180181804338d21f3bf9d4b537b709595902f7` | +5 commits, 20 fichiers | EVOLUTION-FINAL-01. Diverge de la PR #6 (M50) sans fichier commun. | 51/51 en local à `c4abfb0` ; CI 40415562523 à `68e0956` (même code) |
| P7 | SERVICES | `feat/services-final-01` @ `d16dd84f27881460ec9f02d2a54d9ddff23187dc` | `feat/serv-03-services` @ `3decdc47d82f9b43713c48cab244762941770a81` | +4 commits, 107 fichiers | Diverge de la PR #12 (M50 : 28 commits, 2 fichiers communs). Réconciliation requise en F07. | `UNKNOWN` au SHA (à relever) |
| — | NEXUS | `feat/nex-06a-android-api24` @ `374ea2e2fd640e78f2f5e12e60e75b493420e504` | — | +1 commit, 44 fichiers | **Pas de PR proposée.** Retravaillée dans FUSION-01/02 (`9d6928c`, `06ccf98`) : 23 fichiers sur 44 identiques dans N01-A3, les autres ont évolué. Revue de confirmation seulement. | — |
| — | INTERFACE | `feature/avatar-png-001` @ `3daffe7e5c0d9d76c53b10e1029782f4f3e25030` | `feat/interface-final-01` @ `db459ba388a3fea992d80320c3989be0edda8500` | +1 commit, 5 fichiers | Importeur privé d'avatar PNG (36 poses), application historique. **À décider en F05** : porter dans V3 ou archiver. | — |

**Ordre recommandé si tu acceptes :**
1. P1 et P2, qui forment la base de travail commune.
2. P4 et P5, en remplaçants exacts.
3. P6, puis P3 et P7 (F07, F08).

**Pour chaque PR, il me faut ton accord explicite :** dépôt, tête et base.
