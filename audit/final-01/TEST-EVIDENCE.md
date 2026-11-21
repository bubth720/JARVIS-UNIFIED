# F00 — Preuves de test

Chaque ligne indique le SHA exact testé, l'endroit où le test a tourné et son résultat. Les mentions `NOT_RUN` et `BLOCKED` ne valent jamais PASS.

## Rejoué localement le 21/11/2026

Environnement : conteneur Linux x86-64, Python 3.12.3 et 3.13.18, JDK 17 et 21, kotlinc 2.1.20. Il n'y a ni SDK Android ni KVM, et le Maven Google est refusé par la politique réseau.

Le journal brut est dans `local-replay-results.txt`.

| SHA | Commande | Résultat |
|---|---|---|
| UNIFIED `0af322c1e353` | `python3 -m pytest -q <suite>` pour arch01, campaign, gpu_forge, integration, nexus_n01_a2, reuse_r1plus, v1, workspace | **PASS** : 222 tests passés, 1 ignoré, 0 échec |
| UNIFIED `0af322c1e353` | `python3{.12,} -m tooling.research_b0.offline_runner` | **FAIL** : 63 tests, 2 erreurs dans `test_preservation`. Le garde fige 525 fichiers à sa propre base, et un fichier d'audit a changé depuis (R-07) ; s'y ajoute la disposition des checkouts voisins. Aucun échec fonctionnel. `production_connected=false`. |
| UNIFIED `f1f30dc3cef2` (tête B0) | idem | Python 3.12 : **PASS** 63/63. Python 3.13 : **FAIL** (21 échecs, 15 erreurs) = A-037, corrigé par `977e475`. |
| INTERFACE `e6489bf011c8` | `bash labs/v3/tools/tests/test_run_emulator.sh` (avec `CAPTURES_ONLY=1` défini) | **PASS** 19/19 |
| INTERFACE `e6489bf011c8` | `pytest labs/v3/tools/tests` | **PASS** 15/15 |
| INTERFACE `e6489bf011c8` | `python3 labs/v3/tools/check_scope.py --interface .` | **PASS** (V1 : 430 fichiers figés) |
| INTERFACE `e6489bf011c8` | JVM kotlinc, 10 classes `conv/*Test` pures | **PASS** 37/37 |
| EVOLUTION `c4abfb035e3e` | `gradle test` (JDK 17) | **PASS** 51/51, 0 ignoré |
| EVOLUTION `c4abfb035e3e` | lecture du code | Verrous présents : `SANDBOX_NOT_QUALIFIED`, `mayExecute=false`, `productionAuthorized=false`, runner `NOT_RUN` |
| NEXUS `5f1019344097` | `gradle test` | **NOT_RUN** : plugin `com.android.library` sur `dl.google.com` (403 du proxy) |
| SERVICES `8d80d09d6aab` | `gradle test` | **NOT_RUN** : `androidx.sqlite:sqlite-bundled-jvm` sur `dl.google.com` (403) |
| CORE, LLM, VOICE | — | **NOT_RUN** en local (Android et NDK) ; preuves CI ci-dessous |

## CI GitHub (SHA vérifié par l'API)

| Dépôt | Run | SHA | Résultat | Remarque |
|---|---|---|---|---|
| INTERFACE | [44638538519](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/44638538519) | `e6489bf011c804fcbb699f41416e4b389e50d66a` | **PASS** | Journaux lus test par test : qualification 11/11 et « audit-results.txt: 30/30 criteria, 26 recorded cases » sur API 29 et 35 ; audit `aapt` debug et release PASS. Artefacts non téléchargeables ici (hôte blob refusé) : les verdicts proviennent des journaux. |
| INTERFACE | [44391288619](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/44391288619) | `b1224ae612999ac6abe6387f50778694b7e16168` | FAIL (historique conservé) | API 29 11/11, API 35 9/11 ; audits 28/30 (K, P) |
| INTERFACE | [44034195561](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/44034195561) | branche `gpu-forge-g02` | PASS | 22 captures × 2 API vérifiées |
| NEXUS | [44273871327](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44273871327), [44273924562](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44273924562) | `5f10193440972ba25b30645d2811537418eface5` | PASS | N01-A3 et préflight des quotas NEX-07 |
| UNIFIED | [44365141928](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/44365141928) | `f1f30dc3cef2043ccfc68347c2cdc9b4e732de88` | PASS | B0 (Python 3.12, namespace sans réseau) |
| UNIFIED | 44391205905 | `977e475` | PASS | B0 après A-037 |
| EVOLUTION | [40415562523](https://github.com/bubth720/JARVIS-VOLUTION-/actions/runs/40415562523) | `68e095660975cca9004d474d35ad3daad3eebd80` | PASS | `c4abfb0` = `68e0956` + 2 fichiers de documentation ; rejoué localement à `c4abfb0` |
| SERVICES | 40852606525 | `8d80d09d6aabf6eac00a7bc6bb4930862bd72812` | PASS | M50, 29/10 |
| LLM | 43625706542 | `9c3fc500ea74a40c4bfe9d3c3ffd66d09848fc71` | PASS | Successeur A-002 et prototype Android |
| VOICE | 43625576432 | `58907351324b5a86385b08a2b61595efedb28357` | PASS | Gardes A-003 |
| CORE | — | `5da98383ed12` | **UNKNOWN** | API CORE non accessible depuis cette session |

## Ce qui n'a jamais été exécuté

- **Tout essai sur appareil réel** (POCO) : micro, audio, batterie, chaleur, JNI, TalkBack. Statut `BLOCKED_DEVICE`.
- **Toute sandbox EVOLUTION** : `SANDBOX_NOT_QUALIFIED`.
- **Toute mesure TTFT, p50/p95 ou thermique sur appareil** : aucune valeur ne doit être citée.
