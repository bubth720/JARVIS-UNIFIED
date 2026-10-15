# Registre central JARVIS

Commencer par [SUMMARY.md](SUMMARY.md) pour lire le suivi des **neuf dépôts**.
Les données structurées sont dans [modules.json](modules.json) et
[missions.json](missions.json). Les définitions des états sont dans
[REGISTRY_FORMAT.md](REGISTRY_FORMAT.md).

Le registre initial contient des branches/SHA réellement lus par Git, quinze
entrées de suivi et des notes locales. Les PR et la CI distantes restent
`not_checked` : l'API GitHub est bloquée dans cet environnement. Le fonctionnement
de l'API a été testé avec des réponses synthétiques, pas validé en accès réel.
Les missions001/002/003 UNIFIED sont locales et ne sont pas publiées sur GitHub.
Les dépôts `JARVIS-INTERFACE` et `JARVIS-INTERFACE-` sont volontairement distincts.

## Consulter sans accès réseau

Depuis la racine de JARVIS-UNIFIED, Python standard 3.10 ou plus, sans paquet externe :

```sh
python3 registry/scripts/update_registry.py --validate-only
python3 -m unittest discover -s registry/tests -v
```

La lecture des JSON/Markdown existants ne contacte pas GitHub. Les preuves datées
sont conservées dans [evidence](evidence). Une branche accessible ne prouve pas
que l'application marche ; une CI Actions verte ne prouve pas une qualification
matérielle ou le clonage vocal.

## Démonstration sans connexion

```sh
python3 registry/scripts/update_registry.py --mode demo --output-dir /tmp/jarvis-registry-demo
```

Le résumé est affiché et enregistré dans `/tmp/jarvis-registry-demo/SUMMARY.md`.
Le jeu synthétique inclut un dépôt inaccessible, une branche absente, un module
sans CI et des Actions en attente. Le code retour **2 est donc attendu** : données
partielles correctement enregistrées. Le registre réel n'est pas écrasé ; le mode
demo impose un dossier de sortie distinct, n'utilise aucun secret et ne fait
aucune connexion réseau. Réexécuter ne crée pas de doublons de dépôts/missions,
mais ajoute une nouvelle preuve datée, ce qui est intentionnel.

## Actualiser depuis GitHub en lecture seule

```sh
# API anonyme, si api.github.com est accessible ; destinations locales seulement.
python3 registry/scripts/update_registry.py --mode api

# Git disponible sans API : branches/SHA uniquement, PR et CI restent not_checked.
python3 registry/scripts/update_registry.py --mode git
```

Codes retour : **0** collecte réussie selon le mode, **2** observations partielles
sauvegardées (notamment branche absente/CI inconnue), **1** échec de validation ou
d'écriture locale. En mode Git, 0 ne promet pas une collecte PR/CI : elles ne sont
jamais tentées. Dans cet environnement, Git retourne 2 pour les trois branches
UNIFIED non publiées. Ce n'est ni un effacement de travaux locaux ni un échec des
tests applicatifs.

Pour examiner les résultats sans remplacer le registre courant :

```sh
python3 registry/scripts/update_registry.py --mode api --output-dir /tmp/jarvis-registry-api
```

L'environnement actuel autorise les accès GitHub Git mais pas `api.github.com`.
Pour une future collecte API réelle, permettre ce domaine dans les paramètres
réseau autorisés de l'environnement ; aucune règle réseau n'a été élargie ici.
Si l'API exige ensuite une authentification, utiliser un accès GitHub existant en
lecture minimale via une variable sécurisée, puis ajouter `--token-env GH_TOKEN`
ou `--token-env GITHUB_TOKEN`. La valeur n'est jamais un argument CLI et ne doit
pas être collée en chat, dans Git, dans les JSON ou dans une commande versionnée.
Le script tente l'accès anonyme d'abord, ne lit la variable qu'après un refus HTTP
401/403/429 et ne transmet jamais le jeton après redirection.
Une variable présente ne prouve pas un droit API ; un proxy403 ne se résout pas en
inventant un nouveau jeton. Le fonctionnement API authentifié réel reste à vérifier.

## Éditer les informations humaines

Modifier uniquement `role`/`reference_branch` si nécessaire dans modules.json,
ajouter des missions avec ID unique, et compléter `manual` : phase, blockers,
decisions, next_action et preuves datées avec portée. Les champs supplémentaires
manuels sont préservés intégralement. Ne jamais utiliser la CI pour remplacer une
décision humaine. Conserver des rôles « à confirmer » si leur contenu n'est pas
audité. Le script ne fusionne pas des dépôts ou ne devine pas une mission manquante.

Valider ensuite les deux JSON ensemble, puis lancer une actualisation pour créer
le nouveau snapshot et régénérer SUMMARY.md. Éviter une édition concurrente pendant
la collecte ; le verrou ne couvre que la publication locale par le script, pas
un éditeur externe. Les valeurs distantes périmées restent identifiables par leur
date/source et par l'état de la dernière tentative.

Ne pas modifier les snapshots déjà conservés. En cas de générations mixtes après
interruption, vérifier un dossier evidence complet et restaurer ses **deux JSON et
SUMMARY.md ensemble**. Aucun automatisme ne supprime les originaux ou ne fusionne
les branches. Le script ne lance jamais de commandes sur les applications.

[Rapport de Mission003](../MISSION_003_REPORT.md) : base de branche, résultats,
limites et prochaine mission proposée.

## Consolidation de l’architecture

Le nouveau [README central](../README.md) et l’ADR proposée clarifient désormais
UNIFIED comme coordination sans runtime. Le relevé détaillé des sources est dans
[repositories.json](repositories.json), les preuves typées dans
[proofs.json](proofs.json), les relations dans [integrations.json](integrations.json).
Les champs `consolidation` de modules.json sont des annotations sourcées distinctes
des anciennes observations datées ; les champs manual sont préservés. Le résumé
historique SUMMARY n’est pas la matrice runtime. Le nouvel audit reproductible
est décrit dans [RUNBOOK](../docs/RUNBOOK.md), sans remplacer le collecteur existant.
