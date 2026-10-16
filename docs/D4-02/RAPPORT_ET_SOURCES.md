# D4-02 — rapport et preuves de lecture

**Mission documentaire terminée : propositions techniques non adoptées, aucun raccordement réalisé.**
Module : UNIFIED, dépôt : bubth720/JARVIS-UNIFIED.
Branche : `design/d4-02-ownership-mapping`, base locale et origin vérifiée
`db1592a76ba6a10b9798f4803e4e4247bbf89c01`, dernière livraison DESIGN-004 annoncée au moment du départ.
Le SHA final se vérifie par `git rev-parse design/d4-02-ownership-mapping` et dans
le compte rendu de livraison ; aucun auto-SHA inventé ici.
État initial propre, branches antérieures préservées, aucun main fusionné.

## Documents et résultat

- [Matrice de référence proposée](MATRICE_RESPONSABILITES.md) : un propriétaire
  par objet/capacité, CORE autorité, NEXUS stockage futur réemployant SERVICES,
  catalogue conservé LLM, VOICE seule propriétaire de ses profils et PCM.
- [Adaptations/contrats](ADAPTATIONS_ET_CONTRATS.md) : ports existants et manquants,
  incompatibilité du système/prompt, namespace SERVICES, cycle de vie et versions.
- [Premier CORE↔LLM réel](PREMIER_RACCORDEMENT_CORE_LLM.md) : tests puis pilote
  texte local, deux dépôts propriétaires, identité et admission avant génération.
- [Risques et protections](RISQUES_ET_PROTECTIONS.md) : données, double résidence,
  arrêt natif, prompt/provenance, SDK/signatures, permissions et régressions.
- [Décisions et missions ordonnées](DECISIONS_ET_MISSIONS.md) : O1–O5 soumis à accord,
  petites missions par dépôt, aucune démarrée par cette conception.

Le terme matrice « définitive proposée » décrit la référence consolidée de cette
mission, pas une approbation de l’utilisateur. ADR-001 demeure approuvée avec
précisions, inchangée ; son orientation n’est pas redemandée. Aucun contrat v1
ou autre contrat existant n’est modifié. Aucun transfert/effacement de données,
clé, modèle ou profil, aucun autre dépôt modifié.

## État réel des sources GitHub

Cinq clones nus HTTPS **neufs**, acquisition puis lecture au 2026-10-16T15:05:00+00:00.
Commandes, dates et résultats acquisition.json et métadonnées source-inspection.json
dans `.audit-cache/d4-02/`, ignoré par Git. Aucun script externe exécuté.
Les refs UNIFIED ont été lues avant création de branche ; main e4435f4 observée.

| Dépôt exact sous bubth720 | Branche de lecture principale | SHA exact | Ancêtre de son main ? |
|---|---|---|---|
| JAVIS-Local-v2 | `mission-004a-core-stability` | [306a89b7cc33803aba9b7af9c6a553f1bc40f08f](https://github.com/bubth720/JAVIS-Local-v2/tree/306a89b7cc33803aba9b7af9c6a553f1bc40f08f) | Non |
| JARVIS-LLM | `mission-003c-device-qualification` | [43503f59f530f2bb48955bce9d7d71e2470fb668](https://github.com/bubth720/JARVIS-LLM/tree/43503f59f530f2bb48955bce9d7d71e2470fb668) | Non |
| JARVIS-SERVICES | `mission-002a-android-qualification` | [34ab1c2147c439b205b9a49383f3b4f0c6368d43](https://github.com/bubth720/JARVIS-SERVICES/tree/34ab1c2147c439b205b9a49383f3b4f0c6368d43) | Non |
| JARVIS-VOICE | `feat/voice-core-bridge-005k` | [521e613448083ffe6d575de2c9c369b48fb901f8](https://github.com/bubth720/JARVIS-VOICE/tree/521e613448083ffe6d575de2c9c369b48fb901f8) | Non |
| JARVIS-NEXUS | `main` | [b27df0b84d8f0082d17ca6278549298aaaf97926](https://github.com/bubth720/JARVIS-NEXUS/tree/b27df0b84d8f0082d17ca6278549298aaaf97926) | Oui |

CORE004A et LLM003C sont de nouvelles branches à considérer avant une mission
code ; ne pas les remplacer par les anciens main documentaires/non stabilisés.
SERVICES002A a également avancé depuis DESIGN-004 (da762b3→34ab1c2).
Aucun choix de base ne prétend que ces branches sont fusionnées.

CORE004A : LocalLanguageModel est un seam de test réel, pas une implémentation
distante ; AppGraph continue d’instancier/préchauffer son moteur ; stop/unload
ne sont pas publics dans le port, drainage NonCancellable conserve le gate.
Rapport versionné004A :140 tests simulés/JVM réussis, pas de vrai GGUF/Whisper,
aucune campagne physique ou sauvegarde Android réelle ; non réexécutés ici.

LLM003C : interfaces Conversation/LlamaBackend/JNI relues et identiques à003B
aux chemins cités. Prompt natif fixe, API user/assistant, worker unique et baux
process-local, aucun service IPC trouvé dans le code inspecté. Rapport versionné
cite56 tests domaine,21 simulations etCTest1/1, run
https://github.com/bubth720/JARVIS-LLM/actions/runs/38887000314,
code testé4501881 ; le rapport est lu, pas l’API Actions aujourd’hui. Qualification
physique Redmi/POCO explicitement en attente, aucun gain matériel déduit.

SERVICES : CoreAdapter est hôte in-process et LlmPort possède Mock/Unavailable,
pas un vrai client CORE/LLM ; Bridge Simulator reste echo. Les définitions
requestStop par défaut vide et awaitStopped du mock ne prouvent aucun arrêt natif.
NEXUS main README seul ; VOICE005K ne contient qu’un cahier, pas un module bridge
opérationnel. Rien ici ne met à jour automatiquement tout le registre historique.

## Preuves immuables : fichiers déterminants

Type = **source lue**, sauf rapports/docs = documentation versionnée. Hashes de
fichiers Git autorisés, jamais de texte ou voix personnels.

| Dépôt | URL de fichier au SHA inspecté | SHA256 |
|---|---|---|
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/AppGraph.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/306a89b7cc33803aba9b7af9c6a553f1bc40f08f/app/src/main/java/com/stark/jarvislocal/AppGraph.kt) | `3d231561b6b3eed17dabcf670c56ef62bb93c30558403ed6039708b0386cab95` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/JarvisCore.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/306a89b7cc33803aba9b7af9c6a553f1bc40f08f/app/src/main/java/com/stark/jarvislocal/JarvisCore.kt) | `6c2bb464b751d774c22b40f47e78528cf72a22330c50f123b89d5300b73fbe5a` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/LocalLanguageModel.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/306a89b7cc33803aba9b7af9c6a553f1bc40f08f/app/src/main/java/com/stark/jarvislocal/LocalLanguageModel.kt) | `8c43b9c3b1210787942f76465194535770993645c88129f03f9fb66f33e24098` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/LlamaLocalEngine.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/306a89b7cc33803aba9b7af9c6a553f1bc40f08f/app/src/main/java/com/stark/jarvislocal/LlamaLocalEngine.kt) | `e19d81547a30bb96275011b75d932aeb10cbf422e31ebc9033a5f15106cc5ba8` |
| JAVIS-Local-v2 | [app/src/main/java/com/stark/jarvislocal/SessionCoordinator.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/306a89b7cc33803aba9b7af9c6a553f1bc40f08f/app/src/main/java/com/stark/jarvislocal/SessionCoordinator.kt) | `30b8249a0de08ab40de089bcc0cd052f117fbda6c7059c66bdeb7acb5e343433` |
| JAVIS-Local-v2 | [docs/mission-004a/VALIDATION.md](https://github.com/bubth720/JAVIS-Local-v2/blob/306a89b7cc33803aba9b7af9c6a553f1bc40f08f/docs/mission-004a/VALIDATION.md) | `9c43611547f2343006e6bddbb6f5a19dbc4acb6c58efab55e7808488a537a9ef` |
| JARVIS-LLM | [domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt](https://github.com/bubth720/JARVIS-LLM/blob/43503f59f530f2bb48955bce9d7d71e2470fb668/domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt) | `4d058a81cce536691e184253e66069e537f9ae9ffe3c4dd0c6eb9fc6b7e4868a` |
| JARVIS-LLM | [app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt](https://github.com/bubth720/JARVIS-LLM/blob/43503f59f530f2bb48955bce9d7d71e2470fb668/app/src/main/java/fr/jarvis/llm/engine/LlamaBackend.kt) | `f37f10d54ff0589e8980f11aec76037126d3b07bed2570397584aca273c77bed` |
| JARVIS-LLM | [app/src/main/cpp/bridge.cpp](https://github.com/bubth720/JARVIS-LLM/blob/43503f59f530f2bb48955bce9d7d71e2470fb668/app/src/main/cpp/bridge.cpp) | `6d3d8ee338e5cee2ddad35376dc3218624ec418dfd6fed5304b002787ef73b07` |
| JARVIS-LLM | [app/src/main/java/fr/jarvis/llm/ProcessResources.kt](https://github.com/bubth720/JARVIS-LLM/blob/43503f59f530f2bb48955bce9d7d71e2470fb668/app/src/main/java/fr/jarvis/llm/ProcessResources.kt) | `cf1a2959c20ebfac5a0ba176cc9581ac28ee52f71cd6f3645680d1ca11451968` |
| JARVIS-LLM | [docs/mission-003c/RAPPORT.md](https://github.com/bubth720/JARVIS-LLM/blob/43503f59f530f2bb48955bce9d7d71e2470fb668/docs/mission-003c/RAPPORT.md) | `477226df218d71446ba2bcca38715ed2b1346bdb585bff900ee984fc92c72bf3` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/adapters/core/CoreAdapter.java](https://github.com/bubth720/JARVIS-SERVICES/blob/34ab1c2147c439b205b9a49383f3b4f0c6368d43/shared-runtime/src/main/java/fr/jarvis/services/adapters/core/CoreAdapter.java) | `22ba5a4518d0ae522805531f934ebc221cc8ad8e636353c51e11acf897c50c8c` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/adapters/llm/LlmPort.java](https://github.com/bubth720/JARVIS-SERVICES/blob/34ab1c2147c439b205b9a49383f3b4f0c6368d43/shared-runtime/src/main/java/fr/jarvis/services/adapters/llm/LlmPort.java) | `47036a9c67952f0668e20bb5f87f0e9511a8ae4a05c1e4e395685a6c28ab3342` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/modules/memory/Memory.java](https://github.com/bubth720/JARVIS-SERVICES/blob/34ab1c2147c439b205b9a49383f3b4f0c6368d43/shared-runtime/src/main/java/fr/jarvis/services/modules/memory/Memory.java) | `cf09debd97887a1345913b9d4606820b0ea1203f85e383315500dc1377ddf6e3` |
| JARVIS-SERVICES | [shared-runtime/src/main/java/fr/jarvis/services/modules/bridge/Bridge.java](https://github.com/bubth720/JARVIS-SERVICES/blob/34ab1c2147c439b205b9a49383f3b4f0c6368d43/shared-runtime/src/main/java/fr/jarvis/services/modules/bridge/Bridge.java) | `b3649baec22d6a5998eedc461e8eca871f01edd4fb73b6c0c2259c3d6b6b5ee1` |
| JARVIS-VOICE | [docs/mission005k/MISSION.md](https://github.com/bubth720/JARVIS-VOICE/blob/521e613448083ffe6d575de2c9c369b48fb901f8/docs/mission005k/MISSION.md) | `2a403370c7b15c28aabe4d4ec9e51a0be5d59a0db670ce8deeee9e26de3178c5` |
| JARVIS-NEXUS | [README.md](https://github.com/bubth720/JARVIS-NEXUS/blob/b27df0b84d8f0082d17ca6278549298aaaf97926/README.md) | `45434fa5860471568bf2bac9fda69a547b39462107e2f4c4c2d5a62a55aaf8ea` |

## Vérifications réellement exécutées dans UNIFIED

Plateforme : Linux-6.18.44-x86_64-with-glibc2.41, Python3.12.14.

| Commande | Résultat |
|---|---|
| `python3 -m unittest discover -s tests -v` | 27 tests, OK, code0 |
| `python3 -m unittest discover -s registry/tests -v` | 23 tests, OK, code0 |
| `python3 -m unittest discover -s backup_prototype/tests -v` | 30 tests, OK, code0 |
| `python3 scripts/validate_unified.py` | Réussi :9 dépôts,5 contrats et exemples, liens/JSON/jetons usuels |
| `python3 registry/scripts/update_registry.py --validate-only` | Réussi :9 dépôts,16 missions |
| `git diff --check`, puis contrôle indexé | Réussis pour les différences de cette mission |

**80 tests existants réussis, zéro échec et zéro saut.** Logs complets/durées dans
`.audit-cache/d4-02/tests.json`, audit-contracts.txt, registry.txt et backup.txt.
Contrôles finaux de périmètre et hashes documentaires : final-checks.json, même
dossier ignoré. Ces tests n’exécutent pas un nouveau protocole ou un adaptateur.
Aucun test Android des dépôts sources, vrai JNI/GGUF, CI actuelle, essai physique
ou integration E2E exécuté ici. Aucun code ou test ajouté pour simuler une preuve.

## Blocages et limites

Les décisions O1–O5 ne sont pas prises par la rédaction de ces documents. Signature
CORE installée inconnue, absence de transport et arbitre global, lacunes du port
CORE, prompt système non directement représentable et qualification matérielle
manquante bloquent le raccordement futur, pas la livraison documentaire D4-02.

API GitHub absente de la politique réseau enforced observée ; CI/PR courantes non
consultées. Lecture Git des cinq dépôts réussie. La publication éventuelle de cette
branche est vérifiée séparément et consignée dans `.audit-cache/d4-02/delivery.json`
et le compte rendu ; le présent rapport n’est pas une preuve de PR ou de push.
Aucun main modifié. Les preuves anciennes et les contrats restent inchangés.

## Suite recommandée

Utilisateur : examiner O1 puis O2/O4, faire préciser O3 (confiance/transport), puis
missions CORE cycle de vie et LLM contrat de génération, autorisées séparément.
Tests purs avant endpoint isolé et client, vraie qualification avant installation
ou activation. SERVICES/NEXUS réemploi et VOICE005K viennent ensuite, sans devenir
prérequis artificiels de la première inférence texte CORE↔LLM.
