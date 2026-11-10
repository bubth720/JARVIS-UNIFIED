# JARVIS FIRST-RUN — priorité V1 Android (10 novembre 2026)

## Décision
Livrer un APK Android de conversation avec un **vrai LLM local hors ligne**, avant d'étendre les fonctions avancées. Cette branche est un espace de coordination indépendant. Aucun merge, aucune migration, aucune installation personnelle et aucune modification des modules producteurs n'est autorisé par ce document.

## Point de départ vérifié
- M50-S1B : CORE SessionCoordinator + client INTERFACE réels, mais réponses LAB/SYNTHETIC seulement ; tests émulateurs API29/API35.
- G3 vrai LLM : BLOCKED ; G4 documents : BLOCKED ; G8 appareil physique : NOT_RUN.
- Le dépôt UNIFIED coordonne des contrats/preuves ; l'application Android est dans le dépôt INTERFACE. Ne pas fabriquer une fausse application dans UNIFIED.

## Définition stricte de V1
1. APK Android installable, distinct du laboratoire testOnly.
2. Saisie de texte et réponses réellement générées par un modèle local autorisé, en mode avion.
3. Historique local de session, erreurs visibles, arrêt/relance contrôlés.
4. Démarrage, première réponse, tokens/s, RAM et température mesurés, sans inventer les chiffres.
5. Tests Android émulateur + vérification sur téléphone seulement après autorisation explicite.
6. Reproductibilité : commits sources, APK, SHA256, instructions Android simples et rapports.
7. Si le modèle autorisé ne convient pas, produire un verdict de blocage documenté, pas une réponse synthétique annoncée comme V1.

## Règles de préservation
- Ne jamais fusionner vers main.
- CORE, LLM, VOICE, INTERFACE, SERVICES, NEXUS restent indépendants et évolutifs.
- Toute adaptation passe par des interfaces/contrats versionnés et des branches isolées.
- Aucun nouveau poids, licence, téléchargement de modèle ou déploiement payant sans validation spécifique.
- L'autorisation antérieure Qwen3-0.6B était limitée au cloud-lab et à une révision définie : ne pas l'étendre implicitement à Android.
- La voix reste un chantier indépendant prioritaire après la V1, sans blocage de la livraison texte.

## Ordre d'exécution à proposer
A. Auditer les dépôts CORE, LLM et INTERFACE, branches et workflows les plus récents ; vérifier les vrais APK/artefacts.
B. Identifier le chemin le plus court pour remplacer les réponses synthétiques M50 par le vrai moteur local existant.
C. Définir le modèle exact et les droits nécessaires ; demander uniquement les autorisations manquantes.
D. Construire sur une branche d'intégration dédiée dans INTERFACE, avec retour arrière et tests.
E. Livrer l'APK et les mesures ; ne pas déclarer V1 prête avant génération réelle hors ligne.

## Politique de coût
Budget cloud additionnel <= 10 EUR/mois hors ChatGPT. Priorité aux builds et tests GitHub gratuits selon quotas disponibles ; aucun GPU loué sans preuve de gain et autorisation de dépense.

## Prochaine vérification
Identifier la branche la plus récente de chaque module et les dépendances de compilation ; le présent document n'atteste pas que l'APK V1 existe.
