# FUSION-01 F0 — NEXUS et SERVICES, audit de sources en lecture seule

Date : 25 octobre 2026 UTC. Aucun dépôt source, branche, base utilisateur, runtime ou APK modifié. Aucun test externe fraîchement exécuté. Les chiffres ci-dessous sont ceux des preuves versionnées, examinées aujourd'hui ; les conclusions CI ont été revérifiées sur pages publiques GitHub. Les bare clones et snapshots d'audit sont sous `/tmp`.

## Références et divergence prouvée

| Module | Candidat portable | Alternative finale | Parent commun |
|---|---|---|---|
| NEXUS | `feat/nex-06a-android-api24` `374ea2e2fd640e78f2f5e12e60e75b493420e504` | `feat/nexus-final-01` `d903bf04f497ab0dc7f40e9708ed057e4f24c6ee` | `3acec55616ff8e3b1666091780fca59261377e18` |
| SERVICES | `feat/serv-04a-android-tool-port` `f00091a639612b91eca1a301580c8f531249f1e3` | `feat/services-final-01` `d16dd84f27881460ec9f02d2a54d9ddff23187dc` | `3decdc47d82f9b43713c48cab244762941770a81` |

Les SHA distants correspondent exactement. Dans chaque paire, aucune branche n'est ancêtre de l'autre. Les noms « final » ne prouvent donc pas l'inclusion des ports. NEXUS final a pour parent `bbccac2ff2cc052f897c7f5015f234507e047b95` (NEX-04), puis NEX-05. SERVICES final descend du SERV-03 commun via `b71bffd...`, `a3372a4...`, `edfa044...`, pas de SERV-04A.

Le candidat unique portable peut choisir les deux ports, en conservant les finales comme alternatives non composées. Il ne constitue pas une intégration JVM ou Android déjà testée : CORE `aea5ac859ac551d54fe16187c1883a487dbee9d6` consomme toujours NEXUS `777e6afa75ecb99b85e52d68837cb0fefcf161cd` et SERVICES `3decdc47d82f9b43713c48cab244762941770a81`. Recompiler/porter le consommateur nécessite une mission propriétaire CORE et une nouvelle preuve F1.

## CI réellement observée aujourd'hui

- NEXUS port : [run 40115049468](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/40115049468), SHA `374ea2e...`, **FAILURE**. Job `storage` (120934494420) réussit tests JVM, deux processus et backup ; job `android-adapter` (120934494656) échoue sur `Run android-actions/setup-android@v3`. Build/tests/Lint Android sautés et aucun artefact Android. La cause précise de setup n'est pas visible dans les logs anonymes.
- SERVICES port : [run 40115305244](https://github.com/bubth720/JARVIS-SERVICES/actions/runs/40115305244), SHA `f00091a...`, **FAILURE**. Job `jvm` (120935248589) et `android-instrumented` historique API26 (120935248672) réussissent. Job `android-build` (120935248386) échoue à `SERV-04A Android24 adapter regressions and library` ; compilation boot API24 suivante sautée. Le message Gradle/test précis n'est pas accessible anonymement ; ne pas supposer une cause.
- SERVICES final : [run 40142362407](https://github.com/bubth720/JARVIS-SERVICES/actions/runs/40142362407), **SUCCESS**, 7m12s, trois jobs. SHA observé `edfa044321ff09697ae9bec40a6e31aa76a77370` (code/pilote), **pas** le commit de documentation `d16dd84...` ; aucune propagation silencieuse de succès CI vers ce dernier.
- NEXUS final : page Actions filtrée affiche zéro résultat. État **UNKNOWN**, ni échec inventé ni succès déduit.

## NEXUS : code, schéma et contraintes

Au port `374ea2e...` : `nexus-core` est métier partagé ; `nexus-jvm-store` conserve JDBC/snapshots ; `nexus-android-store` est bibliothèque min24, compile35, AGP8.7.3, Kotlin2.0.21, Gradle8.10.2, JDK17, propre bytecode Java8. Aucune `.so`, permission ou JDBC ajouté au produit Android.

`store/NexusStoragePort.kt` expose `readSession`, `inTransaction`, `acquireImportLease`; `NexusSession` porte requêtes/paramètres. La lease concerne uniquement le parseur documentaire, pas une autorité native LLM. `NexusClock` retire le lien java.time. `AndroidNexusStorage.kt` vérifie user_version puis compile_options et vraie création temporaire FTS5/vocab, MATCH, BM25 avant migration ; l'absence donne `CAPABILITY_UNAVAILABLE`, et la version incompatible un refus distinct. Aucun factory public ne contourne la sonde.

Schéma **3** au port, schéma **4** à la finale. Une base v4 ne doit pas être ouverte par le port v3 ; aucune migration personnelle ou downgrade n'est proposé. La finale ajoute métadonnées, emplacements et graphe (`document_metadata`, `import_metadata`, `fragment_location`, `graph_node`, `graph_edge`) ; il faut porter ces changements dans le stockage portable en réexécutant migrations/rollback/snapshots sur copies avant adoption.

`rag/RagTypes.kt` garde `RagContextPort.retrieve(query,scope,limits)` et `resolve(citation,scope)`. Citation : id, documentId, version, ordinal, sourceId, sourceUri, sourceSha256, page nullable, start/end UTF-16, textSha256. Les budgets de contexte sont 4000 caractères/5 items/5 sources par défaut ; plafonds 32000/20/20. `estimatedTokens` est un estimateur éditorial, explicitement ni admission ni tokeniseur. Le carrier `jarvis.nexus.context/1` est `trusted:false`, sans rôle SYSTEM ou permission.

Import SAF/PFD : URI content choisie et confirmée par hôte, flux r fermé, borne 2MiB par importeur, digest et identité vérifiés entre enqueue/process. Le catalogue bas niveau conserve ses limites propres (source16MiB par défaut, fragments2048×8192 caractères, total2M) ; ne pas confondre ces plafonds avec le parcours importeur 2MiB.

**Conflit ArchiveReader** : au port, lecture de plages 64 bits `readRange(offset,maxBytes)` ; à la finale, `article(ArticleSelection): ArchiveArticle`, processus Linux optionnel. Les deux ne sont pas substituables par nom. Le ZIM Android demeure `UNSUPPORTED`. libzim réel/archive réelle non qualifiés dans le rapport final.

Preuves historiques : port 69 JVM +33 Robolectric, 0 échec/saut, compilation API24 et deux tests instrumentés seulement compilés. Android RAG cité non qualifié (SQLite Robolectric sans FTS5). Finale : 10 SQL Python +7 JS +18 ZIM (1 saut), navigateur desktop/tactile émulé ; **Kotlin/JVM final et régression backup chiffré NOT_RUN**.

## SERVICES : capacités et frontières

Au port `f00091a...`, `services-portable-api` partage les classes historiques sans API Path ; `shared-runtime` reste façade JVM ; `services-android-adapter` est min24, compile35, AGP8.9.2, Gradle8.13, Java11/JDK17. L'APK historique reste min26. API locale `jarvis.services.inprocess/1` : `catalogue`, `dispatch`, `confirm`, `close`; classe Android ajoute `selectSource`, `receipts`, `audit`, `capabilities`, `closeAsync`.

Deux outils disponibles : `documents.search` sur pages sélectionnées, et `data.csv.normalize` réutilisant Data. Recherche en mémoire de session = projection bornée, pas catalogue documentaire concurrent NEXUS. Citations lient SHA source/texte, page, offsets, extrait exact. Source2MiB, huit sources/100pages/250000 caractères ; query500 caractères, 50citations de600caractères. Arguments exacts ≤16champs/2MiB ; requestId UUID canonique, timeout1..90000ms. Permissions et principal viennent de l'hôte, jamais de documents/LLM. ApprovalGate : contenu/version/request/principal digest/epoch, expiration60s, usage unique.

Journal privé neuf, owner marker+verrou OS ; 4096 reçus puis refus, aucun reset/purge. Une requête reçue ne rejoue pas après reprise ; reçu ACCEPTED interrompu→UNKNOWN. Persistance avant livraison, défaut de reçu→UNKNOWN/RECEIPT_UNCONFIRMED, fermeture après opérations observées. Annulation coopérative, ni libération JNI ni interruption de provider bloqué prétendues.

**DOCX nouveau port** : `SAF_EXPORT_UNQUALIFIED`, aucun fichier cible écrit. Les outils/workflows17 de la finale ne sont pas présents dans ce port. Conserver ce refus jusqu'au portage et à la qualification SAF/consent/readback/UNKNOWN. L'extraction Guard→AccessGuard impose recompilation des consommateurs, pas remplacement binaire JAR aveugle.

La finale `d16dd84...` garde `java.nio.file`, un shared-runtime non extrait et APK min26 ; elle possède 17 outils et contrats `contracts/services-final/v1`, jobs durables, mémoire atelier consentie, BRIDGE HMAC fichiers. Cette mémoire n'est pas la mémoire personnelle centrale CORE. BRIDGE n'a aucun transport de production activé, n'exécute aucune commande distante. Nouveaux jobs/journaux ne sont pas intégrés au snapshot Recovery historique, limitation explicitement documentée.

Preuves historiques : port94JVM +40Robolectric, compilation réelle des22sourcescontreSDK24, 0échec/saut ; pas d'instrumentation du nouveau port. Finale129JVM +17instrumentés API26x86 +SAF réel/force-stop entre étapes ; pas de qualification ARM64 physique ou autreAPI. ABI empaquetées arm64-v8a/armeabi-v7a/x86/x86_64 ≠ qualification de ces matériels.

## Licences et compatibilité

Aucun fichier de licence racine trouvé pour les projets NEXUS/SERVICES ; statut projet **UNKNOWN**, pas de droit de redistribution inventé. Dépendances SERVICES documentées : Gson2.11 Apache2, PDFBoxAndroid2.0.27 Apache2, BouncyCastle1.86 MIT, SQLiteJDBC Apache2/SQLite domaine public, AndroidXbundledApache2. ZIM optionnel étudié : libzimGPL2+, python-libzimGPL3+, java-libkiwixGPL3+ ; aucun nouveau binaire ajouté/autorisé par cet audit. NOTICES/SBOM complet restant nécessaire avant diffusion.

Matrice déploiement : NEXUS Android24/25/26 cité BLOCKED faute qualification FTS5, API29ARM64 NOT_TESTED ; SERVICES nouveauport API24/25/26/29ARM64 NOT_TESTED en instrumentation, compile et simulations seulement ; application autonome SERVICESfinalAPI26x86 a preuve émulateur historique, pas une preuve du port24. Linux hôte a preuves JVM historiques distinctes ; mini-PC matériel NOT_TESTED partout.

F0 doit donc pouvoir valider la structure du BOM sans promouvoir ces preuves en GO Android. F1 sur la nouvelle paire n'a pas été exécuté, F2/F3 et produit intégré restent bloqués.
