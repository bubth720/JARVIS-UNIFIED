# Runbook — photographie centrale vérifiable

## Lire l’état

Ouvrir README, puis INVENTAIRE, MATRICE_INTEGRATION et PROUVES. Pour une question
« fonctionne avec quoi ? », lire d’abord code de liaison et test d’intégration,
puis qualification appareil. Merge/main est une autre colonne. Un contrat ou une
CI verte n’efface pas une inconnue. CENTRAL conversationnel est une coordination
humaine ; UNIFIED contient les références techniques versionnées.

## Validation sans réseau

Depuis le checkout existant, Python3.12 :

```sh
python3 scripts/validate_unified.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s registry/tests -v
python3 scripts/audit_repos.py --offline --output-dir reports/offline
# Dépendance existante cryptography50.0.0, pas nécessaire aux nouveaux scripts :
python3 -m unittest discover -s backup_prototype/tests -v
```

Le mode offline est **synthétique et déterministe** ; son code0 signifie que le
rapport a été produit, même si la fixture décrit des erreurs403/404. Il ne prouve
pas l’état réel de GitHub. Aucun paquet externe nouveau pour audit/contrats.
Le validateur de schémas est le sous-ensemble fermé documenté dans SEMANTICS.

## Photographie GitHub

```sh
python3 scripts/audit_repos.py --online --output-dir reports/online
```

GET uniquement, accès public d’abord, token optionnel sécurisé via --token-env
GH_TOKEN/GITHUB_TOKEN seulement si nécessaire. Ni valeur en CLI, ni secret dans
fichier.0=preuves récupérées,2=erreurs/inconnues conservées,1=entrée/sécurité/écriture
locale refusée. Rapport JSON et Markdown ; une erreur n’indique pas absence.
--baseline permet de comparer les SHA à une capture archivée. Pas de commit/push
automatique.429 et403 rate-limit sont distincts de forbidden, proxy_forbidden,
timeout et404 inaccessible. Les API PR/CI restent bloquées dans cette session.

Pour reproduire l’inventaire source, préparer des **clones nus** des neuf noms
exacts dans .audit-cache/NOM.git via git clone --bare HTTPS, sans checkout ni
exécution de leurs scripts. Puis :

```sh
python3 scripts/capture_sources.py --cache .audit-cache --output /tmp/repositories-new.json
```

Ce script lit le cache préparé, sans contacter GitHub ni le rafraîchir. La date est
celle d’inspection locale ; noter séparément la date d’acquisition du cache avant
prétendre à une observation live. Les sondes de noms sont consignées séparément
avec leur opération, date et résultat, jamais déduites d’un nom absent du cache.
Relire code/manifestes/appelants après variation de SHA ; un motif IPC automatique
n’est pas une preuve fonctionnelle. Garder l’ancienne capture avant mise à jour.

## Nouvelle mission / décision

Conserver une branche dédiée, base et livrables antérieurs. Ajouter ID stable,
dépôt exact, branche, SHA, preuves datées, blocages et prochaine action dans le
registre de missions existant. Compléter consolidation dans modules.json et une
relation machine dans integrations.json si nécessaire. Préserver tous les champs
manual et snapshots ; ne pas faire disparaître un échec ancien.
Une déclaration doit rester typée déclaration, même si elle paraît plausible.
Les métiers de NEXUS/SERVICES/EVOLUTION sont des cibles, pas des implementations.

Avant livraison : validation, tests, scan de secrets ciblé et état Git ; produire
COMPTE_RENDU_CENTRAL. CI validate-unified se lance en PR ; son job live n’est
activable que manuellement. Aucun APK/modèle construit. CI GitHub non observable
ici : l’indiquer, ne jamais cocher « réussite » à partir des tests locaux.
Si403 empêche la publication, conserver branche/commits et fournir bundle/patch,
sans autre méthode de contournement ni fusion main.

## Reprise 001F — HTTP403 et manipulations sur écran

Constat du 15 octobre2026 : `git ls-remote --symref origin HEAD refs/heads/*`
réussit ; seule main e4435f4 est annoncée. Le contrôle non destructif
`git push --dry-run --porcelain origin refs/heads/mission-001f-closure:refs/heads/mission-001f-closure`
retourne128 et HTTP403 « Permission to bubth720/JARVIS-UNIFIED.git denied to
bubth720. » Aucun push réel tenté en001F, aucun second essai après refus.
[Sorties exactes assainies](../reports/001f/access.json).

Deux blocages distincts : écriture Git refusée sur github.com pourtant autorisé ;
API api.github.com absente de la politique réseau actuellement enforced, et neuf
requêtes API donnent tunnel403/proxy_forbidden. GH_TOKEN est présent par **nom**,
ce qui ne démontre ni sa validité ni sa portée. L’authentification Git est injectée
par le proxy ; aucun secret lu/affiché. Installation GitHub, Contents:write,
Pull requests:write, expiration et règles de branche ne sont pas consultables ici.
Cause exacte du refus Git **non confirmée** : dépôt non autorisé à l’installation,
portée lecture seule, session ou restriction d’environnement restent des hypothèses.
Le refus avant publication d’une nouvelle branche ne prouve pas une protection main.

Étapes à effectuer par l’utilisateur :

1. Ouvrir GitHub connecté à bubth720 → photo du profil → **Settings → Applications →
   Installed GitHub Apps**. Ouvrir **Configure** pour l’installation liée à
   Codex/ChatGPT, si elle apparaît. Dans l’accès aux dépôts, vérifier que
   **JARVIS-UNIFIED** est sélectionné puis enregistrer. Si l’installation est
   gérée par une organisation, demander ce contrôle à son administrateur.
2. Consulter les permissions affichées : **Contents : Read and write** et
   **Pull requests : Read and write** sont nécessaires respectivement au push et
   à la PR. Les permissions d’une GitHub App ne sont pas des cases librement
   modifiables : accepter une mise à jour demandée si disponible ; sinon rétablir
   l’intégration officielle avec les droits proposés ou contacter son support.
   Ne pas générer un PAT dans le chat et ne pas désactiver les protections.
3. Dans les paramètres de connexion GitHub de Codex/ChatGPT, vérifier l’accès au
   dépôt puis réautoriser/reconnecter l’intégration si la sélection GitHub est
   correcte. Les intitulés varient suivant l’interface ; garder cette session et
   son bundle avant de la recréer.
4. Dans la configuration de l’environnement cloud, ouvrir les réglages réseau et
   ajouter **api.github.com** à la liste autorisée **en conservant les domaines
   existants**. Enregistrer/appliquer, puis refaire uniquement le contrôle API.
   Cette modification débloque potentiellement les lectures API/PR ; elle ne
   donne pas de droit GitHub d’écriture. Aucune configuration changée par001F.
5. Après changement effectif, demander la reprise contrôlée : lecture Git/API,
   contrôle d’écriture, puis publication non forcée de mission-001f-closure si
   autorisée, comparaison SHA et fichiers et PR **brouillon** vers main. Au
   premier nouveau refus, arrêter et relever le message. Ne rien fusionner.

## Récupérer et publier manuellement par un accès autorisé

Le bundle initial `.audit-cache/001f/safety.bundle` inclut quatre branches
historiques, sans prérequis externes. Son SHA-256 est
`cae1bb45c87746f695d3db037ea1d2029bd2518737582b5f60319f94e43c4713`.
La restauration clone nu et les SHA de ces quatre branches ont été vérifiés.
Le bundle final `.audit-cache/001f/JARVIS-UNIFIED-001F.bundle` ajoute la branche
001F et contient tous ses commits. Il est ignoré par Git ; son reçu et son SHA
sont livrés à côté dans `JARVIS-UNIFIED-001F.bundle.receipt.json` et
`JARVIS-UNIFIED-001F.bundle.sha256`. Le reçu final est hors Git afin de pouvoir
référencer exactement le commit final sans auto-référence impossible.

Télécharger bundle et fichiers de contrôle depuis l’environnement. Sur une
machine ayant un accès GitHub autorisé, dans un **nouveau dossier** :

```sh
sha256sum -c JARVIS-UNIFIED-001F.bundle.sha256
# Contrôler également l’empreinte annoncée dans le compte rendu de livraison.
git clone -b mission-001f-closure JARVIS-UNIFIED-001F.bundle jarvis-001f-recovery
cd jarvis-001f-recovery
git bundle verify ../JARVIS-UNIFIED-001F.bundle
git fsck --full
git rev-parse HEAD
git ls-tree -r --name-only HEAD
# Clone neuf : origin désigne le bundle, conservé ; ajouter le dépôt réel.
git remote add github https://github.com/bubth720/JARVIS-UNIFIED.git
git ls-remote --symref github HEAD 'refs/heads/*'
# Si la branche existe déjà : comparer/fetcher et vérifier le fast-forward ;
# au moindre désaccord arrêter, aucun forçage.
git push github refs/heads/mission-001f-closure:refs/heads/mission-001f-closure
git ls-remote github refs/heads/mission-001f-closure refs/heads/main
# Après publication, fetch dans le clone de récupération pour comparer les arbres :
git fetch github refs/heads/mission-001f-closure:refs/remotes/github/mission-001f-closure
git diff --exit-code HEAD refs/remotes/github/mission-001f-closure
git ls-tree -r --name-only refs/remotes/github/mission-001f-closure
```

Comparer SHA local/distant, nombre et liste de fichiers, et main au relevé avant
push. Sur GitHub : dépôt → **Pull requests → New pull request**, base main,
compare mission-001f-closure → flèche à côté de Create pull request →
**Create draft pull request**. Résumé : clôture documentaire001F, 80 tests locaux,
ADR non approuvée, aucun raccordement runtime, CI distante à exécuter. Joindre les
liens du bilan et des preuves. Ne pas activer l’auto-merge ni cliquer Merge.
Si main a été modifiée par un tiers, documenter l’écart ; ne pas la réécrire.

## Actualiser après chaque PR ou fusion approuvée

1. Lire les SHA et l’état local, préserver les champs manual et la capture précédente.
2. Créer des clones nus **neufs** datés dans un sous-dossier ignoré .audit-cache ;
   consigner acquisition/commandes/date. Ne pas rafraîchir seulement la date d’un cache.
3. Exécuter capture_sources.py avec ce cache et un fichier temporaire. Comparer
   branches/SHA/graph/fichiers/empreintes, relire chaque changement et appelant.
4. Archiver l’ancienne photographie sous registry/evidence/ avant de promouvoir
   la nouvelle dans repositories.json. Refaire les preuves source liées aux SHA,
   garder rapports historiques et leur date ; ne pas hériter d’une CI d’un autre SHA.
5. Mettre à jour modules.consolidation, missions, matrice et inventaire ; conserver
   intégralement manual, blocages/décisions et anciens snapshots. Une preuve locale
   ne remplit pas last_verified_commit distant.
6. Audit API --online vers un **nouveau** reports daté ; enregistrer API inaccessible,
   unknown ou not_checked par dépôt si nécessaire. Aucun succès inventé. Mettre à
   jour registre historique via son collecteur seulement après choix explicite
   de branches et revue du résultat ; pas de remplacement silencieux par démo.
7. Revalider et tester, commit dédié, revue utilisateur/PR ; indiquer les dates de
   fraîcheur dans README. Les rapports 001F restent une photographie historique,
   jamais une promesse de synchronisation live avec CENTRAL ou les autres chats.
