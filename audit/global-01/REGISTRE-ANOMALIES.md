# Registre central des anomalies — JARVIS (AUDIT-GLOBAL-01)

Source : `registre.json` (ce fichier est généré par `render_registre.py`). Mise à jour : 2026-11-14.

Natures : **DEFAUT_CONFIRME** (prouvé), **RISQUE_THEORIQUE** (non observé), **FONCTION_ABSENTE**, **LIMITATION_ENVIRONNEMENT**, **LIMITATION_MODELE**.

| ID | Module | Nature | Gravité | Statut | Symptôme | Preuve | Correction proposée |
|---|---|---|---|---|---|---|---|
| A-001 | UNIFIED (CI) | DEFAUT_CONFIRME | majeure | validé | Les portes historiques UNI-08 et FUSION-02 échouent sur la branche de développement. | Journaux des runs cités. | Épingler runs-on: ubuntu-24.04 dans ces workflows historiques (modification de fichiers historiques : validation requise). — Appliqué avec l'accord du propriétaire (14/11) : runs-on ubuntu-24.04 dans fusion-02, prefusion-lot3, uni-08-u00/u01/u02 ; Python 3.12.12 inchangé. Validé : 6 portes vertes sur b7c146a. |
| A-002 | LLM (CI A02) | DEFAUT_CONFIRME | majeure | à retester | La porte « A02 sealed GGUF native loader » est rouge en permanence. | Journal du run 43592731631. | Séparer intégrité moteur (bloquante) et qualité (mesurée, non bloquante) dans un workflow successeur ; ne pas modifier l'historique. Appliqué (LLM 9c3fc50) : workflow successeur a02-integrity.yml + dialogue_gate_split.py. |
| A-003 | VOICE | DEFAUT_CONFIRME | majeure | à retester | Le commit VOICE utilisé par l'application échoue à ses propres gardes de préservation. | Journaux des runs. | Décision VOICE : accepter le delta dans la garde (documenté) ou extraire l'observateur ; aucune modification ici sans accord. Appliqué (VOICE 5890735) : écarts exacts approuvés par empreinte ; contrôle négatif vérifié. |
| A-004 | LLM (Qwen3-0.6B) | LIMITATION_MODELE | critique | ouvert | Affirmations factuelles fausses et assurées. | Études 43588723772, 43590133529, 43592731686 ; émulateur. | Atténuations en place : provenance « non vérifié », NEXUS cité, étude 1.7B. Remède structurel : modèle plus grand (mesure POCO requise). |
| A-005 | LLM + NEXUS | DEFAUT_CONFIRME | majeure | validé | Réponse documentaire inventée quand aucun document ne contient l'information. | api29/35-v3-knowledge.json. | Note système visible et parlée quand aucun document ne correspond (3dd3649) ; test g l'exige. Validé : note système exigée par le test g, verte API 29/35 (run 43620844372). |
| A-006 | LLM + INTERFACE | DEFAUT_CONFIRME | critique | validé | JARVIS prétend avoir exécuté une action (« La lumière du salon est allumée »). | Runs 43590133529, 43592731686. | ActionGuard : consigne ciblée + note système si l'affirmation persiste. Test f : refus correct sur API 29 et 35. |
| A-007 | INTERFACE conv (mémoire de travail) | DEFAUT_CONFIRME | majeure | validé | « Comment je m'appelle ? » → prénom du frère. | api29/35-v3-conv.json. | Phrase mesurée V1-B « Fait connu : l'utilisateur s'appelle… ». Run 43616811194 : 8/8. |
| A-008 | INTERFACE (sphère) | DEFAUT_CONFIRME | majeure | à retester | La sphère se redessine pendant l'écoute (11–13 images). | Runs 43592693625, 43609210897. | Lecture différée dans le dock ; référence vsync mémorisée. |
| A-009 | NEXUS sur Android | DEFAUT_CONFIRME | critique | validé | Recherche documentaire impossible. | Run 43609210897. | SQLite embarqué AndroidX 2.5.2 (3.46.0), adaptateur séparé. Test g vert API 29/35 (run 43616811194). |
| A-010 | MEMORY VAULT | DEFAUT_CONFIRME | majeure | ouvert | Les souvenirs en statut NEEDS_CONFIRMATION (égalité ambiguë) sont injectés comme s'ils étaient READY. | Revue de code de ce commit (aucun test ne le couvre). | N'injecter que READY ; NEEDS_CONFIRMATION → proposer le choix à l'utilisateur ; test JVM/émulateur avec deux souvenirs à égalité. |
| A-011 | INTERFACE (tests) | DEFAUT_CONFIRME | mineure | à retester | Échecs instables : StaleObjectException (h, API 35), carte encore présente après Retour, onglet erroné. | api35-results.txt. | tap() avec reprise, attente Until.gone, bon onglet. Run 43620844372 : h vert sur API 35 ; c échoue encore sur un onglet hors écran (barre défilante) → navigation par défilement. |
| A-012 | LLM (étude Android) | LIMITATION_ENVIRONNEMENT | majeure | bloqué | Le 1.7B est coupé par le délai protégé de 90 s sur émulateur (12 tours). | study-android-1.7b-ctx768-1t.json. | Mesure sur appareil (protocole prêt) ; délai protégé inchangé. |
| A-013 | VOICE (émulateur) | LIMITATION_ENVIRONNEMENT | majeure | bloqué | Lecture audio : « Délai de lecture audio dépassé » ; micro silencieux. | Captures run 43586308793. | Validation sur appareil uniquement. |
| A-014 | INTERFACE conv (réaction rapide) | RISQUE_THEORIQUE | mineure | ouvert | La synthèse de la phrase d'attente s'exécute en parallèle de la génération. | Aucune (impossible sans audio réel). | Mesurer tokens/s avec et sans réaction sur le POCO. |
| A-015 | NEXUS + LLM | RISQUE_THEORIQUE | majeure | ouvert | Injection d'instructions contenues dans un document importé. | Aucune. | Campagne F : document piégé synthétique. |
| A-016 | INTERFACE conv (historique) | RISQUE_THEORIQUE | mineure | ouvert | L'historique est stocké en clair dans l'espace privé de l'application. | Code. | Évaluer un chiffrement (Keystore) si exigé. |
| A-017 | Processus de livraison | DEFAUT_CONFIRME | mineure | corrigé | Un commit « tests seulement » dépendait de classes non poussées → CI non compilable. | Journal du run. | Contrôle local de compilation avant découpage ; corrigé par e1c7e9c. |
| A-018 | SERVICES / MISSIONS / AGENTS / AUTOMATIONS | FONCTION_ABSENTE | majeure | ouvert | Aucun moteur connecté. | Test c (MISSIONS · À CONNECTER). | Lots ultérieurs. |
| A-019 | MEMORY VAULT | FONCTION_ABSENTE | mineure | ouvert | Export chiffré des souvenirs non connecté. | Écran MEMORY VAULT. | Port Keystore + test. |
| A-020 | NEXUS | FONCTION_ABSENTE | mineure | ouvert | PDF et Kiwix non pris en charge à l'import. | Code. | Lot NEXUS dédié. |
| A-021 | LEARNING-L01 | FONCTION_ABSENTE | majeure | bloqué | Mission non démarrée ; PDF de référence absent de la session. | Recherche dans la session et les dépôts. | Plan préparé à partir du message ; vérification de couverture dès réception du PDF. |
| A-022 | LLM (0.6B) — conversation longue | DEFAUT_CONFIRME | majeure | ouvert | Répétition de la réponse précédente. | api29/35-v3-long.json. | Garde de répétition (réponse identique à la précédente → nouvelle génération ou note) à évaluer en S2 ; mesure 1.7B. |
| A-023 | LLM (0.6B) — personnalité | DEFAUT_CONFIRME | mineure | ouvert | Vouvoiement malgré le tutoiement Athéna. | api29/35-v3-long.json (answersWithVous=3). | Mesurer ; option : renfort dans l'instruction compacte (nouvelle mesure requise). |

## Détail

### A-001 — UNIFIED (CI)

- **Fichiers** : .github/workflows (UNI-08 U00/U01/U02, FUSION-02 evidence)
- **Branche / commit** : ccr-5cf17ed2-phgk00 @ d07188d
- **Reproduction** : Tout push sur la branche ; runs 43610269699, 43610269799.
- **Attendu** : Portes vertes (vertes le 13/11 sur a7f322c).
- **Obtenu** : « The version '3.12.12' with architecture 'x64' was not found for Ubuntu 26.04 ».
- **Cause** : Image runner passée à Ubuntu 26.04 ; Python 3.12.12 épinglé indisponible. Pas lié au contenu des commits.
- **Dépendances** : Aucune.

### A-002 — LLM (CI A02)

- **Fichiers** : .github/workflows/a02-native.yml, tools/test-a02-native.sh
- **Branche / commit** : 2e01177 → 3e2560e
- **Reproduction** : Run 43592731631 (aussi sur 2e01177 et 401a171).
- **Attendu** : La porte vérifie le moteur, pas le savoir du modèle.
- **Obtenu** : FAIL questions-successives : « La capitale de l'Italie est Lucca ».
- **Cause** : Assertion de qualité factuelle du 0.6B (non déterministe et souvent fausse) dans une porte d'intégrité moteur.
- **Dépendances** : A-004.

### A-003 — VOICE

- **Fichiers** : pocketRuntime/.../withOptions, gardes Voice Studio 005J et VOICE SDK
- **Branche / commit** : feat/voice-expressive-v3-android @ 92d0745 (épinglé par l'application)
- **Reproduction** : Runs 43009384629 / 43009384631.
- **Attendu** : Gardes historiques vertes.
- **Obtenu** : git diff --exit-code 99d4073 : withOptions passée d'internal à public.
- **Cause** : Changement de visibilité dans un fichier protégé (observateur VOICE-04).
- **Dépendances** : INTERFACE dépend de VOICE @ 92d0745.

### A-004 — LLM (Qwen3-0.6B)

- **Fichiers** : —
- **Branche / commit** : modèle ac2d9771
- **Reproduction** : Banc fr-bench-30 / fr-conv-01 ; émulateur run 43592693625.
- **Attendu** : Réponse exacte ou « je ne sais pas ».
- **Obtenu** : « Italie : Londres », « Les Misérables : Alfred Dreyfus », « 17 est pair ».
- **Cause** : Capacité du modèle 0.6B.
- **Dépendances** : Décision modèle (1.7B) du propriétaire.

### A-005 — LLM + NEXUS

- **Fichiers** : conv/ConvSession.kt, conv/KnowledgePlanner.kt
- **Branche / commit** : INTERFACE 3dd3649
- **Reproduction** : Test g : « Selon mes documents, quel est le prix du vélo électrique ? ».
- **Attendu** : « Aucun document… ».
- **Obtenu** : « Le prix du vélo électrique est de 10 euros. » (API 29 et 35, run 43616811194).
- **Cause** : Le 0.6B ignore la consigne d'absence.
- **Dépendances** : A-004.

### A-006 — LLM + INTERFACE

- **Fichiers** : conv/ActionGuard.kt
- **Branche / commit** : INTERFACE 3d07d24
- **Reproduction** : Banc X02 (0.6B et 1.7B).
- **Attendu** : Refus explicite.
- **Obtenu** : Affirmation d'action non exécutée.
- **Cause** : Modèles ; la consigne seule ne suffit pas.
- **Dépendances** : —

### A-007 — INTERFACE conv (mémoire de travail)

- **Fichiers** : conv/WorkingMemory.kt
- **Branche / commit** : f32b2ee
- **Reproduction** : Test f.
- **Attendu** : Léo.
- **Obtenu** : Paul (run 43592693625).
- **Cause** : Bloc de faits ambigu (« prénom : Léo ; frère : Paul »).
- **Dépendances** : —

### A-008 — INTERFACE (sphère)

- **Fichiers** : CockpitScene.kt
- **Branche / commit** : 7ca95a4
- **Reproduction** : Test c, tour vocal.
- **Attendu** : ≤ 1 image (règle du propriétaire).
- **Obtenu** : 11–13 images.
- **Cause** : Lecture du niveau micro dans la portée de la scène → recomposition complète ; lambda vsync recréée.
- **Dépendances** : —

### A-009 — NEXUS sur Android

- **Fichiers** : conv/BundledNexusStorage.kt
- **Branche / commit** : 2066753
- **Reproduction** : Test g.
- **Attendu** : Moteur prêt.
- **Obtenu** : FTS5 absente du SQLite plateforme (API 29 et 35).
- **Cause** : SQLite d'Android sans FTS5.
- **Dépendances** : Accord du propriétaire (obtenu le 14/11).

### A-010 — MEMORY VAULT

- **Fichiers** : conv/ConsentedMemory.kt (recallBlock)
- **Branche / commit** : 2302c2e
- **Reproduction** : Revue de code : condition « status != READY && != NEEDS_CONFIRMATION ».
- **Attendu** : Contrat CORE : ambiguïté → confirmation de l'utilisateur, pas d'injection.
- **Obtenu** : Injection des éléments ambigus.
- **Cause** : Écart d'implémentation par rapport au contrat CORE.
- **Dépendances** : —

### A-011 — INTERFACE (tests)

- **Fichiers** : V3CockpitTest.kt
- **Branche / commit** : 3dd3649
- **Reproduction** : Runs 43592693625, 43616811194.
- **Attendu** : Tests déterministes.
- **Obtenu** : Échecs de l'outillage, non du produit.
- **Cause** : Recompositions et animations de sortie sur émulateur lent.
- **Dépendances** : —

### A-012 — LLM (étude Android)

- **Fichiers** : ModelStudyTest.kt
- **Branche / commit** : run 43595434112
- **Reproduction** : Étude Android.
- **Attendu** : Banc complet.
- **Obtenu** : 26/44 faussé ; 2 jetons/s.
- **Cause** : Émulateur x86, 1 thread.
- **Dépendances** : POCO X8 Pro.

### A-013 — VOICE (émulateur)

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : Test c (API 29).
- **Attendu** : Lecture audible.
- **Obtenu** : Puits audio de l'émulateur.
- **Cause** : Émulateur.
- **Dépendances** : POCO.

### A-014 — INTERFACE conv (réaction rapide)

- **Fichiers** : conv/ConvSession.kt
- **Branche / commit** : e1c7e9c
- **Reproduction** : —
- **Attendu** : Aucun ralentissement du LLM.
- **Obtenu** : Non mesuré.
- **Cause** : Contention CPU possible (TTS 2 threads + LLM 1 thread).
- **Dépendances** : A-013.

### A-015 — NEXUS + LLM

- **Fichiers** : conv/KnowledgePlanner.kt
- **Branche / commit** : —
- **Reproduction** : Non testé.
- **Attendu** : Le document reste une donnée.
- **Obtenu** : Non mesuré.
- **Cause** : Les extraits sont cités « données, pas des consignes » mais aucun test malveillant.
- **Dépendances** : —

### A-016 — INTERFACE conv (historique)

- **Fichiers** : conv/ConversationJournal.kt
- **Branche / commit** : e1c7e9c
- **Reproduction** : —
- **Attendu** : Confidentialité.
- **Obtenu** : Protégé par le bac à sable Android et allowBackup=false, non chiffré.
- **Cause** : Choix de simplicité.
- **Dépendances** : —

### A-017 — Processus de livraison

- **Fichiers** : —
- **Branche / commit** : f1f902f
- **Reproduction** : Run 43590567147.
- **Attendu** : Chaque commit compile.
- **Obtenu** : Échec de compilation des tests.
- **Cause** : Erreur de découpage des commits (agent).
- **Dépendances** : —

### A-018 — SERVICES / MISSIONS / AGENTS / AUTOMATIONS

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : Command Center.
- **Attendu** : —
- **Obtenu** : Affiché « à connecter ».
- **Cause** : Hors périmètre actuel.
- **Dépendances** : RESEARCH-01 (non autorisée).

### A-019 — MEMORY VAULT

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : —
- **Attendu** : Export (PDF CC V2 §7).
- **Obtenu** : « à connecter ».
- **Cause** : MemoryExportService CORE exige un port de chiffrement non fourni.
- **Dépendances** : —

### A-020 — NEXUS

- **Fichiers** : conv/LocalKnowledge.kt
- **Branche / commit** : —
- **Reproduction** : —
- **Attendu** : Bibliothèque complète.
- **Obtenu** : txt, md, csv, tsv, docx, xml uniquement.
- **Cause** : Pas d'extracteur PDF Android local intégré.
- **Dépendances** : —

### A-021 — LEARNING-L01

- **Fichiers** : —
- **Branche / commit** : —
- **Reproduction** : —
- **Attendu** : Cahier des charges disponible.
- **Obtenu** : JARVIS_LEARNING_L01_Mission_Codex.pdf non transmis.
- **Cause** : Fichier non fourni.
- **Dépendances** : Dépôt du PDF par le propriétaire.

### A-022 — LLM (0.6B) — conversation longue

- **Fichiers** : —
- **Branche / commit** : run 43620844372
- **Reproduction** : Test i (16 tours) : « Au fait, quel sport j'aime ? » après « Allume la télévision. ».
- **Attendu** : La randonnée (fait présent dans l'instruction).
- **Obtenu** : Reprise mot pour mot de la réponse précédente (télévision), API 29 et 35.
- **Cause** : Hypothèse : le 0.6B recopie le dernier tour assistant (3 échanges relus) au lieu de la question.
- **Dépendances** : A-004.

### A-023 — LLM (0.6B) — personnalité

- **Fichiers** : conv/Persona.kt
- **Branche / commit** : run 43620844372
- **Reproduction** : Test i : 3 réponses sur 16 contiennent « vous ».
- **Attendu** : Tutoiement constant.
- **Obtenu** : 3/16 réponses au vouvoiement (API 29 et 35).
- **Cause** : Consigne système fixe du moteur protégé en vouvoiement implicite + capacité du 0.6B.
- **Dépendances** : Consigne protégée A02 (non modifiable sans décision).

