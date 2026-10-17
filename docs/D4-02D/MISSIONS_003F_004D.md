# Deux missions proposées :003F puis004D

**Prêtes à transmettre après validation technique et autorisation par dépôt.**
Cette mission D4-02D est documentaire ; aucune des missions ci-dessous n’est lancée.
Décisions V1–V5 de [PROTOCOLE_PROPOSE.md](PROTOCOLE_PROPOSE.md) à valider.
L’orientation ADR-001 est déjà approuvée, pas à redemander. Aucun contrat UNIFIED v1
modifié, aucune fusion main, installation personnelle ou migration autorisée ici.

## Mission LLM003F — preuve fraîche et reprise de l’endpoint

**Dépôt unique :** bubth720/JARVIS-LLM.
Base à vérifier : fixture/003e-p2-secure-endpoint,
`030152a5f3d888017ad7a7fe8026f2e2c48e8fd5` ; code de référence
`5751646acd4a7bb13caaea4b96a4ab3a68ec6adb`, clôture documentaire seulement.
Branche proposée : `fixture/003f-bootstrap-attestation`.
But : livrer un chemin de contrôle attestant les états observables, sans activation
de génération UI et sans faux broker embarqué. Aucun changement CORE/UNIFIED.

### Dépendances et limite de livraison

Validation du protocole proposé, pins/cohorte de laboratoire et politique d’identité.
Les signatures privées restent hors Git ; ne pas créer/re-signer d’installation
historique. Aucun Android physique requis pour les tests de contrat, mais le statut
Binder réel doit rester NON_EXÉCUTÉ sans laboratoire autorisé. Aucun modèle requis
pour le bootstrap propre ; aucun téléchargement automatique de modèle ou outil.

Geler d’abord les tableaux fermés, les AIDL ajoutés en fin et le bundle /2 exact,
vecteurs et diff de compatibilité /1. Ce gel doit être revu conformément à l’accord
technique reçu ; une modification substantielle du présent protocole requiert
nouvelle validation, pas une implémentation permissive. Le SHA/digest livrés par003F
constituent l’entrée immuable de004D. Pas de dépendance circulaire à un broker004D :
les échanges de contrôle sont testables avec harnais explicitement de test, mais
l’absence d’autorité CORE réelle continue d’interdire toute charge en production.

### Fichiers concernés, existants ou proposés

| Chemins LLM | Action limitée |
|---|---|
| fixtures/p2-contract/CONTRACT.txt, src/main/aidl/fr/jarvis/fixture/p2/*.aidl, src/main/java/fr/jarvis/fixture/p2/Wire.kt | Révision expérimentale /2 et négociation ; anciennes ABI/codec/vecteurs /1 conservés comme référence de non-régression ; pas de champ inconnu ignoré |
| fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/FixtureApplication.kt | Autorité unique du processus, registre réel/barrière depuis naissance, distincts du cycle de Service |
| Même dossier : P2EndpointService.kt, EndpointController.kt, AndroidRuntime.kt, Identity.kt, ArbiterConnection.kt | DISCOVER/INSPECT/CHALLENGE/COMMIT et callbacks authentifiés ; aucun accès lourd avant mandat ; stop/drain/unload et baux existants conservés |
| Nouveaux fichiers proposés dans ce dossier : ProcessRecoveryAuthority.kt, RecoveryJournal.kt, RecoveryProtocol.kt | Snapshots synchronisés et journal technique durable, sans deuxième backend ni double acquisition ProcessResources |
| app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt | Seulement si nécessaire : port d’observation minimal de vrais appels/handles/baux sur le worker ; pas d’estimation depuis booléen ou de remplacement du moteur. Si insuffisant, refuser l’attestation plutôt qu’inventer une preuve |
| fixtures/p2-endpoint/src/test/…, fixtures/p2-contract/… tests, tools/check-preservation-003e.py ou nouveau check003f | Tests supplémentaires et conservation des assertions historiques, pas leur désactivation ni nouveau faux runtime de production |
| docs/mission-003f/ et vecteurs synthétiques | SHA, digest, capacités réellement validées, guide004D, traces techniques sans SYSTEM/réponse/URI/secret |

Ces nouveaux noms ne sont pas des fichiers déjà implémentés. Aucun changement à
SafetyPolicy, seuils, profils, ProcessResources, catalogue, chemin legacy, manifest
historique ou minSdk. Les manifestes de fixtures existants ne gagnent pas de nouvel
export non nécessaire ; nouvelle méthode dans services de fixtures déjà protégés.
Pas de moteur concurrent ni acquisition P2Lifecycle empilée sur le backend.

### Tests obligatoires et acceptation

1. B01/B02 sans aucune création native : contrôle frais, autorité process-wide,
   epochs distincts process/service, marqueurs/journaux sains, aucune fausse preuve.
2. B03–B06 et B09–B12 : ancien actif absent, recréation service, challenge périmé,
   ACK perdu, corruption/IO, stop et cleanup échoué. Fichiers originaux conservés ;
   UNKNOWN reste bloquant si l’ancien propriétaire ne peut être résolu.
3. B07/B13 : identité avant unmarshalling et callbacks, paire mixte /1-/2 refusée,
   ABI indices préservés, mauvais digest/UTF-8/champs/nombres/tailles refusés.
4. B14/B15/B16/B18 : tentative de load pendant snapshot, nonce rejoué, clock reboot,
   marqueur absent, queues pleines ; aucune ouverture de barrière ni reset.
5. B08/B17 : distinguer NOT_STARTED et vraie fin native, unload et fsync terminal.
   Backend simulé clairement étiqueté ; conserver le harnais JNI Linux et ses tests
   SYSTEM unique/plafond contextuel sans le déclarer Android. Si pas de GGUF déjà
   disponible/autorisé, noter natif non exécuté, ne pas remplacer par catalogue.
6. Réexécuter suites existantes domaine/app/fixture et contrôles de préservation
   (003E rapporte87+27+19), builds/Lint si environnement disponible, ajouter les
   nouveaux cas sans exiger artificiellement un total historique immuable.

Acceptation : version/digest/vecteurs figés, journal/reçus de reprise sans texte,
preuve uniquement depuis objets réels sous barrière, zéro reset/effacement,
aucun load de production sans CORE, tests et limitations par plateforme/SHA.
Livrer guide consommable par004D et commit publié sur branche dédiée seulement.
Aucune intégration Android E2E revendiquée à ce stade.

## Mission CORE004D — vérificateur et commit de l’arbitre

**Dépôt unique :** bubth720/JAVIS-Local-v2.
Base à vérifier : fixture/004c-p2-client,
`da40ed7155409b85860a22c1dbbfe35029cea29a`.
Branche proposée : `fixture/004d-bootstrap-reconciliation`.
But : remplacer l’absence de fournisseur de preuves par un **vérificateur de
contrôle authentifié**, pas par l’injection d’une RecoveryEvidence optimiste.
Aucun changement LLM/UNIFIED ; pas de génération dans l’Activity durant cette mission.

### Dépendances et périmètre

003F livré/revu avec SHA, bundle /2 exact, vecteurs, transitions et code de refus.
V1–V5 et autorisation de code propres à CORE. La simple publication de003F
n’autorise pas004D. La clé laboratoire commune durable est provisionnée par canal
sécurisé pour une future paire ; les tests isolés ne nécessitent aucun secret réel.
Paquet fixture API29+ seulement ; CORE historique API24 reste intact.

### Fichiers concernés

- fixtures/p2-client/CONTRACT.txt, REFERENCE.json et src/main/aidl/… : reprendre
  exactement le bundle figé003F ; conserver provenance/vecteurs /1, copie /2
  octet-identique, pas de dépendance à un APK LLM comme bibliothèque.
- src/main/java/com/stark/jarvislocal/fixture/{PilotArbiter,AtomicPilotJournal,
  PilotRuntime,Wire,BinderIdentityChecks,P2Session,P2Mapping}.kt : séparer le
  vérificateur de l’entrée de transition locale, génération/high-water mark,
  instantanés de journal, conditions COMMIT/ACK et invalidation des grants.
- Nouveaux fichiers proposés : RecoveryVerifier.kt, RecoveryCoordinator.kt et
  journal expérimental versionné dans le même dossier ; pas de reset de singleton.
- src/main/java/fr/jarvis/fixture/core/P2ArbiterService.kt : entrée contrôle ajoutée
  en fin d’ABI, mêmes contrôles UID/permission avant décodage et callbacks ; aucune
  autorisation depuis query non enregistrée, aucun grant persistant reconstruit.
- FixtureActivity.kt : inspection/diagnostic et demande explicite de cleanup si
  validée, jamais bouton de reset/génération ou preuve de test branchée à production.
- src/test/…, tools/check-004c.py ou nouveau check004d, docs/mission-004d/ : nouveaux
  tests, préservation app/ et suites existantes, guide de paire et preuves techniques.

Le membre local participants={llm} reste la liste de propriétaires natifs admis ;
les deux **attestants de contrôle** core/llm sont vérifiés séparément. Ne pas ajouter
le moteur historical comme candidat réel pour faire réussir un test d’arbitre.
Ne pas modifier app/, ProcessInferenceAdmission historique, données, voix, minSdk,
seuils, prompt ou activation delegated du CORE installé.

### Tests obligatoires et acceptation

1. B01/B02 : demande saine passe au bon IDLE_VERIFIED après deux preuves/ACK
   durables, nouvelle génération strictement croissante, aucun accès lourd.
2. B03/B05/B09/B10/B16 : réservation ancienne sans preuve, journal/marker perdu,
   service/processus mort, ancienne clé différente → RECOVERY_REQUIRED conservé,
   aucun grant ; absence de reset ou de suppression de journal attestée par diff/test.
3. B06/B07/B13/B15 : freshness et identité réelles capturées, mauvais certificat,
   versions/digests, session actuelle vs prior_session, reboot et replay refusés.
4. B04/B08/B11/B12/B14/B17/B18 : pas de double bail ni de texte tardif ; commit
   perdu à chaque frontière, fausse fin/unload, cleanup échoué, deadlocks/IO.
   ReleaseEvidence/RecoveryEvidence ne sont construits qu’après vérification
   typée de toutes obligations ; aucune chaîne JSON qui s’autoproclame RELEASED.
5. Non-régression004C187 historiques +36 fixture rapportés, nouveaux tests séparés,
   codec/vecteurs croisés et préservation app/ ; compilation/Lint si possibles.
   Pas de déduction de physique ou d’E2E depuis Robolectric/JVM/compilation.

Acceptation : journal ancien préservé, aucun IDLE sans preuve fraîche et commit,
pas d’allocation dans bootstrap, refus sûr d’une paire incompatible/absence LLM,
ancien processus irrésolu reste bloqué, mode historique inchangé. Livrer traces
B01–B18 avec plateforme/SHA et cas NON_EXÉCUTÉS, pas un compteur sans couverture.
Si un laboratoire Android est ensuite autorisé, commencer par bootstrap des deux
APK **sans modèle**, puis protocole séparé de qualification JNI ; ne rien installer
ni déclencher de génération réelle sous la seule autorisation de004D.

## Bilan D4-02D et suite immédiate

Branche documentaire : `design/d4-02d-bootstrap-recovery`, base0dbb978.
Fichiers livrés : BOOTSTRAP_RECOVERY.md, PROTOCOLE_PROPOSE.md,
TESTS_ET_PREUVES.md et ce document, plus lien README. Le SHA final et la
vérification de publication sont fournis au compte rendu après commit ; aucun
SHA auto-référent inventé. Pas de PR/merge demandé.

Blocages restant avant implémentation : approbation V1–V5, gel du contrat /2,
provisionnement privé de paire et disponibilité du laboratoire pour une preuve
Binder réelle. Après mort non résolue/corruption, le blocage peut être définitif
pour cette paire sans procédure distincte : c’est une limite explicite de sûreté,
pas une raison d’effacer le journal. La première exécution propre est réalisable
sans prétendre récupérer une ancienne réservation sans preuve.

Ordre recommandé : valider ces choix → autoriser003F → revoir SHA/digest/tests →
autoriser004D → examiner la paire avant toute autorisation de test Android réel.
Aucune mission supplémentaire n’est lancée ; aucune nouvelle version automatiquement
approuvée. Résultats UNIFIED réellement exécutés dans
[TESTS_ET_PREUVES.md](TESTS_ET_PREUVES.md).
