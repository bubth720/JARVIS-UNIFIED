# JARVIS-FINAL-01 — Index des missions

**Coordination** :

- Dépôt et branche : UNIFIED `ccr-e05fe51e-ycqubx`.
- Base : `0af322c1e3531a5ebfb13c6f0a608900da6c7aee`, avancée en fast-forward sur `codex/global-01-s04-20261119`.
- Ajouts : seulement `audit/final-01/`.
- Aucune fusion vers `main`, aucune PR fermée, aucun runtime modifié.

| Lot | Objectif | Dépôt(s) | Base de travail (`BASELINE-LOCK.json`) | Statut |
|---|---|---|---|---|
| F00 | Inventaire vérifiable | UNIFIED | `0af322c` | **DONE_EVIDENCED** (voir les limites CORE R-05) |
| F01 | Contrats et CI de reprise | UNIFIED + adaptateurs | Épinglages de l'APK et têtes du front | **DONE_EVIDENCED** (porte GO ; mises à niveau d'épinglage NO-GO : voir `f01/F01-REPORT.md`) |
| F02 | Android de bout en bout hors ligne | CORE, INTERFACE, LLM, VOICE | INTERFACE `e6489bf` | PARTIAL (émulateur vert) / BLOCKED_DEVICE |
| F03 | LLM mesuré | LLM | `9c3fc500` / pin `2e01177` | À démarrer (CPU et CI) |
| F04 | VOICE sûre | VOICE | `58907351` / pin `92d0745` | À démarrer |
| F05 | INTERFACE et avatar | INTERFACE | `e6489bf` | À démarrer |
| F06 | NEXUS local | NEXUS + UNIFIED B0 | `5f101934` / pin `06ccf98` | À démarrer |
| F07 | SERVICES permissionnés | SERVICES, CORE, UNIFIED M56 | `8d80d09d` + M56 `323a79b` | À démarrer |
| F08 | EVOLUTION supervisée | JARVIS-VOLUTION- | `c4abfb03` → `ccr-e05fe51e-ycqubx` @ `009961a` | **PARTIAL** : adaptateur de campagne en lecture seule, comparaison avant/après et propositions (61/61 tests, essai sur données réelles) ; essai de correctif BLOCKED (`SANDBOX_NOT_QUALIFIED`) |
| F09 | Mémoire et apprentissage avec accord | CORE, NEXUS, UNIFIED | CORE `5da9838` | Après F06/F07 |
| F10 | PC + Android | UNIFIED ARCH-01 | — | Simulation seulement |
| F11 | Réception | Tous | — | NO-GO tant que F02 n'est pas validé sur appareil |

## Ordre proposé pour F01–F11

1. **F01 (en premier, CPU et CI, sans risque)**
   - Tests de contrat entre chaque épinglage de l'APK et la tête du module (R-04).
   - Matrice GO/NO-GO automatisée qui refuse GO si un test requis est absent ou `NOT_RUN`.
   - ADR sur l'orchestrateur (R-03), soumise à décision.
2. **En parallèle, après F01**
   - F05 : release non débogable déjà audité ; procédure de signature documentée.
   - F06 : mise à niveau de l'épinglage NEXUS par test de contrat.
   - F07 : M56 + SERVICES, en laboratoire OFF.
   - F08 : adaptateur de lecture seule.
3. **F03 / F04** : CPU et CI ; les mesures sur appareil restent BLOCKED_DEVICE.
4. **F09** : après F06 et F07.
5. **F10** : PC simulé.
6. **F02 sur appareil, puis F11** : dès accord d'installation et de signature.

## Fichiers F00

| Fichier | Contenu |
|---|---|
| `PR-INVENTORY.csv` | 119 PR : SHA de tête et de base, labels, CI au SHA, `mergeable_state`, présence dans `main`, contenance, empilement, niveau de preuve, décision proposée |
| `BRANCH-STATUS.csv` | 255 branches avec leur statut |
| `DEPENDENCY-GRAPH.md` | Chaînes de PR, front sans PR, architecture de fait |
| `CAPABILITY-MATRIX.md` | Capacités et niveaux de preuve |
| `BASELINE-LOCK.json` | SHA complets : références, épinglages, front |
| `TEST-EVIDENCE.md`, `local-replay-results.txt` | Tests rejoués et preuves CI |
| `RISKS-AND-DECISIONS.md`, `USER-ACCEPTANCE.md`, `GO-NOGO.md`, `EVOLUTION-LEARNING-PLAN.md` | Risques, décisions, verdicts et frontières |
| `tools/collect.sh`, `tools/analyse_prs.py` | Régénération de l'inventaire |
