# Missions Codex suivantes — courtes, proposées et testables

**Aucune mission ci-dessous n’est commencée.** Chaque ligne est une autorisation
séparée dans le dépôt propriétaire, branche dédiée ; aucune fusion/main,
installation, migration ou déploiement implicite. La validation de l’orientation
ADR-001 est acquise : faire décider uniquement les sujets techniques ouverts.
Relire les SHA au lancement, les bases ci-dessous sont une photographie.

| ID / propriétaire / branche suggérée | Objectif borné et livrables prévus | Dépendances / critères testables / portes humaines |
|---|---|---|
| D4-01 UNIFIED / design/transport-trust | Comparer transports locaux PC/téléphone/montre, pairing/révocation, key stores et contraintes réseau ; note de décision et matrice menaces | Plateforme montre identifiée, SERVICES Bridge et manifestes relus. Critère : scénarios T3/T9/T11 couverts et limites offline explicites ; décision humaine transport/auth, pas approbation générale ADR à redemander |
| D4-02 UNIFIED / design/ownership-mapping | Résoudre recouvrements CORE/LLM/SERVICES/NEXUS ; mapping de versions et proposition de schemas sans les activer | D4-01 pour transport, pas requis pour inventaire logique. Critère : propriétaire unique par donnée/capacité, sauvegarde/retour arrière prévus, aucun second catalogue ni confirmation déléguée ; humain tranche rôle de stockage avant migration |
| D4-03 LLM / expressions/pilot-060 | Produire pack pilote20 intentions/60 variantes littérales dans le catalogue existant, provenance et corpus négatif tenu à part ; tests CatalogueStore/IntentRouter | Aucun nouveau schéma nécessaire pour pilote JSON1. Critère : import/export/idempotence/ancien fichier/suppression/contradiction/candidats20, aucun backend chargé pour salutation, aucun effet métier ; revue humaine des textes avant adoption |
| D4-04 LLM / expressions/context-contract | Proposition de sélection contextuelle typée dans le même composant ; migration de métadonnées réversible seulement après accord | D4-03 et CORE port de contexte convenu. Critère : inconnu/périmé→neutre/clarification ; pas de texte « effectué » sans preuve ; limites8 variantes et variantes de même sens conservées ; décision de version et tests avant modification de schéma |
| D4-05 LLM / expressions/curation-800 | Extension par lots60→300→800 formulations, éventuellement600–1000 après utilité/curation | D4-03 validée, D4-04 seulement si variantes conditionnelles ; critère : compte distinct variants,200 intentions cibles sans collision artificielle, tests faux positifs/négation/nombres hors entraînement, revue chaque lot. Pas de performance Android inventée |
| D4-06 SERVICES / bridge/sync-fixtures | Étendre Transport en protocole simulé idempotent et journal/reprise avec faux objets ; tests de crash avant/après commit, ACK perdu et conflit | D4-02/contrats spécifiques approuvés. Critère : T4–T8/T10, aucun réseau réel ni données utilisateur, Simulator clairement signalé ; tests de stockage existants conservés. Aucun port CORE réel raccordé |
| D4-07 CORE / sync/policy-fixtures | Spécifier puis tester grants, confirmations exactes et consentement de partage distinct ; adaptateur de test aux propriétaires | D4-02/06, mission CORE autorisée ; fichiers à fixer après audit AppGraph/SQLite. Critère : absence de preuve/refus, changement de contenu après preview, révocation avant commit, aucune tâche lancée par import ; pas de migration réelle |
| D4-08 SERVICES / bridge/local-transport-fixture | Implémenter le seul transport retenu dans fixture isolée, données synthétiques ; interop PC/téléphone après autorisation dédiée | D4-01 signé, D4-06/07 ; critère : mauvais pair/rejeu/coupure/quota/versions/mode offline, permissions exactes ; revue sécurité et qualification physique séparées. Réseau hors VOICE/LLM ; pas de déploiement automatique |
| D4-09 VOICE / cache/expressions-prototype | Étendre les primitives PCM existantes dans un cache borné de fixtures publiques ; plan de clé et révocation, mesures hit/miss | Coordonner avec mission005K existante, ne pas refaire son audit/bridge. D4-03 fournit textes, profil/pack de test exacts. Critère : E7/E8, consentement par lecture, corruption/éviction sans toucher profils ni A/B, bit-parité rendue, froid/chaud distingués ; choix stockage/chiffrement et écoute humaine séparés |
| D4-10 INTERFACE / sync/conflicts-ui-fixture | Maquettes puis UI de pairing, consentement, état périmé et conflits sur données fictives ; conserver LayoutCodec/DataStore | D4-01/02/07 et contrat de projection. Critère : T2/T4/T8, écran verrouillé, labels brouillon/appliqué/périmé et aucun « succès » fabriqué ; ne pas recopier layouts entre écrans |
| D4-11 SERVICES puis INTERFACE / watch/capability-study | Deux petites missions : inventaire pilote/permissions transport montre ; projection UI bornée sans modèle | Plateforme réelle fournie, D4-01/10 ; critère : téléphone absent/veille/verrouillage, minimum stocké consentie, pas de commande sensible rejouée ; mesures batterie et validation humain sur montre avant pilote |
| D4-12 NEXUS / design/storage-reuse | Cartographier bibliothèques DOCUMENTS/KNOWLEDGE/MEMORY de SERVICES et SQLite CORE ; contrat de propriété et procédure de restauration | D4-02, aucune migration dans cette mission. Critère : plan de réemploi sans second index/source de vérité, sauvegarde/restauration et droits séparés, purge/tombstones/revisions spécifiés ; autorisation migration ultérieure explicite |

Une mission ne modifie jamais plusieurs dépôts sous une seule autorisation. Les
étapes réelles d’intégration future CORE↔LLM/VOICE/SERVICES seront des missions
liées **distinctes**, après qualification du contrat et des appareils. Tests de
fixture réussis ne valident pas E2E, PCM réel ni appareil.

Non-régression transversale : conserver protections RAM/thermique/batterie/annulation,
SQLite et signatures, données et profils privés, fonctionnement autonome sans PC ;
aucune hausse minSdk ou suppression de fonction pour simplifier un raccordement.
Fichiers/chemins de code non connus avant audit laissés à déterminer, jamais
inventés comme API existante. Les budgets proposés dans DESIGN-004 exigent mesure.

Prochaine action recommandée : D4-01 et D4-02 comme propositions documentaires
bornées, puis D4-03 (pilote catalogue) après autorisation LLM. Ces étapes évitent
de développer une synchronisation réseau avant identité/propriété/consentement.
