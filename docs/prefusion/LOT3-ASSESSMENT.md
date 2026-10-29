# Lot3 — bilan de pré-intégration contrôlée

**PARTIAL / BLOCKED pour l'intégration Android.** Aucune APK unifiée livrée ni déclarée utilisable. Travaux de laboratoire OFF, documents et tests seulement. Missions propriétaires distribuées en parallèle conformément au lot UNI-PF-02. Aucun merge, migration, changement de licence/ABI/minSdk ni activation sensible effectué.

## UNIFIED : développement et validation locale

Base mission `e4c678faf630a0a98adfaecd7a87fc11dfd82486`, arbre `d9274d820c9bcf46fe580bb13149371af31d509d`. Branche `codex/prefusion-lot3-unified-20261029`, PR brouillon vers `mission/prefusion-lot3-20261027` seulement. Commit/arbre de livraison et URL de PR communiqués après publication ; ne pas confondre le commit local de reconstruction avec le commit GitHub.

Le clone a échoué sur le proxy8080 ; `gh auth status` indique le jeton GH_TOKEN invalide, aucune identité ou secret configuré confirmé par l'environnement. Le connecteur GitHub a permis la lecture et la publication. Les303 fichiers de base ont été récupérés par API au SHA immuable puis vérifiés contre leurs303 empreintes blob Git exactes. Aucun contournement réseau. Checkout local reconstruit pour tests, pas de worktree.

Nouveaux fichiers : `tooling/integration/lot3_lab.py`, `lot3_scope.py`, `lot3_tests/test_lab.py`, `.github/workflows/prefusion-lot3.yml` et les fichiers `docs/prefusion/LOT3-*`. Les303 fichiers historiques restent byte-identiques. Les schémas v1, propositions v2, registres, BOM et verrous restent inchangés.

Le scénario TXT/CSV synthétique retourne explicitement UNSUPPORTED sans réponse ni citation inventées. Le consommateur Python refuse faux READY, rejeu, mutation d'identité/digest, citations, transport activé et écriture. Ce n'est pas un test E2E des applications Android. [Matrice des contrats](LOT3-CONTRACT-MATRIX.md), [décisions ADR-002 proposées](LOT3-ADR-002-DECISIONS.md).

Plateforme : Linux, Python3.12.14. [Résultats détaillés](LOT3-LOCAL-RESULTS.json).

| Commande réellement exécutée | Résultat unique |
| --- | --- |
| `python3 -m tooling.integration.ci --output /tmp/lot3-unified-ci` | 167 PASS, 0 échec/erreur/saut ; 6 validations exit0 dont validate_unified, v1/v2 locks/proposals/comparison/contracts |
| `python3 -m unittest discover -s tooling/integration/uni08_tests -v` | U00 : 23 PASS |
| `python3 -m unittest discover -s tooling/integration/uni08_u01_tests -v` | U01 : 23 PASS |
| `python3 -m unittest discover -s workspace/tests -v` | U02 : 20 PASS |
| `python3 -m unittest discover -s tooling/integration/lot3_tests -v` | Nouveau scénario : 14 PASS |
| `python3 -m tooling.integration.uni08_candidate docs/uni-08/BOM-PROPOSED.json` | exit0, verdict BLOCKED, aucune autorisation |
| `python3 workspace/check_plan.py workspace/modular-workspace.proposed.json` | exit0, REVIEW_ONLY, runtime_links_enabled0 |
| `python3 -m tooling.integration.lot3_scope --base HEAD` | exit0, aucun chemin interdit ; HEAD local = reconstruction de la base mission |
| `python3 scripts/validate_unified.py` | exit0, 5 schémas, 5 exemples valides, 5 invalides refusés, 9 dépôts |

Total UNIFIED unique : **247 PASS, 0 FAIL, 0 ERROR, 0 SKIP** (233 régressions +14 nouveaux tests). Les répétitions de vérification ne sont pas additionnées. Backup30 inclus car cryptography existant disponible. Android/JVM/Robolectric/émulateur/physique UNIFIED : NOT_RUN ou non applicable au dépôt documentaire ; aucun nombre de cas Android non exécutés inventé.

## Relevé réel des huit PR antérieures

Relevé GitHub daté et métadonnées complètes dans [LOT3-PR-EVIDENCE.json](LOT3-PR-EVIDENCE.json). Toutes ouvertes, brouillon, merged=false au relevé. Les bases sont des branches `mission/prefusion-gates-20261026`, pas main. Les lignes suivantes sont des preuves CI distantes historiques observées, jamais des tests nouveaux du lot3. Les parents exacts, écarts de base et événements CI sont conservés dans le JSON.

| PR | SHA tête | SHA base / arbre tête | Runs observés et conclusions |
| --- | --- | --- | --- |
| JARVIS-UNIFIED #10 | `b8f22bb7091c29b654f5e958e97da4f94434b164` | `6b0ae1a1ca1a257446931a69bdff15a4f77ac019` / `78d0a20e70565da64ed98701e1bb26047e169f44` | 40577947695:success, 40548957355:success, 40548957713:success, 40548958161:success, 40548957667:success, 40548957578:success |
| JARVIS-NEXUS #8 | `201f0d2b03209de104157595a557143fe87eb94e` | `bdb51f77a5fe105dbff43d43032882fe1474a4ee` / `c6debf4d2fe4c539c460229c3efce2736d575f4d` | 40547468137:success |
| JARVIS-SERVICES #7 | `ea541d20b08f7ad0949354829a977f6752cbffa3` | `365da117ccb29b59ed990711b2c3f72472ce2d9d` / `41fad0a190d0517fa27bff37a871a5916a20845e` | 40548088662:success |
| JARVIS-LLM #6 | `6ae8a4f5c2490f6c9814e08957909a8e3a807180` | `12fc58a81ceee70eedbba2d0b187b1294bae6283` / `52a75bfb7b2ee102c958fd0a7bc642c560693fc2` | 40547525669:success, 40547525692:skipped, 40547525750:skipped, 40547525902:skipped, 40547519540:success |
| JARVIS-VOICE #25 | `d10671119fa9a52bc130c28b21ca193edd99d604` | `697110fa5a8dc87c4ed2a7e8df81a2e644a9559b` / `366780b28dd5e5690682d7c638a9e8eb3e6df40f` | 40547583230:success, 40547583238:success, 40547542779:success, 40547542815:cancelled |
| JAVIS-Local-v2 #21 | `a3113797a3c481bc516c5ef1fd4d7a74b919de40` | `cd2adea393287ea94eb3145e8463209f6fa37e9d` / `3d920058cccb9f02ca2af8e7d1bc7acbaedef631` | 40565029341:success, 40565016885:success |
| JARVIS-INTERFACE #10 | `4bc1993d4b6525b248f2b12e95a18a279a3d9fdc` | `82675ade011e69eb3bccd99efbf46d0697a3276b` / `4b87f64cbb1709992c9ee2b36aee47faa304b6ed` | 40578705243:success, 40565042203:success, 40565039146:success |
| JARVIS-VOLUTION- #5 | `2e10d6f5c4d41458d0e55cd6724cd93973db450e` | `4af477877c3ceb32e5805948ca42798970512d44` / `cab1d33b881f78e24930a2f03fdd7f377b17f860` | 40565363719:success |

UNIFIED#10 : cinq workflows distincts SUCCESS (six runs avec la relance push U00). LLM : trois workflows skipped, à préserver comme tels. VOICE : un ancien push cancelled et trois success, pas un verdict entièrement vert sans précision. SERVICES a un parent direct distinct du SHA base de PR, conservé dans la preuve ; aucune réécriture d'histoire.

## Gates et suite

FTS5/SAF Android NEXUS, identité/signature CORE↔UI, JNI et unload LLM/VOICE, sandbox EVOLUTION : **BLOCKED ou NOT_RUN** jusqu'aux preuves propriétaires exactes et essais matériels. Des tests hôte verts n'ouvrent aucun gate. Campagnes physiques : NOT_RUN pour ce lot.

Décisions utilisateur encore ouvertes : autorité/génération, instant de commit/ordre des journaux, ACK perdu/révocation/readback (dossier ADR-002). Choix d'un backend natif NEXUS et toute migration nécessitent aussi une décision distincte. Aucun de ces choix n'est adopté dans cette PR.

Rollback UNIFIED : abandonner la branche ou revert des seuls fichiers additifs lot3 ; aucune donnée ni migration à restaurer. Les rapports propriétaires et références publiées complètent ce document avant clôture du lot.
