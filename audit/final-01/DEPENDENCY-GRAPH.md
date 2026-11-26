# F00 — Graphe de dépendances, chaînes de PR et architecture de fait

Sources : `PR-INVENTORY.csv`, `BRANCH-STATUS.csv` et `BASELINE-LOCK.json`, calculés le 21/11/2026 par `tools/` sur des clones contenant `refs/pull/*/head`.

« Contenue » signifie : la tête de la PR est un ancêtre Git de la tête d'une autre PR ouverte. Son code est donc présent plus loin dans la chaîne. Cela **ne veut pas dire** que la PR est inutile : sa revue, ses preuves rouges historiques ou sa base peuvent rester utiles. La fermeture d'une PR reste une décision du propriétaire.

## 1. Chaînes de PR ouvertes

113 PR sont ouvertes. 23 sont des PR terminales, et 90 sont des maillons contenus dans une PR terminale.

| Dépôt | PR terminale | CI au SHA | Base | PR ouvertes contenues (code préservé dans la terminale) |
|---|---|---|---|---|
| JARVIS-INTERFACE | [#23](https://github.com/bubth720/JARVIS-INTERFACE/pull/23) [M55-A P4] Unchanged R1 diagnostic on KVM, API 29/35, SAF wi | NO_CI | `codex/reuse-first-r1plus-20261108` | #16, #18, #20, #21 |
| JARVIS-INTERFACE | [#22](https://github.com/bubth720/JARVIS-INTERFACE/pull/22) [INTERFACE 008] Cockpit V2 natif expérimental, dashboard et  | PASS | `test/interface-device-006` | — |
| JARVIS-INTERFACE | [#19](https://github.com/bubth720/JARVIS-INTERFACE/pull/19) M54 — contrôleur AVATAR et inventaire privé isolés, runtime  | PASS | `feat/ui-01-native-cockpit` | #16 |
| JARVIS-INTERFACE | [#17](https://github.com/bubth720/JARVIS-INTERFACE/pull/17) [M51.05] Parseurs UI gfxinfo, comparaison et audit sans modi | PASS | `feat/ui-01-native-cockpit` | #16 |
| JARVIS-INTERFACE | [#15](https://github.com/bubth720/JARVIS-INTERFACE/pull/15) [M50-PERF-01] Réponse laboratoire accélérée et mesure p95 <  | PASS | `codex/m50-s1b-android-20261104` | #7, #8, #10, #11, #12, #13, #14 |
| JARVIS-INTERFACE | [#9](https://github.com/bubth720/JARVIS-INTERFACE/pull/9) UI-PF-01 Lot 2 — aperçu de citation inerte | PASS | `mission/prefusion-gates-20261026` | #7, #8 |
| JARVIS-LLM | [#18](https://github.com/bubth720/JARVIS-LLM/pull/18) [M55-A P1] F3B historical verifier on its frozen commit (unb | PASS | `mission/r02-watchers-isolation-202` | #5, #6, #7, #8, #9, #11, #12, #13, #14, #15, #16, #17 |
| JARVIS-NEXUS | [#16](https://github.com/bubth720/JARVIS-NEXUS/pull/16) N01-A3: route REUSE reviews with the approved one-file prese | PASS | `codex/m53-readonly-preparation` | #4, #5, #6, #7, #8, #9, #10, #11, #12, #13, #14 |
| JARVIS-NEXUS | [#15](https://github.com/bubth720/JARVIS-NEXUS/pull/15) [M55-A P3] NEX-07 historical guards in their own context + e | PASS | `codex/reuse-first-r1plus-20261108` | #4, #5, #6, #7, #8, #9, #10, #11, #12, #13, #14 |
| JARVIS-SERVICES | [#12](https://github.com/bubth720/JARVIS-SERVICES/pull/12) [CODEX][M50] SERV-M50-01 — outils locaux et contrat d'écritu | PASS | `feat/lot4-offline-recovery-2026102` | #4, #5, #6, #7, #8, #9, #10, #11 |
| JARVIS-UNIFIED | [#28](https://github.com/bubth720/JARVIS-UNIFIED/pull/28) N01-B0: laboratoire RESEARCH HTTPS synthétique, sécurité et  | PASS | `codex/nexus-n01-a3-evidence-202611` | #1, #6, #7, #8, #9, #10, #12, #13, #14, #15, #17, #19, #20, #21, #22, #25, #26 |
| JARVIS-UNIFIED | [#24](https://github.com/bubth720/JARVIS-UNIFIED/pull/24) LAB-02 — diagnostic priorisé en lecture seule des campagnes  | PASS | `codex/lab-01-complete-integration` | #1, #6, #7, #8, #9, #10, #12, #13, #14, #15, #17, #19, #20, #21, #23 |
| JARVIS-UNIFIED | [#18](https://github.com/bubth720/JARVIS-UNIFIED/pull/18) [CODEX][M50-S1] Corriger la chaîne CI et qualifier une coqui | PASS | `mission/m50-integrated-beta-202610` | #1, #6, #7, #8, #9, #10, #12, #13, #14, #15, #17 |
| JARVIS-UNIFIED | [#16](https://github.com/bubth720/JARVIS-UNIFIED/pull/16) PREFUSION lot3 : complément de vérification du 29 octobre (O | PASS | `mission/prefusion-lot3-20261027` | #1, #6, #7, #8, #9, #10, #12 |
| JARVIS-UNIFIED | [#11](https://github.com/bubth720/JARVIS-UNIFIED/pull/11) UNI-08/U03 — bilan vérifié du lot2, détection de conflits et | PASS | `codex/prefusion-20261026-lot1` | #1, #6, #7, #8, #9, #10 |
| JARVIS-VOICE | [#28](https://github.com/bubth720/JARVIS-VOICE/pull/28) [M55-A P2] Historical SDK/005J guards on their frozen commit | NO_CI | `feat/voice-expressive-v3-android` | #1, #3, #4, #5, #6, #7, #8, #9, #11, #13, #17, #20, #23, #24, #25, #26, #27 |
| JARVIS-VOICE | [#19](https://github.com/bubth720/JARVIS-VOICE/pull/19) VOICE-07: client public et passerelle de refus, activation C | FAIL | `feat/voice-06-voice-delivery` | #1, #3, #4, #5, #6, #7, #8, #9, #11, #13, #17, #18 |
| JARVIS-VOICE | [#2](https://github.com/bubth720/JARVIS-VOICE/pull/2) Mission 002 : Pocket TTS français CPU et serveur vocal privé | PASS | `feat/android-tts-foundation` | #1 |
| JARVIS-VOLUTION- | [#6](https://github.com/bubth720/JARVIS-VOLUTION-/pull/6) [CODEX][M50] EVOL-M50-01 — diagnostic local sans auto-répara | PASS | `codex/prefusion-lot2-20261027` | #3, #5 |
| JARVIS-VOLUTION- | [#4](https://github.com/bubth720/JARVIS-VOLUTION-/pull/4) EVOL-PF-01 Lot 2 — séparer approbation labo et exécution | PASS | `mission/prefusion-gates-20261026` | #3 |
| JAVIS-Local-v2 | [#27](https://github.com/bubth720/JAVIS-Local-v2/pull/27) [M50-S1 A3] CORE : regression du HEAD et gardes historiques | UNKNOWN | `UNKNOWN` | #4, #16, #18, #19, #21, #22, #23, #24, #25, #26 |
| JAVIS-Local-v2 | [#20](https://github.com/bubth720/JAVIS-Local-v2/pull/20) CORE-PF-01 Lot 2 — état des producteurs en lecture seule | UNKNOWN | `UNKNOWN` | #4, #16, #18, #19 |
| JAVIS-Local-v2 | [#9](https://github.com/bubth720/JAVIS-Local-v2/pull/9) Pilote CORE ↔ VOICE C1 : port désactivé, barrière native en  | UNKNOWN | `UNKNOWN` | — |

Constats :

- **Chaînes empilées.** Les missions successives (pré-fusion lot 1 → lot 3 → M50 → M55) ont été poussées chacune sur la branche de la précédente. Le code d'une chaîne n'est donc à jour que dans sa PR terminale.
- **CI rouge des maillons.** Les 31 PR ouvertes dont la CI est rouge au SHA de tête sont presque toutes des maillons intermédiaires : LLM 12, VOICE 12, NEXUS 4, SERVICES 2, INTERFACE 1. Seule VOICE #19 est une PR terminale rouge. Ces résultats rouges sont **conservés comme historique**, sans être corrigés.
- **Aucun conflit avec la base** (`mergeable_state`) : 66 PR `clean`, 34 `unstable` (checks rouges). CORE est `UNKNOWN`.

## 2. Travaux récents sans PR (front des branches)

21 branches ne sont contenues ni dans `main` ni dans une PR ouverte. Les plus importantes :

| Dépôt | Branche | Tête | Rôle |
|---|---|---|---|
| INTERFACE | `codex/global-01-s04-20261119` | `e6489bf011c8` | **Application V3 la plus avancée**. Contient V1, V3, captures, A-031 à A-040 et S04. Aucune PR. |
| UNIFIED | `codex/global-01-s04-20261119` | `0af322c1e353` | Rapports d'audit S04. Contient RESEARCH-B0, G03, N01-A2/A3 et l'audit global. |
| UNIFIED | `codex/m56-action-permission-core` | `323a79b26` | Politique d'actions M56 (F07). |
| LLM | `ccr-5cf17ed2-phgk00` | `9c3fc500ea74` | Successeur d'intégrité A02 (A-002). |
| VOICE | `ccr-5cf17ed2-phgk00` | `58907351` | Gardes VOICE A-003. |
| EVOLUTION | `feat/evolution-final-01` | `c4abfb035e3e` | EVOLUTION-FINAL-01 (51 tests). |
| SERVICES | `feat/services-final-01` | `d16dd84f2` | Livraison SERVICES finale. |
| NEXUS | `feat/nex-06a-android-api24` | `374ea2e2f` | Adaptateur SQLite API 24. |
| INTERFACE | `feature/avatar-png-001` | `3daffe7e5` | Importeur privé d'avatar PNG (36 poses). |

La liste complète figure dans `BRANCH-STATUS.csv` (statut `FRONTIER_NO_PR`).

**Généalogie vérifiée :**

- INTERFACE `ccr-e05fe51e-ycqubx` (`aa344f3`) ⊂ S04 `e6489bf` (6 commits plus loin).
- UNIFIED `00126b3` ⊂ S04 `0af322c`.
- Les deux lignées sont linéaires et sans divergence.

## 3. Architecture de fait (APK V3 au SHA `e6489bf`)

```text
INTERFACE V3 (labs/v3) ── compile et embarque, épinglés par SHA dans v3-cockpit.yml :
   CORE   5da98383ed12  (contient feat/mem-02-intensive 49ad428 : mémoire consentie)
   LLM    2e011776d9e0  A02 llama.cpp scellé, Qwen3-0.6B, 1 seul modèle chargé
   NEXUS  06ccf98a7709  copie compilée (FTS5 via SQLite AndroidX embarqué)
   VOICE  92d07453260   Pocket TTS ; STT whisper.cpp v1.8.4
   SERVICES, EVOLUTION : non embarqués (« à connecter » / désactivés)
```

| Règle cible | Constat | Statut |
|---|---|---|
| Un seul CORE | Un seul CORE (`5da9838`), compilé depuis les sources épinglées | Conforme |
| Un seul LLM actif | Un moteur A02 et un modèle ; l'étude 1.7B est limitée au laboratoire | Conforme |
| VOICE facultative | Le mode texte fonctionne sans voix (tests g1, d2) | Conforme |
| INTERFACE facultative | **Écart.** La couche de conversation `labs/v3/.../conv/` (ConvSession, KnowledgePlanner, DocumentaryAnswer, gardes) vit dans INTERFACE, pas dans CORE. INTERFACE est donc un **second orchestrateur de fait**. | À traiter (décision F01/F02) |
| NEXUS local | Oui, hors ligne. **Écart d'épinglage** : 27 commits de retard sur `5f10193` | À réconcilier (F06) |
| EVOLUTION isolé | Non embarqué ; `SANDBOX_NOT_QUALIFIED`, `mayExecute=false` | Conforme |
| SERVICES permissionnés | Non embarqué ; M56 (UNIFIED) et SERVICES M50 restent hors APK | Conforme (absent) |

Écarts d'épinglage à réconcilier :

- LLM : 10 commits de retard sur `9c3fc500`, dont le successeur CI A-002 (aucun changement de runtime prouvé).
- VOICE : 1 à 2 commits de retard (gardes A-003).
