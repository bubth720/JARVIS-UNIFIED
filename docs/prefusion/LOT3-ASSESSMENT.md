# Lot3 — pré-intégration contrôlée

Observation : 28 octobre 2026 UTC. UNI-PF-02, branche
`codex/prefusion-lot3-unified`, base mission
`e4c678faf630a0a98adfaecd7a87fc11dfd82486`, arbre initial
`d9274d820c9bcf46fe580bb13149371af31d509d`.
Code initial f057ced917c1b49467b93eb462c774bf4e812957; correction CI
3bacb70e32e3909ba154cfe6d57da0812dd7d9cf (run40665265643 SUCCESS).
Le SHA livré et son arbre s'obtiennent avec `git log -1 --format='%H %T'` sur la
branche publiée; ce document ne fabrique pas un SHA autoréférentiel.

## État le plus récent

La [mise à jour de reprise](lot3/LATEST-STATUS.md) complète les premières
captures ci-dessous : SHA propriétaires, campagnes Android et corrections CI.
Les anciens résultats restent datés et ne sont pas réattribués aux nouveaux SHA.

## Travaux communs livrés

- [Audit des huit PR précédentes](lot3/PR-AUDIT.md), [données vérifiées](lot3/PR-AUDIT.json) : tête, base, arbre, diff et CI accessibles. Les huit restent Draft. L'association UNIFIED#10/b8f22 est confirmée. Les CI liées seulement au numéro de PR demeurent UNKNOWN sur le SHA exact.
- [Matrice candidate](lot3/CONTRACT-MATRIX.md), frontières SDK, identité et responsabilités. Aucun schéma v1/v2 ni lock historique changé.
- [Trois décisions ADR-002 proposées](lot3/ADR-002-PROPOSED.md), aucune approbation ni écriture réelle déduite.
- Vérificateur exécutable de transcriptions TXT/CSV synthétiques : source/digest → demande étiquetée CORE → ACK_UNTRUSTED → NEXUS UNSUPPORTED → INTERFACE UNAVAILABLE. Il refuse faux READY, provenance supplémentaire, citation inventée, identité payload, replay, mauvais epoch/session/génération. Ce n'est pas un adaptateur Android ni un test E2E des quatre modules.
- Workflow de régression lecture seule et garde d'allowlist. Les instantanés antérieurs restent datés et intacts.

## Validation UNIFIED réellement exécutée

Hôte Linux, Python standard et dépendance cryptography existante. **251 tests
réussis, 0 échec, 0 erreur, 0 saut** : 167 régressions historiques +23 U00 +23 U01
+20 U02 +18 nouveaux. Les 12 entrées du runner historique réussissent
(6 suites et 6 validateurs). Le manifeste U02 demeure REVIEW_ONLY, zéro lien
runtime et aucune APK unifiée qualifiée. Les deux fixtures CLI donnent
UNSUPPORTED/UNAVAILABLE, aucune mutation ni confiance accordée.

Commandes depuis la racine :

```sh
python3 -m tooling.integration.ci --output /tmp/lot3-unified-validation
python3 -m unittest discover -s tooling/integration/uni08_tests -v
python3 -m unittest discover -s tooling/integration/uni08_u01_tests -v
python3 -m unittest discover -s workspace/tests -v
python3 workspace/check_plan.py workspace/modular-workspace.proposed.json
python3 -m tooling.integration.uni08_candidate docs/uni-08/BOM-PROPOSED.json
python3 -m unittest discover -s tooling/integration/prefusion_lot3_tests -v
python3 -m tooling.integration.prefusion_lot3 docs/prefusion/lot3/txt.json
python3 -m tooling.integration.prefusion_lot3 docs/prefusion/lot3/csv.json
python3 scripts/check_prefusion_lot3.py
git diff --check
```

[Résumé machine et commandes exactes](lot3/VALIDATION.json). Instrumentation locale
NOT_RUN : pas de /dev/kvm. Aucun appareil personnel, modèle ou profil privé testé.

## Livraisons propriétaires

Les branches de travail sont toutes issues de la branche de mission de leur
propriétaire, sans fusion. Les résultats finaux sont consignés dans
[OWNER-RESULTS.md](lot3/OWNER-RESULTS.md); ne pas assimiler compilation d'APK,
Robolectric, JVM et exécution instrumentée.

## Publication et retour arrière

Les pushes Git dédiés restent possibles. Création de PR par API refusée :
`Post "https://api.github.com/graphql": Forbidden`, observée sur INTERFACE.
`api.github.com` absent des destinations réseau autorisées; aucune extraction de
jeton, changement de proxy ni tentative répétée. Une création de PR n'est donc
pas revendiquée. Corps prêt dans [PR-BODY.md](lot3/PR-BODY.md).
Sur GitHub, ouvrir Compare, base `mission/prefusion-lot3-20261027`, compare
`codex/prefusion-lot3-unified`, puis **Create draft pull request**.
Un brouillon de configuration cloud a aussi été sauvegardé : instructions de
reprise de la chaîne testée et ajout proposé du seul domaine `api.github.com`.
Il ne modifie pas le réseau actuel : examiner/enregistrer puis publier dans les
paramètres de l’environnement pour l’appliquer; les droits API restent à vérifier.
Les propriétaires utilisent la même base et leur branche `codex/prefusion-lot3-*`.
Aucune fusion demandée. Pour débloquer l'API dans Codex, autoriser
`api.github.com` dans les paramètres réseau de l'environnement, puis vérifier
l'accès et les droits effectifs; un accès Git ne prouve pas un droit API.

Rollback : rester sur la branche de mission initiale; aucun runtime de production
n'est activé par ces ajouts. Ne supprimer ni réinitialiser des travaux existants.
`main` UNIFIED reste `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b` lors du contrôle.

## Corrections et limites conservées

Le premier workflow UNIFIED a échoué avant tout job : sélecteur pip contenant
`:` non cité en YAML. Correction publiée et CI suivante verte; l’échec initial
40665128398 n’est ni supprimé ni compté comme un test exécuté.
Les premières campagnes INTERFACE et NEXUS ont eu de vrais échecs Android.
La mise à jour finale décrit leurs causes, corrections et campagnes ultérieures
vertes sur les SHA exacts; les échecs antérieurs restent dans les preuves.

## Gates et décisions avant un autre lot

- CORE/UI : LAB UNTRUSTED, aucune attestation Android UID/signature réelle.
- SERVICES : ADR-002 non adoptée, aucune écriture SAF réelle, UNKNOWN bloque.
- NEXUS : FTS5/SAF sur anciens Android à qualifier; aucun backend natif ajouté.
- LLM/VOICE : fin native et unload restent distincts; pas de preuve JNI nouvelle.
- EVOLUTION : sandbox non qualifiée; aucun correctif appliqué.
- Physique et E2E multi-APK : NOT_RUN. Aucune APK unifiée disponible.

Prochaine action : examiner les campagnes propriétaires sur leurs SHA exacts,
traiter leurs échecs sans activation, puis décider les trois points ADR-002 et les
conditions de confiance CORE/UI avant tout raccordement sensible.
