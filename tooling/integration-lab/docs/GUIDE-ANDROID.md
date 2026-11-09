# Lancer le laboratoire depuis son Android

1. Ouvrir https://github.com/bubth720/JARVIS-UNIFIED/actions dans le navigateur, connecté à son compte GitHub autorisé.
2. Choisir **JARVIS INTEGRATION LAB**, puis la campagne de la branche **codex/lab-01-complete-integration** indiquée dans la PR de livraison.
3. Dans le menu de cette campagne, choisir **Re-run all jobs**. Si nécessaire, activer la version « site pour ordinateur » de GitHub pour afficher ce menu. Cela nécessite les droits Actions du dépôt ; aucune clé n'est saisie dans le rapport.
4. Attendre les jobs **lab-tests** et **campaign**. Un résultat rouge peut correspondre à un défaut historique de module : ouvrir le résumé, il explique la commande et le SHA concernés. Le laboratoire n'efface pas ces défauts.
5. Dans **Artifacts**, télécharger **integration-lab-…**. Le ZIP extérieur GitHub contient **evidence.zip**, son SHA256, le rapport Markdown/JSON et **dashboard.html**.
6. Extraire evidence.zip avec le gestionnaire de fichiers Android, puis ouvrir dashboard.html dans un navigateur capable d'ouvrir un fichier HTML local. Les données et styles sont inclus : aucune connexion n'est nécessaire à sa consultation. Le rapport Markdown reste accessible dans le résumé Actions si le navigateur refuse les fichiers locaux.

Aucun Termux ni Android Studio requis. Aucune APK n'est installée par ces actions. Les APK M51 présentes dans evidence.zip sont des artefacts techniques **NON QUALIFIÉS** tant que la réception Android du même build n'est pas satisfaite ; ne pas les présenter comme prêtes à installer.

## Déclencheur manuel et limites actuelles

Le nouveau workflow inclut **workflow_dispatch**, avec SAFE par défaut et ANDROID_LAB conditionnel. GitHub exige sa disponibilité sur la branche par défaut pour le bouton Run workflow. Au relevé initial, main ne contient qu'un README. La mission n'autorise pas sa modification : utiliser la relance Actions ci-dessus, qui exécute SAFE sur le commit choisi et crée un nouvel attempt conservé dans le reçu.

Une nouvelle version de code doit être publiée sur la branche expérimentale ; la relance d'un ancien run conserve son ancien commit. Ne pas confondre les artefacts de deux runs ou attempts. Le dashboard n'exécute aucune commande et ne lance aucun workflow.

ANDROID_LAB exige un émulateur cloud déjà stable et autorisé ; les runners standards n'en fournissent pas automatiquement un. Le LAB refuse les appareils physiques, les API/ABI inconnues et un SystemUI instable avant toute installation. Sans banc approprié, Android reste BLOCKED/NOT_RUN ; audit, tests hôte, compilation et rapports restent utilisables.

Les artefacts expirent90jours après la campagne. Conserver evidence.zip et evidence.zip.sha256 avant cette date. Ne pas importer de modèle, donnée personnelle ou profil privé dans le LAB.
