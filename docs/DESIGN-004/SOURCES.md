# DESIGN-004 — preuves de lecture GitHub

Acquisition de six clones nus neufs HTTPS le16 octobre2026, puis inspection locale
au 2026-10-16T10:18:16+00:00. Aucune source externe modifiée/exécutée ; aucun modèle installé.
Cache ignoré `.audit-cache/design-004/`, commandes/dates/résultats acquisition
dans acquisition.json, refs UNIFIED dans unified-refs.txt. Une copie cache
ancienne n’a pas été présentée comme nouvelle lecture réseau.

Base UNIFIED choisie : mission-001g-maintenance à **41f53501fb18fe727d5fd453dd715f0811d2e897**,
SHA local égal à origin, incluant ADR approuvée e0e6f69 et80/80 tests001G.
Origin main observée e4435f4, aucun livrable ultérieur annoncé dans les refs
interrogées. Branche créée sans rebase : design-004-sync-expressions.

## Références inspectées

| Dépôt | Branche principale de lecture | SHA exact | Portée |
|---|---|---|---|
| bubth720/JAVIS-Local-v2 | `main` | [226e2e8cc3eebd479805b89d035eb5c1cbcad540](https://github.com/bubth720/JAVIS-Local-v2/tree/226e2e8cc3eebd479805b89d035eb5c1cbcad540) | Code et graph lus, pas testés ici |
| bubth720/JARVIS-LLM | `mission-003b-resources` | [1756e29557287550b5cfdffdd911cada2a302db6](https://github.com/bubth720/JARVIS-LLM/tree/1756e29557287550b5cfdffdd911cada2a302db6) | Code et graph lus, pas testés ici |
| bubth720/JARVIS-VOICE | `feat/voice-core-bridge-005k` | [521e613448083ffe6d575de2c9c369b48fb901f8](https://github.com/bubth720/JARVIS-VOICE/tree/521e613448083ffe6d575de2c9c369b48fb901f8) | Code et graph lus, pas testés ici |
| bubth720/JARVIS-SERVICES | `mission-002a-android-qualification` | [da762b3e3204707b5a3a05ec7a4946ec1aad2d64](https://github.com/bubth720/JARVIS-SERVICES/tree/da762b3e3204707b5a3a05ec7a4946ec1aad2d64) | Code et graph lus, pas testés ici |
| bubth720/JARVIS-INTERFACE | `feature/interface-storage-005` | [037e2cbe2e100eb06136e9899b815a4e8351fd72](https://github.com/bubth720/JARVIS-INTERFACE/tree/037e2cbe2e100eb06136e9899b815a4e8351fd72) | Code et graph lus, pas testés ici |
| bubth720/JARVIS-NEXUS | `main` | [b27df0b84d8f0082d17ca6278549298aaaf97926](https://github.com/bubth720/JARVIS-NEXUS/tree/b27df0b84d8f0082d17ca6278549298aaaf97926) | Code et graph lus, pas testés ici |

Les branches de développement sélectionnées ne sont pas assimilées à main : LLM
main917e335 reste documentaire ; VOICE mainb80b172 et SERVICES mainc9f94ad restent
README. INTERFACE n’annonce pas de main et sa branche par défaut reste
development/mission-002 ; la branche storage005 contient le code plus récent.
NEXUS contient seulement README dans ses refs disponibles.

## Fichiers déterminants et empreintes

Type de preuve pour chaque ligne : **source lue**, non exécution. Les URL sont
liées au commit, pas seulement à une branche mouvante. Les hashes servent à
reproduire l’inspection des sources publiques/autorisées, pas à tracer des données
personnelles.

| Dépôt | Fichier source | SHA256 des octets Git |
|---|---|---|
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/AppGraph.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/226e2e8cc3eebd479805b89d035eb5c1cbcad540/app/src/main/java/com/stark/jarvislocal/AppGraph.kt) | `c33015bebc08db742a12f965908c7b2b9319e601524a42cfff437998cb5fd138` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/SettingsStore.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/226e2e8cc3eebd479805b89d035eb5c1cbcad540/app/src/main/java/com/stark/jarvislocal/SettingsStore.kt) | `5806c3452037eec303d37f6ed34b12ae5352ac6e39eab857e72dc45e14233f6d` |
| JARVIS-LLM | [domain/src/main/kotlin/fr/jarvis/domain/catalogue/Catalogue.kt](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/domain/src/main/kotlin/fr/jarvis/domain/catalogue/Catalogue.kt) | `0f083b8c093503e7b0446e51d850db2242fa586bc89300643dd56e475a459c6d` |
| JARVIS-LLM | [app/src/main/java/fr/jarvis/llm/catalogue/CatalogueStore.kt](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/app/src/main/java/fr/jarvis/llm/catalogue/CatalogueStore.kt) | `31e6e4ee5e999206f32e9a24be5860ba6a5347a3607c99d37054aee4f0645de8` |
| JARVIS-LLM | [app/src/main/java/fr/jarvis/llm/catalogue/CatalogueJson.kt](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/app/src/main/java/fr/jarvis/llm/catalogue/CatalogueJson.kt) | `5fa8ff186a83dbc0bdcdd79e0ea622ee6b435e0312ed62d496cc43a4da11de24` |
| JARVIS-LLM | [app/src/main/assets/catalogue-demo.json](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/app/src/main/assets/catalogue-demo.json) | `132b2e850b39d2e7b3d45156e046db4a49ed4b072db56097e99fba28f0e4934c` |
| JARVIS-LLM | [docs/CATALOGUE_003.md](https://github.com/bubth720/JARVIS-LLM/blob/1756e29557287550b5cfdffdd911cada2a302db6/docs/CATALOGUE_003.md) | `9a2697610103c99ec3ac1a822778b960383e8d477b284292753891f436deb39a` |
| JARVIS-VOICE | [docs/mission005k/MISSION.md](https://github.com/bubth720/JARVIS-VOICE/blob/521e613448083ffe6d575de2c9c369b48fb901f8/docs/mission005k/MISSION.md) | `2a403370c7b15c28aabe4d4ec9e51a0be5d59a0db670ce8deeee9e26de3178c5` |
| JARVIS-VOICE | [docs/mission005j/RESULTATS.md](https://github.com/bubth720/JARVIS-VOICE/blob/521e613448083ffe6d575de2c9c369b48fb901f8/docs/mission005j/RESULTATS.md) | `e6a4ce0bcbc20c73417ca195c4e0f35b7ddb58fb63c0d8ee4c1868fbd1594850` |
| JARVIS-VOICE | [pocketRuntime/src/main/kotlin/com/jarvis/voice/pocket/QualityABStore.kt](https://github.com/bubth720/JARVIS-VOICE/blob/521e613448083ffe6d575de2c9c369b48fb901f8/pocketRuntime/src/main/kotlin/com/jarvis/voice/pocket/QualityABStore.kt) | `6e2432566ca5dc856d469f4bcb891dffb5de831f23cc44bcb5dc7c48e4366031` |
| JARVIS-VOICE | [pocketRuntime/src/main/kotlin/com/jarvis/voice/pocket/PrivatePcmStore.kt](https://github.com/bubth720/JARVIS-VOICE/blob/521e613448083ffe6d575de2c9c369b48fb901f8/pocketRuntime/src/main/kotlin/com/jarvis/voice/pocket/PrivatePcmStore.kt) | `5658627b956bb56def927437bf8ffe2bdcc3a6336faea6e664190a334f6f7514` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/modules/bridge/Bridge.java](https://github.com/bubth720/JARVIS-SERVICES/blob/da762b3e3204707b5a3a05ec7a4946ec1aad2d64/shared-runtime/src/main/java/fr/jarvis/services/modules/bridge/Bridge.java) | `b3649baec22d6a5998eedc461e8eca871f01edd4fb73b6c0c2259c3d6b6b5ee1` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/shared/api/Runtime.java](https://github.com/bubth720/JARVIS-SERVICES/blob/da762b3e3204707b5a3a05ec7a4946ec1aad2d64/shared-runtime/src/main/java/fr/jarvis/services/shared/api/Runtime.java) | `4459cc3de2535801afafc9ff5d2b4768de9c2db2432cce4971ee55f223993670` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/adapters/core/CoreAdapter.java](https://github.com/bubth720/JARVIS-SERVICES/blob/da762b3e3204707b5a3a05ec7a4946ec1aad2d64/shared-runtime/src/main/java/fr/jarvis/services/adapters/core/CoreAdapter.java) | `22ba5a4518d0ae522805531f934ebc221cc8ad8e636353c51e11acf897c50c8c` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/modules/memory/Memory.java](https://github.com/bubth720/JARVIS-SERVICES/blob/da762b3e3204707b5a3a05ec7a4946ec1aad2d64/shared-runtime/src/main/java/fr/jarvis/services/modules/memory/Memory.java) | `cf09debd97887a1345913b9d4606820b0ea1203f85e383315500dc1377ddf6e3` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/modules/knowledge/Knowledge.java](https://github.com/bubth720/JARVIS-SERVICES/blob/da762b3e3204707b5a3a05ec7a4946ec1aad2d64/shared-runtime/src/main/java/fr/jarvis/services/modules/knowledge/Knowledge.java) | `eceae842ab18d3d7bd122eda3d938d8aa78092f8ca24468750a0da8d92c509db` |
| JARVIS-SERVICES | [docs/CONTRACT_AUDIT.md](https://github.com/bubth720/JARVIS-SERVICES/blob/da762b3e3204707b5a3a05ec7a4946ec1aad2d64/docs/CONTRACT_AUDIT.md) | `2726616a6f112cd14dcadefd70d7372a39d388a9a1cb35a5334b916f295f3fe2` |
| JARVIS-SERVICES | [android/src/main/AndroidManifest.xml](https://github.com/bubth720/JARVIS-SERVICES/blob/da762b3e3204707b5a3a05ec7a4946ec1aad2d64/android/src/main/AndroidManifest.xml) | `2116e0e9a496561956b44d62ff5edce258850ee6ad14f258a529feab5e7fe8be` |
| JARVIS-INTERFACE | [app/src/main/java/com/jarvis/interfaceapp/storage/LayoutCodec.kt](https://github.com/bubth720/JARVIS-INTERFACE/blob/037e2cbe2e100eb06136e9899b815a4e8351fd72/app/src/main/java/com/jarvis/interfaceapp/storage/LayoutCodec.kt) | `41ca0fbd255e8cb28931061d5f4c050fe367d3715e5dfcd57e3f5e7a792a1074` |
| JARVIS-NEXUS | [README.md](https://github.com/bubth720/JARVIS-NEXUS/blob/b27df0b84d8f0082d17ca6278549298aaaf97926/README.md) | `45434fa5860471568bf2bac9fda69a547b39462107e2f4c4c2d5a62a55aaf8ea` |

## Constats vérifiables et limites

- LLM003B conserve003 catalogue dans son ascendance et les neuf champs JSON1.
  Démo : huit records/neuf variantes ;1–8 variantes et1–12 exemples, FTS4, révisions
  et tombstones.1500 SYNTHETIC est une fixture, pas la bibliothèque demandée.
- SERVICES Runtime construit `new Bridge(... new Bridge.Simulator())` : echo local,
  pas protocole réseau réel. CoreAdapter se déclare hôte in-process, pas connexion
  CORE. Memory exige jeton de confirmation dans son Guard, pas preuve de
  consentement inter-appareil. Knowledge utilise un dictionnaire/hachage lexical,
  pas un encodeur neuronal ; ZimArchive est une interface, pas Kiwix branché.
- VOICE005J est du code Studio réel ;005K à521e613 ajoute un cahier de mission,
  pas le module voiceBridgeContract ou un pont CORE. Le rapport005J cite des
  résultats émulateur24/24 ; le cahier005K rapporte un retour utilisateur Xiaomi.
  Ce dernier reste une **déclaration versionnée**, ni mesure ni essai reproduit ici.
  Aucune latence physique, expressivité native ou cloning universel déduits.
- INTERFACE005 stocke un layout versionné avec champs inconnus conservés/non
  interprétés et refus d’incompatibilité ; pas réplication multi-appareils.
- CORE construit toujours son LlamaLocalEngine et SharedPreferences, pas un client
  de synchronisation ou de catalogue externe.

## CI et matériel

Aucune API Actions/PR consultée pendant DESIGN-004. api.github.com est absent de
la politique runtime enforced observée ; les résultats historiques des autres
modules restent des rapports lus, pas des CI observées aujourd’hui. Aucun build
ou test Android des autres dépôts, aucun téléphone/PC/montre physiquement qualifié,
aucun appairage ou sync réel. Les tests UNIFIED exécutés sont détaillés dans
[RAPPORT](RAPPORT_DESIGN_004.md). Aucun nouveau test produit SYNC/cache n’est revendiqué.

Les nouvelles branches SERVICES/VOICE/INTERFACE complètent l’inventaire001F, sans
écraser ses snapshots. Ce document est une lecture ciblée DESIGN-004, pas une
actualisation exhaustive du registre des neuf dépôts ou de toutes les PR.
