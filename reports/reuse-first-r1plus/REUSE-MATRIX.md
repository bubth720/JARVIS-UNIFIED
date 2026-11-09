# Matrice REUSE FIRST R1+

Les huit critères demandés figurent intégralement dans REUSE-MATRIX.json et REUSE-MATRIX.csv. Les SHA amont et lignes documentaires observées sont dans UPSTREAM-SOURCES.json. Les déclarations de performances amont ne sont pas des mesures JARVIS. Aucun moteur alternatif ou poids n’a été installé.

Décision : conserver les moteurs, profils, bases et design existants. Aucun remplacement n’est justifié par une mesure comparative Android dans cette mission ; aucun remplacement productif n’est proposé ou appliqué. CONNECTER signifie ici le seul adaptateur documentaire de test, jamais une activation productive.

| ID | Domaine | Existant / candidat | Décision | Portée |
|---|---|---|---|---|
| LLM-01 | LLM local | CORE LlamaLocalEngine + LLM LlamaBackend/OwnedStream existants / ggml-org/llama.cpp | CONSERVER | AUDIT_ONLY |
| LLM-02 | LLM alternatif | Même backend existant, profils préservés / google-ai-edge/LiteRT-LM | CONSERVER | AUDIT_ONLY |
| LLM-03 | LLM alternatif | Moteur local et politique one-heavy existants / mlc-ai/mlc-llm | CONSERVER | AUDIT_ONLY |
| STT-01 | Reconnaissance vocale | WhisperLocalEngine/whisper-android 1.0.0 de CORE / ggml-org/whisper.cpp | CONSERVER | AUDIT_ONLY |
| STT-02 | Reconnaissance alternative | Whisper et flux recorder existants / alphacep/vosk-api | CONSERVER | AUDIT_ONLY |
| VOICE-01 | Synthèse hors ligne | VOICE SDK, profils/packs validés et Android LocalTts dans CORE / k2-fsa/sherpa-onnx | CONSERVER | AUDIT_ONLY |
| VOICE-02 | Synthèse alternative | Même profil actif et contrats de lecture existants / OHF-Voice/piper1-gpl | CONSERVER | AUDIT_ONLY |
| MEM-01 | Mémoire et bases | SQLiteOpenHelper, confirmations MEM-01/MEM-02, NexusStoragePort / https://developer.android.com/jetpack/androidx/releases/room | CONSERVER | AUDIT_ONLY |
| DOC-01 | Consultation citée | DocumentaryGateway/1 + LocalRagService + CitationResolver M53 / NEXUS_EXISTING_M53 | CONNECTER | TEST_ONLY |
| DOC-02 | Coût des consultations | Validation des citations déjà faite dans le snapshot de Gateway / NEXUS_EXISTING_M53 | OPTIMISER | TEST_ONLY |
| ZIM-01 | Kiwix et connaissances | Port ArchiveReader/ZIM en lecture seule, aucun backend productif activé / kiwix/libkiwix | CONSERVER | AUDIT_ONLY |
| ZIM-02 | Lecture ZIM native | Même port documentaire et citations existants / openzim/libzim | CONSERVER | AUDIT_ONLY |
| SERV-01 | Automatisations Android | TaskCoordinator, SERVICES Guard/ApprovalGate et port Android existants / https://developer.android.com/develop/background-work/background-tasks/persistent | CONSERVER | AUDIT_ONLY |
| IPC-01 | Communication sûre | Contrats v1, corrélations, baux, refus et projections CORE existants / https://developer.android.com/develop/background-work/services/aidl | CONSERVER | AUDIT_ONLY |
| UI-01 | Interface/animation | Compose UI-01C + AvatarSession + contrôleur M54 déjà livrés / https://developer.android.com/jetpack/compose/animation | CONSERVER | AUDIT_ONLY |
| UI-02 | Rendu alternatif | Contrôleur M54, aucun renderer nouveau activé / airbnb/lottie-android | CONSERVER | AUDIT_ONLY |
| UI-03 | Rendu alternatif | Même contrôleur et ressources M54 préservés / rive-app/rive-android | CONSERVER | AUDIT_ONLY |
| UI-04 | Rendu 3D éventuel | Aucune architecture 3D qualifiée à remplacer / google/filament | CONSERVER | AUDIT_ONLY |
| LAB-01 | Qualification Android | Banc M51/R1, mêmes tests/assertions et versions Compose / M51_EXISTING_DIAGNOSTICS | OPTIMISER | LABORATORY_ONLY |

## Mesures réellement disponibles

Sur le même corpus M53 (trois textes fictifs), 60 appels alternés par variante après échauffement : médiane 1,059 ms → 0,935 ms et p95 1,198 ms → 1,078 ms. La référence est un consommateur de test avec une résolution publique redondante, pas un ancien parcours productif. La réutilisation conserve toutes les validations internes de Gateway et des payloads identiques. Aucun seuil de gain n’est imposé. Le heap 107 146 528 → 145 943 840 octets concerne toute la JVM de test, les deux variantes et le GC ; il ne mesure pas la RAM du seul adaptateur ou d’Android.

LLM TTFT/tokens/s, STT précision/RTF, TTS audible, IPC inter-APK, renderer GPU et batterie : NON QUALIFIÉS, valeurs absentes et jamais remplacées par zéro. Le coût en temps de développement des remplacements n’est pas inventé : la matrice donne les travaux et dépendances réels à prévoir.

## Conditions de réutilisation

- Ne pas migrer SQLite ou ajouter Room pour le seul confort de programmation.
- Ne pas changer de modèle, tokenizer/template, backend ou profil VOICE sans nouveau diff exact et validation.
- Ne pas ajouter un renderer avant qualification Android, droits des assets et preuve de libération des ressources.
- Garder un seul travail lourd et les protections existantes ; préparation mini-PC après calibration matérielle séparée.
- Relire les licences du code et des modèles/contenus avant distribution ; plusieurs dépôts JARVIS n’ont pas de licence racine explicite, et cela n’est pas corrigé par une nouvelle licence inventée.
