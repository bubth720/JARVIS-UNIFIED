# UNI-08/U03 — Bilan deuxième lot et décision de consolidation

**État : REVIEW_ONLY / NO_MERGE.** Document de coordination, pas une fusion logicielle.
Audit des dépôts GitHub effectué le 27 octobre 2026. Source de départ :
UNIFIED lot1 PR #10, `b8f22bb7091c29b654f5e958e97da4f94434b164`.

## Six PR CORE / INTERFACE / EVOLUTION

| Propriétaire | PR de pré-fusion | Commit HEAD | GitHub Actions réussi |
|---|---|---|---|
| CORE | [#20](https://github.com/bubth720/JAVIS-Local-v2/pull/20) | `95a2722dd7c4e67682eb7dc787431274968aa1fa` | [40563102521](https://github.com/bubth720/JAVIS-Local-v2/actions/runs/40563102521) |
| CORE | [#21](https://github.com/bubth720/JAVIS-Local-v2/pull/21) | `a3113797a3c481bc516c5ef1fd4d7a74b919de40` | [40565029341](https://github.com/bubth720/JAVIS-Local-v2/actions/runs/40565029341) |
| INTERFACE | [#9](https://github.com/bubth720/JARVIS-INTERFACE/pull/9) | `a7dd2c37baa2568860557c3cf3f07c31374de1d2` | [40563235219](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40563235219) |
| INTERFACE | [#10](https://github.com/bubth720/JARVIS-INTERFACE/pull/10) | `4bc1993d4b6525b248f2b12e95a18a279a3d9fdc` | [40565042203](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40565042203) |
| EVOLUTION | [#4](https://github.com/bubth720/JARVIS-VOLUTION-/pull/4) | `8d1155fd23078d0a25dbe32edd498a95d60906ac` | [40563113538](https://github.com/bubth720/JARVIS-VOLUTION-/actions/runs/40563113538) |
| EVOLUTION | [#5](https://github.com/bubth720/JARVIS-VOLUTION-/pull/5) | `2e10d6f5c4d41458d0e55cd6724cd93973db450e` | [40565363719](https://github.com/bubth720/JARVIS-VOLUTION-/actions/runs/40565363719) |

**Contrôle GitHub :** les six PR sont ouvertes, brouillon, non fusionnées
et ont toutes comme base `mission/prefusion-gates-20261026`. Chaque campagne
citée conclut à SUCCESS sur son HEAD de PR. Les fichiers modifiés affichés
par l'API des patches n'ont **pas de chemin commun à l'intérieur d'un même
propriétaire**, comme le reflète `LOT2-EVIDENCE.json`. Ceci ne démontre
**ni compatibilité sémantique ni réussite d'un build combiné**.

## Résultats concrets

- CORE #20 : `DocumentToolGateSnapshot`, tests de statut passif.
- CORE #21 : `PinnedDocumentReadiness`, références fixes NEXUS/SERVICES,
  toujours sans droit d'exécution. Le doublon potentiel avec #20 est
  conceptuel (deux projections passives) et doit être évalué, même si
  les chemins des sources sont distincts.
- INTERFACE #9 : aperçu de citation strictement inerte, sans accès URI.
- INTERFACE #10 : état READY non crédible refusé et réutilisation trompeuse
  d'identifiant d'événement traitée comme UNKNOWN ; risque de comportement
  à tester ensemble avec #9.
- EVOLUTION #4 : revue de patch sans exécution même lorsque APPROVED_FOR_LAB.
- EVOLUTION #5 : drainage sérialisé et quarantaine après ACK incertain.
  Aucun remplacement de la sandbox OS bloquée.

## Décision de coordination recommandée

1. **Ne pas fusionner ces PR indépendamment dans la base de mission**, car
   leurs combinaisons n'ont pas encore été qualifiées. Ne jamais fusionner
   vers main sans validation explicite.
2. CORE : garder un port unique de statut passif ; comparer les deux
   projections. Éviter de publier deux mécanismes d'autorité équivalents.
   Tester les six cas nouvellement couverts sur une branche combinée
   **uniquement après revue** et sans activation.
3. INTERFACE : ajouter des tests communs citation inerte + événement UNKNOWN
   pour confirmer que la nouvelle projection ne révèle aucun document.
4. EVOLUTION : exiger l'interaction des gates patch review et télémétrie
   quarantinée sans qu'une approbation laboratoire provoque un correctif.
5. Préparer une **phase R1 de compatibilité combinée** par dépôt sur
   branches isolées, sur copies, sans activation de runtime.
   Un succès CI de chaque PR seule n'est pas un succès de R1.

## Blocages non levés

- FTS5/SAF NEXUS : pas de RAG Android qualifié sur API24/25.
- ADR-002 / CORE/SERVICES : autorité commit réelle et reçus non approuvés.
- JNI/LLM et VOICE : déchargement natif et admission interprocessus inconnus.
- Émotions VOICE : rendu réel et évaluations acoustiques non attestés.
- EVOLUTION : sandbox OS non qualifiée ; aucune auto-réparation.
- Interface/CORE : authentification/signature non activée.
- Appareil physique POCO/Redmi : essais intégrés NOT_RUN.
- Aucune application APK unifiée prouvée.

## Commandes et preuves

```sh
python3 tooling/prefusion/check_lot2.py docs/prefusion/LOT2-EVIDENCE.json
python3 -m unittest discover -s tooling/prefusion/tests -v
python3 workspace/check_plan.py workspace/modular-workspace.proposed.json
python3 -m unittest discover -s workspace/tests -v
```

Le validateur de ce lot lit un **instantané hors ligne**, n'interroge pas
GitHub et ne peut pas affirmer que les six CI restent actuelles à une
date ultérieure. Revalider HEAD et Actions au moment d'une réception réelle.

**Retour arrière :** abandonner la branche U03. Aucun code producteur,
artefact privé, permission, SDK ou version de base n'a été modifié.
