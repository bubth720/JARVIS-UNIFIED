# UNI-02 — Registre exécutable de capacités et ordonnanceur de missions

## 1. Identifiant et responsabilité
**ID :** UNI-02 ; **module :** UNIFIED ; **dépôt :** `bubth720/JARVIS-UNIFIED` ; **priorité :** P1 ; **dépendances :** UNI-01.
**Base réellement vérifiée :** `decision/d4-02d-v1-v5-approved-2026-10-17` au commit `8ddac8fe8a1861a27d3abeca81eb4ab8f110c3a9`.
**Branche de dossier :** `plan/intensive-2026-10-22` ; **branche d'implémentation proposée :** `feat/uni-02-tooling`.
**Statut :** dossier préparé, exécution interdite sans attribution de l'utilisateur.

## 2. Code déjà livré et limites
UNIFIED héberge contrats v1, registre des modules/missions et ADR-001. La validation D4-02D V1–V5 ne s'applique qu'aux fixtures expérimentales. Il n'y a ni moteur Android ni runtime LLM dans UNIFIED ; aucune fonction ne doit y être ajoutée pour orchestrer l'utilisateur.

## 3. Objectif métier
Coder un planificateur local de dépendances et de conflits d'ownership qui empêche les collisions entre agents et suit les preuves, sans déclencher lui-même Codex.

## 4. Fonctionnalités substantielles à programmer
1. Créer MissionNode, RepoReference, CapabilityManifest, EvidenceGate et OwnershipPolicy à partir du registre UNIFIED.
2. Coder validation de 31 IDs, dépendances existantes, absence de cycles et accès explicite aux modules de chaque mission.
3. Construire un ordonnancement topologique par vagues et une matrice des fichiers partagés (CORE, LLM native, dashboard).
4. Suivre PREPARED/ASSIGNED/IN_PROGRESS/DELIVERED/BLOCKED uniquement sur preuves commit/rapport vérifiées, pas sur commentaires libres.
5. Produire sortie CLI JSON/Markdown: missions prêtes, bloquées et action manuelle nécessaire.
6. Créer tests sur ce manifeste réel, cycles fictifs, références absentes, conflits de branche et autorisations sensibles.

## 5. Architecture, classes et interfaces
1. CampaignManifestReader, MissionDAGResolver
2. OwnershipConflictDetector + RepoReferenceCatalog
3. EvidenceGateEvaluator et MissionStatusMachine
4. AssignmentPlanRenderer et CLI report
Architecture claire : parsing du registre → domaine typé → outils CLI. Aucun appel automatique à des services extérieurs.

## 6. Fichiers réellement présents et fichiers projetés
1. Existants : registry/{repositories,modules,missions,integrations}.json, scripts/audit_repos.py
2. À créer : tooling/campaign/{manifest.py,dag.py,ownership.py,status.py,cli.py}
3. À créer : tooling/campaign/tests/ et docs/intensive-2026-10-22/REPORT-UNI-02.md une fois le code créé
Vérifier arborescence actuelle ; les chemins de tooling nouveaux sont des propositions.

## 7. Étapes d'implémentation
1. Charger index MISSIONS.json et valider toutes ses 31 entrées.
2. Implémenter le DAG/tri et détection de cycles, sans supprimer les références inconnues.
3. Codifier ownership/risques et politiques de refus d'écriture concurrente.
4. Ajouter commandes list-ready, list-blocked, explain-mission et export-wave.
5. Tester états sans preuve, commit de base dérivé et dépendance bloquante.

## 8. Technologies et dépendances
Python standard library, JSON, argparse, unittest ; pas de serveur/automate.. Garder possibilité d'un usage intégralement hors ligne. Ne pas remplacer silencieusement des dépendances ou schémas existants.

## 9. Connexions et ownership
UNIFIED ne modifie pas les dépôts enfants et ne déclenche ni sessions Codex ni merges.
Les modules restent propriétaires de leurs objets techniques et données ; les contrats sont distribués de manière volontaire, pas activés par modification de ce dépôt.

## 10. Sécurité et compatibilité
Pas de modification de `main`, `contracts/v1` figé, clés ou archives personnelles. Les outils ne peuvent lancer Codex, exécuter des patches ou déclencher une PR/merge. Codes de retour non nuls sur ambiguïté, compatibilité inconnue ou incohérence.

## 11. Livrables obligatoires
Code CLI effectif, schemas/types/manifests exploitables, tests minimaux passés, démonstration réelle sur registre de la campagne et rapport bref des écarts. Pas une mission de documentation uniquement.

## 12. Critères d'achèvement
1. La CLI génère un ordonnancement vérifiable de ces 31 missions.
2. Un cycle et une collision d'ownership sont refusés avec trace lisible.
3. Une mission préparée n'est jamais comptée comme exécutée ou qualifiée.
Rejeter toute réussite inventée à partir d'une fixture insuffisante.

## 13. Dépendances et parallélisme
UNI-01. UNI-01 peut être développé en parallèle de tous les P0 dans les autres dépôts ; UNI-02 suit UNI-01. Aucun autre agent ne doit changer simultanément les contrats figés.

## 14. Sécurité Git et approbations
Aucune mission lancée par dépôt de ce fichier. Attribution séparée, branche de code distincte, aucune fusion principale, aucun changement sensible transversal avant validation explicite.

## 15. Retour au coordinateur CENTRAL
Indiquer module, ID, branche, commit exact, fichiers codés, commandes et tests réellement exécutés, limites, blocages, risques de régression et prochaine action.
