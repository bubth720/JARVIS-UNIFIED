# Deux missions prêtes à transmettre après validation

**Missions proposées, non commencées.** Gates préalables : approuver contrat de
convergence et périmètre texte synthétique, choix O3 T1–T5, signatures/fixture et
arbitre. Ne pas redemander l’orientation ADR ; obtenir des accords techniques
et de code propres à chaque dépôt. Pas de fusion, migration, installation sur
appareil ou modification des seuils par autorisation implicite.

## 1 — LLM : adaptateur natif P2 et endpoint de fixture sécurisé

Dépôt unique : bubth720/JARVIS-LLM.
Base recommandée après relecture : mission-003d-p2-core-contract,
**daa46432e847ed9613dc403045498e27281eff42** (code testé : 0f13573).
Nouvelle branche suggérée : `fixture/003e-p2-secure-endpoint`.
Ne pas fusionner automatiquement c4e7611 : comparer ses éléments et leurs versions
identiques déjà présents ; référencer sa preuve séparée dans la documentation.

### Périmètre limité

Créer un endpoint Android **expérimental en fixture isolée**, jamais dans l’APK
historique ou une Activity existante. Requête SYSTEM P2 configurable + question
synthétique, aucun historique/doc/mémoire pour ce premier parcours ; refus si
contexte réel non vide. Préserver la voie legacy et les réponses catalogue, sans
les accepter comme preuve de génération native. Aucun autre moteur/JNI recopié.
Ne pas installer l’APK sur téléphone ; émulateur de test isolé seulement si ce
périmètre est expressément autorisé. Modèles publics déjà disponibles/validés ou
absence de modèle signalée, aucun téléchargement automatique ni poids privés.

### Fichiers existants à relire / adapter seulement si nécessaire

- domain/.../generation/{P2Contract,P2Prompt,P2Lifecycle,Core004BMapping}.kt :
  version/refus, rendu canonique et observation des ressources réelles ; ne pas
  empiler les acquisitions de P2Lifecycle sur ProcessResources.
- domain/.../Conversation.kt et app/.../engine/LlamaBackend.kt : port de comptage,
  cycle de vie, comptage/génération sous worker commun, conservation des baux.
- app/src/main/cpp/bridge.cpp et app/src/main/cpp/tests/jni/NativeBridge.java :
  réutiliser format/template/tokenizer ; exposer mesure complète et preuve de
  modèle/template/rendu au port si nécessaire, tests JNI réels conservés.
- app/src/test/.../NativeBackendLifecycleTest.kt, domain tests generation,
  tools/test-jni-p2.sh : non-régressions et cas de preuve simulée vs réelle.

Nouveaux chemins **proposés** : `fixtures/p2-endpoint/` (module Android opt-in,
manifest/endpoint et tests UID/certificat), `docs/mission-003e/CONVERGENCE.md` et
rapports/manifestes de hashes. Config Gradle/CMake à adapter pour réutiliser les
sources/bibliothèques existantes sans fork/copier-coller ; aucune dépendance à un
APK comme bibliothèque. Résoudre avant build la visibilité internal de NativeApi
par une façade minimale, pas accès réflexif. Ne pas déclarer ces chemins existants.

### Obligations et tests

1. Même clé complète et version contractuelle que la fixture CORE, mapping sans
   perte ; gate d’autorisation refusé par défaut, identité avant contenu/modèle.
2. Rendu unique SYSTEM/question, compteur même template/vocabulaire/BOS/préfill ;
   vide explicite=P2, null/legacy non utilisé pour résoudre une incompatibilité.
   Test512 demandé/768 chargé, profil MAIN invalide, bornes UTF-8 et après composition.
3. Tests worker API simulée pour erreurs/charge partielle/stop/unload et toutes
   assertions de baux ; natif Linux réel via harnais distinct, pas preuve Android.
4. Lifecycle piloté par retours réels, reçus fin/unload exacts ; code JNI non traduit
   par parse de chaîne non fiable. Pas de succès avec nativeDone par défaut.
5. Endpoint seulement dans fixture après O3 validée : composant explicite, identité
   UID/cert, permissions, tailles/rejeux/stale session, versions, mauvais client ;
   tous chemins de fixture participent à l’arbitre retenu. UI historique inchangée.
6. Refus/crash avant/après retour/ACK perdu/cancel répété/status idempotent, aucun
   fallback automatique ; UNKNOWN/CLEANUP_FAILED retiennent la réservation.

Le broker de fixture CORE est livré par la mission2 : pas de dépendance circulaire.
La mission1 fournit le port client du broker et les refus en son absence ; une
fausse autorité n’est permise qu’en test unitaire explicitement simulé. Sans broker
réel, aucun chargement via endpoint et aucune preuve d’admission interprocessus.
La mission2 réalise et teste le broker choisi avant le parcours natif E2E.

### Acceptation et sortie de mission

Tests domaine/app historiques conservés, statut des anciens runs séparé ; nouveaux
rapports avec source SHA et empreinte de contrat/fixture, compilation ARM64 et
émulateur clairement séparés de Linux. Preuve de vrai JNI avec GGUF et pas catalogue,
mais **pas encore preuve CORE↔LLM E2E** tant que la mission2 n’a pas consommé ce
serveur. Matériel physique toujours à qualifier. Livrer endpoint de fixture,
contrat/digest, reçus d’exécution, refus et guide de consommation ; pas de merge.
Si l’identité/arbitre n’est pas approuvée, arrêter avant export du service et livrer
les validations locales restantes sans annoncer l’endpoint sécurisé opérationnel.

## 2 — CORE : client de fixture, session corrélée et mode historique préservé

Dépôt unique : bubth720/JAVIS-Local-v2.
Base recommandée après vérification : mission-004b-core-backend-lifecycle,
**29646448c80568d868a702192df761fc9d7a896d**.
Nouvelle branche suggérée : `fixture/004c-p2-client`.
Dépendances : mission1 livrée avec SHA/contrat/digest/signatures de fixtures,
décisions O3 et arbitre/récupération validés. Pas de modification LLM dans cette mission.

### Périmètre et fichiers

Relire InferenceContract.kt, InferenceController.kt, ProcessInferenceAdmission.kt,
LocalLanguageModel.kt, JarvisCore.kt/PromptBuilder.kt et AppGraph.kt. Préserver
HISTORICAL, sa préparation paresseuse, ses données et API24. Pas de mode de
production activé. Ne pas requalifier DELEGATED_SIMULATOR comme preuve native.

Nouveaux chemins **proposés** : `fixtures/p2-client/`, façade d’adaptation locale
au contrat et tests, `docs/mission-004c/CONVERGENCE.md`/rapports. Module opt-in sans
le Application/warm-up historique. Réutiliser contrats/contrôleur et admission
par façade ou source-set explicitement partagé dans ce dépôt, pas copie divergente
ou import de l’APK comme bibliothèque ; vérifier accès internal à la factory.
Si une modification de port de production est nécessaire, la limiter au mapping
versionné autorisé et garder défaut historique, tests/API24 et app installée intacts.
Pas de nouveau service exporté dans CORE historique : un éventuel broker/callback
choisi O3 vit exclusivement dans la fixture et suit la même revue d’identité.

### Obligations et tests

1. Construire requête clé complète depuis session CORE, SYSTEM exact et question
   synthétique. Table privée correlation↔operation/request/lease/epoch ; aucune
   reconstruction de contexte aplati. Requête documentaire/mémoire refuse tant
   que provenance/révision non représentables ; ne rien supprimer pour réussir.
2. Sur API24–28, fixture LLM non activée et historique conservé ; sur API29+, binder
   authentifié/contrat exact avant appel. Aucun relèvement minSdk CORE.
3. Garder admission process-wide296 : plusieurs contrôleurs/instances directes,
   réservations avant préparation, ancien token, même backend génération nouvelle,
   quarantaine survivant à recréation. Aucun reset de singleton pour rendre vert.
4. Demande d’arrêt, résultat tardif et fin/native/unload distincts. Adaptateur ne
   renseigne nativeDone=true que depuis preuve validée ; retour texte n’autorise
   pas changement de moteur. Unload ACK idempotent lié au bail, aucune libération
   d’une nouvelle session par une ancienne réponse.
5. Mauvaise identité, service absent/tué, client mort, deadline, nettoyage inconnu,
   redémarrage et ACK perdu : aucune nouvelle charge legacy/deuxième moteur avant
   réconciliation. Aucune persistance assistant/TTS après annulation ou réponse
   périmée ; question conservée selon comportement historique.
6. Non-régression187 cas CORE rapportés, incluant140 de004A conservés ; tests
   supplémentaires de mapping et IPC sur émulateur isolé si autorisé. Pas de modèle
   simulé ou de réponse catalogue comme preuve de cette dernière étape.

### Acceptation et preuve finale limitée

Parcours **utilisateur de fixture → CORE → vrai LLM natif → réponse corrélée et
preuve de nettoyage → CORE** dans deux processus, même paire de SHA/contrat et
modèle vérifié, sans connexion Internet. Décrire quel environnement exécute le
natif : Linux n’est pas un test inter-APK Android, émulateur n’est pas le téléphone.
Si modèle/ressources/autorisation absents, livrer tests de contrat/IPC mais marquer
**E2E natif non exécuté**, ne pas l’émuler pour satisfaire le critère.

Les APK de fixtures ne touchent pas l’installation utilisateur, ses signatures ou
profils. Qualification physique et installation sur Redmi/POCO exigent mission et
consentement ultérieurs. Aucun déploiement, fusion, migration ni synchronisation
PC/VOICE/SERVICES introduit pour réaliser ce premier parcours texte.
