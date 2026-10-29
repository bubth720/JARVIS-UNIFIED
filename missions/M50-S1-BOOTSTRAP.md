# JARVIS — M50-S1 : récupération CI et première coquille intégrée (Codex)

**Statut : mission distribuée — aucun développement S1 exécuté par ce document.**

**Reprise du travail local du 29 octobre : lire d'abord `missions/M50-S1-RECOVERY.md`.** Les commits locaux A1/A2/A3 et UNIFIED n'ont pas été retrouvés publiés sur GitHub au contrôle; récupérer les patches authentiques avant tout développement supplémentaire. Ce fichier n'autorise aucun merge ni activation.
**Propriétaire : UNIFIED / coordination.**
**Branche de mission** : `mission/m50-s1-bootstrap-20261029`, parent M50 `9b1c1c5880d8f0aae2e93e99e6d4d25d2d232e80`.
**Périmètre** : nouvelle branche de développement par dépôt, uniquement labo/testOnly et gardes. PR brouillon vers la branche M50 de chaque propriétaire, ou vers une branche dédiée de mission revue. Aucune fusion `main`.

Lire d'abord :
- `docs/m50/ACCEPTANCE-AND-ROADMAP.md` (gates G1–G8 ; M50 NON ATTEINT)
- `docs/m50/M50-READINESS.md` (blocages précis et runs)
- `docs/m50/CANDIDATE-SOURCES.json` (propositions de SHAs, non lock approuvé)
- `missions/M50-INTEGRATION-2026-10-29.md` (programme long)
- `AGENTS.md` dans chaque dépôt s'il existe et les rapports/campagnes du SHA exact.

## État vérifié au départ de M50-S1

| Module | PR mission | SHA branche | Observation M50 |
|---|---|---|---|
| UNIFIED | #17 | `9b1c1c5880d8f0aae2e93e99e6d4d25d2d232e80` | 5 workflows SUCCESS, pas d'APK |
| CORE (JAVIS-Local-v2) | #26 | `d754a6c19e3c94e415e8506d0d37b8d943951d88` | aucun workflow M50 identifié ; lot4 était vert sur SHA distinct |
| INTERFACE | #13 | `3a0841266fd691b74fae784004804429e6e2e219` | workflow Android SUCCESS, pas de vrai CORE connecté |
| NEXUS | #11 | `c02a00e8d6829de48a212cc03ac392e7ec73c82c` | run40852579751 FAILURE, scope guard avant tests |
| SERVICES | #12 | `8d80d09d6aabf6eac00a7bc6bb4930862bd72812` | Android/JVM SUCCESS ; export productif OFF |
| LLM | #7 | `615a2f165d6479c0bbb7a7daf2281677884b494f` | run40852611085 FAILURE, garde historique manifeste ; 2 workflows skipped |
| VOICE | #26 | `642d9c19bcba35e5ffe686403d50c65aa9dc992a` | Android SUCCESS, 23 skips historiques connus |
| EVOLUTION | #6 | `84ebc2e2b55d48306247fc9045a712294abaf457` | suite JVM SUCCESS, sandbox toujours non qualifiée |

Pas de `codex/m50-*` publiée au moment du relevé. Ne pas conclure d'une CI documentaire verte qu'un produit unifié tourne.

## Objectif strict de S1

Obtenir :
1. une **chaîne de validation M50 indépendante et honnête** pour NEXUS, LLM et CORE ;
2. une première **coquille JARVIS testOnly/isolée** avec interface conversationnelle et CORE de laboratoire **réellement compilés ensemble**, sans second orchestrateur, sans nouveau transport inter-APK et sans passer des réponses mock pour une intelligence native ;
3. un dossier d'acceptation précis G1/G2/G6/G7 indiquant PASS, PARTIAL, BLOCKED, NOT_RUN au SHA et aux artefacts réels.

**S1 ne valide pas M50, ne remplace pas un vrai LLM ni une vraie recherche documentaire.** Les gates G3/G4/G5/G8 restent à qualifier dans les lots suivants.

## Lot A — CI récupérée sans affaiblissement (priorité immédiate)

### A1. NEXUS / owner : NEXUS

**Sources / tests à lire** :
`tools/check-prefusion.py`, `tools/check-prefusion-lot3.py`,
`.github/workflows/nex-07.yml`, `tests/prefusion_lot3/test_scope.py`,
`missions/M50-INTEGRATION-2026-10-29.md`.

**Bug attesté** : `LOT3_REVIEW=false` pour PR#11 base `codex/prefusion-lot3-nexus` / head `mission/m50-integrated-beta-20261029`, le garde ancien refuse l'intégralité du périmètre lot3 déjà approuvé et la mission M50. Erreur **avant** les tests produit.

**Travail** : créer un garde M50 distinct qui vérifie le gel du SHA `c5dee7ab0344a23bfd80b13cd52d09e8b26241dd` et une allowlist **exacte** des seuls fichiers nouveaux M50. Préserver les gardes historiques sur leurs SHAs dans un clone isolé, les deux lanes JVM/Android-hôte et la route historique. Mettre à jour le routage sous conditions strictes base/head, testé positivement ET négativement. Aucun wildcard global/skip/désactivation de tests ; si un changement de garde existe déjà dans une PR concurrente, réutiliser après vérification plutôt que dupliquer.

**Acceptation** : pipeline dédié au SHA exact ; tests négatifs de changement de runtime, suppression, symlink, modification manifeste/permission ou workflow non revue ; suites JVM et Android-hôte réellement déclenchées. Émulateur/physique NON déduit de la seule CI hôte.

### A2. LLM / owner : LLM

**Sources à lire** :
`tools/check-preservation-003e.py`, `.github/workflows/`, la campagne PRE-FUSION de PR#6, `docs/fusion-02/CORE-CONSUMER.md`.
**Bug attesté** : run40852611085 sur PR#7 s'arrête à `Protected baseline drift: app/src/main/AndroidManifest.xml` ; même famille de workflow échoue sur SHA source #6. La campagne PRE-FUSION différente `40547525669` est verte sur #6 avec 303 tests. Il serait trompeur d'attribuer ce vert à #7.

**Travail** : établir SHA historique/manifeste préservés et portée réelle des gardes ; proposer une campagne M50 qui teste exactement le nouveau delta en laissant les gardes 003E au commit 003E, et vérifie l'absence de changement au runtime/manifest/ABI entre source #6 et travail M50. Ne pas supprimer un garde, réécrire une empreinte historique, masquer l'échec, modifier un manifest de production ni télécharger un poids de modèle.

**Acceptation** : exécution au HEAD avec les 303 cas si l'environnement les expose, contrôle app/domain/native/ARM64/lint/APK exacts, logs et provenance. Si l'ancien workflow reste rouge par conception hors domaine, le dire explicitement et conserver la CI M50 séparée : pas de faux vert.

### A3. CORE / owner : CORE

Lire PR#25, `AGENTS.md`, `SessionCoordinator.kt`, `AppGraph.kt`, les tests CORE lot3 et lot4.

**Travail** : pipeline M50 de régression au SHA de la branche développeur, gardes historiques recontrôlés séparément, builds/lint des variantes historiques, tests synthétiques positifs/négatifs. Aucun AppGraph productif ni modèle natif modifié avant intégration décidée.

**Acceptation** : rapport exact des tests exécutés (629 de lot3 à comparer, 12 tests synthétiques lot4), pas de somme aveugle ; un workflow délibérément lancé et vert sur branche M50, zéro suppression de tests.

## Lot B — Première coquille Android sur émulateur (après A)

**Owners** : INTERFACE + CORE + UNIFIED. Créer une variante indépendante **testOnly**, applicationId distinct, sources synthétiques et stockage volatile, sans import irréversible des dépôts. Vérifier Gradle/Kotlin/Java/SDK/ABI, licences et namespaces avant tout assemblage. La CI peut copier les sources épinglées temporairement pour compiler, sans modifier les branches originales. Si cette action implique changement de licences, import massif de sources, signature, manifest/export/permissions sensibles, **STOP et demander accord utilisateur**.

- Un écran tactile JARVIS affiche chat, état de CORE, états d'indisponibilité et éventuellement avatar en IDLE (pas de lèvres simulées).
- CORE fournit un `ConversationPort` **in-process** de laboratoire, échange Submit/Ack/Chunk/Stop/Error/UNKNOWN. Pas de Binder, socket, permission nouvelle, second modèle ni boucle réseau.
- Les réponses du **simulateur** sont marquées explicitement LAB/SYNTHETIC, jamais prêtes comme LLM. Cas sans modèle => LLM UNAVAILABLE. Les documents et SERVICES affichent UNSUPPORTED/READ_ONLY quand non qualifiés.
- Tests réels instrumentation API29/35 : démarrage, réponse synthétique clairement identifiée, stop, replay, rotation, force-stop/reprise, absence de permissions et de connexion, comportement mode avion. Si CI ne dispose pas d'émulateur, conserver NOT_RUN.
- Prouver APK `testOnly` + manifeste, appId, minSdk, APK SHA256, logs, zéro fuite de chemin/texte, rollback en supprimant cette variante. Une coquille Android qui compile **sans** exécution instrumentée ne satisfait que les contrôles build, pas le gate G2/G7 complet.

**Important** : pour M50 lui-même, il faudra ensuite un vrai LLM natif, un vrai SAF/doc index et un essai physique autorisé. Ne pas monter artificiellement le score à 50 % par un mock.

## Lot C — Réception et plan lot suivant

UNIFIED lit les PR produites, met à jour `docs/m50/M50-READINESS.md` ou rapport versionné `docs/m50/M50-S1-RESULTS.md` avec :
- sources et trees SHA complets et différence entre branches #15/#16 ;
- par module : mission/branche/commit/diff/CI/commandes/TEST PASS FAIL SKIP NOT_RUN ;
- risques de régression, API/ABI, licences, permissions, rollback ;
- résultats du laboratoire in-process et captures de fixtures synthétiques ;
- statut M50-G1..G8 sans aucun PASS non prouvé ;
- **deux suites proposées** : S2 NEXUS recherche réelle + SERVICES read-only, S3 LLM JNI réel + session CORE ; les séparer si l'une est bloquée.

## Interdictions absolues

Aucune fusion `main`, suppression historique, migration de données, déploiement sur appareil personnel, ajout de permissions, connexion réseau obligatoire, transport authentifié fictif, consentement implicite, écriture SAF productive, correctif EVOLUTION automatique ni affirmation « 50 % atteint ». Le principe ADR-002 a été approuvé **comme conception uniquement** : ni `authorizeAtCommit` productif ni journal durable ne sont autorisés.

## Message court à envoyer à Codex

« Dans `bubth720/JARVIS-UNIFIED`, branche `mission/m50-s1-bootstrap-20261029`, lis `missions/M50-S1-BOOTSTRAP.md` et exécute A1/A2/A3 en parallèle sur branches propres ; seulement après leurs preuves, prépare B en variante testOnly isolée. Publie PR brouillon, SHA/tests exacts et bilan M50. Aucun merge main ni activation sensible. »
