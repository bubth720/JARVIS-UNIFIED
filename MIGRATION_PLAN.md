# Plan de migration — missions courtes

Statut : propositions, aucune autorisation de développement implicite.
Chaque mission se déroule sur une branche dédiée de JARVIS-UNIFIED, avec revue
avant toute fusion. Les trois sources restent conservées et inchangées.
Les critères renvoient au [TEST_PLAN.md](TEST_PLAN.md).

| Mission | Périmètre limité | Livrable et sortie attendue | Condition de passage / retour arrière |
|---|---|---|---|
| 001 — présente | Audit, architecture, contrats conceptuels | Cinq documents, SHAs et limites explicites | Relecture ; aucun moteur copié ni main fusionné |
| 002 — préservation | Inventaire des données/installations et protocole d'export/restauration ; appareils et clés identifiés par métadonnées publiques | Matrice package/version/certificat, échantillons synthétiques, format d'archive choisi, procédure d'export source supportée | Restauration synthétique sans perte, chemins d'extraction légitimes identifiés ; conserver anciens APK et fichiers |
| 003 — contrats | Schémas et interfaces CORE/LLM/VOICE/ressources + doubles de test seulement | Contrats v1, unités/bornes/erreurs, tests de confirmation et annulation | Aucun moteur natif, invariants et erreurs testés ; annuler la branche en cas de désaccord |
| 004 — coquille Android | Une app vide et composition de modules sans moteurs | Build reproductible, SDK/ABI et signature de développement identifiés, écran diagnostics passif | Vérification permissions et démarrage sans calcul ; aucune installation remplaçant une source |
| 005 — LLM unique | Adaptateur du seul backend LLM 003B | Import GGUF vérifié, génération/arrêt/déchargement avec protections inchangées | Tests domaine/natifs/JNI/contrôle APK ; aucun wrapper CORE concurrent |
| 006 — CORE texte et données | Commandes, catalogue, historique, mémoire confirmée ; import depuis archive synthétique | Parité fonctionnelle et migrations non destructives | Confirmation non contournable, transactions et restauration exacte ; copie source conservée |
| 007 — documents | PDF, passages, recherche lexicale, citations et budget tokenisé | Corpus de référence et bornes de volume | Aucun original supprimé, erreurs PDF contrôlées ; index reconstruisible séparément |
| 008 — Whisper | Capture et transcription derrière ports, sans VOICE | Pipeline mono finalisé et nettoyé, annulation native qualifiée | Micro refusé, rotation, arrêt/réentrée, limites audio testés sur appareil |
| 009A — VOICE qualifiée séparément | Vérifier pack/profil existant et lecteur 005F, sans changer le LLM | Rapport audibilité/intelligibilité/ressemblance et ressources, consentement | Tests privés locaux Redmi/POCO ; aucune voix générique en remplacement ; profil précédent préservé |
| 009B — VOICE intégrée | Adapter le backend neuronal et les profils compatibles | Texte final→synthèse différée→lecture, baux communs | Échecs distincts, arrêt réel, absence de co-résidence non qualifiée ; réponse texte maintenue |
| 010 — parcours unifié | Texte, documents, STT, mémoire et VOICE avec export/restauration complet | APK de qualification et matrice de non-régression | Mode avion, données et profils récupérables ; anciennes apps intactes |
| 011 — CENTRAL | Étude puis adaptateur PC optionnel, d'abord transfert par archive | Qualification CPU/RAM/OS/modèles/profils ; protocole local si autorisé | Android autonome sans PC ; aucun réseau/cloud imposé |

002 est la prochaine mission recommandée : les clés, les sandbox Android et les
formats de profil sont des contraintes de récupération qu'il faut résoudre avant
les changements d'identité applicative. Elle ne doit pas extraire de secrets ni
ouvrir les données personnelles dans le cloud. Si un export exige une modification
d'une source, fournir d'abord son périmètre précis et obtenir une mission séparée ;
les sources restent inchangées dans le présent plan.

## Ordre et dépendances

002 → 003 → 004 → 005 → 006 → 007/008 → 009B → 010. 009A peut être menée comme
qualification isolée après 002, avant tout couplage. 011 commence après une version
locale restaurable ; aucune dépendance du parcours Android à cette mission.
Ne pas empiler migrations de données, changement de moteur et changement de
signature dans une seule livraison. Chaque mission doit définir sa base SHA,
les sources réutilisées et les licences avant copie.

## Préservation et retour arrière

Avant tout essai sur données réelles : conserver l'installation d'origine,
version/APK/certificat et export local vérifié. Une nouvelle signature incompatible
n'autorise jamais à désinstaller l'ancienne app. Les clés privées sont conservées
par leur propriétaire hors Git ; une clé absente ne se régénère pas sous la même
identité prétendue. Les builds de test utilisent un package distinct si nécessaire.

Importer vers un nouvel espace, comparer contenu/IDs/dates/compteurs/hashes,
obtenir confirmation, activer atomiquement ; garder l'ancien espace tant que la
restauration n'est pas répétée avec succès. Aucun downgrade destructif ni
réinitialisation automatique sur version inconnue. Les données réelles ne servent
pas de fixtures. Les bugs source déjà identifiés restent traçables pendant le
remplacement, sans les contourner par la suppression d'une capacité.

## Définition de fin d'une mission

Rapport concis : comportement livré, preuves exécutées et provenance, tests
réussis/échoués/ignorés/non exécutés, limites, impact sur données/permissions et
retour arrière. Aucun « clonage validé » sans écoute humaine ciblée et consentie ;
aucun « modèle qualifié » sur la seule base d'une compilation ou d'un RSS cloud.
Les tests bloqués nécessaires empêchent le passage de leur porte de qualité.
La fusion complète, les changements source, publication et fusion dans main
restent hors de la Mission 001.
