# FUSION-02 U0 — NEXUS / SERVICES, audit externe en lecture seule

Observation du 25 octobre 2026. Mission directrice UNIFIED #5 et sous-issues NEXUS #3 / SERVICES #3 lues intégralement. Aucun fichier, branche ou build des dépôts sources modifié, aucun test externe fraîchement exécuté. Les nouveaux objets sont lus dans des bare snapshots temporaires ; les anciens résultats sont explicitement historiques.

## Références et correction importante du checkpoint

| Rôle | Branche | SHA exact | Parent |
|---|---|---|---|
| NEXUS candidat nouveau | feat/fusion-01-nexus-integration | 9d6928cd8651f83fa5091bdb474b33761d366412 | d903bf04f497ab0dc7f40e9708ed057e4f24c6ee |
| NEXUS ancien port | feat/nex-06a-android-api24 | 374ea2e2fd640e78f2f5e12e60e75b493420e504 | 3acec55616ff8e3b1666091780fca59261377e18 |
| NEXUS finale parent | feat/nexus-final-01 | d903bf04f497ab0dc7f40e9708ed057e4f24c6ee | bbccac2ff2cc052f897c7f5015f234507e047b95 |
| SERVICES port API24 | feat/serv-04a-android-tool-port | f00091a639612b91eca1a301580c8f531249f1e3 | 3decdc47d82f9b43713c48cab244762941770a81 |
| SERVICES finale alternative | feat/services-final-01 | d16dd84f27881460ec9f02d2a54d9ddff23187dc | edfa044321ff09697ae9bec40a6e31aa76a77370 |

Toutes ces têtes distantes correspondent. Une nouvelle tête NEXUS existe depuis le checkpoint initial de l'issue : **9d6928 a réconcilié le port API24 avec la bibliothèque v4**, par adaptation manuelle depuis sa base finale. Elle n'est pas descendante Git du port374, mais contient les sources portables adaptées et schéma4. Ne pas répéter comme blocage actuel que la bibliothèque finale Kotlin n'a jamais été compilée : cette branche fournit désormais preuves JVM et tests de migration. Cela ne qualifie pas FTS5 Android.

SERVICES n'a aucune nouvelle branche FUSION visible dans l'inventaire distant consulté ; le portf000 et finald16 restent divergents depuis3decdc. NEXUSfinald903 et port374 divergent depuis3acec ; la nouvelle9d est enfant de d903 et conserve v4.

## NEXUS actuel : capacités et limites prouvées par code + preuves versionnées

`NexusSchema.CURRENT_VERSION=4`. Métier partagé dans `nexus-core`, stockage JVM/JDBC et backup dans `nexus-jvm-store`, SQLite Android système dans `nexus-android-store` min24/compile35/build-tools35. Kotlin2.0.21, AGP8.7.3, Gradle8.10.2, JDK17, surface propre bytecodeJava8. Pas de JNI/permission/moteurSQLite supplémentaire dans l'AAR. Recompiler les consommateurs, aucune compatibilité ABI binaire générale promise.

Le nouveau `DocumentaryGateway` version1 vérifie callbacks hôte d'autorisation/annulation, deadline monotone, index, byte budget et résolution des citations dans un snapshot SQLite cohérent. CORE reste propriétaire des IDs/session/génération et du contrôle final tardif ; le gateway ne délivre pas de permissions. `RagContextPort` et tous champs Citation restent conservés. Le port de plages incompatible a été renommé `ArchiveRangeSource`, tandis que `ArchiveReader` d'articles est préservé. ZIM Android reste UNSUPPORTED.

Preuves **historiques relues, pas réexécutées ici** :95JVM(92bibliothèque+3adaptateur SERVICES),37Robolectric(API24/25/26/35 simulés), compilation stubsSDK24(1Java+22Kotlin), AAR+deux tests instrumentés compilés mais **0 exécuté**, Lint0erreur/2avertissements de versions de tests. Le test `FusionSnapshotMigrationTest` crée un véritable snapshot AES-GCM d'une fixtureDDL v3, restaure/migre seulement sa copie versv4, résout une citation après réouverture et vérifie inchangés original/archive/base courante. Ce n'est pas une migration utilisateur ni preuve Android.

Dépendance effectivement consommée pour l'extraction JVM optionnelle : SERVICES `fd41d75015f77e947d22d6a60e619adc00bd70b7`, vérifiée par hash d'arbre, **pas** le port Androidf000. Les coordonnées `nexus-jvm-store` et les nouvelles API doivent être portées dans le consommateur CORE séparément.

FTS5 du backend hôte Robolectric est absent : les refus sont testés, pas les citations Android. Aucune instrumentation réelle API24/25/26/29/35 ou ARM64 ; pas de mini-PC physique. Les états Android RAG restent BLOCKED/NOT_RUN jusqu'au vrai probeFTS5/vocab/MATCH/BM25 et scénario citation/reopen sur cible.

## SERVICES actuel : API24 livré, engagement atomique et export manquants

`jarvis.services.inprocess/1`, min24/compile35, AGP8.9.2, Gradle8.13, Java11/JDK17. Le noyau portable partage Store/Task/Data/DocumentTextExtractor/ToolRegistry/ToolDispatcher/ApprovalGate ; dépendancesGson2.11/PDFBoxAndroid2.0.27/BC1.86. L'application historique min26 est distincte. Deux outils readonly : recherche sur pages choisies et normalisation/dédoublonnage CSV, pas un index NEXUS concurrent.

`AccessGuard.Context` copie les grants. `ToolDispatcher.execute` vérifie ce snapshot avant d'appeler l'adaptateur. Il n'existe **aucun callback live CORE `authorizeAtCommit` ni fence atomique au début de l'effet** dans ce port. L'anti-rejeu et le journal UNKNOWN ne résolvent pas cette race d'autorité. Dans ce port, DOCX reste précisément `SAF_EXPORT_UNQUALIFIED` et aucun fichier cible n'est écrit. Les 17 outilsfinaux et leurs tests API26 ne sont pas composés avec le port24.

Preuves historiques :94JVM +40Robolectric, compilation des22sources contreSDK24 ; aucune instrumentation du nouveau port24/25. Finale autonome :129JVM+17AndroidAPI26 rapportés, non réexécutés ici. Journal Storev1 dédié/owner `jarvis.services.android-journal/1`, anti-rejeu4096, fermeture après fin observée, construction échouée libère le verrou, reçus incomplets→UNKNOWN. Aucune garantie d'unloadJNI ni de rollback universel provider.

## CI recontrôlées et limites du diagnostic

- NEXUS374 [40115049468](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/40115049468) : FAILURE. Job android-adapter120934494656, étape4 `Run android-actions/setup-android@v3` échouée ; sdkmanager, tests/build/Lint et boundarycheck ensuite SKIPPED. Aucun artefact Android. Les warnings Node20/Ubuntu26 sont visibles mais **ne prouvent pas la cause**. Log détaillé exige connexion, cause fine UNKNOWN.
- SERVICESf000 [40115305244](https://github.com/bubth720/JARVIS-SERVICES/actions/runs/40115305244) : FAILURE. Job android-build120935248386, setupAndroid/buildAPK/instrumentationAPK/Lint réussissent puis étape9 `SERV-04A Android24 adapter regressions and library` échoue. Annotation exacte `Process completed with exit code 1.` ; compilation boot24 et provenance suivantes SKIPPED. Quel test/erreurGradle précis : UNKNOWN, logs demandent connexion. Les trois artefacts visibles ne prouvent pas le SDK24.
- NEXUS9d : pageActionsfiltrée à la nouvelle branche affiche0runs, étatUNKNOWN/NOT_RUN, aucun échec374 hérité. Son workflow `fusion-01.yml` est workflow_dispatch seulement ; ce fichier n'est pas dans le mainb27 inspecté. La repriseCI n'est donc pas considérée prouvée ni démarrée par cette mission.

Les attributs publics `check-step data-conclusion` et résumés ont été relus ; aucune API contournée ni logs inventés. JSON fournit SHA256 des pages publiques et métadonnées sélectionnées sans jeton/opaque channel. Les corrections de workflows NEXUS/SERVICES appartiennent à leurs propriétaires, pas UNIFIED.

## Gates et licences

GO pilote exige producteurs N/S réellement instrumentés API24 **et25**, trueSAF neuf/readbackSHA sourceinchangée, refus sansconsentement, fencecontrebarrières de révocation avant/aprèsengagement, crash/ACKperdu UNKNOWN durable sansreplay. Aucune preuve JVM/Robolectric ne remplit ces gates. API26 ne qualifie pas24/25. LLM/VOICE ne doivent pas devenir dépendances artificielles de ce pilote.

Aucune licence racine de projet identifiée dans les arbres inspectés : UNKNOWN. Les licences amont et éventuels lecteursZIM ne fournissent pas une licence de distribution du projet. Bibliothèque nativeSQLite externe nécessite autorisation utilisateur distincte ; ne pas l'introduire pour faire vert.

Sources exactes,62+ empreintes, refs/parents/CI et limites structurées : `evidence/nexus-services.json`. MapGit temporaire : `/tmp/fusion02-nexus-services-paths.json`. Ces chemins ne sont pas des livrables publiés ; le propriétaireUNIFIED peut reprendre les données utiles dans son dossierFUSION02.
