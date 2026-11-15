# MISSION JARVIS-RESEARCH-01 — Recherche Internet contrôlée et dossiers documentaires

**Statut : préparée — EXÉCUTION NON AUTORISÉE** (décision du propriétaire du 14/11/2026).

## Condition de lancement

1. CONVERSATION-01 et l'intégration du Command Center V2 sont terminées.
2. Le propriétaire a donné son **autorisation explicite**.

Jusque-là, aucun code, aucun accès réseau, aucune permission ni dépendance n'est ajouté pour cette mission.

## Résumé de la demande (texte intégral conservé par le propriétaire)

| Fonctionnalité | Contenu |
|---|---|
| **A — Collecte de fichiers** | Missions limitées à des domaines explicitement autorisés. Vérification de chaque URL et de chaque redirection. Métadonnées et empreintes conservées. Espace temporaire isolé. Doublons, classement et renommage sans perte des originaux. |
| **B — Dossiers documentaires** | Personnalités publiques et informations professionnelles publiques uniquement. Chaque affirmation sourcée et classée confirmé / incertain / non vérifié. Exports Markdown, PDF et DOCX. |
| **C — File d'attente des téléchargements (prioritaire)** | Les éléments incertains sont mis en attente sans bloquer la mission. Validation groupée des seuls éléments affichés et sélectionnés, jamais permanente. Les éléments hors périmètre ou dangereux sont bloqués, pas proposés. Décisions journalisées. Nouvelle validation si l'élément change. |
| **D — Gestionnaire de missions** | Section « Recherches » du Command Center. Suspension et reprise, erreurs, comparaison, notification locale. |
| **E — Mise à jour** | Comparaison avec l'existant, signalement des contradictions, version antérieure préservée, confirmation avant tout remplacement. |

**Sécurité réseau :**
- Hors ligne par défaut.
- Réseau limité à la mission, sur liste blanche.
- Aucun accès aux adresses locales ou privées.
- Aucun proxy ni contournement (authentification, CAPTCHA, accès payant).
- Journal local des accès.

## Point d'architecture identifié dès maintenant (à traiter au lot R00)

L'APK actuelle **ne déclare pas la permission INTERNET**. Cette propriété est vérifiée en CI et affichée dans
SECURITY. La mission demande de ne pas la perdre silencieusement. Option à étudier en R00 : un composant
réseau séparé (APK ou module distinct, explicitement installé et autorisé), qui dépose les fichiers dans un
espace d'échange vérifié. L'application principale resterait sans Internet.

Le module MISSIONS du Command Center est aujourd'hui affiché « à connecter ».

## Plan prévu (non démarré)

| Lot | Contenu |
|---|---|
| R00 | Audit |
| R01 | WEB CONTROL |
| R02 | File d'attente |
| R03 | Organisation NEXUS |
| R04 | Dossiers documentaires |
| R05 | Interface |
| R06 | Qualification |

Les 18 tests d'acceptation de la spécification seront exécutés sur des sites de test contrôlés, avec des
données publiques ou synthétiques uniquement.
