# UNI-08 / U00 — Inventaire candidat fail-closed

Dépôt : `bubth720/JARVIS-UNIFIED`
Branche : `feat/uni-08-u00-audit-lock`
Parent : `6de738633586743b3cf3f54e41ab4180c2cf0fee` (`feat/fusion-02-android-first-evidence`).
Date du relevé : 26 octobre 2026.

## Portée effective

Ce lot ajoute un **instantané indépendant** de huit producteurs sous `BOM-PROPOSED.json`, un validateur Python autonome et 23 tests négatifs/positifs. Il ne modifie **ni** `integration-lock.json` **ni** `integration-lock-v2.json`, les contrats v1/v2 en proposition, les workflows historiques ou les applications Android. Aucune sélection n'est approuvée comme composition d'exécution.

Le validateur contrôle la forme fermée, les huit identités GitHub exactes, la SHA complète, les URL d'Actions propres au dépôt, l'unicité, l'écart minSdk et les assertions dangereuses. Il **ne se connecte pas à GitHub**, ne revalide pas le contenu d'une CI, ne télécharge aucun objet et ne prouve ni signature, ni provenance matérielle, ni compatibilité binaire. Un succès d'un commit parent reçoit `STALE_ONLY`, plusieurs workflows de résultats opposés donnent `MIXED`, un échec au SHA courant donne `FAILED`. Un état logiciel vert ne débloque jamais Android.

## Différences avec le gel FUSION-02

- Le dernier HEAD SERVICES relevé est `9dfbf60a...` avec CI exacte en échec, même si `10cdce58...` a obtenu une CI verte antérieure ; le rapport FUSION-02 précédent n'est pas réécrit.
- Le HEAD LLM `f1472368...` n'a dans ce relevé qu'une CI verte de son commit de code parent `34491eee...`; le validateur refuse de l'attribuer au nouveau HEAD.
- VOICE `95f87322...` a une CI FUSION dédiée réussie **et** un ancien job Pocket Probe échoué au même SHA : `MIXED`.
- NEXUS et EVOLUTION n'ont pas de CI correspondant à la branche auditée dans le relevé Actions sélectionné : `UNKNOWN`, non `FAILURE`.
- Le dépôt `bubth720/JARVIS-INTERFACE-` reste distinct de `bubth720/JARVIS-INTERFACE`; son rôle n'est pas prouvé par cet inventaire. **Aucune suppression.**

## Chaîne de dépendances (ordre de déblocage)

```text
UNIFIED (contrats / preuves uniquement)
   └── CORE (autorité d'orchestration, C0 uniquement)
       ├── NEXUS  → FTS5 Android / source et citations
       └── SERVICES → fence autorisation au commit / SAF readback
INTERFACE API26 et VOICE API26 : voies optionnelles après transport validé
LLM API29+ : moteur natif optionnel, pas nécessaire au pilote documentaire API24
EVOLUTION : diagnostic hors exécution autonome de patchs
```

**Matrice minSdk candidate :** CORE24 / NEXUS24 / SERVICES24 ; INTERFACE26 / VOICE26 ; LLM29 ; UNIFIED et EVOLUTION non-applications (`0`). La possibilité de compiler avec ces niveaux **n'atteste pas la compatibilité runtime** ni la présence des preuves E2E API24/25.

## Comment vérifier

```sh
python3 -m unittest discover -s tooling/integration/uni08_tests -v
python3 -m tooling.integration.uni08_candidate docs/uni-08/BOM-PROPOSED.json
# Régressions historiques, dépendance backup cryptography requise :
python3 -m tooling.integration.ci --output /tmp/uni08-baseline
```

Le lot a été développé avec Python 3.13 et les **23 tests UNI-08 ont réussi localement**. L'ancienne suite de 167 tests n'était pas disponible dans ce conteneur au moment de l'édition ; le nouveau workflow l'exécute sur le vrai checkout GitHub, et son résultat distant doit être observé au SHA exact avant de déclarer la régression réussie.

## Portes restantes

1. U00 : validation distante au HEAD et revue des autres propriétaires, de leur ascendance exacte et de leurs licences.
2. U01 : ADR-002 sur autorisation au commit CORE/SERVICES, génération strictement positive, UNKNOWN, UID/certificat et révocation ; **décision humaine nécessaire**.
3. U02 : qualification Android réelle API24/25, négociation minSdk/ABI, budgets globaux ; pas de promotion par la seule UI.
4. U03 : pilote CORE+NEXUS+SERVICES sur applications synthétiques **une fois les deux producteurs qualifiés**.
5. U04/U05 : release gate avec vrais tests de redémarrage, intégrité des données, rollback et autorisation humaine.

**Retour arrière :** fermer la PR ou supprimer uniquement la branche U00 après revue. Les branches FUSION-02, `main`, contrats et bases de données restent inchangés. Aucun schéma ni asset à migrer.
