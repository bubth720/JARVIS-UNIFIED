# UNI-01 — Générateur de DTO et contrôleur de compatibilité des contrats

## 1. Identifiant et responsabilité
**ID :** UNI-01 ; **module :** UNIFIED ; **dépôt :** `bubth720/JARVIS-UNIFIED` ; **priorité :** P0 ; **dépendances :** Aucune.
**Base réellement vérifiée :** `decision/d4-02d-v1-v5-approved-2026-10-17` au commit `8ddac8fe8a1861a27d3abeca81eb4ab8f110c3a9`.
**Branche de dossier :** `plan/intensive-2026-10-22` ; **branche d'implémentation proposée :** `feat/uni-01-tooling`.
**Statut :** dossier préparé, exécution interdite sans attribution de l'utilisateur.

## 2. Code déjà livré et limites
UNIFIED héberge contrats v1, registre des modules/missions et ADR-001. La validation D4-02D V1–V5 ne s'applique qu'aux fixtures expérimentales. Il n'y a ni moteur Android ni runtime LLM dans UNIFIED ; aucune fonction ne doit y être ajoutée pour orchestrer l'utilisateur.

## 3. Objectif métier
Transformer les schémas contrats v1 du registre UNIFIED en sources Kotlin/Java générées reproductibles, avec comparaison de compatibilité machine. UNIFIED demeure hors runtime Android.

## 4. Fonctionnalités substantielles à programmer
1. Lire les schémas contracts/v1 figés et refuser clés ambiguës ou types non reconnus.
2. Générer DTO Kotlin/Java, énumérations typées, parseurs JSON stricts et validateurs de champs dans un dossier généré.
3. Créer empreintes de version canoniques et manifestes de schéma sans dépendre du temps d'exécution ni du réseau.
4. Coder CLI verify-contract comparant des manifests exacts : COMPATIBLE, INCOMPATIBLE ou UNKNOWN avec motifs et écarts.
5. Créer exemples de messages publics, tests aller-retour et vérifications d'Unicode/canonisation, taille et champs inconnus.
6. Documenter l'intégration de ces types dans CORE, LLM, VOICE, SERVICES, sans forcer de mise à jour de ces dépôts.

## 5. Architecture, classes et interfaces
1. ContractSchemaLoader, FrozenContractReader et SchemaError
2. DeterministicDtoGenerator + CanonicalJsonEncoder
3. ContractManifest + DigestCalculator
4. ContractCompatibilityChecker + ContractCli
Architecture claire : parsing du registre → domaine typé → outils CLI. Aucun appel automatique à des services extérieurs.

## 6. Fichiers réellement présents et fichiers projetés
1. À étendre en lecture : contracts/v1/, registry/ et scripts/validate_unified.py (existant)
2. À créer : tooling/contracts/{generator.py,manifest.py,compatibility.py,cli.py} et tests/contract_tooling/
3. À créer : contracts/generated/{kotlin,java}/ (sorties générées, versionnées après vérification)
Vérifier arborescence actuelle ; les chemins de tooling nouveaux sont des propositions.

## 7. Étapes d'implémentation
1. Comparer empreintes et champs existants avant de créer le générateur, sans modifier l'ADR.
2. Définir AST des contrats et règles explicites de compatibilité.
3. Implémenter génération déterministe de sources et manifestes.
4. Compiler sources générées avec Gradle de fixture ou test JVM, sans linker aux APK de production.
5. Exécuter exemples de refus sur versions/champs non autorisés et mesurer reproductibilité.

## 8. Technologies et dépendances
Python 3.12 standard pour tooling ; Kotlin/Java pour les DTO générés ; bibliothèques supplémentaires seulement après justification.. Garder possibilité d'un usage intégralement hors ligne. Ne pas remplacer silencieusement des dépendances ou schémas existants.

## 9. Connexions et ownership
Source de types pour les autres modules, pas de moteur LLM ni transport IPC.
Les modules restent propriétaires de leurs objets techniques et données ; les contrats sont distribués de manière volontaire, pas activés par modification de ce dépôt.

## 10. Sécurité et compatibilité
Pas de modification de `main`, `contracts/v1` figé, clés ou archives personnelles. Les outils ne peuvent lancer Codex, exécuter des patches ou déclencher une PR/merge. Codes de retour non nuls sur ambiguïté, compatibilité inconnue ou incohérence.

## 11. Livrables obligatoires
Code CLI effectif, schemas/types/manifests exploitables, tests minimaux passés, démonstration réelle sur registre de la campagne et rapport bref des écarts. Pas une mission de documentation uniquement.

## 12. Critères d'achèvement
1. Deux générations produisent les mêmes octets/empreintes sur les schémas figés.
2. Les classes générées compilent réellement et sérialisent les exemples canoniques.
3. Le validateur rejette un type de champ inattendu au lieu de modifier silencieusement contracts/v1.
Rejeter toute réussite inventée à partir d'une fixture insuffisante.

## 13. Dépendances et parallélisme
Aucune. UNI-01 peut être développé en parallèle de tous les P0 dans les autres dépôts ; UNI-02 suit UNI-01. Aucun autre agent ne doit changer simultanément les contrats figés.

## 14. Sécurité Git et approbations
Aucune mission lancée par dépôt de ce fichier. Attribution séparée, branche de code distincte, aucune fusion principale, aucun changement sensible transversal avant validation explicite.

## 15. Retour au coordinateur CENTRAL
Indiquer module, ID, branche, commit exact, fichiers codés, commandes et tests réellement exécutés, limites, blocages, risques de régression et prochaine action.
