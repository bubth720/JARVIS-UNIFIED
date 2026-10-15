# ADR-001 — CORE, LLM et UNIFIED

**Statut : proposée — en attente de validation utilisateur.**
Date :15 octobre2026. Remplace comme orientation cible les propositions anciennes
d’application assemblée dans UNIFIED, conservées dans ARCHITECTURE.md historique.
Aucun changement de runtime ou de dépôt d’application n’est autorisé par cette ADR.

## Décision proposée

UNIFIED est la source de vérité technique : registres, preuves, contrats, matrices,
contrôles et roadmap. Ni troisième moteur LLM, ni application Android doublon,
ni runtime requis par CORE. Pas de monorepo applicatif précipité. Le projet
ChatGPT CENTRAL coordonne les décisions humaines ; sa mémoire n’est pas une
synchronisation du code et n’a pas priorité sur les preuves versionnées.

CORE est l’orchestrateur cible et conserve toutes les fonctions du monolithe
historique tant qu’un remplacement testé/récupérable n’existe pas. LLM est le
moteur local privilégié pour une future extraction, non raccordé à CORE aujourd’hui.
Le wrapper LLM de CORE ne sera retiré qu’après parité fonctionnelle, sauvegarde,
restauration et qualification du nouvel adaptateur ; jamais deux moteurs actifs
ou deux résidences sans arbitrage matériel vérifié. Aucun changement appliqué ici.

Session volatile, historique de conversation, catalogue éditorial, souvenirs
personnels durables et contexte natif sont cinq responsabilités distinctes.
« memory » dans LLM002B est de la télémétrie RAM, pas une mémoire personnelle.
Aucune génération, import PDF, conversation ou diagnostic n’autorise un souvenir
sans confirmation explicite du contenu exact. Pas de migration destructive SQLite
ou de réinitialisation sur version inconnue.

VOICE cible les capacités vocales démontrées ; NEXUS cible documents/recherche ;
INTERFACE cible UI/avatar ; SERVICES outils autorisés ; EVOLUTION correctifs
isolés/revus. Les capacités encore dans CORE y restent jusqu’à migration dédiée.
VOLUTION- est un candidat de nom, pas un alias EVOLUTION confirmé. Aucune
suppression/renommage des deux interfaces ou autres dépôts.

## Compatibilité et conséquences

Le contrat ne choisit pas Binder/IPC ou un transport local PC aujourd’hui. Identité
client, permissions, absence/incompatibilité, annulation et libération réelle
précèdent la liaison. Le coordinateur LLM ne réserve pas la RAM et ne contrôle pas
les autres processus. Un arbitre partagé sera une implémentation séparée.

API24 CORE versus API29 LLM : conserver les anciennes cibles comme contraintes,
ne pas augmenter minSdk pour simplifier une fusion. Qualifier explicitement les
appareils réels et prévoir un mode non raccordé si l’API n’est pas supportée.
TABLET Qwen3 0.6B Q4_K_M et MOBILE1.7B sont des références initiales ; CENTRAL
mini-PC reste à qualifier. PLEINE PUISSANCE reste refusée hors matériel qualifié.
GitHub est un outil de développement, jamais une dépendance du runtime hors ligne.

Alternative rejetée : appeler « fusion » une CI verte, un compte GitHub commun,
un DTO, une branche mergée dans son propre dépôt ou un projet ChatGPT partagé.
L’intégration effective exige liaison + chemin d’exécution + tests adaptés ; la
qualification physique exige des essais supplémentaires. Les migrations seront
courtes, réversibles et explicitement approuvées après ce diagnostic.

## Revue de clôture 001F — décision toujours en attente

[Comparaison des trois options et page de décision utilisateur](REVUE-ADR-001F.md).
La revue précise NEXUS comme cible documents/mémoire (stockage), CORE gardant
session, permissions et confirmation. L’objectif initial APK unique et la variante
IPC restent à arbitrer ; aucun transport ni changement de propriétaire physique
des données n’est adopté. Les cinq contrats restent proposés et inchangés.
