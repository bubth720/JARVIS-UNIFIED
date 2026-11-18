# Registre central des anomalies — JARVIS (AUDIT-GLOBAL-01)

Source : `registre.json` (ce fichier est généré par `render_registre.py`). Mise à jour : 2026-11-18.

Natures : **DEFAUT_CONFIRME** (prouvé), **RISQUE_THEORIQUE** (non observé), **FONCTION_ABSENTE**, **LIMITATION_ENVIRONNEMENT**, **LIMITATION_MODELE**.

| ID | Module | Nature | Gravité | Statut | Développée | Test unitaire | Émulateur | Appareil réel | Symptôme |
|---|---|---|---|---|---|---|---|---|---|
| A-001 | UNIFIED (CI) | DEFAUT_CONFIRME | majeure | validé | b7c146a | — | CI verte (6 portes) | — | Les portes historiques UNI-08 et FUSION-02 échouent sur la branche de développement. |
| A-002 | LLM (CI A02) | DEFAUT_CONFIRME | majeure | validé | LLM 9c3fc50 | — | CI verte | — | La porte « A02 sealed GGUF native loader » est rouge en permanence. |
| A-003 | VOICE | DEFAUT_CONFIRME | majeure | validé | VOICE 5890735 | — | CI verte | — | Le commit VOICE utilisé par l'application échoue à ses propres gardes de préservation. |
| A-004 | LLM (Qwen3-0.6B) | LIMITATION_MODELE | critique | ouvert | — | — | — | — | Affirmations factuelles fausses et assurées. |
| A-005 | LLM + NEXUS | DEFAUT_CONFIRME | majeure | à retester | 3dd3649 puis 1354e31 (réponse déterministe) | DocumentaryAnswerTest | NON : c8 rouge sur run 43658134254 (8f77a8d, API 29+35) (« Londres » + note) ; nouveau contrat à exécuter | — | Réponse documentaire inventée quand aucun document ne contient l'information. |
| A-006 | LLM + INTERFACE | DEFAUT_CONFIRME | critique | validé | 3d07d24 | ActionGuardTest | test f vert API 29/35 | — | JARVIS prétend avoir exécuté une action (« La lumière du salon est allumée »). |
| A-007 | INTERFACE conv (mémoire de travail) | DEFAUT_CONFIRME | majeure | validé | f32b2ee | ConversationContextTest | run 43616811194 8/8 | — | « Comment je m'appelle ? » → prénom du frère. |
| A-008 | INTERFACE (sphère) | DEFAUT_CONFIRME | majeure | ouvert | 7ca95a4, e79df9f, 8f77a8d | — | NON : K rouge sur run 43658134254 (8f77a8d, API 29+35) (2 dessins / fenêtre, aussi au repos) ; test P (pixels + coût séparés) à exécuter | — | La sphère se redessine pendant l'écoute (11–13 images). |
| A-009 | NEXUS sur Android | DEFAUT_CONFIRME | critique | validé | 2066753 | — | test g vert API 29/35 | — | Recherche documentaire impossible. |
| A-010 | MEMORY VAULT | DEFAUT_CONFIRME | majeure | validé | 4ee4bc3 | — | B3 vert sur run 43658134254 (8f77a8d, API 29+35) | — | Les souvenirs en statut NEEDS_CONFIRMATION (égalité ambiguë) sont injectés comme s'ils étaient READY. |
| A-011 | INTERFACE (tests) | DEFAUT_CONFIRME | mineure | à retester | 3dd3649, 8656904 | — | partiel : c rouge sur API 35 (run 43658134254 (8f77a8d, API 29+35), onglet cc-tab-missions introuvable) | — | Échecs instables : StaleObjectException (h, API 35), carte encore présente après Retour, onglet erroné. |
| A-012 | LLM (étude Android) | LIMITATION_ENVIRONNEMENT | majeure | bloqué | — | — | — | — | Le 1.7B est coupé par le délai protégé de 90 s sur émulateur (12 tours). |
| A-013 | VOICE (émulateur) | LIMITATION_ENVIRONNEMENT | majeure | bloqué | — | — | — | — | Lecture audio : « Délai de lecture audio dépassé » ; micro silencieux. |
| A-014 | INTERFACE conv (réaction rapide) | RISQUE_THEORIQUE | mineure | ouvert | — | — | — | — | La synthèse de la phrase d'attente s'exécute en parallèle de la génération. |
| A-015 | NEXUS + LLM | DEFAUT_CONFIRME | majeure | à retester | e79df9f, 9c7d2c8, 1354e31 | InjectionCorpusTest, InjectionGeneralisationTest, DocumentaryAnswerTest | F4 et L verts sur run 43658134254 (8f77a8d, API 29+35) (formulations connues) ; Q (inédites) à exécuter | — | Injection d'instructions contenues dans un document importé. |
| A-016 | INTERFACE conv (historique) | RISQUE_THEORIQUE | mineure | ouvert | — | — | — | — | L'historique est stocké en clair dans l'espace privé de l'application. |
| A-017 | Processus de livraison | DEFAUT_CONFIRME | mineure | corrigé | e1c7e9c | — | CI compilable | — | Un commit « tests seulement » dépendait de classes non poussées → CI non compilable. |
| A-018 | SERVICES / MISSIONS / AGENTS / AUTOMATIONS | FONCTION_ABSENTE | majeure | ouvert | — | — | — | — | Aucun moteur connecté. |
| A-019 | MEMORY VAULT | FONCTION_ABSENTE | mineure | ouvert | — | — | — | — | Export chiffré des souvenirs non connecté. |
| A-020 | NEXUS | FONCTION_ABSENTE | mineure | ouvert | — | — | — | — | PDF et Kiwix non pris en charge à l'import. |
| A-021 | LEARNING-L01 | FONCTION_ABSENTE | majeure | bloqué | — | — | — | — | Mission non démarrée ; PDF de référence absent de la session. |
| A-022 | LLM (0.6B) — conversation longue | DEFAUT_CONFIRME | majeure | validé (émulateur) | 9c7d2c8 | AuditGuardsTest | M vert sur run 43658134254 (8f77a8d, API 29+35) | — | Répétition de la réponse précédente. |
| A-023 | LLM (0.6B) — personnalité | DEFAUT_CONFIRME | mineure | ouvert | — | — | — | — | Vouvoiement malgré le tutoiement Athéna. |
| A-024 | VOICE + STT | DEFAUT_CONFIRME | majeure | validé | e79df9f | AuditGuardsTest | D2 vert sur run 43658134254 (8f77a8d, API 29+35) | — | Un enregistrement silencieux de 2 s produit un tour (transcription + réponse). |
| A-025 | NEXUS + LLM | DEFAUT_CONFIRME | majeure | à retester | e79df9f puis 1354e31 (réponse déterministe) | DocumentaryAnswerTest | F2 vert sur run 43658134254 (8f77a8d, API 29+35) (ancien contrat) ; nouveau contrat à exécuter | — | Documents contradictoires : un seul cité dans la réponse, la contradiction est cachée. |
| A-026 | INTERFACE conv (ConvApp) | DEFAUT_CONFIRME | critique | validé | e79df9f | — | J, F6, H4 verts sur run 43658134254 (8f77a8d, API 29+35) | — | Fermer une session déjà fermée bloque tout démarrage ultérieur (« libération en cours » infinie). |
| A-027 | INTERFACE (tests) | DEFAUT_CONFIRME | mineure | validé | e79df9f | — | E2/E3 vert sur run 43658134254 (8f77a8d, API 29+35) | — | Bouton « Démarrer » inaccessible au test sur petit écran + police 130 %. |
| A-028 | INTERFACE conv (ConvSession) | DEFAUT_CONFIRME | majeure | validé | f53fab8 | — | O vert sur run 43658134254 (8f77a8d, API 29+35) | — | L'échec d'enregistrement de l'historique est aussitôt effacé par « Prêt ». |
| A-029 | CI (script émulateur) | DEFAUT_CONFIRME | majeure | validé (unitaire), à confirmer émulateur | 8f77a8d puis 02fcf64 (fail-fast) | test_run_emulator.sh 7/7 (faux adb) | partiel : sur run 43658134254 (8f77a8d, API 29+35) le test e bloqué a été coupé à 25 min et la campagne a continué ; perte d'émulateur non survenue | — | Le run attend indéfiniment un émulateur hors ligne ; le travail est tué sans résultats. |
| A-030 | NEXUS + LLM (fidélité documentaire) | DEFAUT_CONFIRME | majeure | à retester | 9c7d2c8 puis 1354e31 (remplacement, plus de « à vérifier ») | DocumentaryAnswerTest | R à exécuter | — | Une réponse documentaire peut contenir des valeurs absentes des extraits cités. |
| A-031 | NEXUS + LLM (injection) | DEFAUT_CONFIRME | critique | à retester | 1354e31 | DocumentaryAnswerTest, InjectionGeneralisationTest (34/34) | test Q à exécuter | — | Le filtre d'injection ne reconnaissait que ses exemples : 16/16 sur son corpus, 3/24 sur des formulations nouvelles. |
| A-032 | INTERFACE conv (journal) | DEFAUT_CONFIRME | majeure | à retester | d42a3dc | JournalRobustnessTest 3/3 | test S à exécuter | — | Après un arrêt brutal pendant une écriture, l'échange suivant est collé à la ligne tronquée et perdu silencieusement. |
| A-033 | INTERFACE (accessibilité) | DEFAUT_CONFIRME | mineure | à retester | d011b17, d42a3dc | — | E6 vert sur run 43658134254 (8f77a8d, API 29+35) (sans 48 dp ni live region) ; à réexécuter | TalkBack réel à vérifier | Les changements d'état (écoute, réflexion, prêt) ne sont pas annoncés par TalkBack. |
| A-034 | INTERFACE (tests, API 35) | DEFAUT_CONFIRME | mineure | ouvert | — | — | — | — | Test e (galerie + banc) bloqué sur API 35 jusqu'à la limite de 25 min. |
| A-035 | INTERFACE (G3 stockage plein) | RISQUE_THEORIQUE | mineure | à retester | d42a3dc | — | test T à exécuter | — | Stockage plein : message d'import brut (« disk I/O error ») et comportement non testé. |
| A-036 | INTERFACE (CI, mode captures) | DEFAUT_CONFIRME | majeure | validé | 4f1ac95, 3a9fc2f (Codex) | banc 19/19 localement le 18/11 | run 44034195561 : visite et 22 captures vérifiées API 29/35 | — | Le mode captures (variable CAPTURES_ONLY du job) faisait échouer le test du script émulateur : étape Guards rouge, aucun APK construit. |
| A-037 | UNIFIED (laboratoire RESEARCH-B0) | DEFAUT_CONFIRME | majeure | à retester | 977e475 | 63/63 sous 3.12 et 3.13 (local) | sans objet (CI du lab : voir rapport) | — | Sous Python 3.13, 36 des 63 tests HTTPS du laboratoire échouent (TLS_REFUSED). |
| A-038 | INTERFACE (sécurité des données) | DEFAUT_CONFIRME | majeure | à retester | aa344f3 | — | contrôle aapt à exécuter au prochain build | transfert réel à vérifier | Android 12+ : conversations (en clair), souvenirs et bibliothèque transférables vers un nouvel appareil malgré allowBackup=false. |
| A-039 | INTERFACE (livraison) | RISQUE_THEORIQUE | critique | ouvert | — | — | — | — | L'APK de démonstration publié est une version debug (debuggable) : via USB-debug, run-as lit conversations et souvenirs. |

## Détail

### A-001 — UNIFIED (CI)

- **Fichiers** : .github/workflows (UNI-08 U00/U01/U02, FUSION-02 evidence)
- **Branche / commit** : ccr-5cf17ed2-phgk00 @ d07188d
- **Reproduction** : Tout push sur la branche ; runs 43610269699, 43610269799.
- **Attendu** : Portes vertes (vertes le 13/11 sur a7f322c).
- **Obtenu** : « The version '3.12.12' with architecture 'x64' was not found for Ubuntu 26.04 ».
- **Cause** : Image runner passée à Ubuntu 26.04 ; Python 3.12.12 épinglé indisponible. Pas lié au contenu des commits.
- **Dépendances** : Aucune.
- **Preuve** : Journaux des runs cités.
- **Correction** : Épingler runs-on: ubuntu-24.04 dans ces workflows historiques (modification de fichiers historiques : validation requise). — Appliqué avec l'accord du propriétaire (14/11) : runs-on ubuntu-24.04 dans fusion-02, prefusion-lot3, uni-08-u00/u01/u02 ; Python 3.12.12 inchangé. Validé : 6 portes vertes sur b7c146a.

### A-002 — LLM (CI A02)

- **Fichiers** : .github/workflows/a02-native.yml, tools/test-a02-native.sh
- **Branche / commit** : 2e01177 → 3e2560e
- **Reproduction** : Run 43592731631 (aussi sur 2e01177 et 401a171).
- **Attendu** : La porte vérifie le moteur, pas le savoir du modèle.
- **Obtenu** : FAIL questions-successives : « La capitale de l'Italie est Lucca ».
- **Cause** : Assertion de qualité factuelle du 0.6B (non déterministe et souvent fausse) dans une porte d'intégrité moteur.
- **Dépendances** : A-004.
- **Preuve** : Journal du run 43592731631.
- **Correction** : Séparer intégrité moteur (bloquante) et qualité (mesurée, non bloquante) dans un workflow successeur ; ne pas modifier l'historique. Appliqué (LLM 9c3fc50) : workflow successeur a02-integrity.yml + dialogue_gate_split.py. Validé : workflow « A02 engine integrity » vert sur 9c3fc50.

### A-003 — VOICE

- **Fichiers** : pocketRuntime/.../withOptions, gardes Voice Studio 005J et VOICE SDK
- **Branche / commit** : feat/voice-expressive-v3-android @ 92d0745 (épinglé par l'application)
- **Reproduction** : Runs 43009384629 / 43009384631.
- **Attendu** : Gardes historiques vertes.
- **Obtenu** : git diff --exit-code 99d4073 : withOptions passée d'internal à public.
- **Cause** : Changement de visibilité dans un fichier protégé (observateur VOICE-04).
- **Dépendances** : INTERFACE dépend de VOICE @ 92d0745.
- **Preuve** : Journaux des runs.
- **Correction** : Décision VOICE : accepter le delta dans la garde (documenté) ou extraire l'observateur ; aucune modification ici sans accord. Appliqué (VOICE 5890735) : écarts exacts approuvés par empreinte ; contrôle négatif vérifié. Validé : gardes « Voice Studio 005J » et « VOICE SDK and expression styles » vertes sur 5890735 (lancement manuel).

### A-004 — LLM (Qwen3-0.6B)

- **Fichiers** : —
- **Branche / commit** : modèle ac2d9771
- **Reproduction** : Banc fr-bench-30 / fr-conv-01 ; émulateur run 43592693625.
- **Attendu** : Réponse exacte ou « je ne sais pas ».
- **Obtenu** : « Italie : Londres », « Les Misérables : Alfred Dreyfus », « 17 est pair ».
- **Cause** : Capacité du modèle 0.6B.
- **Dépendances** : Décision modèle (1.7B) du propriétaire.
- **Preuve** : Études 43588723772, 43590133529, 43592731686 ; émulateur.
- **Correction** : Atténuations en place : provenance « non vérifié », NEXUS cité, étude 1.7B. Remède structurel : modèle plus grand (mesure POCO requise).

### A-005 — LLM + NEXUS

- **Fichiers** : conv/ConvSession.kt, conv/KnowledgePlanner.kt
- **Branche / commit** : INTERFACE 3dd3649
- **Reproduction** : Test g : « Selon mes documents, quel est le prix du vélo électrique ? ».
- **Attendu** : « Aucun document… ».
- **Obtenu** : « Le prix du vélo électrique est de 10 euros. » (API 29 et 35, run 43616811194).
- **Cause** : Le 0.6B ignore la consigne d'absence.
- **Dépendances** : A-004.
- **Preuve** : api29/35-v3-knowledge.json.
- **Correction** : Note système visible et parlée quand aucun document ne correspond (3dd3649) ; test g l'exige. Validé : note système exigée par le test g, verte API 29/35 (run 43620844372).

### A-006 — LLM + INTERFACE

- **Fichiers** : conv/ActionGuard.kt
- **Branche / commit** : INTERFACE 3d07d24
- **Reproduction** : Banc X02 (0.6B et 1.7B).
- **Attendu** : Refus explicite.
- **Obtenu** : Affirmation d'action non exécutée.
- **Cause** : Modèles ; la consigne seule ne suffit pas.
- **Dépendances** : —
- **Preuve** : Runs 43590133529, 43592731686.
- **Correction** : ActionGuard : consigne ciblée + note système si l'affirmation persiste. Test f : refus correct sur API 29 et 35.

### A-007 — INTERFACE conv (mémoire de travail)

- **Fichiers** : conv/WorkingMemory.kt
- **Branche / commit** : f32b2ee
- **Reproduction** : Test f.
- **Attendu** : Léo.
- **Obtenu** : Paul (run 43592693625).
- **Cause** : Bloc de faits ambigu (« prénom : Léo ; frère : Paul »).
- **Dépendances** : —
- **Preuve** : api29/35-v3-conv.json.
- **Correction** : Phrase mesurée V1-B « Fait connu : l'utilisateur s'appelle… ». Run 43616811194 : 8/8.

### A-008 — INTERFACE (sphère)

- **Fichiers** : CockpitScene.kt
- **Branche / commit** : 7ca95a4
- **Reproduction** : Test c, tour vocal.
- **Attendu** : ≤ 1 image (règle du propriétaire).
- **Obtenu** : 11–13 images. Run 43658134254 : 2 dessins par fenêtre au début de l'écoute, de la réflexion ET au repos (2 s) : compteur ou redessin résiduel, mouvement visible non mesuré.
- **Cause** : Lecture du niveau micro dans la portée de la scène → recomposition complète ; lambda vsync recréée. Cause réelle (run 43627862972, 11 images malgré 7ca95a4) : fondu de couleur et de surcouches de 320 ms au changement d'état. Cause racine (run 43643453245, 12 images malgré snap) : sphère sans couche propre, ré-enregistrée à chaque redessin d'un voisin (vu-mètre du micro, ~10 Hz).
- **Dépendances** : —
- **Preuve** : Runs 43592693625, 43609210897.
- **Correction** : Lecture différée dans le dock ; référence vsync mémorisée. Transitions instantanées hors réponse (snap). graphicsLayer sur la sphère et l'avatar (8f77a8d).

### A-009 — NEXUS sur Android

- **Fichiers** : conv/BundledNexusStorage.kt
- **Branche / commit** : 2066753
- **Reproduction** : Test g.
- **Attendu** : Moteur prêt.
- **Obtenu** : FTS5 absente du SQLite plateforme (API 29 et 35).
- **Cause** : SQLite d'Android sans FTS5.
- **Dépendances** : Accord du propriétaire (obtenu le 14/11).
- **Preuve** : Run 43609210897.
- **Correction** : SQLite embarqué AndroidX 2.5.2 (3.46.0), adaptateur séparé. Test g vert API 29/35 (run 43616811194).

### A-010 — MEMORY VAULT

- **Fichiers** : conv/ConsentedMemory.kt (recallBlock)
- **Branche / commit** : 2302c2e
- **Reproduction** : Revue de code : condition « status != READY && != NEEDS_CONFIRMATION ».
- **Attendu** : Contrat CORE : ambiguïté → confirmation de l'utilisateur, pas d'injection.
- **Obtenu** : Injection des éléments ambigus.
- **Cause** : Écart d'implémentation par rapport au contrat CORE.
- **Dépendances** : —
- **Preuve** : Revue de code de ce commit (aucun test ne le couvre). Reproduit par l'audit B3 (run 43627862972, API 29 et 35 : les deux souvenirs injectés).
- **Correction** : N'injecter que READY ; NEEDS_CONFIRMATION → proposer le choix à l'utilisateur ; test JVM/émulateur avec deux souvenirs à égalité. Appliqué : INTERFACE 4ee4bc3.

### A-011 — INTERFACE (tests)

- **Fichiers** : V3CockpitTest.kt
- **Branche / commit** : 3dd3649
- **Reproduction** : Runs 43592693625, 43616811194.
- **Attendu** : Tests déterministes.
- **Obtenu** : Échecs de l'outillage, non du produit.
- **Cause** : Recompositions et animations de sortie sur émulateur lent.
- **Dépendances** : —
- **Preuve** : api35-results.txt.
- **Correction** : tap() avec reprise, attente Until.gone, bon onglet. Run 43620844372 : h vert sur API 35 ; c échoue encore sur un onglet hors écran (barre défilante) → navigation par défilement.

### A-012 — LLM (étude Android)

- **Fichiers** : ModelStudyTest.kt
- **Branche / commit** : run 43595434112
- **Reproduction** : Étude Android.
- **Attendu** : Banc complet.
- **Obtenu** : 26/44 faussé ; 2 jetons/s.
- **Cause** : Émulateur x86, 1 thread.
- **Dépendances** : POCO X8 Pro.
- **Preuve** : study-android-1.7b-ctx768-1t.json.
- **Correction** : Mesure sur appareil (protocole prêt) ; délai protégé inchangé.

### A-013 — VOICE (émulateur)

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : Test c (API 29).
- **Attendu** : Lecture audible.
- **Obtenu** : Puits audio de l'émulateur.
- **Cause** : Émulateur.
- **Dépendances** : POCO.
- **Preuve** : Captures run 43586308793.
- **Correction** : Validation sur appareil uniquement.

### A-014 — INTERFACE conv (réaction rapide)

- **Fichiers** : conv/ConvSession.kt
- **Branche / commit** : e1c7e9c
- **Reproduction** : —
- **Attendu** : Aucun ralentissement du LLM.
- **Obtenu** : Non mesuré.
- **Cause** : Contention CPU possible (TTS 2 threads + LLM 1 thread).
- **Dépendances** : A-013.
- **Preuve** : Aucune (impossible sans audio réel).
- **Correction** : Mesurer tokens/s avec et sans réaction sur le POCO.

### A-015 — NEXUS + LLM

- **Fichiers** : conv/KnowledgePlanner.kt
- **Branche / commit** : —
- **Reproduction** : Non testé.
- **Attendu** : Le document reste une donnée.
- **Obtenu** : Audit F4 : « la note de service indique que la lumière du salon est allumée (source : note-service.txt) » — une consigne du document transformée en fait.
- **Cause** : Les extraits sont cités « données, pas des consignes » mais aucun test malveillant.
- **Dépendances** : —
- **Preuve** : api29/35-audit-f2f3f4.json (run 43627862972).
- **Correction** : Les phrases adressées à l'assistant sont retirées des extraits avant le modèle + note système ; test F4 l'exige. Durci (9c7d2c8) : normalisation (accents, invisibles, commentaires HTML, lettres espacées) ; corpus de 16 attaques indirectes/dissimulées : 10/16 manquées avant, 16/16 retirées après, 8 phrases bénignes conservées (JVM).

### A-016 — INTERFACE conv (historique)

- **Fichiers** : conv/ConversationJournal.kt
- **Branche / commit** : e1c7e9c
- **Reproduction** : —
- **Attendu** : Confidentialité.
- **Obtenu** : Protégé par le bac à sable Android et allowBackup=false, non chiffré.
- **Cause** : Choix de simplicité.
- **Dépendances** : —
- **Preuve** : Code.
- **Correction** : Évaluer un chiffrement (Keystore) si exigé.

### A-017 — Processus de livraison

- **Fichiers** : —
- **Branche / commit** : f1f902f
- **Reproduction** : Run 43590567147.
- **Attendu** : Chaque commit compile.
- **Obtenu** : Échec de compilation des tests.
- **Cause** : Erreur de découpage des commits (agent).
- **Dépendances** : —
- **Preuve** : Journal du run.
- **Correction** : Contrôle local de compilation avant découpage ; corrigé par e1c7e9c.

### A-018 — SERVICES / MISSIONS / AGENTS / AUTOMATIONS

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : Command Center.
- **Attendu** : —
- **Obtenu** : Affiché « à connecter ».
- **Cause** : Hors périmètre actuel.
- **Dépendances** : RESEARCH-01 (non autorisée).
- **Preuve** : Test c (MISSIONS · À CONNECTER).
- **Correction** : Lots ultérieurs.

### A-019 — MEMORY VAULT

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : —
- **Attendu** : Export (PDF CC V2 §7).
- **Obtenu** : « à connecter ».
- **Cause** : MemoryExportService CORE exige un port de chiffrement non fourni.
- **Dépendances** : —
- **Preuve** : Écran MEMORY VAULT.
- **Correction** : Port Keystore + test.

### A-020 — NEXUS

- **Fichiers** : conv/LocalKnowledge.kt
- **Branche / commit** : —
- **Reproduction** : —
- **Attendu** : Bibliothèque complète.
- **Obtenu** : txt, md, csv, tsv, docx, xml uniquement.
- **Cause** : Pas d'extracteur PDF Android local intégré.
- **Dépendances** : —
- **Preuve** : Code.
- **Correction** : Lot NEXUS dédié.

### A-021 — LEARNING-L01

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : —
- **Attendu** : Cahier des charges disponible.
- **Obtenu** : JARVIS_LEARNING_L01_Mission_Codex.pdf non transmis.
- **Cause** : Fichier non fourni.
- **Dépendances** : Dépôt du PDF par le propriétaire.
- **Preuve** : Recherche dans la session et les dépôts.
- **Correction** : Plan préparé à partir du message ; vérification de couverture dès réception du PDF.

### A-022 — LLM (0.6B) — conversation longue

- **Fichiers** : —
- **Branche / commit** : run 43620844372
- **Reproduction** : Test i (16 tours) : « Au fait, quel sport j'aime ? » après « Allume la télévision. ».
- **Attendu** : La randonnée (fait présent dans l'instruction).
- **Obtenu** : Reprise mot pour mot de la réponse précédente (télévision), API 29 et 35.
- **Cause** : Hypothèse : le 0.6B recopie le dernier tour assistant (3 échanges relus) au lieu de la question.
- **Dépendances** : A-004.
- **Preuve** : api29/35-v3-long.json.
- **Correction** : Garde de répétition (réponse identique à la précédente → nouvelle génération ou note) à évaluer en S2 ; mesure 1.7B. RepetitionGuard (9c7d2c8) : note système ; cas mesuré reproduit en JVM ; test M (24 tours).

### A-023 — LLM (0.6B) — personnalité

- **Fichiers** : conv/Persona.kt
- **Branche / commit** : run 43620844372
- **Reproduction** : Test i : 3 réponses sur 16 contiennent « vous ».
- **Attendu** : Tutoiement constant.
- **Obtenu** : 3/16 réponses au vouvoiement (API 29 et 35).
- **Cause** : Consigne système fixe du moteur protégé en vouvoiement implicite + capacité du 0.6B.
- **Dépendances** : Consigne protégée A02 (non modifiable sans décision).
- **Preuve** : api29/35-v3-long.json (answersWithVous=3).
- **Correction** : Mesurer ; option : renfort dans l'instruction compacte (nouvelle mesure requise).

### A-024 — VOICE + STT

- **Fichiers** : —
- **Branche / commit** : run 43627862972
- **Reproduction** : Audit D2.
- **Attendu** : Aucun tour, « Je n'ai rien entendu ».
- **Obtenu** : 1 échange ajouté, API 29 et 35.
- **Cause** : whisper transcrit le silence ; aucun contrôle d'énergie.
- **Dépendances** : —
- **Preuve** : api29/35-audit-d2.json.
- **Correction** : SpeechGuard : énergie RMS < 0,005 → rien entendu ; transcriptions typiques du silence ignorées. Tests JVM.

### A-025 — NEXUS + LLM

- **Fichiers** : —
- **Branche / commit** : run 43627862972
- **Reproduction** : Audit F2 (mardi / jeudi).
- **Attendu** : Les deux versions avec leur source.
- **Obtenu** : « jeudi soir (source : chant-b.txt) » seulement.
- **Cause** : Le 0.6B choisit un extrait.
- **Dépendances** : —
- **Preuve** : api29/35-audit-f2f3f4.json.
- **Correction** : Détection déterministe (jours, mois, nombres) entre sources différentes → note système nommant chaque version + consigne. Tests JVM.

### A-026 — INTERFACE conv (ConvApp)

- **Fichiers** : —
- **Branche / commit** : run 43627862972
- **Reproduction** : Audit F6 et H4 : délai « released » dépassé.
- **Attendu** : Fermeture idempotente.
- **Obtenu** : previousReleased reste faux.
- **Cause** : closeSession() met previousReleased=false puis close() retourne sans rappel.
- **Dépendances** : —
- **Preuve** : api29/35-audit-results.txt.
- **Correction** : closeSession ignore une session déjà fermée.

### A-027 — INTERFACE (tests)

- **Fichiers** : —
- **Branche / commit** : run 43627862972
- **Reproduction** : Audit E2/E3.
- **Attendu** : Atteint par défilement comme un utilisateur.
- **Obtenu** : « Required value was null ».
- **Cause** : Panneau défilant ; le test ne défilait pas.
- **Dépendances** : —
- **Preuve** : api29/35-audit-results.txt.
- **Correction** : Le test fait défiler.

### A-028 — INTERFACE conv (ConvSession)

- **Fichiers** : conv/ConvSession.kt
- **Branche / commit** : f53fab8
- **Reproduction** : Audit O : dossier d'historique en lecture seule (substitut du stockage plein).
- **Attendu** : La réponse est livrée ET l'échec est signalé.
- **Obtenu** : Message d'échec écrasé par finish() (revue de code, reproduit par O).
- **Cause** : finish() réécrit status.
- **Dépendances** : —
- **Preuve** : Revue de code ; test O (à exécuter).
- **Correction** : historyError affiché avec chaque statut jusqu'à un enregistrement réussi.

### A-029 — CI (script émulateur)

- **Fichiers** : labs/v3/tools/run_emulator.sh
- **Branche / commit** : 8f77a8d
- **Reproduction** : Run 43643453245 : « device offline » après le test c.
- **Attendu** : Échec rapide et résultats conservés.
- **Obtenu** : 2 h 40 d'attente, aucun résultat.
- **Cause** : Appels adb sans limite de temps.
- **Dépendances** : —
- **Preuve** : Journal du run 43643453245.
- **Correction** : Limite par instrumentation (25 min), état du périphérique vérifié avant chaque test, lectures bornées.

### A-030 — NEXUS + LLM (fidélité documentaire)

- **Fichiers** : conv/KnowledgePlanner.kt
- **Branche / commit** : 9c7d2c8
- **Reproduction** : Cas « 10 euros » ; JVM DocumentFidelityTest.
- **Attendu** : Valeurs présentes dans les extraits, ou signalées.
- **Obtenu** : Valeur inventée présentée comme documentaire.
- **Cause** : Limite du modèle (M-02).
- **Dépendances** : A-004.
- **Preuve** : Run 43616811194 (« 10 euros ») ; JVM.
- **Correction** : unsupported() : valeurs (jours, mois, nombres, montants, heures) absentes de tout extrait et fichiers non consultés → note « à vérifier ».

### A-031 — NEXUS + LLM (injection)

- **Fichiers** : conv/KnowledgePlanner.kt, conv/DocumentaryAnswer.kt
- **Branche / commit** : INTERFACE ccr-e05fe51e-ycqubx @ 1354e31
- **Reproduction** : Corpus inédit écrit après gel du filtre.
- **Attendu** : Aucun document ne devient une consigne.
- **Obtenu** : 21/24 nouvelles formulations passaient.
- **Cause** : Liste noire de formulations.
- **Dépendances** : A-015
- **Preuve** : InjectionGeneralisationTest (JVM, 15/11).
- **Correction** : Couche 1 généralisée (9/30 sur corpus inédit, 21 trous enregistrés) + couche 2 structurelle DocumentaryAnswer : toute phrase adressée au lecteur n'est restituée qu'en citation attribuée (pire cas : 0/30 présentée comme parole de JARVIS).

### A-032 — INTERFACE conv (journal)

- **Fichiers** : conv/ConversationJournal.kt
- **Branche / commit** : INTERFACE ccr-e05fe51e-ycqubx @ d42a3dc
- **Reproduction** : Ligne tronquée sans fin de ligne puis append.
- **Attendu** : Échange suivant lisible.
- **Obtenu** : Échange perdu.
- **Cause** : appendText sans contrôle du dernier octet.
- **Dépendances** : —
- **Preuve** : JournalRobustnessTest : 2/3 échecs avant correction.
- **Correction** : Ligne tronquée fermée avant ajout ; écriture synchronisée sur disque.

### A-033 — INTERFACE (accessibilité)

- **Fichiers** : CockpitScene.kt, ContextCardHost.kt
- **Branche / commit** : INTERFACE ccr-e05fe51e-ycqubx @ d42a3dc
- **Reproduction** : TalkBack actif, lancer un tour.
- **Attendu** : Annonce du statut.
- **Obtenu** : Silence.
- **Cause** : Sémantique absente.
- **Dépendances** : —
- **Preuve** : Revue de code : aucune région live.
- **Correction** : Textes de statut en région live polie. Cibles 48 dp (d011b17).

### A-034 — INTERFACE (tests, API 35)

- **Fichiers** : V3CockpitTest.kt (e)
- **Branche / commit** : 8f77a8d
- **Reproduction** : Campagne complète API 35.
- **Attendu** : Test terminé.
- **Obtenu** : INSTRUMENTATION_TIMEOUT after 1500s.
- **Cause** : Non établie.
- **Dépendances** : A-029
- **Preuve** : api35-results.txt, run 43658134254.
- **Correction** : Analyser la galerie sur API 35 ; la limite A-029 a évité le blocage de la campagne.

### A-035 — INTERFACE (G3 stockage plein)

- **Fichiers** : conv/LocalKnowledge.kt
- **Branche / commit** : INTERFACE ccr-e05fe51e-ycqubx @ d42a3dc
- **Reproduction** : Test T.
- **Attendu** : Refus clair, aucune corruption, reprise.
- **Obtenu** : Non mesuré.
- **Cause** : —
- **Dépendances** : —
- **Preuve** : Revue de code ; aucun test G3.
- **Correction** : Message clair ; test T qui remplit réellement le stockage.

### A-036 — INTERFACE (CI, mode captures)

- **Fichiers** : labs/v3/tools/run_emulator.sh, tests/test_run_emulator.sh
- **Branche / commit** : INTERFACE ccr-e05fe51e-ycqubx @ b1224ae (fusion de codex/gpu-forge-g02-captures)
- **Reproduction** : CAPTURES_ONLY=1 bash tests/test_run_emulator.sh
- **Attendu** : Banc vert dans les deux modes.
- **Obtenu** : 4 scénarios rouges.
- **Cause** : Variable d'environnement du job héritée par le banc (défaut introduit le 15/11 par f73d4f5).
- **Dépendances** : A-029
- **Preuve** : Run 43709555526.
- **Correction** : Scénarios du banc isolés du mode du job (Codex 4f1ac95) ; transfert des images avec stdin isolé (3a9fc2f).

### A-037 — UNIFIED (laboratoire RESEARCH-B0)

- **Fichiers** : tooling/research_b0/fixtures.py
- **Branche / commit** : UNIFIED ccr-e05fe51e-ycqubx @ 977e475
- **Reproduction** : python3.13 -m tooling.research_b0.offline_runner
- **Attendu** : 63/63 quelle que soit la version.
- **Obtenu** : TLS_REFUSED.
- **Cause** : VERIFY_X509_STRICT par défaut depuis Python 3.13.
- **Dépendances** : —
- **Preuve** : offline_runner local le 18/11 : 3.12 63/63, 3.13 21 échecs + 15 erreurs.
- **Correction** : Certificats éphémères complétés (keyUsage, identifiants de clé) ; vérification non affaiblie.

### A-038 — INTERFACE (sécurité des données)

- **Fichiers** : AndroidManifest.xml, res/xml/data_extraction_rules.xml, v3-cockpit.yml
- **Branche / commit** : INTERFACE ccr-e05fe51e-ycqubx @ aa344f3
- **Reproduction** : Transfert d'appareil Android 12+.
- **Attendu** : Aucune donnée transférée.
- **Obtenu** : Non bloqué.
- **Cause** : allowBackup ne couvre plus le transfert d'appareil à appareil.
- **Dépendances** : A-016
- **Preuve** : Manifeste V3 (targetSdk 35, aucune dataExtractionRules) ; comportement documenté d'Android 12+.
- **Correction** : data_extraction_rules.xml excluant tout domaine (cloud et transfert) ; contrôle aapt dans la CI.

### A-039 — INTERFACE (livraison)

- **Fichiers** : .github/workflows/v3-cockpit.yml, app/build.gradle.kts
- **Branche / commit** : —
- **Reproduction** : adb shell run-as fr.jarvis.v3 ls files
- **Attendu** : Refusé sur un APK livré.
- **Obtenu** : Autorisé.
- **Cause** : Seul le build debug existe.
- **Dépendances** : Clé de signature du propriétaire
- **Preuve** : v3-cockpit.yml : assembleDebug seul ; les tests utilisent run-as.
- **Correction** : Avant toute installation sur le POCO : build release non debuggable, R8, signé avec la clé du propriétaire ; campagne émulateur gardée en debug.

