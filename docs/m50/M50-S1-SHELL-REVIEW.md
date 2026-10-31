# M50-S1 B — revue de faisabilité, pas de réalisation

État: REVIEW_ONLY. Aucun code runtime, manifeste, source Gradle ou contrat historique changé. Aucun assemblage, APK, test Android ou installation effectué par cette revue. Lot B attend les preuves A1/A2/A3.

## Sources revérifiées
- CORE mission: d754a6c19e3c94e415e8506d0d37b8d943951d88, tree 8d22a663574c611fa108f9656f6dd285083a6f71. AGENTS.md lu; obligations de préservation applicables.
- INTERFACE mission: 3a0841266fd691b74fae784004804429e6e2e219, tree 9c0f615aa9d8795bd376cd0bbe922d8333acb130. Aucun AGENTS.md dans arbre complet.
- Les sept fichiers précis proposés, leurs modes et blob SHA sont dans M50-S1-SOURCE-SELECTION.json. Ils totalisent environ 34 KiB; pas d'import massif, pas d'historique déplacé. Les copies restent dans l'espace temporaire CI.

## Compatibilité observée
CORE: Kotlin2.0.21, AGP8.7.3, JDK17, Gradle8.10.2, coroutines1.9.0, compile/target35, min24, application historique arm64-v8a.
INTERFACE: Kotlin2.1.20, AGP8.9.2, JDK17, wrapper Gradle8.13 SHA256 20f1b1176237254a6fc204d8434196fa11a4cfb387567519c61556e8710aed78, coroutines1.10.2, compile/target35, min26, aucun moteur natif.
Aucun changement à ces versions historiques. L'assemblage de sources Kotlin dans un module lab autonome peut utiliser l'outillage UI plus récent et les mêmes coroutines UI, avec compile/target35, min29. Cette compilation croisée doit être réellement vérifiée; la lecture ne la prouve pas. Aucun JNI et aucune ABI native ajoutés; émulateurs x86_64 API29/35 possibles.

## Licences/provenance
Les arbres complets CORE/UI ne contiennent aucune licence de projet LICENSE/COPYING/NOTICE; CORE ne contient qu'une licence Qwen pour un modèle exclu de la coquille. Il faut donc qualifier explicitement les droits de distribution/SBOM/lock pour G1 avant une diffusion de produit. Cela ne modifie aucune licence et n'interdit pas à lui seul la compilation temporaire privée explicitement autorisée par S1 par le propriétaire utilisateur. Aucun poids, asset privé ou bibliothèque native ne doit entrer dans le labo. Les sources propriétaires doivent conserver attribution SHA/repo/blob et ne pas être relicenciées implicitement.

## Assemblage minimal proposé après A
Un module Android indépendant fr.jarvis.lab.m50s1, android:testOnly=true, allowBackup=false, sans permission, sans service/provider/receiver, une Activity MAIN/LAUNCHER uniquement. Aucun certificat historique réutilisé ni nouvel IPC; signature debug éphémère de build de labo, jamais présentée comme authentification CORE.
Source sets générés par un script SHA-pinné dans RUNNER_TEMP, sans AppGraph, JarvisApplication historique, MainActivity historique, stockage, NEXUS, Services, TTS, Whisper ou LLM.
Compiler ensemble:
1. CORE SessionCoordinator.kt + Models.kt + events/CoreEventBus.kt + events/CoreSessionEvents.kt.
2. UI CoreEventUiPort.kt (types metadata), core/CoreConversationTransport.kt et core/CoreConversationClientAdapter.kt.
3. Nouveau adaptateur de laboratoire dans le même module/package CORE pour SessionActions et constructeur internal, sans modifier la visibilité historique.
4. Nouvelle Activity de laboratoire qui projette réellement CoreConversationClientAdapter.state; contrôles tactile Submit/Stop et statut permanent LAB/SYNTHETIC. Aucun nouveau coordinateur.

Un nouveau écran simple Views est préférable au réemploi de ChatScreen.kt entier: ce dernier entraîne Composer/diagnostics/workspace/DocumentSource et parle d'aucun CORE connecté. Les trois classes UI proposées réemploient le vrai client de conversation qui gère ACK/chunks/Stop/UNKNOWN, sans remonter le graphe applicatif complet.

## Adaptateur in-process concret
- Une seule instance SessionCoordinator, un seul CoreEventBus RAM activé par opt-in de labo, un CoroutineScope propriétaire du processus; aucun moteur réel.
- SessionActions.prepare ne charge rien. chat retourne uniquement un ChatMessage synthétique dont chaque chunk est préfixé LAB/SYNTHETIC; aucune question/document reflété dans logs.
- CoreConversationTransport.origin reste LABORATORY; ses états READY ne sont que disponibilité du port synthétique, jamais LLM_READY ni identité CORE de production.
- submit refuse doublon submissionId/UNKNOWN/busy et appelle uniquement coordinator.send. L'ACK est corrélé au premier UserInput du CoreEventBus (session/request/generation réels du coordinateur), jamais inventé par UI comme lease JNI.
- Les chunks synthétiques émis par SessionActions.chat utilisent le ContentKey corrélé et une séquence locale bornée, puis Completed/Cancelled/Error dérivés des vrais événements CORE. Un petit buffer pré-ACK couvre le démarrage concurrent.
- stop vérifie clé/session/génération, signale l'arrêt synthétique coopératif et appelle coordinator.cancelCurrent. Le verrou CORE ne se libère qu'au retour de son travail NonCancellable; aucune preuve native alléguée.
- RESOURCE_UNCONFIRMED -> UNKNOWN bloquant. Flux interrompu, ACK perdu, erreur drain ou arrêt non confirmé -> UNKNOWN; aucun retry silencieux.
- Tout état et message restent RAM. Rotation conserve l'unique session via propriétaire processus/ViewModel et recrée seulement la vue; force-stop efface RAM et crée nouvel epoch au relancement. Ne jamais restaurer une session UNKNOWN depuis la UI.
- Statuts fixes: LLM UNAVAILABLE, NEXUS UNSUPPORTED, SERVICES READ_ONLY/UNSUPPORTED, VOICE OFF, EVOLUTION OFF.

## Validation requise, actuellement NOT_RUN
JVM tests de l'adaptateur: nominal ACK/chunks/completed; stop; refus double-submit; replay event/ACK; clé/génération périmées; absence de modèle; timeout->UNKNOWN; close/callback tardif.
CI build: assembleDebug, testDebugUnitTest, lintDebug, assembleDebugAndroidTest avec versions figées; inspecter manifeste fusionné et APK aapt/apkanalyzer, testOnly/appId/minSdk29/aucune permission/aucune lib native/aucun asset modèle, SHA256 APK.
Instrumentation API29 et35: lancement; échange synthétique marqué; stop; replay; rotation avec même coordinateur; vraie force-stop/reprise par script adb externe à instrumentation; réseau coupé/mode avion; aucun log de texte/URI/chemin privé. Nouvelle Activity ne déclare aucune permission et ne demande rien.
Publier XML et comptes réels par API, captures synthétiques et run/HEAD; un build sans instrumentation ne qualifie pas G2/G7.

## Décisions/STOP
- Pas de décision sensible nécessaire pour cette proposition de sept copies temporaires en CI déjà autorisée par S1, sous réserve preuves A.
- STOP si davantage de sources/graphes complets doivent être importés, si un nouveau JNI/ABI/permission/transport/signature de production/licence doit être modifié.
- Clarifier les licences avant lock approuvé ou distribution de produit; G1 reste PARTIAL/BLOCKED.
- Appareil physique G8 NOT_RUN sans accord distinct.
Rollback: fermer PR/retirer le module de labo et supprimer RUNNER_TEMP; aucun changement original, schéma, modèle, base ou donnée personnelle.
