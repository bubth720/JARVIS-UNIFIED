# Registre central JARVIS

Génération : ce1712ef03584b5782b0d341ffeebe69. Sources : git.

**success désigne une observation réussie, pas une mission terminée ni une application validée.**

Une valeur conservée après un échec est historique ; vérifier checked_at, verified_at et les preuves.

| Dépôt | Branche de référence | État observation | Dernier SHA vérifié (source) | CI courante | Phase manuelle |
|---|---|---|---|---|---|
| bubth720/JAVIS-Local-v2 | main | success | 226e2e8cc3eebd479805b89d035eb5c1cbcad540 (git) | not_checked | unknown |
| bubth720/JARVIS-LLM | mission-003b-resources | success | 1756e29557287550b5cfdffdd911cada2a302db6 (git) | not_checked | unknown |
| bubth720/JARVIS-VOICE | feat/voice-identity-005h | success | 11a4148cecc5279c8cf5e7ad420f08b2853cb7ab (git) | not_checked | unknown |
| bubth720/JARVIS-INTERFACE | development/mission-002 | success | d1c0931c4507e9af8f1aa60951947c23f4394b56 (git) | not_checked | unknown |
| bubth720/JARVIS-INTERFACE- | main | success | a857f5019354ea1c912e6f66bebdcc053c0cb700 (git) | not_checked | unknown |
| bubth720/JARVIS-NEXUS | main | success | b27df0b84d8f0082d17ca6278549298aaaf97926 (git) | not_checked | unknown |
| bubth720/JARVIS-VOLUTION- | main | success | a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0 (git) | not_checked | unknown |
| bubth720/JARVIS-SERVICES | main | success | c9f94ad2fa219a5e09cda92fb451aca606ee1646 (git) | not_checked | unknown |
| bubth720/JARVIS-UNIFIED | main | success | e4435f4bd60c5fdc5595c411cc8cab9da7ef020b (git) | not_checked | in_progress |

## Missions

| ID | Dépôt / branche | Observation / CI | Phase manuelle | Blocages manuels | Prochaine action |
|---|---|---|---|---|---|
| CORE-KNOWLEDGE | bubth720/JAVIS-Local-v2 / docs/mission-002-project-knowledge | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| CORE-TIME | bubth720/JAVIS-Local-v2 / fix/api-24-25-time-reply | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| CORE-SQLITE | bubth720/JAVIS-Local-v2 / fix/sqlite-data-preservation | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| LLM-002 | bubth720/JARVIS-LLM / mission-002-prototype | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| LLM-002B | bubth720/JARVIS-LLM / mission-002b-memory | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| LLM-002C | bubth720/JARVIS-LLM / mission-002c-tablet | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| LLM-003 | bubth720/JARVIS-LLM / mission-003-catalogue | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| LLM-003B | bubth720/JARVIS-LLM / mission-003b-resources | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| VOICE-CPU | bubth720/JARVIS-VOICE / feat/pocket-tts-cpu-prototype | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| VOICE-005D-G | bubth720/JARVIS-VOICE / feat/android-pocket-cloning-005d | success / not_checked | unknown | Validation humaine sur les appareils cibles non démontrée par l’audit Mission001.; Échecs historiques AudioTrack005D et de parité FP32 à distinguer des résultats 005F/G. | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| VOICE-005H | bubth720/JARVIS-VOICE / feat/voice-identity-005h | success / not_checked | unknown | aucun renseigné | Auditer cette nouvelle branche ; ne pas annoncer une validation de clonage par son seul nom. |
| INTERFACE-002 | bubth720/JARVIS-INTERFACE / development/mission-002 | success / not_checked | unknown | aucun renseigné | Vérifier le contenu de la branche et ses preuves GitHub avant de qualifier la mission. |
| UNIFIED-001 | bubth720/JARVIS-UNIFIED / audit/mission-001 | failure / not_checked | completed | Branche locale non publiée sur GitHub ; aucune publication autorisée. | Préserver les livrables locaux ; mise à jour GitHub uniquement après une publication autorisée séparément. |
| UNIFIED-002 | bubth720/JARVIS-UNIFIED / mission-002-backup | failure / not_checked | completed | Branche locale non publiée sur GitHub ; aucune publication autorisée. | Préserver les livrables locaux ; mise à jour GitHub uniquement après une publication autorisée séparément. |
| UNIFIED-003 | bubth720/JARVIS-UNIFIED / mission-003-central-registry | failure / not_checked | in_progress | Branche locale non publiée sur GitHub ; aucune publication autorisée. | Préserver les livrables locaux ; mise à jour GitHub uniquement après une publication autorisée séparément. |

## Limites

- Les états manuels, décisions et preuves locales ne sont jamais remplacés par GitHub.
- CI : GitHub Actions au SHA exact, derniers essais par workflow/événement ; pas de certification des tests ni de lecture des logs.
- PR : recherche limitée aux branches du même dépôt ; pas de découverte de missions ou branches automatique.
- Mode git : PR/CI not_checked. Mode demo : données synthétiques, aucune preuve GitHub réelle.
