# FUSION-02 U — CI corrigée, verrou v2 et contrats de preuve

La CI FUSION-01 échouait avant les tests sur une syntaxe YAML invalide. La
commande est protégée, et une CI indépendante Python3.12.12 publie les comptes
réels des147 tests initiaux plus les nouvelles régressions et journaux.

Le verrou v2 sépare primaire/alternatives/versions réellement consommées et
niveaux JVM/Android/E2E. Il actualise CORE/LLM/UI et NEXUS portablev4 : aucune
ancienne limite v3 n'est reportée à tort sur le nouveau SHA. Le pilote demeure
BLOCKED faute FTS5/SAF/fence/API24–25, et aucune lane LLM/VOICE n'est imposée.

CapabilityStatus et OperationReceipt sont des schémas de revue2-draft avec
validation sémantique hors runtime ; pas de conversion COMPLETED→COMMITTED, ni
nouvelle Guard ou fence active. Contrats/v1 et données restent intacts.

PR BROUILLON seulement. Ne pas fermer la mission globale ni fusionner/activer.
Consulter docs/fusion-02/REPORT.md, VALIDATION.json et CI_DIAGNOSIS.md.
