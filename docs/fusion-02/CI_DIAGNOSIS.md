# U2 — diagnostic public et remédiation propriétaire

Les observations externes ont été relues le 25 octobre2026 ; les références
Git ont été revérifiées à la reprise du26. Les anciens tests ne deviennent pas
fraîchement exécutés. L'accès aux logs authentifiés reste limité ; aucune cause
fine n'est inventée lorsqu'un step échoue sans message accessible.

| Référence | Observation exacte | Portée |
|---|---|---|
| UNIFIED3caa57d / [40214722427](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/40214722427) | FAILURE, annotation « Invalid workflow file … line48 » ; aucun job, durée/artefact absents | Syntaxe YAML, pas échec des147 tests |
| CORE première0d41e6f / [40215415459](https://github.com/bubth720/JAVIS-Local-v2/actions/runs/40215415459) | setup-android échoue ; étape upload échoue ensuite | Tests sautés, aucun succès anticipé |
| CORE36761ce / [40215604539](https://github.com/bubth720/JAVIS-Local-v2/actions/runs/40215604539) | SUCCESS au SHA exact | Preuve CI logicielle, pas pilote Android composé |
| NEX374 / [40115049468](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/40115049468) | Échec setup-android avant les tests Android | Cause détaillée UNKNOWN anonymement |
| SERVICESf000 / [40115305244](https://github.com/bubth720/JARVIS-SERVICES/actions/runs/40115305244) | Étape régressions API24 en échec, exit1 | Message précis des logs UNKNOWN ; pas contournement |
| LLM / [40214822563](https://github.com/bubth720/JARVIS-LLM/actions/runs/40214822563) | SUCCESS code378a1cf | HEADdocse0b781 distinct ; aucun héritage implicite |
| UI1d0a89f / [40214158554](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40214158554) | SUCCESS exact | Assets privés exclus CI publique, tests Android compilés ; essais privés historiques séparés |

La nouvelle NEX9d6928 n'hérite pas de l'échec374 : CI exacte UNKNOWN, workflow
manuel et aucun run observé. Le schéma4 portable/JVM est une vraie progression
rapportée ; cela ne qualifie pas encore FTS5 Android. Les CI VOICE/EVOLUTION et
les alternatives finales sont détaillées dans les audits et JSON `evidence/`.

## Correction UNIFIED confirmée

À la ligne48, `run: python -m pip install --only-binary=:all: -r …` contient un
`: ` dans un scalaire YAML non protégé. GitHub le refuse avant toute exécution.
Reproduction locale avec le parseur PyYAML déjà disponible : `ScannerError`,
« mapping values are not allowed here », ligne48 colonne54. Aucun install du
parseur n'a été ajouté aux nouveaux contrats/outils standard Python.

La commande a été protégée par quotes, avec les mêmes options et dépendance
`cryptography==50.0.0` existante. Aucun job/test n'a été retiré ou rendu optionnel.
Les deux workflows ont été analysés avec succès après correction.

Le nouveau `.github/workflows/fusion-02.yml` est indépendant et encodé en JSON
(valide YAML1.2) pour pouvoir contrôler sa syntaxe avec Python standard. Python
3.12.12 épinglé, contents:read, checkout sans credentials persistés, déclenchement
push sur branche de mission/PR/manual, artefacts même après échec. Il lance les
147 tests initiaux et les régressions nouvelles via un runner à commandes fixes,
avec stdout/stderr, comptes réels et validateurs enregistrés dans summary.json.
Zéro test/saut/échec ne devient pas un PASS, et aucune source tierce n'est exécutée.

Le succès local de cette reprise est documenté dans VALIDATION.json. Le résultat
GitHub de la nouvelle branche doit être observé séparément après publication ;
aucun badge vert n'est anticipé. Les workflows des autres propriétaires n'ont
pas été modifiés. Les échecs initiaux et snapshots FUSION-01 restent préservés.
