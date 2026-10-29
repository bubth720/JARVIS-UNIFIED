# ADR-002 — trois décisions ouvertes, non adoptées

Statut : **REVIEW_REQUIRED / PROPOSAL_ONLY**. Complète [la proposition U01](../uni-08/ADR-002-PROPOSAL.md) sans l'amender et sans accorder d'autorisation. Aucune écriture réelle avant validation distincte et qualification.

| Décision à soumettre | Option proposée | Avantages | Coûts et alternative |
| --- | --- | --- | --- |
| 1. Autorité et génération | CORE seul émet session, génération et jeton à usage unique ; frontière wire 1..2^53−1, refus explicite de0/overflow ; fixture locale0 conservée sans conversion silencieuse | Une seule décision de consentement/révocation ; erreurs détectables, pas de double autorité | Adaptateur versionné et tests de compatibilité requis. Alternative : nouveau wire à entier étendu/versionné ; moins de bornage mais changement de schéma et migration à autoriser séparément |
| 2. Instant exact du commit et journaux | CORE valide atomiquement identité/preview/génération/échéance/révocation, consomme le jeton et persiste sa décision avant envoi ; SERVICES persiste un marqueur de début avant l'effet ; distinguer DISPATCHED, COMMIT_STARTED et COMMITTED | Décision traçable, refus du double envoi, aucune réussite avant effet et readback durable | Nécessite journaux durables, sérialisation et reprise après crash à qualifier. Alternative : décision durable déléguée à SERVICES ; moins d'aller-retour mais autorité partagée et conflit de révocation à résoudre |
| 3. ACK perdu, révocation et readback | Absence d'ACK/readback complet ou digest divergent → UNKNOWN bloquant ; consultation du journal par identifiant unique, jamais de retry aveugle ; révocation après décision signalée explicitement sans promettre un rollback | Évite doublons et faux succès ; distingue acceptation, effet et preuve durable | Réconciliation manuelle possible et disponibilité réduite. Alternative : retry idempotent seulement après preuve de déduplication durable du fournisseur ; plus disponible mais preuve actuellement absente |

La simulation SERVICES et la fixture UNIFIED ne prouvent ni signature CORE ni atomicité d'un fournisseur SAF, ni persistance après mort Android. Jetons synthétiques en mémoire uniquement, aucune donnée privée.

Répondre aux décisions1/2/3 autoriserait une orientation de conception seulement, sauf accord explicite supplémentaire d'implémentation ou d'activation. La migration, les changements v1/v2 et l'écriture production restent interdits dans ce lot.
