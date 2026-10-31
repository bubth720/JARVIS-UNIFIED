# M50-S1 — registre d'exécution

M50 NON ATTEINT. Ce dossier coordonne les preuves sans runtime UNIFIED.
Base S1 : `a67116b44d828b435a7a1a662d3cd0200993e1c1`, arbre `f2b7bcf01d193c59b9de997ab205e9ff12683431`.
Branche : `codex/m50-s1-unified-evidence-20261029`, PR brouillon vers `mission/m50-s1-bootstrap-20261029`.

## Préparation vérifiée

- Programme central, huit gates et sept missions propriétaires lus.
- [Provenance observée](M50-S1-PROVENANCE.json) : huit HEAD/arbre de mission, branches par défaut, CI au SHA exact et versions existantes. Il ne s'agit pas d'un lock approuvé.
- [Revue de coquille](M50-S1-SHELL-REVIEW.md) et [sélection de sept fichiers](M50-S1-SOURCE-SELECTION.json) : copies temporaires, pas d'import massif ou changement de graphe applicatif historique.
- UNIFIED #15 et #16 divergent : merge-base `e4c678faf630a0a98adfaecd7a87fc11dfd82486`, complément #16 en avance de 2 commits et en retard de 12. Aucune reprise automatique.
- Le réseau Git du shell est indisponible (connexion au proxy port8080). Le connecteur GitHub a permis de récupérer le checkout existant : 337 blobs, arbre et commit source vérifiés par SHA Git avant toute modification.

## Résultat des lots et blocage

A1 NEXUS, A2 LLM et A3 CORE ont été préparés en parallèle depuis leurs HEAD M50. Les modifications sont livrées en patches locaux séparés avec tests, empreintes et corps de PR. Aucun nouveau commit distant, PR brouillon ou run CI produit n'est confirmé. Les appels d'écriture du connecteur ont été interrompus sans résultat après attente prolongée ; ils ne constituent pas une publication. La branche de travail UNIFIED distante créée avant ces interruptions reste au SHA source S1, sans les modifications locales.

| Lot | Correction préparée | Tests locaux réellement exécutés | Reste NOT_RUN |
|---|---|---|---|
| A1 NEXUS | Route base/head/dépôt stricte et checkout HEAD, baseline lot3 gelé, deux lanes préservées | 18 PASS, 0 FAIL, 0 SKIP, fixtures Python synthétiques | Garde Git historique complet, JVM, Android-hôte, build/lint |
| A2 LLM | Campagne M50 additive au HEAD ; garde003E au SHA003E ; mission/source lot1 gelés | 21 PASS, 0 FAIL, 0 SKIP, fixtures Python synthétiques | Gardes Git historiques, 303 cas, CTest, ARM64, lint et APK |
| A3 CORE | Nouvelle régression M50 au HEAD ; gardes historiques séparés ; cinq variantes conservées | 20 PASS, 0 FAIL, 0 SKIP, fixtures Git/Python synthétiques | Gardes historiques, 629 cas lot3 et 12 cas lot4, Gradle/build/lint |

Les nombres 629/12/303 restent des références historiques et objectifs de comparaison, jamais des résultats obtenus par S1. Les patches n'altèrent ni runtime, manifeste, permission, modèle, ABI, dépendance, contrat ou test historique. NEXUS conserve ses commandes JVM/Android-hôte et sa route ancienne. LLM conserve `android.yml`, dont le rouge hors domaine reste visible ; une future CI M50 verte ne doit pas le masquer.

Commits locaux, non publiés : NEXUS `be70faa41d202d77eb8cf0cc5c831e10cfb020b5`, arbre `1045f29dc045ee739630c97f2c241a6f45561a42` ; LLM `b670181987d39d27e2d0d9574fa448397a38fe42`, arbre `e5f723c2010b1add0b7dbc3a78d261214e4d3c16`. Ces objets Git sont conservés dans des bases partielles (métadonnées d'arbre et nouveaux blobs), sans clone produit complet ni exécution Gradle. Les patches restent la voie de reprise dans un clone propre ; leurs empreintes et parents mission figurent dans le bundle.

CORE : commit local `5da98383ed12cb5a54e896fbe57560bacc432fb5`, arbre `bef8a470e25847cff8a09351792133adfa268c38`, parent exact `d754a6c19e3c94e415e8506d0d37b8d943951d88`. Sa base objets est également partielle ; elle ne qualifie aucun build.

B : **BLOCKED_A_CI_UNCONFIRMED**. Faisabilité revue uniquement ; aucune variante créée. Assemblage, APK, SHA256 APK et instrumentation API29/35 NOT_RUN. Le programme S1 exige les preuves de A avant B : leur absence interdit d'annoncer une coquille compilée. Le projet proposé est autonome dans `labs/m50-s1` INTERFACE, applicationId `fr.jarvis.lab.m50s1`, testOnly, min29/compile35/target35, sans permissions/JNI, avec copies temporaires de sept fichiers CORE/UI. Il réutilise un unique `SessionCoordinator` et le vrai `CoreConversationClientAdapter`, en excluant `AppGraph` et les stockages historiques. Les réponses synthétiques seront marquées LAB/SYNTHETIC ; LLM UNAVAILABLE, NEXUS UNSUPPORTED, VOICE/EVOLUTION OFF. Les licences de projet CORE/UI ne sont pas établies : distribution et lock restent non qualifiés.

## Contrôles UNIFIED observés

Sur le contenu initial S1 : `python3 scripts/validate_unified.py` PASS ; `python3 -m unittest discover -s tests -v` 41 PASS ; `registry/tests` 23 PASS ; `backup_prototype/tests` 30 PASS ; `tooling/campaign/tests` 32 PASS ; `tooling/integration/tests` 21 PASS ; `tooling/integration/fusion02_tests` PASS ; `tooling/integration/adr002_lot4_tests` 28 PASS ; `workspace/tests` 20 PASS. Aucun résultat Android ou physique n'en est déduit. Les suites restent distinctes et ne constituent pas un pourcentage.

Le workflow S1 ajouté exécute les contrôles existants au HEAD exact, archive sujet/arbre et comptes de tests, sans modifier les contrôles historiques.

Une campagne journalisée complète a ensuite été exécutée au commit local UNIFIED `048fdfc8a693af9b9cdba6a0d145669ed58d630c` (arbre `9a39c4c4450ae6ea34ea8466c8c3f3c96447a1e2`) : **261 PASS, 0 FAIL, 0 ERROR, 0 SKIP**, dix suites distinctes, plus validateur de livraison PASS. Décomposition : tests 41, registre 23, sauvegarde 30, campagne 32, intégration 21, fusion02 20, ADR002 28, U01 23, U00 23, workspace 20. Les exécutions préalables ne sont pas additionnées à ce total. Commandes exactes, durée/sortie par suite, SHA/arbre sujet et plateforme sont conservés dans `UNIFIED/tests/summary.json` et les logs du bundle. Les ajouts documentaires de bilan postérieurs à cette campagne passent de nouveau le validateur ; ils ne sont pas présentés comme une CI distante.

## Huit gates au relevé de livraison locale

[Registre machine de réception](RELEASE-EVIDENCE.json) : aucun gate accepté, aucun lock approuvé, aucun pourcentage global quantifié.

| Gate | État | Preuve manquante |
|---|---|---|
| G1 | PARTIAL | Huit sources/arbre vérifiés ; licences/SBOM et lock approuvé manquants |
| G2 | NOT_RUN | Aucune APK-lab ; B bloqué par A |
| G3 | BLOCKED | Chargement/génération/libération LLM réels |
| G4 | BLOCKED | Recherche Android et sélection SAF réelle |
| G5 | PARTIAL | Consommation réelle CORE des outils lecture/CSV |
| G6 | PARTIAL | Gardes synthétiques seulement ; frontière in-process intégrée et lifecycle instrumenté manquants |
| G7 | NOT_RUN | Aucune nouvelle CI produit ; régression HEAD et instrumentation API29/35 intégrée manquantes |
| G8 | NOT_RUN | Appareil explicitement autorisé, métriques et reprise |

## Limites, rollback, suite

Aucun merge/main, schéma/migration, permission, modèle, signature de production ou installation personnelle modifié. Les huit branches par défaut ont été relues à `2026-10-29T19:36:33Z` : leurs huit HEAD sont identiques au relevé initial. INTERFACE a pour branche par défaut `development/mission-002` et VOICE `feat/pocket-tts-cpu-prototype` ; ne pas supposer `main` partout. Rollback : ne pas appliquer les patches, ou retirer leurs seuls ajouts et le routage CI NEXUS ; aucune donnée historique touchée.

Les fichiers locaux, logs, SHA256 et corps de PR sont regroupés dans `/workspace/m50-s1-delivery/`. Ils ne sont pas des PR GitHub créées. Le commit local UNIFIED et son patch sont identifiés dans le manifeste du bundle ; les correctifs propriétaires sans historique Git complet sont livrés comme patches, sans inventer de SHA publié.

Prochaine action immédiate : rétablir les écritures GitHub ou un accès Git opérationnel, appliquer les patches dans les clones exacts, créer les trois PR brouillon et observer leurs CI jusqu'au résultat. Corriger les échecs réels sans affaiblissement, puis seulement réaliser B et ses instruments API29/35. Aucune nouvelle autorisation sensible n'est déduite de cette reprise de publication déjà demandée par l'utilisateur.

S2 proposé : recherche NEXUS réellement disponible + SERVICES lecture seule, sans nouveau driver/migration avant accord. S3 proposé séparément : LLM JNI réel + session CORE, sans télécharger de poids ni changer ABI sans accord. L'un ne doit pas attendre artificiellement l'autre.
