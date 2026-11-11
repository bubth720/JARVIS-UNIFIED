# Mission P0 / M01–M03 — A02 et V1-A : état vérifié (11/11/2026, ~23:55 UTC)

**Décision : GO-LAB-ONLY atteint sur émulateurs.** L'APK V1-A charge réellement le modèle Qwen3-0.6B autorisé, scellé par A02, dans le bac à sable applicatif Android. Elle répond en mode avion sur API 29 et API 35. Ce n'est **pas** une qualification sur téléphone : DEVICE-01 (POCO) reste NOT_RUN, faute d'autorisation.

## Branches et commits (aucune fusion dans `main`, aucune installation sur appareil)

| Dépôt | Branche | Commit | Rôle |
|---|---|---|---|
| bubth720/JARVIS-LLM | `claude/repos-folders-analysis-sr65sg` | `c00035b6324a68165748b167e19802029764a52f` | A02 (`a02/`) : memfd scellé, ouverture et mmap servis depuis le fd scellé, journaux llama.cpp |
| bubth720/JARVIS-INTERFACE | idem | `4ed3f99c198fde3b559433bb6fc71c46851c0a3e` | Labo V1-A (`labs/v1a/`) : CORE + A02 + INTERFACE |
| bubth720/JARVIS-VOICE | idem | `1a54da86337394ab702ae35c45c57574cef130cb` | VOICE-00 (inchangé ; non intégré) |
| bubth720/JARVIS-NEXUS | idem | `d2b59e07c329f7d0bfd458a440f831bdc989c4b3` | NEXUS-00 (inchangé) |

Modèle autorisé : `unsloth/Qwen3-0.6B-GGUF` @ `50968a4468ef4233ed78cd7c3de230dd1d61a56b`, 396 705 472 o, SHA-256 `ac2d97712095a558e31573f62f466a3f9d93990898b0ec79d7c974c1780d524a`, apache-2.0. Il n'est ni commité, ni embarqué dans l'APK.

## Causes de l'échec de chargement Android et correctifs (sans affaiblir A02)

| # | Symptôme | Cause | Correctif | Preuve |
|---|---|---|---|---|
| 1 | « Métadonnées GGUF invalides » | SELinux interdit à une app de rouvrir son memfd via `/proc/self/fd/N` | `-Wl,--wrap=fopen` : seul le chemin enregistré par l'appel en cours est servi depuis un `dup` du **même** fd scellé (`168f562`) | run 43093246716 → résolu |
| 2 | `mmap` EPERM (lu grâce à la capture des journaux llama.cpp, `1325a5a`) | Les noyaux antérieurs à 6.7 refusent `MAP_SHARED` sur un memfd scellé en écriture | `-Wl,--wrap=mmap` : `MAP_PRIVATE` uniquement pour une projection en lecture seule de l'inode scellé, avec les 4 sceaux vérifiés (`c00035b`) | run 43118616305 → résolu |
| 3 | Vérification NDK, code de sortie 74 | `nm \| grep -q` casse le tube sous pipefail | table des symboles écrite dans un fichier, puis recherchée | run 43119890553 |

Invariants conservés : aucun chemin hôte, SHA-256 sur les octets copiés puis re-haché après scellement, identité inode/périphérique vérifiée, chargeur par chemin non exporté, inode source jamais projeté, politique protégée du moteur (ctx 768, 1 thread) respectée.

## Résultats

| Test | Environnement | Résultat | Preuve |
|---|---|---|---|
| Gardes historiques, suites adversariales natives (34) et JNI (10) | Linux | **PASS** | A02 run 43119890553 |
| Vrai GGUF via A02 (génération, streaming, Stop, 10 cycles sans fuite) | Linux | **PASS** | idem |
| NDK arm64 : ELF, 16 KiB, chargeur par chemin absent, `__wrap_fopen`/`__wrap_mmap` liés | CI | **PASS** | idem |
| Suite A02 via `adb shell` | Émulateurs API 29 et 35 | **PASS** | idem (API 29 relancé après corruption d'image d'émulateur, problème d'infrastructure) |
| Gardes M50 et successeur, 9 sources extraites sans modification, 12 tests unitaires, Lint | CI | **PASS** | V1-A run 43121833338 |
| Vérification APK : testOnly, aucune permission, aucun modèle embarqué, 16 KiB | CI | **PASS** | idem |
| A02 dans `untrusted_app`, refus visibles, session CORE sans modèle | Émulateurs API 29 et 35 | **PASS** | idem |
| **Conversation réelle CORE → A02 → INTERFACE, mode avion (3 tours, streaming, Stop, déchargement)** | **Émulateur API 29** | **PASS** | idem |
| **Idem** | **Émulateur API 35** | **PASS** | idem |
| Téléphone POCO (DEVICE-01) | Appareil réel | **NOT_RUN** | attend ton autorisation ([protocole](DEVICE-01-PROTOCOL.md)) |

### Mesures (émulateur x86_64, pas un téléphone)

| | API 29 | API 35 |
|---|---|---|
| Import + chargement scellé | 3,1 s + 14,4 s | 3,8 s + 7,4 s |
| Premier texte visible (tours 1/2/3) | 28,5 / 17,7 / 19,0 s | 13,4 / 15,2 / 17,5 s |
| Ouvertures servies depuis le fd scellé / projections privées | 3 / 1 | 3 / 1 |
| RSS avant → chargé | 149 → 645 Mo | 176 → 656 Mo |
| shmem chargée → après déchargement | 373 Mo → 0,5 Mo | 387 Mo → 15 Mo |
| Arrêt (vidage) | 1 ms | 1 ms |

Réponses réelles (identiques sur les deux API) :
1. « Bonjour, présente-toi en une phrase. » → « Bonjour ! Je suis JARVIS, votre assistant local. » ✔
2. « Je m'appelle Thomas. » → « Bonjour ! Je suis Thomas, mon assistant local. » ✘ (confusion d'identité)
3. « Comment je m'appelle ? » → même réponse ✘

La chaîne technique fonctionne. La **qualité multi-tour est insuffisante** : modèle 0.6B, 48 jetons par réponse, historique court.

## APK

- Artefact : `JARVIS-V1A-LAB-APK-4ed3f99c198fde3b559433bb6fc71c46851c0a3e` (ID 13901377795, expire le 11/12/2026). Page du run : https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/43121833338
- SHA-256 de `app-debug.apk` : `6d632fa6ac93d3dfe2093da2407b4bdf60e649ce19480d47bbb601e03715fe5f`
- Paquet `fr.jarvis.v1a.lab`, testOnly (installation : `adb install -t`), minSdk 29, arm64-v8a + x86_64, signature de debug. Le modèle n'est pas inclus : il s'importe depuis l'écran de l'app et son SHA-256 est vérifié.

## Restant / bloqué

1. **DEVICE-01 (POCO)** : NOT_RUN. Nécessite ton autorisation explicite d'installation.
2. **M01, broker A03–A09** : BLOCKED, en attente de tes décisions G-A et G-ROOT/A01 (rapport M00). A01 reste fermée.
3. **M03, stabilité du cockpit M51** (plantage Compose SnapshotStateObserver sur API 29, SAF) : NOT_RUN. Le chemin V1-A est stable, mais le cockpit historique n'est pas corrigé.
4. **Qualité et latence** : réponses multi-tour incorrectes, 13 à 28 s avant le premier texte sur émulateur à 1 thread. Changer de modèle ou de politique moteur nécessite ton autorisation.
5. Report des correctifs sur les PR existantes (#17 LLM, #27 VOICE, #14 NEXUS) : nécessite ton accord.
6. VOICE, sphère, avatar et personnalités : préparables séparément, volontairement non intégrés.
