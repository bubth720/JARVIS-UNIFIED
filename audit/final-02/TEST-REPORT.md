# FINAL-02 — Rapport de tests (preuves GitHub Actions)

Branche `feat/next-01-android-1p7b-20261126` (dépôt UNIFIED). **Aucun test n'a été supprimé, désactivé, affaibli ou falsifié.** Un test non exécuté n'est jamais compté comme réussi.

## Phase 1 — Déblocage CI

| Run | Commit | Résultat | Cause / correction |
|---|---|---|---|
| [45894239555](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45894239555) | `bc1c7c9` | ❌ 6 erreurs aux garde-fous (API 29 et 35), rien d'autre n'a tourné | `test_campaign_preservation` (×3) et `test_s04_campaign` (×3) ont besoin de l'historique git d'INTERFACE (`f73d4f5`), de `.github/workflows/v3-cockpit.yml` et des captures `labs/v3/captures/run-44391288619/*`. Ces ressources sont exclues du monorepo par conception. |
| [45899158387](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45899158387) | `5fc862c` | Garde-fous historiques ✅ ; Android annulé (remplacé par le push suivant) | Nouveau job **`historical-guards`** : il récupère **INTERFACE @ `e6489bf`** (historique complet, ressources intactes) et prouve que les fichiers de test sont **identiques blob pour blob** à `modules/interface/labs/v3/tools/tests`. Il exécute ensuite les 15 tests et `test_run_emulator.sh` **sans modification**. Le job Android dépend de lui ; les nouveaux tests tournent séparément dans le monorepo. Aucune archive APK ni capture n'a été copiée dans UNIFIED. |
| [45899843578](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45899843578) | `cf8ab42` | API 29 ✅ (qualification 11/11, audits 26/27) ; **API 35 ❌** (qualification 10/11, audits 27/27) | API 35 : `h_consentedMemoryProposeConfirmRecallDelete` → `StaleObjectException` d'UiAutomator dans `tap` (`V3CockpitTest.kt:521`). API 29 : l'audit `h4_loadUnloadCyclesDoNotLeak` dépasse le seuil (croissance > 40 Mio). |
| [45908509940](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45908509940) | `5db8f6b` | ✅ **API 29 : 11/11 + 27/27 ; API 35 : 11/11 + 27/27** ; garde-fous historiques ✅ | Seul changement : le log affiche maintenant le détail des audits. **Aucun test ni seuil modifié.** h4 : −38 Mio (API 29) et −1,4 Mio (API 35) sur 6 cycles. |

Les deux échecs du run `cf8ab42` ne se reproduisent pas au run suivant, avec le même code applicatif (`cf8ab42` → `5db8f6b` ne touche que le workflow). Je les classe donc **instables (flaky)**, sans les compter comme réussis :

- **h (API 35)** : élément d'interface obsolète au moment du clic. C'est un problème de synchronisation du test, pas de la fonction mémoire.
- **h4 (API 29)** : sur l'émulateur API 29, le PSS après déchargement oscille entre 412 et 468 Mio d'un cycle à l'autre (`audit-h4.json`). La mesure « dernier moins premier » sur 6 cycles est donc bruitée.

Deux corrections sont à décider : rendre `tap` robuste à un élément obsolète, et mesurer h4 sur une médiane. Je ne les ai **pas** appliquées, car elles touchent des tests de qualification : voir `FINAL-02-REPORT.md`.

## Phase 2 — Qualification de l'APK (run 45908509940, `5db8f6b`)

Le contrôle porte sur l'APK debug et sur la release non signée.

| Contrôle | API 29 | API 35 |
|---|---|---|
| Garde-fous du monorepo : intégrité de l'import au commit `a40db85`, verrou des sources, tests monorepo et final01, `test_capture_evidence`, `test_run_emulator.sh` | ✅ | ✅ |
| Garde-fous historiques INTERFACE @ `e6489bf` (15/15 + run_emulator) | ✅ (job commun) | ✅ |
| Entrées V3 vérifiées blob pour blob contre les verrous figés V1 et core-memory (23 fichiers) | ✅ | ✅ |
| Build Gradle : `testDebugUnitTest`, `assembleDebug`, `assembleRelease`, `assembleDebugAndroidTest`, `lintDebug` | ✅ | ✅ |
| Inspection de l'APK : une seule permission Android (RECORD_AUDIO), **pas d'INTERNET**, moteurs présents (`libjarvis_llm_a02.so`, `libjarvis_stt.so`, `libonnxruntime.so`), **aucun poids** (.gguf/.onnx/ggml/voices), `allowBackup=false`, `dataExtractionRules`, release **non débogable** et **non signée** | ✅ | ✅ |
| Provenance des modèles (lecture seule, Hugging Face) : licence apache-2.0, SHA-256 LFS et taille conformes au verrou V3, pour 0.6B et 1.7B | ✅ | ✅ |
| Qualification V3 complète en mode avion (pixel_6) | **11/11** | **11/11** |
| Audits (sécurité, injections, mémoire, sphère, stockage, cycle de vie) | **27/27** | **27/27** |

Lors de cette campagne, le modèle chargé est le **0.6B (ÉCO, défaut)**.

**Préservation des modules** :

- Le garde-fou `import_manifest.py` vérifie que `modules/{core,llm,voice,interface,nexus,services,evolution}` sont identiques, au commit d'import, aux SHA verrouillés. Il liste aussi les 15 fichiers modifiés depuis l'import, tous dans `modules/interface/labs/v3` (12 fichiers de l'application et de ses tests, plus le verrou V3 et deux outils).
- Les verrous V1 et core-memory figés sont **inchangés**.

**Nettoyage mémoire** :

- Audit h4 : PASS sur les deux niveaux d'API.
- Étude des modèles : déchargement `CONFIRMED`, PSS ≈ 85 Mio après déchargement.
- Audit m (24 tours) : croissance du PSS de 2 Mio sur API 29 et 20 Mio sur API 35, latence stable (médiane des 8 premiers tours ≈ médiane des 8 derniers).

**Sphère**, test P :

- 0 dessin au repos, en réflexion et après la réponse.
- `visibleChange` de 0,21 (API 29) et 0,20 (API 35) pendant la réponse.

## Phase 3 — Modèles

Voir `MODEL-COMPARISON.md`. Runs :

- [JARVIS-LLM 45899288719](https://github.com/bubth720/JARVIS-LLM/actions/runs/45899288719) : Linux, 4/4 ✅.
- [UNIFIED 45900016272](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45900016272) : émulateur API 35, 3/3 ✅. Le 1.7B à 768/1 a 4/59 tours coupés par le délai protégé de 90 s.
- Échec d'environnement non relancé : le run JARVIS-LLM [45899288588](https://github.com/bubth720/JARVIS-LLM/actions/runs/45899288588) (« Android prototype checks ») échoue avec 33/40 tests en `IOException` dans `MavenArtifactFetcher` : Robolectric n'a pas pu télécharger depuis Maven. Le même workflow est vert sur le même code applicatif (`9c3fc50`). Il est compté comme **non concluant**, pas comme réussi.

## Phase 4 — APK candidate

- Artefact **`next01-apk-candidate-5db8f6b9c4f51d8054ce9bed0cfa727edcc6844a`** : run 45908509940, artefact 15159920859, expire le 10/12/2026.
- `app-release-unsigned.apk` : SHA-256 **`da766bec0d74c928fe7b6557cb6c173c89637c2f97573a2064224958aa3ef79f`**.
  - **Identique dans les 4 jobs** des runs `cf8ab42` et `5db8f6b` : la build est reproductible.
  - **Non signée, non installée.**
- `app-debug.apk` du job API 29 : `fd94e44155b48ae5af37d0548079bec0e4730127ad2a2537e33871ae3b23173f`. Le debug varie d'un job à l'autre, car la clé de debug est propre au runner.

## Non exécuté (aucun n'est compté comme réussi)

- **Tout test sur téléphone réel** : voix réelle (micro et haut-parleur), latence, chaleur, batterie, 1.7B sur ARM.
- **Campagne de qualification complète avec le 1.7B chargé** : seule l'étude des modèles l'a chargé.
- **SERVICES** : désactivé. **EVOLUTION** : diagnostic seulement, sandbox non qualifiée.
