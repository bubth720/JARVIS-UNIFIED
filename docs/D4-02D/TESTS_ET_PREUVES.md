# D4-02D — références, validations exécutées et tests futurs

Photographie du **17 octobre 2026**, module UNIFIED, branche
`design/d4-02d-bootstrap-recovery`, issue exactement de
`0dbb978994994fa3210124f1e150ca23426d410d`.
Les scénarios ci-dessous sont des critères **à implémenter**, pas des tests de
protocole déjà passés. Aucun source CORE/LLM exécuté ou modifié dans cette mission.

## Références Git vérifiées

| Référence | Observation Git / niveau de preuve |
|---|---|
| [UNIFIED D4-02C](https://github.com/bubth720/JARVIS-UNIFIED/tree/0dbb978994994fa3210124f1e150ca23426d410d) | HEAD local et tête distante audit/d4-02c-core-llm-convergence égales à la base avant branchement ; checkout initial propre |
| [CORE004C](https://github.com/bubth720/JAVIS-Local-v2/tree/da40ed7155409b85860a22c1dbbfe35029cea29a) | Commit existant et tête distante fixture/004c-p2-client ; ancêtre004B29646448, deux commits supplémentaires :71be9ef puis da40ed7 documentaire |
| [LLM003E code](https://github.com/bubth720/JARVIS-LLM/tree/5751646acd4a7bb13caaea4b96a4ab3a68ec6adb) | Commit existant, ancêtre de la clôture ; contient corrections native/capteurs et fixture |
| [LLM003E clôture](https://github.com/bubth720/JARVIS-LLM/tree/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5) | Tête distante fixture/003e-p2-secure-endpoint ; diff depuis5751646 : ajout EVIDENCE.json et RAPPORT.md, modification VALIDATION.md seulement ; aucun code différent |

Filiation calculée avec merge-base et log ; têtes vérifiées par ls-remote.
Acquisition en clones nus ignorés à l’intérieur du seul dépôt UNIFIED. Lecture de
64 fichiers fixture/documentaires aux SHA ci-dessus ; empreintes recalculables
avec git show SHA:chemin puis SHA-256, aucun checkout externe modifié.
Les caches locaux `.audit-cache/d4-02d/` sont ignorés, non nécessaires pour lire
la livraison : sources immuables et résultats essentiels sont consignés ici.

## Constat de contrat vérifié indépendamment des rapports

Quatre fichiers canoniques comparés octet par octet entre CORE004C et LLM003E :
CONTRACT.txt et les trois AIDL IP2Endpoint/IP2Arbiter/IP2AuthorizationCallback.
Le bundle est calculé sur chemins relatifs triés, UTF-8 chemin,NUL,contenu,NUL.
Résultat : **fab6a66a6b99302884849cd1d8aef97cd761082dc20680a4b036d7bc99d5c3c9**,
identique à REFERENCE.json. Codec CORE volontairement réduit au préfixe portable,
pas prétendu identique à tout Wire.kt LLM.

/1 expose hello/submit/status/cancel et authorize(callback) seulement : aucune
inspection initiale/reprise. /2 reste une proposition sans empreinte fabriquée.
Les corrections003E de rendu SYSTEM unique et de borne512 demandée/768 chargée
sont conservées ; ne pas répéter les anciennes divergences003D comme si003E ne
les avait pas traitées. Le blocage restant est le bootstrap/recovery authentifié.

## Preuves de validation des modules sources : portée limitée

- CORE RESULTS.json/VALIDATION.md rapportent187 tests historiques et36 de fixture,
  sans échec/erreur/saut, APK compilées, fixture non signée faute de clé commune.
  JVM/Robolectric, pas Binder réel. **Non réexécutés ici**, aucune conclusion
  Actions CORE attachée à da40ed7 vérifiée durant D4-02D.
- LLM VALIDATION/EVIDENCE rapportent87 domaine +27 app +19 fixture =133 JUnit,
  zéro échec/erreur/saut, CTest1/1 et harnais JNI/GGUF Linux réussi. Le
  [run38975009901](https://github.com/bubth720/JARVIS-LLM/actions/runs/38975009901)
  a été consulté directement : HTTP200, champ public Status Success et SHA
  complet5751646 présent. Les totaux détaillés ci-dessus viennent des documents
  versionnés ; XML, ZIP et logs détaillés non téléchargés dans D4-02D.
- Compilation ARM64, contrôles APK/certificats et faux moteurs de tests ne
  constituent pas une preuve de permission signature ou Binder entre deux APK.
  Aucun test Android physique, émulateur, génération réelle ou installation exécuté
  ici. Les rapports sources déclarent aussi l’E2E inter-APK non exécuté.
- Aucune clé commune de laboratoire durable ni preuve de mort OS fiable fournie
  par ces sources. Les clés CI éphémères ne peuvent être utilisées pour signer
  une future paire ; aucun secret extrait, transféré ou ajouté à Git.

## Résultats UNIFIED réellement obtenus

Environnement Linux x86_64, Python3.12.14. Scripts et tests existants inchangés :

```text
python3 -m unittest discover -s tests -v
Ran 27 tests in 0.042s
OK
python3 -m unittest discover -s registry/tests -v
Ran 23 tests in 0.229s
OK
python3 -m unittest discover -s backup_prototype/tests -v
Ran 30 tests in 12.480s
OK
python3 scripts/validate_unified.py
{"contracts": 5, "invalid_examples_rejected": 5, "repositories": 9, "valid_examples": 5}
python3 registry/scripts/update_registry.py --validate-only
Registre valide : 9 dépôts, 16 missions.
```

**80 tests réussis, 0 échec, 0 erreur, 0 ignoré**, tous codes retour0.
Sauvegarde testée exclusivement sur fixtures fictives, pas sur données réelles.
Sorties intégrales locales ignorées : `.audit-cache/d4-02d/audit-contracts.txt`,
`registry.txt`, `backup.txt`, `unified-validator.txt`, `registry-validator.txt` ;
plateforme/durées dans tests.json. Ces validations vérifient UNIFIED et ses
contrats actuels, pas la sûreté d’un protocole futur non implémenté.
Contrôle documentaire final exécuté : quatre livrables non vides, **33 liens**
vérifiés (fichiers locaux, objets Git immuables, page Actions observée), **64
empreintes source** recalculées conformes. git diff --check : code0, aucune sortie.
Diff contre0dbb978 vide sur contrats/v1, ADR/décisions, D4-02C, registre, tests,
scripts, sauvegarde, workflows et AGENTS. Aucun autre dépôt de travail modifié ;
les lectures externes passent exclusivement par les clones nus locaux ignorés.
Les liens blob sont vérifiés par existence de l’objet Git/path, pas par une
requête HTTP à chaque URL. Le validateur UNIFIED a aussi été réexécuté après
rédaction avec la même sortie réussie. Détails ignorés : final-checks.json.
La publication et le SHA final sont confirmés dans le compte rendu de livraison
après commit ; aucun succès distant anticipé dans ce document.

## Matrice reproductible pour003F/004D — aucun scénario exécuté ici

Prérequis communs : horloge et aléa injectables uniquement dans les tests ; journaux
privés temporaires, vraie implémentation d’état/codec sous test ; événements worker
contrôlés et compteurs de load/import/generate/unload. Faux runtime et identité
simulée explicitement étiquetés, jamais empaquetés dans production. Chaque test
vérifie trace des transitions, fichiers avant/après, barrières et nombre d’appels.
Un refus ne vaut pas réussite si le journal est perdu ou un second moteur chargé.

| ID / scénario | Arrange et injection précise | Oracle exigé / preuve conservée |
|---|---|---|
| B01 premier démarrage propre | Paire neuve explicitement provisionnée, journaux initiaux, aucun backend touché ; DISCOVER→CHALLENGE→COMMIT | Deux preuves fraîches NOT_STARTED/NO_RESIDENCY, ACK durables exacts ; CORE IDLE_VERIFIED, génération0 ; 0 load/import/generate ; ensuite seul un **nouveau** mandat peut réserver1 |
| B02 redémarrage sans réservation | Commit /2 antérieur sain génération7, détruire instances puis relire ; nonce/epochs nouveaux | Jamais IDLE avant ré-attestation ; high-water mark7 conservé, ancienne preuve refusée, nouvelle opération8 seulement |
| B03 redémarrage avec opération inachevée | Bail7 RUNNING écrit avant crash ; active en RAM perdue | UNKNOWN et bail7 conservé, aucune allocation ; INSPECT retrouve clé/digest durable ; sans preuve terminale l’essai **doit rester bloqué** |
| B04 interruption avec propriétaire vivant | Suspendre retour JNI/import, perdre client puis demander stop | effective_end faux tant que l’appel ne revient pas ; après retour puis unload réel et journal terminal : nouvelle réconciliation autorisée, texte annulé absent |
| B05 journal corrompu | Tronquer payload, checksum faux, version inconnue, .bak/.new incohérents, clé manquante, panne lecture/écriture | JOURNAL_BLOCKED ; octets sources préservés, aucun journal « propre » substitué, 0 grant/load ; récupération automatique absente |
| B06 réponse ancienne/falsifiée | Rejouer nonce consommé, changer champ de clé/epoch/génération/pilot_id/digest/seq ; réponse tardive après5s | Refus explicite, réservation/barrière intactes, aucun dernier bail remplacé ; hash seul ne contourne pas identité |
| B07 mauvaise signature | Certificat différent, permission remplacée, shared UID, rotation, bon package mauvais UID ou callback relayé | Refus avant décodage applicatif et tout accès natif ; Robolectric séparé d’un essai noyau réel Android ultérieur |
| B08 fin native et unload | Même clé : stop, retour JNI, unload, journal terminal ; injecter chaque événement isolément | Aucun événement seul ne libère ; les preuves complètes corrélées + commit/ACK seulement résolvent, nouveau mandat séparé ; pas de RSS=0 exigé/annoncé |
| B09 absence de preuve | Pair muet, status UNKNOWN, journal sans reçu terminal, observation incomplète ou backend orphelin | Barrière maintenue et admission refusée ; pas d’attestation positive ni de timeout libérant |
| B10 mort de service vs processus | Recréer Service avec worker ancien vivant ; puis nouveau process_epoch avec ancienne opération non résolue | Premier : ancienne autorité toujours référencée/drainée ; second : nouvelle instance vide ne libère pas l’ancienne ; PID/Binder morts insuffisants |
| B11 ACK perdu | Couper avant/après chacune des écritures PREPARED/COMMIT/ACK, puis relire | Reprise idempotente de même décision ou nouveau tour frais si expiré ; jamais submit rejoué, génération jamais réduite, aucune double réservation |
| B12 cleanup échoué | Faire échouer unload, demande de retry absente puis explicite ; maintenir mêmes handles/baux | CLEANUP_FAILED reste fermé sans demande ; retry après fin réelle, échec conserve tout ; succès ne suffit pas sans journal + réconciliation ; quarantaine historique non touchée |
| B13 négociation | /1 ancien, /2 digest inconnu, mauvais major, champs dupliqués/tailles/UTF-8/nombres non canoniques | RECOVERY_UNSUPPORTED/INCOMPATIBLE/refus codec, 0 appel natif ; pas de retrait de champs ni fallback /1 |
| B14 course snapshot/charge | Concurrence submit/import/Activity avec défi et commit ; changements seq/phase entre snapshot et écriture | Gate unique empêche allocation ; précondition changée invalide tour ; jamais deux propriétaires lourds ni deux registres de backend |
| B15 reboot/horloge | Recréer toutes instances avec elapsedRealtime inférieur, anciennes deadlines et callbacks | Nouvelles incarnations/nonce, ancienne fenêtre invalide ; aucune comparaison cross-boot ouvrant le gate |
| B16 enrôlement perdu/rollback | Supprimer seulement le journal de test, marqueur connu du pair ; baisser seq/génération ; deux marqueurs différents | JOURNAL_MISSING/ENROLMENT_CONFLICT, pas de réenrôlement auto ; rollback coordonné des deux sandboxes déclaré hors garantie logicielle |
| B17 état propre sans calcul | Échec d’autorisation avant tout dispatch et bail durable CORE conservé | NOT_STARTED n’invente ni native_ever_started ni texte ; preuve fraîche de non-dispatch + aucun import/bail suffit seulement à réconcilier, pas à prétendre une inférence |
| B18 saturation/deadlock | Files/callbacks complets, expiration en plein commit, Binder bloqué, verrous concurrents | Refus borné ou blocage conservateur ; aucun lock tenu en attente réseau/Binder/worker empêchant drainage ; pas de thread interrompu déclaré natif terminé |

Étapes de qualification ultérieure, après autorisation : deux APK de fixtures
signées par clé dédiée, version/digest/pins figés, API29+ ARM64 de laboratoire,
aucune donnée privée, GGUF public déjà disponible et SHA vérifié pour les seuls
scénarios natifs. Ne pas télécharger/installer automatiquement. Examiner le
foreground réel LLM et les capteurs, ne jamais les forcer pour obtenir un succès.
B01/B02 peuvent valider le contrôle **sans modèle** ; ils ne prouvent pas le
parcours CORE→JNI. Rejouer B04/B08/B10/B11 avec vrais processus/worker et journal
après crash avant toute annonce E2E. Linux JNI reste une preuve différente.

## Risques de régression à bloquer en revue

| Risque | Protection / test |
|---|---|
| Résoudre RECOVERY_REQUIRED en passant une RecoveryEvidence fabriquée | Seul vérificateur authentifié/typé peut appeler la transition ; B06/B07/B09 |
| Nouvelle autorité remplaçant ProcessResources ou admission004B | Registry observe les vrais propriétaires, pas double acquisition ; B14 et suites historiques inchangées |
| Oublier backend après recréation Service | Autorité Application/processus, service_epoch distinct ; B10 |
| SharedPreferences default=false interprété comme journal sain | Lecture discriminée absent/corrompu/incomplet avec marqueur, B05/B16 ; jamais simple booléen |
| Ancien receipt sans request_digest connu dans CORE | Refus de résolution si rattachement impossible, aucune reconstruction de contenu ; B03/B06 |
| Libérer sur ACK incomplet ou avant fsync | B11 à chaque frontière et B05 échec écriture |
| Ouvrir génération en phase de négociation | Aucun import/create/prepareOperation dans chemin contrôle ; B01/B09/B13 |
| Modifier budgets/SDK/corpus pour simplifier | Diff protégés, suites historiques ; SYSTEM exact, profils/thermique/batterie et API24 inchangés |
| Confondre tests simulés, CI, JNI Linux et Android | Résultats séparés par SHA/plateforme, niveaux de preuves explicites |

## Lectures de code vérifiables

Les liens suivants sont attachés aux commits demandés ; ils permettent de retrouver
les responsabilités observées sans dépendre du cache local.

| Fichier | Constat | SHA-256 du blob lu |
|---|---|---|
| [JAVIS-Local-v2/PilotArbiter.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/fixtures/p2-client/src/main/java/com/stark/jarvislocal/fixture/PilotArbiter.kt) | RECOVERY_REQUIRED initial ; reconcile local ; générations et preuves | `3dffb62687297d52a0d35ced9bf08b5e5eb11e916aaf67a31dee2cfee0867e20` |
| [JAVIS-Local-v2/AtomicPilotJournal.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/fixtures/p2-client/src/main/java/com/stark/jarvislocal/fixture/AtomicPilotJournal.kt) | AtomicFile, checksum, fsync, version1 et cas absent | `3fdc4e40c2ef5b9283d1468638ba0dfe0fddf67f75ea5850b0c7b198f3b8d9dd` |
| [JAVIS-Local-v2/PilotRuntime.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/fixtures/p2-client/src/main/java/com/stark/jarvislocal/fixture/PilotRuntime.kt) | Seul propriétaire llm ; pas de fournisseur de preuve ; GrantRegistry volatile | `8df62172a16b576bdab103a000644b925e0ab4ef3b22ce5a7672800cf75506c8` |
| [JAVIS-Local-v2/P2Session.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/fixtures/p2-client/src/main/java/com/stark/jarvislocal/fixture/P2Session.kt) | Corrélation, polling, perte=blocage, aucun replay submit | `49c08113265bbfc086bf4f79500d1f20a80ee8a4a80adfa22668994fc4804468` |
| [JAVIS-Local-v2/BinderIdentityChecks.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/fixtures/p2-client/src/main/java/com/stark/jarvislocal/fixture/BinderIdentityChecks.kt) | UID/package/certificat et service/permission explicites | `5586a7877f67deb49c83518cc9551f8e4a4e859bbec001e5aff277aede57fba4` |
| [JAVIS-Local-v2/P2ArbiterService.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/fixtures/p2-client/src/main/java/fr/jarvis/fixture/core/P2ArbiterService.kt) | Contrôle UID avant unmarshalling et authorize exact | `263b26ebda70f7d121765bdbd144ee7a0ab3ac851596649b0d80814c144ce5b6` |
| [JAVIS-Local-v2/REFERENCE.json](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/fixtures/p2-client/REFERENCE.json) | Provenance5751646 et empreintes canoniques | `657a2d4aab5c838854ab199b0684d59ee70d47b3e43bbf8330b7ca9fecf4c2f8` |
| [JAVIS-Local-v2/QUALIFICATION.md](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/docs/mission-004c/QUALIFICATION.md) | Conditions laboratoire/clé ; aucun E2E Android | `fdfb0d0786c9e9135cc3a655469cc7a23e9fc6368fcbb836baf533e8cbc0cc15` |
| [JAVIS-Local-v2/RESULTS.json](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/docs/mission-004c/RESULTS.json) | Résultats rapportés187+36, blocage explicite | `1c3c868e6a4bf2348ecd6ba07c03865ace30e0bb5884dedf1a2f666b352b1e17` |
| [JARVIS-LLM/CONTRACT.txt](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-contract/CONTRACT.txt) | Contrat /1 fermé, limites et absence recovery | `7a850a58aed04511fb3104931e4109f76b87a13304222f5197c14d9b7c403cb6` |
| [JARVIS-LLM/IP2Endpoint.aidl](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-contract/src/main/aidl/fr/jarvis/fixture/p2/IP2Endpoint.aidl) | Les quatre méthodes existantes et indices à préserver | `2a52d720e93e7781fd7828ca5a0928d1acf94c11c61b18ab5a3de68286b976bc` |
| [JARVIS-LLM/P2EndpointService.kt](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/P2EndpointService.kt) | Epoch de service ; journal SharedPreferences ; status lié à active | `97a23d7527e1f6d863c7ca5391ee0bc2ab0485d69a56f8782fd4ad3e531782c0` |
| [JARVIS-LLM/EndpointController.kt](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/EndpointController.kt) | UNKNOWN, drainage, unload et commit avant libération | `c407d6460e653dea7c399ee005f49602ec5a7bcc6bd17cbdf80aab5443b622f5` |
| [JARVIS-LLM/AndroidRuntime.kt](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/AndroidRuntime.kt) | Vrais backend/import/baux ; création paresseuse | `2c5491be8f7dd1e745d39a511cb9bb1f3f48c4724c018bb54215a9916975469d` |
| [JARVIS-LLM/FixtureApplication.kt](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/FixtureApplication.kt) | Composition processus actuelle sans autorité globale de reprise | `b934254e0defd3831819d97f4908d86ebed2a658491ea479164aacef678f8bf7` |
| [JARVIS-LLM/Identity.kt](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/Identity.kt) | Certificat unique et UID/package | `a40104369c5349f704db57aadc910c1775636ddc4985366bce68206802f07d1b` |
| [JARVIS-LLM/ArbiterConnection.kt](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/ArbiterConnection.kt) | Callback authentifié et mandat réel | `5e9a38f17c058b4a3517423eefeccfbf15a1a996b29e42d1a8b50894b5f9b6ee` |
| [JARVIS-LLM/CONVERGENCE.md](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/docs/mission-003e/CONVERGENCE.md) | Mesure/rendu natifs déjà corrigés en003E | `056abfa579177a539dd15e1ae8829e3a690b3c3d4e1393e2bcb613009c037066` |
| [JARVIS-LLM/SIGNATURES.md](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/docs/mission-003e/SIGNATURES.md) | Clés éphémères, collision applicationId sonde/CORE | `3981df900b1008b10e255a65d38194d193c746e790281d2d2b658602480a56ea` |
| [JARVIS-LLM/VALIDATION.md](https://github.com/bubth720/JARVIS-LLM/blob/030152a5f3d888017ad7a7fe8026f2e2c48e8fd5/docs/mission-003e/VALIDATION.md) | 133 tests rapportés et limites physiques | `c5dadde3747d9421b5ea18d0660ee1f1f86d316a436ec4df817f0b7338dbc140` |
