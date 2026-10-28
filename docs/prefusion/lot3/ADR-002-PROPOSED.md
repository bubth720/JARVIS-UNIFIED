# ADR-002 — trois décisions à soumettre

Statut : PROPOSÉE, NON APPROUVÉE. Aucun droit d'écriture ni transport activé.
ADR-001 demeure approuvée; l'autorité centrale CORE n'est pas remise en question.

## 1. Identité, génération et clôture de l'autorisation

Recommandation : une autorité CORE sérialisée fournit un droit borné au triplet
session/requête/epoch et à une génération monotone; le consommateur revalide
l'identité attestée et le droit vivant au point d'engagement. Chaque redémarrage
change d'epoch. Le jeton unique est consommé une fois. Refuser replay, génération
absente/ancienne, droit révoqué/expiré, identité fournie par le payload.

Alternative : justificatif signé portable entre processus. Il facilite le
contrôle indépendant, mais nécessite transport, certificats et anti-rejeu durables
qualifiés. Un callback local simplifie le prototype mais n'atteste aucun processus
extérieur. Ne pas convertir silencieusement génération locale0 en wire>=1.

Décision demandée : figer le mécanisme local de clôture, puis faire approuver
séparément toute extension inter-APK. Une décision ancienne ne peut être remise
au présent par réétiquetage.

## 2. Point de commit et ordre durable

Proposition : PREPARED (aperçu lié aux digests et destination) → décision CORE et
consommation unique → écriture durable COMMIT_STARTED → effet → vérification
indépendante du résultat durable → COMMITTED. L'ordre exact entre consommation
et journal devra avoir un protocole récupérable; aucune paire d'écritures n'est
présentée comme atomique sans preuve. Tester chaque fenêtre de panne.

Alternative A : outbox unique propriétaire CORE, ordre plus lisible mais couplage
et migration à qualifier. Alternative B : deux journaux coordonnés, conservation
de l'autonomie mais divergence et récupération plus complexes. Recommandation :
prototyper B sans effet réel avant de choisir l'implémentation durable.

DISPATCHED n'est pas COMMIT_STARTED; COMPLETED n'est pas une preuve COMMITTED.
Avant engagement, révocation/annulation/expiration doivent produire zéro effet.
Après engagement, signaler honnêtement l'incertitude ou l'effet, sans promettre
une annulation rétroactive. Aucune écriture réelle autorisée par ce document.

## 3. ACK perdu, journal ambigu et UNKNOWN

Recommandation : UNKNOWN bloque les nouvelles mutations; lecture diagnostique
bornée et réconciliation explicite avec droit frais. ACK perdu ne relance pas
l'effet. Un readback indépendant doit vérifier identité de destination, digest,
version et durabilité; un booléen provenant de l'exécutant ne suffit pas.

Alternative : traitement manuel systématique (sûr mais coûteux) ou assistant de
réconciliation en lecture seule (plus utilisable mais nouveaux accès à contrôler).
Aucun nettoyage de journal, reset automatique, réutilisation du jeton ni retry
aveugle. Corruption, close échoué et résultat inconnu restent UNKNOWN.

Décision demandée : autoriser ultérieurement le prototype de réconciliation en
lecture seule et ses critères; toute migration/écriture/signature nécessite une
autorisation distincte. Les tests du banc SERVICES ne lèvent pas ce gate.
