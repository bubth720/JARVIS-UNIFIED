# Instructions JARVIS-UNIFIED

Lire README.md, docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md et le cahier des charges
applicable. UNIFIED coordonne registres, preuves, contrats et plans ; ce dépôt
n'est ni un troisième moteur ni un runtime Android. CORE orchestre, LLM infère,
VOICE fournit les capacités vocales démontrées ; les autres rôles restent cibles
jusqu'à preuve du code. Conserver les fonctions historiques et les inconnues.

Travailler dans le checkout existant sur une branche dédiée. Ne pas créer de
worktree sans demande. Aucun merge/main, auto-merge, déploiement, modification
source externe ou changement de signature/modèles sans autorisation explicite.
Une autorisation d'audit n'autorise pas l'implémentation de l'adaptateur CORE/LLM.
Préserver les missions précédentes et les snapshots ; ne pas réécrire leur preuve.

Hiérarchie : observation directe code/graph Git ; tests réellement exécutés avec
plateforme/SHA ; CI distante réellement observée ; rapports versionnés historiques ;
déclarations/conversations. Une CI est un type de preuve distinct, pas une preuve
matérielle. Distinguer merge Git, contrat, code de liaison, test d'intégration,
qualification physique. Ne pas déduire une absence d'un 403/404 réseau.

Aucun secret, prompt, audio, profil ou donnée personnelle dans Git/log/artefact.
Garder vérifications TLS/signatures/hashes ; ne pas contourner le proxy. GitHub
sert au développement, jamais au runtime hors ligne. Stop après refus d'écriture
403 : livrer branche/patch et diagnostic sans inventer de publication.

Avant livraison : python3 scripts/validate_unified.py ; tests tests/ et
registry/tests/ ; régression backup_prototype/tests/ si dépendance cryptography
existante disponible. Les nouveaux audit/contrats n'ont aucune dépendance externe.
Rapporter commandes, totaux, échecs/sauts/non-exécutés et plateforme. Rapport Codex
obligatoire : module, mission, dépôt, branche, SHA, PR réelle ou blocage, preuves
GitHub datées, intégrations confirmées, état de main et prochaine mission.
