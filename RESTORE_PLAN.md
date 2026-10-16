# Sauvegarde, restauration et récupération — Mission 002

Portée : prototype local Linux/Python, données générées exclusivement. Format et
inventaire : [BACKUP_FORMAT.md](BACKUP_FORMAT.md). Aucun accès aux données Android
réelles ni modification des trois dépôts sources.

## Exécution reproductible

Depuis la racine de JARVIS-UNIFIED : Python 3.12 (SQLite avec serialize/deserialize)
et `cryptography==50.0.0`. Cette version était déjà installée ; aucun paquet ni
modèle n'a été téléchargé pendant la mission. Sur une autre machine, préparer un
venv et installer les dépendances déclarées avant usage ; aucune installation
automatique dans le prototype.

```sh
python3 -m unittest discover -s backup_prototype/tests -v
python3 -m backup_prototype.demo
```

La démo réalise le cycle complet avec clé éphémère en RAM : fixture → archive
chiffrée → vérification → restauration → panne après activation → rollback →
nouvelle restauration. Elle vérifie les octets source et ceux de la génération
précédente, puis supprime son seul répertoire temporaire de démonstration. Aucun
artefact personnel ou mot de passe n'est écrit dans Git. Cette démo est jetable :
sa clé n'est pas conservée pour une utilisation ultérieure.

Pour examiner manuellement une fixture conservée, créer un emplacement privé
hors du checkout (remplacer le chemin ci-dessous par un nouveau dossier) :

```sh
mkdir -m 700 /tmp/jarvis-backup-manual
python3 -m backup_prototype.backup demo-fixture /tmp/jarvis-backup-manual/source
python3 -m backup_prototype.backup export /tmp/jarvis-backup-manual/source /tmp/jarvis-backup-manual/demo.jvb
python3 -m backup_prototype.backup verify /tmp/jarvis-backup-manual/demo.jvb
python3 -m backup_prototype.backup restore /tmp/jarvis-backup-manual/demo.jvb /tmp/jarvis-backup-manual/store
```

Les commandes export/verify/restore demandent le mot de passe au terminal.
Ne pas utiliser de données réelles même si un fichier est renommé en fixture.
Le marqueur `synthetic-demo-only` est une garde d'usage, pas une preuve technique
que des données arbitraires ne sont pas personnelles.

## Export sans écrasement

1. Vérifier marqueur fictif et chemins locaux sans symlinks, schémas et preuves.
2. Lire les fichiers autorisés explicitement, sans parcours d'un disque personnel.
3. Créer le snapshot SQLite en mémoire ; filtrer les souvenirs dans la copie,
   conserver les autres données et les compteurs, compacter la copie.
4. Former manifeste + objets, chiffrer en RAM, redéchiffrer et vérifier entièrement.
5. Écrire un temporaire 0600 dans le même dossier que l'archive, flush/fsync.
6. Publier par lien dur atomique **sans écrasement**, puis fsync du dossier.
   Un nom existant provoque un refus ; le temporaire est retiré, pas l'original.

Le support doit offrir liens durs/fsync pour ce prototype. Sur FAT/SAF Android,
un adaptateur de publication spécifique devra être testé. Le refus est préférable
à une dégradation silencieuse. Une interruption peut laisser un temporaire privé,
jamais interprété comme archive terminée. Les fichiers source ne sont pas modifiés.

## Destination gérée et générations

```text
store/                                  # privé 0700, arbre contrôlé par l'utilisateur
  store.json                            # marqueur/version du démonstrateur
  .lock                                 # verrou exclusif POSIX, libéré à mort du processus
  generations/
    <uuid-hex>/
      payload/...                       # octets vérifiés, permissions fichier 0600
      manifest.json
      receipt.json                      # SHA archive et registre de confirmation
      memory-review.json                # souvenirs inactifs ou confirmés localement
    <uuid-hex>.staging/                  # tentative incomplète, jamais sélectionnée
  state.json                            # {active, previous}, seule bascule atomique
  journal.json                          # ancienne/nouvelle valeur, transaction non terminée
  .pending-<uuid-hex>                    # contrôle orphelin éventuel, conservé sans être utilisé
```

Aucun dossier arbitraire existant n'est absorbé. Symlinks et fichiers étrangers
sont refusés. Le modèle suppose un arbre privé non modifié par un attaquant local
du même compte pendant l'opération ; le contrôle de symlinks par chemin n'est pas
une défense complète contre toutes les courses TOCTOU d'un tel attaquant.
Toutes les écritures du store sont sérialisées par flock. Les adaptateurs Android
futurs doivent fournir un verrou et des primitives équivalentes, non copiés tels
quels depuis cette implémentation POSIX.

## Restauration

1. Lire sous quota et authentifier l'enveloppe ; mauvaise clé ou altération : refus.
2. Vérifier le manifeste, toutes les tailles/SHA, SQLite/intégrité/schéma/relations,
   les versions, moteur et pack vocal. Aucun fichier destination avant cette étape.
3. Vérifier les confirmations locales contre IDs et empreintes exactes, sans
   accepter automatiquement l'autorisation indiquée par l'archive reçue.
4. Sous verrou : valider le store et sa génération active. Journal existant :
   refuser jusqu'à `recover`. Même SHA d'archive et mêmes confirmations : no-op,
   après contrôle de l'intégrité active. Nouvelle archive : conflit par défaut.
5. `--replace` autorise une **nouvelle génération**, sans supprimer ni fusionner
   les données de l'ancienne. Tous les objets sont écrits/fsync dans staging.
6. Renommer staging vers génération, fsync, relire et revalider tous les fichiers.
7. Écrire/fsync le journal ancien/nouveau ; remplacer atomiquement state.json,
   puis fsync. La génération précédente est retenue dans `previous` et sur disque.
8. Retirer le journal, fsync du dossier, annoncer le succès.

Aucune fusion automatique par ID ou sélection de la révision « la plus récente »
n'est implémentée. Les conflits restent des snapshots séparés. Une future fusion
logique doit afficher les écarts et faire confirmer les décisions, sans pertes
ni réactivation de souvenirs refusés. Versions nouvelles, formats vocaux ou
packs différents : refus et conservation des fichiers d'origine.

## Récupération après interruption

`python3 -m backup_prototype.backup recover CHEMIN_STORE` ne demande pas de clé :
il agit sur les générations déjà déchiffrées d'un espace privé. Il ne déchiffre
pas une archive et ne peut pas reconstituer des données perdues sans sauvegarde.

| Point d'arrêt | État possible | Récupération |
|---|---|---|
| Avant publication archive | Aucun nouveau fichier final | Ancienne archive intacte ; supprimer manuellement un temporaire après examen |
| Après staging | Ancienne génération active, staging isolé | Valider état actif ; garder staging pour diagnostic ; réessai possible |
| Journal écrit, avant bascule | Ancien pointeur actif | Vérifier ancien snapshot puis rétablir sa valeur et retirer le journal |
| Après bascule, avant fin de transaction | Nouveau pointeur, journal encore présent | Rollback par défaut vers ancien pointeur ; aucune génération supprimée |
| Première restauration interrompue après bascule | Nouveau pointeur, ancien état absent | Retirer uniquement le pointeur géré ; conserver génération ; restaurer à nouveau |
| Échec d'écriture du pointeur | Ancien pointeur + journal/temporaire | Même rollback ; temporaire orphelin conservé, jamais promu |
| Ancienne génération corrompue ou journal incohérent | Situation non fiable | Refus de rollback automatique, garder journal et tous fichiers pour examen |

La récupération ne supprime jamais les sources ou générations. En absence de
journal, elle contrôle seulement la génération active : ce n'est pas une commande
générale d'annulation d'une restauration déjà achevée. Pour revenir après un succès,
restaurer l'ancienne archive avec `--replace` ; une commande de sélection d'une
ancienne génération n'est pas implémentée dans cette mission.

Les simulations couvrent une exception, un processus terminé par `os._exit(73)`,
ENOSPC et une erreur d'écriture. Elles ne simulent pas une panne de contrôleur
flash ou l'ensemble des garanties SAF/OEM. fsync et remplacement atomique sont
vérifiés fonctionnellement sur le système Linux courant, pas certifiés sur Android.
Les lecteurs futurs doivent refuser un store dont le journal est présent ; aucun
consommateur métier n'est encore branché sur ce store.

## Données privées, mémoire et limites opérationnelles

L'archive est chiffrée ; les données restaurées sont **en clair dans un dossier
privé**. Employer le chiffrement du disque/sandbox sur l'appareil futur. Le
prototype n'est pas un coffre chiffré de données actives et n'efface pas de façon
prouvable les buffers Python en RAM ou les pages SSD. Aucun secret n'est fourni
par la plateforme ni demandé en chat ; sauvegarder les mots de passe séparément.

Les profils vocaux réels nécessiteraient leur propre consentement d'export et
compatibilité exacte de pack. Le faux profil ne peut pas servir à parler.
L'historique et les documents ne sont pas des confirmations de souvenirs.
Le registre de confirmation est une simulation locale, pas une UI Android
anti-contournement. Les données legacy restent à leur origine tant que leur
récupération et leur autorisation ne sont pas établies.

Le prototype borne ses archives mais n'effectue pas une réservation d'espace.
Un disque plein provoque l'échec et garde l'ancienne génération ; tester la place
nécessaire et les callbacks d'annulation Android reste nécessaire avant production.
Les générations/staging sont conservés et peuvent remplir le disque : pas de GC
automatique, toute suppression ultérieure devra être explicite et séparée.
