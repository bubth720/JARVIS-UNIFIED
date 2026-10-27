# Contrats, assemblage et pilote — propositions non approuvées

**REVIEW_REQUIRED**, aucune permission d'architecture/runtime/écriture. ADR-001 reste approuvée comme orientation ; ADR-002 reste proposée. Ce dossier ne modifie aucun contrat gelé.

## U1 — engagement à décider

Sources mission : CORE SessionCoordinator/TaskCoordinator, INTEGRATOR-CONTRACT C0 ; SERVICES CommitAuthorization/ServicesWirePreflight ; UNIFIED ADR-002-PROPOSAL/OperationReceipt2-draft. C0 historique cite encore un SERVICES sans authorizeAtCommit ; le code actuel fournit une proposition additive non connectée, pas une autorité de production.

| Sujet | Écart vérifié | Résolution NON APPROUVÉE |
|---|---|---|
| Génération | SERVICES >=0, wire draft1..2^53−1 | Garder fixtures0 ; futur adaptateur versionné refuse0/overflow, jamais +1 silencieux |
| COMPLETED / COMMITTED | Fin logique CORE != effet relu et durable | Garder états distincts, preuve propriétaire/readback exigés |
| DISPATCHED / COMMIT_STARTED | Worker accepte != point d'engagement | Spécifier les deux points/reçus, aucun alias |
| Journal | RAM/callback ne prouvent pas reprise après crash | CORE journalise décision/consommation ; SERVICES début d'effet selon ordre approuvé, aucun second orchestrateur |
| Consentement | Booléen UI/LLM/document ou jeton synthétique ne donne pas autorité | CORE lie usage unique à aperçu exact/session/request/generation/politique/deadline/source/destination neuve |
| Révocation | Revalidation au retour trop tard après effet | Même sérialisation que fence ; avant => aucun effet, après => effet possible honnêtement signalé ; pas rollback universel |
| ACK/UNKNOWN | Erreur après effet != absence d'écriture | UNKNOWN collant/durable, jamais retry/reset implicite ; réconciliation propriétaire distincte |
| Readback | Write/close réussi ne prouve pas tout le fichier | Relecture intégrale SHA/taille et original identique, corrélation/source/grant revérifiés |
| Identité | UUID/digest/paquet déclaré ne prouve pas origine | UID kernel, paquet/certificat/permission épinglés à revoir ; aucun transport ajouté |

Avant implémentation : décider versions/états, ordre des journaux, fenêtre de révocation et reprise process death/rotation/force-stop ; tests de coupure à chaque point. Pas de migration des anciens reçus. Les validateurs de revue restent BLOCKED même sur valeurs compatibles.

## U3 — assemblage réversible proposé

| Option | Après décision formelle | Avantage / coût |
|---|---|---|
| Fédération multi-repo avec lock | Lock revu repo/branche/SHA/arbre/licence ; récupération sources uniquement au développement | Autonomie et rollback par module ; contrats consommateurs et versions d'outils à vérifier |
| Monorepo modulaire | Import contrôlé des historiques sous modules autonomes, provenance/notices/builds séparés | Changements coordonnés ; migration majeure, chemins Gradle, namespaces/JNI, signatures/stockages, taille à revoir |

Préférence de première qualification soumise à revue : **fédération documentaire avec lock**, sans trancher topologie finale. EVIDENCE est une photo, pas un lock de release approuvé. Aucun import de sources/historiques, submodule auto-fetch runtime, chemin Gradle changé, migration ou renommage. Les applications autonomes restent conservées.

Pipeline proposé :
1. Déterminer modules touchés depuis lock revu, refuser SHA incomplet/périmé ou arbre différent.
2. Exécuter suite propriétaire complète puis contrats de ses consommateurs : NEXUS/SERVICES→CORE, CORE→UI, LLM/VOICE→CORE.
3. Séparer Python/JVM, Robolectric, build ABI, instrumentation et physique ; publier SHA/nombres/échecs/skips/hashes sans vert d'ancêtre.
4. Avant release : campagne complète tous modules/consommateurs, licences/ABI/schémas et appareil autorisé, même après changed-module vert.
5. Rollback par revert isolé, conservation UNKNOWN/binaires/signatures/données ; retour Git ne remplace pas restauration persistante.

Ce pipeline reste une spécification, sans réseau obligatoire au runtime.

## U4 — pilote documentaire/CSV proposé, actuellement BLOQUÉ

LLM/VOICE/avatar/EVOLUTION optionnels : ne pas les rendre dépendances du premier pilote lecture/CSV.
1. Fixtures synthétiques TXT/PDF2pages/CSV0.10+0.20 ; SHA/taille source ; hors ligne effectivement attesté sur émulateur autorisé.
2. ACTION_OPEN_DOCUMENT réel, flags/grant/provider/révocation vérifiés ; aucun URI ou grant fabriqué.
3. NEXUS sonde CREATE/MATCH/vocab/BM25, index/citation/réouverture ; URI/version/SHA/page/offset et unité explicite, pas conversion silencieuse UTF16/UTF8. Sonde négative => UNSUPPORTED, aucune citation inventée.
4. CORE session/request/generation/politique, contrôle avant/après, annulation/délai. Documents comme données non fiables, jamais droits.
5. SERVICES aperçu exact CSV, destination neuve, consentement unique CORE après protocole approuvé ; fence/journaux aux points décidés. Refus avant engagement => aucun effet.
6. ACK corrélé puis fermeture/relecture complète SHA/taille, source intacte ; perte ACK après effet => UNKNOWN sans réessai.
7. Cas négatifs : refus permissions, source modifiée/trop grosse, grant révoqué, UID/signature invalides, replay, expiration, interruption/crash avant/après fence, WAL/corruption préservés.
8. Conserver conversation/offline et anciennes fonctions, rotation/arrêt ; RAM/latence/thermique distincts de qualité fonctionnelle. Physique sur accord séparé.

Aujourd'hui **BLOCKED** : FTS5 plateforme24/25, vrai SAF persistant NEXUS, autorité CORE/SERVICES non approuvée et transport consommateur non qualifié. La réussite SAF de laboratoire SERVICES ne déverrouille pas ce pilote. Aucun APK final ni résultat matériel inventé.

## Décisions réservées, éléments concrets

- Accepter/refuser fédération effective ou monorepo modulaire/imports, avant migration.
- Accepter/refuser ADR-002, versions/états/journaux/fence ci-dessus avant écriture ; aucun amendement des schémas présumé.
- Backend SQLite NEXUS : [BACKENDS au SHA mission](https://github.com/bubth720/JARVIS-NEXUS/blob/bdb51f77a5fe105dbff43d43032882fe1474a4ee/docs/fusion-02/BACKENDS.md), AndroidX2.5.2 candidat inspecté uniquement, Requery/FTS4 non substituts qualifiés.
- LLM : [diff exact à approuver](https://github.com/bubth720/JARVIS-LLM/blob/12fc58a81ceee70eedbba2d0b187b1294bae6283/docs/mission-003f-f3b/DIFF-A-APPROUVER.md), patch SHA256 be4bcce5ec7066851a09e2e372edca562a45dad3a3a88e35b6a7d5792c07b374 **non appliqué**. Revue sèche != accord JNI/ABI.
- Installation personnelle, connexion sensible, permission nouvelle, export production et merge main : accords distincts.

Rollback : revert des seuls fichiers docs/prefusion sur branche, aucun état produit changé. Phases B purement OFF reprenables lorsque l'environnement d'exécution revient ; aucun raccordement actif avant gates.
