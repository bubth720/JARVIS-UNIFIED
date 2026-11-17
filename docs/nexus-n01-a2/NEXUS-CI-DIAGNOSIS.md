# N01-A2 — reproduction et correctif de contexte CI NEXUS

## Cause reproduite

Run historique [42523863724](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42523863724), source `b7d9d884`, événement pull_request #14 de `codex/reuse-first-r1plus-20261108` vers `codex/m53-readonly-preparation`.

`.github/workflows/nex-07.yml` ne reconnaît que les contextes M50 et LOT3. REUSE tombe dans le `else` qui exécute `tools/check-prefusion.py`. Ce garde contrôle un autre socle (`bdb51f77`) et quatre ajouts permis ; il refuse correctement les fichiers M53/REUSE avec `ValueError: Undeclared files`. Les tests qui suivent sont sautés. Il ne s’agit pas d’une preuve de défaut du RAG ni d’un garde à désactiver.

Au même source REUSE, `reuse-r1plus/check.py` passe : les **329 fichiers et modes M53** (`eae61fb6`) sont identiques ; seuls les ajouts sous `reuse-r1plus/` et son workflow dédié sont autorisés. Le workflow NEX-07 lui-même appartient à ces fichiers M53 gelés.

## Changement appliqué dans la portée autorisée

Branche NEXUS : `codex/nexus-n01-a2-ci-review-20261117`, commit `2dd4447acb592e9e63123c0377b6310d4dae2bf1`.

- Ajout de 11 régressions dans `reuse-r1plus/n01-a2/tests/test_scope_context.py` et d’une note de diagnostic.
- Ajout du déclenchement manuel et de cette branche au workflow REUSE, fichier explicitement autorisé comme ajout par le garde actuel. Sa commande de préservation historique reste inchangée.
- Aucun changement de `tools/check-prefusion.py`, `tools/check-nex07.py`, `reuse-r1plus/check.py`, du workflow NEX-07 gelé, d’un contrat ou d’une source métier.

Les tests vérifient : refus du contexte PRE-FUSION sur REUSE, passage du garde REUSE, identité des scripts de garde, refus d’une mutation métier/contrat, d’un changement du workflow gelé, d’un mode exécutable, d’un symlink ou d’un ajout hors portée ; passage des anciens gardes à leurs propres SHA historiques. Les mutations négatives sont limitées à des clones synthétiques temporaires.

## CI observée

[REUSE N01-A2 44181266121](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44181266121) : **SUCCESS au commit `2dd4447a`**. Résultats issus des logs/JUnit : 108 tests JVM, 11 régressions de garde, 10 tests Python historiques, zéro échec/erreur/saut JUnit. Gate M53 et identité des 329 fichiers conservées. Android/LLM/raccordement de production : NOT_RUN.

Le refus historique 42523863724 reste FAILURE, sans nouvelle tentative ni modification de ses preuves. La CI verte du contexte REUSE ne le transforme pas en succès. Un lancement manuel en doublon 44181373764 a été annulé ; le run push de référence est conservé.

Le JVM local n’a pas pu commencer : le wrapper ne résout pas `services.gradle.org` dans cet environnement et le JDK local est 21, contre 17 en CI. Aucune vérification TLS ou réseau n’a été contournée. Les tests Python locaux et la CI JVM sont rapportés séparément.

## Correctif de routage proposé, non appliqué

Le changement minimal de sélection serait de reconnaître explicitement la PR REUSE dans les deux jobs, de contrôler le dépôt/base/head exacts, de tester son SHA de tête plutôt qu’un merge artificiel, puis de choisir un contrôle successeur adapté à REUSE. Les autres routes M50/LOT3/PRE-FUSION doivent rester inchangées.

**Un patch de routage seul ne suffit pas** : modifier `.github/workflows/nex-07.yml` fait échouer la protection M53, comme le démontre le test négatif. Pour l’appliquer, il faut d’abord un accord sur une exception bornée à ce seul fichier et un garde successeur contrôlant son delta exact, tout en conservant les octets/modes des autres fichiers et les gardes historiques à leurs SHA. Aucun joker de chemin, skip ou succès forcé n’est proposé.

La proposition de delta est dans `patches/nex07-routing-proposal.patch`. Elle n’est pas applicable comme livraison autonome et **n’est pas appliquée**. Le garde successeur et son intégration demandent la validation préalable de la modification de protection ; ils ne sont pas introduits subrepticement par A2.

La demande découle de la consigne utilisateur : « Arrêter et demander mon accord si une modification des contrats existants ou des protections historiques devient nécessaire. » Les autres travaux A2 ont été achevés dans leur portée autorisée.
