# Audit JARVIS — Mission 001

Date : 15 octobre 2026. Périmètre : lecture et préparation, sans fusion de code.
Branche de travail UNIFIED : `audit/mission-001`, base `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b`.

## Conclusion

Conserver les capacités métier de JAVIS-Local-v2 comme CORE, retenir le moteur
llama.cpp et les protections de JARVIS-LLM 003B comme unique fournisseur LLM,
et préparer VOICE à partir du runtime neuronal et des profils FP32 005E/F.
005G reste un laboratoire de qualité ; ses réglages ne deviennent pas des valeurs
par défaut qualifiées. Aucun moteur ni source n'est copié dans UNIFIED ici.

Le clonage possède un chemin de code réel de création et de réutilisation de
profil. **La ressemblance personnelle, le naturel et le fonctionnement complet
sur Redmi Pad SE / POCO X8 Pro ne sont pas validés par cet audit.** Les résultats
ASR et les tests de lecture synthétique ne suffisent pas à les valider.

## Méthode et niveaux de preuve

- **Lu** : source, configuration, tests ou rapport présents au SHA indiqué.
- **Historique rapporté** : résultat consigné dans le dépôt ; non réexécuté ici.
- **Vérifié ici** : commande effectivement exécutée pendant cette mission.
- **Proposé** : contrat ou architecture à réaliser dans une mission ultérieure.

Clones HTTPS séparés sous `/tmp/jarvis-mission001`, sans checkout de travail des
sources ; lecture par `git show`, inventaires et archives aux révisions retenues.
Aucun push, modification source, suppression de projet, commit ou merge effectué.
Les archives temporaires et les clones ne sont pas des dépendances de UNIFIED.
Les branches distantes disponibles ont toutes été inventoriées. Les branches
anciennes ont été comparées par inventaire/historique ; la lecture fonctionnelle
approfondie porte sur les trois bases retenues, pas sur chaque ligne de chaque
ancienne branche. Les PR non exposées comme branches et branches supprimées ne
font pas partie de cet inventaire. Aucun état CI distant n'a été revalidé via API.

## Bases retenues et navigation des preuves

Les chemins cités ci-dessous sont relatifs au dépôt source correspondant, au SHA
immuable. Ils ne désignent pas des fichiers livrés dans UNIFIED.

- [CORE : main, 226e2e8](https://github.com/bubth720/JAVIS-Local-v2/tree/226e2e8cc3eebd479805b89d035eb5c1cbcad540).
  Références : `AGENTS.md`, `docs/PROJECT_KNOWLEDGE.md`,
  `app/src/main/java/com/stark/jarvislocal/`, `app/src/test/`.
- [LLM : mission-003b-resources, 1756e29](https://github.com/bubth720/JARVIS-LLM/tree/1756e29557287550b5cfdffdd911cada2a302db6).
  Références : `domain/src/main/kotlin/fr/jarvis/domain/`, `app/src/main/cpp/`,
  `app/src/main/java/fr/jarvis/llm/`, `docs/VALIDATION_003B.md`.
- [VOICE : feat/android-pocket-cloning-005d, 9429a9e](https://github.com/bubth720/JARVIS-VOICE/tree/9429a9ebf0f21909ac6c59a07491fa2bca027493).
  Cette branche inclut aussi 005E/F/G : `pocketRuntime/`, `voicePrototype/`,
  `voiceQuality/`, `docs/mission005e/`, `docs/mission005f/`, `docs/mission005g/`.
- [VOICE CPU : 6d8a04b](https://github.com/bubth720/JARVIS-VOICE/tree/6d8a04bfb49f0d08ac948c8bb981fc6a92f2e7c4),
  `prototype/` : piste future CENTRAL, pas le runtime Android retenu.

CORE : toutes les branches distantes de correction/documentation sont ancêtres
de main. LLM : main ne contient que deux documents ; les cinq branches de missions
sont hors main. VOICE : main ne contient que README ; les six branches de
fonctionnalités sont hors main. Sa branche par défaut distante est le prototype
CPU, moins avancé que la branche Android 005D/E/F/G. Ne pas choisir seulement main
ou la branche par défaut pour une migration.

## Tableau comparatif des composants

| Capacité | CORE actuel | LLM 003B | VOICE Android / CPU | Choix proposé |
|---|---|---|---|---|
| Orchestration et UI | `JarvisCore`, `MainActivity`, `AppGraph` ; commandes et historique | ViewModel, session textuelle bornée | UI distinctes pour probe, prototype et A/B | Une UI, cas d'usage CORE, adaptateurs |
| Inférence GGUF | wrapper `llama-android:0.1.1`, modèle résident, mutex | llama.cpp CPU/JNI épinglé, import SHA-256, annulation native | Aucun LLM | Un seul backend issu de LLM ; remplacer progressivement le wrapper CORE |
| Modèles | assets `jarvis.gguf` et `whisper.bin`, contrôles de taille | Qwen3 0.6B/1.7B Q4_K_M, slots SMALL/MAIN stricts | Packs ONNX avec manifests/hashes | Registre d'artefacts versionné ; adaptateurs spécifiques |
| Protections | gestion OOM partielle, timeout coroutine | réserve RAM, PSS, batterie, thermique, premier plan, deadline, baux | un thread ONNX, garde 2 Gio, arrêt thermique/lowMemory | Conserver chaque garde et coordonner globalement |
| Mémoire durable | SQLite `memories`, `/remember`, bouton Ajouter | conversation RAM ; « memory » 002B = télémétrie RAM | profils vocaux persistés, pas mémoire conversationnelle | CORE propriétaire ; confirmation avant écriture |
| Historique | SQLite `messages` | session en RAM | caches PCM et notes privées bornés | Distinguer historique, souvenir, audio, diagnostics |
| Documents | PDFBox, passages, recherche lexicale, extraits/pages | interfaces futures `RetrievalIndex`, pas RAG implémenté | Sans objet | Garder PDF/RAG ; pas d'OCR ni embeddings annoncés |
| Réponses locales et outils | salutations, heure, `/docs`, `/remember` | catalogue SQLite éditorial, variantes et clarification, JSON import/export | Sans objet | Conserver les deux types de réponses avec priorité explicite |
| Reconnaissance | WAV mono 16 kHz PCM16 + Whisper local français | Absente | import/extraction audio, pas STT conversationnel | CORE garde Whisper et capture |
| Synthèse | Android TextToSpeech | Absente | ONNX neuronal français FP32, profils JVFP1, PCM privé ; CPU PyTorch distinct | VOICE neuronal, aucun repli Android générique automatique |
| Personnalisation vocale | choix TTS système | Absente | extrait 5–15 s, consentement, profil lié au pack, A/B 005G | Préserver les profils, qualification humaine requise |
| Sauvegarde/transfert | aucune archive globale ; backup Android désactivé | export catalogue/diagnostic, pas historique persistant | imports privés et caches ; backup système exclu | Archive explicite et chiffrée à concevoir |
| Hybride PC | non implémenté | backend interchangeable, aucun transport PC | prototype HTTP CPU loopback authentifié | Garder comme référence ; protocole LAN/USB futur séparé |

## Ce qui est implémenté et ce qui est testé

### CORE

`JarvisCore.kt` confirme le routage réponses locales → commandes → preuve PDF →
contexte/RAG/mémoires → LLM. `LocalDatabase.kt` conserve quatre tables et la
migration 1→2 non destructive ; `insertOrThrow` et contrôle de -1, transaction
complète pour document/passages. Les anciens schémas 1/2 sont identiques.
`PdfImporter.kt` conserve le texte découpé, pas une copie du PDF original : une
sauvegarde future ne pourra pas recréer un original absent.

Historique rapporté dans `docs/PROJECT_KNOWLEDGE.md`, actualisations 003/004 :
33 cas SQLite (11 scénarios × API 24/25/35 Robolectric natif), 7 tests d'heure,
aucun ignoré ; build et Lint réussis, 34 avertissements. Ce sont des tests JVM,
pas des essais sur appareils. IA complète, microphone, Whisper, PDF/RAG et TTS
sur appareil non démontrés par cette campagne ; modèles absents de l'APK de
validation historique. Les défauts anciens de migration destructrice sont
corrigés : ne pas les reporter comme encore présents.

Risques restant visibles : chargement LLM sans libération publique dédiée à la
pression mémoire ; modèle reconnu surtout par taille ; prompt limité en caractères
sans budget total tokenisé ; PDF/corpus/audio sans plafonds globaux explicites ;
`WavRecorder.stop()` attend au plus deux secondes sans preuve de fin du worker.
`/remember` écrit directement ; le dialogue Ajouter exprime une intention mais
n'implémente pas le protocole commun de confirmation proposé. Le retrait des
permissions réseau du manifeste ne qualifie pas le moteur TTS externe.

### LLM

`LanguageModel` sépare load/generate/requestStop/unload/close. Source llama.cpp
épinglée à `1b70350c92563449576bcbbf552994b1d1ed847d` ; vérifications GGUF/JNI,
contexte et sortie bornés. Catalogue éditorial local et import/export JSON
implémentés ; embeddings seulement sous forme d'interface, désactivés.
`ResourceCoordinator` gère travail lourd et résidence séparément ; annuler ne
libère pas le bail avant fin effective. Il ne coordonne pas encore CORE/VOICE.

Rapport `docs/VALIDATION_003B.md` et JSON `docs/evidence/mission003b-e9d408e.json` :
55 tests domaine, 16 simulations Android API35, 1 CTest natif réussis ; build ARM64,
Lint 0 erreur/36 avertissements CI et contrôle APK rapportés. Commit testé
`e9d408e77319f4998821e723ef8bc0c872ee3274`, run GitHub `38636152472`.
Diff testé→base auditée : trois fichiers documentaires seulement, vérifié ici.

Budget SMALL 2 Gio, MAIN 4 Gio ; réserve `max(1 Gio, 20 % RAM accessible,
seuil low-memory Android + 256 Mio)`. Crédit PSS seulement si modèle déjà résident.
FULL_POWER refusé ; batterie <10 %, thermique sévère, capteurs requis absents,
lowMemory ou arrière-plan entraînent refus/arrêt selon le chemin concerné.
Conserver cette politique ; ne pas déduire un budget Android du RSS Linux.
Les relevés utilisateur de ~593 Mio PSS et les comparaisons cloud ne qualifient
pas un budget plus faible. Régression JNI, autonomie et thermique physiques
restent à mesurer. La compatibilité de nouveaux GGUF n'est pas universelle :
slots, architecture, tailles et profils sont aujourd'hui spécifiques à Qwen3.

### VOICE

`VoiceState.kt` : PTVB1 est un **preset**, pas un profil cloné. `PersonalVoiceProfile`,
`CandidateVoiceEncoder`, `ExperimentalModelPack` et `ExperimentalEngine` : création
réelle FP32, intégrité, 18 états exacts, pack identifié, activation atomique,
consentement et stockage privé. JVFP1 n'est pas compatible par simple renommage
avec PTVB1 ou les profils safetensors CPU. 005F conserve lecture différée STATIC
PCM16, preuve de progression des frames et cache privé de dernière synthèse.
005G ajoute sampler multi-étapes, caches A/B et notes explicites après lecture.
Les réglages d'échantillonnage ne sont pas une personnalisation de timbre validée.

Résultats **historiques rapportés**, non rejoués pendant cet audit :

| Campagne | Résultats consignés | Limite |
|---|---|---|
| CPU prototype | 37/37 tests, voix prédéfinie Estelle et génération hors ligne | Modèle public sans clonage ; serveur loopback, pas Android |
| 005E FP32 | 32/32 JVM privées, 4 tests Android confidentialité/import ; 18/18 sorties finies, 7/18 parité stricte | 11 échecs stricts ; WER tiny 40,97 %, small 9,03 % ; pas de ressemblance humaine validée |
| 005F | 29 réussis/41, 12 ignorés ; 10/10 instrumentés synthétiques, deux passages | Xiaomi personnel encore à vérifier ; « stable » décrit la livraison, pas une certification du clonage |
| 005G publique | 33 réussis/46, 13 ignorés ; 14/14 instrumentés Android35 x86_64 ; Lint 29 avertissements | Sans poids privés ni profil personnel sur émulateur |
| 005G locale privée | 35 réussis/46, 11 ignorés ; 72 cas sampler conformes ; 114 sorties finies dont 66 strictes | 48 échecs de parité audio indépendante ; naturel non validé |
| 005D probe | 4/5 instrumentés, échec strict AudioTrack connu | Non corrigé par les réussites des autres modules |

Sources : `prototype/docs/results.md` sur branche CPU ;
`docs/mission005e/RESULTATS.md`, `docs/mission005f/RESULTATS.md`,
`docs/mission005g/RESULTATS.md` et `VALIDATION-CI.json` sur branche Android.
005G commit testé `b0a3a477012bb6c953372a6a8e26ec3f997c5cbc`, run `38718352623`.
Diff vers base auditée : trois documents seulement, vérifié ici.

Le pack FP32 et les clés privées de signature ne sont pas dans Git ; leurs
emplacements cités dans les anciens rapports ne prouvent pas leur présence dans
cet environnement. Aucun secret, poids gated ou audio personnel n'a été demandé.
Licence/attribution et conditions des poids restent à vérifier pour toute
redistribution. Ne pas utiliser le TTS Android de `app`/fallback probe comme
remplacement de la voix personnalisée.

## Conservation et remplacement progressif

| Élément | Décision | Préalable au remplacement |
|---|---|---|
| SQLite CORE, corrections heure et migrations | Conserver schéma, données, fixtures | Export/restauration équivalente, refus des versions inconnues |
| PDFBox, découpage, recherche lexicale | Conserver derrière ports | Tests de référence, limites de volume ; OCR futur séparé |
| Catalogue LLM et variantes utilisateur | Conserver séparé des souvenirs et documents | Import idempotent et résolution explicite des conflits |
| LlamaLocalEngine CORE et copie par taille | Remplacer par adaptateur LLM 003B | Parité des fonctions + import vérifié + un seul moteur empaqueté/actif |
| PromptBuilder et orchestration Activity | Encapsuler puis remplacer par cas d'usage et budget tokenisé | Scénarios de non-régression, citations, annulation |
| Whisper et capture WAV | Conserver fonction, fiabiliser adaptateur | Arrêt réel, finalisation, nettoyage et pression mémoire |
| VOICE FP32/JVFP1 et lecteur 005F | Conserver candidat expérimental | Écoute et mesures physiques, identité du pack/profil préservée |
| VOICE 005G | Garder comme banc de comparaison | Aucune promotion sans gains mesurés et écoute humaine |
| TTS système CORE / VOICE foundation | Ne pas retenir dans la synthèse cible | Afficher indisponibilité neuronale et conserver réponse texte |
| Prototype CPU VOICE | Référence CENTRAL distincte | Compatibilité des profils/protocole et licences à qualifier |

## Difficultés et vérifications de cette mission

Réussis ici : accès Git aux trois sources, inventaire complet des branches
annoncées, `git fsck --full` des trois clones, contrôle d'ascendance vers main,
diff des commits historiquement testés vers les bases LLM/VOICE auditée,
empreinte inchangée de `SafetyPolicy.kt`
(`7fefc8ce65f80375666eefb8ea05d44ab5edee940d49c2d53183e675818f3999`).

ZIP vocaux 005F/G : CRC, tailles APK et SHA-256 concordent avec `delivery.json` :
005F `af9f1b3974163c8c255f551c88bdb65a9e9bd67adf75f43d75b0edd1755bf083` ;
005G `ab690aa2d4dfad8f80a226c28d59c37e11f994f58e2f45963210c24644bd843c`.
Cela vérifie la concordance, pas une nouvelle vérification cryptographique de
signature APK ; les certificats et alignements restent des résultats rapportés.
Fixture SQLite historique exécutée en mémoire avec Python : intégrité OK,
2 messages, 1 souvenir, 2 documents et 3 passages. Ce contrôle ne rejoue ni
SQLiteOpenHelper Android, ni les tests de migration Robolectric.

Non exécutés : builds Android, suites Gradle/JVM/CTest, APK sur émulateur ou
appareil, génération GGUF/Whisper/ONNX et écoute humaine. Gradle, SDK/adb, CMake
et Kotlin CLI n'ont pas été trouvés dans le PATH ; aucune chaîne Android ou gros
modèle n'a été installé pour cette mission documentaire. Ce n'est pas un échec
fonctionnel constaté. Les rapports historiques sont accessibles dans Git mais
les jobs/artefacts Actions distants n'ont pas été réinterrogés.

Difficultés de préparation : maturité différente des branches, résultats répartis
sur plusieurs missions, versions Android différentes, profils incompatibles,
clés et packs absents du versionnement, défaut AudioTrack 005D et parités
numériques incomplètes. Aucun de ces points n'est masqué par la documentation.

## Inventaire immuable des branches inspectées

### JAVIS-Local-v2

| Branche distante | SHA audité |
|---|---|
| `docs/mission-002-project-knowledge` | `e0417e1609b478073e7cd019a25f8146a25a0fb8` |
| `fix/api-24-25-time-reply` | `d7e51b4ac55b0726e5289b7f062478903fb7aa67` |
| `fix/sqlite-data-preservation` | `7a5b53e3247dc7132eb9e5648ecf4169a4054d62` |
| `main` | `226e2e8cc3eebd479805b89d035eb5c1cbcad540` |

### JARVIS-LLM

| Branche distante | SHA audité |
|---|---|
| `main` | `917e3351f9b525857b6aa019e98d07872d8f6e76` |
| `mission-002-prototype` | `aa6b3d37c9109dc3da1296bc00214839bb218e39` |
| `mission-002b-memory` | `204c6c9a117501286aac54202c6e7dd1365c48b5` |
| `mission-002c-tablet` | `fbda51f3ed762d8e63d5397618daf052567002d6` |
| `mission-003-catalogue` | `0b5eba7a37d9304e2a33e66ab6e84a0f70e02a2a` |
| `mission-003b-resources` | `1756e29557287550b5cfdffdd911cada2a302db6` |

### JARVIS-VOICE

| Branche distante | SHA audité |
|---|---|
| `feat/android-pocket-cloning` | `a5e2c056a3e98bee7132aa8e50dcf0d5ec18d387` |
| `feat/android-pocket-cloning-005d` | `9429a9ebf0f21909ac6c59a07491fa2bca027493` |
| `feat/android-pocket-probe` | `de38598faf7a3a09c2d0f53d86a150725c953f01` |
| `feat/android-tts-foundation` | `2aad62625121fa436e5af84bbd9d01f00aafceed` |
| `feat/pocket-tts-cpu-prototype` | `6d8a04bfb49f0d08ac948c8bb981fc6a92f2e7c4` |
| `main` | `b80b1728c481200b3b0e11c0843f1a268a184fa1` |

