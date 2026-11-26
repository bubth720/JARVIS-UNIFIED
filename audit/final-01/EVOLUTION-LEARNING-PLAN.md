# F00 — Séparation : mémoire, savoir documentaire, diagnostic, sandbox, entraînement

Ce document est un plan, pas une implémentation. Il fixe les frontières à respecter par F06, F08 et F09.

| Couche | Ce qu'elle contient | Écrit par | Condition d'écriture | État au 21/11 |
|---|---|---|---|---|
| **Mémoire personnelle durable** | Faits et préférences de l'utilisateur | CORE (`MemoryApprovalWorkflow`, `ConfirmedMemoryStore`) | Texte exact présenté et **confirmé** par l'utilisateur ; l'absence de réponse vaut refus | Embarqué (mem-02 ⊂ CORE `5da9838`) ; tests émulateur h, b3, a5, g6 verts |
| **Savoir documentaire** | Documents importés, index FTS5, citations | NEXUS | Import explicite ; les documents restent des **sources**, jamais des consignes | Embarqué (pin `06ccf98`) ; F4, L, Q, R verts |
| **Diagnostic technique** | Mesures expurgées, incidents, comparaisons avant/après | EVOLUTION (lecture seule) | Sources de mesure autorisées par CORE ; aucune conversation | Code et 51 tests ; adaptateur CORE absent |
| **Proposition d'amélioration** | Diff, justification, preuves, risques, rollback | EVOLUTION | Dossier de revue uniquement ; aucune PR ni édition automatique | Format présent ; signature ED25519 synthétique |
| **Essai en sandbox** | Exécution d'un candidat sur une fixture éphémère | EVOLUTION, sur laboratoire qualifié | Sandbox **qualifiée** et autorisation spécifique avant le premier essai | **BLOCKED** : `SANDBOX_NOT_QUALIFIED` |
| **Déploiement** | Modification d'un module installé | Propriétaire | Porte d'approbation distincte de l'essai, jamais automatique | Hors périmètre |
| **Entraînement des poids** | Ajustement du LLM | — | **Interdit sur Android** ; protocole PC futur distinct | Non prévu |

Invariants à tester en F09 :

- Aucun candidat rejeté n'est persisté.
- Une hypothèse n'est jamais promue en fait.
- Une mémoire révoquée ou expirée n'est plus rappelée.
- Le rappel fonctionne après redémarrage, sans fuite entre sessions.
- Les données sensibles sont exclues par défaut.
