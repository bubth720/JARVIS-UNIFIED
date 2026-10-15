# Mission001G — clôture de maintenance UNIFIED

**80 tests réussis ; sept branches publiées ; PR brouillon non créée : API bloquée.**
Dépôt exclusif : bubth720/JARVIS-UNIFIED. Aucun raccordement, migration, changement
de voix ou modification d’autre dépôt. Aucune fusion dans main.

## Branche et conservation

Branche : `mission-001g-maintenance`, issue de
`e0e6f69c4908a152da4e43864a08fef0c8f7a7af` (ADR approuvée).
Commit de correctif testé et publié : `0aa8f7063732a2c7a6ab13b0d6652db1b892c0b2`.
Le commit de rapport qui le suit et le SHA final sont fournis par `git rev-parse
mission-001g-maintenance`, la vérification distante finale et le reçu de sauvegarde
hors Git. Les anciens constats ne sont pas réécrits comme observations live.

Branches antérieures préservées et publiées sans réécriture :
- `audit/mission-001` : `004b89d1f86135962e452fb644b489f69fc177d1`.
- `mission-002-backup` : `55680bcfe1f793618c79eb1bdc7b2b8c847b369e`.
- `mission-003-central-registry` : `f7b7a5ad96527bc43bd5349b97b7834667da9f03`.
- `mission-001-architecture-unified` : `d74730a4b5ed817de1cdd163a96c3bdf72a1e4d8`.
- `mission-001f-closure` : `4f06ef43ae98cf093dcc1601d0c95016d89e8ffd`.
- `docs/adr-001-approved-2026-10-15` : `e0e6f69c4908a152da4e43864a08fef0c8f7a7af`.

## Correction strictement limitée

Dans registry/tests/test_registry.py, test_read_valid_registry : attente du
nombre de missions15→16, une seule ligne changée. Les15 entrées d’origine au
commitf7b7a5a sont intégralement identiques et UNIFIED-001F est une mission locale
légitime sur sa branche existante. Les16 IDs sont uniques et le registre valide.
[Inventaire de justification](reports/001g/inventory.json).

L’échec précédent a été reproduit avant correction :
[log avant correction](reports/001g/before-test.txt). Aucun test désactivé,
aucune donnée changée, aucune assertion retirée. Schémas, runtime et ADR inchangés.

## Vérifications exécutées

| Commande | Résultat |
|---|---|
| python3 -m unittest discover -s tests -v | 27 réussis |
| python3 -m unittest discover -s registry/tests -v | 23 réussis |
| python3 -m unittest discover -s backup_prototype/tests -v | 30 réussis |
| python3 scripts/validate_unified.py | Réussi : neuf dépôts, cinq contrats et exemples |
| python3 registry/scripts/update_registry.py --validate-only | Réussi : neuf dépôts, seize missions |
| git diff --check et contrôle indexé | Réussis pour les changements001G |

**80/80, zéro échec, zéro saut**. Journaux/durées/plateforme/empreinte du test :
[validation.json](reports/001g/validation.json), audit-contracts.txt, registry.txt,
backup.txt ; [contrôles](reports/001g/checks.json). Les anciens rapports79/80
restent historiques. Aucun test Android, physique ou résultat CI distant obtenu.

## Publication et diagnostic

Remote assaini : https://github.com/bubth720/JARVIS-UNIFIED.git.
Lecture Git et contrôle à blanc réussis, puis **push réel atomique réussi** des
sept branches explicitement choisies, sans force et sans main. Leurs SHA distants
ont été relus et comparés : tous identiques aux SHA locaux.
[Preuve de publication](reports/001g/publication.json).
Main reste `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b`.
Le refus Git d’écriture observé précédemment n’est plus reproductible :
la publication effective fonctionne. Sa cause passée exacte n’est pas prouvée.

**Blocage restant distinct : API GitHub.** GET anonyme vers api.github.com
retourne « Tunnel connection failed: 403 Forbidden ». Le domaine est absent de
la politique réseau appliquée (restricted/enforced). GitHub.com est autorisé.
GH_TOKEN est présent par nom, aucune valeur inspectée ou publiée. La portée du
jeton/installation, les protections et permissions PR ne sont pas observables :
une publication Git réussie ne prouve pas l’accès API ou le droit PR.
[Contrôles d’accès](reports/001g/access.json). Aucune répétition du refus API,
aucun contournement proxy/TLS/authentification.

PR : **non créée**, aucune URL de PR inventée. Une seule PR agrégée vers main
est à ouvrir depuis mission-001g-maintenance : elle inclut consolidation,
approbation ADR et maintenance dans un historique linéaire.
[Texte de PR préparé](reports/001g/PR_DRAFT.md).

## Opérations à effectuer sur écran

1. La configuration réseau a été enregistrée **en brouillon** via le workflow
   cloud-environment-onboarding:setup : ajout de api.github.com aux règles
   personnalisées, règles personnalisées existantes et presets conservés.
   Aucun secret, script ou dépôt de configuration changé. Enregistrement confirmé,
   requires_publish=true ; cela n’applique pas le réglage à cette session.
2. Ouvrir paramètres de l’environnement Codex → réseau ; examiner/enregistrer
   l’ajout api.github.com puis **publier l’environnement**. Conserver le bundle
   avant tout changement de session. Ne pas élargir à tous les domaines.
3. Après application, demander uniquement la reprise de création de PR brouillon.
   Si l’API répond mais refuse encore, vérifier GitHub → Settings → Applications →
   Installed GitHub Apps → Configure l’intégration Codex/ChatGPT : accès à
   JARVIS-UNIFIED et permission Pull requests en écriture. Accepter si nécessaire
   une mise à jour d’autorisation officielle ; aucun jeton à transmettre au chat.
4. Alternative immédiate dans le navigateur : ouvrir
   https://github.com/bubth720/JARVIS-UNIFIED/compare/main...mission-001g-maintenance?expand=1
   puis Create pull request → flèche → **Create draft pull request**. Utiliser
   le titre/texte préparés. Ne pas activer l’auto-merge ni cliquer Merge.

## Sauvegarde vérifiée

Bundle initial complet incluant le commit ADR approuvé :
`.audit-cache/001g/before-001g.bundle`, SHA256
`584379ed12ecdca0e483bcf3062790aaa2cc5e6b98241e1337b4523c03c0b2c9`.
Vérification Git, clone nu isolé et fsck réussis ; les six branches ont été
comparées aux SHA d’origine. [Reçu initial](reports/001g/preservation.json).

Bundle final hors Git : `.audit-cache/001g/JARVIS-UNIFIED-001G.bundle`.
Il ajoute la branche001G aux six branches précédentes. Les fichiers adjacents
`.sha256` et `.receipt.json` fournissent empreinte finale, SHA et restauration
isolée vérifiée. Reçu hors Git pour pouvoir référencer le commit final exact.
Aucun ancien bundle, export, fichier ou branche supprimé.

## ADR et prochaines missions proposées

[ADR-001](docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md) reste **APPROUVÉE AVEC PRÉCISIONS**,
option3, orientation seulement. Aucune nouvelle approbation demandée. Contrats v1
inchangés ; aucune intégration CORE↔LLM/VOICE déclarée opérationnelle.

- CORE : mission séparément autorisée de stabilisation du CORE actuel,
  commandes/SQLite/PDF/capture/lifecycle, sauvegarde et restauration fictives,
  sans suppression des fonctions ni raccordement.
- LLM : mission séparément autorisée de qualification003B sur Redmi/POCO,
  diagnostic passif puis admission naturelle, arrêt/déchargement effectifs,
  RAM/thermique/batterie. Conserver les refus et protections, sans baisse de seuil
  ni activation prématurée de PLEINE PUISSANCE.

La proposition technique du futur parcours CORE→LLM→CORE dépend de ces preuves,
de choix IPC/identité/arbitre approuvés et d’une autorisation distincte. Aucune
mission supplémentaire commencée ici.

## Fichiers de cette maintenance

Code : uniquement registry/tests/test_registry.py (15→16).
Documentation : README.md et le présent rapport. Preuves : reports/001g/
(inventaire, échec initial, logs, contrôles, accès/publication, texte PR).
Anciennes preuves, données du registre et décision ADR conservées.
