# Preuves de clôture 001F

Photographie datée, non synchronisation live. Aucun log ne contient de jeton,
prompt utilisateur, audio/profil privé ou données réelles de sauvegarde.

| Fichier | Portée |
|---|---|
| [preservation.json](preservation.json) | Quatre branches protégées, bundle initial, SHA256, restauration isolée vérifiée |
| [access.json](access.json) | Lecture Git réussie, dry-run écriture refusé403, aucune publication réelle |
| [acquisition.json](acquisition.json) | Neuf clones nus neufs, dates UTC, commandes et résultats |
| [repositories.json](repositories.json) | Capture fraîche des fichiers/branches/graph, identique à l’inventaire promu dans registry |
| [comparison.json](comparison.json) | Différence avec photographie antérieure, VOICE seule tête sélectionnée modifiée |
| [naming-probes.json](naming-probes.json) | Sondes CORE/EVOLUTION inaccessibles ; absence non prouvée |
| [online/SUMMARY.md](online/SUMMARY.md) | Neuf refus API proxy403 ; sortie2 attendue pour audit incomplet, pas CI réussie |
| [validation.json](validation.json) | Commandes, plateforme, durées, totaux et empreintes des sources effectivement testées |
| [audit-contracts.txt](audit-contracts.txt) | Log réel 27 tests |
| [registry.txt](registry.txt) | Log réel 23 tests |
| [backup.txt](backup.txt) | Log réel 30 tests avec fixtures et archives synthétiques |

Le collecteur source et les tests ne modifient pas les dépôts distants. Un clone
nu télécharge leurs objets Git (y compris livraisons déjà versionnées), n’installe
aucun APK, n’exécute aucune application et ne télécharge aucun modèle séparé.
La CI GitHub UNIFIED n’a pas été exécutée ; les rapports Android historiques ne
sont pas des exécutions de cette mission.

Reproduction depuis le checkout UNIFIED :

```sh
python3 scripts/validate_unified.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s registry/tests -v
python3 -m unittest discover -s backup_prototype/tests -v
```

Le bundle **final**, son SHA256 et son reçu sont dans le dossier ignoré
`.audit-cache/001f/` ; voir [runbook](../../docs/RUNBOOK.md). Son reçu n’est pas
commité, afin de pouvoir référencer le SHA final exact. Une empreinte SHA256
assure l’intégrité par comparaison avec le compte rendu, pas une signature tierce.
