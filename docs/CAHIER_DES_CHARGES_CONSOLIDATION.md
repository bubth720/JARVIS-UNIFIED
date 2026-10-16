---
title: "JARVIS-UNIFIED | Mission 001 — Consolidation, traçabilité et contrats d'intégration"
version: "1.0"
date: "2026-10-15"
status: "Mission proposée — aucune exécution autorisée par ce document seul"
owner: "JARVIS-CENTRAL"
---

# JARVIS-UNIFIED — MISSION 001
## Consolidation de l'architecture, vérification des intégrations et source de vérité commune

**Destinataire :** Codex, environnement GitHub `bubth720/JARVIS-UNIFIED`.

**Objectif final :** supprimer les ambiguïtés entre JARVIS CORE, JARVIS LLM et JARVIS UNIFIED, construire dans UNIFIED un registre vérifiable de tous les modules, établir la réalité des fusions et intégrations, définir les contrats futurs, puis fournir un plan d'intégration ordonné. **Ne pas prétendre que des modules sont déjà techniquement connectés lorsqu'aucun code, test ou chemin d'exécution ne le démontre.**

**Nature de la mission :** grande mission de consolidation **dans le seul dépôt UNIFIED**. Elle ne vise pas à fusionner précipitamment les bases de code Android ni à modifier les autres dépôts. La consolidation documentaire, les contrôles automatisés et les contrats sont les réalisations obligatoires ; l'intégration physique CORE ↔ LLM sera une mission d'implémentation séparée, soumise à autorisation après le présent diagnostic.

## 0. Règles non négociables

1. Examiner les dépôts GitHub accessibles avant toute conclusion. Une conversation ou un README ne suffit pas à prouver qu'une fonctionnalité fonctionne. Lire code, manifestes, Gradle, contrats, branches, commits, pull requests et tests accessibles.
2. **Ne modifier que `bubth720/JARVIS-UNIFIED`**, sur une branche dédiée telle que `mission-001-architecture-unified`. Ne rien supprimer, renommer ou fusionner dans un autre dépôt.
3. **Ne jamais fusionner vers `main` sans validation explicite de l'utilisateur.** Ne pas activer l'auto-merge. Livrer une PR ou un rapport de branche seulement, en attente d'approbation.
4. Ne pas présenter une compilation cloud comme un test matériel. Ne pas inventer de tests, d'intégration IPC, de compatibilité Android ou de succès GitHub Actions.
5. Protéger le fonctionnement hors ligne : GitHub est un outil de développement, **pas une dépendance de JARVIS à l'exécution**. Aucun accès cloud obligatoire dans CORE, LLM, VOICE ou l'application finale.
6. Préserver les données, fonctions et historiques existants. Ne pas remplacer le moteur actif, la mémoire SQLite, la voix ou les documents au cours de cette mission.
7. Aucun secret, jeton ou donnée utilisateur privée dans les commits, artefacts, logs ou exemples. Les accès GitHub en lecture seule suffisent pour l'audit.
8. Limiter les dépendances du registre/audit ; privilégier Python standard et JSON Schema/documentation portable. Si une dépendance est ajoutée, justifier précisément son intérêt.
9. Si l'accès GitHub ou l'environnement empêche l'inspection ou l'écriture (dont HTTP 403), marquer les preuves **inaccessibles/non vérifiées**, signaler le blocage et fournir les livrables disponibles sous forme de patch ou contenu. Ne pas simuler une écriture réussie.
10. À chaque étape : préciser **module, mission, branche, commit, tests réellement lancés, blocage, prochaine action**.

## 1. Situation de référence, à revérifier obligatoirement

Les repères suivants proviennent d'une consultation GitHub du **15 octobre 2026**. Ce sont des indices de départ, pas une dispense de contrôle en direct.

| Fonction ou dépôt | Constat de départ | Conséquence |
|---|---|---|
| `bubth720/JAVIS-Local-v2` | Contient notamment `JarvisCore.kt`, `LlamaLocalEngine.kt`, `LocalDatabase.kt`, PDF/RAG, Whisper/TTS. `main` relevé à `226e2e8`. | **CORE historique monolithique**, pas encore un orchestrateur modulaire pleinement séparé. Ne pas le confondre avec un éventuel nouveau dépôt `JARVIS-CORE` non trouvé lors de la consultation. |
| `bubth720/JARVIS-LLM` | `main` relevé à `917e335` (cahier des charges) ; prototype sur `mission-003b-resources`, tête `1756e29`, code testé `e9d408e`. | Moteur Android autonome en développement ; **la branche de mission n'est pas fusionnée dans `main`**. |
| `bubth720/JARVIS-UNIFIED` | `main` relevé à `e4435f4` ; uniquement README initial. | Dépôt de coordination **non encore structuré**. |
| `bubth720/JARVIS-VOICE` | Dépôt autonome observé. | À inventorier, **pas intégré par simple présence**. |
| `bubth720/JARVIS-INTERFACE` | Dépôt autonome observé ; autre dépôt `JARVIS-INTERFACE-` également visible. | Identifier la cible active et les doublons, sans suppression. |
| `bubth720/JARVIS-NEXUS` | Dépôt observé. | Déterminer son rôle et son état par lecture. |
| `bubth720/JARVIS-SERVICES` | Dépôt observé. | Déterminer son rôle et son état par lecture. |
| `bubth720/JARVIS-VOLUTION-` | Nom observé, potentiellement lié à EVOLUTION mais équivalence **non démontrée**. | Établir si dépôt actif, alias ou erreur de nommage, sans supposition. |

Donnée de validation connue : [GitHub Actions LLM mission 003B, exécution 38636152472](https://github.com/bubth720/JARVIS-LLM/actions/runs/38636152472) a été rapportée comme réussie sur le commit `e9d408e` (55 tests JVM domaine, 16 Android simulés, 1 test natif). Cela ne qualifie ni l'intégration à CORE, ni la batterie/thermique sur appareil. Le dernier workflow CORE réussi consulté datait du 5 octobre 2026, antérieurement aux corrections ensuite fusionnées. **Codex doit vérifier de nouveau ces éléments**.

## 2. Décision d'architecture à documenter, puis confronter au code

### 2.1 Rôles canoniques proposés

- **JARVIS-CENTRAL (projet ChatGPT)** : conversation de coordination humaine ; aucune garantie de synchronisation temps réel ni d'exhaustivité de la mémoire.
- **JARVIS-UNIFIED (GitHub)** : **source de vérité technique**, registres, états de vérification, contrats versionnés, matrices d'intégration, procédures et feuille de route. Ce dépôt **ne sera ni un troisième moteur LLM ni une application Android doublon**.
- **JARVIS CORE (fonction, initialement dans `JAVIS-Local-v2`)** : décisions, routage, session, autorisations, politiques de ressources et coordination entre capacités. Le noyau actuel contient historiquement plusieurs fonctions ; les extraire sera progressif.
- **JARVIS LLM** : **un moteur local de génération** interchangeable, avec garde-fous et API d'inférence. Lors de l'intégration, éviter de maintenir en parallèle deux moteurs actifs sans arbitrage matériel.
- **JARVIS VOICE** : capture/transcription/synthèse/parole personnalisée selon capacités effectivement démontrées.
- **JARVIS INTERFACE** : UI et avatar 2.5D, pouvant fonctionner en mode autonome puis être raccordés à CORE.
- **JARVIS NEXUS** : documents, index/recherche/connaissances locales ; fonctions futures à distinguer du code existant dans CORE.
- **JARVIS EVOLUTION** : diagnostic et correctifs **isolés**, soumis à validation avant déploiement.
- **JARVIS SERVICES** : capacités/outils supplémentaires soumis à permissions.

### 2.2 Interdictions d'interprétation

Ne jamais assimiler les quatre notions suivantes :

1. **Même projet ChatGPT** = contexte de discussion partagé partiellement, pas code synchronisé.
2. **Même organisation / même compte GitHub** = dépôts visibles, pas lien logiciel.
3. **Branches Git fusionnées dans `main`** = intégration de commits dans **un dépôt donné**, pas communication entre applications.
4. **Intégration fonctionnelle** = **code de liaison + chemin d'exécution démontré + tests appropriés**. La disponibilité opérationnelle sur appareil exige en plus des essais matériels.

La mission doit donner à chacune de ces notions un verdict séparé et argumenté.

## 3. Phase A — Inventaire complet et reconnaissance des dépôts

**A1.** Lister les dépôts accessibles réellement pertinents. Relever leurs noms exacts, visibilité/accessibilité, branche par défaut, dernier commit et date, branches actives, PR ouvertes/fermées, workflows/CI disponibles, langage, point d'entrée, manifestes/packages, tests et README.

**A2.** Identifier les ambiguïtés de nommage (`JAVIS-Local-v2`, `JARVIS-CORE`, `JARVIS-VOLUTION-`, deux interfaces) par preuves. Étiqueter chaque relation : `confirmée`, `plausible`, `inconnue`, `obsolète documentée`. Ne renommer aucun dépôt.

**A3.** Comparer notamment CORE historique ↔ JARVIS-LLM : moteurs llama.cpp et responsabilités qui se chevauchent, interfaces existantes, stockage local, mécanismes de sauvegarde, politique mémoire, opérations concurrentes, modèles embarqués/importés, SDK Android et compatibilité de versions.

**A4.** Reconstituer les changements réels de `main` et des branches de mission, sans déclarer une branche de fonctionnalité « intégrée » à partir de son seul succès CI. Comparer branches / commits lorsque possible ; signaler les divergences.

**A5.** Collecter des preuves avec URL GitHub, ref de branche, SHA, date UTC, type (`source`, `CI`, `matériel`, `documentation`, `déclaration`) et date de consultation. Une impossibilité d'accès est une donnée à enregistrer.

**Livrables A :** `registry/repositories.json`, `docs/INVENTAIRE.md`, `docs/PROUVES.md` et inventaire reproductible des duplications et incertitudes.

## 4. Phase B — Source de vérité et matrice de fusion/intégration

Créer une représentation compréhensible à l'humain et exploitable par un script, sans état fictif.

### 4.1 Registre machine

Créer `registry/modules.json`, lié aux identifiants de `registry/repositories.json`. Pour chaque module :

- identifiant stable, nom affiché, responsabilité unique et frontières de périmètre ;
- dépôt(s) et branches de référence ; branche **développée** distincte de la branche **fusionnée** ;
- commit observé, horodatage, liens de preuve ;
- interfaces existantes, interfaces prévues et dépendances ;
- état du code, état des tests, état de qualification physique ;
- propriétaire de chaque capacité commune (`inférence`, `voix`, `documents`, `routage`, `mémoire`, `UI`, `outils`, `correction`) ;
- points non vérifiés, blocages et prochaine mission.

Prévoir un champ permettant `inconnu` / `non vérifié` sans le convertir arbitrairement en `absent` ou en `échec`.

### 4.2 Matrice d'intégration

Dans `docs/MATRICE_INTEGRATION.md`, rendre lisibles les relations CORE ↔ LLM, CORE ↔ VOICE, CORE ↔ NEXUS, CORE ↔ SERVICES, CORE ↔ INTERFACE, EVOLUTION ↔ modules et UNIFIED ↔ tous.

Pour chaque lien, donner **séparément** :

- `contrat` : absent / proposé / défini et versionné ;
- `code de liaison` : absent / partiel / présent / inconnu ;
- `test d'intégration` : non exécuté / échec / réussi / inconnu ;
- `test sur appareil` : non exécuté / échec / réussi / inconnu ;
- `présence dans main` : oui / non / partielle / inconnu ;
- preuves associées, risques et prochaine action.

Ne pas inventer de pourcentages d'avancement. Ne pas fabriquer de coche verte à partir d'un simple README ou d'une compilation.

### 4.3 Décision sur la « fusion »

Rédiger `docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md` proposant formellement :

- **pas de monorepo applicatif précipité** ;
- UNIFIED = coordination et registres, **pas runtime** ;
- CORE = orchestration cible et conservation des fonctions historiques jusqu'à remplacement testé ;
- LLM = moteur futur privilégié mais **pas déclaré raccordé** sans preuve ;
- migration progressive, réversible, sans double chargement actif du modèle ;
- séparation de la gestion de la conversation, du catalogue, de la mémoire durable et du moteur inférentiel ;
- politique de compatibilité Android et de migration vers mini-PC.

Statut de l'ADR : **`proposée — en attente de validation utilisateur`** ; jamais « approuvée » par défaut.

**Livrables B :** registre, matrice, ADR, diagramme de dépendances et tableau « quel module fait quoi ? » dans le README.

## 5. Phase C — Contrats techniques, mais pas de fausse intégration

Préparer `contracts/v1/` avec des schémas et exemples portables. Définir **les interfaces**, ne pas simuler une connexion effective entre APKs.

### 5.1 Contrats minimaux

- `capability-manifest` : ID module, version sémantique, capacités disponibles, exigences d'environnement, état local/disponible, compatibilités.
- `request-envelope` : version de protocole, correlation ID, origine, destination/capacité, portée et limites, échéance, identifiant d'annulation, version du contrat.
- `response-envelope` : même correlation ID, statut, résultat ou erreur structurée, provenance et métadonnées d'exécution non sensibles.
- `resource-lease` : propriétaire, opération, admission/refus, résidence réelle, annulation, signal de fin effective, sans prétendre réserver directement la RAM Android.
- `health-status` : disponibilité/diagnostic minimal, valeur `unknown`, aucune fuite de chemins privés ou de prompts.

Les formats proposés peuvent être JSON Schema avec exemples valides et invalides + un document de sémantique. Éviter toute propriété qui impose HTTP ou Internet.

### 5.2 Contraintes d'architecture

- Transport **local** et remplaçable : Android IPC explicite/Binder ou autre mécanisme choisi ultérieurement ; pour mini-PC, transport local interchangeable. **Ne pas imposer le transport au niveau du contrat métier.**
- Contrôle d'identité des applications clientes, permissions, `exported=false` par défaut si pertinent, authentification si service exporté, réduction des données échangées.
- Gestion des indisponibilités : module absent, incompatible, non autorisé, interrompu, expiration, annulation, redémarrage, ressources insuffisantes. Pas de fausse réponse « réussite ».
- Versionnement rétrocompatible, negotiation de capacité et absence de changement destructif silencieux.
- **Politique d'un seul travail lourd/résidence modèle active à la fois** à l'échelle pertinente ; le coordinateur interne actuel de LLM ne régule pas les autres processus Android. Un arbitre IPC interprocessus restera à développer/tester.
- Protection des données historiques SQLite ; migration avec sauvegarde, restauration testée et accord explicite.
- Compatibilité Android : CORE historique `minSdk=24`, LLM prototype `minSdk=29` dans les états consultés ; ne pas promettre un lancement identique sur les deux anciennes cibles sans qualification.

**Livrables C :** contrats v1, exemples et `docs/PLAN_INTEGRATION_CORE_LLM.md` avec séquence précise d'implémentation à soumettre à approbation plus tard. Aucun changement de code dans CORE ou LLM.

## 6. Phase D — Audit automatisable en lecture seule

Implémenter dans UNIFIED un petit vérificateur reproductible, de préférence `scripts/audit_repos.py` avec Python standard uniquement.

### 6.1 Fonction minimale

1. Charger et valider le registre de dépôts.
2. En mode `--online`, lire les métadonnées de GitHub (branches, SHAs, PR/workflows/commits pertinents), avec un jeton **facultatif** fourni par l'environnement si nécessaire. Ne jamais écrire sur GitHub. Ne jamais afficher les jetons.
3. En mode `--offline`, lire des fixtures déterministes permettant de reproduire les vérifications sans réseau.
4. Produire un rapport JSON lisible et un résumé Markdown (`reports/` ou répertoire de sortie explicitement documenté).
5. Distinguer sans ambiguïté **preuve confirmée**, **déclaration**, **erreur de récupération**, **404**, **403**, **rate limit**, **absence de CI** et **preuve périmée**. Une erreur API n'implique jamais que le dépôt n'existe pas.
6. Enregistrer l'instant UTC de capture et la provenance des données sans inclure les tokens/headers sensibles.
7. Montrer les changements de ref entre un état archivé et un état relu ; **ne jamais conclure automatiquement** que le runtime Android fonctionne.
8. Sortie non destructive. Pas de commit automatique des résultats vers `main`.

### 6.2 Tests obligatoires du vérificateur

Créer `tests/` et des fixtures couvrant au moins :

- dépôt contenant seulement README ;
- branche `main` en retard sur une branche de mission ;
- CI réussie sans validation matérielle ;
- 404 / 403 / limitation API / timeout ;
- doubles dépôts ou alias ambigus ;
- preuve sans SHA, donnée inconnue ou horodatage périmé ;
- données sensibles dans un champ inattendu, test de non-publication ;
- modification d'un commit attendu entre deux captures.

### 6.3 CI de UNIFIED

Créer `.github/workflows/validate-unified.yml` pour lancer en PR : validation JSON/schémas, tests offline, cohérence des liens/IDs connus, absence de secrets évidents et vérification des fichiers attendus. Les appels live GitHub restent un job **manuel** (`workflow_dispatch`) facultatif, en lecture seule, et leurs échecs d'autorisation sont signalés sans produire un état trompeur.

**Livrables D :** script, tests, fixtures, procédure d'exécution et CI. Ni APK ni modèle GGUF ne sont construits ici.

## 7. Phase E — Pilotage et feuille de route exécutable

Rédiger :

- `docs/ROADMAP.md` : ordre des futures missions, dépendances, propriétaire et critères d'acceptation, distinguant COURT / MOYEN / LONG terme ;
- `docs/RISQUES.md` : double moteur en mémoire, pertes SQLite, régressions de voix, fuite des secrets, limites batterie/chauffe, IPC Android, dépendance GitHub au runtime, permissions GitHub 403 ;
- `docs/RUNBOOK.md` : comment produire une photographie d'état, enregistrer une nouvelle mission et répondre à la question « qu'est-ce qui fonctionne avec quoi ? » ;
- `docs/COMPTE_RENDU_CENTRAL.md` : **rapport de synthèse immédiatement réutilisable dans le chat JARVIS-CENTRAL**, contenant pour chaque module : rôle, dépôt, branche, SHA, fonctionnalités prouvées, tests, intégrations réelles, blocages, prochaine mission.

La feuille de route doit proposer au minimum :

1. Stabiliser et valider le CORE historique sur son commit actuel ; corriger ses défauts de concurrence/lifecycle/ressources sans perdre les fonctions.
2. Finaliser les essais matériels prudents de la branche LLM 003B ; conserver protections et profils de puissance.
3. Développer, sur **mission distincte et autorisée**, un adaptateur local CORE ↔ LLM à contrat versionné, avec tests d'indisponibilité, redémarrage, arrêt, mémoire et sécurité.
4. Définir les migrations de voix, documents et services un par un, en conservant le mode autonome pendant la transition.
5. Qualifier Android puis mini-PC ; PLEINE PUISSANCE seulement sur matériel qualifié.

## 8. Arborescence de livraison indicative

Ne pas produire des fichiers vides uniquement pour cocher cette liste ; adapter les noms avec justification, tout en conservant les capacités demandées.

```text
JARVIS-UNIFIED/
├── README.md
├── AGENTS.md
├── registry/
│   ├── repositories.json
│   └── modules.json
├── contracts/v1/
│   ├── capability-manifest.schema.json
│   ├── request-envelope.schema.json
│   ├── response-envelope.schema.json
│   ├── resource-lease.schema.json
│   └── health-status.schema.json
├── docs/
│   ├── INVENTAIRE.md
│   ├── PROUVES.md
│   ├── MATRICE_INTEGRATION.md
│   ├── PLAN_INTEGRATION_CORE_LLM.md
│   ├── ROADMAP.md
│   ├── RISQUES.md
│   ├── RUNBOOK.md
│   ├── COMPTE_RENDU_CENTRAL.md
│   └── DECISIONS/ADR-001-CORE-LLM-UNIFIED.md
├── scripts/audit_repos.py
├── tests/
│   ├── fixtures/...
│   └── test_audit_repos.py
└── .github/workflows/validate-unified.yml
```

`AGENTS.md` doit rappeler la séparation des responsabilités, l'interdiction de `main` sans accord, la hiérarchie des preuves, la sécurité des données et le rapport Codex obligatoire.

## 9. Critères d'acceptation — fin de Mission 001

La mission est **terminée** uniquement si les points suivants sont démontrés par fichiers et sorties réellement obtenues :

- [ ] Les dépôts accessibles et leurs alias/doublons sont inventoriés avec provenance datée ; les inaccessibles sont signalés explicitement.
- [ ] La distinction CORE historique / LLM spécialisé / UNIFIED coordination apparaît clairement dans le README et l'ADR en statut « proposition ».
- [ ] L'état réel des merges `main` et l'état réel des communications intermodules sont **deux mesures indépendantes**.
- [ ] La matrice rend impossible de confondre documentation, implémentation, CI et test matériel ; ses inconnues restent inconnues.
- [ ] Les fonctionnalités CORE historiquement intégrées et les redondances CORE/LLM/VOICE/NEXUS sont listées sans suppression.
- [ ] Contrats portables v1, exemples et cas d'erreur complets ; aucun transport cloud obligatoire.
- [ ] Script d'audit en lecture seule et mode offline, tests des anomalies, sorties reproductibles.
- [ ] Validation CI du dépôt UNIFIED réellement observée, ou blocage exact indiqué. Ne pas inventer une CI verte.
- [ ] `COMPTE_RENDU_CENTRAL.md` est compréhensible sans relire les anciennes conversations.
- [ ] Une roadmap intégrable par missions courtes et vérifiables est livrée.
- [ ] **Aucun fichier d'autre dépôt modifié, aucune fusion dans `main`, aucun secret publié.**

## 10. Contrôle final et compte rendu Codex

Avant remise :

1. Lister tous les fichiers changés et vérifier qu'ils appartiennent **uniquement** à UNIFIED.
2. Exécuter les tests offline et les validations disponibles ; donner **commandes exactes, totaux, échecs et limites**. Si possible, exécuter un audit GitHub en lecture seule, en indiquant les droits réellement utilisés.
3. Créer la branche dédiée, les commits et une PR vers `main` **non fusionnée**, si les permissions le permettent.
4. Publier un compte rendu final dans ce format :

```text
Module : JARVIS-UNIFIED
Mission : 001 — Consolidation
Dépôt : bubth720/JARVIS-UNIFIED
Branche : <nom réel>
Commit(s) : <SHA réels, ou non créés>
PR : <URL réelle, ou impossible + raison>
Inventaire : <nombre et identité des dépôts réellement vérifiés>
Matrice : <états des liens principaux, avec preuves>
CORE vs LLM : <doubles fonctions, frontières, action prévue>
Tests : <commandes, résultats réels, limites>
Blocages : <liste et conséquences>
État de main : <inchangée / autre situation vérifiée>
Prochaine action : <mission nommée, dépôt cible, critères>
```

### Condition d'arrêt

Si une écriture GitHub est interdite (HTTP 403) : **ne pas multiplier les tentatives destructives**. Préparer le patch/les fichiers et indiquer précisément la permission ou l'environnement manquant. Si la lecture d'un dépôt manque, ne pas conclure à son absence.

### Résultat attendu

À la fin, l'utilisateur doit pouvoir ouvrir **un seul README de UNIFIED** et comprendre immédiatement : **qui fait quoi ; ce qui est implémenté ; ce qui est déjà fusionné dans Git ; ce qui communique réellement ; ce qui a passé des tests ; ce qui reste à faire ; par quelle mission continuer**. Le dépôt devient un centre de coordination fiable, sans se substituer au runtime CORE et sans déployer silencieusement une intégration non vérifiée.
