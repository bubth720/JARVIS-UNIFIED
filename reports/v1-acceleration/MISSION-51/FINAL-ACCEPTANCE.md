# Réception finale M51 — NON ACCEPTÉE

Livraison du code, des preuves et des PR brouillon clôturée le8novembre2026. **La qualification Android échoue ; aucune APK prête à installer n'est déclarée.** Les APK testOnly compilées restent des artefacts techniques non qualifiés. Aucune nouvelle campagne n'est lancée après le crash.

Source cockpit : `9c8960a7c9d3f572dff41fe18a5b002c9f66ac8a`, tree`39427d75257a841208e6e75e2f1755d1cb564d85`, branche`codex/m51-v1-foundation`, [INTERFACE PR18](https://github.com/bubth720/JARVIS-INTERFACE/pull/18). [CI42456346025](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456346025) : buildPASS, API29FAIL, API35FAIL. Les CI Android historiques42456349663/42456346153 sont SUCCESS ; elles ne valident pas les tests appareils M51.

| Lot M51 | Bilan exact | Preuve |
|---|---|---|
|01 audit/composition|PASS préparation, versions/licences inconnues conservées|BASELINE-LOCK/SOURCE-EVIDENCE et DELIVERIES.md|
|02 enveloppe|APK compilées, testOnly, paquets privés distincts ; AndroidFAIL|RECEPTION.json et build.json artefact13607369943|
|03 UI-01C|89 fichiers historiques identiques ; préimages/postimages vérifiées ; candidat non exécuté|9C8960A-CI-SOURCE-RECEIPT.json|
|04 registre|9 rôles,6 dimensions séparées ;15 JVM uniques dont9nouveaux PASS ; panneau Android NOT_RUN|INTERFACE18 et reçu de build|
|05 UI/performance|instrumentation et parseurs testés ; benchmark NOT_RUN ; aucun gain qualifié|UI-PERF.json, INTERFACE17|
|06 ambiance|décor historique provisoire conservé ; master officiel non fourni|composition INTERFACE18, préparation AVATAR19|
|07 autoritéLAB|audit exécuté ; avisNO_GO, patch non appliqué|LLM16 et AUTHORITY-REVIEW-RECEIPT.json|
|08 non-régression|JVM/lint/PythonPASS, qualification AndroidFAIL, suite interrompue|reçusAPI29/35 et logsbruts ci-dessous|

## Résultats appareils au même build exact

API29 :1080×1920/420 vérifiés, avion enabled/Wi-Fi0. Sur18cas baseline prévus :12 commencés,9PASS,3FAIL signalés puis processus interrompu ;6noncommencés. Le picker SAF ne sélectionne pas la fixture dans le délai, la navigation atteint un timeout, puis crash `SnapshotStateObserver` au test `projectContractStepsProgressAndHistoryAreReal`. La pile signale une observation multithread lors du draw Compose. Une interaction entre captureToImage, Compose et l'instrumentation est une **hypothèse**, pas une causalité productive prouvée. La capture finale inspectée montre un écran blanc après l'arrêt. [Archive13608212432](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456346025/artifacts/13608212432), SHA256`3f707f362ac5cde18f02f8f8af46af0e3ee18d73d693b63c219a5934beeab95e`.

API35 :1200×1920/240 vérifiés, avion enabled/Wi-Fi0. Le processus d'instrumentation renvoie `Process crashed` avant le premier cas ; aucun test réussi ou échec de cas n'est inventé. Le buffer crash collecté est vide ; la cause précise resteUNKNOWN. La capture inspectée montre le dialogue **System UI isn't responding** : ANR système observé sur cet émulateurTCG. [Archive13608192178](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456346025/artifacts/13608192178), SHA256`8c9e6e5a6cb3e8953d14dfc7a83f7cd22ca5031637afe30acdc29c7860859724`.

Le candidat n'a été ni installé ni exécuté après l'échec baseline. Ses24cas, les probes force-stop/restart, les captures du cockpit candidat et les fenêtres de frames restentNOT_RUN. Aucune comparaison de performances avant/après, aucun PSS/RSS, aucune latenceLLM ou énergie physique n'est publiée. Aucune absence de mesure n'est remplacée par zéro. Le runner ne donne pas de droitKVM ; aucune protection ni limite mémoire/batterie/thermique n'a été modifiée pour forcer un succès.

Les copies texte brutes `RAW-9C8960A-*` et les comptes `9C8960A-API*-COUNTS.json` sont conservés dans ce dossier. Les PNG sont dans les archivesCI et dans la sauvegarde workspace vérifiée, pas présentés comme des captures de cockpit validé. Les premières campagnes défaillantes6c2656d/e2a2aca/5aa2193 restent conservées et ne deviennent pasPASS.

## APK et préservation

[Archive de build13607369943](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42456346025/artifacts/13607369943), ZIP SHA256`fbc2f63a7fdefce6237d54fced3cdc6206a0be90fd13e6e22069b4cd3ef871a7`. APK candidate `fr.jarvis.v1.lab`, SHA256`d0d4ad2edc4196dc933a793d754bbf9ad475032bd62f4ed1af41c2608f764416`. Version51, min26/target35, testOnly et allowBackup=false. Certificat debug éphémère`94118d7fedc865d2a99fdcc3fb2d079bfef459f5c29c6fea56912392e1153086`. Aucune permission plateforme ; receiver signatureAndroidX conservé. Seul helpergraphiqueAndroidX sur quatreABI, alignementELF/ZIP16KstatiquePASS, Android16KNOT_RUN. Aucun JNI LLM.

JVM6historiques et15parvariante, soit15casuniques dont9nouveaux ;7Python PASS. Lint0erreur/41avertissements. Les89fichiershistoriques et modes sont inchangés. SHAducode réellement exécuté séparé du commit de réception UNIFIED ; ces ajouts de rapports ne modifient aucune APK ni aucune donnée utilisateur.

## Livraisons parallèles et décisions

NEXUS[PR13](https://github.com/bubth720/JARVIS-NEXUS/pull/13) : source`eae61fb62a9ccd4073b96d71454f89e5a943eae9`,100JVM dont8nouveaux et10PythonPASS,317fichiers préservés. CI dédiée42456624435SUCCESS ; historiqueNEX-07resteFAIL au scope. Android/SAF et raccordementNOT_RUN.

AVATAR[PR19](https://github.com/bubth720/JARVIS-INTERFACE/pull/19) : source`2397bf29526ba48ac881e67c8e07dde3e01cf489`,21JVM+20PythonPASS,89fichiers préservés. Contrôleur/inventaire seulement ; renderer/master/Android non fournis/non exécutés. Les archives et leurs empreintes sont dans PREPARATION-RECEIPTS.json.

LLM[PR16](https://github.com/bubth720/JARVIS-LLM/pull/16) : avisNO_GO, défauts de révocation/deadline/FD/attestation documentés ; aucune activation ou racine opérateur. Le garde historiqueAndroidManifest.xml resteFAIL. CORE/LLM/NEXUS/SERVICES/VOICE/AVATAR/EVOLUTION ne sont pas raccordés dans le cockpit.

**Score reçu :0/100 de la nouvelle composition**, pas0%duprojet historique ; aucune attribution par documentation/testsJVM. Les31critères et le graphiqueRECEPTION-SCORE.svg conservent ce périmètre. GatesG-A/G-ROOT/G-B/G-C/G-V1/G-MERGE non ouverts. Aucune fusion, installation personnelle, migration réelle, acquisition de modèle, dépense cloud ou modification JNI productive.

Prochaine action prioritaire : mission de diagnostic bornée du crash Compose sous instrumentation API29 et de l'ANR systèmeAPI35, sur un laboratoire réellement compatible, sans modifier les garde-fous. Ensuite seulement reprendre la réception du candidat et les benchmarks. Les corrections d'autoritéLLM doivent rester un diff séparé soumis à validation exacte ; le patch actuel ne doit pas être approuvé en l'état. Le rollback demeure l'abandon des branches additives, sans toucher aux applications ou données historiques.
