# Feuille de route 001F — missions proposées P0 à P3

Aucune mission ci-dessous n’est commencée par cette clôture. Chaque mission
nécessite une autorisation distincte dans son dépôt propriétaire. Branche dédiée,
aucune fusion principale ni déploiement sans accord. Commencer par enregistrer le
SHA courant et archiver les preuves ; les têtes citées ici sont datées dans
[repositories.json](../registry/repositories.json).

| Priorité / mission | Propriétaire / branche proposée | Dépendances et fichiers prévus | Acceptation testable / risque / validation humaine |
|---|---|---|---|
| P0-PUBLISH | UNIFIED / mission-001f-closure existante | Droits rétablis ; registre et rapports existants | Push sans force, SHA/fichiers identiques, PR brouillon ; main inchangée. Risque : droits/confidentialité ; humain rétablit accès et relit PR |
| P0-ADR | CENTRAL + UNIFIED / decision/adr-001 | Revue 001F ; ADR et note de décision | Réponse explicite et objections enregistrées ; aucun transport adopté implicitement. Risque : confondre rôle logique et nombre d’APK ; humain décide |
| P0-CORE | JAVIS-Local-v2 / stabilization/current-core | Autorisation dédiée, tête226e2e8 à revérifier ; AppGraph/JarvisCore, LocalDatabase, WavRecorder et tests associés | Tests commandes/heure, SQLite V1→V2+échec, PDF/RAG, capture/lifecycle et annulation ; restauration fictive démontrée. Risques : perte/race/legacy mémoire ; humain valide symptômes et essais prudents |
| P0-LLM | JARVIS-LLM / qualification/003b-devices | Appareils et modèles déjà locaux, code003B1756e29 à revérifier ; ESSAIS_MEMOIRE_003B.md, rapports synthétiques | Redmi/POCO : mesures froid/chaud/repos, PSS, capteurs, arrêt effectif ; si admission refusée conserver refus, pas de benchmark forcé. Risque : RAM/chauffe ; accord humain pour essai et toute modification de seuil |
| P0-VOICE | JARVIS-VOICE / qualification/005i-xiaomi | 005H et sauvegarde privée conservées, pack exact local ; TEST-XIAOMI et rapport sans audio personnel | Restauration B locale, même UUID/SHA, écoute A/B, Arrêt, mode avion et métriques disponibles ; conserver H si échec. Risques : voix/données/signature ; propriétaire écoute et confirme, aucune archive au cloud |
| P0-UI-CI | JARVIS-INTERFACE / diagnosis/mission-002-ci | Lecture Actions autorisée, SHA d1c0931 à revérifier ; workflow, Gradle/tests si défaut confirmé | Diagnostic exact job/SHA/URL ; tests JVM et instrumentation distingués. Ne pas présumer CI rouge. Risque : défaut setup ou ABI ; humain valide toute correction produit et appareil |
| P1-E2E-SPEC | UNIFIED / contracts/core-llm-pilot | ADR approuvée, CORE stable, LLM qualifié ; contrats/plan/tests de spécification | Définir transport, mapping, quotas, identité, sessions/baux, rollback et scénarios négatifs avant code ; aucune prétention de liaison par mock. Risque : surface IPC ; revue humaine sécurité/contrat |
| P1-E2E-CORE | JAVIS-Local-v2 / integration/llm-pilot | P1-E2E-SPEC autorisée ; adaptateur et tests, fichiers exacts à fixer après choix transport | CORE→LLM→CORE réellement testé, annulation, délais, mauvais certificat, module absent, mort de processus ; un modèle résident ; ancien mode sélectionnable sans double chargement. Risque : perte/duplication ; aucun déploiement avant consentement |
| P1-E2E-LLM | JARVIS-LLM / integration/core-pilot | Mission distincte coordonnée avec P1-E2E-CORE ; endpoint uniquement si nécessaire, tests transport | Vérifier fin native/libération, interprocessus sur cible, mode avion, incompatibilité négociée ; même preuve E2E SHA des deux côtés. Risque : IPC/mémoire ; accord séparé pour code et installation |
| P2-VOICE | CORE puis VOICE, deux missions / integration/voice-pilot | P1 et qualification005I ; mapping DTO/enveloppe et tests dans chaque dépôt | Synthèse personnalisée de bout en bout, profil/pack exact, annulation/refus, pas de TTS générique substitué ; ancien parcours intact. Risque : voix/RAM ; écoute humaine obligatoire |
| P2-UI | INTERFACE puis CORE / integration/ui-pilot | P1, CI UI comprise, contrat événements ; adaptateur UI et tests | État/erreurs/cancel visibles, UI lifecycle et avatar2.5D réellement rendu séparément qualifiés ; CORE historique utilisable. Risque : UI bloquée ; validation visuelle humaine |
| P2-NEXUS | NEXUS puis CORE / design/knowledge-memory | ADR, export Android cohérent d’abord ; contrats documents/mémoire/Kiwix, tests fixtures | Citations/index/revisions, consentement précis, refus d’import incompatible et rollback ; aucune extraction de données réelles. Risque : migration/perte/mémoire implicite ; confirmation humaine avant transfert |
| P2-SERVICES | SERVICES puis CORE / design/authorized-tools | P1, permissions par outil ; capacités/quotas/tests de refus | Outils optionnels désactivables, aucun appel implicite depuis documents/LLM ; refus fermé. Risque : effets externes ; autorisations par action |
| P3-EVOLUTION | Dépôt à confirmer / design/isolated-patches | Identité validée et preuves stables ; sandbox, format patch, tests | Correctif proposé isolé, revue/tests/rollback, aucun auto-déploiement. Risque : exécution non autorisée ; humain accepte chaque patch |
| P3-CENTRAL-PC | UNIFIED spécification puis dépôts runtime / design/local-pc | Export/restauration réels qualifiés, transport local authentifié, modèles/licences à qualifier | Archive portable restaurée sans perte, Android autonome hors ligne, panne PC récupérable ; modèles non téléchargés automatiquement. Risque : incompatibilité/identité/réseau ; validation humaine matériel et migration |

Pour toutes les lignes, non-régression : conserver les fonctions, seuils,
signatures et données existants jusqu’à preuve de parité et restauration ; ne pas
supprimer une ancienne installation pour simplifier les tests. Une mission qui
touche deux modules devient deux autorisations et deux PR liées, jamais une
permission globale de modifier les dépôts. Après chaque PR/fusion **approuvée**,
actualiser l’inventaire selon [RUNBOOK](RUNBOOK.md) ; GitHub n’est pas requis au runtime.
