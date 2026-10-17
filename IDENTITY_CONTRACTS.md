# ID-001 — structures et compatibilité proposées

**Spécification documentaire jarvis.identity/1-draft, non approuvée et non codée.**
Ce namespace conceptuel est distinct de UNIFIED contracts/v1, SERVICES contracts/v1,
CoreVoiceRequestV1 et jarvis.fixture.p2/1 ou /2. Aucun fichier de schéma existant
modifié, aucune nouvelle méthode Binder, aucun déploiement de codec.

## Types proposés

| Type | Champs et invariants proposés |
|---|---|
| IdentityManifest | schema_version, identity_id, revision, constitution_ref/digest, policy_ref/digest, traits, allowed_styles, default_locale, composer_revision, provenance. Configuration technique sans données privées ; traits dans vocabulaire fermé à geler, pas texte de commande d’outil |
| IdentityPolicy | policy_id/revision, allowed_style_keys/values, data_scopes, capability_requirements, privacy_rules, expiry_rules. Contraintes effectives calculées par CORE à partir des politiques de sécurité, jamais élargies par manifeste ou modèle |
| IdentitySnapshot | snapshot_id, identity_id/revision/digest, policy_revision/digest, preference_revision, consent_revision, storage_owner/ref, composer_revision, session_id, created_at, expiry, content_digest. Valeurs résolues immuables, catégories/provenance conservées, pas URI/poids vocaux |
| IdentityPreference | preference_id, category=PROGRAMMED_STYLE ou USER_PREFERENCE, key, typed_value, subject_scope, owner_namespace, base_revision, provenance, created_at/expires_at, decision_ref, sensitivity. Une donnée personnelle ne devient pas publique parce qu’elle est appelée preference |
| IdentityChangeProposal | proposal_id/revision, proposer, target_namespace/id, base_revision/digest, exact_patch, rationale_ref, provenance_refs, sensitivity, requested_scope, created_at/expires_at, decision_state, application_state. Proposer peut être utilisateur/CORE/EVOLUTION, jamais autorité implicite |
| IdentityDecisionReceipt | decision_id, proposal_id/revision/digest, exact_operation, subject/principal_ref, scope, base_revision/digest, UI_confirmation_ref, decided_at, valid_until, consent_revision, decision=APPROVED ou REJECTED. Référence authentifiée hors bande nécessaire ; UUID/digest seuls ne confèrent pas autorité |
| IdentityApplicationRecord | application_id, decision_ref, previous_revision/digest, resulting_revision/digest, transaction_id, outcome, rollback_ref, time. Durabilité transactionnelle et CAS sur version de base ; aucun grant d’outil persistant |
| IdentityExpressionIntent | session/correlation/cancellation refs, snapshot_ref, final_text_ref, bounded_style, requested_voice_identity_ref, visual_intent, capability_revision, expires_at. Référence privée au texte final exact ; n’est pas un clone vocal ni un appel d’outil |
| IdentityAssessment | proposition_kind=FACT/OPINION/HYPOTHESIS/PREFERENCE/INSTRUCTION/UNKNOWN, claim_ref, evidence_refs/revisions, freshness, uncertainty_reason, recommended_response. Évaluation proposée, pas moteur de vérité universelle ou autorisation |

Manifestes et snapshots sont des données inspectables, pas des scripts. Aucun
chemin arbitraire, code, shell, classe à charger, prompt de permission, modèle à
télécharger ou clé de signature ne peut être inclus comme trait. Les valeurs libres
personnelles ne sont pas interpolées telles quelles en SYSTEM ; préférences de style
passent par clés typées autorisées et rendu contrôlé. Souvenirs/docs restent des
contenus à provenance distincte, jamais une extension de l’identité programmée.

Identifiants opaques canoniques, révisions positives monotones, UUID de session
corrélés au CORE ; pas de réinitialisation au changement de modèle. Empreinte
SHA-256 d’une sérialisation canonique à figer avec vecteurs avant ID-002/003 : clés
triées, types explicitement vérifiés, aucune normalisation implicite des textes.
Les futurs codecs devront refuser doublons/champs inconnus/types faux et borner
UTF-8/profondeur/listes **avant construction**. Les bornes quantitatives des nouveaux
objets restent à geler en revue ; limites existantes ne sont jamais augmentées
par une borne IDENTITY. Absence de version/capacité/digest attendu = INCOMPATIBLE.
Aucun objet exécuté par désérialisation permissive d’une classe de confiance.

## Propositions et transaction d’approbation

États décisionnels : PENDING → APPROVED ou REJECTED. Pas de modification du patch
après décision ; tout nouveau contenu crée une nouvelle révision PENDING.
Expiration/révocation sont des événements séparés qui rendent l’usage invalide,
sans transformer un ancien APPROVED en nouvelle approbation ni perdre le refus.
États d’application distincts : NOT_APPLIED, STAGED, APPLIED, FAILED, ROLLED_BACK.
PENDING ou APPROVED seul n’autorise ni exécution sensible ni création de mémoire.

1. CORE classe contenu/risque/propriétaire. Proposition personnelle : brouillon
   volatil, sauf consentement explicite au stockage exact de cette proposition.
   Non-personnelle : stockage PENDING autorisé par politique du namespace.
2. Afficher patch exact, ancien/nouveau contenu, portée, finalité, expiration et
   conséquences. Enregistrer la décision explicite liée au digest **de tout cela**.
3. Vérifier principal, autorisation, contenu inchangé, base actuelle, validité,
   absence de révocation, compatibilité de politique et capacité du propriétaire.
4. Commit atomique décision/application/donnée et révision, ou procédure de journal
   de transaction conservatrice si plusieurs composants ne partagent pas une DB.
   Aucun succès annoncé avant durabilité et ACK ; erreur = état non appliqué/inconnu,
   pas réémission automatique d’une action sensible.
5. Au prochain point de session sûr, créer un nouveau snapshot, jamais muter celui
   d’un calcul en cours. Un changement de base entre aperçu et commit = CONFLICT,
   nouveau diff et nouvelle confirmation ; pas d’écrasement last-writer-wins.

Guard.confirm/consume existants restent des primitives in-process, délai60s/usage
unique. Un jeton consommé suivi d’un store.put raté ne constitue pas un reçu durable
ni une transaction multi-objet. ID-003 doit concevoir cette adaptation, en conservant
les refus et en sollicitant une nouvelle confirmation si le résultat est inconnu.
Un restore/export n’est pas une nouvelle approbation de chaque ancien candidat.

## IdentityPort : interface logique, transport encore ouvert

| Opération proposée | Autorité et effet |
|---|---|
| loadManifest / readApprovedState | Lecture bornée du namespace autorisé ; manifeste fiable et état privé explicitement séparés |
| createSnapshot | CORE résout un état approuvé/versionné, vérifie consentements et capacités ; état immuable de session |
| proposeChange | Candidat sans effet ; données personnelles volatiles sauf confirmation propre à leur stockage |
| decideProposal | Entrée de confiance CORE/UI avec contenu/diff exact ; ni document ni modèle ne peut l’appeler avec une décision auto-fabriquée |
| applyApprovedChange | CAS et transaction, mandat exact limité à cette application, aucune nouvelle permission |
| revoke / expire | Interdiction immédiate d’usage concerné et invalidation des sorties ; nettoyage de dérivés selon politique distincte |
| exportSelected / stageRestore / validateRestore / commitRestore | Sélection explicite, archive privée protégée, intégrité/versions, conflits et révocations ; aucune écriture directe dans DB historique |

Interface locale interchangeable pour SERVICES initial puis NEXUS cible ; pas de
nouveau service exporté, protocole réseau ou accès à une sandbox d’un autre APK
approuvé par ce texte. Si ID-003 n’est disponible que dans un autre processus,
ID-002 reste en mode manifeste embarqué/volatil jusqu’à adaptateur qualifié.
Le Guard.Context doit venir du vrai hôte de confiance ; aucun champ serialized
principal/APPROVED ne prouve l’identité. IPC éventuel exige contrat et validation
propres, sans réutiliser les fixtures d’inférence comme API de stockage.

## IdentityComposer et SYSTEM

Entrées : manifeste/snapshot approuvés, politique effective CORE, instructions
utilisateur autorisées, capacités exactes du backend/modèle et budgets existants.
Sortie : fragment SYSTEM contrôlé + manifeste technique de composition privé
(composer/model/template/snapshot digests, tailles et résultat de validation).
Aucune permission n’est dérivée du texte de sortie.

Ordre logique : politique de sécurité effective → constitution approuvée → traits
techniques autorisés → préférences confirmées typées → instruction de session
compatible. Le backend LLM reste propriétaire de sa politique fixe/template ;
le composer ne les copie pas. Le systemPrompt configurable existant conserve son
rôle et son contenu ; conflit avec la politique/constitution = refus ou aperçu
d’une modification explicitement approuvée, pas écrasement des préférences
historiques. ID-002 est opt-in et n’altère pas les réglages installés par défaut.
Ne pas ajouter la persona à question/context/user.
Si separateSystemPrompt=false, refuser le chemin identité ou signaler maintien du
mode historique sans persona ; aucune conversion silencieuse de rôle.

Le budget inclut SYSTEM complet, question, contexte/historique/sources conservés,
template/BOS/préfill et sortie. CORE possède actuellement un proxy UTF-8 prudent,
**pas un tokenizer réel**. P2 a une borne SYSTEM8192octets ; elle ne remplace pas
le plafond de tokens réel. Après composition, compteur du même modèle/template
que génération ; sinon chemin natif non qualifié/TOKENIZER_UNAVAILABLE.
En dépassement : refuser clairement ou proposer explicitement une configuration
moins riche **avant appel**, sans retirer politique, consentement, question,
provenance ni convertir en user. Pas de troncature cachée d’un snapshot approuvé.
ID-002 ne relève ni context_size, ni threads, ni RAM/thermique/batterie.

**Fixtures /2 exclues :** le candidat003F contrôle le bootstrap et refuse l’admission
native /2 ; le corpus /1 de référence est synthétique fermé. Ni nouveau SYSTEM
persona, ni champ identity, ni requête personnelle, ni assouplissement SYNTHETIC_ONLY
n’est autorisé. L’intégration IDENTITY exige une voie applicative ultérieure
qualifiée et un contrat distinct revu ; l’Alpha historique peut être évaluée
séparément, sans prétendre résoudre le raccordement inter-APK.

## Expression sans nouveau schéma VOICE/INTERFACE

Mapping futur, après accord ID-005 : style conversationnel → intention existante
CoreVoiceRequestV1 ; personaId VOICE sélectionné explicitement n’est pas identity_id
conversationnel. Vérifier profil/conditioning/moteur/pack et consentement VOICE ;
texte exact limité300caractères et contraintes tokenizer/durée réelles. Si trop
long, refuser vocalisation complète ou proposer un plan autorisé, jamais tronquer
ou réécrire silencieusement. Le texte intégral reste accessible.

NEUTRAL est le rendu validé dans le contrat lu ; HUMOROUS/SERIOUS et intensité/vitesse
sont métadonnées non acoustiques prises en charge actuellement. Une préférence
« humour » ne garantit ni rire ni prosodie. Inconnu/degradé signalé selon politique
VOICE existante. Intention visuelle proposée NEUTRAL/ATTENTIVE/THINKING/SPEAKING,
strictement bornée ; pas ajout à AvatarSession ni renderer supposé.
La priorité d’expression n’autorise jamais préemption d’un calcul/son natif.

## Erreurs et compatibilité

Codes proposés locaux : INCOMPATIBLE, UNAUTHORIZED, CONSENT_REQUIRED,
EXPIRED_OR_REVOKED, CONFLICT, CORRUPT_STATE, OWNER_UNAVAILABLE,
CAPABILITY_UNSUPPORTED, CONTEXT_EXCEEDED, TOKENIZER_UNAVAILABLE, CANCELLED,
STALE_SESSION, APPLY_FAILED, RESTORE_BLOCKED, CLEANUP_UNCONFIRMED.
Ne pas les ajouter aux enums/enveloppes v1 actuelles ; futur mapping explicite
avec détails privés versionnés, jamais parse du texte d’une exception.

Chaque réponse conserve session/request/correlation, snapshot/revision et état
terminal réel. Réponse tardive ou snapshot révoqué : pas d’assistant persistant,
TTS/cache/animation tardifs ni proposition personnelle durable. Annulation ne
vaut ni retour natif ni libération ; le même arbitre/gates existants s’appliquent.
Changement de modèle : snapshot logique stable, nouveau contrôle de capacités et
budget, aucune promesse de formulations identiques ou de performance non mesurée.
