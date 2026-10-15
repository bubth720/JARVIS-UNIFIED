# Inventaire de consolidation — Phase A

Capture de neuf dépôts Git accessibles, lecture des branches et des sources aux
SHA ci-dessous. Visibilité public/privé inconnue : l’authentification du proxy
peut autoriser un dépôt privé. PR ouvertes/fermées et Actions courantes non
vérifiables via API (proxy403), pas assimilées à des listes vides.
Le relevé complet, dates de commit UTC, historique main, tests, langages,
manifestes/packages, SDK et workflows est dans
[repositories.json](../registry/repositories.json). Les compteurs de tests ci-dessous
comptent des **fichiers**, parfois fixtures, pas des tests exécutés.

| Dépôt | Branche inspectée | SHA | Fichiers suivis / fichiers tests |
|---|---|---|---|
| bubth720/JAVIS-Local-v2 | `main` | `226e2e8cc3eebd479805b89d035eb5c1cbcad540` | 39 / 3 |
| bubth720/JARVIS-LLM | `mission-003b-resources` | `1756e29557287550b5cfdffdd911cada2a302db6` | 77 / 12 |
| bubth720/JARVIS-VOICE | `feat/voice-expression-005i` | `56ffebc5b514d683f977ea177a26e2b6a91b4930` | 293 / 40 |
| bubth720/JARVIS-INTERFACE | `development/mission-002` | `d1c0931c4507e9af8f1aa60951947c23f4394b56` | 28 / 2 |
| bubth720/JARVIS-INTERFACE- | `main` | `a857f5019354ea1c912e6f66bebdcc053c0cb700` | 1 / 0 |
| bubth720/JARVIS-NEXUS | `main` | `b27df0b84d8f0082d17ca6278549298aaaf97926` | 1 / 0 |
| bubth720/JARVIS-VOLUTION- | `main` | `a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0` | 1 / 0 |
| bubth720/JARVIS-SERVICES | `main` | `c9f94ad2fa219a5e09cda92fb451aca606ee1646` | 1 / 0 |
| bubth720/JARVIS-UNIFIED | `main` | `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b` | 1 / 0 |

## Reconnaissance et ambiguïtés

CORE est une fonction historiquement implémentée dans JAVIS-Local-v2 : relation
**confirmée** par AppGraph/JarvisCore. L’essai Git vers JARVIS-CORE retourne
« Repository not found »/128 : **inaccessible**, pas preuve d’inexistence.
JARVIS-VOLUTION- est le nom réel du dépôt observé ; lien avec EVOLUTION
**plausible**, non confirmé par son README initial. JARVIS-EVOLUTION inaccessible
à l’essai Git. Aucun nom corrigé automatiquement.
INTERFACE et INTERFACE- sont **confirmés distincts** par identités Git, SHA et
contenu. Le premier contient l’UI autonome Compose sur development/mission-002,
le second seulement README. Leur relation de doublon voulu est **inconnue**.
Aucun dépôt n’est déclaré obsolète faute de décision documentée.

NEXUS/SERVICES/VOLUTION-/INTERFACE- : seulement README, aucun point d’entrée,
Gradle ou test dans les refs disponibles. INTERFACE : MainActivity Compose,
HomeViewModel/StateFlow, trois tests JVM déclarés, trois tests instrumentés
historiquement compilés ; contrat AvatarSession sans rendu 2.5D implémenté.
Pas de widgets mobiles/persistants ou lien CORE déduit du nom de l’application.

VOICE s’est développée jusqu’à 005H et 005I depuis l’ancien audit. identityRuntime
implémente bibliothèque, références/profils par identité et archives JVIENC01 ;
expressionRuntime ajoute un DTO strict et une politique d’expression, sans contrôle
émotionnel natif annoncé. Les rapports locaux/CI source sont lus et cités comme
**historiques**, non validés de nouveau via Actions. 005I réutilise des bibliothèques
VOICE dans ce dépôt : c’est une intégration **intradépôt VOICE**, pas CORE↔VOICE.

## Merges Git observés

CORE main contient les trois branches docs/heure/SQLite par ascendance, avec
parents des commits de merge dans l’inventaire. C’est une consolidation CORE
interne ; le nom d’une PR dans un sujet Git ne confirme pas son état API actuel.
LLM main n’a que deux documents ; toutes les branches de développement listées
sont hors main par ascendance et leurs sources app/domain n’y figurent pas.
VOICE main n’a que README ; aucune des sept branches de fonctionnalités n’est
ancêtre de main. INTERFACE n’annonce aucune ref main ; sa branche par défaut
est development/mission-002, relation main **inconnue**. UNIFIED distant main
reste e4435f4 (README), les missions locales sont conservées comme ancêtres de
la branche de consolidation. Les graphs Git ne prouvent pas un chemin runtime.

Les verdicts d’ascendance ne détectent pas toutes les équivalences par squash ou
cherry-pick ; ici l’inventaire des fichiers de main confirme en plus l’absence
d’application dans main LLM/VOICE/UNIFIED. Tous les états sont bornés aux clones
Git datés, pas à une synchronisation en temps réel.

## Chevauchements à conserver sans effacement

| Capacité | Propriétaire actuel démontré | Cible proposée / chevauchement |
|---|---|---|
| Routage et historique | CORE JarvisCore/SQLite | CORE, séparé de l’inférence |
| Inférence | CORE LlamaLocalEngine ; autre APK LLM LlamaBackend | LLM seul après adaptateur testé, pas deux résidences |
| Mémoire personnelle | CORE memories et dialogue Ajouter /remember | CORE, confirmation explicite commune encore à réaliser |
| Catalogue éditorial | LLM catalogue SQLite | Couche connaissance distincte du moteur, exposition sous orchestration CORE |
| Documents/index | CORE PdfImporter/TextChunker/RagEngine | NEXUS cible, dépôt encore vide de code ; migration future |
| Capture/STT | CORE WavRecorder/WhisperLocalEngine | Capacité VOICE cible, orchestrée par CORE ; pas déplacée ici |
| Synthèse | CORE AndroidTTS ; VOICE neuronal autonome | VOICE personnalisée, pas de remplacement générique silencieux |
| UI | CORE UI historique et INTERFACE Compose autonome | INTERFACE cible, avatar seulement contrat |
| Outils/correctifs | Commandes simples CORE ; services/évolution sans runtime | SERVICES/EVOLUTION cibles sous permissions/revue |

CORE minSdk24, SDK35, Kotlin2.0.21, JDK17, pas de wrapper ; LLM minSdk29,
SDK36, Kotlin2.1.21, JDK21/outils natifs épinglés ; VOICE et INTERFACE minSdk26,
SDK35. CORE copie ses assets surtout par taille ; LLM vérifie SHA et métadonnées
GGUF ; VOICE profils liés au pack exact. Ces incompatibilités interdisent une
substitution non testée. SQLite CORE corrigée V1→V2 conserve les données, sans
export global Android ; backup UNIFIED reste fictif. Archives vocales JVIENC01
sont un autre format et ne rendent pas JVBK interopérable.
