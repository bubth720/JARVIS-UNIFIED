# Correction du workflow de coordination — pas de modification métier

Premier commit49f33737473550509512f2087c15eab18b7e1e74 : run42388516326 en échec avant tout job (liste jobs vide). Le parser YAML rejetait la commande pip non quotée contenant `--only-binary=:all:` (ligne20, colonne54 : mapping values are not allowed here). Aucun test de ce nouveau workflow ne s'était exécuté ; son échec n'est pas reclassé PASS.

Correction limitée au **quotage du scalaire run** dans le nouveau workflow M51. La même dépendance historique cryptography demeure demandée ; aucun garde, contrat, validation de source, statut de module ou test métier n'est changé. Analyse syntaxique YAML exécutée avant publication corrigée ; une nouvelle campagne du nouveau commit doit fournir les preuves. Il ne s'agit pas d'un retry automatique masquant un échec de test ou d'inférence.

Les workflows historiques de PR au premier commit peuvent réussir indépendamment : ils ne réparent pas le workflow nouveau invalide. Leurs identités et le premier échec restent dans le bilan final. Aucun poids, modèle, clé ou installation n'est concerné.
