# FUSION-02 U0 — CORE et LLM, audit en lecture seule

Date : 25 octobre 2026 UTC. Aucun build/test externe exécuté, aucune source ou branche modifiée. Les deux sous-issues CORE#17 et LLM#4 et la mission mère UNIFIED#5 sont lues intégralement. Sources et 35 empreintes dans `fusion02-core-llm-audit.json` ; map locale séparée sous `/tmp`.

## Références et preuves Git

- CORE `feat/fusion-01-core-integration` : `36761cea101b5f88b87cd4136dc075d28a1adb96`, parent `0d41e6f3f412386371a81fe0d1a862fc87ae22cf` puis base CORE03 `aea5ac859ac551d54fe16187c1883a487dbee9d6`. Ref distante exacte. Aucun diff `app/` ou `fixtures/` depuis CORE03 ; MEM02/ID02 et contrats conservés.
- LLM `feat/fusion-01-llm-integration` : `e0b781442b21034a251f6af450396faabc5f667d`, parent de code `378a1cf4c2ceaaf531ded60670dc9161dc269575`, base `2efb3f7aa6205062ab71f570212019fd1d9885b6`. Ref distante exacte. Diff HEAD/code = documents et preuves sous `docs/fusion-01/` seulement ; ne pas transformer ceci en CI du HEAD documentaire.
- CORE consomme toujours NEXUS `777e6afa75ecb99b85e52d68837cb0fefcf161cd` et SERVICES `3decdc47d82f9b43713c48cab244762941770a81`, pas les ports Android. `CORE03-SOURCES.json` fixe arbres et SHA-256 ; `integration-lab/build.gradle.kts` dépend encore `nexus-core`, `shared-runtime`, `desktop`.

## CI réellement observée aujourd'hui

- CORE première [40215415459](https://github.com/bubth720/JAVIS-Local-v2/actions/runs/40215415459) **FAILURE** sur `0d41e6f…` : `android-actions/setup-android@v3` échoue puis upload-artifact échoue faute de sorties. Message interne non accessible ; aucune cause inventée. Le rapport du dépôt conserve l'échec et indique que les logs Azure sont refusés par le proxy.
- CORE reprise [40215604539](https://github.com/bubth720/JAVIS-Local-v2/actions/runs/40215604539) **SUCCESS sur SHA exact `36761cea…`**. Le job121235951011 réussit les snapshots/verrou, vrai labo JVM, setup SDK épinglé, suites historiques 501+36/builds/Lint et comparaison des cas, puis upload. Pas d'instrumentation Android dans ce workflow.
- LLM [40214822563](https://github.com/bubth720/JARVIS-LLM/actions/runs/40214822563) **SUCCESS sur code `378a1cf…`**, pas le HEAD documentaire. Le job121233565167 réussit freeze, setup, tests natifs historiques sans modèle, JVM/simulations/buildARM64/Lint, vérifications APK, collecte et upload. Ni GGUF réel ni instrumentation/physique.
- Ces conclusions sont extraites des pages publiques et attributs `check-step` nom/conclusion/SHA/log-path. Les archives/logs complets ne sont pas téléchargés indépendamment. Elles ne sont pas des exécutions locales nouvelles.

## Résultats historiques relus, non rejoués

CORE annonce567cas distincts (448debug+53mvp2+36fixtureP2+30laboratoire), 0échec/saut. Les dix anciens cas JVM sont inclus dans30, pas ajoutés. Builds debug/mvp2/mvp3, Lint0erreur/27et37warnings, APK min24ARM64 sans réseau. Le défaut d'origine CANCELLED_RESULT_ACCEPTED a une preuve rouge conservée, puis sticky-cancel et confirm grant périmé sont corrigés. Nouveau workflow : vrai TXT/NEXUS/citations, CSV exact0.10+0.20=0.30 et exportCSV/DOCX après consentement synthétique relu. Cela reste in-process JVM horsAPK.

LLM annonce285tests (127domain+40app+118fixture), 0échec/saut ; ancien CTest native_safety sansGGUF distinct de toute preuve F3B. Aucun de ces comptes n'est à ajouter aux suites fraîches UNIFIED de cette mission.

## Contrats / risques pour U4 et le BOM v2

CORE `WorkflowReceipts` est `core.workflow-receipt/1`, dans **le Store SERVICES existant**, namespace `core_workflow_receipts`, quota256. Champs `schema/session/request/generation/state` ; génération sérialisée chaîne, UUIDs corrélés. États **PREPARED, DISPATCHED, COMPLETED, REFUSED, UNKNOWN**. Reprise PREPARED/DISPATCHED→UNKNOWN après arrêt ancien propriétaire ; pas de retry/reset, corruption refuse. `COMPLETED` est l'acceptation d'un résultat après await et revalidation des droits, **pas une preuve de commit linéarisé / hash de destination / relecture SAF**. Le nouveau contrat U4 doit rester versionné et soumis à revue ; pas de renommage silencieux COMPLETED→COMMITTED.

Le workflow revalide HostAccessPort avant dispatch et après résultat, et le grant `confirm`. Cependant le worker SERVICES possède un snapshot Guard.Context : **race révocation/effet non résolue**. Une écriture déjà admise peut finir même si CORE refuse son résultat tardif ; aucun rollback/suppression promis. Il faut une fence `authorizeAtCommit` propriétaire avec génération et confirmation exacte à usage unique liée aussi à destination/digest. Avant le point d'engagement : révocation interdit tout effet ; après : résultat peut aboutir honnêtement, ACK perdu/crash→UNKNOWN sans retry automatique. Conserver cette distinction, ne pas réclamer une révocation rétroactive impossible.

LLM `jarvis.llm.client/1` est local/passif, transportNONE ; requête P2/version/profile/priority/target, référence7UUID+generation+SHA256 de framing complet. Ce hash **n'authentifie pas** l'appelant. Événements Ack/StreamChunk/Completed/Error d'origine FIXTURE ou UNAVAILABLE ; en live seul ErrorUNAVAILABLE est accepté. Limites4096octets/chunk,65536total,258événements,seq0..257. Le monitor a WAITING/STREAMING/CONTENT_DONE/STOP_REQUESTED/REFUSED/UNKNOWN et timeout/retour horloge inconnu bloque. Aucune bool native de succès : TokenCountStatusUNSUPPORTED, termination/unloadUNATTESTED, mayAdmitAnotherEngine=false. Catalogue sélectionné ne signifie pas running, fileRevalidatedNow=false. Core004BMapping.textOnly refuse encore documents/contexte nonvide.

## Versions et portes

CORE min24/compile35/ARM64, Kotlin2.0.21/AGP8.7.3/Gradle8.10.2/JDK17. SchémaSQLitehistorique2, mémoireconfirmée1, inchangés. LLM appmin29/compile36/ARM64, Kotlin2.1.21/AGP8.10.1/Gradle8.11.1/JDK21, NDK28.1/CMake3.22 ; domainbytecode17. CatalogueLLMschéma1 inchangé. Aucun LICENSE projet racine : UNKNOWN, dépendances notées séparément, pas de droit de distribution déduit.

Pilote CORE/NEXUS/SERVICES peut progresser **indépendamment** de LLM/VOICE, mais pas sans producteurs qualifiés API24/25 et fence. Native LLM reste bloqué ; aucun portinprocess29 dansCORE24/25/26. LinuxminiPC backend LLM NOT_IMPLEMENTED, matérielNOT_TESTED. La CI CORE verte ne remplace ni FTS5/SAF ni modeavion/rotation/processkill sur émulateur.
