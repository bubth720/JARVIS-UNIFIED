# R-11 — Plan d'archivage des branches (aucune suppression, aucune action réalisée)

## Principe

Archiver signifie **conserver chaque commit sous une étiquette annotée** `archive/<date>/<branche>`, puis, seulement sur ton accord, retirer la branche de la liste active. Une branche n'est jamais supprimée sans étiquette préalable vérifiée (même SHA).

## Candidats

Source : `audit/final-01/BRANCH-STATUS.csv`.

| Groupe | Critère vérifiable | Nombre | Action proposée |
|---|---|---|---|
| A | Tête contenue dans une PR ouverte (`in_open_pr`) | 214 | Aucune tant que la PR est ouverte : la branche porte la PR |
| B | Tête contenue dans une autre branche (`inside_other_branch`) | 17 | Étiquette `archive/` puis retrait possible : le code reste accessible par la branche contenante et l'étiquette |
| C | Tête déjà dans la branche par défaut (`in_main`) | 3 | Étiquette puis retrait possible |
| D | Front sans PR (`FRONTIER_NO_PR`) | 21 | **Ne pas archiver** : travail le plus récent (voir R-01) |

## Procédure, branche par branche

1. Vérifier que le SHA de la branche est identique à celui inscrit dans `BRANCH-STATUS.csv`.
2. Créer l'étiquette annotée `archive/2026-11/<branche>` sur ce SHA ; la vérifier avec `git ls-remote`.
3. Lister les PR qui utilisent la branche comme tête ou comme base : s'il y en a une, **stop**.
4. Retrait de la branche **uniquement avec ton accord écrit** (dépôt, branche, SHA). Réversible : `git push origin archive/…:refs/heads/<branche>`.

Les branches historiques gardées par une CI (V1, M50, prefusion, UNI-08) restent inchangées ; leurs gardes sont rejoués sur leur propre SHA (R-07).
