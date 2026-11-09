# LAB-01 — livraison du laboratoire exécutable

Module : UNIFIED, outillage de développement. Dépôt : bubth720/JARVIS-UNIFIED. Mission : LAB-01. Branche : **codex/lab-01-complete-integration**. [PR23 brouillon](https://github.com/bubth720/JARVIS-UNIFIED/pull/23).

**Le LAB est opérationnel pour les campagnes SAFE. La qualification de l'ensemble des modules reste PARTIAL.** La campagne réelle est correctement marquée FAIL : deux gardes historiques LLM échouent et un cas VOICE est ignoré faute de ses préconditions. Ces résultats ne sont pas neutralisés. Android n'est pas qualifié ; aucune APK prête à installer n'est déclarée.

## Code et preuve exacte

Code exécuté : **1a10328459a71578a6e56427b848cb6467fba57d** ; tree **b37563981c7fb2db0a236c48cda6adcfa016aff4**. Le reçu CI confirme lab_dirty=false. Base de coordination : a7625a31513be5c56fa36ed946fbdcd3c23c2a15. Les ajouts documentaires finaux ont leur propre commit à la tête de PR23 ; ils ne remplacent pas ce SHA pour les résultats et APK.

Cahier intégral analysé : JARVIS_MISSION_LAB-01.pdf, 16 pages, SHA256 `73b6480af0dc3b667b14654a142cc88003f31a692a199850b9876e4f5aa590e6`. Les références de huit modules ont été résolues en SHA complets via GitHub puis vérifiées à nouveau sur leurs objets Git et leurs fichiers. [Verrou complet](../config/modules.lock.json), [reçu essentiel de livraison](../reports/CI-RECEIPT.json).

| Module | Référence exécutée |
|---|---|
| CORE | 5da98383ed12cb5a54e896fbe57560bacc432fb5 |
| LLM | 08fbda527d187f324d94e0adafbca76fa955a343 |
| VOICE | fe57452fcb33f5b6870070f30ba6c5f1d349c4ba |
| INTERFACE | b9a9506785b8851f55789ed4329c9394a3937447 |
| NEXUS | eae61fb62a9ccd4073b96d71454f89e5a943eae9 |
| SERVICES | 8d80d09d6aabf6eac00a7bc6bb4930862bd72812 |
| EVOLUTION | 84ebc2e2b55d48306247fc9045a712294abaf457 |
| UNIFIED | a7625a31513be5c56fa36ed946fbdcd3c23c2a15 |

## CI et campagne réelles

[Run SAFE 42638506700](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638506700), campagne fa4db0c6-75b6-47ca-8e69-940413456fd2 :

| Contrôle | Résultat exact |
|---|---|
| Tests du LAB | 48 PASS, zéro saut, job129234262072 SUCCESS |
| Campagne des modules | 19 commandes exécutées, 16 PASS / 3 FAIL ; sortie2, job129234370613 FAILURE |
| Vérification indépendante de l'export | SUCCESS |
| Résumé et publication des artefacts | SUCCESS malgré l'échec de campagne |
| Références et intégrité après tests/builds | 8/8 PASS, sources préservées |

Les cinq CI historiques UNIFIED du même SHA sont SUCCESS : [U00](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638518385), [U01](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638518479), [U02](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638518294), [FUSION-02](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638518454), [validation/backup](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638518518). La [CI LAB de PR](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638518672) est SUCCESS pour les 48 tests ; la campagne complète y est SKIPPED par sélection de déclencheur, car elle est déjà lancée au push. Aucune assertion de module n'est ignorée par cette sélection.

Les premiers essais sont conservés : commit37992f1/run42637073935 refusé avant les jobs pour syntaxe YAML ligne61 ; correction au commit5c5930f, campagnes42637416572 et42637428156 complètes et FAIL. Leurs références et empreintes d'archives sont conservées dans le reçu. La dernière version évite les campagnes complètes doublées push/PR. Aucun retry Android ni effacement d'échec.

## Résultats des modules — aucune addition trompeuse

| Module / tâche | Type et résultat |
|---|---|
| CORE, garde M50-S1 | 20 UNIT PASS ; ceci ne rejoue pas tous les tests Android de SessionCoordinator |
| LLM PERF02 | 34 UNIT PASS |
| LLM helpers C++ | 31 cas uniques PASS en exécution simple puis ASan/UBSan ; aucun modèle/JNI complet/TTFT qualifié |
| LLM gardes historiques | 2 STATIC FAIL : périmètre PRE-FUSION dépassé par les ajouts historiques ; Protected baseline drift: app/src/main/AndroidManifest.xml |
| INTERFACE, tests hôte | 17 UNIT PASS |
| INTERFACE M51 | 6 JVM historiques,15 baseline, 15 candidat PASS :36 invocations, 15 cas uniques |
| NEXUS | 10 tests SQLite/Python PASS ;100 JVM PASS, assemblage CLI effectué |
| SERVICES | 134 JVM PASS |
| EVOLUTION | 40 JVM PASS, distribution CLI construite |
| VOICE | 52 JVM recensés :51 PASS, 1 SKIPPED, 0 failure/error ; tâche LAB FAIL selon sa politique de complétude |
| UNIFIED | validateur PASS ; suites41/23/30/32/21/51 PASS, chacune conservée séparément |

Le cas VOICE ignoré est PublicNeutralParityTests.publicAlbaNeutralAndUnsupportedStyleAreBitIdenticalToUnchanged005gBackend. Son assumeTrue exige POCKET_EXPERIMENTAL_MODEL_DIR et IDENTITY_PUBLIC_ALBA_WAV, un pack FP32 existant et une référence licenciée. Ils ne sont pas fournis à cette campagne ; aucun téléchargement ou recours à des données privées n'est effectué. [JUnit original](../reports/voice-skipped.xml). Le LAB n'affirme donc aucune parité audio réelle.

Les logs des [gardes LLM](../reports/llm-manifest-guard.log) et [helpers natifs](../reports/llm-native-helpers.log) restent disponibles. Un garde en échec n'est ni assoupli ni remplacé. Des unités réussies ne valident pas la racine LAB_CLOUD ou une connexion CORE–LLM.

## APK et export

[Artefact GitHub13686030170](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638506700/artifacts/13686030170) : contient evidence.zip, son empreinte et les vues du rapport. Archive extérieure SHA256 `611cbe0d3126a7db952bfc6be2a46c55e04151cbb0ecd453061169002b3eb761`.

evidence.zip SHA256 : `d3403eca0abd32e8f0003906a4a5e69bfd3361461a93101da11f1fd10c0f3e42`. Ses82 fichiers ont été vérifiés indépendamment après téléchargement ; le vérificateur interne et sha256sum -c passent. Aucun poids, clé de signature, voix privée ou fichier utilisateur n'est exporté.

| APK | SHA256 |
|---|---|
| M51-baseline.apk | af928d83eca4c2439bf3fca25ba2f15f9d33c2068d499630d79a1e5bf6e227e5 |
| M51-baseline-tests.apk | e15b021cf0d475dcb60b123f7901517212d5cc8681621b3b191e59eaeb091e97 |
| M51-candidate.apk | 711c0d87f239681dabbffb01a01b8cb6cfd2b312d97d214a6e244e66decf7fea |
| M51-candidate-tests.apk | 49b1b264580ac5c8965c22646037ddffb8fd3af81c46cfee9e3922f420760dd1 |

Paquets fr.jarvis.v1.lab.baseline et fr.jarvis.v1.lab, testOnly=true, allowBackup=false, minSDK 26 / target35, version51. Signature v2 vérifiée par le collecteur historique et de nouveau après téléchargement ; certificat debug `ec80f2b6c0f33b867d3caf23845aa37952544fbfb0c8e8b55f7bcb8a2f10dc9c`. Aucune permission plateforme, receiver interne AndroidX sous signature seulement. Quatre ABI, seul helper graphique AndroidX et aucun JNI LLM dans ces APK. Elles restent **NON QUALIFIÉES**.

Les artefacts expirent le 7 février 2027 : conserver evidence.zip et son SHA256 avant échéance. Sauvegarde intégrale locale : /workspace/lab01-20261108/BACKUP, avec manifeste ; ce workspace n'est pas un hébergement durable. Les essentiels, le dashboard et les anomalies sont aussi versionnés dans reports/.

## Couverture et limites

Le noyau fonctionne : CLI, huit références, préimages, commandes autorisées, processus bornés, builds séparés, APK contrôlées, registres, rapports, dashboard, export et récupération sans retry. Les397 fichiers de la coordination de départ et les sources des huit modules sont préservés. Aucun contrat historique, garde, JNI, signature personnelle ou base utilisateur n'est réécrit.

La matrice calculée comporte56 relations de toolchain :38 INCOMPATIBLE et 18 UNKNOWN. Elle décrit des candidats à un build commun, pas une interdiction de compilation indépendante. Le LAB ne les assemble pas arbitrairement. Les cinq schémas UNIFIED ont leurs exemples valides/invalides vérifiés ; les copies de schémas VOICE sont statiquement identiques. Huit relations de contrats restent préparées/inconnues ou bloquées, jamais présentées comme raccordements productifs.

La comparaison conserve les tests non rejoués et ne déclare pas une ancienne régression résolue sur un simple PASS d'inventaire. Les recommandations restent prudentes ; pas de remplacement de moteur ou de gain mémoire/latence sans données comparables. Les métriques absentes restent UNKNOWN/NOT_RUN, jamais zéro.

Le dashboard a neuf vues et a été rendu avec Chromium aux formats mobile/desktop, mode hors ligne, zéro requête HTTP. La politique du navigateur cloud bloque les file:// ; elle n'a pas été modifiée. Le test rend les mêmes octets HTML en mémoire. Le reçu JSON régénéré est identique octet pour octet et les données embarquées dans le HTML sont identiques ; l'ordre des champs JSON affichés dans Markdown/HTML peut différer après relecture. [Preuve et limite de régénération](../reports/REPLAY-BROWSER.json).

Android : le mode SAFE ne lance aucun émulateur. Une exécution distincte de la vraie sous-commande android, au même SHA propre, a compilé/vérifié M51 puis renvoyé BLOCKED/NO_AUTHORIZED_EMULATOR, sortie4, sans installation. [Reçu](../reports/ANDROID-ADMISSION.json). Le préflight positif est couvert par fixtures ; aucune réception réelle API29/35 n'est ajoutée. Physique, LLM réel, mémoire/thermique/énergie et TTFT restent NOT_RUN.

## Lancer et poursuivre

Depuis Android : ouvrir [ce run SAFE](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42638506700), choisir **Re-run all jobs**, puis récupérer l'artefact et consulter le résumé/dashboard. [Guide détaillé](GUIDE-ANDROID.md), sans Termux ni Android Studio. Le résultat peut rester rouge tant que les défauts LLM et les préconditions VOICE persistent. Ne pas les supprimer pour rendre la CI verte.

Main reste e4435f4bd60c5fdc5595c411cc8cab9da7ef020b. Son absence de workflow limite actuellement le bouton workflow_dispatch ; la relance Actions sur la branche expérimentale fonctionne sans modifier main. Une publication future du déclencheur sur la branche par défaut nécessite une décision séparée. Le dashboard statique ne déclenche pas de builds.

Prochaines actions : corriger légitimement les gardes LLM dans une mission séparée ; décider d'une qualification VOICE avec les ressources et droits nécessaires ; fournir un laboratoire Android stable puis recevoir18 baseline / 24 candidat sans modifier leurs assertions. Les intégrations CORE/LLM, les clés réelles, les modèles et les appareils personnels demeurent soumis à leurs autorisations distinctes. Aucun de ces accords n'est présumé ici.

Rollback : [ROLLBACK.md](ROLLBACK.md), abandon de la branche additive, aucun remplacement d'application ou restauration automatique de données. Aucune fusion dans main, installation personnelle, modification de protection ou activation productive.
