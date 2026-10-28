# Revue indépendante du lot3 — 28 octobre 2026

Lecture des diffs et preuves, sans nouveau build ni installation.

- Contrats UNIFIED v1/v2/locks : aucun delta.
- INTERFACE : fichiers historiques de production, dépendances, permissions et assets intacts.
- SERVICES : aucun changement de production; banc dans les sources de tests uniquement.
- NEXUS : modules historiques intacts; packages de tests opt-in, provider testOnly protégé par MANAGE_DOCUMENTS; minSdk24 préservé. TargetSdk35 du seul laboratoire.
- CORE : nouveau port lab non composé dans AppGraph, OFF/UNTRUSTED, canExecute=false et authenticated=false. Aucune identité Android réelle attestée.
- Aucun commit de fusion dans les cinq deltas de branche.
- Les trois APK CORE correspondent aux SHA256 du rapport propriétaire. Aapt confirme indépendamment l'absence INTERNET et ACCESS_NETWORK_STATE.

629 tests CORE =510+53+36+30. Ils s'exécutent sur hôte JVM et incluent Robolectric;
la ventilation quantitative JUnit pur/Robolectric n'est pas établie. Ne pas les
présenter comme une campagne d'émulateur ou une qualification physique.

`origin/main` n'est pas disponible dans les clones mono-branche. Les têtes
principales sont donc contrôlées avec `git ls-remote`, jamais déduites d'un
ref local manquant. Pour INTERFACE, aucune branche main/master n'est publiée;
la HEAD distante annonce development/mission-002. Ces noms sont conservés.

La revue du code ne remplace pas les campagnes Android. Voir LATEST-STATUS.md
pour les échecs préservés, correctifs et résultats sur chaque SHA.
