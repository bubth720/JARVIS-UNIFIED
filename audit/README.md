# AUD-00 — Audit probant JARVIS V1 (11/11/2026)

Mission : `JARVIS_MISSION_GLOBALE_V1_AUDIT_ET_DEVELOPPEMENT_2026-11-11.pdf`, section 3. Lecture seule de 12 dépôts (236 branches JARVIS), des PR et des runs GitHub Actions. Aucun dépôt applicatif modifié par cet audit ; aucune fusion, installation ni téléchargement de modèle.

| Livrable | Contenu |
|---|---|
| [repository-inventory.json](repository-inventory.json) | dépôt, URL, branche de référence/candidate, SHA, date, PR, workflows observés |
| [module-capability-matrix.csv](module-capability-matrix.csv) | 36 capacités classées IMPLEMENTED_TESTED / COMPILED_ONLY / PROTOTYPE / ABSENT / NOT_VERIFIABLE |
| [integration-contracts.md](integration-contracts.md) | frontières réelles, incompatibilités, versions, risques |
| [critical-path.md](critical-path.md) | P0/P1/P2, parallélisation, actions humaines |
| [evidence-index.json](evidence-index.json) | liens exacts de preuve, horodatage, SHA-256 des livrables |

## Constats qui corrigent le dossier PDF

1. **CORE existe** : `bubth720/JAVIS-Local-v2` (orthographe JAVIS), `SessionCoordinator.kt` sur ses branches CORE. **EVOLUTION** : `bubth720/JARVIS-VOLUTION-`.
2. **Deux moteurs LLM** : CORE utilise `llama-android:0.1.1` (minSdk 24), JARVIS-LLM son llama.cpp/JNI épinglé (minSdk 29). A02 ne s'applique qu'au second : décision P0.2 requise.
3. **CI rouges = gardes historiques mal portées**, pas des défauts produit : LLM F3B (corrigé `59ce4d4`, run 43073699901 SUCCESS), VOICE SDK/Studio (base `99d4073` sur toutes les PR), NEXUS « quota preflight » (`nex-07.yml` sur toutes les PR, 39 fichiers successeurs non déclarés). Le workflow propre à chaque branche est vert.
4. L'ancrage LLM `59ce4d4` **descend** de R02 `0ef3635` (+1 commit CI) : pas de divergence fonctionnelle.

## Limites (NOT_RUN)

Point 06 du protocole : seules les gardes de préservation LLM ont été rejouées localement ; aucune suite Gradle/Android relancée ici. Point 08 (coûts RAM/CPU/batterie Android) : aucune mesure appareil n'existe dans les dépôts — NOT_VERIFIABLE. Runs marqués `source: mission PDF` non re-consultés.

## Décision AUD-00

**Accepté sous réserve** : chaque module a un statut sourcé, les noms de dépôts sont résolus, aucune fonction n'est déclarée opérationnelle sans test. Prochaine action atomique : décision P0.2, puis LLM-02.
