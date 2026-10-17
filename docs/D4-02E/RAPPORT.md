# UNIFIED — D4-02E : revue de clarification livrée

**Proposition technique D4-02E.1 à valider, pas un bundle LLM approuvé.**
Issue : https://github.com/bubth720/JARVIS-UNIFIED/issues/2, lue intégralement
HTTP200, updatedAt2026-10-17T12:38:25Z. Date de mission17 octobre2026.
Branche `design/d4-02e-f1-f2-recovery-clarification` ; base
**1748cb0706fa4b0cfac2df963d82a14195b9d25a**, dérivée documentaire explicite
de27e6740 via8ddac8f et ID-001db63719 ; conserve les décisions et livraisons sans merge.
SHA final donné dans la livraison Git ; pas d’auto-référence de commit inventée.

## Livrables et conclusion

- [DECISIONS_F1_F2.md](DECISIONS_F1_F2.md) : provenance authentifiée des epochs et
  propriété séparée des journaux, correction des ambiguïtés D4-02D reconnue.
- [COMMIT_CANONIQUE.md](COMMIT_CANONIQUE.md) : deux preuves complètes, formules
  exactes, records/outboxes non auto-référents, fsync et ACK perdu.
- [CONTRAT_DIFF_PROPOSE.md](CONTRAT_DIFF_PROPOSE.md), [tables](TABLES_PROPOSEES.json)
  et [diff](TABLES_DIFF.json) : champs/enums/tailles/AIDL et refus exacts à revoir.
- [MISSIONS_CORRECTION_003F.md](MISSIONS_CORRECTION_003F.md) : corrections futures
  F1/F2/COMMIT, port F3 minimal et gate de revue avant toute consommation CORE.
- [Vecteurs synthétiques](vectors.json) et [vérificateur offline](verify_vectors.py).

L’ambiguïté F1 est levée dans la proposition par DISCOVER11champs ; F2 par SNAPSHOT
LLM seul et preuve CORE séparée. L’appartenance COMMIT est vérifiable à partir des
deux preuves et de leurs correspondants authentifiés conservés localement. Les
hashes ne remplacent pas l’authentification ni l’inspection native. F3 est spécifié,
**non codé** ; les cas irréconciliables restent UNKNOWN.

## Sources immuables lues et contrôlées

LLM003F **111be993e970051686bd5c27b3115320513a4be7** :

- [RAPPORT](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/docs/mission-003f/RAPPORT.md),
  [GUIDE-CORE](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/docs/mission-003f/GUIDE-CORE.md),
  [PREUVES](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/docs/mission-003f/PREUVES.md).
- [CONTRACT](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/fixtures/p2-contract/CONTRACT.txt),
  [TABLES](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/fixtures/p2-contract/TABLES.json),
  [SHA](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/fixtures/p2-contract/CONTRACT.sha256),
  [autorité](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/ProcessRecoveryAuthority.kt),
  [journal](https://github.com/bubth720/JARVIS-LLM/blob/111be993e970051686bd5c27b3115320513a4be7/fixtures/p2-endpoint/src/main/java/fr/jarvis/fixture/llm/RecoveryJournal.kt).

CORE004C **da40ed7155409b85860a22c1dbbfe35029cea29a** : contrats, admission,
journaux et guides lus dans les audits précédents, puis session/contrat relus aux
mêmes objets : [InferenceContract](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/app/src/main/java/com/stark/jarvislocal/InferenceContract.kt),
[SessionCoordinator](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/app/src/main/java/com/stark/jarvislocal/SessionCoordinator.kt).
Accords et quatre documents D4-02D intégralement lus et conservés.

Bundle candidat recalculé depuis CONTRACT+TABLES+AIDL triés :
**4b4129b595b78481d846c521993026fe2477c64fccfe4259ba9a5e30f9d68e62**,
conforme à la référence ; pas accepté comme solution. Source testée
b2f6bc052871a2e4f604d9170f385b71c241837b →111be99 : code/contrat inchangés.
[Run39031742868](https://github.com/bubth720/JARVIS-LLM/actions/runs/39031742868)
consulté HTTP200 : Status Success, SHA testé complet présent. Les157 JUnit,
CTest et JNI Linux/GGUF sont **rapportés par PREUVES** ; logs/XML non téléchargés
ou rejoués ici. Aucun bootstrap Android positif ni preuve physique déduit de cette CI.

## Vérifications réellement exécutées

Linux x86_64, Python3.12.14 ; scripts/tests historiques inchangés :

```text
python3 -m unittest discover -s tests -v                 27 tests OK
python3 -m unittest discover -s registry/tests -v        23 tests OK
python3 -m unittest discover -s backup_prototype/tests -v 30 tests OK
python3 scripts/validate_unified.py
{"contracts": 5, "invalid_examples_rejected": 5, "repositories": 9, "valid_examples": 5}
python3 registry/scripts/update_registry.py --validate-only
Registre valide : 9 dépôts, 16 missions.
python3 docs/D4-02E/verify_vectors.py
11 contrôles OK ; android_or_native_proof=false
```

**80 tests réussis, aucun échec/erreur/saut** ; tous codes retour0. Les onze contrôles
de vecteurs incluent encodeurs indépendants, ordre, Unicode et mutations/proof local
incorrect ; pas des tests Binder/natif ni approbation d’un codec Android.
Sorties complètes ignorées dans `.audit-cache/unified-two-missions/d4-02e/` ;
liens source/empreintes vérifiés localement, git diff --check requis avant commit.
Aucun changement CORE/LLM, Android, contrats UNIFIED v1, seuils ou données. Aucun APK,
modèle, E2E Android, installation, migration, reset, nouvelle génération ou fusion.
README référence ce dossier ; fichiers ajoutés uniquement sous docs/D4-02E/.

## Blocages et prochaine action

Valider D4-02E.1 puis corriger LLM003F et produire nouveau SHA/bundle réellement
testé ; revoir exactitude des tables, appartenance de preuves, points durables,
F3 et refus. **CORE004D reste bloquée jusqu’à revue réussie de ce nouveau bundle.**
Le gate IDENTITY ID-002 est distinct et inchangé. Rien n’est fusionné dans main ;
publication seulement sur branche dédiée, PR non nécessaire et non créée ici.
