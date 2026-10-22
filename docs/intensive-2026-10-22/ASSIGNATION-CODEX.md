# Distribution des missions à Codex — instructions concrètes
Les documents ont été déposés dans une branche **`plan/intensive-2026-10-22`** de chaque dépôt cible, et dans l'index central UNIFIED. Il n'y a **aucune preuve ici que chaque environnement Codex a effectivement chargé cette branche** : l'accès final doit être vérifié quand l'agent prend une mission.
## Pour attribuer une mission
1. Ouvrir l'environnement Codex connecté au dépôt figurant dans INDEX.md.
2. Sélectionner la branche de lecture `plan/intensive-2026-10-22`, ou ouvrir le lien GitHub immuable du dossier si l'environnement ne synchronise pas automatiquement les nouvelles branches.
3. Envoyer : « Je t'autorise à exécuter **uniquement** la mission `[ID]` déposée dans `docs/intensive-2026-10-22/[ID].md` du dépôt courant. Vérifie le commit de référence, crée une branche code distincte, livre les fonctions réelles, exécute les tests minimaux puis donne branche, commit, fichiers, résultats et blocages. Pas de fusion main, ni d'action sensible non autorisée. »
4. Réserver deux missions qui touchent les mêmes classes, même si les dépôts sont identiques, à des sessions séquencées. Les missions indépendantes de vague 0 peuvent être confiées simultanément à différents agents.
5. L'agent doit relire et valider les signatures des contrats amont avant d'intégrer quoi que ce soit ; si absent, arrêter sans fabriquer un stub opérationnel.
## Limites
Les branches publiées sont un **espace GitHub de préparation**, pas un démarrage du travail agent ni une modification du runtime. Les outils Codex Cloud peuvent être liés à un seul dépôt ; utiliser l'index central en lecture et le document de mission du dépôt concerné. Pas de fusion ni d'accès à appareils personnels sans nouvel ordre.
