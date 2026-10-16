# DESIGN-004 — responsabilités, recouvrements et ADR

**Conception proposée, non implémentée.** ADR-001 reste approuvée avec précisions,
orientation seulement. Source : [ADR actuelle](../DECISIONS/ADR-001-CORE-LLM-UNIFIED.md).
[Preuves fraîchement lues](SOURCES.md) ; les captures001F restent historiques.
Aucun changement de rôle approuvé n’est appliqué par cette mission.

## Conflits et réserves à signaler avant les architectures proposées

| Point observé ou hypothèse | Risque de conflit avec ADR-001 | Traitement proposé, décision encore ouverte |
|---|---|---|
| SERVICES possède maintenant DOCUMENTS, KNOWLEDGE et MEMORY | Recouvrement de NEXUS futur et SQLite historique CORE ; trois mémoires concurrentes | Garder le code, sans déplacer de données. SERVICES reste fournisseur réutilisable ; NEXUS cible domaine documents/recherche/mémoire, CORE confirme. Cartographier les adaptations avant toute migration |
| SERVICES expose Runtime, Guard et CoreAdapter | Confondre orchestration interne d’outil et autorité centrale CORE | Guard peut refuser localement mais ne peut créer un consentement à la place de CORE. CoreAdapter est explicitement in-process/test, pas le CORE réel. Aucun nouvel orchestrateur de synchronisation autonome |
| Catalogue éditorial dans LLM, alors que LLM cible l’inférence | Extraire prématurément ou recréer une seconde base dans CORE/NEXUS | Réutiliser le catalogue existant comme composant hébergé dans LLM ; propriété technique conservée, sélection/autorisations de parcours sous CORE. Aucun transfert de responsabilité physique décidé |
| Téléphone autonome et PC plus puissant | PC transformé implicitement en CORE global obligatoire | CORE autorité locale sur chaque appareil actif ; téléphone fonctionne sans PC. Les sessions d’exécution ne sont pas répliquées. PC ne déclenche pas d’action sur téléphone par un changement synchronisé |
| BRIDGE multi-appareils | Un second service de connexion ou nouvel APK SYNC | Étendre à terme le port BRIDGE existant dans SERVICES, sous autorisation CORE ; pas de dépôt ou moteur SYNC supplémentaire |
| Futur transport local chiffré, authentification et arbitre | Sujets expressément ouverts par ADR | Options de sécurité documentées, aucun transport, clé partagée, permission ou localisation de broker adopté |
| Cache audio conversationnel vs caches VOICE existants | Nouvelle pile vocale, duplication de profils/PCM ou consentement périmé | Extension future bornée dans VOICE, jamais moteur parallèle ni cache CORE. Réutiliser format/intégrité/profil/lecture existants après qualification |
| Préférences de performances synchronisées | Transférer des réglages PC dangereux sur mobile | Préférences utilisateur distinctes des budgets matériels locaux ; limites/permissions/PLEINE PUISSANCE jamais propagées comme autorisations |

Aucun amendement à ADR-001 n’est nécessaire pour **décrire** ces propositions dans
ces limites. Tout déplacement de données/compétences effectives, accès réseau,
transport/signature/arbitre, déploiement ou nouvelle résidence de modèle exige une
proposition précise et une autorisation distincte. Le code SERVICES développé
n’établit ni transfert approuvé à SERVICES ni connexion inter-applications.

## Propriétaires et frontières

| Module | État réellement lu | Responsabilité DESIGN-004 proposée | Duplication interdite |
|---|---|---|---|
| CORE | JarvisCore/AppGraph, SQLite, SharedPreferences, LlamaLocalEngine historiques | Politique, session locale, confirmations exactes, choix du mode autonome/distant, validation avant application ; exécution d’actions indépendante de la réplication | Pas de deuxième routeur d’autorité dans BRIDGE ; pas de nouveau moteur LLM ni catalogue |
| LLM | AnswerRecord, CatalogueStore/Json, IntentRouter, FTS4, backend local | Héberger et étendre le catalogue existant ; renvoyer réponse/clarification/candidat ; inférer uniquement si CORE et protections l’autorisent | Aucun second catalogue SQLite ; pas d’outil déclenché par une variante |
| VOICE | Studio005J, profils/archives, PrivatePcmStore et caches A/B ;005K cahier seulement | Seul propriétaire de synthèse, compatibilité profil/pack, consentements et éventuel cache d’expressions | Aucun profil copié dans CORE/BRIDGE/LLM, aucun TTS générique silencieux |
| NEXUS | README seul dans refs accessibles | Cible future : documents/recherche et stockage des souvenirs confirmés ; intégrer/réutiliser les bibliothèques existantes après décision | Ne pas recréer l’index SERVICES/CORE sans analyse de réemploi ; ne pas déplacer SQLite ici |
| SERVICES / BRIDGE | Foundation Java/SQLite Android et desktop ; Bridge.Transport + Simulator echo ; Guard ; adaptateurs internes | Transport local/remontée de capacités/reprise future et services documentaires optionnels ; primitives de synchronisation sous politique CORE | Simulator n’est pas réseau réel, Runtime n’est pas CORE ; pas de deuxième système de mémoire personnelle |
| INTERFACE | Dashboard, LayoutCodec/DataStore local versionné | Appairage visible, sélection des données, conflits/reprises/consentements, rendu téléphone/montre selon capacités | Ne pas copier DataStore brut entre tailles d’écran ; pas de décision métier dans l’UI |
| UNIFIED | Registres, contrats proposés, preuves, backups fictifs | Conception/versionnement/compatibilités et critères de tests | Aucun runtime, aucun daemon de synchronisation, aucune donnée personnelle |

La montre est un **rôle client léger** à qualifier, pas un huitième module ni une
plateforme Wear OS présumée. Aucun code de montre ou pilote réel n’est attesté.
EVOLUTION reste hors du chemin de données ; les correctifs logiciels ne sont pas
des objets de synchronisation.

## Gates de décision

D1 : transport et appairage/revocation par plateforme, y compris présence réseau
et stockage des clés ; D2 : politique de réplication et durée de rétention par type ;
D3 : coexistence SERVICES/NEXUS/CORE et accès au catalogue sans duplication ;
D4 : plateforme montre et permissions ; D5 : cache vocal, conservation et mesures.
Ces gates ne rouvrent pas le choix option3 de l’ADR. Aucun développement n’est
lancé ici. Missions bornées dans [MISSIONS_SUIVANTES](MISSIONS_SUIVANTES.md).
