# Contrats d’intégration proposés — DESIGN-004

**Spécification documentaire1-draft, non exécutable et non approuvée.** Aucun
schéma/contrat v1 existant n’est modifié. Les noms ci-dessous sont des noms de
travail, pas des endpoints présents. Responsabilités d’abord :
[matrice ADR](RESPONSABILITES_ET_ADR.md). Détails métier dans [SYNC](SYNC_V1.md)
et [EXPRESSIONS](EXPRESSIONS_V1.md).

## Compatibilités existantes et séparation des namespaces

| Existant | Écart constaté | Traitement proposé |
|---|---|---|
| UNIFIED protocol1.0 / contract1.0.0, cinq schémas fermés | enum capabilities ne contient pas sync.*, catalogue.select ou audio.cache ; payload = références opaques bornées | Pas d’injection de champs/chaînes inconnues ; une version de schéma négociée devra être autorisée séparément avant usage |
| SERVICES Contracts.VERSION et Bridge.Message | request_id/peer/type/payload≤4096 caractères, echo simulé ; ni identité authentifiée ni pagination/durabilité SYNC | Adaptateur sémantique à étudier ; ne pas faire passer documents dans payload string ou supposer4Kio=4096 caractères |
| CatalogueJson1 | Neuf champs fermés, variantes sans identifiant stable hors record/révision/position ; merge révision entière | Préserver format, passer par propriétaire LLM ; contexte/provenance multi-pair non ajoutés en place |
| CoreVoiceRequestV1 local | Texte1–300, identité/persona/flags ; pas d’enveloppe sync ni service CORE réel | Mapping futur limité, refus si texte dépasse limites ; pas de découpage audio implicite ou profil universel |
| LayoutCodec1 INTERFACE | Document profil d’écran local≤65536 octets, inconnu conservé mais non interprété | Ne pas en faire une préférence portable arbitraire ; adaptateur UI allowlist + validation locale de géométrie |

Les exemples ne sont pas des messages validables par les schémas existants.
Session d’échange SYNC distincte de session conversation CORE, corrélation distincte
d’opération durable. Taille en **octets UTF-8**, entiers bornés sans booléen,
clés uniques/profondeur bornée, erreurs fermées, références privées sans chemin/URL
fourni par un LLM. Chiffrement et contrôle d’identité appartiennent au futur canal,
pas au champ déclaré origin. Rien ne rend une signature IPC approuvée.

## Famille SYNC — modèle de données proposé

Enveloppe minimale : namespace/version, exchange_id, correlation_id, sender_device_ref,
recipient_device_ref, group_epoch, grant_ref, operation_id et durée restante.
Une durée devient deadline monotone **locale** ; timestamps muraux informatifs,
pas de comparaison des horloges monotones entre appareils. Authentification de
l’identité/epoch hors payload, clés privées jamais sérialisées.

| Message de travail / producteur→consommateur | Champs métier requis, après authentification | Réponse/effet et refus |
|---|---|---|
| SyncHello / BRIDGE↔BRIDGE | Versions supportées, capacités, limites, algorithmes reconnus et identités de pair liées au canal | Compatible ou INCOMPATIBLE ; aucun inventaire privé avant autorisation |
| ScopeGrant / CORE→BRIDGE local | Pair(s), types/IDs filtrés, sens, finalité, version de politique, preuve de consentement, expiration/epoch | Refus CLOSED/UNAUTHORIZED si couverture manquante ; ce n’est pas une commande venue du pair |
| DeltaManifest / propriétaire→pair via BRIDGE | Snapshot/watermark, collection/schema, références d’objets autorisés, causalité, tombstones, pagination et total borné | NEED/NOOP/CONFLICT ; absence d’objet ne supprime rien |
| ChangeOperation / propriétaire→propriétaire | OperationID stable, objectID/type, parents et vecteur borné, révision/digest, consentement recevable, upsert/tombstone, contenu privé référencé | APPLIED/ALREADY_COMMITTED/CONFLICT/DENIED/INCOMPATIBLE, jamais succès implicite |
| BlobOffer/Need/Chunk / BRIDGE↔BRIDGE | ObjectID, taille, liste ordonnée digests, chunkIndex/longueur, quota/référence staging, grant et snapshot | ACK bloc uniquement après hash ; absence de place=QUOTA ; commit final distinct |
| CommitReceipt / propriétaire→pair | OperationID, commit durable, version/digest résultants, watermark contigu applicable, epoch | ACK métier après commit ; curseur inchangé si réponse perdue ou conflit |
| ResumeStatus / BRIDGE↔propriétaire | OperationID, snapshot/epoch/grant, blocs attestés, curseur durable | Committed/recoverable/expired/unknown ; ancien snapshot ou epoch exige bootstrap |
| Cancel/Revocation / CORE→opération ou BRIDGE | OperationID/grantRef/epoch, portée exacte | CANCELLED avant commit ; ALREADY_COMMITTED sinon ; révocation propagée selon disponibilité |
| ConflictPreview/Resolve / propriétaire↔INTERFACE via CORE | Versions/digests parents, type de conflit ; aperçu privé ; décision et confirmation exacte si mémoire | Nouveau changement causal signé/autorisé ; ne pas modifier l’ancien événement |

Tombstone sans texte mais sous identité autorisée ; les metadonnées peuvent être
sensibles. Aucun secret/clé dans un reçu. Digest clair d’un contenu personnel
uniquement dans périmètre autorisé ; logs d’audit utilisent refs opaques.

Propositions initiales de bornes à mesurer : message contrôle≤16Kio,100 opérations
par lot,16 pages maximum avant reprise explicite,256Kio/bloc, un transfert lourd
actif pilote ; maxima négociés par politique plus restrictive, aucune promesse
sur capacité/watch. BlobOffer peut référencer un manifeste paginé plutôt qu’une
liste de digests dépassant le message. Un groupe de pairs est borné (exemple8) ;
au-delà refuser/renégocier, jamais tronquer causalité silencieusement. Pas de
champs personnels dans découverte publique ; quotas de staging totaux locaux.

## Famille EXPRESSIONS — propriétaire unique du catalogue

| Message/port proposé | Requête/conditions | Résultat et garde |
|---|---|---|
| ExpressionCandidates / CORE→composant catalogue LLM | Session/corrélation, requête privée référencée, locale, faits de contexte typés autorisés, version catalogue/normaliseur | Answer(recordID,revision,position,textRef,digest) OU Clarify OU LlmFallbackReason ; pas de rôle LLM supplémentaire |
| ExpressionSelect / CORE↔catalogue | Candidats et contexte vérifié, préférence de forme ; si absent utiliser variante neutre existante | Aucun changement de sens, source de faits toujours CORE/propriétaire ; session volatile, pas de souvenir automatique |
| CataloguePackPreview/Apply / INTERFACE→LLM sous CORE | Pack versionné, base attendue, provenance/licence, consentement d’import, différence revue | Réutiliser CatalogueJson/merge et transaction ; même révision divergente refuse tout le lot |
| SpeechPlan / CORE→VOICE | Texte final exact borné, corrélation/session, profil opaque choisi et pack compatible, consentement, limites/durée, annulation | Généré, lecture commencée et lecture terminée distincts ; mapping CoreVoiceRequestV1 à qualifier |
| AudioCacheLookup/Store/Invalidate / interne VOICE | Clé privée complète et autorisation fraîche ; résultat intègre dérivé/profil/pack/texte/paramètres | Hit/Miss/Invalid/Denied ; hit ne prouve pas lecture audible ; Store jamais export ni chargement permanent |

Le port catalogue réutilise IntentRouter et KnowledgeSource. Une donnée retournée
ne donne aucune permission d’exécuter ou mémoriser. Aucun accès direct du CORE
au fichier SQLite LLM, aucun accès LLM au coffre vocal, aucun cache audio dans
UNIFIED. Les métadonnées conditionnelles réclament une extension explicitement
négociée ; le pilote peut rester strictement littéral compatible JSON1.

## Catalogue d’erreurs de travail et sémantique

INCOMPATIBLE_VERSION/CAPABILITY, UNAUTHORIZED, CONSENT_REQUIRED/REVOKED,
PEER_UNAVAILABLE, EXPIRED, CANCELLED, ALREADY_COMMITTED, CONFLICT,
INTEGRITY_FAILURE, STALE_EPOCH, QUOTA_EXCEEDED, BUSY, UNKNOWN_COMMIT.
Ces noms ne sont pas ajoutés à l’enum v1 existante. Un futur adaptateur devra
mapper sans perte ou refuser une version ne permettant pas le diagnostic.
Réessayer seulement les opérations explicitement idempotentes ; UNKNOWN_COMMIT
exige enquête ResumeStatus, pas nouveau lancement d’outil. Mauvais digest jamais
traité comme une simple déconnexion. Erreur≠absence définitive de module/donnée.

## Cas de contrat à transformer en tests après autorisation

C1 champ inconnu/version future ; C2 faux origin/grant et pair non appairé ;
C3 réémission/collision ID ; C4 JSON dupliqué/UTF-8/taille Unicode ; C5 digest faux ;
C6 ACK perdu et commit durable ; C7 tombstone/snapshot filtré ; C8 consentement retiré ;
C9 hors-ligne/timeout/session périmée ; C10 mauvais pack/PCM corrompu ; C11 aucune
variante « effectué » sur état inconnu ; C12 absence totale de backend lourd pour
réponse littérale. Ces spécifications ne sont pas des tests runtime exécutés.
