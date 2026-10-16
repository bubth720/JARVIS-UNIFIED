# Rapport final — Mission 002

Date : 15 octobre 2026. Branche : `mission-002-backup`.

## Préalable accompli

Les cinq livrables Mission001 existaient sur `audit/mission-001`, non commités.
Ils ont été lus et préservés dans le commit documentaire **004b89d**
(`docs: preserve Mission 001 audit and architecture`), puis la branche dédiée
Mission002 a été créée à partir de ce commit. Aucun changement de main, push,
merge, suppression de projet ou modification d'une source.

Précision documentaire : le tableau des SHAs de Mission001 contient 4 branches
CORE, 6 LLM et 6 VOICE hors alias HEAD ; la mention « 7 VOICE » et « six branches
de fonctionnalités VOICE » dans le texte ancien surcomptait cette liste.
L'inventaire immuable lui-même reste utilisable ; cette mission n'a pas relancé
une découverte distante ni prétendu connaître de nouvelles branches.

## Livré

- [BACKUP_FORMAT.md](BACKUP_FORMAT.md) : inventaire des données et emplacements,
  conteneur chiffré v1, manifeste et limites de portabilité.
- [RESTORE_PLAN.md](RESTORE_PLAN.md) : commandes, export sans écrasement,
  générations, transaction et récupération après panne.
- [COMPATIBILITY.md](COMPATIBILITY.md) : identités d'applications, moteurs,
  profils vocaux, ressources et conditions du futur transfert mini-PC.
- [backup_prototype](backup_prototype/README.md) : CLI Python, démo complète,
  dépendance déclarée, [manifeste fictif lisible](backup_prototype/manifest.example.json)
  et tests automatisés.
- [resources](resources/README.md) : TABLET/MOBILE/CENTRAL/VOICES préparés,
  uniquement métadonnées, aucun téléchargement ni poids.

Le prototype crée un snapshot SQLite fictif cohérent, catalogue/préférences et
profil vocal de démonstration ; chiffre par AES-256-GCM avec clé scrypt ; vérifie
manifeste, SHA-256 et compatibilités avant écriture. La restauration crée une
nouvelle génération et bascule un pointeur atomique, sans supprimer les anciennes.
Les souvenirs sans autorisation sont exclus de la copie, pas de la source ; ceux
restaurés attendent une confirmation locale du contenu exact.

## Vérifications exécutées

Environnement : Python **3.12.14**, SQLite **3.53.1**, cryptography **50.0.0** déjà
installée. Pas d'installation de dépendance, de requête réseau ou de modèle.

```sh
python3 -m unittest discover -s backup_prototype/tests -v
python3 -m backup_prototype.demo
python3 -m backup_prototype.backup --help
```

**30 tests réussis, 0 échec, 0 erreur, 0 ignoré**, code retour 0.
Durée de la campagne finale : 10,698 s sur cette machine, pas une mesure Android.
Le journal local de cette campagne est `/tmp/jarvis-mission002-tests-final.log` ;
le [résumé structuré](backup_prototype/validation.json) reste dans le dépôt.

| Domaine | Preuve réalisée |
|---|---|
| Cycle complet | Six objets chiffrés, vérifiés et restaurés à l'identique ; textes du payload absents de l'archive en clair |
| Intégrité et cryptographie | Mauvais mot de passe, sel/nonce/ciphertext/tag altérés et troncature refusés ; sel/nonce nouveaux à chaque export |
| Sémantique et formats | Mauvais SHA sous AEAD valide, métadonnées malformées, version future, JSON dupliqué, SQLite corrompu/version future, moteur et pack incompatibles refusés |
| Chemins et quotas | Traversée, chemins absolus/Windows, doublons, fichiers inconnus, symlinks, objets/enveloppes trop grands et store étranger refusés |
| Données | IDs, contenu, relations et compteur d'auto-incrément conservés ; comparaison byte-à-byte des sources fictives sans WAL |
| SQLite WAL | Snapshot inclut une ligne commitée dans WAL et exclut la transaction en cours ; base de travail toujours lisible avec son état intact |
| Mémoire | Souvenirs en attente/refusés absents de la copie et de ses pages libres ; preuve fausse rejetée ; réactivation locale exacte seulement |
| Conflits | Archive existante jamais écrasée ; restauration identique idempotente ; nouvelle archive refusée sauf --replace, ancienne génération retenue |
| Récupération | Panne après staging, avant activation, après activation ; récupérateur dans un nouvel interpréteur ; première activation annulable |
| Processus et erreurs IO | Mort abrupte os._exit(73), ENOSPC, échec d'écriture du pointeur et temporaire orphelin ; récupération/réessai sans perte |
| Concurrence | Deux processus restaurent le même store : une activation et un no-op, pas de double bascule incohérente |
| Destination abîmée | Une génération active corrompue n'est pas silencieusement remplacée |

La démo indépendante a renvoyé PASS pour création chiffrée, vérification,
restauration des octets, panne après activation, retour à l'ancienne génération,
conservation de cette génération et des sources, puis réessai réussi.
Aucune donnée privée n'a été utilisée comme fixture. La clé de démonstration est
éphémère et n'est ni affichée ni conservée.

Contrôles de livraison : liens Markdown locaux, JSON de ressources/manifeste,
`git diff --check`, présence des cinq fichiers dans le commit Mission001, branche
dédiée et origine main inchangée. Les 320 fichiers des archives des trois sources
retenues ont été comparés aux blobs Git immuables, sans différence.

## Difficultés résolues et limites

Une validation ajoutée avant compactage a exposé un problème : le snapshot
intermédiaire pouvait encore porter un en-tête WAL et ne pouvait pas être
redésérialisé sans fichiers annexes. La validation est faite sur la connexion
Backup API vivante avant filtrage/compactage ; le test WAL passe avec les autres.
Les contrôles abandonnés de transaction laissent volontairement des générations
ou temporaires privés : la récupération ne les promeut pas et ne les supprime pas.

Ce prototype ne sauvegarde aucune installation Android réelle. Son profil vocal
est un JSON synthétique non utilisable pour l'inférence, pas un clone testé. Les
limites v1 (4 Mio/objet, 16 Mio décodés, 24 Mio enveloppe) excluent les vrais poids.
Les données restaurées sont en clair dans un store privé, pas dans un coffre
chiffré actif. Les primitives POSIX, les sauvegardes multi-fichiers, l'import
Android/SAF, la cohérence du catalogue natif et les packs/profils réels nécessitent
des adaptations et validations séparées avant usage personnel.

Les confirmations de la fixture sont des preuves synthétiques ; aucune ancienne
confirmation réelle n'est supposée. Les sources ne possèdent pas toutes un export
global utilisable et leurs sandbox ne sont pas accessibles à UNIFIED. Les données
réelles restent donc dans leurs applications ; ne pas désinstaller pour contourner
l'extraction. Aucun développement de fusion ni mission supplémentaire commencé.
