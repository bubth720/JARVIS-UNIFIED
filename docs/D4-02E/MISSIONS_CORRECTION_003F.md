# Corrections LLM003F après validation — CORE004D reste bloquée

**Missions futures proposées, aucun code CORE/LLM exécuté ou modifié ici.**
La décision1748cb0 autorise le cadrage et impose revue ; D4-02E.1 n’est pas
une acceptation automatique du bundle candidat4b4129b5.

## Lot A — F1/F2 et engagements, dépôt LLM uniquement

Base à revérifier : fixture/003f-bootstrap-attestation,
111be993e970051686bd5c27b3115320513a4be7 ; ne pas fusionner les branches divergentes.
Conserver la branche propre LLM selon autorisation de correction. Relire issue LLM1,
les rapports003F, cette clarification et les limites d’accord avant toute modification.

Fichiers concernés : fixtures/p2-contract/{CONTRACT.txt,TABLES.json,CONTRACT.sha256},
RecoveryTables.kt/RecoveryProtocol.kt, vecteurs et générateur de tables ; côté endpoint
ProcessRecoveryAuthority.kt, RecoveryJournal.kt et contrôles Binder existants.
AIDL inchangés sauf nécessité nouvelle faisant l’objet d’une nouvelle revue.

- DISCOVER fournit les epochs CORE vrais issus de l’autorité CORE et leur fraîcheur,
  liés au token vivant/canal ; retirer toute dépendance de production à une injection
  de test trustedPeerEpochs pour un chemin positif.
- SNAPSHOT ne publie que journal LLM ; preuve CORE explicite et bornée, pas accès
  à sa sandbox. Toute mutation entre aperçu et préparation fait échouer le tour.
- Geler les tables D4-02E.1 ou déclarer tout écart, prouver appartenance des deux
  preuves et égalité aux preuves locales authentifiées, outboxes et fsync exacts.
- Tests de corps inconnus/doublons/tailles, nonce/epoch/date, inversion de rôle,
  omission/remplacement de preuve même avec hashes recalculés, rejoués/ACK perdu,
  coupure après chaque fsync/publication de tête, capacité de journal saturée.

Acceptation : vecteurs Kotlin et Python exacts, préservation /1, aucun grant natif
/2 sur simple COMMIT. Rapport SHA/bundle/table/CI/simulations précis ; pas d’APK
installée ni de qualification physique annoncée. F1/F2 corrigés en code ne suffisent
pas à lever le gate tant que F3 et les preuves manquantes restent bloquantes.

## Lot B — F3 : port minimal d’observation et nettoyage, dépôt LLM uniquement

Interface **proposée**, pas nouveau moteur ni implémentation UNIFIED :

| Opération interne du port | Données obligatoires / règle |
|---|---|
| observe(expectedProcessEpoch, expectedOperationKey) | Snapshot sérialisé sur vrai worker : registry_generation, process/worker/owner IDs opaques, clé complète ou NONE, queue/imports/calls/counts, handle/model/context states, baux et générations exactes, call_end_seq, unload_seq, terminal_record_ref ; chaque inconnu explicite |
| freezeAdmission(round,barrier) / inspectFrozen | Gate unique couvrant toutes les entrées participantes ; pas second acquéreur de baux P2Lifecycle/ProcessResources, pas création de backend pour sonder son vide |
| requestStopExact(key) puis awaitDrainExact(key) | Arrêt demandé séparé de retour des appels load/generate/import ; aucun abandon de coroutine comme preuve de fin ; callback corrélé et pas attente sous verrou de l’autorité |
| unloadExistingExact(key,owner,leaseGeneration) | Retry seulement sur demande explicite, après fin connue, mêmes handles/baux ; aucun prepareOperation/load, aucune libération d’un nouveau propriétaire |
| persistTerminal(observation) / readTerminal(ref) | Reçu réel sans texte, clé/fin/unload/baux/digest/provenance process liés, journal durable avant preuve ; hash seul n’est pas une observation |

Les indicateurs handle/model/context peuvent être KNOWN_EMPTY/KNOWN_OWNED/UNKNOWN ;
ils viennent des vraies transitions backend/JNI, jamais de PSS, backend==null ou
un isLoaded isolé. Ressources import et cleanup/close en file incluses dans le drain.
Une bibliothèque/handle vide n’est pas un modèle résident ; pas de RSS=0 garanti.
Le port ne donne aucune preuve OS de mort du propriétaire. Ancienne opération
perdue sans reçu terminal ou journal corrompu : UNKNOWN conservé, même après relance.

Fichiers à examiner pour adaptation minimale : AndroidRuntime, LlamaBackend et port
natif existant si nécessaire pour observation fiable ; ne pas modifier SafetyPolicy,
seuils, profils, legacy, catalogue ou /1. Tout changement sensible de port natif
nécessite périmètre approuvé. Pas de deuxième backend ni d’auto-nettoyage périodique.

Tests obligatoires : vrais chemins worker avec API native simulée explicitement
étiquetée, échecs create/load/generate/unload/close et capteur ; conservation des baux
jusqu’à succès prouvé, ancien key/lease refusé ; tests JNI Linux réels séparés si
ressources autorisées déjà présentes. Android Binder réel et physique restent non
exécutés sans mission/laboratoire distinct. Conserver157 JUnit rapportés ou expliquer
chaque évolution, ne jamais retirer les assertions historiques pour passer.

## Gate de reprise CORE004D, toutes conditions nécessaires

1. Clarification D4-02E validée et écarts éventuels explicitement acceptés.
2. Nouveau code LLM publié avec SHA exact ; bundle /2 vrai recalculé, tables/ABI /
   codecs et vecteurs testés ; candidat4b4129b5 ne suffit pas.
3. F1/F2 corrigés sans valeurs de test en production ; F3 positif dans son périmètre
   instrumenté, cas irréconciliables refusés, appartenance COMMIT vérifiée.
4. Tests et CI réellement observés, non-régression/protections/préservation démontrées ;
   limites plateformes et absence de preuve physique documentées.
5. Revue technique du bundle exact pour consommation CORE ; autorisation004D
   conditionnelle satisfaite seulement après cette revue, pas par publication UNIFIED.

Si une condition manque : **CORE004D BLOQUÉE**. IDENTITY ID-002 possède son propre
gate de contrat ; aucune persona ajoutée pour tester le protocole synthétique.
