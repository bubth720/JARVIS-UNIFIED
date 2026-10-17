# JARVIS CENTRAL — Validation des deux révisions pour poursuivre le développement

**Décision utilisateur :** 17 octobre 2026.  
**Statut :** APPROUVÉE DANS LE PÉRIMÈTRE EXPÉRIMENTAL CI-DESSOUS.  
**Autorité :** confirmation explicite « Très bien faisons ça et continuons », donnée après présentation du bilan et de la proposition d'approuver `IDENTITY 001B.1` et `D4-02E.1`, puis de préparer CORE ID-002 et la correction LLM 003F.

## Références immuables

- Constitution/architecture ID-001 déjà approuvées séparément : `design/identity-001-constitution`, `db63719c09435fd2e7863dd72e7bec0e055fa32e` ; approbation enregistrée `1748cb0706fa4b0cfac2df963d82a14195b9d25a`. Ne pas redemander la même décision.
- IDENTITY 001B.1 : dépôt `bubth720/JARVIS-UNIFIED`, branche `design/identity-001b-contract-freeze`, **commit `d7c90785ae4263892a6c96e140cfa88206cb4197`**. Bundle de **14 fichiers normatifs**, `docs/IDENTITY/001B/BUNDLE.json`, SHA-256 **`431b5212f742bd9028477a6a603acf328c414801873efdd529f45b6ed5e619de`**.
- Clarification D4-02E.1 : dépôt `bubth720/JARVIS-UNIFIED`, branche `design/d4-02e-f1-f2-recovery-clarification`, **commit `49dd4027d2ccb54bf330f591d3ee17f5dc577132`** ; documents `docs/D4-02E/{DECISIONS_F1_F2,COMMIT_CANONIQUE,CONTRAT_DIFF_PROPOSE,MISSIONS_CORRECTION_003F}.md`, `TABLES_PROPOSEES.json`, `TABLES_DIFF.json`, `vectors.json`.
- LLM 003F base courante : `bubth720/JARVIS-LLM`, `fixture/003f-bootstrap-attestation`, `111be993e970051686bd5c27b3115320513a4be7`, CI verte exécutée au code `b2f6bc052871a2e4f604d9170f385b71c241837b`, blocages F1/F2/F3 documentés. Le bundle /2 **candidat bloqué** `4b4129b595b78481d846c521993026fe2477c64fccfe4259ba9a5e30f9d68e62` n'est PAS adopté pour CORE.
- CORE référence de revue : `bubth720/JAVIS-Local-v2`, `fixture/004c-p2-client`, `da40ed7155409b85860a22c1dbbfe35029cea29a`. Ce n'est pas une base fusionnée automatiquement.

## Décision A — IDENTITY 001B.1 acceptée pour CORE ID-002

Accepter **les octets exacts** du bundle épinglé : styles fermés `ASSERTIVE/CALM`, `WARM/NEUTRAL`, `CONCISE/BALANCED/DETAILED`, `OFF/LIGHT`, `EVIDENCE_FIRST`, `VOUS/TU`; persona B, fr-FR, contrôles de types, bornes, canonicalisation et six vecteurs comme données de référence. Le manifeste ne confère aucun droit d'outil, permission ou consentement.

Autoriser la préparation de CORE ID-002 dans une branche propre après audit/choix explicite d'une base compatible. Le codec Kotlin/Android n'a **pas encore été implémenté ni testé** : il devra reproduire les six vecteurs et refuser les données invalides. Port IdentityPort **technique en lecture seule**, snapshot immuable, manifeste approuvé, opt-in, SYSTEM uniquement ; contrôle du prompt complet avec template/tokenizer réel. Tokenizer absent ou modèle incompatible : refus sûr, sans troncature ni modification des réglages existants.

Les schémas de consentement et préférences servent ici à définir des types, pas à autoriser une écriture de données personnelles. ID-003, migrations, restauration et persistance personnelle exigent mission/validation distinctes. Toute altération normative du bundle/change de SHA appelle une nouvelle revue.

## Décision B — D4-02E.1 acceptée pour la correction LLM 003F

Approuver la **clarification de conception** D4-02E.1 comme cible expérimentale, sans valider automatiquement son futur code :
1. F1 : DISCOVER apporte `core_process_epoch`, `broker_epoch`, émission/expiration ; CORE est propriétaire de ses incarnations, UID/cert/permission et liaison au nonce contrôlés.
2. F2 : chaque pair atteste son **propre** journal. INSPECT/SNAPSHOT LLM ne prétendent pas lire la sandbox CORE ; CORE_PREPARE est la preuve locale CORE sous canal authentifié ; cohérence de génération, opération et état strictement vérifiée.
3. COMMIT : deux preuves complètes corrélées (CORE_PREPARE, ATTEST) et digests canoniques étiquetés, journal/outboxes durables sans autoréférence, fsync/ACK, replay interdit.
4. F3 : cadrer et instrumenter les états réels du worker, des appels JNI retournés, handles, imports et baux sans ajouter un second moteur ni simuler la libération. Retenir UNKNOWN/CLEANUP_FAILED si preuve incomplète. Toute extension sensible au runtime historique/native dépassant le périmètre de fixture demande revue et autorisation spécifique.

La correction LLM doit produire de **nouveaux** CONTRACT/TABLES/vecteurs/codec, SHA du bundle calculé depuis les fichiers effectivement testés, suites/CI et rapport par plateforme. L'ancien /1 reste inchangé ; aucun downgrade. **CORE 004D n'est pas autorisée à consommer le bundle candidat actuel**. Elle reste bloquée jusqu'à livraison et revue complète du nouveau bundle /2 et preuve F3.

## Autorisations de mission et interdictions

- Préparer une mission Codex LLM ciblée F1/F2/COMMIT, puis F3 sous gate technique, dans **LLM seulement**.
- Préparer la mission CORE ID-002 et lancer d'abord l'audit de base/compatibilité; implémentation strictement limitée au socle identité après contrôle du bundle exact. Éviter tout couplage aux fixtures /2.
- Aucune fusion ni modification de `main`, aucun auto-merge, aucune installation/téléchargement personnel, aucune migration, aucune suppression de données, aucun accès à des secrets privés, aucune nouvelle permission ni recul thermique/batterie/RAM Android. Pas d'activation PLEINE PUISSANCE Android.
- Consentement exact avant mémorisation durable d'une donnée personnelle ; ni modèle, document ou persona ne se valide des droits. Aucun essai Android physique ou E2E natif revendiqué sur une simple CI.
- Chaque livraison consigne module, mission, branche, SHA, tests réellement exécutés, blocages et prochaine action. L'exécution des missions par Codex n'est **pas** déclenchée automatiquement par une issue GitHub.

Cette décision ne fusionne pas les deux branches documentaires UNIFIED : elles demeurent indépendantes ; les références exactes ci-dessus constituent l'accord.
