# U4 — propositions, compatibilité et frontière d'engagement

Statut : **PROPOSÉ / NON APPROUVÉ / AUCUN CONSOMMATEUR ACTIVÉ**.
Les contrats `contracts/v1` et le draft FUSION-01 restent inchangés. Les deux nouveaux
schémas sont séparés, version `2-draft`, avec exemples synthétiques valides/invalides
et vérificateurs sémantiques Python. Ils ne constituent ni protocole IPC ni nouvelle
source d'autorisation. Leur adoption nécessite diff/revue/version négociée dans les
modules propriétaires ; aucune migration de base n'est réalisée.

## CapabilityStatus : disponibilité du produit, pas état d'un collecteur

[Schéma](proposals/capability-status.schema.json),
[valide](proposals/capability-status.valid.json), [invalide](proposals/capability-status.invalid.json).

Module/build exact, capacité, cible (API exacte), `READY/UNSUPPORTED/UNKNOWN/BLOCKED`,
raison fermée et identifiants de preuves. READY exige une CI sélectionnée réussie,
des preuves correspondant au même module/SHA/capacité/cible et un vrai driver
instrumenté pour Android. JVM/Robolectric ne deviennent jamais instrumentation ;
API26 n'est pas API24/25, ni un émulateur un téléphone. La lecture Git vérifie les
empreintes des fichiers cités ; elle ne fabrique pas les résultats des producteurs.
`CollectorStatus.READY` EVOLUTION signifie seulement collecte activée et n'est donc
pas convertible en disponibilité produit. Statuts natifs UNKNOWN restent bloquants.

La matrice v2 garde séparés `JVM_PASS / ANDROID_EMULATOR_PASS / ANDROID_DEVICE_PASS /
END_TO_END_PASS`, avec driver, cible, scénario, SHA et empreinte de preuve. Le GO
expérimental Android concerne seulement CORE/NEXUS/SERVICES et les scénarios A–J
sur API24/25 ; LLM/VOICE/INTERFACE/EVOLUTION ne deviennent pas prérequis artificiels.
Les autres plateformes restent non qualifiées sans preuves distinctes. Un GO de
revue n'accorde aucune installation, distribution, signature, IPC ou permission.

## OperationReceipt : effet confirmé, refus et incertitude

[Schéma](proposals/operation-receipt.schema.json),
[valide](proposals/operation-receipt.valid.json), [invalide](proposals/operation-receipt.invalid.json).

- Identité : UUID session/request, génération1..2^53−1, séquence croissante.
- Liaisons immuables : digest SHA-256 de l'opération/aperçu exact et destination,
  référence de nouvelle destination et confirmation exacte unique. Le hash doit
  porter les octets effectivement approuvés, pas une représentation reformatée.
- États : PREPARED, DISPATCHED, COMMITTED, UNKNOWN. COMMITTED exige décision GRANTED,
  confirmation consommée, effet CONFIRMED, digest des octets de sortie et relecture
  vérifiée. Une ouverture/flush/retour de fonction n'est pas cette preuve.
- Décision : `authorization_at_commit`, `permission_generation`, effet NONE/STARTED/
  CONFIRMED/UNKNOWN. DENIED ne peut annoncer d'effet démarré. Après décision GRANTED,
  un reçu suivant ne réécrit pas sa génération ni son résultat historique.
- ACK perdu : UNKNOWN, pas succès ni relance automatique. COMMITTED et UNKNOWN sont
  terminaux pour ce protocole ; une réconciliation exige une nouvelle revue explicite.
  Relire exactement le même reçu est idempotent et n'autorise aucune réexécution.
- Révocation après engagement : peut coexister avec un effet confirmé et un avis
  PERMISSION_REVOKED ; pas de promesse d'effacement d'octets déjà confiés au provider.

Le reçu actuel CORE `core.workflow-receipt/1` possède COMPLETED/REFUSED, sans preuve
atomique worker ni digest cible/readback durable. **COMPLETED ne se renomme pas en
COMMITTED.** Préserver l'ancien reçu ; produire une vue marquée historique/non
qualifiée, ou UNKNOWN si l'issue est incertaine. Ajouter une table/version nouvelle
sur copies synthétiques seulement après revue ; pas de migration utilisateur.
Une référence UUID ou digest n'authentifie ni appelant ni confirmation.

## Point de linéarisation proposé : à arbitrer CORE + SERVICES avant runtime

1. CORE possède la session, la génération live et la décision. L'aperçu exact lie
   opération, digest des octets, destination neuve, version et expiration.
2. Juste avant l'effet, SERVICES demande un `authorizeAtCommit` à cette autorité.
   La comparaison génération/consentement et consommation unique doivent partager
   le même point de décision sérialisé que la révocation, pas un Context copié.
3. Révocation gagnant avant ce point : DENIED/NONE, aucun effet. SERVICES n'ouvre
   pas la destination en écriture et journalise le refus.
4. Engagement gagnant : reçu durable/confirmation consommée avant écriture, worker
   unique ; une révocation ultérieure arrête les nouvelles admissions mais ne
   promet ni rollback du provider ni retrait des octets déjà écrits.
5. Fermeture + ACK + relecture exacte : COMMITTED si tout est observé ; sinon
   UNKNOWN, journal conservé, source intacte, aucune relance aveugle.

Un crash entre décision et écriture, une destination ambiguë, un ACK trompeur ou
un journal corrompu ne se résolvent pas par reset. Les producteurs doivent faire
les tests à barrières de concurrence avant/après engagement et les essais SAF
instrumentés ; les tests de transitions UNIFIED **ne prouvent pas cette race résolue**.
Les budgets de schéma/JSON (2MiB pour le verrou, UUID, hash64, listes bornées)
ne changent aucun seuil RAM, batterie, thermique ou contexte.

## Écarts préservés et revues demandées

- CORE consomme toujours NEX777/SERV3de ; nouvelle compilation requise avant les
  ports primaires NEX9d/SERVf000. Pas de substitution binaire ou d'ABI imaginée.
- SERVICES Context snapshot n'est pas un contrôle live ; DOCX API24 reste désactivé.
- NEXUS portable v4 est maintenant testé sur JVM ; il serait faux de conserver
  le diagnostic ancien « Kotlin final jamais compilé » pour ce nouveau SHA. FTS5
  et instrumentation API24/25 restent toutefois absents.
- EVOLUTION métriques camelCase flottantes/bornes diffèrent du draft technique
  UNIFIED ; pas de conversion implicite ni d'observateur connecté.
- LLM client passif et UI premium ne sont pas raccordés au pilote ; ni portraits
  privés ni voix/poids ne sont copiés. Rig articulé et phonèmes ne sont pas livrés.

Accords distincts : adoption runtime de la fence/contrats, SQLite natif externe,
JNI/admission, signatures/permissions, IPC sensible, migration réelle, distribution
ou installation personnelle. L'orientation ADR-001 reste approuvée, inchangée.
