# F01-CONTRACTS-AND-INTEGRATION-GATES — rapport

```text
MODULE : UNIFIED (coordination) + contrôles en lecture seule de CORE, LLM, VOICE, NEXUS, INTERFACE, SERVICES, EVOLUTION
MISSION : FINAL-01/F01-CONTRACTS-AND-INTEGRATION-GATES
DÉPÔT : bubth720/JARVIS-UNIFIED, branche ccr-e05fe51e-ycqubx
  base a9098df22148f96d8f22dd80f6d28b46697c73ba (F00)
  outillage dce5a2a65177adf0f8ea62780f388121987bac02 (+ ce rapport)
INTERFACE : ccr-e05fe51e-ycqubx @ 4e140c0 (arbre identique à S04 e6489bf ; essai de workflow 8ae1f87 annulé par revert)
PR : aucune créée (liste proposée : R01-REVIEW-PR-PROPOSAL.md)
STATUT : DONE_EVIDENCED pour F01 (porte GO). Mises à niveau d'épinglage : NO-GO (preuves manquantes nommées).
```

## 1. Compatibilité réelle : version embarquée → dernière candidate

| Module | Embarqué (APK S04) | Candidate | Code compilé dans l'APK | API publique | Tests | Verdict de mise à niveau |
|---|---|---|---|---|---|---|
| CORE | `5da98383` | aucune plus récente (= tête de la PR #27) | — | — | CI `UNKNOWN` (API CORE non rattachée) | Inchangé |
| LLM | `2e011776` | `9c3fc500` (A-002) | **DROP_IN** : 8 fichiers natifs verrouillés identiques (blob et taille) | IDENTICAL 302/302 | CI 43625706542 PASS | **NO-GO** : verrou V1 figé (exception propriétaire) et émulateur `NOT_RUN` |
| LLM | `2e011776` | `61ae3a4b` (référence du document de mission) | **NOT_DROP_IN** : ligne divergente, 5/8 fichiers natifs différents | — | — | **Ne pas embarquer** (vérificateur F3B, CI seulement) |
| VOICE | `92d07453` | `58907351` (A-003), `cb32fbbd` (M55-A P2) | **DROP_IN** : arbre `pocketRuntime` identique | IDENTICAL 445/445 | CI 43625576432 PASS | **NO-GO** : verrou V1 figé et émulateur `NOT_RUN` |
| NEXUS | `06ccf98a` | `5f101934` (N01-A3) | 1 fichier source modifié en 27 commits : `SelectedDocumentImporter` (refus > 2 Mio avant ouverture du fichier) ; **non appelé par V3** | IDENTICAL 545/545 | JVM **92/92** sur les deux SHA ; **APK construit** (63/63 tests unitaires, Lint, inspection PASS) ; seule entrée différente : `classes10.dex`, classes modifiées limitées à `fr.jarvis.nexus.android` | **NO-GO** : campagne émulateur avec la candidate `NOT_RUN` |
| SERVICES | non embarqué | `8d80d09d` (M50) et `d16dd84f` (final), lignes divergentes | — | — | JVM `NOT_RUN` (Maven Central 429 depuis ce conteneur) ; CI 40852606525 PASS à `8d80d09d` | Réconciliation en F07 |
| EVOLUTION | non embarqué | `c4abfb03` | — | — | 51/51 en local (F00) | F08 |

**Point de blocage structurel.** Les épinglages LLM et VOICE sont verrouillés dans `labs/v1/sources.json`, qui fait partie de la livraison V1 figée (garde de 430 fichiers). Les mettre à niveau exige **ton exception explicite** sur ce verrou, ou un verrou successeur propre à V3. Je n'ai rien modifié.

## 2. Gardes historiques (R-07) — chacun rejoué sur son commit de référence

| Garde | Commit | Résultat |
|---|---|---|
| V1, 430 fichiers figés (`check_scope.py`) | INTERFACE `e6489bf` | PASS |
| Réutilisation byte-identique et VOICE épinglée (`check_reuse.py`) | INTERFACE `e6489bf` + VOICE `92d0745` | PASS |
| Sources exactes et LLM A02 vérifié (`prepare_sources.py`) | `e6489bf` / CORE `5da9838` / LLM `2e01177` | PASS |
| Mémoire CORE byte-identique (`prepare_core_memory.py`) | CORE `5da9838` | PASS |
| **Préservation de campagne G02** (`test_campaign_preservation`) | INTERFACE `8ae1f87` | **FAIL, comme conçu**. Le garde a refusé mon ajout d'entrées `nexus_ref` / `build_only` dans le workflow (run 44896807860). Changement annulé (`4e140c0`), garde intact. |
| Préservation de campagne G02 | INTERFACE `4e140c0` | PASS (local) |
| Préservation B0 | UNIFIED `f1f30dc` (sa tête) | PASS sous 3.12 (non rejoué sur les descendants, R-07) |

## 3. Livrables

| Fichier | Contenu |
|---|---|
| `tooling/final01/api_surface.py` | API publique d'un module à un SHA et diff (IDENTICAL, ADDITIVE ou BREAKING_CANDIDATE) |
| `tooling/final01/candidate_check.py` | Une candidate remplace-t-elle exactement la version embarquée, d'après le verrou V1 (sans le modifier) ? |
| `tooling/final01/gonogo.py` | Porte stricte : seul `PASS` au SHA complet compte |
| `tooling/final01/tests/` | 17 tests, positifs et négatifs |
| `f01/gates/*.requirements.json`, `evidence.json`, `*.verdict.json` | Exigences par lot, preuves sourcées, verdicts calculés |
| `f01/ADR-F01-01-CORE-ORCHESTRATOR.md` | CORE orchestrateur unique ; migration M0–M5 avec parité et retour arrière |
| `f01/R01-REVIEW-PR-PROPOSAL.md` | 7 PR de revue proposées (P1–P7), têtes et bases exactes ; aucune créée |
| `f01/R02-PR-CLASSIFICATION.csv` | 113 PR ouvertes : 91 remplacées (dont 90 maillons), 8 à conserver, 6 à finaliser, 5 à archiver après validation, 3 bloquées |
| `f01/R11-ARCHIVE-PLAN.md` | Plan d'archivage par étiquette ; aucune suppression |
| `f01/DEVICE-01-SIMPLE.md` | Protocole téléphone en 11 étapes |

## 4. Commandes réellement exécutées

Environnement : conteneur Linux ; Android SDK 35, NDK 28.1.13356709, CMake 3.22.1 et JDK 17 installés dans le conteneur ; Gradle 8.14.3 (la CI utilise 8.13).

- `python3 -m pytest tooling/final01/tests` → **17 passed** au SHA `dce5a2a6`.
- `python3 -m tooling.final01.api_surface <repo> <pin> <candidat> <racines>` (×4) → IDENTICAL.
- `python3 -m tooling.final01.candidate_check --lock labs/v1/sources.json …` (×6) → voir §1.
- `gradle test` NEXUS à `06ccf98` puis `5f10193` → 92/92, 92/92. SERVICES → `NOT_RUN` (429).
- Préparation reproduisant la CI : `check_scope`, `check_reuse`, `prepare_sources`, `prepare_core_memory`, `prepare-native.sh` (llama.cpp `1b70350`), `prepare_whisper.sh` (whisper.cpp `9386f23`).
- `gradle -p labs/v3 … :app:testDebugUnitTest :app:assembleDebug :app:assembleDebugAndroidTest :app:lintDebug` avec NEXUS `06ccf98`, puis `5f10193` (`--rerun-tasks`) → BUILD SUCCESSFUL ×2, 63/63 tests unitaires ×2.
  - APK de référence : SHA-256 `9edb59b41cdf9b6af524b39b35852a55342629e9d91720185c722f9de386ca2b`.
  - APK candidate : SHA-256 `0bdf5d983d8513651480cd79fb7e2b71979eb52c4c2163e7a3174239606be085`.
  - Ce sont des APK de laboratoire **non publiés et non signés**.
- `python3 -m tooling.final01.gonogo` (×4) → F01 GO ; PIN-NEXUS, PIN-LLM et PIN-VOICE NO-GO.

## 5. Non testé

- Campagne émulateur avec une candidate : pas de KVM ici, et la CI refuse un changement d'épinglage (garde G02).
- Tests JVM de SERVICES en local (429).
- CI de CORE (`UNKNOWN`).
- Tout essai sur appareil.

## 6. Risques de régression

- **Nuls à ce stade** : aucun épinglage, aucun runtime et aucun garde modifié ; l'arbre INTERFACE est identique à S04.
- **À la future mise à niveau NEXUS** : seul `SelectedDocumentImporter` change, et il n'est pas appelé par V3. Risque faible, mais à prouver sur émulateur.

## 7. Décisions demandées

1. **Exception G02.** Autoriser un mode de test de candidate dans le workflow V3 (entrée manuelle, valeurs par défaut inchangées), pour exécuter la campagne émulateur avec NEXUS `5f10193`. C'est indispensable pour PIN-NEXUS.
2. **Verrou V1.** Pour LLM et VOICE : exception sur `labs/v1/sources.json`, ou création d'un verrou successeur `labs/v3/sources.json`, avec le V1 conservé intact.
3. **Accès CORE.** Il ne m'est pas possible de rattacher CORE moi-même : la demande a été refusée par le contrôle d'accès de la session. Toi, ajoute `bubth720/JAVIS-Local-v2` aux dépôts de cette session ou de son environnement (paramètres Claude Code → Repositories), ou installe l'app GitHub Claude sur ce dépôt. Sans cela, CORE reste `UNKNOWN`.
4. **R-01.** Validation de la liste P1–P7 avant toute création de PR.

## Erratum F00

INTERFACE n'a **pas** de branche `main` ; sa branche par défaut est `development/mission-002` (`d1c0931`). La colonne `in_main` de `PR-INVENTORY.csv` pour INTERFACE vaut donc « faux » **par absence de `main`**, et non après vérification. Aucune décision F00 n'en dépendait : aucune PR INTERFACE n'était marquée « déjà dans main ».
