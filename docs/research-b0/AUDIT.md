# B0-01 — audit ciblé préalable, 18 novembre 2026

État lu dans les vrais checkouts et relu sur GitHub : NEXUS `5f10193440972ba25b30645d2811537418eface5`, UNIFIED `1834472161ff961b6c7a20a766d0e255d545ab44`, CORE `f6a3b2d0c280c69ef1570544fdbf5bcf5818810c`, SERVICES `7c7fc95ad19e10de877b14fb5d3fe7f53b27d3e4`, INTERFACE `d2e737a99f36fea4f837d54c24be4c6ffe86e3b9`. Checkouts initialement propres. Les runs NEXUS 44273871327 et 44273924562 sont relus completed/success au SHA 5f101934 ; pas déduits du seul rapport A3.

| Composant examiné | Observation / compatibilité B0 |
|---|---|
| CORE `DocumentToolReadiness.kt`, manifeste | Admission documentaire indisponible, opt-in refusé ; INTERNET retirée. Aucun branchement RESEARCH ni permission ajouté |
| NEXUS `rag/RagTypes.kt`, `DocumentaryGateway.kt`, catalogue | Consultation et import par flux local sous autorité hôte ; aucune API HTTP métier trouvée dans ces modules. Les URL XML du parseur sont des identifiants de schéma ; accès externes désactivés |
| SERVICES `ServicesToolPort.java`, `proposal/CommitAuthorization.java` | Ports locaux et propositions distincts ; ni client HTTP ni autorité réseau ajoutés. Réutilisation conceptuelle uniquement, aucun mapping de reçus nouveau |
| UNIFIED `contracts/v1`, validateurs, A2 | Enveloppes fermées : RESEARCH et research.collect incompatibles v1. Namespace Python laboratoire distinct, sans modification du carrier |
| A2 `network_review.py` | Oracle sans sockets, verdict toujours sans autorité transport ; conservé et testé. N'est pas employé comme client ou grant |
| A3 `check_routing_scope.py` | 337 fichiers de base et cinq ajouts exacts ; nouveau fichier NEXUS refusé. Laboratoire placé dans tooling UNIFIED, sans édition du garde ou du workflow NEX-07 |
| INTERFACE V1 / V3 | Base V1 9599d991 à 430 fichiers protégés ; vérification octets/modes et tests du garde, aucune modification UI, avatar, mémoire ou Athéna |

Décision réversible B0 : un outil de test Python 3.12/stdlib dans `tooling/research_b0`, exécuté explicitement hors runtime Android, documents sous `docs/research-b0`, nouveau workflow dédié. NEXUS et les quatre autres producteurs sont uniquement lus/épinglés. Aucun client HTTP de production, contrat historique, migration ou permission Android modifié. La branche A3 et la PR NEXUS #16 restent intactes.

Risques identifiés avant développement : HTTP/TLS réel exige de distinguer loopback volontaire et SSRF ; seuls les sockets de la fixture possédée sont admissibles. L'autorité du laboratoire ne représente pas CORE. Une reprise doit conserver les compteurs, réadmettre l'opération et refuser les originaux divergents. Les vieux gardes conservent leur contexte historique ; ils ne sont ni élargis ni désactivés. La CI UNI-08/U02 déclenchée globalement sur PR peut avoir son propre contexte figé ; tout refus éventuel sera rapporté, pas masqué.

Critères : tests négatifs sur TLS/DNS/destinations avant connexion, transfert borné, nettoyage et reprise sans doublon, provenance vérifiable, absence d'egress dans un namespace réseau CI, préservation des sources et des contrats. Les résultats seront écrits après exécution, pas présumés ici.
