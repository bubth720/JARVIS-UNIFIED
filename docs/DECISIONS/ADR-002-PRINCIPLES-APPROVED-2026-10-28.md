# JARVIS — Décision utilisateur : ADR-002 / principes de conception

**Date de la validation exprimée en conversation : 28 octobre 2026.**
**Portée : VALIDATION DE PRINCIPES, PAS APPROBATION DE PROTOCOLE EXÉCUTABLE.**
**Porteur : JARVIS-UNIFIED.**
**Statut dérivé : DESIGN_PRINCIPLES_ACCEPTED / RUNTIME_NOT_AUTHORIZED.**

## Contexte vérifié

Référence de discussion : `docs/prefusion/lot3/ADR-002-PROPOSED.md`,
UNIFIED lot3 `4fa55d468228a6f222f6177e807938660d735a8c`.
Proposition détaillée du producteur : SERVICES
`docs/prefusion/lot3/ADR-002-PROPOSEE.md`, commit
`cfb5f117edc72acd8d5967980d3dfc9dfbf2903f`.

L'utilisateur a explicitement répondu « Oui » à la question :
valider ces trois orientations comme **principes de conception**,
**sans autoriser** les connexions réelles, écritures, migrations ou fusion main.

## Décisions validées

**D1 — Autorité unique CORE.** CORE détient la décision d'admission,
session, permission, epoch/génération, annulation et révocation. SERVICES
ne s'octroie aucun droit à partir d'une copie de contexte, d'un document,
d'un prompt ou de son propre journal. Le contrat proposé requiert un
`authorizeAtCommit` effectif et linéarisé avec le revoke/consentement
usage unique. Toute absence d'autorité live => refus; l'identité d'un
processus distant **n'est pas** établie par un UUID dans un payload.

**D2 — Étudier le protocole à deux journaux, en laboratoire.** Deux
propriétaires de preuve : CORE pour décision/consentement, SERVICES
pour le worker et la trace de l'effet. Le prototype n'exécute aucun
effet réel. Les fenêtres de panne entre aperçu, dispatch, consommation,
COMMIT_STARTED, effet et readback doivent être documentées/testées.
**Non tranché** : ordre atomique irréalisable entre deux bases, format
wire/version, mécanisme de transport signé et protocole exact de reprise.
Aucune réécriture silencieuse de `DISPATCHED` en `COMMIT_STARTED`,
`COMPLETED` en `COMMITTED`, ni de génération 0 en >=1.

**D3 — UNKNOWN fail-closed et réconciliation en lecture seule.** Une
perte d'ACK, un timeout, une fermeture incertaine ou un crash empêche
toute répétition automatique d'une mutation. Une inspection bornée,
autorisée, sans nouvel effet, peut comparer le document destination
réellement relu, son identité et son SHA-256 complet. Seules fermeture
attestée, corrélation et vérification durable explicite permettent
d'envisager COMMITTED. Les journaux UNKNOWN ne sont ni purgés ni reset.

## Ce consentement NE permet PAS

- Aucun merge `main` (UNIFIED, CORE, SERVICES ou autre).
- Aucun câblage CORE↔SERVICES en production, AIDL/Binder/socket,
  activation de port, export SAF ou permission ajoutée.
- Aucune migration de base ou de journal, copie de données personnelles,
  installation APK, modification du coffre vocal, clé/certificat,
  ou changement du SDK/ABI.
- Aucun passage du manifest de workspace à APPROVED/READY/GO.
- Aucun choix définitif de transport, signatures, protocole journal
  ou backend SQLite Android.
- Aucun passage de `SAF_EXPORT_UNQUALIFIED` à ON.
- Aucun remplacement d'un contrat UNIFIED v1/v2 gelé.
- Aucune présomption d'autorisation de monorepo ou de fusion des dépôts.

## Autorisé dès maintenant

1. Écrire une spécification candidate versionnée et de petits tests purement
   synthétiques négatifs, reproductibles hors ligne.
2. Construire en branches isolées une preuve de concept sans IO externe
   ni mutation, simulant deux journaux et décisions/revocations.
3. Mesurer les incompatibilités de schémas/états existants, sans les corriger
   silencieusement et sans modifier les anciens reçus.
4. Publier rapports, issues/PR brouillon et propositions de validation à
   l'utilisateur pour les étapes encore sensibles.

## Critères de fermeture de cette décision

L'enregistrement de cette décision ne rend aucun gate runtime PASS.
Le lot4 peut être considéré terminé seulement avec CI au SHA exact pour
chaque module, journal de tests négatifs complet, aucune mutation réelle,
absence de changement des garde-fous historiques et revue d'une proposition
de contrat séparée. Après lot4, une **nouvelle autorisation explicite** sera
nécessaire avant le premier raccordement réel.

## Traçabilité

Cette décision est enregistrée sur une branche mission issue de UNIFIED
lot3. Elle n'est pas fusionnée dans `main`. La source de l'autorisation
est la réponse explicite de l'utilisateur dans la conversation, non un
test ou un agent Codex. Les limites fixées dans la question approuvée
restent inchangées.
