# Évolution expérimentale : défi, preuves et commit de réconciliation

**PROPOSÉE, NON APPROUVÉE ET NON IMPLÉMENTÉE.** Ce texte ne change aucun schéma
UNIFIED v1, ni l’ADR, ni CONTRACT.txt des dépôts sources. Il propose une évolution
**du seul contrat de fixture jarvis.fixture.p2/1 vers jarvis.fixture.p2/2**.
Le nom /2 est réservé ici pour la proposition ; aucune compatibilité acquise.
Les contrats de domaine jarvis.llm.p2/1.0 et engine/1.0 restent distincts.

## 1. Négociation : jamais de downgrade silencieux

/1 reste figé : bundle canonique SHA-256
`fab6a66a6b99302884849cd1d8aef97cd761082dc20680a4b036d7bc99d5c3c9`.
Ses hello/status et codecs fermés ne savent pas négocier les nouveaux champs.
Ajouter des champs à hello /1 ou accepter /2 comme un /1 serait incompatible.

Proposition d’ABI pour implémentation après accord : conserver les indices et
signatures des quatre méthodes IP2Endpoint existantes, **ajouter en fin** une
entrée `recovery(in byte[] message, IBinder peerLiveness, IRecoveryCallback callback)`.
Ajouter en fin d’IP2Arbiter une entrée de contrôle équivalente pour les messages
endpoint→CORE ; pas de déplacement de authorize, pas de nouvel export historique.
IRecoveryCallback est une interface dédiée avec complete(byte[]) ; traitements
asynchrones/bornés, UID vérifié à chaque entrée/callback avant désérialisation et
dispatch. Les frontières et limites Parcel de003E/004C restent exigées.
Les noms sont proposés, aucun fichier AIDL généré dans cette mission.

Premier message DISCOVER, sans autorité ni capacité de génération : objet fermé
`kind, version, contract, pilot_id, session_id, round_id, nonce` où kind=DISCOVER,
version=/2 et contract=empreinte **pré-épinglée de la révision exacte /2**.
Il s’agit d’une offre unique, pas d’une liste permettant un choix opportuniste.
Réponse NEGOTIATED = écho exact + `code, endpoint_epoch, llm_process_epoch,
llm_service_epoch, core_process_epoch, broker_epoch` ; code=NONE uniquement si
l’autre paire connaît exactement la même révision et identité. Le transport
réel et le nonce authentifient ce retour, pas le contenu d’un ancien fichier.

Un /1 qui ne connaît pas la transaction supplémentaire répond UNKNOWN_TRANSACTION
ou échoue : **RECOVERY_UNSUPPORTED et admission bloquée**. Aucun repli hello→preuve,
aucun test submit pour découvrir la version. /2 inconnu, digest différent,
capacité manquante, JSON inconnu → INCOMPATIBLE, sans effet journal ni natif.
Une révision /2 approuvée devra inclure CONTRACT.txt+AIDL **et les tables fermées
normatives de cette révision** dans le bundle canonique ; chaque paire génère le
même vecteur. L’empreinte /2 n’est pas calculable avant ces fichiers et n’est pas
inventée ici. Elle doit être gelée et approuvée avant consommation par CORE004D.

## 2. Identité et périmètre de confiance

Pins issus du provisionnement autorisé, jamais d’une réponse réseau/JSON :
pilot_id, deux packages/components de fixtures, certificat courant unique commun,
UID Android résolu et lié à chaque package, version/digest et paire de builds.
UID capturé par Binder.getCallingUid **dans le thread de transaction**, avant
clearCallingIdentity/dispatch. Package unique, permission signature et propriétaire
de permission vérifiés ; shared UID, plusieurs signataires, rotation et mauvais
certificat refusés comme003E/004C. Mise à jour de package invalide le tour et exige
revue des pins, pas de confiance automatique en version annoncée dans le corps.

Les deux sens exigent une transaction/callback originaire du pair attendu.
Les champs UID/certificat sont des échos contrôlés contre ces faits Android,
pas des faits issus du client. Un résultat synchrone ou un IBinder relayé n’ajoute
pas une autorité : callbacks authentifiés, liaison explicite et défi corrélé.
Nonce n’est ni secret ni preuve cryptographique de RAM ; checksum/digest ne sont
ni signature ni protection contre OS/paire compromise. Clé de signature des APK
hors Git, aucune nouvelle clé privée transmise au protocole.

## 3. Types et messages fermés proposés

Même codec de base : UTF-8 strict, objet plat de chaînes, refus des champs inconnus,
dupliqués/manquants, trailing data et nombres JSON natifs. Contrôle <=24Kio/corps,
<=32Kio/transaction ; borner aussi la sortie, nombre d’appels et appels simultanés.
Un seul tour de récupération actif ; refus BUSY aux autres, sans file non bornée.
Hash canonique de003E : uint32BE nombre de champs, clés triées puis longueurs et
UTF-8 exacts, sans normalisation Unicode. Digests SHA-256 minuscules64hex.

UUID canoniques minuscules pour identifiants/epochs. nonce =32 octets
SecureRandom, base64url sans padding (43 caractères avec décodage canonique vérifié),
jamais UUID ou timestamp comme source de fraîcheur suffisante. Génération
0..9007199254740991 pour état sans opération ; une opération conserve1..max.
Séquences journal monotones bornées, jamais remises à0 après récupération.

Les groupes ci-dessous sont des **ensembles de champs**, développés en clés plates,
pas des sous-objets JSON ou listes sérialisées non validées. Un tableau de champs
exact par kind sera intégré dans la révision /2 à geler par003F.

| Groupe | Champs obligatoires / sens |
|---|---|
| R — ronde | version, contract, kind, pilot_id, participant_set_digest, session_id, round_id, recovery_id, nonce, issued_elapsed_ms, expires_elapsed_ms |
| I — identités | core_uid, core_cert_sha256, llm_uid, llm_cert_sha256, core_process_epoch, broker_epoch, llm_process_epoch, llm_service_epoch, endpoint_epoch ; packages/components épinglés dans le contrat |
| J — lecture durable pour chaque pair | core_journal_id/seq/state/sha256, llm_journal_id/seq/state/sha256, generation, owner ; owner=NONE ou llm |
| K — opération antérieure | prior_key_state=NONE ou PRESENT ; si PRESENT, les7 UUID de clé /1 préfixés prior_ + prior_generation + prior_request_digest ; aucun UUID fictif si NONE |
| O — observations du participant | participant=core ou llm, barrier_id, backend_registry_state, queue_state, native_state, residency_state, lease_state, observation_seq, backend_count, active_native_calls, queued_operations, active_imports, resident_models, heavy_leases, resolution_kind, terminal_receipt_sha256 |
| D — transaction | decision_id, prepare_set_sha256, decision_sha256, predecessor_journal_sha256, prepared_journal_seq, prepared_journal_sha256 |

R.session_id est la session de **contrôle actuelle**. L’ancienne session reste
prior_session_id ; endpoint_epoch actuel n’écrase jamais prior_epoch. generation
est le high-water mark durable de la cohorte, pas un nombre proposé par un ancien
client. participant_set_digest désigne exactement les deux rôles de fixture avec
les pins : pas suppression d’un pair absent pour compléter le tour.

Messages après NEGOTIATED :

| kind | Champs / effet permis |
|---|---|
| CHALLENGE | R+I+J+K ; CORE enregistre attente et barrière, exige snapshot LLM correspondant à la lecture J ; aucune charge |
| ATTEST | R+I+J+K+O+prepared_journal_seq+prepared_journal_sha256+predecessor_journal_sha256 ; LLM écho exact, observation locale et état PREPARED durable. decision_id et prepare_set_sha256 sont seulement introduits par COMMIT ; aucun champ D implicite |
| COMMIT | R+I+J+K+decision_id+prepare_set_sha256+decision_sha256 ; lie les deux preuves et décision CORE déjà durable ; n’est pas un mandat natif |
| COMMIT_ACK | Même transaction/digests + état et seq/hash du journal local après commit ; aucun texte ni booléen de génération |
| INSPECT | R+I+recovery_id+clé antérieure complète ou NONE ; inspection de journal/opération même sans active en RAM, jamais relance submit |
| SNAPSHOT | Écho INSPECT + J+K+O + code ; observation fraîche, pas permission de libérer en elle-même |
| CLEANUP_REQUEST | R+I+K+cleanup_command_id ; demande explicite sur propriétaire existant, seulement si fin native positivement connue ; pas de load/import/prepareOperation |
| REFUSED | version, contract, kind, round_id, nonce, code ; état conservateur, aucun effet positif ; authentifier avant de lire même un refus |

ATTEST n’affirme un état vide que si O est intégralement connu :
barrier fermée, registry COMPLETE, queue EMPTY, native NOT_STARTED ou
NATIVE_RETURNED, residency NO_RESIDENCY_CONFIRMED, lease NONE. active_native_calls,
queued_operations, active_imports, resident_models et heavy_leases sont tous0,
observés et non fournis par défaut. backend_count est0 ou1 avec état complet connu ;
un backend vide peut exister sans modèle résident. Comptage incomplet = UNKNOWN,
pas0. Ces compteurs concernent exclusivement le registre instrumenté du processus.
resolution_kind
vaut INITIAL, CLEAN_RESTART, TERMINAL_REATTESTED ou CLEANUP_RETRY_COMPLETED.
terminal_receipt_sha256 vaut NONE uniquement quand aucune ancienne opération
n’était admise ; sinon hash d’un vrai reçu sans texte. UNKNOWN/CLEANUP_FAILED,
queue non vide ou backend orphelin donnent SNAPSHOT/REFUSED, jamais ATTEST positif.

**Point de gel obligatoire :** ces groupes et conditions sont la spécification
proposée ;003F livre les tables exactes/vecteurs avant toute implémentation client.
Pas d’acceptation permissive d’un « champ facultatif » pour compenser une divergence.
Les types O remplacent la confusion entre NATIVE_RETURNED et NOT_STARTED : un
reçu initial sans calcul ne prétend ni native_ever_started=true ni réponse native.

## 4. Expiration et anti-rejeu

CORE tire un nonce neuf pour chaque tour et l’enregistre avec les incarnations,
snapshots J et phase attendue **avant l’envoi**. Proposition de fenêtre contrôle :
5s maximum, à qualifier, distincte du budget génération90s et sans changement de
seuil matériel. Un timeout laisse les barrières fermées ; pas de retry positif.
Chaque pair vérifie sa réception dans la fenêtre et sa propre borne monotone,
les échos exacts et l’état local inchangé. Les deux processus sont sur le même
Android vivant : elapsedRealtime partagé ; ne jamais comparer une ancienne deadline
persistée à une horloge remise à zéro après reboot. Le reboot détruit les canaux :
nouvelle négociation/epochs/nonce et relecture durable obligatoires.

Le callback doit aussi être rattaché à la même liaison Binder authentifiée et aux
incarnations épinglées de la ronde ; un corps qui annonce un autre processus est
refusé. Les PID éventuels restent diagnostics et peuvent être indisponibles pour
une transaction oneway : aucune déduction de sûreté depuis getCallingPid.

nonce/round_id consommés atomiquement à la première transition positive.
Réception doublonnée n’ouvre rien ; COMMIT/ACK peuvent seulement re-confirmer
la même décision déjà durable et liée aux mêmes digests. Même clé avec payload
différent = REPLAY_CONFLICT. Stockage borné non évictable des high-water marks /
décisions nécessaires ; saturation = blocage, pas oubli autorisant un replay.
Après expiration ou nouvelle incarnation, tour frais obligatoire : les anciens
reçus sont **des éléments d’historique à re-attester**, jamais des attestations
courantes réutilisables. Une session renouvelée ne remet pas la génération à0.

## 5. Transition durable, sans fenêtre d’allocation concurrente

États CORE proposés : BLOCKED → INSPECTING → PREPARED → COMMIT_DURABLE
→ IDLE_VERIFIED. Pannes : RECOVERY_REQUIRED/JOURNAL_BLOCKED.
États LLM proposés : RECOVERY_BLOCKED → QUIESCENT_PREPARED → RECOVERY_COMMITTED.
Les états d’opération003E demeurent distincts ; aucune transformation directe
UNKNOWN→UNLOADED par réception de message.

1. CORE bloque toute nouvelle réservation/GrantRegistry, lit sans réinitialiser
   son historique et celui de LLM via INSPECT ; les deux gardent leurs barrières.
2. Si en cours : procédure de drain/cleanup, puis nouvelle inspection. Si inconnu
   non résoluble ou journal corrompu : arrêt sûr. Si propre : préparer R/I/J/K,
   persister tour et propre preuve CORE, envoyer CHALLENGE.
3. LLM compare les préconditions, inspecte sous l’autorité de processus, persiste
   QUIESCENT_PREPARED **avec l’ancienne réservation toujours référencée**, puis
   ATTEST. Les empreintes de snapshot portent sur les états précédant PREPARED ;
   les champs prepared_* décrivent le nouvel enregistrement. Aucun hash auto-référent.
4. CORE vérifie l’attestation et son propre snapshot sous barrière, compose les deux
   preuves triées core/llm, persiste COMMIT_DURABLE puis envoie COMMIT. La décision
   contient ancienne clé/issue, high-water mark, hashes des preuves et journaux.
5. LLM compare décision/prepared/incarnations/fenêtre, persiste la résolution et
   son ACK sans effacer le prédécesseur ; renvoie COMMIT_ACK. Il ne peut toujours
   pas charger : il attend une autorisation **nouvelle** liée à decision_id.
6. CORE authentifie/vérifie tous les ACK, persiste IDLE_VERIFIED avec dernier bail
   résolu et génération conservée. Seulement alors une nouvelle requête peut
   réserver génération+1, clé neuve et mandat réel. Chaque grant /2 ajoute
   decision_id et les incarnations vérifiées à la query/écho autorisé ; endpoint
   doit retrouver sa décision durable et sa barrière, et refaire les contrôles
   matériels. La preuve consommée n’est jamais rejouée comme nouveau mandat.

Après commit réussi, l’état de décision est une **base durable d’admission**, pas
une attestation réutilisable. Elle ne reste applicable que tant que canaux/identités/
incarnations et barrières n’ont pas changé et qu’aucune réservation inconnue n’est
survenue. Rupture = RECOVERY_REQUIRED. Après chaque travail, reçu réel et journal
terminal restent obligatoires ; pas de réconciliation intégrale périodique au repos.

Crash après n’importe quelle écriture : aucun IDLE déduit de son absence.
ACK perdu : INSPECT peut constater la décision sans refaire une génération ; si
la fenêtre est expirée, nouveau tour frais lié à la décision historique et deux
snapshots actuels. Écriture COMMIT impossible = blocage, même si LLM est réellement
vide. Pas d’ouverture LLM anticipée sur COMMIT reçu ; ne jamais attendre un ACK
à la sortie d’un verrou retenant le worker/Binder distant. Ordre de verrous,
queues bornées et appels asynchrones devront être testés en003F/004D.

## 6. Journaux, quarantaine et limites irréductibles

Proposition de journal privé de fixture versionné : identité cohorte/processus,
format/version, seq monotone, hash prédécesseur, dernier commit commun, clé/digest
et obligation pendante, états préparés/décision/ACK. Aucun prompt/réponse/URI/audio,
secret ou profil. Empreinte technique ne doit pas inclure du texte personnel.
Écritures atomiques/fsync et contrôle d’intégrité ; échec interdit une preuve
positive. Le marqueur de cohorte et la séquence de journal sont distincts d’une
simple valeur SharedPreferences unresolved=false ; clé absente et erreur de
lecture ne sont pas assimilées à un journal sain. Checksum/chaîne non authentifiée ne résistent pas au rollback malveillant.

Lire les journaux /1 sans les altérer, conserver les originaux ; évolution interne
écrite dans un nouveau journal de fixture avec référence/hash au prédécesseur,
jamais interpréter clé/receipt absent comme « propre ». CORE AtomicPilotJournal
v1 conserve generation/lastReleased mais pas tous les digests ; LLM SharedPreferences
ne suffit pas à exporter un historique complet/contrôlé. Si les données /1 ne
suffisent pas, rester bloqué ; pas de migration des données utilisateur ou du CORE
historique. Erreur/corruption v1 interdit de fabriquer un journal /2 propre.
La gestion des .bak/.new et des écritures interrompues doit être explicitement
validée, pas seulement le fichier principal. Pas de garbage collection d’une
preuve non acquittée ; archives techniques de fixture préservées pour diagnostic.

Le protocole ne fournit pas de preuve OS de mort du propriétaire. Ancien processus
avec réservation non résolue et sans reçu durable : UNKNOWN persiste, même si le
nouveau processus s’inspecte vide. Autoriser cette sortie demanderait un mécanisme
de confiance séparé et une validation ultérieure, jamais un simple nouveau nonce.

## 7. Décisions à soumettre, pas prises ici

- V1 : adopter l’évolution expérimentale /2, ses tables fermées et son nouveau
  digest ; garder /1 figé et refuser les paires mixtes.
- V2 : accepter l’attestation logicielle bornée, l’autorité de processus/barrières
  et le périmètre exact des deux fixtures, sans garantie mémoire Android absolue.
- V3 : enrôlement de laboratoire explicite, pins/cohorte et journaux de fixture
  conservateurs ; pas de réenrôlement automatique après perte/corruption.
- V4 : commit durable avec ACK et fenêtre contrôle proposée5s à qualifier ;
  CLEANUP_REQUEST explicite et UNKNOWN maintenu si preuve manquante.
- V5 : autoriser séparément003F et004D après gel de contrat ; qualification et
  installation réelles demeurent des autorisations distinctes.

Aucune de ces décisions n’approuve automatiquement O3 ni un déploiement.
