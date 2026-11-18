# Qualification N01-A3

## Sources et changements

NEXUS : base `2dd4447acb592e9e63123c0377b6310d4dae2bf1`, tête
`5f10193440972ba25b30645d2811537418eface5`. Le garde construit les octets attendus
de NEX-07 depuis la version Git figée : deux substitutions de checkout, deux
déclarations de contexte REUSE et deux branches de garde/tests. Toute autre
édition de ce workflow est refusée, même un commentaire. Les cinq nouveaux
chemins sont énumérés, sans règle autorisant tout un préfixe.

| Fichier NEXUS | Rôle |
|---|---|
| `.github/workflows/nex-07.yml` | Seule exception historique approuvée ; routage PR dans les deux jobs |
| `.github/workflows/n01-a3-routing.yml` | Nouvelle CI sur la branche A3, régressions REUSE et artefacts |
| `reuse-r1plus/n01-a3/check_routing_scope.py` | Contrôle des octets/modes et du contexte PR |
| `reuse-r1plus/n01-a3/tests/test_routing_scope.py` | 40 tests positifs/négatifs, mutations en clones temporaires |
| `reuse-r1plus/n01-a3/AUTHORIZATION.json` | Trace de l'accord et des limites ; aucune autorité runtime |
| `reuse-r1plus/n01-a3/README.md` | Périmètre, commandes et limites des anciens gardes |

## Vérifications locales

Linux x86_64, Python 3.12. Les traces complètes et commandes sont conservées dans
le dossier de livraison daté ; seuls les résumés sont versionnés ici.

| Vérification | Résultat / portée |
|---|---|
| Nouveau garde NEXUS | PASS ; 337 fichiers de base, 336 inchangés et une exception exacte |
| `unittest discover -s reuse-r1plus/n01-a3/tests -v` | 40 tests réussis ; mutations de contrat, garde, permissions, symlinks, fichiers et contexte PR |
| `unittest discover -s tests/final -v` | 10 tests SQLite historiques réussis à la tête A3 |
| `unittest discover -s tests/prefusion -v` | 6 tests de préservation sur fixtures réussis ; ce n'est pas le garde PRE-FUSION à HEAD |
| Replay NEXUS A2 `2dd4447a` | 11 tests et garde REUSE réussis ; gardes M53/NEX-07 rejoués à leurs propres SHA |
| Ancien garde REUSE à la tête A3 | Refus attendu sur `.github/workflows/nex-07.yml`, exit 1 |
| Validateur UNIFIED | PASS ; 5 contrats, 5 exemples valides, 5 invalides rejetés |
| Tests UNIFIED | 171 réussis : 41 généraux, 23 registry, 30 backup, 23 U01, 54 A2 |
| Sources des cinq dépôts | Empreintes des vrais contrats relues et identiques ; pas d'invocation des producteurs |
| Fichiers V1 INTERFACE | 430 fichiers et modes identiques à `9599d991`, lecture seule |
| Socle UNIFIED A2 | 519 fichiers et modes inchangés ; ajouts documentaires A3 uniquement |

Total : 227 tests Python à la tête des branches concernées et 11 replays
historiques, sans additionner les répétitions CI. Les régressions A2 de revue
réseau utilisent des fixtures et interdisent les sockets : elles ne valident
pas un transport RESEARCH réel.

## CI GitHub

Deux exécutions distinctes sont observées au même SHA NEXUS :

- [44273871327 — N01-A3 / REUSE](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44273871327), événement push.
- [44273924562 — NEX-07](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44273924562), événement pull_request #16.

Les deux runs terminent en **SUCCESS** au commit `5f101934`. La CI A3 produit
108 tests JUnit REUSE, zéro échec, erreur ou saut, puis passe les 10 tests Python
SQLite. NEX-07 passe les deux contrôles de contexte au SHA réel de la PR, les
tests JVM et les distributions CLI/adaptateur SERVICES, 19 tests ZIM et 7 tests
JavaScript de graphe. Android-host passe les tests hôtes, assemble l'AAR et l'APK
de test et exécute le lint. La compilation sur stubs API24 couvre 1 source Java
et 23 Kotlin propres ; le contrôle de frontière observe 131 classes CORE et 23
classes adaptateur, minSdk 24, sans permission ni charge native dans l'AAR.

L'[artefact JUnit et provenance](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44273871327/artifacts/14414026693)
est annoncé disponible jusqu'au 16 février 2027. Ses métadonnées et les journaux
de jobs sont lus. Le téléchargement local du ZIP est bloqué par le proxy sur
l'hôte de fichier du connecteur puis sur la redirection blob GitHub ; aucune
vérification locale de ses empreintes internes n'est revendiquée. Les 108 cas
proviennent du résumé JUnit calculé et lié au SHA dans la CI elle-même.

Anomalies non bloquantes : avertissement de licence/absence de Platform-Tools
dans le job Android-host, et action checkout historique Node20 exécutée sous
Node24 par GitHub. Les commandes hôtes prévues réussissent ; aucun ADB,
émulateur ou appareil n'est utilisé. Les versions historiques ne sont pas
modifiées au-delà du routage autorisé.

Le résultat final, les jobs et les métadonnées des artefacts sont consignés dans
`evidence/ci-summary.json`. Une réussite Android-host couvre compilation, tests
hôtes, lint et frontière de l'AAR, sans instrumentation sur émulateur API29/35 ni
installation matérielle. Aucun nouveau résultat de performance Android, LLM,
GPU ou énergie n'est annoncé.

Le [refus historique 42523863724](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42523863724)
de la PR #14 est conservé ; le correctif ne réécrit pas cette preuve. Les succès
A2 antérieurs ne sont pas attribués au nouveau commit.
