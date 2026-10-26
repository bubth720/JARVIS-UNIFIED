# JARVIS — Mission directrice CODEX PRE-FUSION / 2026-10-26

**Mise en place** : dans `bubth720/JARVIS-UNIFIED`, branche `mission/prefusion-gates-20261026` issue de `feat/uni-08-u02-modular-workspace` commit `ade69697f55d425f871e4e3b90c7155bf7657d7a`.

**Objet** : qualifier les huit modules avant d'étudier une véritable fusion. Cette mission **n'est pas une autorisation de fusion**, de migration de dépôt, de modification des contrats gelés, de connexion sensible ou de déploiement. L'architecture cible est un produit unique avec modules autonomes, pas un monolithe. Le manifeste de workspace est une photo documentaire, pas un APK.

## 1. Entrées directes : missions propriétaires

Chaque module a sa mission versionnée sous `missions/PREFUSION-2026-10-26.md` sur la branche **`mission/prefusion-gates-20261026`** du dépôt indiqué. Ouvrir **ces documents sur leur branche mission** (pas sur main).

| Ordre | Module | Mission | Dépôt / référence consultable | Dépendance |
|---|---|---|---|---|
| A | UNIFIED | UNI-PF-01 | [Mission centrale](https://github.com/bubth720/JARVIS-UNIFIED/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | Aucune, coordonne |
| A | NEXUS | NEX-PF-01 | [Mission NEXUS](https://github.com/bubth720/JARVIS-NEXUS/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | Backend FTS5/Android et preuve SAF |
| A | SERVICES | SERV-PF-01 | [Mission SERVICES](https://github.com/bubth720/JARVIS-SERVICES/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | API35 SAF et autorité commit |
| A | LLM | LLM-PF-01 | [Mission LLM](https://github.com/bubth720/JARVIS-LLM/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | JNI GGUF/budgets, hors phase documentaire |
| A | VOICE | VOICE-PF-01 | [Mission VOICE](https://github.com/bubth720/JARVIS-VOICE/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | PCM/émotions/latence, hors phase documentaire |
| B | CORE | CORE-PF-01 | [Mission CORE](https://github.com/bubth720/JAVIS-Local-v2/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | NEXUS/SERVICES qualifiés et ADR-002 avant écriture |
| B | INTERFACE | UI-PF-01 | [Mission INTERFACE](https://github.com/bubth720/JARVIS-INTERFACE/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | CORE transport authentifié avant activation |
| B | EVOLUTION | EVOL-PF-01 | [Mission EVOLUTION](https://github.com/bubth720/JARVIS-VOLUTION-/blob/mission/prefusion-gates-20261026/missions/PREFUSION-2026-10-26.md) | Sandbox réelle sans auto-application |

**Attention** : A et B sont des priorités de livraison, non une autorisation d'exécuter des actions sensibles. Les travaux OFF/dry-run de CORE/INTERFACE/EVOLUTION peuvent débuter en parallèle, mais **leurs raccordements actifs attendent les gates**.

## 2. Mission UNIFIED spécifique : UNI-PF-01

### U0 — Capturer état vérifiable
Lire `AGENTS.md`, `docs/uni-08/ADR-002-PROPOSAL.md`, `workspace/README.md`, `workspace/modular-workspace.proposed.json`, `tooling/integration/uni08_candidate.py` et le code de chaque dépôt propriétaire aux SHA des missions. Vérifier `git rev-parse` et les CI exactes. Ne pas reprendre comme actuels les succès d'ancêtres.

### U1 — Arbitrer les contradictions des contrats (préparation uniquement)
Comparer CORE (SessionCoordinator, FUSION-02 C0), SERVICES (CommitAuthorization proposal/1, ServicesWirePreflight) et les schémas UNIFIED /2-draft. Formaliser décision **non approuvée** sur génération 0 versus 1..2^53-1, `COMMIT_STARTED` versus `DISPATCHED`, `COMPLETED` versus `COMMITTED`, journal durable, consentement unique, révocation au point d'engagement, erreur UNKNOWN sans retry et preuve de readback. **Ne pas imposer une conversion, ni activer export avant validation humaine.**

### U2 — Matrice de compatibilité Android et modules
Épingler branche, commit SHA40, minSdk, ABI/JNI, Java/Gradle/Kotlin, dépendances et licences, schémas de données, objets publics et version des contrats. Signaler explicitement CORE API24, NEXUS/SERVICES API24, INTERFACE/VOICE API26, LLM API29 (référence examinée) ; un minSdk24 global n'assure pas un LLM API29. Chaque propriétaire fournit résultat CI/JVM/Robolectric/émulateur/physique séparé. Aucune qualification depuis le manifest seul.

### U3 — Préparer assemblage **modulaire et réversible** (pas importer tous les codes)
Documenter le choix entre fédération multi-repo avec lockfile et monorepo modulaire ; proposer pipeline changed-module et validation des contrats consommateurs, puis pipeline complet avant release. Interdire l'import réel d'historiques, les submodules auto-fetch runtime, les modifications de chemins Gradle et les migrations sans approbation formelle. Conserver l'autonomie des applis lors de la transition.

### U4 — Essai bout-en-bout *proposé*, fail-closed
Spécifier scénario hors ligne Android : entrée TXT/PDF autorisée → source NEXUS SHA/page/offset → CORE → SERVICES CSV/export vers nouveau document avec consentement, ACK/relecture et original intact. Le RAG FTS5 API24/25 et l'export production restent aujourd'hui BLOQUÉS ; n'inventer ni pilote opérationnel ni APK final. Les voies LLM/VOICE/AVATAR et EVOLUTION sont optionnelles et ne doivent pas bloquer le premier pilote lecture/CSV.

### U5 — Qualification et paquet de revue
Exécuter `python3 workspace/check_plan.py workspace/modular-workspace.proposed.json`, `python3 -m unittest discover -s workspace/tests -v`, suites U00/U01 et validateurs historiques ; publier CI au HEAD exact, PR brouillon, matrice et rapport `docs/prefusion/ASSESSMENT.md` avec états PASS/BLOCKED/NOT_RUN, preuves et exigences de validation. Ne pas falsifier FUSION-02 ni lever un gate à partir d'une CI partielle.

## 3. Instructions d'exécution aux agents Codex

- Sur **chaque dépôt** : consulter la mission sur la branche indiquée et `AGENTS.md` si présent ; créer une **nouvelle branche de développement** à partir du SHA HEAD vérifié de la branche mission ; faire une étape courte, testable, commitable et réversible à la fois.
- Faire des commits et PR **brouillon vers la branche de mission ou base explicitement sélectionnée**, jamais directement vers main.
- Aucune suppression de test, aucune augmentation de minSdk, aucune permission Internet/runtime, aucun transfert de voix personnelles, aucun merge, déploiement, clé, action ou écriture réelle sans validation. Les agents ne se bloquent pas mutuellement : publication de contrats sur branches séparées et revues avant adoption.
- Distinguer version de proposition et contrat approuvé ; `CONNECTED` ≠ `READY`, test JVM ≠ preuve Android, logiciel vert ≠ résultat sur appareil.
- À chaque étape, rendre : **module, mission, branche, commit, PR, commandes, tests/échecs/skips/non exécutés, CI source SHA, dépendances, blocages, rollback, prochaine action**. Si une autorisation manque : STOP, livrer un ADR et un plan, demander décision.

## 4. Points de décision réservés à l'utilisateur

1. Accepter ou refuser **l'architecture effective** mono-dépôt ou workspace fédéré et les imports Git (actuellement seulement une proposition U02).
2. Accepter ou refuser **ADR-002** et l'activation d'une autorité d'écriture CORE/SERVICES.
3. Accepter ou refuser nouveau backend SQLite Android, changement de licence/ABI, migration persistante ou installation sur appareil personnel.
4. Autoriser séparément tout merge `main`, après preuves et revue.

## 5. Commande courte pour Codex

**Dans le dépôt JARVIS-UNIFIED, ouvre ce fichier depuis la branche mission/prefusion-gates-20261026 ; suis ses liens vers les sept missions propriétaires et exécute uniquement les phases non sensibles sur branches dédiées. Publie les commits, tests et PR brouillon. Aucun merge main ni activation sensible ; stop aux décisions d'architecture.**

Cette mission est une feuille de route publiée, **pas une exécution automatique** par Codex.
