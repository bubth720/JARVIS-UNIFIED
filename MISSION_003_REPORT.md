# Rapport final — Mission 003 : registre central JARVIS

Date : 15 octobre 2026. Branche créée : **mission-003-central-registry**.
Base locale : `55680bcfe1f793618c79eb1bdc7b2b8c847b369e` (Mission002).
Mission001 préservée : `004b89d1f86135962e452fb644b489f69fc177d1`.

Commit final : le commit de livraison contenant ce rapport, à résoudre sans
ambiguïté avec `git log -1 --format=%H -- MISSION_003_REPORT.md`. Son SHA exact est
également fourni dans le message final de livraison ; il n'est pas remplacé par
un SHA GitHub fictif. La génération du registre ci-dessous n'est pas un commit Git.

## Sécurité préalable et préservation

L'arbre était propre sur mission-002-backup. Les branches locales, l'historique,
les cinq documents Mission001, les documents/prototype/tests/ressources Mission002
et le rapport de validation ont été inspectés. audit/mission-001 est ancêtre de
mission-002-backup ; ses quatre documents d'audit/architecture/plans sont inchangés.
GitHub n'annonce que main pour UNIFIED, au commit initial ; les deux missions
validées sont donc dans les branches locales, qu'il fallait préserver.
La base choisie est la branche locale validée la plus récente, sans ambiguïté.

Aucun fichier suivi de la base Mission002 n'a été modifié ; toutes les additions
se limitent à registry/ et au présent rapport. Aucune écriture sur les autres
projets, aucun push, aucune PR créée, aucun merge/main réécrit, aucun déploiement,
aucune suppression et aucun secret enregistré. Les commandes réseau exécutées
sont des lectures Git et des GET API. La branche centrale reste locale.

## Livrables

- [registry/modules.json](registry/modules.json) : les neuf noms exacts, rôles
  documentés ou à confirmer, branches, derniers SHA vérifiés, dates et observations.
- [registry/missions.json](registry/missions.json) : quinze entrées initiales avec
  suivi de branche, CI/PR séparées, blocages, décisions et prochaines actions manuels.
- [registry/REGISTRY_FORMAT.md](registry/REGISTRY_FORMAT.md) : champs, états,
  règles de validation, limites et traçabilité.
- [registry/README.md](registry/README.md) : consultation, édition et actualisation.
- [registry/scripts/update_registry.py](registry/scripts/update_registry.py) :
  Python standard, collecte API GET ou Git ls-remote, démo locale sans connexion.
- [registry/SUMMARY.md](registry/SUMMARY.md) : résumé Markdown régénéré.
- [registry/tests/test_registry.py](registry/tests/test_registry.py) : tests hors ligne.
- [registry/demo/github.json](registry/demo/github.json) : réponses explicitement
  synthétiques, jamais prises pour des résultats réels.
- [registry/evidence](registry/evidence) : snapshots complets datés, preuve de base
  locale et diagnostic API. Aucun fichier préexistant des missions001/002 modifié.

Les noms INTERFACE et INTERFACE- ne sont pas réunis ni corrigés. Les rôles non
audités restent à préciser ; les missions ne sont jamais déclarées finies à partir
d'un simple nom ou d'une CI verte. Les statuts manuels restent indépendants des
observations distantes. En particulier, les missions UNIFIED001/002 sont terminées
localement malgré l'absence de leurs branches sur GitHub.

## État réel des neuf dépôts

Dernière collecte Git : **2026-10-15T12:29:31+00:00**, génération **39fa39d3478d4bf7ac97317909c25543**.
Chaque SHA ci-dessous provient de git ls-remote, pas d'un jeu de démonstration.

| Dépôt | Branche de référence choisie | SHA observé | Branche / CI |
|---|---|---|---|
| bubth720/JAVIS-Local-v2 | `main` | `226e2e8cc3eebd479805b89d035eb5c1cbcad540` | success / not_checked |
| bubth720/JARVIS-LLM | `mission-003b-resources` | `1756e29557287550b5cfdffdd911cada2a302db6` | success / not_checked |
| bubth720/JARVIS-VOICE | `feat/voice-identity-005h` | `17c5697ba3bdb21bcbcbf4ce041cd4fc41615f55` | success / not_checked |
| bubth720/JARVIS-INTERFACE | `development/mission-002` | `d1c0931c4507e9af8f1aa60951947c23f4394b56` | success / not_checked |
| bubth720/JARVIS-INTERFACE- | `main` | `a857f5019354ea1c912e6f66bebdcc053c0cb700` | success / not_checked |
| bubth720/JARVIS-NEXUS | `main` | `b27df0b84d8f0082d17ca6278549298aaaf97926` | success / not_checked |
| bubth720/JARVIS-VOLUTION- | `main` | `a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0` | success / not_checked |
| bubth720/JARVIS-SERVICES | `main` | `c9f94ad2fa219a5e09cda92fb451aca606ee1646` | success / not_checked |
| bubth720/JARVIS-UNIFIED | `main` | `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b` | success / not_checked |

Git a répondu pour les neuf dépôts. Les trois branches UNIFIED des missions
001/002/003 ne sont pas annoncées sur le remote : leur observation distante est
failure/branch_not_advertised_by_git, leur CI not_checked ; les livrables locaux
sont conservés et documentés séparément. Le module UNIFIED suit main pour l'état
GitHub et précise sa base de travail locale dans manual.

VOICE005H est une branche nouvellement observée, non auditée fonctionnellement.
Elle a changé de SHA pendant les relevés ; les captures successives sont conservées.
Cela illustre le besoin de dates et de SHAs exacts, sans prouver une amélioration
fonctionnelle ni un clonage validé. Aucun acteur de ces changements n'est inféré.
Les branches de référence sont des choix de suivi, pas une preuve qu'elles sont
les plus récentes ou les meilleures pour tous les usages.

## Accès API et informations absentes

La politique d'environnement est restreinte et ne liste pas api.github.com.
L'essai réel a reçu `Tunnel connection failed: 403 Forbidden`. Le collecteur API
sans jeton a ensuite enregistré network_unavailable sur les neuf dépôts, dans
[api-access.json](registry/evidence/api-access.json). Le mode API réel ne permet
donc pas de confirmer les numéros/états des PR ni les résultats Actions ici.
Un nom de variable GH_TOKEN était présent ; aucune valeur n'a été imprimée ni
utilisée pour tenter de contourner ce refus de réseau. Aucun nouveau jeton demandé.

Le registre principal conserve PR/CI **not_checked** (mode Git). Le relevé API
séparé donne unknown ou non tenté pour les opérations en aval. Les rapports de
CI historiques Mission001/002 ne sont pas recyclés comme CI GitHub courante.
Pour activer une prochaine collecte API, autoriser api.github.com dans les
paramètres réseau, puis tester l'accès public avant tout besoin de jeton en lecture.
La configuration réseau n'a pas été modifiée pendant cette mission.

## Tests exécutés et résultats

- `python3 -m unittest discover -s registry/tests -v` : **23 tests réussis**,
  zéro échec/erreur/ignoré, 0,219 s dans la dernière campagne, code retour0.
- `python3 -m unittest discover -s backup_prototype/tests -v` : **30 tests
  Mission002 réussis**, zéro échec/erreur/ignoré, code retour0. Le prototype est intact.
- `--validate-only` : neuf modules, quinze missions, registre valide.
- Démo via CLI avec sortie distincte : exécutée sans connexion, neuf modules
  source demo, cas inconnus/absents/en attente fidèlement représentés ; retour2
  attendu pour les résultats partiels, sans écraser le registre réel.
- Collecte Git réelle : neuf dépôts accessibles ; retour2 attendu pour les trois
  branches UNIFIED locales non annoncées sur le remote.
- Collecte API réelle : observations d'indisponibilité enregistrées, retour2 ;
  ce n'est pas une validation du fonctionnement API connecté/authentifié.
- Validation des liens Markdown/JSON, des générations et des preuves, diff/check
  et comparaison des fichiers suivis à la base : effectuées avant livraison.

Les sept obligations sont couvertes : registre valide, dépôt inaccessible,
branche absente, mission sans résultats CI, préservation des blocages, aucune
mutation distante et mises à jour répétées sans doublons. S'y ajoutent redirections
refusées, jeton uniquement après nécessité, absence de secret dans les traces,
pagination bornée, filtrage SHA/branche/identité PR, tentatives CI les plus récentes,
statuts pending/failure/unknown, doublons PR, dates historiques conservées,
générations mixtes refusées et protection du registre réel en démo.

## Limites connues

API réelle bloquée ; transport/API authentifiés testés avec doubles seulement.
CI limitée aux Actions observées au SHA exact, pas aux protections de branche,
checks externes ou décomptes JUnit. Aucun test d'application ni validation matérielle
n'est inféré. PR limitées aux branches de tête du même dépôt, pagination plafonnée
à 1000 résultats par endpoint. Le jeu initial de missions est manuel et non exhaustif.

Les snapshots sont locaux et audités par Git, pas signés par GitHub. Les copies
racine ne sont pas une transaction multi-fichier ; une interruption est détectée
par generation et récupérable depuis un snapshot complet. Verrou local contre
les publications concurrentes, mais pas contre une édition externe concurrente.
Aucun nettoyage automatique des preuves. Les champs humains sont du texte à
maintenir sans secrets/données personnelles. Le script ne modifie que ses sorties
locales explicitement choisies ; il ne peut pas rendre visibles sur GitHub des
commits qui n'y ont pas été publiés.

## Utilisation et prochaine mission recommandée

Lire registry/SUMMARY.md, valider les JSON puis actualiser explicitement :

```sh
python3 registry/scripts/update_registry.py --validate-only
python3 registry/scripts/update_registry.py --mode demo --output-dir /tmp/jarvis-registry-demo
python3 registry/scripts/update_registry.py --mode git
# Lorsque le domaine API sera autorisé :
python3 registry/scripts/update_registry.py --mode api --output-dir /tmp/jarvis-registry-api
```

Les codes0/1/2 sont expliqués dans registry/README.md. Un jeton éventuel vient
d'une variable sécurisée opt-in ; sa valeur ne doit jamais être enregistrée.

Prochaine mission recommandée : **qualifier la collecte API en lecture seule et
compléter les preuves PR/CI ainsi que les rôles des modules encore inconnus**,
après ouverture réseau appropriée. Cette recommandation n'est pas exécutée.
Aucune mission de fusion fonctionnelle ou modification d'application commencée.
