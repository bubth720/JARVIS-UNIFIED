# JARVIS IDENTITY ID-001 — Validation utilisateur limitée

**Date :** 17 octobre 2026.  
**Statut :** ARCHITECTURE ET CONSTITUTION APPROUVÉES POUR PRÉPARATION DU DÉVELOPPEMENT ; CONTRAT RUNTIME NON FIGÉ.  
**Fondement :** accord explicite de l'utilisateur dans JARVIS-CENTRAL après revue ID-001 et bilan des blocages LLM 003F (« Vas'y je suis d'accord »). L'accord porte sur le programme de deux chantiers en parallèle : socle IDENTITY et clarification UNIFIED F1/F2/F3.

## Références immuables
- ID-001 : `bubth720/JARVIS-UNIFIED`, `design/identity-001-constitution`, commit `db63719c09435fd2e7863dd72e7bec0e055fa32e`.
- Livrables approuvés sur le fond : `IDENTITY_CONSTITUTION.md`, `IDENTITY_ARCHITECTURE.md`, `IDENTITY_CONTRACTS.md`, `IDENTITY_SECURITY.md`, `IDENTITY_MISSIONS.md`.
- CORE 004C : `bubth720/JAVIS-Local-v2`, `da40ed7155409b85860a22c1dbbfe35029cea29a`.
- LLM 003F : `bubth720/JARVIS-LLM`, `111be993e970051686bd5c27b3115320513a4be7` (testé au commit `b2f6bc052871a2e4f604d9170f385b71c241837b`). **F1/F2/F3 non résolus**.
- ADR-001 et validation expérimentale D4-02D restent en vigueur dans leurs périmètres antérieurs.

## Accord sur la personnalité B
La cible est une assistante locale à identité reconnaissable, au tempérament affirmé, chaleureux et critique, avec goûts et préférences **simulés** et adaptables de façon contrôlée. Elle peut corriger les erreurs factuelles de l'utilisateur avec des sources ou un raisonnement, exposer l'incertitude et exprimer une opinion distincte d'un fait.

L'utilisateur conserve l'autorité finale pour ses préférences, objectifs, décisions et permissions autorisables ; il ne peut par simple injonction rendre vrai un fait faux ou forcer une action interdite par la sécurité. Le style/persona ne confère ni privilège exécutable, ni droit légal, ni preuve de conscience.

## Architecture et responsabilités approuvées
- **CORE** : seul décideur des sessions, permissions, confirmations, snapshots d'identité et actions. Politique exécutée hors prompt, révocation contrôlée.
- **LLM** : moteur local unique interchangeable ; inférence sans nouvelles permissions, sans second moteur lourd.
- **SERVICES** : hébergement initial **candidat** du namespace privé `identity.*` via port; **NEXUS** : cible future; ni migration ni copie parallèle des bases historiques.
- **VOICE / INTERFACE** : intentions expressives bornées sans prétention d'émotions acoustiques ou renderer non implémentés.
- **EVOLUTION** : diagnostics, propositions et tests en isolement, jamais auto-validation/auto-merge/auto-déploiement sensible.
- **UNIFIED** : documents, versions, contrats et preuve de compatibilité, pas runtime.

## Limites de l'accord
1. Les structures `jarvis.identity/1-draft` sont **acceptées comme base de conception**, pas approuvées comme codec ou ABI final. Avant code persisté ou intégration : figer tables fermées, types, limites, digests et vecteurs synthétiques, documenter compatibilité/risques et faire revue. Pas de modification des contrats UNIFIED v1, SERVICES v1 ni des fixtures d'inférence `jarvis.fixture.p2/2`.
2. **ID-002 autorisée comme mission de développement préparatoire en branche isolée**, avec revue préalable de la base CORE et du contrat figé; pas de branche de production ni de changement de comportement historique par défaut. Si le gel est manquant ou la compatibilité avec 004D incertaine, limiter le travail au cadrage/test de fixtures; ne pas introduire de runtime incompatible.
3. La clarification UNIFIED du protocole LLM 003F est **autorisée comme mission documentaire distincte** pour F1 (epochs CORE), F2 (journal CORE/SNAPSHOT), relation des engagements COMMIT et plan F3. Elle ne valide aucun digest candidat et n'autorise pas CORE 004D prématurément.
4. Après validation et publication de la clarification, LLM 003F pourra être corrigée sur **sa branche propre**, avec nouvelles preuves et revue du bundle exact. **CORE 004D reste bloquée** jusqu'à cette revue.
5. Aucune donnée personnelle persistée sans consentement exact. Les propositions contenant des données personnelles restent volatiles avant accord. Aucune migration SQLite, voix/profils/archives, coffre de clés ou application historique.
6. Aucune nouvelle permission Android, réduction thermique/RAM/batterie, second LLM résident, activation PLEINE PUISSANCE sur téléphone, installation personnelle, test physique, auto-fusion ni auto-déploiement.
7. Aucune fusion dans `main` sans accord explicite distinct. Aucune promesse de tests Android, de personnalité active ou de conversation CORE↔LLM E2E avant preuves exécutées.

## État et prochaines preuves
ID-001 est une livraison documentaire ; ses 80 tests UNIFIED sont rapportés, non des tests de runtime IDENTITY. Créer des issues de mission n'exécute aucun code. Chaque mission doit fournir dépôt, branche, commit, diff, tests réellement effectués, blocages, dépendances et action suivante. Priorité : revue de schéma IDENTITY et base CORE d'un côté ; clarification F1/F2/COMMIT puis preuves F3 et gel /2 de l'autre.
