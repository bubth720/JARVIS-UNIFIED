# JARVIS-UNIFIED — Décision officielle ADR-001

Date : 15 octobre 2026

Décision : APPROUVÉE AVEC PRÉCISIONS

Référence documentaire locale : `USER-ADR-001-2026-10-15`.
Source : message explicite de l’utilisateur dans cette conversation, intitulé
« JARVIS-UNIFIED — Décision officielle ADR-001 ». Cet identifiant est une référence
locale de documentation, pas un identifiant GitHub ni une preuve de publication.
Le texte de la décision et de son périmètre autorisé est reproduit ci-dessous.

---

Je valide explicitement l'ADR-001, option 3 : architecture modulaire hybride, avec JARVIS CORE comme orchestrateur et des adaptateurs interchangeables.

Cette approbation concerne exclusivement l'orientation architecturale.

## 1. Architecture approuvée

- JARVIS-UNIFIED : registre technique central, contrats, versions, compatibilités, preuves de tests et feuille de route. Aucun rôle d'orchestrateur à l'exécution.
- JARVIS CORE : autorité centrale des sessions, décisions, permissions, confirmations et orchestration.
- JARVIS LLM : inférence locale, moteurs et modèles interchangeables.
- JARVIS VOICE : synthèse vocale, identités vocales et fonctions associées.
- JARVIS INTERFACE : interface utilisateur et avatar.
- JARVIS NEXUS : cible future pour les documents, la recherche et le stockage des souvenirs confirmés.
- JARVIS SERVICES : fonctionnalités complémentaires soumises aux autorisations CORE.
- JARVIS EVOLUTION : diagnostics et propositions de correctifs isolés, jamais appliqués automatiquement sans approbation.

## 2. Précisions obligatoires

### A — Modularité

Conserver initialement les applications autonomes existantes, avec une interface commune comme objectif ultérieur.

Ne pas imposer huit APK distinctes ni un monolithe unique. Le déploiement définitif sera décidé après qualification.

### B — Ressources

Pour la configuration Android pilote, privilégier un seul travail lourd à la fois.

Maintenir les protections RAM, température, batterie et annulation.

Plusieurs modèles résidents ne pourront être autorisés que sur une configuration matériellement qualifiée, avec arbitrage vérifié. Aucun second chargement non maîtrisé.

Conserver le mode PLEINE PUISSANCE pour un futur matériel adapté, sans activation prématurée sur téléphone ou tablette.

### C — Préservation

Aucune suppression des fonctions historiques CORE sans remplacement fonctionnel démontré.

Toute migration de données doit être réversible, précédée d'une sauvegarde vérifiée et accompagnée de tests de restauration.

Préserver SQLite, documents, profils vocaux, signatures et données privées.

Toute nouvelle mémorisation personnelle durable exige une confirmation explicite du contenu exact.

### D — Portabilité

Préserver le fonctionnement 100 % local et hors ligne. Préparer la compatibilité Android → mini-PC, avec moteurs remplaçables.

## 3. Décisions restant ouvertes

Ne pas considérer comme approuvés :

- Le transport IPC définitif.
- La stratégie de signature et d'authentification entre applications.
- Le nombre définitif d'APK.
- L'emplacement et l'implémentation de l'arbitre global de ressources.
- Les migrations physiques de données.
- Le renommage ou la suppression des dépôts candidats.
- Les paramètres de performance non qualifiés sur appareils.

Ces sujets nécessitent des propositions techniques et, lorsqu'il y a un changement sensible, une autorisation distincte.

## 4. Périmètre autorisé

Je t'autorise uniquement à consigner cette décision architecturale dans la documentation JARVIS-UNIFIED, sur une branche de travail préservant la consolidation existante.

Mettre à jour le statut de l'ADR-001 en indiquant clairement les précisions approuvées, les décisions encore ouvertes et la référence de cette validation utilisateur.

Ne pas modifier les contrats v1 automatiquement si cette décision nécessite de nouveaux schémas. Documenter les évolutions proposées.

Interdictions :

- Aucune fusion dans main.
- Aucune modification des autres dépôts JARVIS.
- Aucun développement d'adaptateur.
- Aucun raccordement CORE/LLM/VOICE.
- Aucune migration de données.
- Aucune suppression de code existant.
- Aucun contournement des permissions GitHub.

Si la publication GitHub reste bloquée par HTTP 403, préserver les modifications documentaires localement et signaler le blocage.

## 5. Compte rendu attendu

Fournir :

- Le document ADR-001 actualisé.
- Le statut exact de l'approbation et des réserves.
- La branche et le commit documentaire, si créés.
- Les vérifications documentaires réellement exécutées.
- Les décisions toujours en attente.
- La prochaine action recommandée.

Cette approbation clôt le choix de l'orientation architecturale. Elle n'autorise ni son déploiement ni l'intégration technique des modules.
