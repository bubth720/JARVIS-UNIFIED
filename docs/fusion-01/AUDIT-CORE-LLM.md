# FUSION-01 F0 — CORE / LLM, audit en lecture seule

Date UTC : 2026-10-25. Aucun fichier de dépôt modifié, aucun build/test relancé.
Les SHA sont confirmés par `git ls-remote`; la filiation par les objets Git locaux.

## Sources immuables et graphes

| Module | Branche | SHA | Git checkout consulté |
|---|---|---|---|
| CORE retenu | feat/core-03-intensive | aea5ac859ac551d54fe16187c1883a487dbee9d6 | /workspace/JAVIS-Local-v2 |
| MEMORY inclus | feat/mem-02-intensive | 49ad428e94edd75c2a1d115c8c2504f26609eace | même |
| IDENTITY inclus | feat/id-02-intensive | 283423cb8b9d567539f33cf7f2f1fafa602cf974 | même |
| CORE-VOICE distinct | feat/core-voice-pilot | 7426665f2794cba83646008fa0f342d102141201 | même |
| LLM retenu | feat/llm-03-runtime | 2efb3f7aa6205062ab71f570212019fd1d9885b6 | /workspace/JARVIS-LLM |
| LLM-02 inclus | feat/llm-02-runtime | 895a067ffc860d56a2dbb1ce22cb274096f8e3a2 | même |
| F3B revue incluse | design/003f-f3b-worker-connection | 8f1c2f5a936d6c01874d7be6bb987f4459b83374 | même |

CORE03 → MEM02 → ID02fix sont des parents directs. CORE02 e86107b8213b0aeaf9d22025cf6bef91a8e544a5 est ancêtre.
CORE-VOICE diverge de CORE03 depuis main226e2e8cc3eebd479805b89d035eb5c1cbcad540 : 35commits côtéCORE03 contre4côtéVOICE. Vingt chemins modifiés côtéVOICE, dont AppGraph.kt et MainActivity.kt. Aucun cherry-pick ou merge ne peut être présumé sûr.
LLM03 → LLM02 est parent direct ; F3B est ancêtre. Le patch sensible F3B demeure non appliqué.

## Compatibilité / BOM

CORE app : min24/compile35/target35, ARM64, JDK17, Kotlin2.0.21, AGP8.7.3, Gradle8.10.2.
LLM app : min29/compile36/target36, ARM64, JDK21, Kotlin2.1.21, AGP8.10.1, Gradle8.11.1, NDK28.1.13356709, CMake3.22.1. Le domain LLM cible le bytecodeJVM17 ; ce n'est pas l'APK ni le worker.
Lier l'application LLM en processus CORE24/25/26 est incompatible. Le transport IPC n'est pas activé.

CORE03-SOURCES.json verrouille exactement NEXUS777e6afa75ecb99b85e52d68837cb0fefcf161cd et SERVICES3decdc47d82f9b43713c48cab244762941770a81. Le vrai integration-lab repose sur ces versions : remplacer par NEX06A/SERV04A requiert un portage explicite et la révision contrôlée de la provenance. En particulier, NexusDatabase/JDBC est déplacé vers nexus-jvm-store dansNEX06A, tandis que le client CORE03 déclare seulement nexus-core.

## Code et preuves

CORE : app/build.gradle.kts, settings.gradle.kts, integration-lab/build.gradle.kts ; integration-lab/src/main/kotlin/com/stark/jarvislocal/integrations/{NexusSearchAdapter,ServicesToolAdapter,CoreIntegrationLab}.kt ; app/src/main/java/com/stark/jarvislocal/{InferenceContract,LlamaLocalEngine,ProcessInferenceAdmission,SessionCoordinator}.kt.
Rapports : docs/intensive-2026-10-22/{REPORT-CORE-03.md,VALIDATION-CORE-03.json,CORE03-SOURCES.json,VALIDATION-ID-02.json,VALIDATION-MEM-02.json}.
CORE03 rapporte10tests JVM réels sur NEXUS/FTS5/citations/CSV/DOCX. MEM02 rapporte501tests (448debug+53mvp2), ID02fix406incluantles400anciens. Cescomptes se recouvrent : nepaslesadditionner. Aucun de ces tests fraîchementexécuté durantcet audit.

LLM : app/build.gradle.kts, domain/build.gradle.kts, docs/THIRD_PARTY.md ; domain/src/main/kotlin/fr/jarvis/domain/generation/{P2Contract,P2Prompt,Core004BMapping}.kt ; prompt/ContextPlanner.kt ; runtime/RuntimePolicyProfiles.kt ; app/src/main/java/fr/jarvis/llm/runtime/ProcessRuntimeObservationPort.kt.
Rapports : docs/intensive-2026-10-22/{REPORT-LLM-02.md,REPORT-LLM-03.md,RECEIPT-LLM-02.json,RECEIPT-LLM-03.json}, docs/mission-003f-f3b/VALIDATION.md.
LLM03 rapporte254tests (100domain+36app+118fixture). LLM02 rapporte249sous-ensemble. Le CTest historique native_safety n'est pas la sonde F3B proposée.

## Contrats / risques concrets

- CORElab Correlation exige UUIDsession/request et génération>=0 ; LLM OperationKey exige7UUID et génération1..9007199254740991. Une référence UUID n'authentifie pas un appelant.
- CORElab search : question<=1024octetsUTF8, contexte256..16000octets et5items/sources ; ContextAssembler max20000octets, untrusted_data=true, confirmed_memory=null, generation_available=false.
- ToolReview :16arguments/8192octets, invocation5s, preview30s,32aperçus/128IDs. La mutation exige appel explicite du propriétaire et ApprovalGate. Ce n'est pas encore SessionCoordinator.
- LLM version jarvis.llm.p2/1.0 : SYSTEM/question8192octets,6toursmax enpaires,4documents4096octets chacun ; input65536octets, délai90000ms, contexte512..2048par256, sortie1..256tokens ; garde8tokens. Comptage exact non disponible.
- Core004BMapping.textOnly REFUSE tout contexte ou source nonvide : CONTEXT_NOT_REPRESENTABLE. Aucun mapping documentaire sans perte n'est démontré.
- UnavailableNativeTokenCountPort retourne UNSUPPORTED/TOKENIZER_UNAVAILABLE ; UnavailableNativeP2Port refuse NATIVE_P2_UNAVAILABLE. Le planificateur ne remplace pas le worker.
- RuntimeResourceProjection retourne nativeTermination/nativeUnload UNATTESTED, ycompris brokerEMPTY_UNATTESTED. Aucunreset/release/autoritésecondaire.
- CORE requestStop retourne UNSUPPORTED. Retour JNI, fin coroutine, déchargement, libération attestée restent distincts.
- Athéna reste inactive. SYSTEMpersona borné et tokenizernatifqualifié obligatoire.

## Données / licences / CI

CORE historique jarvis_local_v2.db schéma2 ; v1→v2 même schéma logique. Mémoireconfirmée confirmed_memory_lab.sqlite schéma1 ; autres migrations refusées. CatalogueLLM catalogue.db schéma1, différent de la mémoirepersonnelle.
Aucun LICENSE projet de premierniveau trouvé dans CORE ou LLM : statut licenceprojetUNKNOWN, nepasinventerMIT. LLM docs/THIRD_PARTY.md décrit llama.cppMIT@1b70350c92563449576bcbbf552994b1d1ed847d et Kotlin/AndroidX/coroutinesApache2, noticestransitivesencoreàassembler.
GitHub API check-runs : proxyCONNECT403Forbidden ; aucuncontournement. Pagesdescommits accessiblesHTTP200, aucunstatutCI fiable extrait ⇒ CIUNKNOWN. Les rapports historiques locaux ne deviennent pas succèsCIobservé.

## Gates

F1 peut repartir du laboratoire JVM épinglé ; F2 Android est bloquée parFTS5/qualification desports et absence de raccordementSessionCoordinator. F3/CORE004D demeureBLOCKED par tokeniseur/résidence nonattestés ; F5 doit conserver TTS historique et pilotesinactifs. API24/25 : CORE compatible déclaré +Robolectric historique, aucune preuvephysique. LLM24/25/26 BLOCKEDmin29. API29ARM64/mini-PC : qualificationphysiqueNOT_TESTED.

Voir `evidence/core-llm.json` pour champsstructurés et SHA256 dessources.
