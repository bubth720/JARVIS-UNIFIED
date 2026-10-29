# JARVIS M50 — État de départ et preuves à produire

**Référence :** 29 octobre 2026, branche `mission/m50-integrated-beta-20261029`, sans merge.
**Jalon M50 : NON ATTEINT.** Les pourcentages du projet global restent non quantifiés, car la V1 finale n'a pas encore un périmètre et un système d'acceptation approuvés.
**Cette fiche ne certifie aucun livrable Android unifié.** Voir `ACCEPTANCE-AND-ROADMAP.md`.

| Gate | Statut actuel | Qui doit prouver quoi |
|---|---|---|
| M50-G1 Provenance | PARTIAL | UNIFIED doit vérifier les huit arbres, licences, Gradle et rapport de convergence ; #16 et #15 sont des branches distinctes |
| M50-G2 APK unique | NOT_RUN | CORE/UI/UNIFIED doivent construire et inspecter une APK-laboratoire réellement combinée |
| M50-G3 Conversation LLM | BLOCKED | LLM JNI/chargement/unload non qualifié sur matériel; aucun faux succès via mock |
| M50-G4 NEXUS documents | BLOCKED | FTS5 API24/25 manquant, sélection/consultation Android source/citations encore non raccordée à CORE |
| M50-G5 SERVICES lecture/CSV | PARTIAL | Outils portables seuls qualifiés; consommation effective par CORE dans la même APK NON DÉMONTRÉE |
| M50-G6 Sécurité/lifecycle | PARTIAL | Rejets synthétiques CORE/ADR-002 acquis, transport externe Android signé ou boundary in-process non intégré |
| M50-G7 E2E Android/offline | NOT_RUN | Les campagnes existantes sont des tests par module, non une application réelle unique |
| M50-G8 Physique/reprise | NOT_RUN | Aucun essai d'appareil personnel, métrique thermique ou migration/restauration de l'application unique |

Les `PARTIAL` ne sont jamais des PASS. Une suite Android d'un producteur ne qualifie pas un consommateur absent. Chaque gate doit avoir un lot et des preuves exactes.

## CI déjà observées à l'ouverture du lot M50 (nouvelles branches documentaires)

- UNIFIED : workflows U01/U02/coordination réussis au SHA du premier dossier ; d'autres jobs étaient en cours lors du relevé. Les résultats du lot4 au SHA antérieur restent distincts.
- INTERFACE et VOICE : workflows Android lancés ; succès d'une exécution initiale, les autres runs doivent être recontrôlés aux SHAs du dernier commit.
- SERVICES/EVOLUTION : jobs lancés, non annoncés verts tant que non terminés.
- **NEXUS** : run `40852579751` FAILURE au SHA `c02a00e8d6829de48a212cc03ac392e7ec73c82c`. Le script historique `check-prefusion.py` a refusé les nombreux fichiers déjà livrés en lot3 ainsi que la mission M50, parce que `LOT3_REVIEW=false` sur une PR dont la base est la branche de développement lot3. Les jobs JVM/Android-host n'ont pas atteint leurs tests produit. **Ne pas désactiver le contrôle ; spécifier une route d'intégration M50 revue avec gel du baseline lot3 et tests positifs/négatifs.**
- **LLM** : run `40852611085` FAILURE sur le garde historique `tools/check-preservation-003e.py` : `Protected baseline drift: app/src/main/AndroidManifest.xml`. La même famille de workflows échouait également sur le SHA de base lot1 `6ae8a4f5c2490f6c9814e08957909a8e3a807180`. Le workflow PRE-FUSION complet du lot1 `40547525669` était SUCCESS au SHA source mais ne remplace pas le contrôle historique et ne qualifie pas M50. **Résoudre le routage/historique sans modifier le manifeste protégé, sans désactiver les garde-fous et sans promettre un gain JNI.**

## Consignes Codex de récupération de CI

1. D'abord consulter les logs exacts et source des validateurs (NEXUS `tools/check-prefusion-lot3.py`, `tools/check-prefusion.py`, `.github/workflows/nex-07.yml` ; LLM `tools/check-preservation-003e.py` et workflows M50/lot1). Repérer quel engagement/branche chaque garde est conçu pour protéger.
2. **Ne jamais modifier un manifeste de production, des tests historiques ou des empreintes/reçus pour obtenir du vert.** Exécuter les anciens gardes à leurs SHAs historiques dans un clone isolé, comme les lots précédents. Concevoir une voie CI *nouvelle et explicitement bornée* pour le nouveau périmètre et tester négativement ses conditions de routage.
3. Les suites d'intégration devront confirmer les deux types de preuves : préservation à l'ancien SHA exact et tests du nouveau contenu M50 au nouveau SHA. Si l'ancien workflow peut rester volontairement rouge hors domaine sans affecter la sécurité, signaler la limitation plutôt que mentir.
4. Publier PR brouillon de correction CI séparée du code d'intégration, chiffres de tests réellement observés, SHA et diff.
5. La décision de construire une APK unifiée et les futures autorisations sensibles restent indépendantes d'une CI documentaire verte.

## Méthode de bilan

À chaque revue : module, mission, SHA source/HEAD/tree, tests JVM/Robo/Android/physique distingués, CI, blocage, rollback et prochain test. Une erreur à l'étape de garde ne vaut pas un échec des tests produit, mais rend le gate global **non validé**.
