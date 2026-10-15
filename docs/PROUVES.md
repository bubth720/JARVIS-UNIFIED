# Preuves et limites — Phase A

Le registre [proofs.json](../registry/proofs.json) sépare type, statut, SHA, branche,
date du commit si connue et date de consultation. Le type source signifie **lu**,
pas exécuté. CI et matériel ne sont pas des degrés interchangeables de réussite.
La lecture des tests identifie ce qu’ils couvrent ; seuls les tests listés dans
COMPTE_RENDU_CENTRAL ont été effectivement lancés pendant cette consolidation.

| ID | Type / statut | SHA concerné | Source GitHub immuable | Constat limité |
|---|---|---|---|---|
| source-core-1 | source / confirmed_by_reading | `226e2e8cc3eebd479805b89d035eb5c1cbcad540` | [app/src/main/java/com/stark/jarvislocal/AppGraph.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/226e2e8cc3eebd479805b89d035eb5c1cbcad540/app/src/main/java/com/stark/jarvislocal/AppGraph.kt) | Composition locale : le noyau instancie son propre LlamaLocalEngine, SQLite, RAG, Whisper et TTS. |
| source-core-2 | source / confirmed_by_reading | `226e2e8cc3eebd479805b89d035eb5c1cbcad540` | [app/src/main/java/com/stark/jarvislocal/JarvisCore.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/226e2e8cc3eebd479805b89d035eb5c1cbcad540/app/src/main/java/com/stark/jarvislocal/JarvisCore.kt) | Routage commandes, preuve documentaire, souvenirs et génération par le wrapper local. |
| source-llm-1 | source / confirmed_by_reading | `1756e29557287550b5cfdffdd911cada2a302db6` | [domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt) | LanguageModel est une interface intraprojet, pas un service IPC. |
| source-llm-2 | source / confirmed_by_reading | `1756e29557287550b5cfdffdd911cada2a302db6` | [app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt) | JNI llama.cpp, arrêt natif, worker unique et déchargement ; pas de client CORE. |
| source-llm-3 | source / confirmed_by_reading | `1756e29557287550b5cfdffdd911cada2a302db6` | [domain/src/main/kotlin/fr/jarvis/domain/resources/ResourceCoordinator.kt](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/domain/src/main/kotlin/fr/jarvis/domain/resources/ResourceCoordinator.kt) | Baux lourd/résidence coopératifs dans ce processus seulement. |
| source-voice-1 | source / confirmed_by_reading | `56ffebc5b514d683f977ea177a26e2b6a91b4930` | [expressionRuntime/src/main/kotlin/com/jarvis/voice/expression/ExpressionContract.kt](https://github.com/bubth720/JARVIS-VOICE/blob/56ffebc5b514d683f977ea177a26e2b6a91b4930/expressionRuntime/src/main/kotlin/com/jarvis/voice/expression/ExpressionContract.kt) | CoreVoiceRequestV1 parse un DTO utilisé dans l’application VOICE ; pas de liaison depuis CORE. |
| source-voice-2 | source / confirmed_by_reading | `56ffebc5b514d683f977ea177a26e2b6a91b4930` | [voiceExpression/src/main/AndroidManifest.xml](https://github.com/bubth720/JARVIS-VOICE/blob/56ffebc5b514d683f977ea177a26e2b6a91b4930/voiceExpression/src/main/AndroidManifest.xml) | Activité de lancement ; pas de service IPC ou de permission réseau/micro dans ce manifeste. |
| source-interface-1 | source / confirmed_by_reading | `d1c0931c4507e9af8f1aa60951947c23f4394b56` | [app/src/main/java/com/jarvis/interfaceapp/avatar/AvatarContract.kt](https://github.com/bubth720/JARVIS-INTERFACE/blob/d1c0931c4507e9af8f1aa60951947c23f4394b56/app/src/main/java/com/jarvis/interfaceapp/avatar/AvatarContract.kt) | AvatarSession est un contrat préliminaire sans moteur de rendu. |
| source-interface-2 | source / confirmed_by_reading | `d1c0931c4507e9af8f1aa60951947c23f4394b56` | [app/src/main/java/com/jarvis/interfaceapp/ui/HomeViewModel.kt](https://github.com/bubth720/JARVIS-INTERFACE/blob/d1c0931c4507e9af8f1aa60951947c23f4394b56/app/src/main/java/com/jarvis/interfaceapp/ui/HomeViewModel.kt) | Réduction locale de l’état UI ; pas de connexion CORE. |
| source-nexus-1 | source / confirmed_by_reading | `b27df0b84d8f0082d17ca6278549298aaaf97926` | [README.md](https://github.com/bubth720/JARVIS-NEXUS/blob/b27df0b84d8f0082d17ca6278549298aaaf97926/README.md) | Dépôt README seul, aucun moteur documentaire implémenté à cette ref. |
| source-services-1 | source / confirmed_by_reading | `c9f94ad2fa219a5e09cda92fb451aca606ee1646` | [README.md](https://github.com/bubth720/JARVIS-SERVICES/blob/c9f94ad2fa219a5e09cda92fb451aca606ee1646/README.md) | Dépôt README seul, aucun outil runtime implémenté à cette ref. |
| source-evolution-candidate-1 | source / confirmed_by_reading | `a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0` | [README.md](https://github.com/bubth720/JARVIS-VOLUTION-/blob/a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0/README.md) | Nom exact VOLUTION-, README seul ; identité EVOLUTION non démontrée. |
| source-interface-placeholder-1 | source / confirmed_by_reading | `a857f5019354ea1c912e6f66bebdcc053c0cb700` | [README.md](https://github.com/bubth720/JARVIS-INTERFACE-/blob/a857f5019354ea1c912e6f66bebdcc053c0cb700/README.md) | Dépôt distinct et README seul ; aucune équivalence de code avec INTERFACE. |
| source-unified-1 | source / confirmed_by_reading | `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b` | [README.md](https://github.com/bubth720/JARVIS-UNIFIED/blob/e4435f4bd60c5fdc5595c411cc8cab9da7ef020b/README.md) | main distant initial, distinct des travaux locaux préservés. |
| reported-core | documentation / historical_report_not_reexecuted | `226e2e8cc3eebd479805b89d035eb5c1cbcad540` | [core](https://github.com/bubth720/JAVIS-Local-v2/blob/226e2e8cc3eebd479805b89d035eb5c1cbcad540/docs/PROJECT_KNOWLEDGE.md) | Rapport historique : 33 cas SQLite et 7 tests heure ; aucune nouvelle exécution Android ici. |
| reported-llm | documentation / historical_report_not_reexecuted | `e9d408e77319f4998821e723ef8bc0c872ee3274` | [llm](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/docs/VALIDATION_003B.md) | Rapport historique 55 domaine +16 Robolectric +1 natif ; API CI actuelle inaccessible. |
| reported-voice | documentation / historical_report_not_reexecuted | `532c6580835525b8879e012bde56fae8159fbe55` | [voice](https://github.com/bubth720/JARVIS-VOICE/blob/56ffebc5b514d683f977ea177a26e2b6a91b4930/docs/mission005i/CI-RESULTATS.json) | Rapport historique 005I : 11/12 expression,18/19 identité,33/46 pocket en CI ;31 tests instrumentés I ; échec D4/5 conservé. |
| reported-interface | documentation / historical_report_not_reexecuted | `d1c0931c4507e9af8f1aa60951947c23f4394b56` | [interface](https://github.com/bubth720/JARVIS-INTERFACE/blob/d1c0931c4507e9af8f1aa60951947c23f4394b56/docs/mission-002.md) | Rapport local historique :3 JVM, AndroidTest compilés mais non exécutés, CI distante non attestée. |

## Accès et reproductibilité

Les neuf clones nus ont été acquis en HTTPS dans `.audit-cache/` (ignoré par Git),
sans checkout ni modification de source. `scripts/capture_sources.py` lit leurs
arbres, manifestes/Gradle, interfaces, workflows et graph d’ascendance. Les hits
IPC par motif ne suffisent pas à prouver absence/présence : ils ont été confrontés
aux manifestes, points d’entrée, dépendances Gradle et appelants inspectés.
Pour répéter : cloner en lecture chaque dépôt sous `.audit-cache/NOM.git`, puis
lancer la capture documentée dans RUNBOOK. Un cache existant est un instantané,
pas une nouvelle lecture live ; ne pas rafraîchir la date d’une preuve historique
pour prétendre qu’elle est récente.

LLM e9d408e→1756e29 : diff limité à trois documents, code correspondant au rapport
historique inchangé. VOICE code testé532c658→56ffebc : diff vide sur kt/kts/xml,
les ajouts de livraison/docs ne deviennent pas une nouvelle campagne CI.
Source VOICE005I rapporte11 expression/18 identité/33 pocket réussis en CI, avec
respectivement1/1/13 ignorés ;31 instrumentés I,18 H,14 G,10 F. 005D reste4/5
avec échec AudioTrack. Aucun nombre ignoré n’est compté comme réussite.
Ces chiffres restent des **rapports versionnés**, pas des observations directes
Actions de cette session. Le retour humain 005G mentionné dans VOICE est une
déclaration de propriétaire, pas une mesure matérielle de cette consolidation.

[reports/online](../reports/online/SUMMARY.md) enregistre les neuf refus de tunnel
proxy403, sans token ni header. API PR/Actions et exécution de la nouvelle CI
UNIFIED inaccessibles. Les deux sondes de noms retournent erreur Git128 sans
prouver absence des dépôts. [reports/offline](../reports/offline/SUMMARY.md) est
**synthétique**, jamais utilisable comme état réel des neuf dépôts.

Publication antérieure f7b7a5a refusée403 par routeHTTPS, aucune PR créée. Cette
consolidation ne contourne pas les politiques réseau ni l’authentification et ne
prétend pas que les permissions ont changé. Les bundles/patchs locaux sont des
livrables, pas une écriture GitHub.
