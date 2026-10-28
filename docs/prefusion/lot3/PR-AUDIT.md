# Audit lecture seule des huit PR antérieures

Observation : 28 octobre 2026, UTC. Sources : références Git `refs/pull/N/head`, commit/tree Git, JSON public incorporé aux pages PR (baseSha/baseBranch/headBranch), listes Actions publiques. Aucun checkout de module modifié.

Toutes les huit PR sont toujours Draft. Les SHA40 head/base et arbres sont vérifiés. Les diff de noms de fichiers ont été recalculés depuis les deux SHA Git. Les listes Actions affichent SUCCESS, mais les runs déclenchés par PR ne fournissent pas un SHA40 dans la liste ; le statut exact sur la tête est donc UNKNOWN. Ne pas convertir ces listes en tests frais ou en qualification physique.

| Module | PR | Head | Base | Tree | Fichiers diff | Runs SUCCESS observés | CI SHA40 exact |
|---|---|---|---|---|---:|---:|---|
| UNIFIED | [10](https://github.com/bubth720/JARVIS-UNIFIED/pull/10) | `b8f22bb7091c29b654f5e958e97da4f94434b164` | `6b0ae1a1ca1a257446931a69bdff15a4f77ac019` | `78d0a20e70565da64ed98701e1bb26047e169f44` | 4 | 5/5 | UNKNOWN |
| NEXUS | [8](https://github.com/bubth720/JARVIS-NEXUS/pull/8) | `201f0d2b03209de104157595a557143fe87eb94e` | `bdb51f77a5fe105dbff43d43032882fe1474a4ee` | `c6debf4d2fe4c539c460229c3efce2736d575f4d` | 4 | 1/1 | UNKNOWN |
| SERVICES | [7](https://github.com/bubth720/JARVIS-SERVICES/pull/7) | `ea541d20b08f7ad0949354829a977f6752cbffa3` | `365da117ccb29b59ed990711b2c3f72472ce2d9d` | `41fad0a190d0517fa27bff37a871a5916a20845e` | 1 | 1/2 | UNKNOWN |
| LLM | [6](https://github.com/bubth720/JARVIS-LLM/pull/6) | `6ae8a4f5c2490f6c9814e08957909a8e3a807180` | `12fc58a81ceee70eedbba2d0b187b1294bae6283` | `52a75bfb7b2ee102c958fd0a7bc642c560693fc2` | 5 | 2/5 | UNKNOWN |
| VOICE | [25](https://github.com/bubth720/JARVIS-VOICE/pull/25) | `d10671119fa9a52bc130c28b21ca193edd99d604` | `697110fa5a8dc87c4ed2a7e8df81a2e644a9559b` | `366780b28dd5e5690682d7c638a9e8eb3e6df40f` | 4 | 3/4 | UNKNOWN |
| CORE | [21](https://github.com/bubth720/JAVIS-Local-v2/pull/21) | `a3113797a3c481bc516c5ef1fd4d7a74b919de40` | `cd2adea393287ea94eb3145e8463209f6fa37e9d` | `3d920058cccb9f02ca2af8e7d1bc7acbaedef631` | 7 | 2/2 | UNKNOWN |
| INTERFACE | [10](https://github.com/bubth720/JARVIS-INTERFACE/pull/10) | `4bc1993d4b6525b248f2b12e95a18a279a3d9fdc` | `82675ade011e69eb3bccd99efbf46d0697a3276b` | `4b87f64cbb1709992c9ee2b36aee47faa304b6ed` | 3 | 2/2 | UNKNOWN |
| EVOLUTION | [5](https://github.com/bubth720/JARVIS-VOLUTION-/pull/5) | `2e10d6f5c4d41458d0e55cd6724cd93973db450e` | `4af477877c3ceb32e5805948ca42798970512d44` | `cab1d33b881f78e24930a2f03fdd7f377b17f860` | 3 | 1/1 | UNKNOWN |

UNIFIED #10 correspond bien à b8f22bb7091c29b654f5e958e97da4f94434b164. Le nom historique codex/prefusion-20261026-lot1 ne constitue pas une contradiction : cette branche a reçu ce commit. Les cinq workflows SUCCESS visibles sont des observations historiques distantes ; leur liaison complète au SHA doit encore être obtenue pour attester une campagne exacte.

Les fichiers result.json et diffs.json contiennent les liens individuels Actions et les fichiers modifiés. Aucun secret, auteur/e-mail Git ou valeur de jeton n’est conservé dans ces livrables sélectionnés. Aucun push, commit, PR, installation ou test matériel exécuté par cet audit.

Précision : les descriptions de runs Commit fournissent un lien SHA40 pour LLM 40547519540 (SUCCESS), VOICE 40547542779 (SUCCESS) et 40547542815 (CANCELLED), CORE 40565016885 (SUCCESS). Ces succès exacts sont des preuves CI logicielles partielles, sans attestation de toute la campagne. LLM affiche aussi trois workflows PR SKIPPED ; SERVICES affiche un run PR CANCELLED. Le JSON distingue chaque cas.
