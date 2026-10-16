# Prototype fictif de sauvegarde — Mission 002

Python 3.12 + cryptography 50.0.0. Aucun moteur, poids ou profil personnel.
Depuis la racine du dépôt :

```sh
python3 -m unittest discover -s backup_prototype/tests -v
python3 -m backup_prototype.demo
python3 -m backup_prototype.backup --help
```

La démo automatique génère sa clé en RAM et supprime son répertoire temporaire
après validation. Le CLI interactif permet de conserver une fixture et une archive
avec un mot de passe saisi au terminal. Ne pas lui confier des données réelles.

Documentation : [format](../BACKUP_FORMAT.md), [procédure](../RESTORE_PLAN.md),
[compatibilités](../COMPATIBILITY.md), [rapport](../MISSION_002_REPORT.md).
Les tests ne requièrent aucun réseau, Android, modèle ou secret externe.
