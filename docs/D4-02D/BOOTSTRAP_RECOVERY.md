# D4-02D — amorçage et réconciliation du pilote

**PROPOSITION À VALIDER — aucune implémentation ni nouvelle approbation.**
UNIFIED, 17 octobre 2026. Base : `audit/d4-02c-core-llm-convergence`,
`0dbb978994994fa3210124f1e150ca23426d410d` ; branche de travail :
`design/d4-02d-bootstrap-recovery`. ADR-001 reste approuvée pour l’orientation ;
les choix de fixture décrits ici ne deviennent pas des décisions O3 définitives.

## Diagnostic vérifié et périmètre

CORE004C `da40ed7155409b85860a22c1dbbfe35029cea29a` démarre toujours son
PilotArbiter en RECOVERY_REQUIRED. Sa méthode reconcile consomme des preuves
**locales de confiance**, pas des preuves authentifiées reçues de LLM. Le runtime
n’en fournit aucune : ce blocage volontaire empêche une admission inventée.
LLM003E code `5751646acd4a7bb13caaea4b96a4ab3a68ec6adb`, clôture documentaire
`030152a5f3d888017ad7a7fe8026f2e2c48e8fd5`, offre hello/submit/status/cancel,
mais pas de défi d’état initial ou d’inspection durable après perte de active.
Le hello actuel n’atteste pas la quiescence. Sources et preuves datées dans
[TESTS_ET_PREUVES.md](TESTS_ET_PREUVES.md).

Le pilote comprend **deux processus de fixtures**, fr.jarvis.fixture.core et
fr.jarvis.fixture.llm. Le seul propriétaire natif admis reste llm ; CORE est aussi
un participant de contrôle à attester, sans ajouter un propriétaire « historical »
à PilotRuntime. APK historiques, Whisper, VOICE et autres applications ne sont
pas enrôlés. On ne revendique aucune exclusivité face à eux ni à tout Android.
Leur arrêt éventuel en laboratoire est une condition de qualification distincte,
pas une capacité de ce protocole. CORE historique API24 demeure inchangé ; paire
expérimentale ARM64 API29+, corpus synthétique fermé, protections inchangées.

## Ce qu’une attestation signifie

Attestation = déclaration **logicielle authentifiée, fraîche, bornée et vérifiable**
d’un état instrumenté, sous hypothèse d’OS/paire signée fiables. Le Binder et le
certificat authentifient le participant ; le nonce lie la réponse au défi.
Cela ne mesure pas absolument toute la mémoire Android, ne prouve ni RSS=0 ni
absence de code malveillant dans un processus compromis. Pas de TEE/attestation
matérielle inventée, ni de nouvelle clé privée d’attestation obligatoire.

LLM peut déclarer, si observés sous une même barrière :

- Inventaire des backend/worker réels du processus, importations, tâches en file,
  appels natifs en cours, handles/models/contextes et baux ProcessResources connus.
- NOT_STARTED : aucun travail admis/déclenché pour l’opération précise ; ce n’est
  pas l’affirmation qu’un modèle ne fut jamais chargé dans toute l’application.
- NATIVE_RETURNED : tous les appels associés ont réellement rendu la main et le
  worker est drainé. Une annulation de coroutine ou stop=true ne suffit pas.
- UNLOADED_CONFIRMED : unload réel réussi et inventaire sans résidence du modèle,
  sans appel/import/bail lourd restant ; la bibliothèque JNI et son handle peuvent
  rester chargés si leur état vide est effectivement connu. Pas d’assertion par
  défaut depuis backend==null, isLoaded=false ou une estimation PSS.
- Journal validé avec séquence/empreinte, dernier propriétaire/clé/digest/issue,
  incarnation du processus et du service observés et barrière encore active.

CORE atteste sa propre barrière, l’absence de runtime lourd **par construction de
sa fixture**, l’absence de tâches/appels dans son registre, et son journal/bail.
Il ne signe pas à la place de LLM une libération native. Les deux attestations
sont nécessaires, bien que participants de contrôle et propriétaires soient distincts.
Une erreur d’inspection, un trou d’instrumentation ou un journal ambigu produit
UNKNOWN ; jamais une valeur « vide » optimiste.

## Barrière et identité d’incarnation

Installer dès Application.onCreate une autorité **unique au processus de fixture**,
avant toute possibilité d’allocation/import/warm-up. Elle inventorie et garde
les vrais objets du backend ; recréer le Service ne doit pas oublier un ancien
worker en drainage. Elle n’ajoute pas un second acquéreur de baux natifs.
La barrière ferme tous les chemins participants et est fermée par défaut.
Une attestation prend un snapshot sérialisé avec cette autorité ; la barrière
reste fermée jusqu’à commit et autorisation ultérieure d’une nouvelle opération.
Une simple suite de lectures non atomiques n’est pas suffisante.

Créer process_epoch UUID une fois par processus via cette autorité ; service_epoch
UUID par instance de service ; broker_epoch par instance d’autorité CORE. Le champ
epoch de003E naît actuellement dans P2EndpointService.onCreate : **ne pas le
présenter comme une preuve d’incarnation du processus**. Nouveau contrat : epoch
opérationnel conserve son rôle d’epoch endpoint, avec process_epoch distinct.
PID reste une observation de diagnostic, pas un facteur de déverrouillage.

## Enrôlement initial : aucun ancien bail à effacer

Prérequis proposé : provisionnement explicite d’une **nouvelle paire de laboratoire**
avec clé commune dédiée hors Git, pins des certificats/APK/contrat et cohorte
pilot_id. Ni réinstallation ni effacement d’une paire existante pour débloquer.
La sonde authorized de LLM porte le même applicationId que CORE : ne pas les
coinstaller ou remplacer implicitement l’une par l’autre.

1. Chacun entre BLOCKED et valide identité/version, fichiers de journal et marqueur
   d’enrôlement avant tout accès natif. L’absence d’un fichier seule ne suffit pas.
2. Si première paire autorisée : enregistrer durablement une intention d’enrôlement
   puis deux marqueurs rattachés à pilot_id/pins. Registres créés dans l’ordre
   journalisé, génération initiale0, aucune ancienne clé et aucun ancien bail.
   Une intention incomplète au redémarrage reste bloquée jusqu’à réconciliation.
3. Les deux processus, instrumentés depuis leur naissance, prouvent sous barrière
   NOT_STARTED et NO_RESIDENCY_CONFIRMED, journaux sains et cohérents avec cette
   création. Pas de création JNI ni appel modèle pour « sonder » l’absence.
4. Défi frais et commit durable décrits dans [PROTOCOLE_PROPOSE.md](PROTOCOLE_PROPOSE.md).
   Aucun mandat de génération nécessaire pour ce chemin de contrôle ; celui-ci ne
   peut charger, importer ou répondre du texte. Cela évite la dépendance circulaire.
5. Seulement après tous les ACK exacts : CORE inscrit IDLE_VERIFIED. Une opération
   nouvelle, de génération1 et clé neuve, exige encore la véritable autorisation,
   l’admission matérielle et le contrôle de foreground ; l’attestation n’est pas un bail.

Journal absent avec marqueur existant, marqueur absent face à l’historique connu du
pair, cohorte différente, application mise à jour non autorisée, rollback observé :
JOURNAL_MISSING/ENROLMENT_CONFLICT, aucun enrôlement automatique. Si **tous** les
stockages ont été effacés/restaurés ensemble, ces seules applications ne peuvent
prouver cet historique perdu. La nouvelle paire exige autorisation de laboratoire
et inventaire indépendant ; ce risque n’est pas « résolu » par un UUID ou checksum.
OS rooté, rollback coordonné des deux sandboxes, certificat compromis sont hors
preuve logicielle ; diagnostic/blocage, pas promesse d’anti-rollback matériel.

## Réconciliation selon la cause

| Situation | Actions permises sans nouvelle charge | Condition de sortie | Ce qui reste interdit |
|---|---|---|---|
| Redémarrage sans réservation | Fermer barrières, lire journaux et dernier commit, défi des deux processus actuels | Journaux sains/chaînés, génération non régressée, aucune ancienne opération non résolue, deux snapshots frais vides et commit/ACK | hello→IDLE, réutiliser ancien nonce ou deadline persistée |
| Interruption, worker encore actif | Révoquer génération de texte, stop corrélé, attendre appels/imports puis unload sous propriétaire existant | Reçu réel terminal durable de la clé exacte + deux attestations fraîches + commit | Nouveau load, timeout comme fin, replay submit |
| Mort du client CORE/broker | LLM conserve bail et journal, stop/drain/unload ; CORE suivant charge l’ancienne réservation sans l’approuver de nouveau | Reçu durable vérifiable/re-attesté, cohérence des deux journaux et nouveau défi | Reconstituer GrantRegistry à partir d’une ancienne query ; ancien callback approuvé |
| Destruction/recréation du Service LLM, processus vivant | Retrouver autorité de processus et vrais objets en drainage ; service_epoch change | Drain/unload observés par l’autorité, même process_epoch, défi lié au nouveau service et anciens journaux | Nouveau backend masquant l’ancien ; confondre disparition Binder et mort du processus |
| Mort effective du processus propriétaire | Reconnecter sans native ; inspecter historique terminal et incarnation nouvelle | Si reçu terminal durable préexistant et cohérent : attestation fraîche le rattache. Sinon il manque une preuve de résolution de l’ancienne résidence | Nouveau process vide→ancienne opération libérée, PID absent/réutilisé, DeathRecipient seul |
| ACK de fin ou commit perdu | status de récupération sans génération, relire décision/transaction et reçus conservés | Même transaction/décision idempotente, mais nouvelle attestation si défi expiré ou incarnation changée | Replay submit, allouer pour savoir si ancien appel a fini |
| CLEANUP_FAILED, même propriétaire vivant | Inspection ; une **demande explicite** de retry cleanup uniquement après fin native, avec les mêmes handles/baux encore instrumentés | unload réel réussi + journal terminal sain + nouvelle réconciliation complète | Retry périodique automatique, reset du flag, prepareOperation nouveau, baux rendus avant succès |
| UNKNOWN | Collecter uniquement les preuves manquantes sous barrière ; drain/cleanup si objet existant identifié | Chacune des obligations redevient positivement démontrable | Interpréter inconnu comme NOT_STARTED, reset au timeout/redémarrage |
| Journal corrompu, illisible, écriture échouée | Bloquer et préserver fichier exact + secours ; diagnostic hors ligne sans données personnelles | Pas de récupération automatique définie ; réparation/import contrôlé exigerait mission et autorisation distinctes | Supprimer/remplacer le journal par vide, checksum « réparé », marquer libéré en mémoire |

Pour une ancienne opération non résolue après mort du propriétaire, aucun mécanisme
actuel ne donne une preuve fiable de sa disparition. Un superviseur OS de confiance
ou une procédure contrôlée de redémarrage complet documentée pourrait être étudié
séparément ; **non livré, non autorisé, jamais remplacé par PID/hello/Binder**.
Dans003F/004D cette branche conserve UNKNOWN. Le chemin propre est débloquable ;
la disponibilité après panne arbitraire n’est pas promise.

## Invariants à préserver

Tout changement d’identité, incarnation, participant, journal, expiration ou
barrière invalide le tour. Aucun reset automatique, suppression de journal,
réemploi d’attestation, création d’ancien reçu ou fallback lourd. Réconciliation
peut être déclenchée automatiquement pour **observer**, jamais réussir sans toutes
les preuves ; retry cleanup requiert demande explicite. Aucune réponse récupérée
après annulation/expiration/mort du client ne redevient un texte consommable.
Les quarantaines CORE004B historiques restent hors périmètre et ne sont pas levées.
