# D4-02 — risques de régression, protections et preuves attendues

Aucun contrôle futur ci-dessous n’est présenté comme implémenté par cette mission.
La preuve existante est séparée de la preuve requise pour un raccordement réel.

| Gravité / risque | Observation actuelle | Protection proposée / critère bloquant |
|---|---|---|
| Critique : double résidence | CORE004A préchauffe toujours son wrapper ; LLM coordonne son processus seulement | Factory exclusive avant warm-up, gate sur tous chemins participants, fin/déchargement prouvés avant bascule ; refuser si inconnu |
| Critique : données perdues/dupliquées | SQLite CORE, SERVICES propres, NEXUS futur ; pas d’export global Android opérationnel prouvé | Aucun déplacement initial ; writer unique par objet ; sauvegarde cohérente et restauration isolée avant migration ; pas de double-write ni reset sur schéma inconnu |
| Critique : mémoire sans confirmation | /remember CORE reste direct ; Memory SERVICES confirmation interne ≠ preuve externe | Aperçu exact+version+acte, confirmation CORE, contrôle destination ; refuser si contenu/base modifiés ; aucun legacy effacé ni automatiquement confirmé |
| Élevée : faux arrêt | CORE NonCancellable + drainage ; LocalLanguageModel sans stop/unload public ; LLM requestStop n’est pas retour natif | Pas de libération au timeout, états séparés, test JNI et erreur partielle ; pas de nouveau moteur sur déconnexion |
| Élevée : dégradation du prompt | CORE systemPrompt configurable et texte RAG ; LLM system natif fixe et messages limités | Choix P1/P2 explicite, budget tokenizer, provenance des extraits, aucun rôle système déclassé en user ou ignoré |
| Élevée : garde matérielle contournée | Backend seul n’est pas l’ensemble SafetyPolicy/admission/UI | Pipeline partagé avec validations, GGUF SHA, réserves conservées, API/capteurs inconnus→refus ; mesures physiques, aucun seuil abaissé |
| Élevée : identité IPC usurpée | Aucun endpoint actuel prouvé ; certificats de production/appareils inconnus | Décision identité puis UID/package/certificat et permission adaptée ; service non exporté sauf export dédié justifié ; mauvais client refuse sans donnée ni chargement |
| Élevée : dépendance/signature ou SDK régressés | CORE24, LLM29, VOICE26 ; clés et ABI différentes possibles | Conserver packages/signatures/modes API24–28, pas de re-signing ou relèvement minSdk implicite ; tests de compatibilité et installation séparément autorisée |
| Élevée : faux « sources » ou action | LlmPort SERVICES mock retourne des citations, vrai LanguageModel renvoie texte | Sources gardées par propriétaire, pas de citation inventée ; simulated visible ; génération n’exécute ni outil ni souvenir |
| Élevée : voix dégradée/profil perdu | Studio005J et LocalTts séparés ;005K n’est que cahier | Hors premier pilote ; conserver consentement et pack/profil, archives privées et sons ; aucun TTS générique substitué silencieusement |
| Élevée : helper TLS tiers ou parseur | Rapports CORE004A et SERVICES002A conservent avertissements tiers trust-all | Revue des dépendances et atteignabilité avant toute surface transport ; ne pas activer helper ni masquer Lint ; aucun transport réseau introduit ici |
| Modérée : catalogue concurrent | Réponses simples CORE et catalogue LLM sont des chemins distincts | CORE garde commandes, catalogue existant hébergé LLM, délégation éditoriale seulement après parité ; pas d’index ou base copiés |
| Modérée : preuves périmées | Nouvelles branches004A/003C/002A absentes de l’ancien instantané | SHA/date/portée par lecture ; rapports versionnés ≠ CI actuelle ; tests UNIFIED ≠ native E2E |

La suppression logique et les durées d’expiration SERVICES ne garantissent pas
la non-résurrection SYNC. Ne pas activer sync/transfert pour fournir une mémoire
au premier pilote ; causalité/tombstones/purge sont des sujets D4-01/D4-06 distincts.
Un lock logiciel ne réserve pas la RAM et ne maîtrise pas les applications tierces.
L’ADR permet une future multi-résidence qualifiée, jamais un essai improvisé sur mobile.
