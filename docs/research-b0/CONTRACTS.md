# Contrats B0 proposés — namespace expérimental uniquement

Ces types ne changent ni UNIFIED v1, ni RagContextPort, DocumentaryGateway/1,
ServicesToolPort/1, les générations, les reçus ou l'identité Athéna.

| Type local B0 | Contenu et frontière |
|---|---|
| `Plan` | source_id fictif, URL de fixture, SHA-256 attendu issu du plan, type attendu et profondeur ; immuable, digest stable |
| `Limits` | budgets explicites bornés ; même configuration exigée à la reprise |
| `LabPermit` | identité d'objet enregistrée par le contrôleur RAM, digest exact, génération et expiration ; aucun droit CORE ou carrier wire |
| `LabPolicy` | endpoint de fixture possédée et contexte TLS vérifié ; pas de liste blanche Internet configurable |
| `Ledger` | magasin B0 isolé, compteurs, événements et provenance ; ni mémoire personnelle ni base NEXUS |
| `jarvis.research-b0-document/1` | manifeste documentaire de test, schéma proposé dans document.schema.json |
| `jarvis.research-b0-test-results/1` | résultats réellement mesurés, plateforme, tests, isolation, CPU/RAM et non-activation production |

Le manifeste porte document_id (digest du plan), source_id, origin_url et
final_url fictives, retrieved_at simulé avec date_kind=SIMULATED, content_type,
size_bytes, sha256, validation=VERIFIED_SYNTHETIC et transformations. La seule
transformation B0 est identity-stream-copy, avec entrée/sortie SHA identiques et
outil versionné. Le hash attendu ne vient jamais d'un en-tête du serveur.

Les futurs adaptateurs proposés sont séparés : CORE-admission → RESEARCH-plan,
RESEARCH-manifeste → réception locale NEXUS, SERVICES-transformation → nouvelle
révision dérivée. Aucun n'est implémenté ou branché en production ici. Les notices
B0 n'ont pas encore les garanties licence/rétention/effacement d'un DATA VAULT
de production ; aucune donnée réelle n'y est admissible.

Les erreurs sont des codes fermés de laboratoire sans corps, cookie, clé TLS,
prompt ou jeton dans les logs. Les états READY/RUNNING/PAUSED/CANCELLED/FAILED/
INTERRUPTED/COMPLETED ne sont pas traduits en reçus wire existants.
