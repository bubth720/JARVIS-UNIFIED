# CODEX — JARVIS LOT 4 / UNI-PF-03
## Traduire les principes ADR-002 approuvés en contrats testables, sans raccordement réel

**Emplacement de mission :** `bubth720/JARVIS-UNIFIED`,
`mission/adr002-principles-lot4-20261028`,
`missions/LOT4-ADR002-UNI-PF-03.md`.

**Décision approuvée et enregistrée :**
`docs/DECISIONS/ADR-002-PRINCIPLES-APPROVED-2026-10-28.md` sur
cette même branche. La validation concerne **trois principes de conception
uniquement**, et ne permet pas de mutation, transport ou fusion.

**Base UNIFIED vérifiée :**
`4fa55d468228a6f222f6177e807938660d735a8c`;
lot3 `codex/prefusion-lot3-unified` et
CI `40755167508` SUCCESS au SHA. Ne pas déduire des tests du lot3
qu'un contrat de mutation est approuvé.

## Ordre et délégation

1. CORE / CORE-PF-03 :
   https://github.com/bubth720/JAVIS-Local-v2/blob/mission/adr002-principles-lot4-20261028/missions/LOT4-ADR002-CORE-PF-03.md
   Base `aed84860f2ca85713140a687ba7d86efc0203dc8`.
   Propriétaire de la session, consentement unique et révocation.
2. SERVICES / SERV-PF-03 :
   https://github.com/bubth720/JARVIS-SERVICES/blob/mission/adr002-principles-lot4-20261028/missions/LOT4-ADR002-SERV-PF-03.md
   Base `cfb5f117edc72acd8d5967980d3dfc9dfbf2903f`.
   Simulateur à deux journaux, crash matrix, inspect UNKNOWN sans effet.
3. UNIFIED / UNI-PF-03 :
   ce document, exécuter **après lecture des rapports propriétaires**
   la réconciliation de versions/états et les validateurs purs.

**CORE et SERVICES peuvent être développés en parallèle** sur leurs branches.
Aucun agent ne doit modifier le dépôt d'un autre module pour gagner du temps.
UNIFIED conserve la proposition sans activer les ports.

## Mission UNIFIED

### U0. Inventaire et fausses équivalences
Consulter `workspace/modular-workspace.proposed.json`,
`docs/prefusion/lot3/CONTRACT-MATRIX.md`,
`docs/prefusion/lot3/ADR-002-PROPOSED.md`,
`docs/uni-08/ADR-002-PROPOSAL.md`,
`tooling/integration/uni08_u01.py` et tous les tests existants.
Vérifier refs/têtes/CI et comparer à l'approbation **limitée** de la
décision. Le plan de workspace demeure `approved:false`,
`runtime_enabled:false`, `android_multi_module_go:false`.

### U1. Spécification candidate D1
Préparer contrat lisible par humains et validateurs hors ligne :
CORE seul peut autoriser au point d'engagement sur un preview exact et
identité attestée; session, request, epoch, generation bornée,
nonce unique, deadline monotone, révision de politique, source/destination
et digests. La version est explicite, les champs inconnus refusés.
Aucune identité UID/CERT n'est inférée d'un UUID ou d'un callback fourni
par l'appelant; `authenticated` reste faux dans le laboratoire.

### U2. D2 : identifier toutes les fenêtres de crash
Créer matrice des séquences CORE↔SERVICES et une machine pure de vérification
en lecture seule, **sans rendre le journal mémoire du banc durable par décret**.
Refuser équivalences de statuts, génération 0 et promotion d'un ACK.
Rapporter l'impossibilité de transaction atomique prouvée entre deux
journaux indépendants. Proposer conditions supplémentaires nécessaires
pour choisir un protocole durable ultérieur.

### U3. D3 : fail-closed / UNKNOWN
Tester que toute perte d'ACK, relecture partielle, fermeture incertaine,
conflit de digest, révocation ou erreur de consentement bloque mutation et
retry. L'outil diagnostique ne peut que noter des preuves de lecture
correspondantes ou non; jamais effacer un journal, désactiver une garde
ou promettre rollback d'octets déjà écrits.

### U4. Traçabilité et qualification
Écrire sous `docs/prefusion/lot4/` :
- `CONTRACT-CANDIDATE.md` : distinction acceptation de principe /
  champs et version encore proposés;
- `CRASH-WINDOWS.md` : matrice coupure / réaction attendue;
- `GATES.md` : preuve CORE, SERVICES, UNIFIED, Android et tests physiques,
  bloqueurs et statut `NOT_RUN` si besoin;
- `REPORT.md` : module/mission/branche/SHA/CI/tests/échecs/rollback.

Ajouter des tests de négociation en Python qui refusent :
génération 0, génération >2^53−1, contexte incomplet, replay,
état fabriqué, UNKNOWN→COMMITTED sans attestation, booléen
`authorized:true` dans un payload, ID de source changeant, version
inconnue, séquences de journaux incompatibles. Garder la proposition
**fail-closed et sans connecteur Android**. Ne modifier aucun contrat
UNIFIED existant ou hash gelé.

### U5. Exécution et revue
Relancer au SHA exact :
`python3 workspace/check_plan.py workspace/modular-workspace.proposed.json`
`python3 -m unittest discover -s workspace/tests -v`
`python3 -m unittest discover -s tooling/integration/uni08_u01_tests -v`
plus les suites U00/UNIFIED disponibles documentées dans le dépôt.
Nouveaux tests négatifs séparés. Relever tests ignorés/non lancés.
Créer PR **brouillon vers la branche de mission**, pas vers main.

## Critères d'acceptation

- D1/D2/D3 explicites et traçables à la décision utilisateur;
  aucune approbation implicite du format final de transport/wire.
- Registre des états distingue `DISPATCHED` et
  `COMMIT_STARTED`, `COMPLETED` et `COMMITTED`; pas de
  generation0→1 implicite.
- Toute incertitude est bloquante, diagnostics en lecture seule;
  pas de mutation, migration, installation ou connexion réelle.
- Un seul CORE arbitre; SERVICES ne se délivre aucune permission;
  suppression du port CORE entraîne refus.
- Pas de merge main, pas de changement de default branch,
  pas de modification d'APK personnelle ou de dépôt d'un autre owner.
- Rapport critique honnête sur ce qui reste nécessaire pour un
  **pilote Android intermodules** : UID/certificat, liaison de
  permission, journal durable, source NEXUS et FTS5, SAF, JNI,
  collecte de preuve Android et validation physique.
- Si une étape requiert signature/binder, nouveau backend natif,
  choix définitif du commit ou écriture réelle : **STOP, demander
  une approbation spécifique**, puis reprendre sur branche dédiée.

## Message de lancement Codex

Dans JARVIS-UNIFIED, branche mission/adr002-principles-lot4-20261028,
lis missions/LOT4-ADR002-UNI-PF-03.md. Lis la décision ADR-002
enregistrée, puis les deux missions CORE/SERVICES liées. Exécute
les travaux de laboratoire non sensibles sur branches dédiées,
avec tests et PR brouillon. Aucun raccordement réel, aucune
écriture, aucune migration, aucun merge main. Rends un bilan
précis et arrête-toi aux gates qui exigent mon accord.
