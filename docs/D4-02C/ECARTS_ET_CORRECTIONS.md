# Écarts et contrat de convergence proposé

**Spécification documentaire `core-llm-convergence/1-draft`, non approuvée et non
implémentée.** Aucun changement des cinq schémas UNIFIED v1, des apps ou des seuils.
CORE reste orchestrateur/autorité des permissions ; LLM propriétaire de l’inférence.
[Matrice détaillée](MATRICE_CONVERGENCE.md), [références](REFERENCES.md).

## Corrections à retenir pour le contrat commun

| Priorité / écart | Correction proposée | Propriétaire / dépendance |
|---|---|---|
| P0 E1 IDs et epoch | Clé complète immuable par opération, mapping enregistré par CORE et validé par LLM ; UUID non vides vérifiés, replays refusés | CORE crée/retient, LLM contrôle ; accord version DTO |
| P0 E2 aplatissement | Exposer structures avant PromptBuilder.render, ou refuser contexte non représentable. Aucun découpage de chaînes sur en-têtes SOURCE/HISTORIQUE | CORE ; fixture texte vide de contexte d’abord, pas perte du contexte réel |
| P0 E3 rendu système | Une seule fonction de rendu final, politique fixe une fois + SYSTEM configurable une fois, préfill officiel une fois ; même fonction pour compteur et génération | LLM ; réutiliser format() C++ et backend existants, préserver la voie historique |
| P0 E4 tokens/limites | Compteur JNI de tous les messages + template/vocabulaire/BOS/préfill, bornes effectives vérifiées sur le rendu réellement décodé | LLM ; countP2Tokens(system,question) seul ne couvre pas historique/docs, pas exposé dans NativeApi Kotlin |
| P0 E5 callbacks réels | Adapter P2GenerationPort aux appels réels et à la clé active ; état P2 reflète les baux réels sans en acquérir une seconde fois | LLM ; P2Lifecycle actuel reste modèle opt-in, pas branchement direct sur LlamaBackend |
| P0 E6 fin et libération | Reçus distincts de stop, native_done et unloaded, clé/génération/digest liés ; aucun défaut true ou isLoaded=false comme preuve | LLM atteste, adaptateur CORE vérifie ; contrat de retour d’unload à définir |
| P0 E7 autorité commune | Arbitrage interprocessus choisi en O3, couvrant tous les chemins participants ; pas de nouveau moteur après état inconnu | CORE politique ; emplacement proposé en O3 ; aucun reset de quarantaine |
| P1 E8 erreurs/capacités | Type d’échec conserve code P2 détaillé, phase et état natif ; ne pas faire croire structuredCoreSession=true avant validation | Deux adaptateurs ; UNIFIED résumé existant possible, détails versionnés hors v1 inchangé |
| P1 E9 preuves Android | Tests ARM64 réel/permissions/identités puis matériel après autorisation, sans modèles privés envoyés au cloud | Deux missions de fixture, qualification physique ultérieure distincte |

## Requête commune et mapping exhaustif proposé

Les noms de champs ci-dessous ne sont pas un schéma existant ni un endpoint actif.
Le protocole filaire sera séparé, fermé et négocié après validation O3.

| Champ commun | Mapping CORE → LLM | Règle de conservation / refus |
|---|---|---|
| namespace/version | Int1 CORE et jarvis.llm.p2/1.0 sont deux versions locales ; adapter explicitement vers version commune | Un chiffre1 identique n’établit pas la compatibilité ; major inconnu refuse |
| session_id | InferenceRequest.sessionId → OperationKey.sessionId | UUID canonique requis ; identifiant legacy arbitraire non transformé silencieusement |
| request_id / operation_id | requestId → operationId | Une requête native par ID ; pas de relance après ACK perdu sans status |
| correlation_id | UUID de transport indépendant, lié par table CORE au requestId | Ne pas interchanger correlationId et operationId ; réponse doit conserver les deux |
| epoch | Epoch UUID de connexion/processus négocié ; CORE epoch Long reste compteur local d’invalidation | Ne pas convertir Long en UUID factice ; ancien epoch rejeté après réconciliation |
| cancellation_id, authorization_ref | UUID de commande/mandat issus du CORE, vérifiés au canal/hôte | Ce ne sont ni tokens d’authentification ni permissions auto-accordées |
| lease_id, generation | Bail de l’autorité d’admission, génération monotone bornée | CORE admissionToken process-local et LLM lease réels restent distincts ; mappings explicites, libération ancienne sans effet |
| system | systemPrompt exact autorisé → P2Request.system puis paramètre custom natif | Jamais user, jamais null pour activer P2 ; vide explicite garde voie P2. Politique fixe non fournie par client |
| question | question exacte, UTF-8 strict ; pas de suffixe UTILISATEUR/ASSISTANT historique dans le texte métier | Pas de troncature ou retrait de caractères silencieux ; délimiteurs interdits = refus explicite |
| history | Tours structurés sélectionnés par CORE, rôles user/assistant | P2≤6, alternance par paires, puis question ; autre historique refuse ou nouvelle proposition de contexte avant envoi, jamais parser context aplati |
| memory_context | Souvenirs confirmés et références séparés dans contrat futur, jamais SYSTEM ni document inventé | P2 actuel n’a pas ce champ : contexte mémoire non vide refuse tant que type/consentement/mapping non définis. Ne pas camoufler dans question |
| documents / provenance | Extraits intègres + référence opaque UUID liée au documentId/chunkId/nom/index, snapshot/digest et révision réelle si connue | P2 revision>0 inconnue côté CORE : refuser le mode documentaire jusqu’à contrat/versionné ou métadonnées de propriétaire. Pas de revision1 fabriquée ni perte de noms/index |
| model et model_sha256 | Modèle SMALL/MAIN choisi selon politique locale et SHA vérifié par LLM | Pas de chemin envoyé par client ; revalider fichier réellement chargé ; incompatibilité refuse |
| limits | Contexte, sortie, bytes et durée restante = intersection demande/admission/format | Context512..2048 par256 et restrictions SMALL/MAIN ; config résultante invalide refuse, aucune hausse silencieuse |
| audit_context | Versions app/contrat/backend et provenance des données distinctes | Sans prompt, nom privé, document, secret ou empreinte de voix dans logs ; refs opaques et état technique minimal |

Pour le pilote : fixture volontairement sans historique/documents/mémoire et avec
SYSTEM synthétique configurable. Le mapping textOnly existant s’applique uniquement
à ce domaine explicitement restreint ; une requête CORE réelle contenant du contexte
ne devient jamais « compatible » en le supprimant. Les cas exclus restent des refus
couverts par tests. Pour généralisation, CORE fournit une nouvelle vue structurée
avant aplatissement et la provenance reste dans un registre privé de snapshot lié
au digest de requête. Ce registre ne migre pas les documents ou la base.
Une référence conservée hors texte modèle n’est pas perdue : elle est résolue chez
CORE au retour, contrôlée au snapshot et n’est jamais remplacée par citation générée.

## Rendu exact et budgets

Choix recommandé : le formateur natif canonique est la seule autorité du rendu
final. P2Planner garde validation/planification, mais ne transmet pas son SYSTEM
déjà préfixé comme systemPrompt de GenerationRequest, sinon la politique est
ajoutée deux fois et la mesure de PromptSpec ne décrit plus l’entrée générée.
Le banner documentaire doit être produit exactement une fois au même endroit,
avec IDs/révisions cohérents, avant comptage. Template et vocabulaire du GGUF
chargé, flags BOS/special tokens et préfill identiques entre compter/générer.

Étendre séparément l’accès au compteur pour tous les tours/documents et fournir
le digest du template réel, du modèle et du rendu. Le symbole countP2Tokens natif
n’est aujourd’hui exposé que dans le harnais Java hôte et n’est pas un adaptateur
TemplateTokenizer Android complet. Interdiction de marquer NATIVE_VERIFIED à partir
d’un compteur de fixture ou d’un entier sans provenance.

Le contrôle final porte sur `tokens(rendu final)+sortie_effective+8 ≤ contexte_effectif`.
Le JNI actuel compare au contexte **chargé**, pas au plafond CORE plus petit.
Solution proposée : configuration effective validée au profil dont le contexte
chargé ne dépasse pas la demande, ou enforcement natif explicite du plafond négocié.
Demande512 sur contexte768 : prouver la limite512, recharger512 si autorisé, ou
refuser ; jamais accepter parce que cela tient dans768. MAIN minimum768 : demande512
refusée, pas relevée. Enveloppes d’admission2/4Gio et réserves restent inchangées.
Le proxy UTF-8 CORE demeure une précaution legacy, pas le compteur officiel P2.

Les plafonds s’appliquent aussi **après composition** :6 tours≤4096octets/tour,
4 docs≤4096octets/doc, question/système≤8192octets, total raw≤65536 ne garantissent
pas qu’un dernier message composé respecte16000 caractères ni le budget natif.
Tester ces deux bornes et le prompt final ; aucun fractionnement de rôles ou
suppression de sources improvisé. Négocier les capacités spécifiques au profil.

## Cycle de vie commun et preuves

Proposition : admitted → loading → ready → counting → running → stop_requested
si besoin → native_done → unloading → unloaded → résultat consommable. Échec de
nettoyage = CLEANUP_FAILED, information manquante = UNKNOWN ; ces états retiennent
la réservation/quarantaine et interdisent un second modèle. Stop ACK n’est qu’une
confirmation de réception, pas la fin. begin ne doit pas réarmer le flag natif
pendant une ancienne opération. Le délai natif fixe90s ne remplace pas la durée
restante plus courte : watchdog corrélé et vérification avant chaque phase.

Un seul propriétaire des baux internes LLM : **LlamaBackend/ProcessResources
réels**. Relier P2Lifecycle par observation/protocole adapté, pas en empilant ses
acquisitions actuelles sur celles du backend : le heavy déjà détenu provoquerait
BUSY (ou états mensongers en utilisant un autre broker). Le compteur/formatage
s’exécute dans le même worker/admission que le modèle, pas en accès natif concurrent.

Reçu commun proposé : clé complète, phase terminale, native_ever_started,
effective_end, model_unloaded/release_confirmed, état de nettoyage, configuration
et modèle effectifs, digests de requête/rendu et état de baux. Chaque booléen exige
observation du vrai retour d’appel et déchargement, ou preuve explicite d’absence
d’appel avant dispatch ; aucune exception générique ne prouve la libération.
Pas de garantie de PSS nul : libérer un modèle n’efface pas tous caches du système.

Le serveur ne livre un Text final qu’après nettoyage confirmé, comme le modèle
P2Lifecycle le prévoit. En cas de cleanup_failed, renvoyer un échec et l’état sûr,
pas le texte comme succès. Le CORE conserve ses contrôles session/epoch avant
historique et TTS. Le proxy renseigne nativeDone **explicitement** depuis reçu
vérifié, jamais via son défaut true. Le CORE reste conservateur modelUnloaded=false
jusqu’à son appel unload/ACK idempotent lié à la même réservation ; pas de libération
d’un nouveau propriétaire par un ancien reçu. Un replay de status/unload lit l’état,
ne relance pas l’inférence. Tout ACK perdu se résout par interrogation corrélée.

CORE296 quarantiné ne se réarme pas sur nouveau contrôleur ni sur simple reçu de
retry LLM. Le pilote conserve cette politique stricte ; une récupération commune
ou un redémarrage de processus nécessite réconciliation de tous les participants,
pas reset de singleton. Perte de client/service ne vaut pas mort du processus ni
zéro résidence. Le broker doit bloquer au démarrage tant que l’ancienne réservation
n’est pas résolue selon [O3](DECISION_O3_PROPOSEE.md).

## Erreurs, versions et absence de transport implicite

| Source | Résumé CORE possible | Détail/état à conserver dans nouveau contrat |
|---|---|---|
| P2 BUSY | BUSY | Titulaire/phase non sensibles, pas de retry lourd parallèle |
| P2 CONTEXT_EXCEEDED/INVALID_LIMIT/INPUT_TOO_LARGE | BUDGET | Code précis et limites effectives ; aucune troncature |
| P2 UNSUPPORTED_VERSION/INVALID_UTF8/INVALID_ROLE | CONTRACT | Cause typée, aucune commande ou texte d’exception interprété |
| P2 STALE_OPERATION | STALE_RESPONSE | Clé/epoch invalidés, aucune persistance assistant |
| P2 CANCELLED/EXPIRED | STOP_REQUESTED ou erreur de délai future | Délai≠arrêt confirmé ; native_end/unload restent distincts |
| P2 CLEANUP_FAILED/UNKNOWN_STATE | RELEASE_UNCONFIRMED | Quarantaine, propriétaire et preuve de fin, pas false ready |
| P2 UNAUTHORIZED/MODEL_MISMATCH/NATIVE_P2_UNAVAILABLE | Pas d’équivalent CORE fidèle actuel | Conserver code nommé et raison de refus via adaptation versionnée ; ne pas l’effacer dans CONTRACT générique |

Le mapping P2Error.unifiedCode existant est un résumé, pas un sérialiseur ou preuve
que toutes les erreurs passent sans perte. Les IllegalStateException JNI doivent
être traduites dans le fournisseur avant transport, sans parse de messages arbitraires.

Contrats locaux Int1/engine1.0/P2 1.0 et UNIFIED1.0.0 restent distincts. Les cinq
schémas UNIFIED acceptent des références privées mais pas tous les nouveaux messages
status/cancel/release ; définir une proposition de contrôle versionnée séparée
puis obtenir validation, sans modifier enum/champs v1 en place. Les Fields actuels
ne sont pas un parseur wire. Capacités nativeP2, correlatedSession, fullTokenizer,
releaseReceipt et interprocessAdmission ne doivent être annoncées vraies que dans
la fixture où elles sont réellement câblées et testées.
