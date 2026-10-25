# Contrats, écarts et menaces — FUSION-01 F0

Statut : cartographie/propositions, aucune nouvelle approbation de protocole.
Les cinq schémas `contracts/v1` restent inchangés, bornés et gelés par SHA-256 dans
le verrou. Les sources et versions ci-dessous sont celles des SHA primaires et
alternatives identifiés dans les audits ; aucun DTO ne prouve un transport.

| Domaine | Contrat/source existant | Correspondance et écart | Taille/limite observée |
|---|---|---|---|
| Session | CORElab Correlation ; LLM OperationKey | UUID session/request/cancellation ; LLM exige aussi epoch, operation, authorization, lease et generation>=1, CORElab>=0. Pas de conversion silencieuse | UUID canonique, génération LLM <=9007199254740991 |
| Génération | `jarvis.llm.p2/1.0`, InferenceContract CORE | SYSTEM séparé ; textOnly refuse contexte/sources. Préserver provenance avant tout nouveau mapping | entrée65536 octets ; SYSTEM/question8192 chacun ; sortie1..256 tokens ; 6 tours en paires ; 4 documents4096 octets |
| Idempotence/reprise | SERVICES receipts, ApprovalGate | requestId unique ; ACCEPTED interrompu→UNKNOWN ; ne pas faire de l'UI un journal d'autorité | 4096 reçus ; quota plein refuse sans purge |
| Annulation/deadline | CORElab, P2, ToolDispatcher | Corrélation et refus tardif ; stop demandé, retour JNI, fin et unload distincts ; horloges monotones de processus non directement comparables | P2/SERV timeout<=90000ms ; CORE outil5000ms et aperçu30000ms |
| Statut natif | resource-lease v1 / RuntimeResourceProjection | UNKNOWN/UNATTESTED n'autorise pas la réadmission ; refus du second lourd non maîtrisé | Contexte P2 512..2048 par256 ; pas une capacité matérielle nouvellement admise |
| Identité | `jarvis.identity/1`, éditeur local | Profil/persona sans permission ; modifications exactes en prévisualisation et validation CORE ; aucune activation d'Athéna | Pourcentages éditoriaux non acceptés comme champs numériques du contrat actuel |
| Source | NEXUS sources/révisions/import | URI/hash/version stables ; une sélection SAF n'est pas un grant de tous les documents | importeur2MiB, source16MiB bas niveau distinct ; pas de scan/duplication ZIM |
| Citation | NEXUS RagTypes / SERVICES EvidenceReportBuilder | Conserver sourceId, URI, SHA, page, offsets UTF-16, version et quote vérifiable. UI ne possède pas encore de body Citation complet | NEXUS défaut4000car/5items/5sources ; plafond32000/20/20 ; SERVICES50citations×600car |
| Outil | SERVICES ToolDescriptor/Invocation/Registry | Hôte in-process fournit principal/grants ; arguments exacts sans autorité implicite ; 17 outils finaux ne sont pas dans le port24 | <=16 champs et2MiB dans SERVICES, CORElab resserre à8192octets |
| Approbation | ApprovalGate et aperçu CORElab | Liée contenu/version/request/principal/epoch/expiration, consommée une fois ; SAF incertain=UNKNOWN sans faux rollback | SERVICES60s ; CORElab32aperçus/128IDs ; bornes distinctes à négocier |
| Voix/temps | `voice.final01.events/1`, PilotWire V1, proposition Voice07 | START/FIRST_AUDIO/COMPLETE ne prouvent pas phonèmes/audibilité ; DTO final sans UUID/horloge ; V1 fixture ne permet pas vrai CORE | pilote4096octets, texte300UTF16/1200UTF8 ; sessionfinale4000segments |
| Animation/UI | UI CoreConversationTransport, AvatarV2 | OrigineLABORATORY uniquement ; manque ToolApproval/Citation complets et transport réel ; textures ne sont pas rig premium | texte/chunk16KiB ; total256KiB/256chunks ; manifeste64KiB,16textures/calques |
| Diagnostic | EVOL EvolutionEvent/LocalTelemetryService | Allowlist numérique fermée ; contrat intermodule absent. Schéma de revue proposé ci-dessous, sans déploiement | file64(max256), DB4MiB/2048lignes/7jours par défaut ; pas de texte libre |

Les limites en octets, caractères UTF-16 et tokens ne sont pas interchangeables.
`estimatedTokens` NEXUS ne devient jamais le tokenizer natif. Préserver les rôles
SYSTEM/question/historique/documents ; refuser une traduction qui perd l'origine.

## Exemples réellement validables, sans inventer un protocole opérationnel

Les exemples fermés existants [request valide](../../contracts/v1/examples/request-envelope.valid.json),
[request invalide](../../contracts/v1/examples/request-envelope.invalid.json),
[lease valide](../../contracts/v1/examples/resource-lease.valid.json) et
[lease invalide](../../contracts/v1/examples/resource-lease.invalid.json) restent
consommés par les tests historiques. Ils portent références privées, pas le contenu
d'une conversation. Ajouter ToolApproval, Citation ou profil numérique à ces schémas
fermés sans version/revue doit être refusé, pas accepté par un champ libre.

[F7 technical-health proposé](proposals/technical-health.schema.json),
[exemple valide synthétique](proposals/technical-health.valid.json),
[exemple invalide avec champ interdit](proposals/technical-health.invalid.json) :
`jarvis.technical-health/1-draft`, enums fermées, observation UUID, horloge monotone
locale, quatre métriques entières bornées seulement. Proposition **non approuvée**.
Les bornes proposées (latence90000ms, octets16GiB, file256) sont des limites de
sérialisation, jamais des budgets matériels ni une autorisation d'admission.
Aucun texte, chemin, prompt, conversation, profil, principal ou permission admis.
Le récepteur futur devra authentifier l'hôte et expurger avant la file, gérer
révocation/doublons/expiration ; le schéma seul ne garantit ni origine ni consentement.
La CLI `proposals` teste cette proposition hors ligne, jamais le runtime EVOLUTION.

## Menaces et protections à conserver

| Menace | Protection/validation attendue | État de cette tranche |
|---|---|---|
| Rejeu/reçu perdu | ID lié session/epoch/contenu, usage unique, UNKNOWN durable | Provenance documentée ; nouveau flux intermodules non testé |
| TOCTOU source/cible | hash relu, version et grant revérifiés avant effet/après retour ; destination SAF fraîche | Port DOCX désactivé, aucun effet réel ici |
| Prompt injection | document non fiable, jamais SYSTEM/permission ; citation relue | Écart de mapping LLM bloquant, pas de concaténation silencieuse |
| Confusion credentials | host principal/UID/certificat précis ; UUID n'est pas authentification | Pas d'IPC ou nouveau service activé |
| Unlink/révocation | invalider pending/retours tardifs par génération ; pas de confirmation réutilisée | À qualifier avec vrai CORE propriétaire |
| Processus mort/annulation | fin observée et journal conservé ; UNKNOWN refuse la réadmission | Aucune preuve native inventée, F3 bloquée |
| Batterie/thermique/RAM | bornes existantes et un lourd pilote ; ne pas monter seuils | Aucune modification de protections |
| Bibliothèque/asset douteux | SHA, ABI, licence/provenance, revue humaine | Licences projet UNKNOWN ; aucune distribution composée |
| Lock malveillant | schéma fermé, chemins sûrs, SHA/parents, pas de shell/build/fetch ; revue Git | Tests négatifs locaux de l'outil |
| CI étrangère/ancienne | SHA exact + dépôt exact ; parent vert non hérité | Refus automatisé dans validateur |
| Exfiltration diagnostic | schema closed et enums, aucun texte libre ; expurgation producteur | Exemples proposés testés, pas d'observateur connecté |
| Auto-correctif | signature/revue ne lève pas gate sandbox ; jamais auto-merge | Runner NOT_RUN/SANDBOX_NOT_QUALIFIED inchangé |

Les évolutions de contrats gelés, JNI/admission, activation IPC, signatures,
permissions critiques, installation physique, migration ou exécution de correctifs
restent aux validations distinctes indiquées dans l'issue. L'orientation ADR déjà
approuvée n'a pas à être revalidée ; ses choix techniques ouverts demeurent ouverts.
