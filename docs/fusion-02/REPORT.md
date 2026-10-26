# UNIFIED — FUSION-02 / U0–U5

Branche : `feat/fusion-02-android-first-evidence`.
Base : `3caa57d91ce0dba31043e7cb6373a5e2df8b9fa4`.
Le HEAD est le commit contenant ce rapport, donné exactement dans le compte rendu
final et vérifiable par Git sur la branche publiée.

**Tranche UNIFIED logicielle livrée ; pilote Android global BLOCKED.**
Aucun dépôt applicatif n'est modifié. L'issue directrice#5 et les sept sous-issues
ont été lues intégralement ; audits, SHA, contrats, CI et gates sont actualisés.
La totalité de FUSION-02 n'est pas déclarée DONE.

## Fonctions programmées

- `integration-lock-v2.json`, schéma fermé et CLI v2 : primaire/alternatives,
  versions contrat/ABI/data/minSdk/proof, versions réellement consommées, diff
  FUSION-01→02, sources SHA/parents/hash et matrice des niveaux de preuve.
- Réutilisation des lecteurs et protections F0 : JSON borné/strict, fichiers Git
  réguliers et chemins sûrs, pas de fetch/checkout/commande source externe.
- Refus d'un READY avec CI N/S/CORE non réussie, consommateur non aligné, preuves
  instrumentées24/25 ou scénarios E2E A–J manquants. JVM/Robolectric/API26 ne se
  transforment pas en preuve API24/25 ; les lanes L/V/I/E restent indépendantes.
- Propositions CapabilityStatus/OperationReceipt2-draft et contrôles sémantiques :
  décision au commit, confirmation/hash/destination/génération liés, readback,
  révocation avant/après engagement, ACK perdu UNKNOWN et absence de relance.
  Ce sont des contrats testés **hors runtime, non approuvés**, pas une fence active.
- CI indépendante Python3.12.12 et runner à commandes fixes : résultats réels,
  journaux/stdout/stderr, artefacts même si un check échoue, pas de faux PASS zéro-test.
  Le YAML historique est corrigé sans retirer les147 tests ni la sauvegarde.

## Corrections et faits nouveaux

La CI UNIFIED initiale échouait avant les jobs : annotation GitHub YAML ligne48,
reproduite localement par ScannerError. Les quotes protègent maintenant la commande
pip. Le nouveau workflow est JSON valide YAML1.2, vérifié avec json Python standard ;
les deux workflows ont aussi été analysés avec le parseur déjà disponible localement.
Voir [diagnostic CI](CI_DIAGNOSIS.md) pour les erreurs et reprises propriétaires.

NEXUS a une nouvelle tête `9d6928cd8651f83fa5091bdb474b33761d366412` : schéma4
portable, contrats reader distingués et95 JVM+37 Robolectric **historiques**.
Le diagnostic ancien « finale Kotlin jamais compilée » n'est plus appliqué à
cette nouvelle tête. Android FTS5/instrumentation24–25 restent absents.
CORE36761ce est maintenant CI verte exacte ; LLM e0b781 a un parent de code vert,
non une CI héritée implicitement. UI1d0a89 a sa CI exacte verte, pack privé préservé.
SERVICES reste f000 et son Context snapshot ne résout pas la fence live. CORE
consomme encore NEX777/SERV3de : pas les producteurs primaires Android proposés.
Les références distantes de26 candidats sont revérifiées ; aucune têteFUSION02
applicative n'était publiée au snapshot, aucune donnée privée copiée.

## Tests et limites

Résultats exacts, commandes et plateforme : [VALIDATION.json](VALIDATION.json).
**167 tests distincts réussis, zéro échec/erreur/saut** : 41 audit/contrats +23
registre +32 campagne +30 sauvegarde +21 FUSION-01 +20 FUSION-02. La suite
historique147 est conservée et réexécutée. Les répétitions ne sont pas additionnées.
Le premier passage local du runner avait167 tests verts mais un contrôle de liens
en échec (fichiers de livraison encore absents) ; les fichiers ont été complétés,
puis le runner entier a réussi. Les logs et summaries initial/final sont conservés.
Les contrôles de sources lisent26 références,238 fichiers et5 schémas gelés ;
ce ne sont pas des tests unitaires additionnels. Les tests applicatifs cités dans
les audits sont relus, pas relancés ; aucun nouvel Android/emulateur/téléphone,
SAF provider, FTS5 natif, tokeniseur ou génération n'est exécuté par UNIFIED.

Les tests de contrat ne démontrent pas un fencing concurrent réel, ni l'authenticité
d'une autorisation ou d'un rapport tiers. Les empreintes garantissent des octets,
pas la véracité physique d'une déclaration ; revue et vrais producteurs requis.
Les outils/portraits/voix ne sont pas prétendus intégrés ; SERVICES final reste17
outils distincts, le port24 seulement recherche/CSV, DOCX désactivé.

## Livrables et utilisation

Voir [guide](README.md), [contrats et revue](CONTRACTS.md),
[matrice générée](RELEASE_MATRIX.md), [comparaison](COMPARISON.json),
[provenance](PROVENANCE.json), [runbooks/rollback](RUNBOOK.md).
Les sources machine et audits sont sous `evidence/`. Aucun contrat v1 ou verrou
FUSION-01 n'est réécrit ; aucune dépendance de runtime/cloud ajoutée.

## Publication et prochaine action

Publication uniquement sur branche dédiée, sans force. Main doit rester
`e4435f4bd60c5fdc5595c411cc8cab9da7ef020b` ; SHA distant vérifié au compte rendu.
La CI indépendante a réussi au commit de code
`2fa138c90deab313ab5a6fe880c0b37d37400a54` :
https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/40287363679 (39s).
L’artefact de preuves est présent, digest serveur consigné dans PROVENANCE.json ;
son archive n’a pas été téléchargée/recalculée ici. Les avertissements Node20→24
et migration ubuntu-latest sont conservés, pas supprimés. Ce succès CI est
distinct des167 tests locaux, et n’est pas une qualification Android.
Le commit final de rapport ne reçoit pas automatiquement la CI du parent ;
la conclusion de son propre run est vérifiée séparément dans le bilan final. L'accès API actuel renvoie Forbidden :
PR brouillon non créée ; [texte prêt](PR_DRAFT.md), aucun jeton remplacé ou exposé.

Priorité suivante : NEXUS probe FTS5 instrumentée24/25 et backend autorisé,
SERVICES fence et export SAF réellement vérifiés, puis composition CORE C1 après
réception des deux producteurs. CORE C0/refus peut avancer indépendamment. Les
changements JNI/SQLite natif/signatures/IPC, migrations, installation personnelle
ou distribution nécessitent une décision distincte. Aucun merge/activation
sensible, seuil matériel modifié, asset privé publié ou donnée réelle migrée.
