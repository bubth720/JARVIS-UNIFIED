# Décision utilisateur — revue 001F

**PROPOSED / AWAITING USER APPROVAL. Aucun accord enregistré.**
Cette note commente [ADR-001](ADR-001-CORE-LLM-UNIFIED.md) et les cinq contrats
v1 existants ; elle n’autorise aucun raccordement ni changement d’application.

## Comparaison et recommandation

| Option | Bénéfices | Coût / risque / migration | Critère de choix |
|---|---|---|---|
| 1. Monolithe Android | Un processus, appels directs, déploiement et arbitrage plus simples | Harmoniser SDK24/26/29, toolchains et bibliothèques natives ; APK lourd, signature et régressions communes ; risque de perdre les fonctions historiques | Si un seul APK est impératif et si les bibliothèques sont extractibles avec tests et budget mémoire qualifiés |
| 2. APK indépendantes avec IPC local | Livraisons séparées et isolation des données ; réutilise les prototypes | Plusieurs processus/coûts RAM ; services exportés, UID/certificats, versions, panne et transactions à sécuriser ; aucun IPC actuel | Si l’isolation et les cycles indépendants justifient ces coûts après essai comparatif sur appareil |
| 3. Hybride modulaire, CORE orchestrateur et adaptateurs | Découple les contrats du transport ; garde le CORE utilisable et permet backend intégré ou APK local, puis mini-PC | Adaptateurs et arbitrage à développer ; risque de maintenir trop de variantes, tests de compatibilité obligatoires ; transport Android encore à décider | Si transition progressive, préservation et portabilité priment, avec une seule configuration active qualifiée |

**Recommandation : option3**, migration progressive avec une configuration Android
pilote unique. « Hybride » désigne ici modules/adaptateurs ; aucun cloud obligatoire.
Un seul APK reste un objectif produit initial à arbitrer explicitement : une
architecture modulaire peut finir en APK unique, plusieurs APK ne sont pas décidées
par cette note. Ne pas annoncer le choix d’IPC comme déjà fait. L’option3 coûte une
couche de traduction ; un prototype séparément autorisé devra vérifier que son
coût et ses pannes sont acceptables avant d’en faire une architecture déployée.

## Responsabilités proposées et doublons à conserver jusqu’à parité

| Composant | Responsabilité / frontière |
|---|---|
| CORE | Propriétaire unique de session, routage, décisions, permissions, autorisations et confirmation des souvenirs. Conserve aujourd’hui SQLite, PDF/RAG, Whisper, UI et son wrapper LLM |
| LLM | Inférence locale, modèles interchangeables et protections internes ; ni décision métier ni mémoire personnelle. Catalogue SQLite éditorial distinct de la RAM et des souvenirs |
| VOICE | Synthèse/identités et compatibilité exacte moteur–pack–profil ; capture/STT seulement après migration explicite depuis CORE ; aucun remplacement de voix par TTS générique |
| INTERFACE | Affichage, événements, avatar 2.5D à qualifier ; pas de décision métier ni moteur |
| NEXUS | Documents, Wikipedia/Kiwix, recherche et stockage des souvenirs confirmés comme cible ; aucun code actuel. CORE conserve la politique de consentement et l’autorité de session |
| SERVICES | Outils optionnels bornés par autorisations CORE, sans commande implicite issue d’un PDF ou LLM |
| EVOLUTION | Audit et propositions de correctifs en sandbox, revue humaine, jamais application automatique. Nom du dépôt encore à confirmer |
| UNIFIED | Registres, contrats, preuves et gouvernance ; aucune résidence de modèle ni rôle d’arbitre runtime |

La phrase historique « mémoire CORE » désigne aujourd’hui le stockage SQLite et,
dans la cible proposée, l’autorité de confirmation. Le futur stockage NEXUS ne
peut pas conférer de consentement. Aucune conversation ni import n’autorise une
mémorisation : proposition, aperçu exact, confirmation explicite traçable puis
transaction idempotente ; données legacy sans preuve conservées mais inactives
pour la nouvelle mémoire durable. /remember écrit directement dans CORE actuel :
le parcours cible de confirmation commune reste à réaliser, sans effacer l’ancien.

## Revue des contrats réellement présents

| Contrat v1 | Ce qui est défini | Limite / travail avant transport |
|---|---|---|
| capability-manifest | Capacités, versions, plateforme et compatibilités | Une annonce ne prouve ni disponibilité ni droits ; compatibilités moteur/profil encore orientées inférence, NEXUS/SERVICES exigent spécification métier |
| request-envelope | Corrélation, session, référence d’autorisation, payload opaque, limites, délai, annulation | origin et authorization_ref ne sont pas une authentification ; 256 tokens/90s sont des plafonds de proposition, pas un engagement de performance ; négocier avant extension |
| response-envelope | Résultat OU erreur, provenance et état natif | Réponse ne contient pas session/génération de bail ; mapping corrélation→session/génération à garder dans CORE et rejets de réponses tardives à tester |
| resource-lease | Bail lourd/modèle, génération, fin native et libération | Aucun broker interprocessus ni réservation RAM, pas de heartbeat/expiration du bail dans le schéma actuel ; récupération après panne à spécifier avant usage |
| health-status | Disponible/dégradé/inconnu, diagnostics bornés | Pas une preuve d’admission ni de qualification physique ; capteur inconnu/refus fermé |

Les schémas fermés et leurs exemples passent un validateur de sous-ensemble
documenté, pas une implémentation complète de JSON Schema. Le DTO VOICE
CoreVoiceRequestV1 est **différent** de l’enveloppe UNIFIED ; aucun mapping actif.
Aucun schéma n’est modifié pendant cette revue. Les plafonds, erreurs, compatibilités
et durées devront être négociés ; ajout de champ fermé = nouvelle version négociée,
majeure inconnue refusée. Sérialisation UTF-8 stricte, taille/profondeur bornées,
clés uniques, pas de chemins arbitraires ni d’autorité transmise par texte.

## Politique runtime proposée, non implémentée

CORE attribue sessions et corrélations et reste autorité des décisions. Un arbitre
local unique à concevoir admet au plus **un travail lourd et un modèle résident**
pour tous les processus participants, VOICE/Whisper/import compris. Aucun second
chargement tant que fin native et déchargement ne sont pas confirmés ; stop demandé
ne libère rien. Les baux du LLM actuel ne coordonnent que son propre processus.
Morts de processus et redémarrages invalident les anciennes générations, ignorent
réponses tardives et imposent état inconnu/refus jusqu’à réconciliation. Ne pas
relancer automatiquement une génération ou une mémorisation après timeout.

Budgets conservateurs mesurés par appareil : mémoire disponible/réserve système,
PSS par phase et pics, thermique et batterie, foreground/background. Toute mesure
absente ou périmée refuse l’admission lourde selon politique ; aucun abaissement
du seuil SMALL2Gio ni retrait de protection pour réussir un essai. TABLET Qwen3
0.6B Q4_K_M et MOBILE1.7B sont références initiales, pas contraintes définitives.
CENTRAL mini-PC nécessite qualification distincte, Android continue sans lui.

Pour une variante IPC : services **exported=false par défaut**. Un appel entre APK
nécessite un export dédié justifié, permission de signature et vérification UID,
package et certificat (même clé seulement après décision de signature explicite ;
sinon politique d’identités approuvée). Ne pas simplement exporter un service fermé.
Quotas, droits de lecture uniques des artefacts privés, annulation idempotente,
deadline locale reconstruite depuis durée restante, décès Binder et nettoyage
seront testés. Authref seule ou nom de module ne donnent aucun droit. Aucun accès
réseau implicite. Transport PC futur authentifié sur réseau local, contrat négocié,
choix crypto/stockage des clés soumis à revue distincte ; pas un port ouvert ici.

Préserver APK/signatures actuelles, SQLite/index/citations et profils. Snapshot
cohérent, restauration testée, étape de migration réversible, ancien mode conservé
jusqu’à parité ; backup JVBK fictif ≠ export Android ≠ archive vocale JVIENC01.

## Points ouverts et question d’approbation

1. Confirmer option3 et préciser priorité finale : APK unique ou plusieurs APK qualifiées ?
2. Accepter CORE autorité des sessions/confirmations et NEXUS stockage cible seulement ?
3. Définir après benchmark le lieu de l’arbitre, le transport pilote et la stratégie
   de signature ; API24 CORE versus29 LLM exige mode compatible explicite.
4. Confirmer les noms/relations VOLUTION-/EVOLUTION et INTERFACE-/INTERFACE sans suppression.

**Question à l’utilisateur : approuvez-vous l’orientation option3 et ces frontières,
ou quelles modifications demandez-vous ?** Une approbation de cette ADR ne vaut
ni autorisation de développer les adaptateurs, ni publication d’APK, ni fusion.
Une réponse explicite distincte sera consignée avec date et portée. D’ici là,
ADR-001 reste proposée, en attente de validation utilisateur.
