# UNI-PF-01 — assessment pré-fusion, lot 1

Date : 2026-10-27 UTC. **Verdict global : BLOCKED / REVIEW_ONLY. Aucune fusion autorisée.**
Base de travail UNIFIED : `6b0ae1a1ca1a257446931a69bdff15a4f77ac019`, parent `ade69697f55d425f871e4e3b90c7155bf7657d7a`. Branche `codex/prefusion-20261026-lot1`, PR brouillon vers `mission/prefusion-gates-20261026`. Le SHA publié est le HEAD de la PR contenant ce rapport.

## U0 — références réellement vérifiées

Les huit missions ont été lues **sur leur branche mission**, les dépôts clonés sans modification des branches propriétaires, les HEAD/parents relevés par `git rev-parse` et revérifiés via GitHub. Toutes les missions sont accessibles ; aucun dépôt de cette liste déclaré absent à partir d'un 404 de fichier. Branches de développement distinctes créées depuis ces HEAD. Aucun worktree créé. AGENTS UNIFIED/CORE lus ; les autres checkouts n'avaient pas de AGENTS.md trouvé.

Toutes les références de cette table désignent `mission/prefusion-gates-20261026`, pas la branche par défaut :

| Dépôt bubth720/ | SHA40 mission | Parent code/documentaire |
|---|---|---|
| JARVIS-INTERFACE | `82675ade011e69eb3bccd99efbf46d0697a3276b` | `3c6921e2e40dd8e7c0756e07e854ce0bc1d9c5ff` |
| JARVIS-LLM | `12fc58a81ceee70eedbba2d0b187b1294bae6283` | `f147236820e0633b0c88f6f1725e828f71167b27` |
| JARVIS-NEXUS | `bdb51f77a5fe105dbff43d43032882fe1474a4ee` | `8c778be1b302d10c8dcbf8444f6e6e051477c825` |
| JARVIS-SERVICES | `365da117ccb29b59ed990711b2c3f72472ce2d9d` | `7c7fc95ad19e10de877b14fb5d3fe7f53b27d3e4` |
| JARVIS-UNIFIED | `6b0ae1a1ca1a257446931a69bdff15a4f77ac019` | `ade69697f55d425f871e4e3b90c7155bf7657d7a` |
| JARVIS-VOICE | `697110fa5a8dc87c4ed2a7e8df81a2e644a9559b` | `95f873226a6b80e2517266a943dfbead94432b86` |
| JARVIS-VOLUTION- | `4af477877c3ceb32e5805948ca42798970512d44` | `c0180181804338d21f3bf9d4b537b709595902f7` |
| JAVIS-Local-v2 | `cd2adea393287ea94eb3145e8463209f6fa37e9d` | `f6a3b2d0c280c69ef1570544fdbf5bcf5818810c` |

Le manifeste historique `workspace/modular-workspace.proposed.json` est préservé comme photo datée ; ce rapport ne le réécrit pas. Son SERVICES f8976c… ne représente pas SERV-09/mission365da… ; son UNIFIED25d714… n'est pas le nouveau HEAD. Le manifeste n'est pas un APK ni une qualification ABI. Les nouveaux relevés sont dans [EVIDENCE.json](EVIDENCE.json).

Sources relues : README/AGENTS/ADR-001 et ADR-002 proposés, workspace README/manifest/checker, uni08_candidate, rapports et sources propriétaires citées dans [COMPATIBILITY.md](COMPATIBILITY.md) et [REVIEW-AND-PILOT.md](REVIEW-AND-PILOT.md). Les PR ouvertes, notamment UNIFIED6/7/8/9, NEXUS5/6/7, SERVICES4/5/6, LLM5, VOICE23/24, sont conservées. Aucun travail antérieur n'est remplacé par ce lot.

## Priorités A — lots livrés

| Module / mission | Commit publié, PR brouillon | Étape et état |
|---|---|---|
| NEXUS / NEX-PF-01 | `201f0d2b03209de104157595a557143fe87eb94e`, [PR8](https://github.com/bubth720/JARVIS-NEXUS/pull/8) | Garde CI mission corrigé, sources gelées ; [CI40547468137](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/40547468137) SUCCESS au SHA exact, 2 jobs JVM/Android-hôte. Aucune instrumentation/appareil inférée |
| SERVICES / SERV-PF-01 | `ea541d20b08f7ad0949354829a977f6752cbffa3`, [PR7](https://github.com/bubth720/JARVIS-SERVICES/pull/7) | Rapport/cataloque17vs2, Java11 revérifié, runtime intact ; 15/15 par API24/25/26/35 sur la **base mission365da…** (run40412745341). Nouvelle CI documentaire à contrôler séparément |
| LLM / LLM-PF-01 | `6ae8a4f5c2490f6c9814e08957909a8e3a807180`, [PR6](https://github.com/bubth720/JARVIS-LLM/pull/6) | Routage vers campagne complète et gel JNI/runtime ; [CI40547525669](https://github.com/bubth720/JARVIS-LLM/actions/runs/40547525669) en cours lors de ce relevé, pas de succès anticipé |
| VOICE / VOICE-PF-01 | `d10671119fa9a52bc130c28b21ca193edd99d604`, [PR25](https://github.com/bubth720/JARVIS-VOICE/pull/25) | Campagne complète désormais déclenchée sur mission ; [CI40547583230](https://github.com/bubth720/JARVIS-VOICE/actions/runs/40547583230), JVM SUCCESS, audio26/35 en cours/attente au relevé |
| UNIFIED / UNI-PF-01 | HEAD de cette PR | U0/U1/U2/U3/U4 documentaire + bilan U5 logiciel ; aucune qualification globale |

Chaque lot propriétaire contient `docs/prefusion/ASSESSMENT.md` : commandes, nombres réellement observés, limites, dépendances, rollback et prochaine étape. Les gardes historiques NEX-07/FUSION restent intacts et exécutés au **SHA historique propre** dans un clone local temporaire ; les nouveaux gardes contrôlent séparément le gel du SHA mission. Aucun succès d'ancêtre n'est attribué au HEAD. Les arbres GitHub des trois corrections sont égaux aux arbres locaux testés ; auteurs/dates des commits de publication peuvent différer, ces correspondances sont précisées dans les PR.

## Priorités B — audit passif, travaux non achevés

- **CORE-PF-01** : SessionCoordinator, AppGraph, TaskCoordinator, DocumentToolReadiness, AGENTS/PROJECT_KNOWLEDGE et contrat C0 relus. Le port reste enabled=false/canExecute=false ; CONNECTED donne UNKNOWN, aucun nouveau registre/adaptateur. CI de PR au SHA mission : aucune renvoyée par le connecteur (première page filtrée PR), donc UNKNOWN, pas affirmation qu'aucun run n'existe. Aucun nouveau test/build CORE ni PR propriétaire dans ce lot.
- **UI-PF-01** : revue transport et code CoreConversationClientAdapter/AvatarExpressionStateMachine relus. Le transport réel est absent, origine NONE ; ACK/Stop5s/UNKNOWN et références inertes sont conservés. CI Android source40412782652 SUCCESS, couverture instrumentée/physique non déduite. Aucun code UI/citation/personnalité changé ni PR propriétaire dans ce lot.
- **EVOL-PF-01** : README/REPORT-EVOL-03 relus, schéma/propositions sans exécution. CI JVM source40412785717 SUCCESS ; sandbox OS historiquement bloquée, non retestée. Aucun patch, essai non isolé, données CORE ou réseau accordé. Aucun nouveau build/PR propriétaire dans ce lot.

Le nouvel environnement d'exécution n'est plus utilisable (`No usable execution environment is available`) ; la lecture/publication GitHub fonctionne. Pas de travail Android local ou sandbox possible après cette interruption. Les travaux B purement OFF restent autorisés en principe mais **NOT_RUN**, à reprendre dans un environnement disponible ; les raccordements attendent les gates.

## U5 — tests réellement exécutés UNIFIED

Linux x86_64, Python3.12.14, source mission6b0ae1… avant ajouts documentaires :

| Commande | Résultat |
|---|---|
| `python3 workspace/check_plan.py workspace/modular-workspace.proposed.json` | PASS, REVIEW_ONLY, 8 modules, 0 liaison active |
| `python3 scripts/validate_unified.py` | PASS : 5 contrats, 5 exemples valides, 5 invalides rejetés, 9 dépôts historiques |
| `python3 -m tooling.integration.ci --output <dossier-preuves-local>` | 167/167 cas comptés, 0 échec/erreur/saut ; 12 entrées de contrôle réussies |
| `python3 -m unittest discover -s workspace/tests -v` | 20/20 PASS |
| `python3 -m unittest discover -s tooling/integration/uni08_tests -v` | 23/23 PASS |
| `python3 -m unittest discover -s tooling/integration/uni08_u01_tests -v` | 23/23 PASS |
| `python3 -m unittest discover -s tests -v` | 41/41 PASS, réexécution déjà comprise dans le runner |
| `python3 -m unittest discover -s registry/tests -v` | 23/23 PASS, réexécution déjà comprise |
| `python3 -m unittest discover -s backup_prototype/tests -v` | 30/30 PASS, dépendance cryptography existante ; réexécution déjà comprise |

233 cas comptés par les quatre runners non redondants (167+20+23+23), aucune addition des 94 réexécutions. Les nouveaux fichiers UNIFIED sont documentaires : aucune modification des validateurs/contrats/tests et aucun test artificiel ajouté pour cette documentation. **Nouvelle CI au HEAD exact à exiger**, les résultats locaux du SHA mission ne sont pas renommés comme une CI du nouveau commit.

Autres tests locaux : NEXUS garde +6 négatifs, SQL10, ZIM18PASS/1SKIP archive absente, Node1 runner ; LLM garde +6 négatifs, preuves11, contrôle APK et revue native sèche ; VOICE garde +6 négatifs. Tests Python de préservation =18/18, pas tests Android. Tentative desktop SERVICES bloquée au téléchargement Gradle ; aucun test local compté. Les totaux historiques JVM/Robolectric/appareils figurent dans leurs sources datées, pas dans ces nouveaux totaux.

## Gates maintenus et décisions réservées

| Gate | État | Justification / action suivante |
|---|---|---|
| Source lock / plans | PASS logiciel / REVIEW_ONLY | Références disponibles, validateurs négatifs ; pas une autorisation |
| NEXUS Android FTS5 / SAF persistant | BLOCKED | Plateforme24/25 historiquement sans FTS5 ; backend alternatif à décider avant ajout JNI/migration |
| SERVICES SAF laboratoire | PASS sur SHA365da… uniquement | 4×15 cas observés ; stabilité et nouvelles CI séparées |
| Autorité d'écriture CORE/SERVICES | BLOCKED | ADR-002 non approuvée, génération/commit durable/consentement à arbitrer |
| LLM natif / tokenizer / unload | BLOCKED | Patch sensible non appliqué, modèles/Android non qualifiés par tests JVM |
| VOICE émotions / arbitrage natif | BLOCKED | Autres émotions UNSUPPORTED, fin audio non preuve unload |
| Runtime E2E Android / physique | NOT_RUN / BLOCKED | Aucun pilote opérationnel ni APK unifié |
| Architecture effective / imports | REVIEW_REQUIRED | Comparaison fédération/monorepo seulement ; aucun import autorisé |

Les décisions concrètes non approuvées sont détaillées dans REVIEW-AND-PILOT. Aucun changement majeur d'architecture, SQLite/JNI, minSdk, permission réseau/runtime, signature, profil, migration persistante, installation personnelle, déploiement, merge/main ou auto-merge effectué. Aucun schéma gelé ni preuve FUSION-02 réécrit.

Rollback UNIFIED : revert des seuls fichiers `docs/prefusion/` de cette branche. Pour chaque propriétaire : revert du lot isolé, sans restauration de données nécessaire. Les sources/historiques/applications autonomes restent conservés.

Prochaine action : lire les CI exactes des PR publiées, traiter leurs échecs indépendamment ; reprendre les phases OFF de priorité B quand l'environnement revient. Ne pas fermer les huit missions tant que les vrais critères Android/natifs/humains ne sont pas satisfaits.
