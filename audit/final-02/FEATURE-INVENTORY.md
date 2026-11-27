# FINAL-02 — Inventaire des fonctionnalités réellement opérationnelles

APK V3 construit **uniquement depuis JARVIS-UNIFIED** (`modules/`). Niveaux de validation :

- **D** : développé ;
- **U** : test unitaire JVM ;
- **E** : émulateur Android (API 29 et/ou 35, mode avion) ;
- **A** : appareil réel.

**Aucune fonctionnalité n'est au niveau A** : rien n'a été installé sur ton téléphone.

Sources :

- [run 45899843578](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45899843578) (`cf8ab42`) : campagne complète ;
- [run 45900016272](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45900016272) : étude des modèles ;
- [run 45908509940](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45908509940) (`5db8f6b`) : rerun complet, 11/11 + 27/27 sur API 29 et 35 ; voir `TEST-REPORT.md`.

| Fonction | Module(s) | Niveau | Preuve (test) | État |
|---|---|---|---|---|
| Installation hors ligne, une seule permission (micro), pas d'INTERNET | INTERFACE | U + E | `a_manifestSinglePermissionNoNetworkInstallable` ; inspection de l'APK en CI | ✅ API 29 / 35 |
| Premier lancement, import vérifié des modèles (SHA-256, taille) | INTERFACE, LLM | E | `b_firstLaunchThenVerifiedImport` | ✅ API 29 / 35 |
| Moteur réel : états, cartes, menu, paysage, arrière-plan | INTERFACE, LLM | E | `c_realEngineStatesCardsMenuLandscapeBackground` | ✅ API 29 / 35 |
| Conversation texte avec contexte, persona, reprise | CORE (mémoire), INTERFACE | E | `f_conversationContextPersonaResume`, `n_resumeKeepsSystemNotices`, `s_tornJournalLine…` | ✅ |
| Connaissances locales citées ; « je ne trouve pas » si absent | NEXUS | E | `g_localKnowledgeCitedAnswer`, `c8_…`, `r_absentValue…`, `a3_knowledgeImport…` | ✅ |
| Mémoire avec consentement (proposer → confirmer → rappeler → supprimer) | CORE | U + E | `h_consentedMemory…` ; audits `a5`, `b3`, `g6`, `f6` | ✅ au rerun `5db8f6b` (API 29 et 35) ; un FAIL instable sur API 35 au run `cf8ab42` (`StaleObjectException` d'UiAutomator) |
| Conversation longue, bornée et cohérente | LLM, INTERFACE | E | `i_longConversation…`, `m_longConversationMemoryAndLatency` | ✅ |
| Défense contre les injections dans un document | NEXUS, LLM | E | `l_hiddenInjections…`, `q_unseenInjections…`, `f2f3f4_…` | ✅ |
| Sphère / avatar : immobile hors réponse, animée pendant la réponse | INTERFACE | E | `p_sphereStillAndCheapOutsideTheAnswer`, `k_…`, `d_reducedMotion…` | ✅ (0 dessin au repos et en réflexion ; visibleChange de 0,17 à 0,19 pendant la réponse) |
| Mise en page, accessibilité, avatar | INTERFACE | E | `e2e3e6e7_layoutStressAccessibilityAvatar` | ✅ |
| Interruption (Stop) à chaque étape | LLM, VOICE | E | `d3_interruptionAtEachStage` ; étude : Stop → retour en 1–2 ms | ✅ |
| Erreurs vocales sans blocage ni doublon ; micro révoqué → le texte marche | VOICE | E (simulé) | `d2_…`, `g1_microphoneRevokedTextStillWorks` | ✅ en émulateur, **voix réelle non testée** (pas de micro ni de haut-parleur réels) |
| Refus du tour en thermique sévère | INTERFACE, LLM | E (simulé) | `g2_thermalSevereRefusesTurn` | ✅ en simulation |
| Stockage plein refusé proprement ; base corrompue refusée et conservée | CORE | E | `t_storageFull…`, `a4_corruptFutureAndSymlink…`, `o_historyWriteFailure…` | ✅ |
| Cycles chargement / déchargement sans fuite | LLM | E | audit `h4_loadUnloadCyclesDoNotLeak` ; étude : PSS → ≈ 85 Mio après déchargement | ✅ au rerun (−38 et −1,4 Mio) ; un FAIL instable sur API 29 au run `cf8ab42` (mesure PSS bruitée sur l'émulateur) |
| Cycle de vie de session sans interblocage | INTERFACE | E | `j_sessionLifecycleNeverDeadlocks` | ✅ |
| Galerie et banc de rendu | INTERFACE | E | `e_galleryCapturesAndBeforeAfterBench` (GPU logiciel, non représentatif) | ✅ |
| Réouverture après arrêt forcé, aucun plantage | INTERFACE | E | `reopen_after_force_stop`, `no_crash` | ✅ |
| Catalogue de modèles ÉCO / ÉQUILIBRÉ / PERFORMANCE, avec repli automatique vers ÉCO | INTERFACE (NEXT-01) | U | `ModelCatalogTest` (6), `ModelStoreTest` (3) | ✅ en test unitaire ; profil affiché dans Command Center |
| Import vérifié du 1.7B (SHA-256, écriture atomique, refus si l'espace manque) | INTERFACE (NEXT-01) | U | `ModelStoreTest` | ✅ en test unitaire ; **désactivé par défaut** |
| Qwen3 1.7B dans l'application | LLM, INTERFACE | E (étude) | `ModelStudyTest` (emu35) | ⚠️ fonctionne, mais 4/59 tours dépassent 90 s à 768/1 ; pas le modèle par défaut |
| SERVICES | SERVICES | — | — | **Désactivé** (ISOLATED_OFF), pas embarqué |
| EVOLUTION | EVOLUTION | U | 61/61 en lecture seule (F08) | **Diagnostic uniquement**, pas embarqué, sandbox non qualifiée |
