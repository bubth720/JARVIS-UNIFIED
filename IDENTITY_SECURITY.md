# ID-001 — sécurité, permissions et restauration proposées

**Modèle de menaces documentaire, aucune protection nouvelle annoncée implémentée.**
Les protections existantes restent obligatoires. Lire
[constitution](IDENTITY_CONSTITUTION.md), [architecture](IDENTITY_ARCHITECTURE.md)
et [contrats proposés](IDENTITY_CONTRACTS.md).

## Actifs, autorités et frontières

Actifs : configuration programmée approuvée ; préférences privées ; contenu personnel
exact et preuve de consentement ; snapshots ; décisions d’évolution ; SQLite,
documents, index, voix/profils/archives et signatures historiques. Les journaux
techniques ne doivent pas devenir une copie des conversations.

Frontières : utilisateur/UI de confiance → CORE politique ; CORE → stockage
propriétaire via port ; CORE → LLM propositions non autoritaires ; CORE → VOICE /
INTERFACE capacités et consentements propres ; EVOLUTION sandbox → revue humaine.
Un modèle, un document, un manifeste importé, un pack éditorial ou un backup ne
peut créer un Guard.Context ni une permission effective. La sécurité est appliquée
hors prompt, avant action/écriture/lecture vocale, même si le modèle l’ignore.

## Menaces et refus attendus

| Menace | Protection proposée / preuve à exiger |
|---|---|
| Document « ignore le système / mémorise ceci » | Classe de confiance source conservée ; pas interpolation en SYSTEM ou appel direct d’outil ; test de non-persistance et refus d’action |
| Modèle inventant APPROVED ou une signature CORE | Type de décision construit seulement par chemin UI/CORE authentifié et confirmation exacte ; JSON/UUID n’accorde aucun droit |
| Persona importée avec commande, clé, nouveau modèle ou accès fichier | Format fermé, attributs typés permis, provenance/digest et aperçu ; rejet de code/chemin/grant et absence de chargement automatique |
| Glissement de personnalité ou flatterie | Manifeste/snapshot versionnés, modifications explicites, corpus critique avec cas d’accord légitime et d’incertitude ; pas simple détection lexicale présentée comme garantie |
| Inférence de préférence personnelle en arrière-plan | Adaptation volatile ; proposition personnelle non persistée sans consentement exact, pas d’embedding/log/cache de substitution |
| Rejeu d’approbation / changement après aperçu | Opération+contenu+portée+base+expiration liés au reçu, usage unique et CAS, aucune approbation transférée vers un nouveau diff |
| Ancien snapshot/consentement révoqué | Révision de consentement contrôlée avant génération/écriture/expression ; invalider session et sorties concernées, stop/drain selon règles natives |
| Rollback de backup ou migration partielle | Révocations actuelles prioritaires, staging/diff/conflits, versions et empreintes, commit atomique ou journal avec rollback testé ; pas d’ancien grant réactivé |
| Corruption d’état/journal ou IO | Refus de l’état privé, diagnostic, versions intactes ; baseline technique fiable approuvée seulement si mode dégradé explicite autorisé ; aucune reconstruction personnelle inventée |
| EVOLUTION qui s’octroie une permission ou valide son propre correctif | Sandbox, refus réseau/FS selon périmètre de test, diff/mesures, approbateur externe, aucun accès main/déploiement sensible |
| Double moteur/évaluation parallèle | Réemploi du LLM existant via admission commune, un lourd/résident pilote ; aucune sandbox qui contourne RAM/thermique/batterie/annulation |
| Fuite par logs/voix/cache/exports | Métadonnées techniques minimales, aucun contenu/hachage public de texte personnel ; consentements de sortie, propriétaire VOICE, exports privés chiffrés |
| Mauvais APK ou faux stockage | Pas de nouveau transport implicitement approuvé ; interface locale de confiance initiale, future identité UID/certificat à qualifier distinctement |

Les tests ne couvrent pas totalement OS compromis, extraction root, matériel
malveillant ou rollback coordonné de tous les stockages. Aucune garantie TEE,
mémoire absolument effacée, chiffrement universel ou fact-checking mondial.
Ces limites ne justifient pas la levée d’une quarantaine ou l’invention d’une preuve.

## Permissions : aucun nouveau droit Android par ID-002

Permissions logiques proposées, contrôlées par CORE/port : lire manifeste approuvé,
lire préférences autorisées, proposer sans effet, décider après aperçu, appliquer
une décision exacte, révoquer et exporter/restaurer une sélection confirmée.
Ces capacités ne sont pas des permissions Android nouvelles ni une extension
automatique des grants GUARD existants. ID-003 devra proposer leur mapping exact,
avec refus par défaut et minimum de droits, avant code.

Le LLM peut proposer/clarifier, jamais approuver ou écrire directement. EVOLUTION
peut produire diagnostic/diff et mesures isolées, jamais autorité de validation.
VOICE peut refuser profil/texte/pack ; INTERFACE ne réécrit pas une décision.
L’utilisateur décide des changements autorisables, mais un choix de ton ne permet
ni d’abaisser une protection matérielle ni d’inventer une source ou libération.

Les données personnelles durables nécessitent aperçu et confirmation du contenu
exact, finalité, portée et expiration ; un consentement général au programme
IDENTITY n’est pas une validation de données encore inconnues. Une conversation,
un « oui » hors contexte, une sortie LLM ou une préférence supposée ne suffit pas.
Proposition personnelle PENDING : volatile tant que son stockage exact n’a pas
été autorisé. Stocker un brouillon/embedding/historique d’évolution privé constitue
également une persistance ; ce n’est pas un contournement autorisé.

Une confirmation durable peut être portée par l’action explicite d’une UI affichant
le changement exact ; conserver reçu technique minimal et contenu privé chez le
propriétaire, pas double question inutile. Nouvelle opération différente, contenu
modifié ou base conflictuelle exigent nouvelle décision.

## Révocation et durée de vie

Vérifier validité avant lecture, composition et émission, puis avant persistance
ou expression. Toute modification urgente de consentement invalide le snapshot
concerné ; aucune réponse ancienne rejouée après révocation. On demande l’arrêt,
attend la fin réelle et le nettoyage requis, sans annoncer une interruption native
à partir d’une coroutine annulée. Les files texte/audio/animation concernées ne
peuvent plus produire d’effet nouveau ; limites du son déjà émis explicitement reconnues.

Préférences non urgentes : nouvelle version à la session suivante, pas mutation
cachée du snapshot. Rétention déterminée par type/finalité ; refus de conservation
illimitée implicite. Révocations/tombstones techniques minimaux doivent empêcher
la résurrection par restauration, selon durée et portée à faire approuver.
Leur stockage privé lui-même fait partie de la politique de consentement et ne
va jamais en Git. Purge explicite/plan approuvé des seuls objets éligibles ; aucune
suppression de données historiques ou preuve d’approbation requise sans décision.
Aucune promesse d’effacement physique absolu du flash ou des backups externes.

## Protection au repos et sauvegarde

État technique public et état privé ont des supports différents. Manifeste de
personnalité sans données utilisateur peut être versionné dans Git après revue.
Préférences privées, souvenirs, profil, audio, clés et données de qualification
personnelles restent hors Git et des artefacts CI, même dans des fixtures de test.
Les tests utilisent uniquement des données synthétiques identifiables.

Proposition ID-003 : sandbox privée, données sensibles chiffrées avec mécanisme
AEAD et clés protégées par plateforme selon matériel disponible ; export portable
chiffré avec secret fourni par canal sûr, KDF/paramètres bornés et versionnés.
Réutiliser les primitives de sauvegarde qualifiées si compatibles, après audit ;
ne pas inventer la compatibilité des paquets Recovery SERVICES, JVBK de démonstration
UNIFIED et JVIENC01 VOICE. Un checksum ne chiffre pas et ne garantit pas l’origine.
Pas de clé embarquée, secret dans Git/log, API cloud obligatoire ou clé PC requise
pour lire l’état local Android. Protection hardware-backed seulement si mesurée
et disponible ; récupération de clé, changement d’appareil et perte du secret
à documenter sans promettre de déchiffrement impossible.

Aucune migration crypto des bases actuelles autorisée par ID-001. Ne pas présenter
le backup prototype fictif UNIFIED comme une sauvegarde Android réelle. Les journaux
GUARD bornés ne remplacent pas un registre de transactions d’identité durable.

## Restauration réversible : protocole proposé, non exécuté

1. Sélection explicite des namespaces/versions et finalité, backup vérifié de l’état
   existant avant toute future mutation autorisée. Les originaux ne sont pas effacés.
2. Import privé en staging borné : type/version/tailles/compte, AEAD avant usage,
   empreintes et schémas, refus traversal/symlink/ZIP bomb et fichiers incomplets.
   Aucune application automatique d’un manifeste, d’une proposition ou d’un script.
3. Comparer propriétaire, révisions, politique/consentements actuels, révocations,
   expiration, schémas et compatibilités ; index dérivés régénérables séparés des
   originaux. Une révision plus haute ne prouve pas l’autorité d’un backup.
4. Présenter le diff exact. Rétablir une préférence personnelle inactive requiert
   confirmation de sa nouvelle utilisation durable ; les APPROVED historiques ne
   restaurent pas de permissions/grants ou la validité d’un secret révoqué.
5. Commit atomique du pointeur/révision ou protocole de transaction conservateur
   avec journal/rollback ; panne simulée à chaque frontière, restauration de
   l’état précédent vérifiée avant déclaration de réussite. Snapshot de session
   non réutilisé, prochaine session reconstruite depuis état autorisé.
6. Conserver original/staging/rapport selon politique et consentement ; purge
   ultérieure explicite, pas nettoyage destructif automatique pour cacher l’échec.

Les journaux/quarantaines de bootstrap CORE–LLM ne sont jamais restaurés comme un
état sain d’identité ou écrasés par ce processus. Contrats /2 et données IDENTITY
restent séparés. Des données historiques sans preuve de consentement ne sont pas
supprimées ; elles ne sont pas automatiquement promues comme consentements nouveaux.

## Critères de sécurité qui bloquent l’activation

Refus d’action et persistance sans preuve exacte ; aucun SYSTEM issu de document ;
aucun second LLM ; validation de quotas/annulation, révisions et versions ; essais
corruption/rejeu/restauration et preuves de rollback ; snapshots périmés refusés ;
profils vocaux inchangés ; journal minimal privé conservé ; capacités non prouvées
signalées. Sans ces preuves, mode réduit explicite ou refus du nouveau parcours,
jamais affaiblissement du mode historique. Un mode dégradé n’autorise pas à charger
un autre moteur si fin/libération du précédent restent inconnues ; les quarantaines
et preuves de résidence conservent leur priorité. Le catalogue et moteur existants ne
sont pas recréés pour satisfaire un test de personnalité.
