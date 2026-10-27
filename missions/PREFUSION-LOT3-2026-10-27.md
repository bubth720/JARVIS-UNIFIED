# JARVIS — LOT 3 / Pré-intégration contrôlée — UNI-PF-02

**État : mission distribuée dans GitHub, PAS une exécution Codex.**
Dépôt directeur : `bubth720/JARVIS-UNIFIED`.
Branche : `mission/prefusion-lot3-20261027`.
Référence initiale : UNIFIED `b8f22bb7091c29b654f5e958e97da4f94434b164` (PR #10, cinq workflows SUCCESS sur cette tête).
Toutes les missions propriétaires sont déposées au même chemin dans leurs branches de lot3.

## Objectif

Passer de huit modules qualifiés isolément à un **premier parcours documentaire unifié en laboratoire**, sans le présenter comme produit Android utilisable ni lever les blocages de confiance et d'écriture. Les étapes sensibles se limitent à des propositions et tests de refus.

## A. Travaux Codex parallélisables immédiatement

| Priorité | Module / PR lot précédent | Nouvelle mission source | Livrable principal |
| --- | --- | --- | --- |
| 1 | CORE [#21](https://github.com/bubth720/JAVIS-Local-v2/pull/21) | [CORE-PF-02](https://github.com/bubth720/JAVIS-Local-v2/blob/mission/prefusion-lot3-20261027/missions/PREFUSION-LOT3-2026-10-27.md) | Port de laboratoire CORE→UI, événements/replay/refus ; transport production OFF |
| 1 | INTERFACE [#10](https://github.com/bubth720/JARVIS-INTERFACE/pull/10) | [UI-PF-02](https://github.com/bubth720/JARVIS-INTERFACE/blob/mission/prefusion-lot3-20261027/missions/PREFUSION-LOT3-2026-10-27.md) | Vraies instrumentations Android API26/35 ; faux READY/replay refusés |
| 1 | SERVICES [#7](https://github.com/bubth720/JARVIS-SERVICES/pull/7) | [SERV-PF-02](https://github.com/bubth720/JARVIS-SERVICES/blob/mission/prefusion-lot3-20261027/missions/PREFUSION-LOT3-2026-10-27.md) | Contrat autorité/commit simulé et dossier de décision ADR-002 |
| 2 | NEXUS [#8](https://github.com/bubth720/JARVIS-NEXUS/pull/8) | [NEX-PF-02](https://github.com/bubth720/JARVIS-NEXUS/blob/mission/prefusion-lot3-20261027/missions/PREFUSION-LOT3-2026-10-27.md) | Matrice FTS5/SAF, option backend et diagnostics API24/25 |

Les quatre tâches ci-dessus sont indépendantes et peuvent être distribuées simultanément **uniquement pour les prototypes OFF, tests et documents**. Elles ne modifient pas `main`.

## B. Coordination UNIFIED à réaliser par Codex

1. **Relever l'état réel.** Vérifier PR #10/#8/#7/#6 LLM/#25 VOICE et les PR CORE #21, INTERFACE #10, EVOLUTION #5 ; noter SHA40, commit de base, arbre, CI exacte, statut, écarts. Ne pas recopier les chiffres d'une discussion comme des tests nouveaux.
2. **Geler les contrats candidats.** Préparer un tableau versionné CORE→UI, CORE→NEXUS, CORE→SERVICES, CORE→LLM/VOICE. Pour chaque lien, producteur/consommateur, identité de l'appelant, schema, SDK, permissions, rôle CORE, blocages et test consommateur. Les schémas historiques UNIFIED v1 et les propositions v2 ne sont **pas modifiés**.
3. **ADR-002 — décision explicite.** Proposer (ne pas adopter) l'autorité unique CORE, génération, instant exact de commit et ordre des journaux, double envoi/ACK perdu, token unique, révocation et readback durable. Transmettre trois décisions ouvertes à l'utilisateur avec avantages/inconvénients ; aucune écriture réelle avant autorisation.
4. **Premier scénario d'intégration uniquement synthétique.** Parcours source TXT/CSV de test → demande CORE → résultat/citation simulés ou explicitement UNSUPPORTED → affichage INTERFACE. Les réponses documentaires inventées, les faux statuts READY et toute mutation SAF sont refusés.
5. **Blocages de livraison.** FTS5/SAF NEXUS, signature CORE↔UI, JNI/unload LLM/VOICE et sandbox EVOLUTION doivent rester BLOCKED ou NOT_RUN jusqu'aux preuves propriétaires et essais matériels. Ne pas déclarer une APK unifiée disponible.
6. **CI.** Exécuter les validations UNIFIED U00/U01/U02, scripts de scope et tests ajoutés ; exiger les campagnes propriétaires exactes avant révision des gates. Publier `docs/prefusion/LOT3-ASSESSMENT.md`, matrice et PR brouillon sur la branche de mission.

## C. Politique GitHub et sûreté

- Chaque agent lit le `AGENTS.md` du dépôt s'il existe et sa mission propriétaire.
- Développement sur `codex/prefusion-lot3-*` **créée depuis la branche de mission**, PR brouillon **vers `mission/prefusion-lot3-20261027`**.
- Le lot ne permet jamais : fusion `main`, déplacement massif de code, migration, changement de licence/ABI/minSdk, activation transport signée, SAF écriture production, collecte/voix personnelle, auto-correctif EVOLUTION ou installation sur appareil.
- Une PR documentaire avec tests verts ne lève pas un gate. Chaque changement sensible exige une demande de validation distincte.

## D. Rapport attendu avant tout autre lot

Pour chaque module : mission, branche, SHA commit/arbre, fichiers modifiés, commandes, nombre de tests réussis/échoués/sautés/non exécutés (JVM, Robolectric, Android-hôte, émulateur, physique), PR, régression, blocage et rollback.

### Commande courte d'exécution

`Codex : ouvre JARVIS-UNIFIED, branche mission/prefusion-lot3-20261027, lis missions/PREFUSION-LOT3-2026-10-27.md et distribue les quatre missions liées. Exécute seulement les travaux OFF et les tests, crée les branches/PR brouillon, rapporte les SHA et blocages. Rien dans main, aucune activation sensible.`

**Aucune migration ni fusion définitive n'est autorisée par ce document.**
