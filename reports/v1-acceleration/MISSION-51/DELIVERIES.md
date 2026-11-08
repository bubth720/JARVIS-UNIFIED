> **Réception finale : NON ACCEPTÉE — qualification Android FAIL.** Voir [bilan final](FINAL-ACCEPTANCE.md). Les états de préparation historiques ci-dessous conservent leur date.

# Réception coordonnée M51 — sources et niveaux de preuve

État observé le 8 novembre 2026. Chaque référence ci-dessous désigne sa propre branche ; les branches historiques et main restent intactes. Une mise à jour documentaire de ce dossier ne recompile pas les APK ni ne remplace le SHA effectivement exécuté.

| Lot / dépôt | PR brouillon et branche | Commit / tree exécutés | Résultat et limite |
|---|---|---|---|
| M51.01 UNIFIED | [PR21](https://github.com/bubth720/JARVIS-UNIFIED/pull/21), codex/m51-unified-gates | 3420a4e0a099bad7e79f2ac5fb1218cb522d6994 / 7f4dbde3633d29776ee8c9cdfa453fc46307a1c4 | CI 42418494306 SUCCESS ; 349 fichiers historiques figés ; coordination uniquement |
| M51.02–06/08 INTERFACE | [PR18](https://github.com/bubth720/JARVIS-INTERFACE/pull/18), codex/m51-v1-foundation | 9c8960a7c9d3f572dff41fe18a5b002c9f66ac8a / 39427d75257a841208e6e75e2f1755d1cb564d85 | Job build 128656069523 SUCCESS ; APK vérifiées ; réception Android séparée ci-dessous |
| M51.05 instrumentation de référence | [INTERFACE PR17](https://github.com/bubth720/JARVIS-INTERFACE/pull/17), codex/m51-ui-performance-review | a7ced2e97a010aadb5827986ea90ec0ed1907aa0 / bbe57020af44fa4e7c73ec6f644478da32afbb90 | CI 42421922587 SUCCESS ; 19 tests de parseur/comparaison ; aucun gain Android déduit de ces tests |
| M51.07 revue indépendante LAB_CLOUD | [LLM PR16](https://github.com/bubth720/JARVIS-LLM/pull/16), codex/m51-lab-cloud-audit | 08fbda527d187f324d94e0adafbca76fa955a343 / 053a59b808396314943b21bb5005887076a2e08e | CI 42387659515 SUCCESS ; 247 cas existants + 12 reproductions adversariales ; **NO_GO de sécurité**, génération NOT_RUN |
| Préparation M53 / NEXUS | [PR13](https://github.com/bubth720/JARVIS-NEXUS/pull/13), codex/m53-readonly-preparation | eae61fb62a9ccd4073b96d71454f89e5a943eae9 / 1f5d78b084946e162617ac0525b32658cea80e15 | [CI dédiée 42456624435](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42456624435) SUCCESS ; 100 JVM (92 historiques +8 nouveaux), 10 Python SQLite PASS ; 317 fichiers historiques préservés ; Android NOT_RUN |
| Préparation M54 / AVATAR | [INTERFACE PR19](https://github.com/bubth720/JARVIS-INTERFACE/pull/19), codex/m54-avatar-preparation | 2397bf29526ba48ac881e67c8e07dde3e01cf489 / 85286f4d763c53e77e56dc1291cacc62ef530446 | [CI dédiée 42456453636](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456453636) SUCCESS ; 21 JVM +20 Python CI PASS ; 89 fichiers historiques préservés ; aucun renderer/asset officiel/Android activé |

Les PR préparatoires M53/M54 restent distinctes de l'APK M51. Elles ne donnent aucun point Android, artistique ou de génération. [Reçus complets et empreintes](PREPARATION-RECEIPTS.json) : archives téléchargées, commit/tree et empreintes internes vérifiés par la réception du parent.

## Première campagne conservée — APK 6c2656d

L'[artefact 13607270918](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42454245088/artifacts/13607270918) provient du build 6c2656d… ; ZIP SHA256 `a7999eb8c762e8f294adfbb625af4d58b7c354c91d1aad7393d228b250f22f30`, rétention jusqu'au 6 février 2027. Archive téléchargée et contenu/SHA256SUMS vérifiés avant réception.

| Variante | Paquet | SHA256 APK |
|---|---|---|
| Candidate | fr.jarvis.v1.lab | 7ee19087d92844468f493bbb211c401f3f16271a6f39c712cd3fee98e65a8d40 |
| Baseline comparable | fr.jarvis.v1.lab.baseline | fe28c2d4463d23d6c40f52ae2811040ce17243f2371df95e35f43bd0f825f23b |

Version 0.51.0-m51-lab/code 51, minSDK 26 / target 35, testOnly=true, allowBackup=false. Certificat debug SHA256 `5dbb8d81ff9d209271956244a82f5231f6cd9849b8899064be996ff84c957401`. Aucune permission de plateforme Android ; la permission signature AndroidX de receiver non exporté reste présente. Les quatre ABI ne contiennent que le helper AndroidX `libandroidx.graphics.path.so`, identique entre variantes. Ce helper graphique n'est pas du JNI LLM ; Android 16 Kio reste NOT_RUN.

6 cas JVM historiques, 15 pour chaque variante du laboratoire (15 cas uniques dont 9 nouveaux), 3 tests Python et lint candidat PASS. Ne pas additionner les replays comme de nouveaux cas. Les 89 fichiers UI-01C restent identiques. Workflows historiques Android [42454245075](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42454245075) et [42454354298](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42454354298) SUCCESS au même SHA.

## Réception Android et métriques

Première campagne 6c2656d… : API 29 et API 35 ont démarré en émulation logicielle TCG, sans modifier les droits KVM. Le banc a ensuite échoué avant installation des APK : Android a refusé le broadcast protégé AIRPLANE_MODE. Fonctionnel et benchmark restent NOT_RUN. Les échecs sont conservés dans les artefacts API 29 id 13606589799 (ZIP SHA256 `cac2cab9168ae853642bb16914423376eb64a06fbd41d3ea0d8ae0714c418ce8`) et API 35 id 13606958735 (ZIP SHA256 `52eae5c05a414b93ddcdaf008f9b4c87b66b487673376ccfa0344080bdcf5840`). Le correctif du banc doit utiliser la commande Android officielle de connectivité, puis produire un nouveau commit et une campagne distincte ; ce résultat échoué ne devient pas PASS. Un job lancé ne vaut pas exécution réussie. Les essais x86_64 sur émulateur UI ne sont ni une qualification LLM ARM64 ni une performance POCO/Redmi. La génération LLM et le TTFT CORE–INTERFACE restent NOT_RUN ; aucune mesure absente n'est remplacée par zéro.

## Décisions conservées

M52/G-A/G-ROOT/G-B : bloqués. Le patch LAB 8df826… reste non appliqué. Les douze tests adversariaux reproduisent notamment les risques de notification, deadline, handle de fichier et attestation de chargement ; leur succès ne valide pas le patch. Le prochain lot sensible doit proposer un diff distinct et demander validation exacte après correction et nouveaux tests.

Aucun téléchargement de modèle, provisionnement de clé, installation personnelle, migration réelle, achat cloud ou fusion ne découle de cette réception. NEXUS/SERVICES/VOICE/AVATAR/EVOLUTION restent non raccordés au cockpit. Les assets artistiques officiels et la réception humaine restent absents.

## Nouvelle campagne après correctif borné du banc

Commit INTERFACE `e2a2aca68465eff05a4e01781047d297b582f841`, tree `ca5902838c758cb41338cea50adb656298828f2c`. Le correctif emploie la commande Android officielle de connectivité au lieu du broadcast protégé ; la politique configChanges historique est conservée et les tests de recréation explicite restent présents. Aucun droitKVM ni garde Android n'est abaissé.

Build [42455129665/job128652400436](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42455129665/job/128652400436) SUCCESS. [Artefact 13607218676](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42455129665/artifacts/13607218676), ZIP SHA256 `b121aafbe497bc9f0910acea8a576b67de0718ea6ab18c2375dbe7980f798dea`, empreintes internes vérifiées ; rétention jusqu'au 6 février 2027.

- APK candidate : `257bfc0e3d2cbf5beddca70961fa73dacd1fce3a1eddc7dfb4f811cda5df13b2`.
- TestAPK candidate : `1052897488380238fbcf76e5bed82fb5d3fe17b570764a10f23ab5ac08647ba1`.
- APK baseline : `50855675df3d4c2bb776564cfd5d8ba85e4762a81423cc15050f7a3134ec78a9`.
- TestAPK baseline : `cc740d8fa83a2f88bea5c746a4bac2126e7b49acb702478c549ca8c5b9e142d1`.

Certificat debug éphémère partagé des deux variantes de cette campagne : SHA256 `a0e97dadfc8edbe42195f1a60659095b9cd8be71c80527178673ffa6da277e5b`. Il diffère du premier runner : aucune compatibilité de mise à jour entre ces APK de laboratoire n'est promise et aucun certificat historique n'est changé. Aucun remplacement forcé d'une installation existante. Les paquets/testOnly/permissions et la portée graphique AndroidX restent identiques ; les deux APK/testAPK sont transmis aux jobs Android sans recompilation ni nouvelle signature.

La commande officielle de mode avion a fonctionné sur API 35. Le banc e2a2aca… a ensuite échoué avant installation des APK : `svc data disable` présumait la présence du service téléphonie absent de l'image tablette (`Can't find service: phone`). L'[artefact 13607621939](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42455129665/artifacts/13607621939), ZIP SHA256 `6eee1b15e250a324dde8d332b522cdf8a5c6b5fc3fccd902c41942830aed1e6f`, conserve cet échec ; fonctionnel et benchmark API 35 restent NOT_RUN. Le correctif suivant retire cette commande redondante après le mode avion officiel, vérifie l'état avion et le Wi-Fi coupé, et relève les capacités téléphonie réelles. Aucun garde ou test applicatif n'est supprimé pour masquer l'erreur. La campagne corrigée doit utiliser son propre commit et ses propres APK. API 29 de e2a2aca… a exécuté18testsbaseline :7PASS/11FAIL en262,957s. Le candidat, les probes et les benchmarks restentNOT_RUN. Le device.json relève une taille physique320×640 et un override effectif640×1280 à420dpi, alors que1080×1920était demandé : Android a borné le changement au double du petit AVD par défaut. Le contexte géométrique est non comparable ; les11échecs sont conservés sans les qualifier automatiquement de11régressions applicatives ni de fauxPASS. [Artefact13607632149](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42455129665/artifacts/13607632149), ZIP SHA256`e895231944769138c88a5a64fe822cb8ce3ee5f5c08f7ff26c5799576eca326c`. Les échecs de 6c2656d restent également visibles.

## Préimages et vérifications locales reproductibles

Le build CI conserve preservation.json, mais n'a pas archivé le reçu généré source-receipt.json. Cette omission est déclarée : le [reçu reproduit localement](E2A2ACA-LOCAL-SOURCE-RECEIPT.json) provient de l'exécution déterministe du générateur exact épinglé au commit e2a2aca… dans un checkout propre, avec 15 préimages Kotlin comparées au Git UI-01C. **Ce fichier n'est pas présenté comme une entrée de l'artefact CI.** Le reçu contient sa provenance et sa commande ; ses empreintes sont également dans RECEPTION.json.

CockpitScreen baseline SHA256 `af808e9ef251abb90bf262d7c43218ab820dfc1740de45e4b903b1205ca25e39` ; sortie candidate SHA256 `c7c4386ef6100842c9ff0606030ff8dc3a5403e521baca7b336248e08076056a`. Les 14 autres sources Kotlin sont copiées octet pour octet ; les 89 fichiers historiques de la base restent préservés. Les différences candidates sont un overlay de laboratoire régénérable, pas une réécriture du code historique.

La [vérification native statique locale](E2A2ACA-NATIVE-STATIC.json) des APK exactes e2a2aca… est PASS pour zipalign 16 Kio et alignements ELF des quatre ABI du seul helper AndroidX graphique ; outils SDK build-tools 35.0.0 zipalign et GNU readelf. Ces contrôles locaux sur les APK CI ne sont ni des tests JNI du LLM ni une exécution Android 16 Kio, qui reste NOT_RUN.

## Correctif de géométrie et campagne suivante

Le commit sourceINTERFACE`9c8960a7c9d3f572dff41fe18a5b002c9f66ac8a`, tree`39427d75257a841208e6e75e2f1755d1cb564d85`, choisit explicitement le profilAVDpixel_2 et vérifie taille/densité effectives avant toute installation. Quatre nouveaux tests de clamping complètent les trois tests du parseur de frames. Il conserve aussi le reçu générésource-receipt dans les prochains artefactsCI. La campagne intermédiaire5aa219… avait commencé avant réception du diagnosticAPI29final ; elle conserve ses propres résultats, sans être présentée comme comparable. Aucun nouveauPASS ou APK9c8960… n'est présumé avant lecture des artefacts effectifs.

## Archives des préparatifs M53/M54

NEXUS : [artefact13607547887](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42456624435/artifacts/13607547887),19fichiers texte, ZIP SHA256`476d3ab192b50f9997c9288934bf25e2731432475a16c65c898a52ad97df26c9`, rétention jusqu'au8décembre2026. Le premier workflow42456495284 au commit7b0591a… a échoué avant tout job : référence runner.temp dans l'environnementjob invalide, remplacée par un répertoirebuild dans le workflow dédié. Les échecs historiquesNEX-07 [42456627732](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42456627732) et [42456497929](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42456497929) restentFAIL : garde de portée non approuvée conservé. Le vert dédié ne les efface pas. Aucun corpus privé, modèle ou appelLLM, aucun portAndroid raccordé.

AVATAR : [artefact13608031391](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456453636/artifacts/13608031391),6fichiers texte, ZIP SHA256`8196e1c715aac1be9eef134a264e8b215c56e57cc6eb4944b2845f6c2b620c7f`, rétention jusqu'au6février2027. Les workflowsAndroid historiques42456453605/42456455914 sontSUCCESS au mêmeSHA. Le contrôleur et l'inventaire utilisent seulement des fixtures anonymes ; aucun renderer, master approuvé, asset privé, PCM réel ou visème qualifié n'est activé. Cette CI ne vaut ni qualificationGPU/Android ni réception artistique.

## Build9c8960a reçu — Android en cours

[Build42456346025/job128656069523](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456346025/job/128656069523) SUCCESS. [Artefact13607369943](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456346025/artifacts/13607369943), ZIP SHA256`fbc2f63a7fdefce6237d54fced3cdc6206a0be90fd13e6e22069b4cd3ef871a7`, rétention jusqu'au6février2027. Reçu source désormais inclus dans leCI et copié [sans modification](9C8960A-CI-SOURCE-RECEIPT.json),15Kotlin et mêmes pré/postimages. Les vérifications internesSHA et source/tree sont PASS ; ce reçuCI est distinct de la reproductionlocale6c/e2 décrite ci-dessus.

| Binaire | SHA256 |
|---|---|
| APK candidate | d0d4ad2edc4196dc933a793d754bbf9ad475032bd62f4ed1af41c2608f764416 |
| TestAPK candidate | d0a427635ff972d760db86c12e92e8b41635df626c766ce5c7e7180c3229a530 |
| APK baseline | f3088de5cd424a89c2c002eb31ce32d2aee20cbc5e63df2b502d37070fe9404f |
| TestAPK baseline | 7e2beb6ec4cd1863327d3923b51f938c7e599f1798d798cf4c9b20ff266068d7 |

Certificatdebug commun à cette campagne : SHA256`94118d7fedc865d2a99fdcc3fb2d079bfef459f5c29c6fea56912392e1153086`. Chaque campagne utilise sesAPK exactes pour les deuxAPI ; aucune mise à jour d'un ancien paquet n'est forcée. Résultats build :6JVMhistoriques/15JVMbaseline/15JVMcandidat,7testsPython (3parseurframes+4géométrie) et lintPASS. Les replays ne sont pas additionnés. CIAndroid historiques42456349663/42456346153 égalementSUCCESS.

[Contrôles locaux sur les APK exactes](9C8960A-NATIVE-STATIC.json) : alignementZIP/ELF16Kio PASS des quatre ABIAndroidX ; exécutionAndroid16KioNOT_RUN, aucun JNI LLM. Les jobsAPI29/35 restent en attente de réception définitive. Aucun score ne découle de ce seul build.
