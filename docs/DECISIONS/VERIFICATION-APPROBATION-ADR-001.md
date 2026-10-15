# Consignation de l’approbation ADR-001 — vérifications

Date de décision : 15 octobre2026. Vérifications locales : 2026-10-15T20:41:06+00:00.
Référence : [USER-ADR-001-2026-10-15](VALIDATION-UTILISATEUR-ADR-001-2026-10-15.md).
Module : UNIFIED ; opération documentaire d’enregistrement d’une décision,
aucune nouvelle mission de consolidation ou d’intégration commencée.

## Résultat documentaire

- [ADR-001](ADR-001-CORE-LLM-UNIFIED.md) : **APPROUVÉE AVEC PRÉCISIONS**, option3,
  exclusivement l’orientation ; huit rôles, applications autonomes initiales,
  pilote Android prudent et protections, préservation/réversibilité, consentement
  exact et fonctionnement local. Les sept sujets ouverts restent explicitement
  non approuvés. Les contrats v1 et les détails de la revue préalable ne sont
  pas automatiquement acceptés par cette décision.
- Décision utilisateur et portée autorisée consignées avec référence locale ;
  aucune prétention d’identifiant ou de validation GitHub.
- README, roadmap et plan futur alignés ; revue001F et bilan central signalés
  historiques. Les observations GitHub et anciens résultats ne sont pas réécrits.
- Les anciens bundle/ADR autonome/ZIP001F restent des exports historiques,
  intacts et antérieurs à l’approbation. Le document ADR versionné actuel ci-dessus
  est la référence pour la décision approuvée.

## Branche, conservation et publication

Branche documentaire : `docs/adr-001-approved-2026-10-15`.
Base exacte : `4f06ef43ae98cf093dcc1601d0c95016d89e8ffd` (mission-001f-closure).
Le SHA du commit documentaire est donné par `git rev-parse HEAD` sur cette branche
et dans le compte rendu de livraison ; pas d’auto-référence à son propre SHA.

Références historiques locales vérifiées inchangées :
- `mission-001f-closure` : `4f06ef43ae98cf093dcc1601d0c95016d89e8ffd`.
- `mission-001-architecture-unified` : `d74730a4b5ed817de1cdd163a96c3bdf72a1e4d8`.
- `mission-003-central-registry` : `f7b7a5ad96527bc43bd5349b97b7834667da9f03`.
- `mission-002-backup` : `55680bcfe1f793618c79eb1bdc7b2b8c847b369e`.
- `audit/mission-001` : `004b89d1f86135962e452fb644b489f69fc177d1`.
- `origin/main` : `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b`.

Aucune tentative de push, aucune PR, aucune fusion ou réécriture de main.
Dernier constat d’accès distant conservé : contrôle001F refusé HTTP403 dans
[access.json](../../reports/001f/access.json). Les droits n’ont pas été déclarés
rétablis ; aucune nouvelle opération réseau réalisée pendant cette consignation.
Le statut distant est historique, pas une nouvelle lecture de GitHub.

## Vérifications réellement exécutées

Plateforme : Linux-6.18.44-x86_64-with-glibc2.41, Python3.12.14.

| Commande | Résultat |
|---|---|
| `python3 scripts/validate_unified.py` | Réussi : 9 dépôts, 5 contrats, 5 exemples valides et 5 invalides rejetés ; liens/JSON/jetons usuels vérifiés |
| `python3 registry/scripts/update_registry.py --validate-only` | Réussi : 9 dépôts, 16 missions |
| `git diff --check` puis contrôle des changements indexés | Réussis, aucune anomalie dans les changements documentaires |
| `python3 -m unittest discover -s tests -v` | 27 tests ; OK ; code sortie0 |
| `python3 -m unittest discover -s registry/tests -v` | 23 tests ; FAILED (failures=1) ; code sortie1 |
| `python3 -m unittest discover -s backup_prototype/tests -v` | 30 tests ; OK ; code sortie0 |

**80 tests exécutés : 79 réussis, 1 échec, aucun saut.** Les journaux complets
restent dans `.audit-cache/adr-001-approved/` (audit-contracts.log, registry.log,
backup.log et tests.json), hors Git. Aucun test Android, appareil ou CI distante.

### Échec préexistant confirmé, laissé intact

`registry/tests/test_registry.py`, test_read_valid_registry, attend exactement15
missions ; le registre contient16 missions depuis l’ajout de UNIFIED-001F.
Ce nombre et cette assertion sont déjà présents à la base4f06ef4, avant la présente
modification. Le validateur de registre accepte les16 missions. Les22 autres tests
registre réussissent ; aucune donnée supprimée pour rendre ce test vert, aucun
code/test modifié sous cette autorisation documentaire. Une correction éventuelle
exige une autorisation distincte. Les80 réussites du rapport historique001F ne sont
pas utilisées pour masquer cet échec constaté sur son état final.

## Contrôles de périmètre

Diff contre la base : uniquement fichiers Markdown. Aucun changement de
contracts/, scripts/, tests/, registry/, backup_prototype/, .github/ ou AGENTS.md.
Branches historiques et références locales de main inchangées. Bundle et ADR
exportés précédemment vérifiés par SHA256, originaux préservés. Aucun contenu
applicatif ni donnée personnelle ajouté. Aucun adaptateur, transport, arbitre ou
migration développé ; les évolutions de contrats sont seulement documentées.

## Prochaine action recommandée

Rétablir l’accès GitHub autorisé pour publier la documentation sans forçage ni
fusion, puis soumettre une proposition technique bornée sur les choix encore
ouverts. Ne pas redemander l’approbation de l’orientation. Toute implémentation,
installation, migration ou correction de code/test requiert une autorisation
séparée. Ne pas commencer ces travaux dans la présente opération.
