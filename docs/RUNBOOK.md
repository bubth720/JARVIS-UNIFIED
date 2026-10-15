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
