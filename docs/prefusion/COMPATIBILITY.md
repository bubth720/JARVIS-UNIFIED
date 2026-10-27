# Compatibilité pré-fusion — non qualifiée pour assemblage

Références SHA40 et branche mission : [ASSESSMENT](ASSESSMENT.md). Le code des trois corrections est gelé depuis ces sources. Une compilation minSdk24 globale ne rend pas un runtime minSdk29 utilisable sur API24.

| Module | SDK/ABI/JNI | Java / Gradle / Kotlin / AGP | Dépendances et formats | Objets publics / contrats |
|---|---|---|---|---|
| CORE | min24, ARM64, moteurs historiques | Java17 ; Gradle8.10.2 CI, sans wrapper racine ; Kotlin2.0.21 / AGP8.7.3 | coroutines1.9.0, llama-android0.1.1, whisper-android1.0.0, PDFBox Android2.0.27.0 ; LocalDatabase intacte | SessionCoordinator/AppGraph, TaskCoordinator ; DocumentToolReadinessPort C0 diagnostique OFF ; aucun nouveau producteur adopté |
| NEXUS | AAR min24 ; SQLite plateforme ; aucun nouveau JNI ; JDBC hôte distinct | toolchain17, bytecode Java/Kotlin1.8 ; Gradle8.10.2 / Kotlin2.0.21 / AGP8.7.3 | schéma v4, FTS5/MATCH/vocab(instance)/BM25 ; SourceRecord URI/SHA/taille, snapshots existants | NexusStoragePort, DocumentaryGateway/RagContextPort ; FTS5 absent => refus ; Robolectric n'est pas Android réel |
| SERVICES | SDK min24, diagnostic min26 ; pas de nouveau JNI | **Java11** API portable/adaptateur ; JDK21 CI ; Gradle8.13 / AGP8.9.2 | Gson2.11.0, PDFBox Android2.0.27.0, BouncyCastle1.86 ; journaux locaux ; 17 historiques vs2 portés | ServicesToolPort/1, ServicesAndroidToolPort ; CommitAuthorization proposal/1 et ServicesWirePreflight non autorité runtime ; SAF export OFF |
| LLM | min29, compile/target36, ARM64 ; NDK28.1.13356709 ; 16Kio à vérifier par artefact/cible | JDK21, bytecode17 ; Gradle8.11.1 / Kotlin2.1.21 / AGP8.10.1 | llama.cpp épinglé, GGUF import manuel SHA/taille ; aucun modèle téléchargé dans ce lot | jarvis.llm.client/1, P2/1.0, Binder fixture/1 et bundle/2 distincts ; client hash f29f8a9f3e10645fe1f25ea01913ccc8cf2ee883cbc45f7adca18645ac322b0f ; tokenizer structuré UNSUPPORTED |
| VOICE | min26 ; ARM64 Studio, ABI de test explicitement remplaçable ; ONNX natif | Java17 ; Gradle8.13 / Kotlin2.1.20 / AGP8.9.2 | ONNX Runtime Android1.27.0 ; profils/packs privés et JVFP1/JVIENC01 historiques conservés | Binder V1 signé ; voice.final01.events/1 et fusion02.audio/1-draft / speak/1-draft ; pas d'émotion non neutre ni phonèmes qualifiés |
| INTERFACE | min26 ; Compose/presentation, ABI transitive à inventorier | Java17 ; Gradle8.13 / Kotlin2.1.20 / AGP8.9.2 | Compose BOM2025.04.01, DataStore1.1.7, serialization1.8.1, coroutines1.10.2 ; formats persistants non requalifiés | client UI-03 local, HostCapabilityReport/2 proposé, AvatarExpressionStateMachine ; origine réelle NONE, pas de transport authentifié |
| EVOLUTION | JVM seulement ; aucun minSdk Android attesté | Java17 ; Gradle8.13 / Kotlin2.1.20 | coroutines1.10.2, sqlite-jdbc3.46.1.0 ; schéma technique1, revue Ed25519 | EventSink/diagnostics/propositions ; runner fermé selon dossier EVOL-03, sandbox OS non qualifiée |
| UNIFIED | hors runtime, ni APK ni JNI | Python3.12 testé, aucun assemblage Gradle ajouté | contrats/v1 gelés, v2 draft, photos BOM/workspace inchangées | registre/preuves/validateurs, jamais autorité runtime |

## Licences et compatibilité persistante

Cette table n'est pas une SBOM de redistribution approuvée. **Licences des dépôts et inventaire transitif complet : NOT_QUALIFIED** pour assemblage. Ne pas déduire un droit de l'absence d'un LICENSE racine.
- CORE : licences/notices des AAR llama/Whisper et de leurs natifs à vérifier avant import commun ; licences des modèles distinctes.
- NEXUS : SQLite plateforme domaine public / wrappers AOSP Apache2 selon l'étude historique. AndroidX sqlite-bundled2.5.2 n'est qu'un candidat inspecté : min21 déclaré, quatre ABI, AAR3 365 857octets / .so ARM641 932 216octets. Ni taille APK finale ni garantie FTS5 ; transitifs/CVE/16Kio/migration/budgets à revoir avant décision. Requery3.50.4 reste documentaire. FTS4/littéral ne fournit pas le même contrat. JDBC hôte ne doit pas être embarqué dans l'APK24.
- SERVICES : Gson/PDFBox Apache2 et BC permissive décrits dans REPORT historique ; notices/distribution à confirmer. Catalogue17 non migré.
- VOICE : licences ONNX, pack, modèle et référence vocale séparées. Aucune permission de transférer les profils/audio ou redistribuer des poids n'est présumée.
- UI/EVOLUTION : versions épinglées ne remplacent pas les notices ; le dossier EVOL décrit Kotlin/coroutines/sqlite-jdbc Apache2, SQLite domaine public, JUnit test EPL1.
- Aucun schéma, migration persistante, version SDK, dépendance ou ABI n'est harmonisé par ce lot.

## Preuves séparées

| Module | Logiciel JVM/host | Robolectric/build | Émulateur / physique |
|---|---|---|---|
| UNIFIED | 167+20+23+23 PASS locaux à base mission ; nouvelle CI requise | n/a | physique NOT_RUN |
| NEXUS | garde6, SQL10, ZIM18PASS/1SKIP locaux ; CI40547468137 SUCCESS au SHA201f0d2… | lane Android-hôte SUCCESS même SHA | nouvelle instrumentation NOT_RUN ; anciennes24/25 FTS5 absent ; physique NOT_RUN |
| SERVICES | JVM source365da… SUCCESS sans total inventé ; local bloqué | build/lint source SUCCESS | 15/15 sans skip par API24/25/26/35 au SHA365da… ; nouvelle CI documentaire indépendante ; physique NOT_RUN |
| LLM | garde6/preuves11 locaux, nouvelle CI en cours au relevé | ne pas anticiper résultat | GGUF Android/physique NOT_RUN |
| VOICE | garde6 local ; nouvelle lane JVM SUCCESS | simulation distincte du natif | nouvelle campagne audio26/35 en cours/attente ; physique NOT_RUN |
| CORE | audit source, nouvelles suites NOT_RUN | nouveau build NOT_RUN | NOT_RUN |
| INTERFACE | CI source40412782652 Android SUCCESS | couverture limitée au workflow observé | nouveaux instrumentés/physique NOT_RUN |
| EVOLUTION | CI source40412785717 JVM SUCCESS | aucun Android qualifié | sandbox/physique nouveau NOT_RUN |

Sources : build.gradle(.kts), wrapper properties, libs.versions.toml et contrats aux SHA du relevé. Les succès antérieurs sont datés et non attribués aux nouveaux commits. Pas de qualification par le seul manifeste, ni de conversion implicite des offsets UTF16/UTF8.
