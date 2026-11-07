# JARVIS V1 Acceleration — M51, audit et coordination

Référence documentaire : cahier des charges du 7 novembre 2026 (46 pages), SHA256 `93cb9f7bb8acf518ea4218ab2db0d450beba8aa14a465760f63a7bac70915c8c`. Dépôt `bubth720/JARVIS-UNIFIED`, branche `codex/m51-unified-gates`, base exacte `a73c1571f3e1dd0acd50e87b9742fbe2214a93d2`, tree `0226f108b72f44ec90a5640b8ca8f77d058fc686`.

UNIFIED conserve les versions, capacités, refus et preuves. **Aucun module runtime raccordé par cette PR.** Le cockpit M51 est développé séparément dans INTERFACE ; ses futurs reçus ne seront pas confondus avec l'inspection des sources UI-01C. Les références historiques restent intactes.

- [Verrou des sources](BASELINE-LOCK.json) et [DAG/compatibilité](DEPENDENCY-DAG.md).
- [Capacités par dimension](CAPABILITY-EVIDENCE.json), [preuves sources](SOURCE-EVIDENCE.json), [gates fermés](GATES.json).
- [Grille 100 points préenregistrée](SCORE.json), [graphique de points non attribués](SCORE.svg).
- [Réception M51](MISSION-51/TECHNICAL-REPORT.md), [décisions](MISSION-51/DECISIONS.md), [rollback](MISSION-51/ROLLBACK.md).
- [Préparation M52](MISSION-52/PLAN.md), [M53](MISSION-53/PLAN.md), [M54](MISSION-54/PLAN.md).

Le score de cette **nouvelle composition non encore reçue** est non attribué (0 acquis ici, 100 à évaluer/bloqués). Il ne dit pas que l'ensemble historique du projet vaut 0 %, ni que les documents ont gagné des points. Une préparation, un mock ou un workflow vert n'accorde aucun critère produit. Les APK/tests finaux du parent seront reliés à leurs SHA effectifs dans le complément de réception, sans remplacer la baseline.

Vérification hors ligne : `python3 -m tooling.v1.validate`, `python3 -m unittest discover -s tooling/v1/tests -v`. Le code refuse les états READY flous, vrais booléens sans preuve, mauvais SHAs, p95 sous 20 essais, confusion émulateur/physique, points documentaires et gate autoproclamé. Il n'a pas le pouvoir d'approuver ou d'exécuter une action sensible.

Les JSON/Liens CI décrivent des observations GitHub à leurs dates et commits. LLM et VOICE conservent des CI historiques FAIL/SKIPPED malgré leurs campagnes dédiées réussies. Aucun clone de poids/profil vocal/asset privé, téléchargement de modèle, mutation de contrat CORE/LLM, migration, installation personnelle, dépense de service ou merge n'a lieu ici.
