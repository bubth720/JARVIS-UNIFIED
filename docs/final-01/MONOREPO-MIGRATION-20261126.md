# JARVIS-FINAL-01 — Transition vers un dépôt unique

**Statut au 26/11/2026 : M0, fondation technique de migration ; les modules ne sont PAS encore importés ni qualifiés ensemble.**

## Décision de propriété

- Dépôt central : `bubth720/JARVIS-UNIFIED`, devenu le futur MONOREPO source de vérité pour le code.
- Branche de migration : `feat/final-01-monorepo-foundation-20261126`, basée sur la coordination F00/F01 @ `cb04988f71217a1ae486185d269aa9794dcc10ca`.
- Les sept anciens dépôts restent en lecture/référence tant que le code et son historique nécessaires ne sont pas repris et que les tests ne sont pas passés.
- **Pas de merge vers `main`, pas de changement de branche par défaut, pas d'archivage, de suppression de données ou de retrait d'un module sans réception explicite.**
- L'objectif n'est pas de copier aveuglément tous les anciens commits, PR, captures et binaires : c'est de conserver les sources actuelles qualifiées avec provenance et contrat.

## Organisation cible

| Répertoire dans UNIFIED | Responsabilité | Condition |
|---|---|---|
| `modules/core/` | Orchestrateur et autorité unique (mémoire, sessions, permissions) | Conserver la mémoire consentie `mem-02` |
| `modules/llm/` | Moteur local unique derrière un port interchangeable | Modèle GGUF hors ligne, budgets thermique/RAM |
| `modules/voice/` | STT/TTS et expression vocale locale | Audio réel non qualifié sur appareil |
| `modules/interface/` | Cockpit Android V3, avatar et accessibilité | S04 API29/35 baseline |
| `modules/nexus/` | Documents, index et citations | Les sources n'ont aucune autorité de commande |
| `modules/services/` | Actions à permissions explicites | Tout effet réel désactivé par défaut |
| `modules/evolution/` | Diagnostic, comparaison, revue humaine | `SANDBOX_NOT_QUALIFIED`, jamais de patch exécuté |
| `tooling/monorepo/` | Provenance, import local, contrôles d'intégrité | N'écrit jamais dans les dépôts sources |

**Important :** cette arborescence est la **cible de migration**. Les nouveaux fichiers de cette branche sont de l'outillage de préparation, pas la preuve que le runtime intermodule a été intégré.

## M0 — Fondation (cette branche)

1. F00/F01 restent intacts. Les 90 PR maillons ont été fermées sans supprimer branches ni commits ; 26 PR brouillons demeurent ouvertes, dont les trois nouvelles revues #30 / INTERFACE #25 / EVOLUTION #7.
2. `tooling/monorepo/sources.lock.json` conserve les SHA complets des sept modules. CORE/LLM/VOICE/INTERFACE/NEXUS sont les révisions V3 S04 **déjà épinglées** ; SERVICES et EVOLUTION sont des sources **isolées**, non embarquées.
3. Les révisions candidates plus récentes de LLM/VOICE/NEXUS restent **NO-GO** pour mise à niveau de l'APK jusqu'à de nouvelles campagnes d'intégration API29/35.
4. `validate_sources.py` vérifie hors ligne chemins, SHA, identités des dépôts, statut des candidats et règles de sécurité.
5. `stage_local_sources.py` fabrique, à partir de sept dépôts Git **déjà présents localement**, un snapshot de code source unique dans un **nouveau dossier**. Il lit les blobs des commits épinglés par `git archive` ; il ne fait ni fetch, ni clone, ni commit, ni push, ni suppression.
6. Exclure les workflows historiques internes, le build généré, les binaires de modèles, les APK, clés privées/keystores et bases locales. Conserver un rapport d'origine et les empreintes des archives.

## Utilisation par Codex (dans un environnement avec les sept clones en lecture)

1. Cloner le nouveau dépôt de coordination sur sa branche de migration (pas de commande automatique dans ce document).
2. Mettre à disposition des clones locaux dans `/workspace/sources/{core,llm,voice,interface,nexus,services,evolution}`. Chaque clone doit contenir l'objet Git du commit choisi.
3. Exécuter `python3 tooling/monorepo/validate_sources.py`.
4. Exécuter `python3 -m unittest discover -s tooling/monorepo/tests -v`.
5. Exécuter `python3 tooling/monorepo/stage_local_sources.py --sources-dir /workspace/sources --destination /workspace/JARVIS-SNAPSHOT-NEW`.
6. Lire le rapport `SOURCE-SNAPSHOT-REPORT.json`, examiner les exclusions, la provenance, les licences et les fichiers avant **tout ajout Git** sur une branche candidate distincte.

Un snapshot n'est ni un build ni une APK : c'est seulement le matériel source pour M1. Les répertoires sources existants ne sont jamais modifiés.

## M1 — Import du code réel

- Valider l'inventaire du snapshot, les licences, la suppression d'artefacts sensibles et les doublons.
- Importer les sept modules sur **une branche candidate**, sans copier leur historique Git en un énorme graphe de commits ni écraser F00/F01.
- Conserver les liens SHA vers leurs dépôts originaux ; créer un test de cohérence des imports ; minimiser la duplication du runtime Android.
- Ne pas supprimer les dépôts d'origine à cette étape.

## M2 — Une application Android, un CORE, un LLM

- Conserver une application Android de référence à partir d'INTERFACE V3 S04 ; adapter Gradle et les namespaces pour compiler les modules locaux par chemins.
- Écrire le successeur de verrou `labs/v3/sources.json` en conservant intégralement `labs/v1/sources.json` et ses 430 fichiers gardés.
- Migrer progressivement le cycle de conversation de l'adaptateur INTERFACE vers CORE selon ADR-F01-01 M1–M5, avec tests de parité et drapeau de retour arrière.
- Activer uniquement les fonctionnalités ayant passé les contrôles de contrat et les tests en émulation.

## M3 — Qualification

- CI JVM/Android, tests API29/35, tests négatifs sur permissions/mémoire/absence de réseau/modèles invalides.
- Réception `DEVICE-01` sur téléphone réel : microphone → STT → LLM local → TTS, température, RAM, batterie et stockage.
- NEXUS, SERVICES et EVOLUTION activés séparément ; EVOLUTION reste lecture seule si sandbox non qualifiée.
- Release signée seulement après validation du propriétaire.

## M4 — Réduire réellement l'encombrement GitHub

- D'abord clarifier si le « 100 % » concerne Actions storage, minutes, LFS, Packages ou autre ; ne pas l'attribuer automatiquement aux PR.
- Inventorier par ID les artefacts expirés/obsolètes ; protéger les preuves S04 et les dernières APK utiles. Les suppressions d'artefacts doivent être chiffrées et tracées.
- Réduire la durée des **futurs** artefacts de démo, sans effacer les preuves de qualification.
- Après import vérifié : possibilité d'archiver les dépôts historiques ; ne pas les supprimer avant preuve d'équivalence et validation explicite des SHA.

## Critères d'acceptation

- Le monorepo contient réellement les sept sources nécessaires, aucune clé ni poids privé, et une seule chaîne de build Android.
- Contrats CORE/LLM/VOICE/NEXUS préservés ; aucune régression des tests S04.
- Fonctionnement Android hors ligne vérifié en émulation **et sur appareil**.
- Les fonctions encore expérimentales sont indiquées BLOCKED/OFF, jamais réputées opérationnelles.
- Aucun merge dans `main` sans approbation par commit et branche.

**M0 n'atteint pas encore ces critères.** Prochaine mission : M1, import et construction de la source intégrée par Codex dans son environnement de build.
