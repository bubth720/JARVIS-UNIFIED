# Diff contractuel proposé /2 — aucune adoption du candidat existant

Référence comparée : LLM111be993e970051686bd5c27b3115320513a4be7,
bundle candidat `4b4129b595b78481d846c521993026fe2477c64fccfe4259ba9a5e30f9d68e62`.
Les [tables complètes proposées](TABLES_PROPOSEES.json) et le
[diff exact des champs](TABLES_DIFF.json) sont des spécifications de revue UNIFIED,
pas des fichiers remplacés dans LLM. Pas de nouveau digest réel LLM inventé.

| Table / source | Modification exacte proposée | Refus / vecteur attendu |
|---|---|---|
| DISCOVER | +core_process_epoch, broker_epoch, issued_elapsed_ms, expires_elapsed_ms | Champs manquants/faux type refusés ; epochs CORE authentifiés, expiré=EXPIRED |
| NEGOTIATED | +issued_elapsed_ms, expires_elapsed_ms, écho exact des11 champs DISCOVER sauf kind | Ancien nonce/epoch/date, nouvelle liaison non reconnue : STALE_INCARNATION/REPLAY_CONFLICT |
| SNAPSHOT | Retirer core_journal_id/seq/state/sha256, conserver seulement journal LLM et ses observations | Un champ J_CORE restant doit refuser INVALID_FIELD ; pas de valeur fabriquée |
| CORE_PREPARE | Nouvelle table de preuve locale CORE : ATTEST antérieur moins les4 llm_journal_* et +code ; rôle core uniquement | Pas d’appel RPC autonome ; déclaration du CORE transmise par canal CORE authentifié |
| CHALLENGE | +core_prepare_b64/core_prepare_sha256 | Hash/table/borne/non-canonical b64 refusés INVALID_PROOF ; J_CORE doit correspondre au CORE_PREPARE, J_LLM au snapshot réel |
| ATTEST | +core_prepare_sha256 | Relier exactement la preuve CORE reçue ; rôle llm, propre tête PREPARED ; hash manquant/incohérent refusé |
| COMMIT | +core_prepare_b64, llm_attest_b64, core_prepare_sha256, llm_attest_sha256 ; recalcul p et d selon COMMIT_CANONIQUE | PROOF_SET_MISMATCH/DECISION_MISMATCH, y compris ensemble de preuve incomplet mais hashes recalculés |
| COMMIT_ACK | +core_prepare_sha256,llm_attest_sha256 ; committed_* cite COMMITTED, pas ACK_OUTBOX | Ancienne décision ou hash sans ACK durable refusé ; pas de réponse positive après IO ratée |
| INSPECT/CLEANUP_REQUEST/REFUSED | Champs inchangés ; nouvelles erreurs ci-dessous et récupération adaptée aux journaux propres | Absence de F3 : CLEANUP_UNAVAILABLE/BACKEND_OBSERVATION_UNAVAILABLE ; pas UNKNOWN→libéré |

Les neuf prior_fields s’ajoutent exactement quand prior_key_state=PRESENT à toute
table portant ce discriminant, y compris CORE_PREPARE. Ils sont absents si NONE ;
aucune clé fausse au premier enrôlement. Génération/prior/propriétaire cohérents
entre les deux journaux avant challenge, aucun écrasement du high-water mark.

En plus de TABLES.fields : proof_max_decoded_bytes=6144, proof_max_base64_bytes=8192,
local_proof_kinds=[CORE_PREPARE], journal_states explicites dans le fichier proposé.
Nouveaux codes : INVALID_PROOF, PROOF_SET_MISMATCH, SNAPSHOT_OWNERSHIP,
BACKEND_OBSERVATION_UNAVAILABLE. Codes existants non supprimés ; PEER_INCARNATION_REQUIRED
et PEER_JOURNAL_REQUIRED restent des diagnostics de paire non qualifiée, pas des
valeurs de remplissage pour réussir. UNKNOWN conserve son sens bloquant.

États de journal supplémentaires : CORE_PROOF_OUTBOX, ATTEST_OUTBOX, DECISION_OUTBOX,
ACK_OUTBOX, FINALISED. Adapter explicitement RecoveryProtocol.journalStates et
RecoveryJournal aux nouvelles tables/chaînes ; ne pas garder une enum cachée divergente.
Caps24576/32768bytes, fenêtre5000ms,128tours/512records inchangés. Capacité de records
réservée avant tour ; refus si la chaîne/outbox nécessaire ne tient pas.

## AIDL, sérialisation et compatibilité

**Aucun changement AIDL requis** pour F1/F2/COMMIT : recovery(byte[],IBinder,
IRecoveryCallback) transporte ces objets et preuves bornés. Vérifier les mêmes
packages/descripteurs/ordres : endpoint hello1,submit2,status3,cancel4,recovery5 ;
arbiter authorize1,recovery2 ; callbacks complete1. Aucun nouveau service exporté,
aucune API de lecture de journal d’un autre APK. Ancien /2 ne doit pas ignorer les
champs : nouveau bundle normatif/digest obligatoire et pin commun avant échange.
Refus INCOMPATIBLE sans downgrade, même si version majeure reste /2 expérimental.

/1 figé : `fab6a66a6b99302884849cd1d8aef97cd761082dc20680a4b036d7bc99d5c3c9`,
snapshot v1/ et préfixes ABI byte-identiques. DOMAIN P2/engine et UNIFIED v1
inchangés. Tests fixture /1 de référence restent séparés ; ni les méthodes /1 ni
la génération historique ne deviennent des preuves de reprise /2.

Révision proposée D4-02E.1 doit être revue avant LLM. LLM produira ensuite le bundle
CONTRACT.txt+TABLES.json+AIDL, son vrai SHA et ses vecteurs Kotlin/Python. Le SHA de
TABLES_PROPOSEES.json seul n’est pas le SHA de ce bundle. Les vecteurs publiés ici
utilisent un contract nul de test et ne prouvent aucune admission native.
