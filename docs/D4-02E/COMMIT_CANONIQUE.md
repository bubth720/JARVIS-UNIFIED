# COMMIT canonique — révision proposée D4-02E.1

**Non approuvée, non implémentée dans CORE/LLM.** Aucun digest candidat antérieur
n’est adopté. Formule remplace l’engagement opaque constaté dans003F ; elle relie
les deux preuves complètes et leurs rôles sans autoréférence.

## Encodage exact et séparation de domaines

Tous les messages/proofs sont objets plats de chaînes UTF-8 strictes, champs/enums
fermés. IDs/nombres/nonces restent ceux de /2. Refuser doublons et types JSON faux.
C(M) = uint32BE(nombre de champs), puis pour chaque clé ASCII triée croissante :
uint32BE(taille UTF-8 clé), clé, uint32BE(taille UTF-8 valeur), valeur.
Aucune normalisation Unicode ; é et e+accent combinant ne sont pas identiques.

H_L(M)=SHA256(ASCII(L) || octet00 || C(M)), hex minuscule64. Labels exacts :

- c = H_jarvis.fixture.p2/2.core_prepare.D4E1(CORE_PREPARE)
- l = H_jarvis.fixture.p2/2.llm_attest.D4E1(ATTEST)
- p = H_jarvis.fixture.p2/2.prepare_set.D4E1({core_prepare_sha256:c,llm_attest_sha256:l})
- d = H_jarvis.fixture.p2/2.decision.D4E1(COMMIT **sans decision_sha256**)

COMMIT contient c,l,p,decision_id et **les deux preuves complètes** core_prepare_b64,
llm_attest_b64 ; decision_sha256=d est ajouté après le calcul. Aucun champ de preuve
ne contient le hash du COMMIT ; aucun prepared record ne contient son propre hash.
Les quatre formules utilisent C, pas l’ordre d’insertion ni le JSON pretty-print.

b64 = base64url sans padding de JSON UTF-8 canonique restreint : clés ASCII triées,
separateurs ',' et ':', sans espaces, UTF-8 non-ASCII direct, guillemets/backslash
échappés comme JSON, contrôles refusés dans ces preuves techniques. Decoder vérifie
borne, absence doublon, UTF-8 et ré-encodage octet-identique. Une représentation
JSON équivalente mais non canonique n’est pas acceptée dans les champs b64.
Pas de listes ni objet imbriqué dans une preuve. Au plus6144octets décodés par
preuve,8192 caractères b64, corps total24576octets/Parcel32768. Bornes contrôlées
avant allocation/décodage ; preuve dépassée = INPUT_TOO_LARGE, pas retrait de champs.

## Vérification : pas simplement recalculer des hashes

1. Authentifier canal/callback, version/digest exacts, session/incarnations, nonce,
   fenêtre et barrière. Récupérer les preuves conservées localement depuis le tour
   courant, pas depuis un répertoire d’exemples ou le seul corps COMMIT.
2. Valider les tables fermées CORE_PREPARE/ATTEST, rôles core/llm respectifs ; toutes
   identités et R/I/K/génération/owner communs égaux. CORE_PREPARE ne contient pas
   J_LLM ; ATTEST lie J_CORE comme écho et J_LLM comme déclaration du LLM.
3. Vérifier core_prepare_sha256 d’ATTEST=c ; les champs communs de CHALLENGE et
   ATTEST sont égaux ; CORE_PREPARE est celui reçu de CORE dans CHALLENGE ; ATTEST
   est exactement celui produit/conservé par LLM, ou reçu/authentifié par CORE.
   prepared_journal_seq/hash et predecessor_journal_sha256 restent propres à leur
   participant, jamais confondus malgré leurs noms identiques.
4. Recalculer c,l,p,d ; vérifier présence des deux membres, pas p arbitraire. Changer
   une preuve, inverser les rôles, omettre un membre, changer l’ancienne clé ou
   réutiliser une tête de journal est refusé, même si l’attaquant recalcule tous
   les hashes : la comparaison à la preuve locale/canal reste indispensable.
5. Vérifier qu’aucune observation/écriture inattendue n’a eu lieu sous barrière.
   queue native/import vide et absence résidence attestées par F3 ou registre de
   naissance qualifié, pas par cette algèbre. Le COMMIT n’est pas un grant natif.

## Graphe d’enregistrements durable, sans hash auto-référent

Chaque journal possède id/seq, prev_record_sha256, phase et payload canonique ;
son format de bytes exact doit être figé/testé dans le prochain bundle LLM.
Proposition pour le calcul interop du record : H_jarvis.fixture.p2/2.record.D4E1
sur {journal_id,seq,prev_record_sha256,phase,payload_b64}. Le hash n’appartient pas
à ces champs. Premier prev_record_sha256=NONE est réservé à l’enrôlement autorisé.

1. CORE persiste PREPARED : observation propre + snapshot LLM référencé + tour,
   sans CORE_PREPARE ni hash de cette preuve. Après fsync fichier et répertoire,
   calculer sa tête, construire CORE_PREPARE qui la cite. Conserver cette preuve
   dans un outbox durable distinct, puis envoyer CHALLENGE avec cette preuve.
2. LLM compare tête attendue/J, persiste PREPARED lié au CHALLENGE/digest c, puis
   construit ATTEST citant ce record. Persister un ATTEST_OUTBOX distinct contenant
   la preuve exacte avant callback. Sa tête est différente du record PREPARED
   cité ; la précondition attend cette progression exacte, pas une égalité naïve
   last.sha==prepared.sha après l’outbox.
3. CORE vérifie les deux preuves, persiste DECISION_OUTBOX avec le COMMIT complet
   et d ; enregistrement propre sans hash de soi. Aucun IDLE. Envoyer COMMIT.
4. LLM vérifie l’appartenance, sa preuve/outbox et dernière tête attendue ; persiste
   COMMITTED avec d,p,c,l,identifiants/issue et prédécesseur, sans ACK. Calculer tête
   COMMITTED après fsync ; construire ACK citant committed_journal_seq/hash.
5. LLM persiste ACK_OUTBOX exact dans **un autre** record avec lien au COMMITTED,
   fsync fichier/répertoire, puis callback ACK. L’ACK cite COMMITTED, pas ACK_OUTBOX.
   Échec de l’outbox = aucun ACK positif, même si COMMITTED est déjà durable.
6. CORE vérifie callback/ACK et décision exacte, persiste FINALISED avec les deux
   références durables. Seulement ensuite IDLE_VERIFIED ; barrière LLM n’autorise
   toujours aucun load sans nouveau mandat/génération supérieure validé séparément.

À chaque étape : temporaire créé sans écraser original → données fsync → publication
atomique → répertoire fsync → tête publiée de même manière ; ACK seulement quand
tête et chaîne sont durables. Les .pending/.bak incohérents sont conservés et
bloquent ; aucun nettoyage automatique comme preuve. Format exact, phases,
capacités d’AtomicFile/fsync et plateformes à tester dans LLM ; pas promesse d’une
atomicité distribuée instantanée. Réserver le nombre de records nécessaires avant
PREPARED, conserver caps512records/128tours : si insuffisant, JOURNAL_BLOCKED/QUEUE_FULL,
pas éviction ni augmentation silencieuse des plafonds.

## ACK perdu, redémarrage et égalités

Même COMMIT vivant/frais et mêmes preuves/digests : renvoyer le même ACK durable,
sans append concurrent inutile et sans deuxième résolution. Outbox présente mais
corrompue : blocage, pas reconstruction d’un ACK à partir de valeurs absentes.
Une panne entre COMMITTED et ACK_OUTBOX peut reprendre la construction du même
ACK depuis le COMMITTED exact, mais sa durabilité doit être obtenue avant réponse.

Après expiration/nouvelle incarnation : ancien ACK et ancienne attestation ne
rouvrent rien. INSPECT neuf peut décrire la décision historique ; nouveau défi et
deux preuves actuelles, nonce neuf et lien à l’ancienne décision. Aucune relance
submit, nouvelle génération lourde ni remise à zéro du journal pour récupérer.
La clé ancienne reste entière ; corruption/fin inconnue/décès sans preuve terminale
conserve UNKNOWN. Les effets de chaque frontière sont à tester avec coupure I/O.

## Vecteurs normatifs synthétiques

[vectors.json](vectors.json) contient les deux proofs, COMMIT complet, bytes de
primitive C et les quatre hashes attendus. contract=64zéros est un **sentinel de
test**, pas le digest du futur bundle ni une autorisation. Le nonce fixe est
réservé au test. Taille du COMMIT d’exemple7508octets, pas garantie de tous les cas.
Dix vecteurs de messages couvrent toutes les tables modifiées, INSPECT/SNAPSHOT et
une ancienne clé PRESENT complète ; le label de hash de ces messages est
jarvis.fixture.p2/2.message.D4E1.
[verify_vectors.py](verify_vectors.py) vérifie deux encodeurs indépendants et
mutations ; ne vérifie pas un UID/Binder ou l’état réel du worker.

Le prochain contrat doit publier ses propres vecteurs Kotlin/Python byte-identiques
avec sa vraie empreinte. Un hash de vecteur vérifié n’approuve aucun codec futur.
