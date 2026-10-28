# Lot3 — bilan de clôture technique

Mise à jour : 28 octobre 2026 UTC. Ce document complète les premières captures
sans les réattribuer à de nouveaux SHA. Les branches sont dédiées; aucune fusion,
migration, installation personnelle ou activation de production.

## Livraisons publiées

| Module / mission | Branche | Commit propriétaire | Preuves |
|---|---|---|---|
| CORE / CORE-PF-02 | codex/prefusion-lot3-core | aed84860f2ca85713140a687ba7d86efc0203dc8 | 629 tests hôte JVM/Robolectric réussis, 0échec/erreur/saut;3builds/3Lint; CI40667196196 SUCCESS |
| INTERFACE / UI-PF-02 | codex/prefusion-lot3-interface | 9e60e4571fe21d112b2f5e425391b8bcdcc3299e | 217JVM etbuilds/Lint verts au4914dcc;18testsPython du dernier correctif réussis; campagne de capture au9e60 en cours lors de cette capture |
| SERVICES / SERV-PF-02 | codex/prefusion-lot3-services | cfb5f117edc72acd8d5967980d3dfc9dfbf2903f | 121JVM+40Robolectric réussis; CI40665178466 SUCCESS,7jobs dont matricesAPI24/25/26/35 |
| NEXUS / NEX-PF-02 | codex/prefusion-lot3-nexus | c5dee7ab0344a23bfd80b13cd52d09e8b26241dd | CI40752240534 SUCCESS,56tests instrumentés (14/API24/25/26/35),0échec/erreur/saut |
| UNIFIED / UNI-PF-02 | codex/prefusion-lot3-unified | Voir git log du rapport publié | 251Python réussis,0échec/erreur/saut; CI265734b SUCCESS; garde etvalidateur relancés après reprise |

[SHA distants et arbres](CURRENT-OWNER-COMMITS.json),
[contrôle des références principales](MAIN-REFS.json),
[revue indépendante](REVIEW-NOTES.md).
La ventilation des629cas CORE entre JUnit pur etRobolectric n'est pas établie :
510+53+36+30 sont des suites hôte, aucune qualification émulateur ou physique.
Les SDK, modèles et protections matériels de production sont préservés.

## Capacités réelles

- CORE : port read-only de métadonnées, corrélation et refus/replay testés, OFF par défaut; opt-in synthétique UNTRUSTED, jamais READY ni permission. Non composé dans AppGraph.
- INTERFACE :13nouveaux tests Android de refus/états/rotation, plus outillage CI public. Aucun fichier historique app/manifest/dépendance/asset modifié.
- SERVICES : banc de protocole déterministe avec14nouveaux cas, sans écriture productive ni autorité CORE simulée présentée comme réelle.
- NEXUS : laboratoire FTS/SAF avec provider de test séparé protégé et opt-in. Vérificateur public réellement appelé sous Android. Aucun driver natif ajouté; RAG reste BLOCKED/UNSUPPORTED.
- UNIFIED : audit des8PR antérieures, matrice candidate, ADR-002 proposée et revue exécutable du parcours TXT/CSV synthétique. Aucun raccordement Android E2E ni APK unifiée.

## Validation NEXUS confirmée

[Run40752240534](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/40752240534)
au c5dee7ab, SUCCESS en5m58s. Les pages publiques des4jobs identifient les API24,
25,26,35 et publient chacune les comptes JUnit9anciens+5nouveaux, sans échec,
erreur ni saut : **56 cas instrumentés**. [Preuve sélectionnée](NEXUS-CI-FINAL.json).

Bilan local cumulé231réussites+1sautZIM (archive non fournie) :95JVM,71Robolectric,
24Pythonlot3,6gardes,10SQLhôte,18ZIM,7Node. Les dernières modifications n'ont
rejoué que les vérifications pertinentes : APK/Lint du laboratoire,24Python et
garde; les sources des autres suites sont gelées. LocalAndroid NOT_RUN sansKVM,
physique NOT_RUN. Compilation contre stubs API24 distincte d'un émulateur.

Échecs et corrections conservés dans le rapport propriétaire : callback de
sélection lu trop tôt, cible trop ancienne du seul APKlab, handle DocumentsUI
périmé surAPI35. Correction : attente du vrai callback sous délai monotone,
targetSdk35 du seul labo/minSdk24 intact, réacquisition bornée de la navigation
idempotente. Aucun rejeu de lecture/grant/export, aucune assertion retirée.
Les runs8bc0154 et748b3c5 restent en échec dans l'historique; ils ne sont pas
renommés en succès par la campagne ultérieure.

## Validation INTERFACE et limite de capture

[Run40747853353](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40747853353)
au4914dcc :22tests initiaux passent sur chacune des API26/35; le script valide
ensuite2cas après redémarrage. API26 COMPLETE/0. API35 atteint CAPTURE puis
sort255 : les tests réussis ne transforment pas la campagne entière en succès.

La désinstallation des APK en fin de connectedAndroidTest a d'abord été corrigée
par réinstallation explicite des2APK compilées. Chaque commande cible le serial
émulateur validé; aucun appareil physique n'est accepté. Ce correctif a résolu
le contrôle de reprise sans modifier les assertions Android.

Le correctif9e60e457 utilise maintenant ADB exec-out pour extraire **le même
fichier PNG public de fixture**, sans fallback sur un autre écran ou fichier.
Signature, CRC etdimensions sont vérifiés; stderr classifié en constantes bornées,
aucun contenu privé publié.18tests Python réussis, garde114fichiers historiques,
Bash etdiffcheck PASS. Nouvelle campagne exacte :
[40753173250](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40753173250),
au9e60e457, IN_PROGRESS lors de la capture. Le résultat final n'est pas anticipé.
Trois anciens tests à pack privé non autorisé restent NOT_RUN dans cette sélection.

## Autres preuves et préservation

[SERVICES-CI.json](SERVICES-CI.json) :7jobsSUCCESS vérifiés, dont4matrices.
Le validateur CI inchangé impose15cas/API; les XML protégés n'ont pas été relus
indépendamment, aucun compte XML inventé. Les données de test restent fictives.

Les contrats UNIFIED v1/v2/locks, fonctions historiques et profils privés n'ont
aucun delta.3APK CORE indépendamment contrôlés : empreintes conformes et absence
INTERNET/ACCESS_NETWORK_STATE. Aucun commit de fusion dans les5branches.
Les4références main publiées restent égales à leur valeur initiale. INTERFACE
n'expose ni main ni master; sa HEAD annonce development/mission-002, sans renommage.

[Rapports propriétaires et comparaisons PR](OWNER-RESULTS.md),
[audit antérieur](PR-AUDIT.md), [matrice candidate](CONTRACT-MATRIX.md),
[trois décisions ADR-002 proposées](ADR-002-PROPOSED.md).

## Publication, décisions et prochaine action

Les pushes dédiés fonctionnent, SHA distants vérifiés. Les PR ne sont pas créées :
POSTapi.github.com/graphql Forbidden, accès réseau toujours absent au contrôle
après reprise. Aucune nouvelle tentative équivalente ni contournement.
Corps prêts dans les rapports, comparaisons vers mission/prefusion-lot3-20261027,
jamais main; choisir **Create draft pull request** manuellement.

Le brouillon cloud sauvegardé propose le seul domaineapi.github.com et les
instructions de reprise. Il n'est pas appliqué : examiner/enregistrer dans les
paramètres puis publier l'environnement pour l'activer; droitsAPI encore à vérifier.
Aucun jeton demandé, extrait ou stocké.

Prochaine action : terminer la vérification de capture INTERFACE, puis examiner
ADR-002 (clôture du droit/génération, point de commit/journaux, UNKNOWN/readback).
Confiance réelle CORE/UI, driverFTS, mutationsSAF, JNI/unload, sandboxEVOLUTION et
installation physique restent soumis aux preuves et autorisations distinctes.
Aucun de ces gates n'est levé par une CI verte du laboratoire.
