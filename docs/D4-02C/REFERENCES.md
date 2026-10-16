# D4-02C — références vérifiées, filiation et preuves

Date de lecture : 2026-10-16T21:45:58+00:00.
UNIFIED base imposée **52a44fb6cf01623a8c5d96edc5d2bbac76abd9a1**, branche
`design/d4-02-ownership-mapping`, vérifiée locale et origin avant branchement.
Nouvelle branche : `audit/d4-02c-core-llm-convergence`, sans merge/rebase.
Deux clones nus HTTPS neufs dans `.audit-cache/d4-02c/`, aucun checkout/code
externe modifié ou exécuté. Métadonnées : acquisition.json, git-comparison.json,
unified-refs.txt. main UNIFIED observée e4435f4, inchangée par la mission.

## Les quatre références demandées

| Dépôt sous bubth720 | Branche | Commit demandé et tête distante observée | Choix technique proposé |
|---|---|---|---|
| JAVIS-Local-v2 | mission-004b-inference-contract | [07cd282603205d57f3d2ded1b14d5d95e68989e2](https://github.com/bubth720/JAVIS-Local-v2/tree/07cd282603205d57f3d2ded1b14d5d95e68989e2) | Comparaison historique174 tests rapportés |
| JAVIS-Local-v2 | mission-004b-core-backend-lifecycle | [29646448c80568d868a702192df761fc9d7a896d](https://github.com/bubth720/JAVIS-Local-v2/tree/29646448c80568d868a702192df761fc9d7a896d) | **Retenir** : admission commune au processus et protections de génération supplémentaires |
| JARVIS-LLM | mission-003d-core-generation-contract | [c4e7611eebb64a96a796164bc3d4c961dbc7dcba](https://github.com/bubth720/JARVIS-LLM/tree/c4e7611eebb64a96a796164bc3d4c961dbc7dcba) | Contrat/type et preuve de référence ; pas chemin P2 natif |
| JARVIS-LLM | mission-003d-p2-core-contract | [daa46432e847ed9613dc403045498e27281eff42](https://github.com/bubth720/JARVIS-LLM/tree/daa46432e847ed9613dc403045498e27281eff42) | **Retenir pour future fixture** : JNI P2 et worker durci ; pas qualification Android physique |

Les quatre préfixes fournis résolvent des commits existants égaux aux têtes des
branches nommées au relevé. Le choix ci-dessus est une recommandation de base,
aucune fusion ou activation de branche divergente.

## Filiation réellement calculée

CORE : base004A306a89b →07cd282 → deux commits →29646448. merge-base des deux
branches =07cd282 ; rev-list left/right=0/2. La branche renforcée contient donc
l’initiale. Le complément ajoute ProcessInferenceAdmission, son emploi par le
contrôleur **et les instances historiques directes**, et des jetons de génération
qui empêchent une ancienne confirmation de libérer le nouveau propriétaire.
Cela ne coordonne toujours pas un autre APK.

LLM : merge-base des deux branches =**43503f59f530f2bb48955bce9d7d71e2470fb668**
(003C), rev-list left/right=**4/7**. Ni branche n’est ancêtre de l’autre.
Les quatre fichiers de domaine P2Contract/P2Prompt/P2Lifecycle/Core004BMapping
ont pourtant des blobs identiques aux deux têtes : divergence du chemin natif,
contrat moteur, tests/outillage/docs, pas deux contrats P2 entièrement différents.
Aucune résolution automatique des27 chemins différents.

Les lignes ci-dessous sont les commits exclusifs, obtenus par git log, pas une
liste de PR prétendument fusionnées :

### JAVIS-Local-v2 — côté initial seulement

```text
(aucun)
```

Côté renforcé/natif seulement :

```text
29646448c80568d868a702192df761fc9d7a896d fix: correlate release acknowledgements with admission leases
c28bdcc4cec2b99304826ac85a1df83fd296f2d2 fix: enforce process-wide inference backend admission
```

### JARVIS-LLM — côté initial seulement

```text
c4e7611eebb64a96a796164bc3d4c961dbc7dcba Record successful Mission 003D validation and native P2 limitations [skip ci]
74093e37c3cf2e9951af7f0fe4c98defe4972159 Preserve CORE 004B default no-think directive in authorized system only
b25af4a6167e6d5cc9bad8dc8025e9b202737e51 Track prompt tokenization completion and bound composed P2 messages
89a9defb725259b6be9af8e26b1b0b2e2ace6366 Define opt-in P2 generation contract and CORE 004B text mapping without native activation
```

Côté renforcé/natif seulement :

```text
daa46432e847ed9613dc403045498e27281eff42 Record successful P2 JNI and Android CI with physical and CORE session limits [skip ci]
0f13573eafaf461714ba9dc00bbb208b1e723fb8 Quarantine failed unload and destruction until cleanup is confirmed
56cd3c7d4a9e3d41ec6030b126d0759ba9513e3a Verify backend lease retention and concurrent generation refusal with injected native failures
ebd45a0c045af289ba8c3c1a384e39886c38717e Transmit optional P2 system through existing JNI engine with strict context retention and host coverage
955713d047b51cec4030bda16453542c0633abdf Preserve CORE 004B default no-think directive in authorized system only
d5e2515f9b3068b219e173cd7006d4a866bae68e Track prompt tokenization completion and bound composed P2 messages
f679ec09c269f4ca0b1c1cd730253a62a955d8f8 Define opt-in P2 generation contract and CORE 004B text mapping without native activation
```

## Fichiers exactement modifiés dans les comparaisons

Statuts git diff --name-status entre têtes, avant toute interprétation :

### JAVIS-Local-v2 — tête initiale → renforcée/native

```text
M	AGENTS.md
M	app/src/main/java/com/stark/jarvislocal/InferenceContract.kt
M	app/src/main/java/com/stark/jarvislocal/InferenceController.kt
M	app/src/main/java/com/stark/jarvislocal/LlamaLocalEngine.kt
A	app/src/main/java/com/stark/jarvislocal/ProcessInferenceAdmission.kt
M	app/src/test/java/com/stark/jarvislocal/InferenceControllerTest.kt
A	app/src/test/java/com/stark/jarvislocal/IsolatedInferenceFactory.kt
M	app/src/test/java/com/stark/jarvislocal/LlamaLifecycleTest.kt
A	app/src/test/java/com/stark/jarvislocal/ProcessInferenceAdmissionTest.kt
M	app/src/test/java/com/stark/jarvislocal/SessionInferenceLifecycleTest.kt
M	docs/PROJECT_KNOWLEDGE.md
M	docs/mission-004b/LLM_003D_MAPPING.md
M	docs/mission-004b/REPORT.md
M	docs/mission-004b/VALIDATION.md
```

### JARVIS-LLM — tête initiale → renforcée/native

```text
M	.github/workflows/android.yml
M	app/src/main/cpp/CMakeLists.txt
M	app/src/main/cpp/bridge.cpp
A	app/src/main/cpp/tests/jni/NativeBridge.java
M	app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt
A	app/src/test/java/fr/jarvis/llm/NativeBackendLifecycleTest.kt
D	docs/evidence/mission003d-74093e3.json
A	docs/evidence/mission003d-p2-0f13573.json
M	docs/mission-003d/ADAPTATIONS-NATIVES.md
M	docs/mission-003d/AUDIT.md
M	docs/mission-003d/COMPATIBILITE-CORE-004B.md
M	docs/mission-003d/CONTRAT-P2.md
M	docs/mission-003d/CYCLE-DE-VIE.md
M	docs/mission-003d/RAPPORT.md
A	docs/mission-003d/VALIDATION.md
A	docs/mission-003d/reference-contract-only/ADAPTATIONS-NATIVES.md
A	docs/mission-003d/reference-contract-only/AUDIT.md
A	docs/mission-003d/reference-contract-only/COMPATIBILITE-CORE-004B.md
A	docs/mission-003d/reference-contract-only/CONTRAT-P2.md
A	docs/mission-003d/reference-contract-only/CYCLE-DE-VIE.md
A	docs/mission-003d/reference-contract-only/RAPPORT.md
M	domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/NativeRequestTest.kt
M	tools/check-preservation-003d.py
M	tools/compare-model-memory.py
A	tools/test-jni-p2.sh
M	tools/test-native.sh
```

### Chaque livraison par rapport à sa base

`JAVIS-Local-v2` `306a89b..07cd282603205d57f3d2ded1b14d5d95e68989e2` :

```text
M	AGENTS.md
M	app/src/main/java/com/stark/jarvislocal/AppGraph.kt
A	app/src/main/java/com/stark/jarvislocal/InferenceContract.kt
A	app/src/main/java/com/stark/jarvislocal/InferenceController.kt
M	app/src/main/java/com/stark/jarvislocal/JarvisCore.kt
M	app/src/main/java/com/stark/jarvislocal/LlamaLocalEngine.kt
M	app/src/main/java/com/stark/jarvislocal/LocalLanguageModel.kt
M	app/src/main/java/com/stark/jarvislocal/PromptBuilder.kt
M	app/src/main/java/com/stark/jarvislocal/SessionCoordinator.kt
A	app/src/test/java/com/stark/jarvislocal/CoreInferenceContractTest.kt
A	app/src/test/java/com/stark/jarvislocal/InferenceControllerTest.kt
A	app/src/test/java/com/stark/jarvislocal/LlamaLifecycleTest.kt
A	app/src/test/java/com/stark/jarvislocal/SessionInferenceLifecycleTest.kt
M	docs/PROJECT_KNOWLEDGE.md
A	docs/mission-004b/LLM_003D_MAPPING.md
A	docs/mission-004b/REPORT.md
A	docs/mission-004b/VALIDATION.md
```

`JAVIS-Local-v2` `306a89b..29646448c80568d868a702192df761fc9d7a896d` :

```text
M	AGENTS.md
M	app/src/main/java/com/stark/jarvislocal/AppGraph.kt
A	app/src/main/java/com/stark/jarvislocal/InferenceContract.kt
A	app/src/main/java/com/stark/jarvislocal/InferenceController.kt
M	app/src/main/java/com/stark/jarvislocal/JarvisCore.kt
M	app/src/main/java/com/stark/jarvislocal/LlamaLocalEngine.kt
M	app/src/main/java/com/stark/jarvislocal/LocalLanguageModel.kt
A	app/src/main/java/com/stark/jarvislocal/ProcessInferenceAdmission.kt
M	app/src/main/java/com/stark/jarvislocal/PromptBuilder.kt
M	app/src/main/java/com/stark/jarvislocal/SessionCoordinator.kt
A	app/src/test/java/com/stark/jarvislocal/CoreInferenceContractTest.kt
A	app/src/test/java/com/stark/jarvislocal/InferenceControllerTest.kt
A	app/src/test/java/com/stark/jarvislocal/IsolatedInferenceFactory.kt
A	app/src/test/java/com/stark/jarvislocal/LlamaLifecycleTest.kt
A	app/src/test/java/com/stark/jarvislocal/ProcessInferenceAdmissionTest.kt
A	app/src/test/java/com/stark/jarvislocal/SessionInferenceLifecycleTest.kt
M	docs/PROJECT_KNOWLEDGE.md
A	docs/mission-004b/LLM_003D_MAPPING.md
A	docs/mission-004b/REPORT.md
A	docs/mission-004b/VALIDATION.md
```

`JARVIS-LLM` `43503f5..c4e7611eebb64a96a796164bc3d4c961dbc7dcba` :

```text
M	.github/workflows/android.yml
M	README.md
A	docs/evidence/mission003d-74093e3.json
A	docs/mission-003d/ADAPTATIONS-NATIVES.md
A	docs/mission-003d/AUDIT.md
A	docs/mission-003d/COMPATIBILITE-CORE-004B.md
A	docs/mission-003d/CONTRAT-P2.md
A	docs/mission-003d/CYCLE-DE-VIE.md
A	docs/mission-003d/RAPPORT.md
A	docs/mission-003d/SOURCES.json
A	domain/src/main/kotlin/fr/jarvis/domain/generation/Core004BMapping.kt
A	domain/src/main/kotlin/fr/jarvis/domain/generation/P2Contract.kt
A	domain/src/main/kotlin/fr/jarvis/domain/generation/P2Lifecycle.kt
A	domain/src/main/kotlin/fr/jarvis/domain/generation/P2Prompt.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/Core004BMappingTest.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/P2ContractTest.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/P2Fixtures.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/P2LifecycleTest.kt
A	tools/check-preservation-003d.py
M	tools/publish-validation-003b.py
```

`JARVIS-LLM` `43503f5..daa46432e847ed9613dc403045498e27281eff42` :

```text
M	.github/workflows/android.yml
M	README.md
M	app/src/main/cpp/CMakeLists.txt
M	app/src/main/cpp/bridge.cpp
A	app/src/main/cpp/tests/jni/NativeBridge.java
M	app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt
A	app/src/test/java/fr/jarvis/llm/NativeBackendLifecycleTest.kt
A	docs/evidence/mission003d-p2-0f13573.json
A	docs/mission-003d/ADAPTATIONS-NATIVES.md
A	docs/mission-003d/AUDIT.md
A	docs/mission-003d/COMPATIBILITE-CORE-004B.md
A	docs/mission-003d/CONTRAT-P2.md
A	docs/mission-003d/CYCLE-DE-VIE.md
A	docs/mission-003d/RAPPORT.md
A	docs/mission-003d/SOURCES.json
A	docs/mission-003d/VALIDATION.md
A	docs/mission-003d/reference-contract-only/ADAPTATIONS-NATIVES.md
A	docs/mission-003d/reference-contract-only/AUDIT.md
A	docs/mission-003d/reference-contract-only/COMPATIBILITE-CORE-004B.md
A	docs/mission-003d/reference-contract-only/CONTRAT-P2.md
A	docs/mission-003d/reference-contract-only/CYCLE-DE-VIE.md
A	docs/mission-003d/reference-contract-only/RAPPORT.md
M	domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt
A	domain/src/main/kotlin/fr/jarvis/domain/generation/Core004BMapping.kt
A	domain/src/main/kotlin/fr/jarvis/domain/generation/P2Contract.kt
A	domain/src/main/kotlin/fr/jarvis/domain/generation/P2Lifecycle.kt
A	domain/src/main/kotlin/fr/jarvis/domain/generation/P2Prompt.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/Core004BMappingTest.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/NativeRequestTest.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/P2ContractTest.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/P2Fixtures.kt
A	domain/src/test/kotlin/fr/jarvis/domain/generation/P2LifecycleTest.kt
A	tools/check-preservation-003d.py
M	tools/compare-model-memory.py
M	tools/publish-validation-003b.py
A	tools/test-jni-p2.sh
M	tools/test-native.sh
```

## Validation publiée et observation GitHub Actions

L’API api.github.com renvoie **Tunnel connection failed:403 Forbidden** pour le
GET du run P2. Pas de token envoyé, pas de retry API ni de contournement. La voie
**page publique github.com/actions** est normalement autorisée et a été consultée
avec TLS/proxy conservés ; ce n’est pas une URL API déguisée.

| Référence | Rapport versionné | Résultat directement accessible observé ici | Limite |
|---|---|---|---|
| CORE07cd282 |174 succès,0 saut ; simulations/JVM, natif simulé | Pas de run au SHA exact attesté | Aucun test CORE exécuté dans D4-02C |
| CORE29646448 |187 succès,0 échec/erreur/saut ;140 anciens+34+13 | Liste Actions publique accessible, résultat exact SHA non vérifié ; workflow build-apk manuel lu | Rapports locaux, pas CI verte inventée ; aucun natif GGUF/Android physique |
| LLM c4e7611 / code74093e3 |83 domaine+21 simulations+CTest1/1 | [38928638903](https://github.com/bubth720/JARVIS-LLM/actions/runs/38928638903) : **Status Success**, SHA complet74093e37c3cf2e9951af7f0fe4c98defe4972159 présent,83/21/1 et0 échec/saut dans annotation JSON | CTest historique n’est pas P2 ; tokenizer/lifecycle de fixture |
| LLM daa46432 / code0f13573 |87 domaine+25 app JUnit (21 simulés+4 worker/nativeAPI simulée)+CTest1/1 et harnais JNI Linux | [38963365435](https://github.com/bubth720/JARVIS-LLM/actions/runs/38963365435) : **Status Success**, SHA complet0f13573eafaf461714ba9dc00bbb208b1e723fb8 présent,87/25/1 et0 échec/saut dans annotation JSON | Le harnais JNI/GGUF relève de Linux, pas du worker Android physique ni CORE inter-APK |

Pages lues le16 octobre2026 ; UI affiche push16:01 et20:35 sans que le fuseau de
ces libellés soit inféré. Horodatages précis de consultation et extraits d’annotation
normalisés dans actions-observed.json, dossier cache. Les résumés visibles sont
cohérents avec les rapports ; **ZIP/XML JUnit et logs complets non téléchargés**,
aucune prétention de réexécution ou vérification individuelle des XML.
Les widgets de navigation GitHub peuvent afficher «Uh oh» ; le champ Status et
les annotations de run restent lisibles, pas pris pour un échec du workflow.

Après les commits testés74093e3 et0f13573, les diffs jusqu’aux têtes c4e7611/daa46432
ne changent que docs et preuves. Le runtime des deux têtes correspond donc à leurs
commits de code cités ; cela ne qualifie toujours pas Android physique.
CORE workflow build-apk.yml est workflow_dispatch : télécharge modèles et publie
une release, sans test/Lint. Il n’a pas été déclenché par cet audit et son simple
build ne prouverait pas les187 cas locaux rapportés.

## Preuves source déterminantes

Type = code lu ou documentation versionnée, pas exécution. Chaque lien blob a été
résolu avec git cat-file à son SHA ; un HTTP200 de page ne remplace pas ce contrôle.

| Dépôt | Fichier au commit | SHA256 du blob |
|---|---|---|
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/InferenceContract.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/app/src/main/java/com/stark/jarvislocal/InferenceContract.kt) | `4588606d1f403fa04d770d1d7f51adb168efb7eb26c7fb98e1826dfda779b997` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/InferenceController.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/app/src/main/java/com/stark/jarvislocal/InferenceController.kt) | `488a79c5fe28df0279f9d16af9783f3b2184029fa773ab94c550eb1ef6b0c3e5` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/ProcessInferenceAdmission.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/app/src/main/java/com/stark/jarvislocal/ProcessInferenceAdmission.kt) | `0611c8b12d036f0de6329308ccf10bb9d09838198420073f9dea482a091a2602` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/LocalLanguageModel.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/app/src/main/java/com/stark/jarvislocal/LocalLanguageModel.kt) | `2b980c6a4d4603fcfbc3b5320b7e60a3a135ecd7e4296c879b15011f8665dc07` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/LlamaLocalEngine.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/app/src/main/java/com/stark/jarvislocal/LlamaLocalEngine.kt) | `94eef86357b1e6985785cea540395ca30640e1ca8c5ce4b6d001671195ef81d9` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/PromptBuilder.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/app/src/main/java/com/stark/jarvislocal/PromptBuilder.kt) | `7867a3c6c2e76e4ab5e4d1a436f9cd61bfd88f7bd82661e660f2a2015640fb4d` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/JarvisCore.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/app/src/main/java/com/stark/jarvislocal/JarvisCore.kt) | `98383134a95e182c74313d5a188b753b3904be4ffa954b1a772f510b755a4082` |
| JAVIS-Local-v2 | [docs/mission-004b/VALIDATION.md](https://github.com/bubth720/JAVIS-Local-v2/blob/29646448c80568d868a702192df761fc9d7a896d/docs/mission-004b/VALIDATION.md) | `2429a610aecf188280689cd4ab7155b5092230cadc42e8d0fd8076d2096427c9` |
| JARVIS-LLM | [domain/src/main/kotlin/fr/jarvis/domain/generation/P2Contract.kt](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/domain/src/main/kotlin/fr/jarvis/domain/generation/P2Contract.kt) | `740441c8ee4a0001e91744ade5eb5f5343480c4d491979ec1019d38fbd20d696` |
| JARVIS-LLM | [domain/src/main/kotlin/fr/jarvis/domain/generation/P2Prompt.kt](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/domain/src/main/kotlin/fr/jarvis/domain/generation/P2Prompt.kt) | `1cf0784c6e4f83a4752fd4c981d79773aa5f2696795844149c230f824703a70f` |
| JARVIS-LLM | [domain/src/main/kotlin/fr/jarvis/domain/generation/P2Lifecycle.kt](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/domain/src/main/kotlin/fr/jarvis/domain/generation/P2Lifecycle.kt) | `cf95695a5be8484aa6673143c8c13c7df9fb8bea67f4b9038a144f6ec16ef148` |
| JARVIS-LLM | [domain/src/main/kotlin/fr/jarvis/domain/generation/Core004BMapping.kt](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/domain/src/main/kotlin/fr/jarvis/domain/generation/Core004BMapping.kt) | `a64a818e7d4891db8ec30c28d9f93a6e6acd0e1f9dcd58d00acd49ad23c1c7b3` |
| JARVIS-LLM | [domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt) | `2a8d59c53ce6b964f4345d608ad7bdc83f2a6f18d2e0e7406fed0f396baf52f6` |
| JARVIS-LLM | [app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt) | `3feed68780907affdf4bdfd9d4a5a83119371dd59a8c253736916618c3dccebb` |
| JARVIS-LLM | [app/src/main/cpp/bridge.cpp](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/app/src/main/cpp/bridge.cpp) | `736d6707682b56d2cfa52ffb79d960b498b122958a51f9b95a78e4b6c46458a3` |
| JARVIS-LLM | [app/src/main/cpp/tests/jni/NativeBridge.java](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/app/src/main/cpp/tests/jni/NativeBridge.java) | `8b6f7f7a7446d0d1bf18615ce8b065d0cd68c4b02ab04af5df0814e52cd881f9` |
| JARVIS-LLM | [docs/mission-003d/VALIDATION.md](https://github.com/bubth720/JARVIS-LLM/blob/daa46432e847ed9613dc403045498e27281eff42/docs/mission-003d/VALIDATION.md) | `4e475a0eb369455fe804b9f0b347f5e36c65a0eaf9d200be984c425e5d40ad92` |
| JARVIS-LLM | [docs/mission-003d/RAPPORT.md](https://github.com/bubth720/JARVIS-LLM/blob/c4e7611eebb64a96a796164bc3d4c961dbc7dcba/docs/mission-003d/RAPPORT.md) | `ac901d8495a58cd7c77b3625fdff7d2f28dbb3871bd5676a972240a237ab45bb` |

Les détails/bornes de contrat sont analysés dans MATRICE_CONVERGENCE et
ECARTS_ET_CORRECTIONS ; ces fichiers ne sont pas un contrat de transport approuvé.
Les vieux rapports affirmant «contrat natif absent» restent exacts pour c4e7611,
mais ne doivent pas remplacer le constat de generateP2 réellement présent dans
daa46432. Les assertions «P2Lifecycle non câblé» restent vraies pour les deux.
