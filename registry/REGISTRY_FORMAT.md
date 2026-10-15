# Format du registre central — version 1

Registre de suivi et d'observations, sans commande d'exécution des applications.
Les deux fichiers `modules.json` et `missions.json` sont des JSON UTF-8 avec
`schema_version: 1` et un identifiant `generation` commun. Un lecteur doit valider
les deux ensemble ; des générations différentes signalent une copie interrompue.
Aucune donnée manquante n'est reconstituée à partir d'un nom de branche.

## modules.json

Racine : `schema_version`, `generation`, liste `modules` contenant **exactement les
neuf dépôts demandés**, sans doublon, normalisation ni suppression du tiret final.
Chaque module contient :

| Champ | Type / définition |
|---|---|
| repository | Nom GitHub exact `owner/repository`, dans la liste autorisée du script |
| role | Description manuelle ; préciser « à confirmer » si seul le nom est connu |
| reference_branch | Branche suivie explicitement ; peut différer de la branche par défaut GitHub |
| last_verified_commit | Objet historique ou null : sha complet, branch, verified_at UTC, source, scope, evidence_id |
| state | État de l'observation de branche courante, pas état de santé du module |
| checked_at | Date UTC de la dernière tentative, même infructueuse |
| verified_at | Date de la dernière vérification de SHA réussie ; inchangée après échec |
| observation | Dernier relevé automatique, détaillé ci-dessous ; null si jamais tenté |
| manual | Informations humaines, jamais écrasées par une actualisation |

Une référence de commit peut rester connue alors que `state` vaut unknown ou
failure. Elle est alors historique, avec sa date/source/branche conservées : elle
ne prouve pas que la branche actuelle existe encore. Un rôle dans `role` est une
description de suivi, pas une capacité certifiée par les APIs GitHub.

## missions.json

Racine identique avec liste `missions`. Chaque mission a :

- `id` unique et stable, caractères lettres/chiffres/point/tiret/underscore ;
- `repository` exact, `branch` suivie explicitement ;
- `last_verified_commit`, `state`, `checked_at`, `verified_at`, `observation` et
  `manual`, avec le même sens que pour les modules.

Le SHA automatique décrit la tête de branche observée. Il n'est pas nécessairement
le commit de la livraison historique ou du test évoqué dans une note manuelle.
Ajouter les références de livraison dans `manual.local_evidence` ou une note de
preuve, en indiquant leur portée ; ne pas substituer un ancien SHA testé à la
nouvelle tête de branche. Le script ne découvre pas ni ne clôture les missions.
Les quinze entrées initiales ne prétendent pas épuiser l'historique des neuf dépôts.
Les campagnes VOICE005D/E/F/G partagent une entrée de branche, sans amalgamer
leurs résultats historiques détaillés dans AUDIT.md.

## Champs manuels

`manual` exige `phase`, `blockers` (liste de textes), `decisions` (liste de textes)
et `next_action` (texte). Les autres champs sont permis et conservés intégralement,
y compris les objets imbriqués. Exemples : `role_basis`, `evidence_note`,
`local_branch`, `local_base_commit`, `local_evidence` et `validation_note`.

Phases autorisées : `proposed`, `in_progress`, `completed`, `blocked`, `unknown`.
Elles résultent d'une décision humaine, pas d'une déduction de CI verte. Un module
peut être inconnu, tandis que sa branche a été correctement lue. Une mission
locale terminée peut avoir une branche distante absente. Ce n'est pas une
contradiction : les champs décrivent des faits et des portées différents.

## États d'observation autorisés

| État | Sens |
|---|---|
| success | Observation demandée réussie : dépôt/branche lu, liste PR complète, ou Actions observées réussies selon leur portée |
| failure | Échec connu de l'opération ou conclusion CI négative observée ; conserver le motif précis |
| pending | Actions encore queued/in_progress/waiting/requested/pending |
| unknown | Information insuffisante, API indisponible, aucun run pour ce SHA, résultat neutre/ignoré ou réponse inutilisable |
| not_checked | Opération non tentée : par exemple PR/CI en mode Git ou CI quand le SHA n'est pas connu |

`success` ne signifie **jamais** « application validée », « clonage validé »,
« mission terminée », « tests sur téléphone réussis » ou « tous les checks requis
par GitHub sont verts ». Un résultat de CI n'est pas un décompte de tests.

## Objet observation

Champs communs : `source` (`api`, `git`, `demo`), `checked_at` UTC et `evidence_id`
liant la génération à `evidence/<id>/`. Sous-objets obligatoires, chacun avec
`status` et `reason` :

- `repository` : opération de lecture du dépôt. Métadonnées minimales, branche
  par défaut et éventuel code HTTP. Un 404 signifie inaccessible **ou** inexistant,
  sans conclure qu'un dépôt privé n'existe pas.
- `branch` : nom et SHA complets en cas de réussite ; sinon motif précis.
  Git donne `branch_not_advertised_by_git`, API404 donne `branch_not_found` après
  lecture réussie du dépôt. Les deux ne sont pas fusionnés artificiellement.
- `pull_requests` : `items` dédupliqués par numéro, état open/closed, draft,
  merged_at, head_sha, base_branch et URL GitHub filtrée. Recherche `state=all`
  par branche de tête **du même dépôt** ; pas d'exhaustivité des forks.
- `ci` : GitHub Actions au SHA exact, `runs`, portée
  `exact_sha_actions_only`, `required_workflows_known:false`, `tests_count:null`.

Actions : derniers run_number/run_attempt/id par couple workflow_id/événement.
Un ancien run vert ne masque pas le run rouge plus récent. Une conclusion
failure/cancelled/timed_out/action_required/startup_failure/stale donne failure ;
skipped/neutral ou valeur inconnue donne unknown. Priorité d'agrégation :
failure → pending → unknown → success. Aucune sortie Actions donne unknown,
jamais success. Les runs d'un autre SHA sont exclus. Une nouvelle tentative qui
n'a pas encore produit de résultat ne devient pas une réussite par héritage.

La pagination est parcourue à 100 résultats/page, au plus 10 pages. Limite atteinte,
page inaccessible ou réponse invalide : unknown pour la liste concernée, sans
publier une liste partielle comme exhaustive. Les anciennes observations restent
dans leur snapshot, pas dans un faux résultat courant. Les checks externes,
commit statuses, protections de branche et logs/rapports JUnit ne sont pas
collectés par cette v1 ; la portée Actions est explicitement affichée.

## Sources et traçabilité

- `git` : commande exacte `git ls-remote --symref https://github.com/OWNER/REPO.git
  HEAD refs/heads/*`. Aucun fetch, checkout, changement de remote, push ou PR.
- `api` : requêtes HTTP **GET exclusivement** vers `https://api.github.com`,
  métadonnées dépôt, branche, PR et runs Actions. Redirects refusés ; aucun
  renommage automatique de dépôt. TLS, CA et proxy existants sont conservés.
- `demo` : relecture locale de `demo/github.json`, explicitement synthétique,
  sans accès réseau, Git ou lecture de jeton. Ses SHA/PR/runs ne sont pas réels.
- `local_git` : preuve manuelle initiale dans `evidence/local-baseline.json` ;
  ne représente jamais un commit observé sur GitHub.

Chaque actualisation crée un nouveau `evidence/<generation>/` non écrasable :
`modules.json`, `missions.json`, `SUMMARY.md` et `evidence.json`. Ce dernier contient
les endpoints/méthodes/motifs, observations Git minimales ou empreintes SHA-256 des
réponses API normalisées, heure du relevé et SHA-256 du collecteur. Les snapshots
antérieurs produits avant l'ajout de ces deux derniers champs restent historiques.
Le snapshot contient les données normalisées affichées ; les corps API bruts,
headers d'authentification, logs, descriptions de PR et secrets ne sont pas stockés.
Ce journal est une trace locale auditable par Git, pas une signature GitHub ou une
preuve infalsifiable. Les URLs servent à une vérification indépendante ultérieure.

La preuve `evidence/api-access.json` décrit le test API réellement tenté dans cette
session (réseau indisponible, tunnel proxy403), distinct du registre principal
alimenté par Git. Les snapshots sont des observations datées, pas de l'état live.
VOICE005H a changé de SHA entre deux relevés : les deux snapshots sont conservés,
sans prétendre connaître le contenu ou les tests des nouveaux commits.

## Validation et persistance locale

Le script valide versions, neuf noms exacts, unicité des IDs, branches, états,
champs manuels, SHAs et dates UTC avant et après collecte. Les clés JSON dupliquées,
valeurs non finies et fichiers JSON de plus de 4 Mio sont refusés. Les champs
manuels inconnus sont conservés. L'ajout d'une mission est une édition locale
explicite, suivie de `--validate-only`.

Un verrou `.update.lock` exclut les écritures locales concurrentes ; un fichier
orphelin doit être examiné avant retrait manuel. Le snapshot complet est écrit
et fsync avant remplacement individuel des deux fichiers racine et du résumé.
La racine n'est pas une transaction multi-fichier : une panne peut laisser des
générations mixtes que le validateur refuse. Restaurer alors **les deux JSON et le
résumé du même snapshot complet**, après vérification. Un disque plein avant la
fin du snapshot peut laisser un dossier incomplet : ne jamais le sélectionner.
Pas de nettoyage/suppression automatique des preuves et aucune modification
GitHub, déploiement, push, fusion ou extraction de données applicatives.

Les fichiers publics du registre ne doivent recevoir ni secret ni donnée
personnelle dans les champs manuels. Un jeton peut être lu en RAM via
`--token-env GH_TOKEN` ou `GITHUB_TOKEN`, uniquement après un refus HTTP anonyme
401/403/429 ; jamais sur simple échec de tunnel. Aucun jeton n'est demandé ni
ajouté aux fichiers par le script. Son absence n'empêche ni la démo ni le mode Git.
