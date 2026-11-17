# N01-A2 — contrats confrontés au code réel

Les orientations sont approuvées ; aucun contrat existant n’est modifié par cette livraison. « Conservé » signifie réutilisable dans sa portée prouvée, pas connecté à un nouveau runtime.

## Sources et méthode

Les cinq lectures GitHub exactes sont dans `evidence/five-repository-source-check.json`. Le contrôle local/CI recalcule le Git blob SHA sur chaque vrai checkout et vérifie l’ascendance du commit de référence. Le garde A2 conserve également les 503 fichiers du socle UNIFIED `6539b444`, octets et modes, notamment contrats v1, propositions UNI-08 et préparation GPU G03.

| Dépôt | Référence de code contrôlée | Preuve complémentaire |
|---|---|---|
| CORE | `f6a3b2d0`, `DocumentToolReadiness.kt` | `enabled=false` et `canExecute=false` ; un état de santé ne vaut ni admission ni autorité. Laboratoire JVM et mémoire G02 ne sont pas confondus |
| SERVICES | `7c7fc95a`, `CommitAuthorization.java` | `commit-proposal/1` reste une proposition non composée ; génération locale ≥0 ; consentement opaque, non sérialisable |
| NEXUS | `2dd4447a`, `RagTypes.kt` | Contrats métier identiques à REUSE ; ContextLimits, SearchScope, Citation et RagContextPort conservés ; CI JVM distincte |
| UNIFIED | `6539b444`, `request-envelope.schema.json` et vrais validateurs | Enveloppes fermées, modules/capacités énumérés ; tests de refus sur messages synthétiques |
| INTERFACE | `d2e737a9`, `LocalKnowledge.kt` | Chemin G02 local NEXUS `06ccf98`, Gateway et SQLite embarqué ; aucune permission Internet ajoutée |

Le dossier N01-A précédent conserve les autres fichiers lus, leurs empreintes et les locks CORE03. Le laboratoire CORE03 consomme NEXUS `777e6afa` et SERVICES `3decdc47`, différents des références actuelles. Aucun remplacement de pin n’est effectué ici. Les tests A2 de schéma ne qualifient pas le runtime CORE, l’IPC ou les appareils Android.

## Verdicts

| Élément proposé | Verdict | Adaptation nécessaire |
|---|---|---|
| Réutiliser `RagContextPort` / `DocumentaryGateway/1` pour une lecture locale autorisée | **CONSERVÉ dans sa portée** | Adapter les références locales, conserver chaque citation et revérifier l’autorité. Aucune lecture réseau dans NEXUS |
| Conserver document/révision/source/hash et offsets de citations | **CONSERVÉ** | Offsets UTF-16 du texte extrait ; hash RAW, hash d’archive et hash de fragment restent distincts. Tester toute normalisation future |
| Forme v1 de `document.retrieve` vers `nexus` | **COMPATIBLE syntaxiquement** | Le vrai validateur l’accepte. Cela ne prouve pas la disponibilité du producteur ni l’autorisation de l’appelant |
| Ajouter `research`, `profiles`, `data_vault` aux modules v1, ou `research.collect` aux capacités | **REJETÉ en v1** | Une enveloppe distincte/version négociée doit être revue ; ne pas modifier les enums actuels |
| Ajouter mission, licence, RAW ou policy directement au payload v1 | **REJETÉ en v1** | Métadonnées dans un manifeste local proposé et références bornées ; nouveau carrier à valider avant raccordement |
| RESEARCH seul composant réseau ; SERVICES transforme localement | **VALIDÉ architecturalement par l’utilisateur** | Corrige le placement ambigu du worker dans N01-A. Aucun transport n’est implémenté par A2 |
| `ServicesToolPort/1` et mécanismes d’aperçu/approbation existants | **CONSERVÉS** | Aucun ajout d’outil réseau et aucun export de production débloqué. Le champ d’autorité ne vient pas du document |
| Traduire génération locale 0 en wire 1 en ajoutant 1 | **REJETÉ** | Refus explicite à la frontière ; contrat d’adaptateur versionné, sans changer les fixtures historiques |
| Java long au-delà de 2^53−1, booléen ou valeur négative comme génération wire | **REJETÉ** | Pas de conversion silencieuse, troncature ou type coercion |
| `COMMIT_STARTED` → `DISPATCHED` ou `COMPLETED` → `COMMITTED` | **REJETÉ** | Décision d’autorité et effet durable distincts ; conserver UNKNOWN. Sémantique du futur reçu à faire approuver |
| Un booléen ou une référence textuelle comme preuve d’autorité CORE | **REJETÉ** | Port d’autorité réellement authentifié ; l’oracle A2 ne possède que des fixtures et n’autorise jamais de transport |
| Fiches de personnes stockées dans `identity/profiles` ou MEMORY VAULT | **REJETÉ** | Domaine documentaire NEXUS distinct ; ID de sujet distinct du nom ; aucune inférence psychologique |
| RAW/CURATED avec provenance, quotas et suppression | **VALIDÉ architecturalement, non implémenté** | Catalogue local versionné et stratégie de rétention à détailler sans migrer NEXUS v4. Les champs licence/rétention ne sont pas déjà fournis par le schéma actuel |
| Mission longue obtenue en augmentant le timeout v1 | **REJETÉ** | Décomposer en opérations bornées ; checkpoints et réadmission à chaque reprise |

L’outil UNI-08/U01 conserve son verdict BLOCKED même pour un reçu synthétique bien formé. Les nouveaux tests exécutent les validateurs actuels ; ils ne développent pas l’adaptateur de génération ou de reçus.

## Changements nécessaires, non appliqués

- Nouveau carrier local de mission/manifestes et adaptateurs versionnés, dans un namespace expérimental distinct, sans prétendre une compatibilité v1 directe.
- Frontière d’identité/autorité entre CORE et RESEARCH ; aucune valeur venant du LLM ou d’un document ne peut signer sa propre permission.
- Réception locale RAW et transformation SERVICES sans réseau ; conservation des occurrences de provenance et de licence même pour des octets identiques.
- Modèle documentaire de sujet/affirmation et politique de rectification/suppression, séparés de la mémoire et d’Athéna.
- Choix du canal Android et de l’authentification après examen sensible explicite. Rien n’est ajouté à AppGraph, aux modèles, aux bases ou aux manifestes.

Ces changements sont des exigences pour la prochaine mission, pas des modifications de contrat autorisées implicitement par A2.
