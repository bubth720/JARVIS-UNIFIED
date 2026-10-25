# FUSION-01 F0 — architecture et composition candidate

Date d'observation : 25 octobre 2026. Mission directrice :
https://github.com/bubth720/JARVIS-UNIFIED/issues/4
Base UNIFIED : `329f304115c9bc5b6dd6ccc2d68d19bf455b5e6c`.
La branche de cette livraison est `feat/fusion-01-integration-lock`.

L'ADR-001 approuvée conserve CORE comme autorité de sessions/permissions/mémoire
confirmée et LLM comme autorité d'inférence. UNIFIED ne devient pas un runtime.
Cette tranche est F0 et un schéma F7 proposé hors ligne : aucun sous-lot applicatif
n'est développé dans le dépôt d'un autre propriétaire. Les sous-issues des sept
autres modules ont été lues intégralement, y compris UI03 ; leurs codes restent
sur leurs branches. Leur parallélisme n'autorise pas l'activation des gates.

## Choix unique, non encore intégrable

Le [verrou racine](../../integration-lock.json) choisit exactement un SHA primaire
par module. CORE `aea5ac…`, LLM `2efb3f…`, VOICE `fe5745…`, INTERFACE `db459b…`,
NEXUS API24 `374ea2…`, SERVICES API24 `f00091…`, EVOLUTION `c01801…`, UNIFIED base
`329f30…`. Les SHA complets, parents et empreintes sont dans le verrou ; les
branches candidates sont toutes inventoriées dans le
[snapshot distant](evidence/remote-heads.json).

La paire portable prépare API24 mais **n'est pas le tuple JVM historique** :
CORE03 utilise NEXUS `777e6a…` et SERVICES `3decdc…`, contenus/verrouillés dans
`docs/intensive-2026-10-22/CORE03-SOURCES.json` côté CORE. Modifier ce tuple réclame
un portage du consommateur et une nouvelle F1, pas seulement une substitution de
versions. Le module JDBC NEXUS a notamment changé d'emplacement. L'API extraite
SERVICES impose recompilation, sans promesse ABI binaire.

Les finales NEXUS `d903bf…` (v4/JDBC) et SERVICES `d16dd8…` (17 outils/min26)
divergent des ports. Les conserver comme alternatives de revue évite de jeter
leur bibliothèque/graph/outils, sans prétendre qu'ils sont présents dans le port.
VOICE07 diverge aussi du Studio final ; CORE-VOICE diverge du CORE mémoire/ID.
Les graphes et surfaces concurrentes sont dans les trois audits de ce dossier.

## Ownership et données

| Domaine | Propriétaire | Frontière à maintenir |
|---|---|---|
| Sessions, intentions, permissions, révocation | CORE | L'UI propose ; document, outil et LLM ne créent aucun grant |
| Souvenirs personnels confirmés | CORE actuellement | Confirmation du contenu exact ; historique SQLite intact ; cible NEXUS seulement après décision/migration réversible séparée |
| Inférence/résidence/tokeniseur | LLM/backend natif qualifié | Un lourd Android pilote, UNKNOWN bloque ; catalogue sélectionné ne signifie pas modèle actif |
| Sources/révisions/index/citations | NEXUS | Conserver URI/SHA/page/offset/version ; documents non fiables, jamais SYSTEM |
| Outils, aperçu et effets | SERVICES sous permissions CORE | ApprovalGate exact à usage unique ; ACK perdu = UNKNOWN, pas retry implicite |
| Voix, modèles/profils/horloge | VOICE | Pas de transfert de coffre ni preuve d'audibilité depuis PCM_READY |
| Présentation et avatar | INTERFACE | NON CONNECTÉ et AVATAR TECHNIQUE visibles ; aucune autorité supplémentaire |
| Observation/diagnostic | EVOLUTION | Données techniques expurgées ; correctif inerte, sandbox non qualifiée |
| Contrats/BOM/preuves | UNIFIED | Outillage de développement hors ligne, aucune admission runtime |

## Plateformes et distribution

La [matrice BOM](BOM.md) distingue compatibilité de surface et qualification du
produit. SUPPORTED signifie seulement le périmètre logiciel expliqué dans le
verrou ; les rapports détaillent compilation, simulations et émulateurs historiques.
Aucun nouvel essai API24/25/26/29/35, ARM64, POCO, Redmi ou mini-PC n'est exécuté ici.
CORE reste min24 ; LLM APK min29, INTERFACE/Studio VOICE min26. EVOLUTION reste JVM.
Le matériel mini-PC n'est fourni/qualifié pour aucun module.

Aucune licence projet racine n'a été identifiée aux SHA inspectés : UNKNOWN.
Les licences des dépendances ne permettent pas de redistribuer les projets, voix,
poids ou portraits privés. Pas de nouvel asset/modèle/binaire publié. Un futur SBOM
de distribution doit qualifier licences/ABI/provenance/empreintes exactes ; ce BOM
de sources n'est pas un SBOM exhaustif des dépendances transitives ni un manifeste
prêt à installer.

## Ordre concret et rollback

1. Recevoir F0 et examiner les conflits ; aucun changement de l'orientation ADR.
2. CORE C0/C1 : relancer le vrai integration-lab épinglé, puis porter son consommateur
   sur les bibliothèques candidates dans une branche CORE, avec conservation de l'ancien tuple.
3. NEXUS : corriger sa CI de préparation Android, qualifier une solution FTS5 avec
   licence/ABI, puis porter v4 sur copies synthétiques. SERVICES : isoler l'échec
   CI API24, porter les outils et le DOCX après qualification SAF/consentement.
4. F2 seulement après nouvelles preuves ; préserver 501 résultats historiques
   MEM/ID comme historiques tant qu'ils ne sont pas relancés sur le nouveau SHA.
5. UI peut proposer le protocole contenu/citations/consentements sans activer IPC.
   F3/F5 restent soumis aux preuves natives et autorisations sensibles distinctes.
6. EVOLUTION peut revoir le schéma technique fermé proposé ; aucun runner ni accès croisé.

Rollback de cette tranche : revenir au SHA central précédent pour l'outillage.
Aucune donnée utilisateur ni installation n'a été modifiée, donc aucune restauration
physique n'est requise. Garder anciens rapports/branches et ne pas les réécrire.
