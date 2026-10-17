# D4-02E — F1/F2 : clarification proposée, non approuvée

Mission autorisée par [issue2](https://github.com/bubth720/JARVIS-UNIFIED/issues/2)
et [décision1748cb0](../DECISIONS/VALIDATION-IDENTITY-ID-001-2026-10-17.md).
Base1748cb0706fa4b0cfac2df963d82a14195b9d25a : descend de27e6740, préserve
l’accord expérimental8ddac8f et la décision IDENTITY, sans changer D4-02D.
Cette revue corrige des ambiguïtés de notre proposition D4-02D, effectivement
rencontrées par LLM003F111be993e970051686bd5c27b3115320513a4be7.
La publication de ce dossier ne vaut pas approbation du nouveau bundle.

## F1 : les incarnations CORE viennent de CORE

Décision proposée : DISCOVER apporte explicitement **core_process_epoch** et
**broker_epoch**, plus issued_elapsed_ms/expires_elapsed_ms ; passer de7 à11
champs fermés. NEGOTIATED reprend exactement ces champs et ajoute les incarnations
LLM/endpoint et code=NONE. Tables exactes dans TABLES_PROPOSEES.json.

CORE crée process_epoch une fois dans l’autorité Application du processus de fixture,
broker_epoch une fois par instance d’arbitre, session_id pour la session de contrôle.
LLM crée ses propres process/service epochs, jamais ceux du CORE. Aucune dérivation
UUID depuis PID, UID, getCallingPid ou service_epoch de l’autre module.
Les UUID sont déclarations logicielles d’incarnation, pas attestations OS.

Avant décodage et dispatch : UID réel, package unique, certificat courant unique,
permission signature et composant attendus ; après dispatch, revalider les pins.
Lier le tuple (pilot, UID/cert, core_process_epoch, broker_epoch, session_id,
round_id, nonce, clientLiveness, liaison et service_epoch LLM) à la négociation.
Réponse par callback authentifié du pair et écho exact ; nonce32octets CSPRNG,
fenêtre monotone >0 et<=5000ms, pas de comparaison de deadline persistée cross-boot.
Les exemples sont synthétiques et ne sont jamais des tokens utilisables.

Rejeu identique dans le même tour vivant/frais : réponse idempotente sans ouverture.
Tuple différent sur un tour déjà lié : STALE_INCARNATION/REPLAY_CONFLICT. Nouveau
broker/Service, token mort, changement de certificat/package ou expiration invalide
le tour et garde RECOVERY_REQUIRED. Une nouvelle négociation ne termine aucun travail
ancien et ne peut reprendre un grant volatil. Pas de copie de trustedPeerEpochs
injecté en test vers production ; la source devient ce DISCOVER authentifié.

## F2 : chaque participant atteste son propre journal

Choix proposé : **séparation des propriétaires**, pas lecture de sandbox distante.
INSPECT garde ses champs R+I+K ; SNAPSHOT retire les quatre core_journal_* et
n’annonce que J_LLM, génération/propriétaire/prior-key locaux et observations LLM.
Pas de valeur CORE inventée, même vide. Un champ étranger est INVALID_FIELD.

CORE lit son propre journal sous sa barrière, reçoit SNAPSHOT LLM frais et corrèle
pilot/session/epochs/clé entière/génération/nonce. Divergence non résolue =
PRECONDITION_CHANGED/UNKNOWN, pas max(générations) effaçant une obligation.
CORE produit **CORE_PREPARE**, preuve locale typée de son état et de sa tête PREPARED.
Il transmet cette preuve dans CHALLENGE, canonique base64url bornée + digest.
LLM vérifie identité CORE, cohérence des champs et tête LLM attendue, puis prépare
sa propre preuve ATTEST. Les core_journal_* encore présents dans ATTEST sont un
**écho de déclaration CORE**, jamais une attestation de LLM sur la sandbox CORE.
COMMIT transmet les deux preuves exactes pour vérification d’appartenance.

Une preuve CORE n’est authentifiée qu’au travers du chemin de confiance CORE et
Binder actuel ; un hash/UUID ne la signe pas. LLM conserve sa propre preuve pour
comparaison octet canonique, ne fait confiance à aucun ATTEST renvoyé par un client.
CORE vérifie le callback LLM et sa propre preuve locale immuable. Les signatures
APK/UID identifient les logiciels participants ; hypothèse de paire/OS fiables,
pas preuve absolue de mémoire Android ni de sincérité d’un pair compromis.

## Invariants inchangés

Deux attestants de contrôle core/llm, seul propriétaire natif pilote llm. Historique
CORE/Whisper/VOICE et applications non participantes hors garantie, pas ajout de
moteur historical réel à PilotRuntime. Barrières avant toute allocation, absence
native comptée depuis objets réels, fin/drain/unload distincts. Journal absent,
corrompu, cleanup raté, mort de processus sans reçu durable : UNKNOWN reste bloquant.
Ni hello, PID, mort Binder, process neuf vide, deadline ni COMMIT ne libèrent un bail.
Aucune génération /2 ou persona IDENTITY ajoutée ; pas de seuil matériel changé.

## Critères de résolution de F1/F2

DISCOVER positif sans valeurs inventées ; chaque mutation d’epoch/session/nonce
refusée ; SNAPSHOT complet construit uniquement depuis données LLM ; CORE_PREPARE
construit uniquement depuis données CORE ; preuve CORE discordante rejetée avant
PREPARED ; ancien journal/attestation refusés. Tests hôtes ne deviennent pas des
preuves Binder Android. F1/F2 résolues dans la **spécification proposée**, toujours
à corriger et tester dans le dépôt LLM après validation.
