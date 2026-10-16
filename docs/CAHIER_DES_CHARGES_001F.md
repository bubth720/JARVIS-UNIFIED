# JARVIS-UNIFIED — MISSION 001F
## Clôture de la consolidation, publication vérifiable, revue ADR et bilan global JARVIS

**Date de référence : 15 octobre 2026**  
**Dépôt de travail exclusif :** `bubth720/JARVIS-UNIFIED`  
**Type :** continuation de la Mission 001 (ne pas repartir de zéro)  
**Rôle :** mission Codex ; aucun changement dans les dépôts des autres modules.

## 0 — Objectif et état de départ

Rendre l'audit et la consolidation précédemment réalisés **visibles, reproductibles et utiles à JARVIS-CENTRAL**, puis préparer une décision d'architecture humaine. Ne pas confondre la publication d'un registre central avec une connexion réelle entre applications.

État **rapporté** par l'exécution précédente, à vérifier localement avant toute action :
- Branche locale `mission-001-architecture-unified`, commits `61b30fc` et `d74730a` ; 51 fichiers ajoutés ou modifiés, 80 tests locaux rapportés réussis (27 audit/contrats, 23 registre, 30 sauvegarde).
- Branche de travail précédente `mission-003-central-registry` préservée à `f7b7a5a`.
- Remote `main` à `e4435f4` et uniquement `README.md` ; la publication de `mission-001-architecture-unified` a échoué avec HTTP 403 ; aucune PR distante.
- Une ADR (décision d'architecture) est **proposée, NON APPROUVÉE**.
- Aucun contrat IPC fonctionnel CORE↔LLM, CORE↔VOICE n'est démontré.

Les SHA ci-dessus sont des identifiants de référence **à recontrôler** dans l'environnement Codex, non des preuves d'accès aux objets locaux par ChatGPT.

## Règles non négociables

1. Modifier **uniquement** `JARVIS-UNIFIED` sur une branche de travail dédiée. Les autres dépôts sont accessibles en **lecture seule**. Ne jamais fusionner dans `main`, ni le modifier ou le réécrire, sans validation explicite de l'utilisateur.
2. Préserver tous les commits et travaux antérieurs, notamment `mission-003-central-registry`. Interdiction de `push --force`, `reset --hard` destructeur, suppression de branches, rebase risqué ou écrasement de contenu.
3. Ne jamais divulguer de jetons, secrets, URLs Git contenant des credentials, données vocales personnelles, archives chiffrées privées ou clés de signature. Aucun contournement d'autorisation, de proxy ou de politique de sécurité.
4. Distinguer constamment : **prévu / code présent / testé localement / CI distante validée / testé physiquement / intégré de bout en bout**. Un DTO, un contrat ou un test isolé ne prouve pas une connexion inter-applications.
5. Aucun ajout de fonctionnalité produit et aucun raccordement CORE↔LLM/VOICE pendant cette mission. Toute décision ADR reste `PROPOSED` jusqu'à acceptation écrite distincte de l'utilisateur.
6. Exécuter les tests existants sans falsifier résultats, dates ou SHA. En cas d'impossibilité, consigner « non exécuté » avec cause.
7. Préserver la compatibilité Android, la sobriété thermique et énergétique, les données locales, les signatures APK et la possibilité de migrer vers un mini-PC. Aucun cloud obligatoire à l'exécution.

## PHASE A — Préservation et diagnostic HTTP 403

### Travail
- Constater le répertoire courant, `git status --porcelain`, `git branch -vv`, remotes **assainis de tout credential**, `git log --all --oneline --decorate`, l'ascendance des commits attendus et la présence des fichiers de mission. Relever la branche, les SHA et le statut de l'arbre.
- Vérifier l'existence et l'intégrité des commits cités ; protéger les deux branches de travail. Créer et vérifier un bundle Git de récupération couvrant les branches utiles (avec empreinte SHA-256 et procédure de restauration). Ne pas inclure des fichiers de secrets ou d'artefacts privés.
- Diagnostiquer séparément lecture et écriture : accès à `origin`, droits du jeton/installation de l'environnement Codex, permission GitHub `Contents: write`, autorisation de dépôt, session expirée, contraintes de proxy et protections de branche. Utiliser des contrôles non destructifs ; ne jamais afficher de secret.
- Expliquer de façon falsifiable la source probable du 403. Si elle n'est pas confirmée, distinguer hypothèses des causes observées et fournir à l'utilisateur les étapes de configuration à effectuer lui-même.

### Acceptation A
- Branches et commits historiques préservés, arbre non altéré hors mission.
- Bundle de secours **restaurable**, SHA-256 fourni, procédure de récupération vérifiée dans un emplacement isolé lorsque possible.
- Diagnostic écrit du 403 avec commandes expurgées, réponse du serveur et actions utilisateur nécessaires ; aucun secret exposé.

## PHASE B — Publication contrôlée et PR sans fusion

### Travail
- **Seulement si l'écriture GitHub est autorisée**, pousser sans forçage `mission-001-architecture-unified` ou une branche de reprise explicitement documentée (ne pas remplacer l'historique antérieur).
- Vérifier sur GitHub les SHA distants réellement publiés et le nombre de fichiers, comparer la branche locale/distante, ouvrir une **PR brouillon** vers `main` contenant résumé, liens vers les preuves, état des tests, limites et risque de régression.
- Confirmer que `main` reste inchangée ; ne jamais activer l'auto-merge. Toute approbation d'ADR et toute fusion nécessitent une décision ultérieure de l'utilisateur.
- **Si HTTP 403 persiste :** s'arrêter proprement avant publication, conserver le bundle, fournir son chemin téléchargeable depuis l'environnement Codex et une procédure de restauration/publication par la voie GitHub autorisée. Ne jamais déclarer la mission publiée.

### Acceptation B
- Soit URL de branche distante, SHA, PR brouillon et vérification que `main` n'a pas bougé ; soit **blocage explicitement documenté + bundle vérifié**, sans perte de travaux.

## PHASE C — Revue complète de l'ADR (sans l'adopter)

### Travail
- Lire l'ADR proposée et les contrats v1 **réellement présents**. Reprendre leur état `PROPOSED`, relever les contradictions et les dépendances.
- Comparer trois options : (1) monolithe Android, (2) applications Android indépendantes reliées par IPC local, (3) architecture hybride modulaire avec un CORE orchestrateur et adaptateurs interchangeables. Exposer coûts, risques, migration et critères de choix.
- Préciser la responsabilité de chaque composant : CORE = orchestration/décisions/permissions ; LLM = inférence locale ; VOICE = audio/synthèse ; INTERFACE = UI/avatar ; NEXUS = documents/mémoire ; EVOLUTION = audit/correctifs isolés ; SERVICES = outils optionnels ; UNIFIED = registre, contrats, preuves et gouvernance (pas un moteur d'exécution).
- Définir à titre de **proposition** : propriétaire unique des sessions, un modèle lourd actif à la fois, budget thermique/batterie/mémoire, autorisations IPC Android (identité appelant, permissions, exported=false par défaut), versionnement et sérialisation des messages, annulation, expiration, panne/mort de processus, dégradation hors ligne et compatibilité mini-PC. Prévoir migration non destructive des historiques et données.
- Construire une page de **décision utilisateur** : recommandation motivée, alternatives, points ouverts et question d'approbation. Ne pas modifier le statut de l'ADR ni la considérer acceptée.

### Acceptation C
- ADR relue et commentée avec preuves et alternatives ; statut toujours `PROPOSED` / `AWAITING USER APPROVAL`.
- Aucun moteur CORE réécrit ; aucune API IPC annoncée comme active avant essais de bout en bout.

## PHASE D — Audit global des modules avec preuves GitHub

### Périmètre minimum à inspecter en lecture seule
1. `bubth720/JAVIS-Local-v2` (candidat CORE historique ; vérifier plutôt qu'affirmer l'équivalence absolue).
2. `bubth720/JARVIS-LLM`.
3. `bubth720/JARVIS-VOICE`.
4. `bubth720/JARVIS-INTERFACE`.
5. `bubth720/JARVIS-NEXUS`.
6. `bubth720/JARVIS-SERVICES`.
7. `bubth720/JARVIS-VOLUTION-` (candidat EVOLUTION, ne pas supposer qu'il correspond au dépôt attendu).
8. `bubth720/JARVIS-UNIFIED`.
9. `bubth720/JARVIS-INTERFACE-` (doublon/candidat à identifier, ne pas supprimer).

Chercher aussi les autres noms exacts CORE/EVOLUTION si l'accès les autorise, et signaler clairement `404`, `403`, non accessible, plutôt que conclure « inexistant ».

### Travail
- Pour chaque dépôt : URL, identité/alias, branche par défaut, branches importantes, commit SHA, dernier code significatif, fonctions réellement présentes, statut des tests locaux et GitHub Actions avec URL/date/SHA, essais physiques, fonctionnalités manquantes et risques.
- Vérifier en particulier : CORE continue-t-il d'utiliser `LlamaLocalEngine` interne ? LLM expose-t-il une connexion IPC réelle ? VOICE expose-t-il seulement un DTO CORE→VOICE ? INTERFACE est-elle autonome ? Quels autres dépôts se limitent à un README ?
- Documenter la **matrice de communication réellement vérifiée** : CORE↔LLM, CORE↔VOICE, CORE↔NEXUS, CORE↔SERVICES, CORE↔INTERFACE et coordination de ressources entre processus ; classer `aucun`, `contrat seul`, `intégration testée`, `essai physique`, avec preuve pour chaque ligne.
- Distinguer les branches de développement des branches `main`. Une réussite CI sur une branche non fusionnée ne signifie pas que `main` contient la fonctionnalité.
- Vérifier les résultats de tests rapportés pour la mission de consolidation : 27 audit/contrats + 23 registre + 30 sauvegarde = 80 annoncés localement. Fournir les commandes, logs, sorties et nombre exact. Indiquer les tests non exécutables.
- Rédiger un bilan compréhensible pour JARVIS-CENTRAL, sans transformer objectifs, conversations, mocks, simulateurs ou documents en preuves de fonctionnement réel.

### Acceptation D
- Neuf dépôts examinés ou limite d'accès documentée individuellement.
- Tableau central par module + matrice des intégrations + références SHA et CI consultables.
- Risques classés par gravité, différence nette entre « développé », « validé » et « opérationnel ensemble ».

## PHASE E — Feuille de route vérifiable et restitution centrale

### Travail
- **P0 :** publication UNIFIED, revue ADR humaine, stabilisation CORE sur la tête actuelle, qualification prudente LLM 003B sur Redmi et POCO, tests VOICE 005I sur Xiaomi avec données privées conservées, résolution/diagnostic CI INTERFACE.
- **P1 :** après accord ADR, spécifier et tester le premier parcours bout en bout **CORE → LLM → CORE**, sans second modèle résidant et avec annulation, sécurité et maintien du mode local. Tests d'abord, déploiement séparé après consentement.
- **P2 :** intégrer VOICE via contrat local, puis interface, NEXUS, SERVICES selon dépendances prouvées ; préserver les fonctions historiques CORE jusqu'à parité testée.
- **P3 :** développer EVOLUTION isolé et la montée en gamme mini-PC ; aucun auto-déploiement de correctifs sans validation explicite.
- Pour chaque mission future : dépôt propriétaire, objectif limité, branche, dépendances, fichiers prévus (si connus), critères testables, risques, validation humaine, condition de non-régression.
- Produire une section **« Que faire dans chaque chat »** : JARVIS-CENTRAL gouvernance ; CORE stabilisation et orchestration ; LLM moteur et mesures ; VOICE synthèse et identité ; INTERFACE avatar 2.5D ; NEXUS Wikipedia/Kiwix, documents et mémoire ; EVOLUTION sandbox et correctifs ; SERVICES modules optionnels. Les chats ne constituent pas des preuves de code.
- Ajouter un mode opératoire pour actualiser l'inventaire à chaque PR/fusion approuvée, sans laisser les snapshots obsolètes devenir « état actuel ».

### Livrables à conserver dans `JARVIS-UNIFIED`
Réutiliser en priorité les 51 fichiers existants et l'organisation de la branche ; ne pas créer de doublons inutiles. Au minimum, exposer clairement :
- `README.md` central avec rôles et liens.
- Inventaire des dépôts et commits sourcés.
- Matrice réelle des intégrations / contrats v1.
- ADR proposée et note de décision non approuvée.
- Rapport central `JARVIS_CENTRAL_BILAN_GENERAL.md` (ou chemin justifié).
- Feuille de route priorisée et missions Codex distinctes.
- Rapport tests/CI, runbook de reprise 403 et d'actualisation.
- Bundle de sauvegarde et son SHA-256 disponibles via l'environnement Codex **hors Git**, si publication impossible.

### Acceptation E
- Un lecteur peut répondre pour chaque module : « à quoi sert-il ? quel code existe ? quel SHA ? quelles validations ? qui lui parle réellement ? que faut-il développer ensuite ? ».
- Prochaines missions petites, dépendances explicites, aucune tâche présentée comme déjà faite.
- Rien fusionné dans aucun `main` sans accord utilisateur ; ADR laissée en attente.

## Format de compte rendu final obligatoire

1. **Publication :** état 403 (résolu ou non), branche locale/distante, commits, PR/URL, `main` distant, bundle + empreinte.
2. **Architecture :** ADR proposée, décisions demandées et objections.
3. **Bilan :** tableau des 8 composants et des 9 dépôts avec SHA / tests / limites.
4. **Connexions :** matrice inter-applications fondée sur le code et les tests ; mention `non prouvé` si applicable.
5. **Validation :** commandes exécutées, résultats, écarts par rapport aux 80 tests annoncés.
6. **Roadmap :** P0/P1/P2/P3, propriétaire et portes de validation.
7. **Risques :** sécurité locale/IPC, mémoire RAM, thermique/batterie, signatures, perte de données, duplication de moteurs et régressions.
8. **Action utilisateur nécessaire :** étapes exactes pour résoudre 403, examiner l'ADR et autoriser séparément les missions suivantes.

**Définition de « terminée » :** audit et livrables locaux validés ; publication et PR seulement si les autorisations fonctionnent. Si 403 persiste, la livraison demeure **« terminée localement, publication bloquée »**. Aucune phrase ne doit laisser croire que CORE↔LLM ou CORE↔VOICE est intégré sans test bout en bout et preuve reproductible.
