# D4-02 — adaptations et contrats nécessaires, proposés seulement

**Aucun contrat existant modifié, aucun nouveau schéma exécutable créé.**
L’approbation ADR porte sur l’orientation ; les cinq schémas v1 restent proposés.
Même un contrat qualifié/approuvé ultérieurement ne sera pas modifié sans validation.
Sources et versions dans [rapport](RAPPORT_ET_SOURCES.md).

## Frontières d’adaptation

| Port de travail | Propriétaire / existant réutilisé | Lacune réelle et adaptation proposée | Acceptation future |
|---|---|---|---|
| CoreInferencePort | CORE LocalLanguageModel004A, JarvisCore, SessionCoordinator | warmUp/generate/isLoaded ne couvrent pas prepare/cancel/awaitEnd/unload ; AppGraph instancie et préchauffe encore le moteur interne | Mode choisi avant construction/préchauffage ; contrat de cycle de vie fermé, pas un backend de plus |
| LlmGenerationAdapter | LLM LanguageModel, LlamaBackend/JNI/ProcessResources | Aucune API IPC réelle ; pipeline de sécurité du ViewModel non garanti en appelant le backend directement | Réutiliser admission, vérification GGUF, lifecycle et annulation ; endpoint sans recréer moteur ni déclencher UI/catalogue |
| ContentAndContextRef | CORE prépare contexte, propriétaire résout refs | PromptBuilder texte unique et systemPrompt CORE ≠ liste Message user/assistant du LLM | Mapping versionné exact et budget tokenizer, provenance distincte ; refus d’entrée non représentable |
| CataloguePort | LLM CatalogueStore/KnowledgeSource/IntentRouter | Pas de port CORE réel ; JSON1 strict sans contexte/version distribuée | Même catalogue et révisions ; pilote indépendant de première inférence, pas deuxième routeur |
| DocumentKnowledgePort | CORE/NEXUS domaine futur, SERVICES bibliothèques | DOCUMENTS/KNOWLEDGE déjà présents ; CoreAdapter SERVICES ne fait que health/search dans un hôte in-process | API de preuves sourcées, refs privées et writer unique ; pas de migration pour réaliser un test LLM |
| ConfirmedMemoryPort | CORE autorité, NEXUS futur, Memory/Guard SERVICES réutilisables | Save/delete/purge locaux SERVICES ne portent pas une preuve inter-APK ou journal SYNC ; CORE /remember écrit sans parcours commun de preview | Reçu lie contenu exact, parents/révision, acte et grant ; aucune adoption rétroactive de legacy sans preuve |
| ToolExecutionPort | CORE→SERVICES ACTIONS/DATA | Contrats namespace SERVICES et guards locaux, LlmPort Mock/Unavailable | Mapping sémantique explicite ; simulated=true toujours visible ; texte généré n’exécute rien |
| SpeechPort | CORE→VOICE, DTO005I et cahier005K | Aucun pont réel ; texte≤300, identité/pack exacts ; synthèse/généré/lu distincts | Coordonner005K, consentements et arbitrage, sans toucher profils ni fallback actuel |
| BridgeTransportPort | SERVICES Bridge.Transport | Simulator echo/payload limité4096 caractères, pas découverte authentifiée, reprise ou TLS | Futur transport séparé D4-01 ; pas nécessaire à la première inférence Android locale |

Les noms des ports nouveaux sont des propositions, pas des classes existantes.
Un adaptateur est situé dans le dépôt consommateur ou fournisseur approprié,
jamais un runtime UNIFIED. Aucune dépendance directe à un APK comme bibliothèque
ni import du code de l’autre dépôt par copier-coller. Révisions de contrats et
interfaces verrouillées par digest dans les missions coordonnées après accord.

## Mapping CORE → LLM à résoudre avant l’E2E

CORE004A prépare un texte UTF-8 borné avec souvenirs/historique/PDF et provenance ;
JarvisCore l’envoie à LocalLanguageModel avec un systemPrompt configuré. LLM003C
conserve GenerationRequest003B :1–8 messages, rôles user/assistant uniquement,
texte≤16000 caractères/message, dernier user ; contexte512–2048 multiple256,
sortie1–256, threads1–4 et restrictions SMALL/tablette plus fortes.
Son bridge.cpp ajoute un **system prompt fixe**. Injecter le systemPrompt CORE
comme simple message user ou l’ignorer perdrait la sémantique et la parité.

Deux variantes à faire décider :

- P1 : fixture pilote explicitement limitée à la politique système native LLM,
  texte synthétique, aucune prétention de parité des réglages CORE. Refuser toute
  demande exigeant un prompt système non représentable ; ne pas remplacer ce
  réglage dans le CORE installé. Bonne preuve technique limitée, pas migration.
- P2 recommandée pour un raccordement fonctionnel : évolution versionnée du port
  de génération, transmission du contexte système autorisé et borné en conservant
  les politiques indépendantes des permissions/ressources. Adapter JNI/template
  existants et tester parité ; pas recréer un moteur. Nécessite une validation
  du contrat et une mission LLM distinctes, aucune modification appliquée ici.

Décider la stratégie de réduction de contexte : préserver la question et les
instructions autorisées, sélectionner historique et extraits selon budget réel
du tokenizer (caractères/octets ne sont pas des tokens), refuser si question seule
ne tient pas. LLM refait la validation, jamais contexte agrandi automatiquement.
Une citation renvoyée par le LLM n’est pas un fait vérifié ; CORE conserve le lien
aux extraits réellement fournis, indique troncature et sources retenues et refuse
une citation inconnue. Les textes PDF restent des données non fiables, pas des
instructions d’outil ou de mémoire. Le pilote texte évite le RAG au premier test.

## Enveloppes et contrôle du cycle de vie

| UNIFIED v1 inchangé | Usage possible après mapping | Ce qu’il ne prouve pas |
|---|---|---|
| capability-manifest | Plateforme, versions, moteur/modèle et disponibilité | Qualification physique, droit d’appeler ou compatibilité du prompt |
| request-envelope text.generate | Session/corrélation/authorization_ref, contenu opaque, SHA modèle, limites et délai | Identité appelant ; pas de transport défini pour contenu ou cancel |
| response-envelope | Résultat référencé OU erreur, provenance module/commit/moteur, exécution | Succès natif sans observation ; provenance du module ≠ source factuelle de réponse |
| resource-lease | Génération de bail, lourd/modèle, stop_requested→fin effective→released | Réservation RAM ou autorité globale inter-APK |
| health-status | Santé disponible/dégradée/inconnue | Réconciliation automatique d’une opération orpheline ou d’une ancienne session |

Le futur protocole doit préciser les messages prepare/generate/cancel/status/unload,
leur version, erreurs fermées et refs privées, sans ajouter des champs/capacités
en place. Les cinq enveloppes ne définissent pas tous ces endpoints : nouveau
contrat de contrôle à proposer séparément si nécessaire, puis test de négociation.
Ne pas envoyer cancel avec une capability inventée acceptée par v1. Le DTO métier
peut être stocké derrière content_ref, mais son type/version/autorisation doivent
être négociés ; ce n’est pas un contournement de schéma.

Métadonnées proposées : operationID idempotent, sessionID et corrélation, génération
de bail, digest de requête, moteur/modèle/configuration effective, délai restant,
état native_started/native_done/model_unloaded et confirmation de fin. Résultat
personnel uniquement en ref privée à durée courte ; aucune URI/chemin arbitraire,
aucun prompt/audio/token en diagnostics. Entiers et UTF-8 stricts, champs uniques,
limites de taille/profondeur en octets et limites métier vérifiées séparément.

Durée restante construite chez destinataire, jamais comparaison d’horloges
monotones entre appareils/processus sans domaine défini. Timeout client ne prouve
pas arrêt ; cancellation idempotente ne clôt pas le bail. Perte de client/service :
état inconnu, réconciliation status/epoch ; aucune relance automatique d’inférence
sur un deuxième moteur. Une ancienne réponse est rejetée avant historique/TTS.
ProcessResources reste responsable des baux internes LLM ; autorité globale et
emplacement du broker restent un choix utilisateur, pas une propriété de UNIFIED.

## Réemploi SERVICES / NEXUS sans deuxième donnée canonique

Ne pas mapper automatiquement Contracts.VERSION SERVICES vers contract_version
UNIFIED parce que les deux portent «1». Identifier namespaces, champs, erreurs,
annulation et portée des confirmations. LlmPort SERVICES Generation possède des
citations et simulated ; LanguageModel retourne texte : ne pas inventer des
citations ou awaitStopped effectif parce qu’un mock l’a fait. Faute d’adaptation
vérifiée, annoncer indisponible/non intégré et garder les fixtures séparées.

Future façade NEXUS : read/search/write-confirmed avec propriétaire/ID/révision,
preuves et décisions CORE ; les pilotes SERVICES ouvrent leur propre stockage
sous autorisation, pas des tables CORE à distance. Une opération prévisualisée
lie sa base et son contenu ; si base changée, refuser et demander nouvelle
confirmation. Réemploi du code possible sans déplacer les fichiers ou les données.
Transfert réel, purge, tombstones distribuées et format de backup restent des
missions séparées, avec restauration et retour arrière démontrés.
