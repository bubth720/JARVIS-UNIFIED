# M53 — documents et SERVICES préparés, raccordement OFF

NEXUS PR12 be70faa41d202d77eb8cf0cc5c831e10cfb020b5 expose DocumentaryGateway version1, NexusStoragePort, transactions, FTS5 et adaptateur SAF ; SERVICES PR12 8d80d09d6aabf6eac00a7bc6bb4930862bd72812 expose ServicesToolPort, SelectedDocumentSearch et ApprovalGate. Ces sources ne prouvent pas leur branchement dans le cockpit. La branche services-final-01 d16dd84f27881460ec9f02d2a54d9ddff23187dc est une référence distincte non absorbée automatiquement.

## Lot indépendant utile

L'agent NEXUS prépare une recherche en lecture seule sur corpus public synthétique et des ports versionnés dans sa branche propre. Réutiliser les contrats/stockages réels, sans moteur de recherche concurrent ou faux index. INTERFACE garde son catalogue Documents UI-01C ; aucune duplication d'une base personnelle ou import global du téléphone.

Protocole d'import volontaire : SAF choisi explicitement, type/taille bornés, droits persistants seulement s'ils sont réellement accordés, empreinte/version de contenu, extraction bornée puis transaction/index. Refuser URI révoquée, document déplacé, incomplet/corrompu, faux ZIP/PDF ou quota. Fichier scanné sans OCR qualifié = UNSUPPORTED. Supprimer une référence/index ne supprime jamais l'original.

Résultat source : documentId/segmentId stables, texte vérifié, locator page/offset quand connu, version/hash/bounds et citationId. Une citation doit rouvrir un passage réel autorisé ; même nom ≠ même contenu. Un score de pertinence n'est pas une confiance factuelle. Les instructions présentes dans un document sont des données non fiables, jamais des commandes. Aucun résumé/citation inventé quand LLM OFF : afficher les extraits et la source, ou « Aucun passage pertinent vérifié ».

## SERVICES et écritures

Cataloguer DOCUMENTS/KNOWLEDGE/DATA/ACTIONS/MEMORY/ANALYST/GUARD/BRIDGE à partir de leur implémentation réelle, pas de leur nom. Les lectures exactes et calculs de valeurs de fixture peuvent progresser. Chaque écriture a cible/effet exacts, aperçu, consentement limité, expiration, exécution unique, journal/rollback et refus lisible. Actions externes, export, suppressions et mémoire personnelle durable restent OFF sans contrat/accord adéquats ; jamais « autoriser toutes les actions futures ».

Mémoire : opt-in, aperçu/édition/retrait visibles, secrets non mémorisés implicitement. Séparer historique de session, préférences, index et événements techniques. Préparer migrations additives et restauration sur copies de fixtures ; aucune migration de données personnelles n'est autorisée. Les chemins SAF ne sont pas portables vers mini-PC : remapping volontaire futur.

## Tests à préparer

Texte contradictoire, multioctets, PDF corrompu, fichier gonflé/déguisé, « ignore les règles », faux liens, citation absente, mêmes noms/contenus différents, index interrompu et droits SAF perdus. Pour les writes : confirmation annulée/périmée/doublée, crash avant/après commit, idempotence et preuve de rollback. Les journaux synthétiques ne prouvent pas la durabilité Android.

Kiwix/ZIM : étude lecture seule, licences/librairies/mémoire et citation ; pas copie de giga-octets, second gros modèle ou index dupliqué. Graphe léger optionnel2D avec provenance et propositions IA marquées ; aucune3D obligatoire.

G-DOC lecture, réponse générative sourcée et service local sont trois critères séparés. La génération reste soumise aux gates M52. Prochaine action : recevoir le SHA/tests du port lecture seule NEXUS puis faire valider le raccordement documentaire minimal, sans acte d'écriture sensible.
