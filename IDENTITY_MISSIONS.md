# Programme IDENTITY V1 — missions et compte rendu ID-001

**Proposition, non implémentée.** Seule ID-001 est réalisée ici : documentation
UNIFIED. Les missions ID-002 à007 ci-dessous restent à autoriser dans leurs dépôts.
L’utilisateur garde la décision finale ; aucune validation de l’ADR, d’IDENTITY,
d’un contrat concret ou d’une qualification physique n’est déduite d’une autre.

## Dépendances et portes d’approbation

ID-001 documentaire progresse indépendamment du raccordement CORE–LLM. Le code
LLM003F observé est candidat bloqué F1/F2/F3 et revue de commit ; CORE004D n’est
pas une intégration disponible présumée. **Aucun travail IDENTITY dans /2.**
Cette mission ne résout pas les blocages de transport et ne lance pas ces missions.

Ordre proposé : approbation constitution/frontières/contrats/sécurité ID-001 →
revue de base CORE compatible → ID-002 ; ID-003 après choix stockage/port ;
ID-004 après ses interfaces de preuve et le socle CORE. ID-005 VOICE et INTERFACE
peuvent avancer séparément après contrats/capacités validés. ID-006 indépendant,
non bloquant pour une Alpha conversationnelle. ID-007 seulement sur les fonctions
réellement implémentées, avec absences explicites et accord de laboratoire séparé.
Un module absent n’est pas remplacé par un doublon silencieux.

| Décision encore à prendre | Proposition soumise |
|---|---|
| Identité B détaillée | Constitution franche/calme/critique, chaleur sobre et humour facultatif, limites non négociables hors préférences |
| Hébergement ID-003 | Namespace privé identity.* dans SERVICES comme fournisseur initial, NEXUS cible domaine, CORE autorité ; aucune migration des bases existantes |
| Structures/codecs/digests | jarvis.identity/1-draft à figer avec bornes/vecteurs ; pas modification UNIFIED v1 ou fixture /2 |
| Consentements/rétention/restauration | Confirmation exacte, brouillon personnel volatil, révisions et révocations, rollback ; chiffrement/gestion de clé à qualifier avant données privées |
| Prompt et base CORE | Composer local sans nouveau moteur/permission, comptage réel pour chemin P2, base choisie après revue004D/intermédiaires ; aucune fusion imposée |
| Expression/évolution | Capacités VOICE/INTERFACE prouvées seulement, EVOLUTION isolé sans auto-application ; validation de nom/rôle du dépôt candidat avant ID-006 |

## ID-002 — moteur de personnalité CORE

Dépôt : bubth720/JAVIS-Local-v2.
Branche proposée : `feature/identity-002-core-runtime`.
Dépendance : ID-001 approuvée et types/bornes figés, revue de compatibilité de la
base CORE avec004D et missions intermédiaires au moment du lancement. da40ed7
est une référence **d’audit**, pas la base d’implémentation automatiquement imposée.
Aucune fusion des branches historiques/fixtures pour produire cette base.

Périmètre court : IdentityManifest/Snapshot/Policy/Composer/Port ; manifeste technique
approuvé embarqué, état personnel volatil tant qu’un port validé est absent.
Chemins **proposés** : app/src/main/java/com/stark/jarvislocal/identity/,
tests identity et docs/identity-002/. Relire AppGraph, JarvisCore, PromptBuilder,
InferenceContract, SessionCoordinator ; adaptateur limité au SYSTEM/budget/snapshot.
Pas de second routeur, catalogue, backend ou stockage parallèle.

Tests : snapshot identique après redémarrage du manifeste, chargement/corruption/
version/refus, contenu SYSTEM exact et non copié en user, budget avant/après rendu,
annulation et snapshot révoqué, plusieurs modèles compatibles sans formulation
identique imposée, non-régression CORE historique/API24 et absence de permission
Android nouvelle. Tests de persona sur corpus synthétique, modèle et seeds signalés.

Acceptation : aucun changement par défaut du moteur historique ni données, un
seul lourd, manifeste/version stables, dépassement explicite sans troncature
cachée, aucun rôle/permission créé par prompt, suites existantes réussies ou
blocage précisément décrit. Sans port durable qualifié, seule continuité du
manifeste technique est revendiquée, pas de préférences personnelles persistantes.
Les fixtures /2 et leurs corpus restent byte-identiques.

## ID-003 — préférences et continuité

Dépôt initial : bubth720/JARVIS-SERVICES.
Branche proposée : `feature/identity-003-state`.
Dépendances : ID-001 approuvée, choix d’hébergement/port/format/consentement validé ;
coordination NEXUS future, aucune implémentation NEXUS présumée.

Périmètre : namespace identity.* distinct, propositions PENDING/APPROVED/REJECTED,
application séparée, CAS, révocation/expiration et export/restore de **fixtures**.
Relire shared-runtime/.../modules/{guard,memory}, shared/storage/{Store,Recovery},
shared/api/Contracts ; proposer une couche identité versionnée dans shared-runtime
avec tests et docs/identity-003/. Ne pas ajouter des champs aux schémas SERVICES
v1 fermés ou détourner Memory.type pour stocker sans contrat une nouvelle catégorie.
Réemployer les primitives compatibles, adaptateurs explicites ; pas de nouvelle DB
concurrente des souvenirs CORE ou de catalogue LLM.

Tests : confirmation exacte et contenu modifié/rejeu refusés ; proposition personnelle
volatile sans consentement propre ; transaction ratée après consume et reprise sans
fausse approbation ; conflit de révision ; corruption ; export chiffré/borne/secret
manquant ; restore avec ancienne révocation et panne simulée ; journal et rollback
vérifiés ; bases historiques et namespace non ciblés inchangés.

Acceptation : propriétaire unique, aucun souvenir durable sans confirmation, aucune
migration de CORE/NEXUS/VOICE ; journal privé durable distinct de l’audit GUARD borné,
restauration démontrée sur fictif, contrat de consommation ID-002 documenté sans
supposer un IPC existant. Chiffrement/format et clés validés avant données privées.
Compatibilité de la cible NEXUS décrite, aucune synchronisation automatique.

## ID-004 — sens critique et contradiction

Dépôt : bubth720/JAVIS-Local-v2.
Branche proposée : `feature/identity-004-critical-dialogue`.
Dépendances : socle ID-002 et contrat d’évaluation/provenance validés ; pas de
dépendance à un NEXUS opérationnel ni à un EVOLUTION inexistant. ID-003 nécessaire
seulement pour préférences durables, pas pour un test critique volatil.

Périmètre : classification bornée de nature de proposition, accès aux preuves
locales autorisées existantes, règles d’incertitude/fraîcheur et nouvelle preuve
utilisateur. Chemins proposés : core identity/critical, adaptateurs RAG/source
existants, tests/corpus et docs/identity-004/. Calculs déterministes réemployés,
pas de second modèle/fact-checker/index et pas de citations produites sans source.

Tests : corpus figé avec faits vrais/faux démontrables, opinions légitimes, hypothèses,
préférences/instructions et questions sans preuve ; données locales périmées ;
nouvelles preuves contradictoires ; document contenant fausses instructions système ;
flatterie, contradiction artificielle et insultes ; annulation/absence de source.
Mesurer corrections justifiées, faux désaccords, citations valides et reconnaissance
d’incertitude par catégorie. Fixer seuils avant exécution, conserver les échecs ;
la seule présence du mot « non » ou un auto-jugement LLM n’est pas un oracle.

Acceptation : verdict lié aux sources/révisions, aucune citation inventée dans le
corpus, pas d’action/mémoire dérivée du verdict, désaccord respectueux et révisable,
aucun nouveau lourd ni baisse de sécurité. Validation humaine séparée du score
modèle ; pas de promesse de correction factuelle universelle.

## ID-005 — deux missions d’expression indépendantes

**ID-005V**, dépôt bubth720/JARVIS-VOICE,
branche proposée `feature/identity-005-voice-expression`.
Dépendances : ID-001/contrat d’intention validés, texte final autorisé et chemins
réels disponibles. Relire expressionRuntime/ExpressionContract, ExpressionPolicy,
LocalProsodyPlanner et lecteurs/caches existants ; adaptateur persona/intent et tests
séparés proposés, sans modifier CoreVoiceRequestV1 ni les profils privés.
Tests : mapping de style, profil/pack/conditioning erronés, effet non supporté
signalé, neutralité comparable, limites300caractères/tokenizer/durée, annulation
et zéro nouvelle lecture après révocation. Aucune réécriture/troncature cachée.
Acceptation : réemploi VOICE, aucune modulation acoustique non prouvée annoncée,
aucun TTS générique substitué, profils/consentements intacts. Latence/RAM/thermique
mesurées sur matériel compatible avant activation par défaut, sinon non qualifiée.

**ID-005I**, dépôt bubth720/JARVIS-INTERFACE,
branche proposée `feature/identity-005-avatar-intents`.
Validation et commit séparés de VOICE. Relire avatar/AvatarContract, state/layout et
cycle de vie existants ; intentions visuelles typées bornées, adaptateur/session
proposés sans nouveau renderer/média chargé implicitement. Test visibilité,
masquage/release, réponse tardive/cancel, orientation et absence de ressource
persistante en arrière-plan ; fluidité/consommation à mesurer séparément.
Acceptation : aucun avatar opérationnel revendiqué si seul contrat livré ; aucune
permission/core authority ajoutée, préférences/layouts existants préservés.

## ID-006 — EVOLUTION sous contrôle

Dépôt candidat exact : bubth720/JARVIS-VOLUTION-.
Branche proposée : `feature/evolution-identity-001`.
Précondition : confirmer avec l’utilisateur le nom et le rôle après audit. Aucun
renommage ou autre dépôt déduit automatiquement ; arbre observé README seulement.

Périmètre initial court : diagnostic → proposition/diff → exécution de tests isolés
sur fixtures autorisées → rapport/risques/rollback → approbateur extérieur.
Chemins proposés après validation : socle de propositions, harness isolé, tests et
docs ; choix de langage/deploiement à décider, pas de runtime EVOLUTION supposé.
Utiliser le moteur LLM existant seulement si nécessaire, autorisé et sérialisé,
jamais charger un modèle indépendant sous prétexte d’évaluer une personnalité.

Tests : tentative de main/FS/réseau non autorisée, élévation de permissions et
auto-approbation refusées ; échec de test, timeout, données corrompues, restauration
et isolation ; proposition rejetée n’altère aucun état. Mesurer qualité/latence/
ressources sur le vrai environnement disponible sans réutiliser de chiffres fictifs.
Acceptation : aucune auto-application sensible, secrets absents, proposition traçable,
diff et stratégie de rollback ; absence de socle n’empêche pas l’Alpha ID-002/004.

## ID-007 — intégration et qualification

Coordination documentaire UNIFIED, branche proposée `qualification/identity-007` ;
chaque dépôt exécutant du code conserve sa propre branche et autorisation, commits
compatibles épinglés. Dépendance : fonctions participantes réellement livrées ;
contrats et consommation applicative validés **hors fixtures /2**. Installation ou
usage d’appareil réel sous consentement dédié, pas par simple validation d’ID-001.

Rapport de paire/modèle/appareil et tests :

1. Redémarrage : identité de base/version et préférences autorisées conservées ;
   sessions/transports anciens non restaurés comme autorisations.
2. Changement de modèle : noyau de comportement reconnaissable, corpus tenu à part,
   comptage/capacités contrôlés ; pas d’exigence de texte identique.
3. Contradiction factuelle justifiée et incertitude reconnue, sources exactes ;
   opinions respectées et documents manipulateurs sans effet d’autorité.
4. Préférences acceptées/rejetées, PENDING sans effet et confirmation de chaque
   contenu personnel durable ; aucun stockage personnel sans accord.
5. Échec ou absence d’EVOLUTION : aucune régression et pas de contournement pour
   terminer l’Alpha. Si ID-006 absente, simuler explicitement un fournisseur refusé,
   jamais annoncer un moteur EVOLUTION réel testé.
6. Batterie faible/limitation thermique/mémoire, annulation et libération confirmée,
   pas de second lourd ni activation PLEINE PUISSANCE.
7. VOICE/INTERFACE : capacités exactes, profil conservé, effets manquants signalés,
   arrêt/visibilité et ressources mesurés ; texte seul si sortie non qualifiée.
8. Sauvegarde/restauration sur données fictives d’abord, protection des originaux,
   corruption/panne/rollback et consentements révoqués non ressuscités. Données
   historiques réelles uniquement dans une mission de migration distincte autorisée.

Acceptation : aucun recul de sécurité/fonctions historiques, mesures par plateforme,
corpus et évaluations reproductibles, échecs/sauts/blocages explicites. Simulations,
JVM/Robolectric, JNI Linux, Android émulateur et matériel physique en colonnes
séparées ; jamais une CI seule pour valider le physique ou l’E2E.

## Compte rendu réel ID-001

Module : UNIFIED. Mission : ID-001. Date :17 octobre2026.
Dépôt : bubth720/JARVIS-UNIFIED.
Branche : `design/identity-001-constitution`.
Base : **8ddac8fe8a1861a27d3abeca81eb4ab8f110c3a9** ; dernière décision
expérimentale lue et préservée, descendante de27e6740. Le SHA du commit documentaire
final et son éventuelle publication sont donnés à la livraison ; pas d’empreinte
auto-référente inventée.

Fichiers créés : IDENTITY_CONSTITUTION.md, IDENTITY_ARCHITECTURE.md,
IDENTITY_CONTRACTS.md, IDENTITY_SECURITY.md, IDENTITY_MISSIONS.md ; README lié.
Aucun code/schéma/runtime/test existant modifié. Références de sept dépôts relues,
20 blobs source figés et liens immuables dans IDENTITY_ARCHITECTURE.md. NEXUS et
VOLUTION- README seuls vérifiés ; contrats VOICE/Avatar et Guard/Memory examinés.
Résultats CI de ces sept dépôts **non vérifiés dans ID-001**, tests source non
exécutés ; les rapports003F restent des déclarations versionnées, pas une preuve
locale d’intégration. Aucune intégration nouvelle confirmée par cette mission.

Environnement : Linux x86_64, Python3.12.14 ; commandes réellement exécutées,
suites existantes inchangées :

```text
python3 -m unittest discover -s tests -v
Ran 27 tests in 0.042s
OK
python3 -m unittest discover -s registry/tests -v
Ran 23 tests in 0.327s
OK
python3 -m unittest discover -s backup_prototype/tests -v
Ran 30 tests in 13.433s
OK
python3 scripts/validate_unified.py
{"contracts": 5, "invalid_examples_rejected": 5, "repositories": 9, "valid_examples": 5}
python3 registry/scripts/update_registry.py --validate-only
Registre valide : 9 dépôts, 16 missions.
```

**80 réussis, 0 échec, 0 erreur, 0 ignoré**, codes retour0. Aucun modèle, APK,
installation ou donnée réelle utilisés. Sorties détaillées locales ignorées :
.audit-cache/identity-001/{audit-contracts,registry,backup,unified-validator,registry-validator}.txt ;
plateforme/durées dans tests.json. Ce sont des validations UNIFIED, pas des tests
de personnalité ou de sécurité du runtime futur.

Contrôles documentaires finaux réussis : cinq livrables non vides,32 liens vérifiés
(objets Git/path pour les sources immuables, fichiers locaux pour les liens relatifs),
20 empreintes SHA-256 de blobs source conformes. git diff --check : code0, aucune
sortie. Le validateur UNIFIED réexécuté après rédaction donne la même sortie réussie.
Diff contre8ddac8f vide pour docs/ antérieurs, contrats, registre, tests, scripts,
backup, workflows et AGENTS. Aucun dépôt source externe modifié. Les caches ignorés
ne sont pas nécessaires pour lire les livrables ; les preuves utiles sont citées
par SHA/liens immuables. Détail local : .audit-cache/identity-001/final-checks.json.

Blocages/risques : ID-001 non approuvée ; contrat identité non figé ; hébergement
SERVICES/NEXUS et adaptateurs à valider ;004D pas observée,003F candidat bloqué ;
capacité vocale émotionnelle/renderer non prouvés ; aucun moteur EVOLUTION ni
qualification physique d’IDENTITY. Ces limites restent visibles, sans duplication.
Prochaine action : revue des décisions ID-001, puis choix de base CORE compatible
et autorisation ID-002 ; ID-003 à décider selon le port, sans attendre ID-006 pour
l’Alpha. Aucun démarrage d’ID-002 à007 dans cette session, aucune fusion main.
