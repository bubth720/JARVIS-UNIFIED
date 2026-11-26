# F00 — GO / NO-GO par lot

Une valeur `UNKNOWN` ou `NOT_RUN` ne vaut jamais GO. Un GO ci-dessous signifie seulement « le lot peut **démarrer** sur une branche isolée ». Ce n'est en aucun cas une autorisation de fusion, d'installation ou d'activation.

| Lot | Verdict | Condition ou blocage |
|---|---|---|
| F00 inventaire | **DONE_EVIDENCED** | 119 PR (113 ouvertes, 111 brouillons) recensées sans doublon, 255 branches, CI au SHA. CORE : CI et bases `UNKNOWN` (R-05). |
| F01 contrats et CI de reprise | **GO** (`f01/gates/F01.verdict.json`) | ADR-F01-01 acceptée ; épinglages NEXUS, LLM et VOICE NO-GO (`f01/gates/PIN-*.verdict.json`) |
| F02 Android de bout en bout | PARTIAL / BLOCKED_DEVICE | Émulateur vert à `e6489bf` ; appareil requis (R-09). |
| F03 LLM | GO (laboratoire CPU et CI) / BLOCKED_DEVICE (mesures) | Aucune valeur TTFT ou thermique sans appareil ; GPU payant désactivé. |
| F04 VOICE | GO (CI) / BLOCKED_DEVICE (audio réel) | Écart d'épinglage `92d0745` → `5890735`. |
| F05 INTERFACE | GO sur `e6489bf` | Release non signé seulement (R-08) ; TalkBack réel `BLOCKED_DEVICE`. |
| F06 NEXUS | GO (CI) | Écart d'épinglage de 27 commits (R-04) ; compilation locale `BLOCKED` (R-06) ; réseau extérieur OFF. |
| F07 SERVICES | GO (laboratoire OFF) | M56 sans PR (R-01) ; aucun service activé par défaut. |
| F08 EVOLUTION | GO (diagnostic et adaptateur lecture seule) / **BLOCKED** (essai de correctif) | `SANDBOX_NOT_QUALIFIED` (R-10). |
| F09 apprentissage et mémoire | GO (après F06/F07) | Mémoire consentie déjà embarquée (mem-02 ⊂ `5da9838`). |
| F10 PC + Android | GO (simulation et contrats) / BLOCKED (mini-PC) | |
| F11 réception | **NO-GO** | Exige F02 sur appareil, signature et décisions R-01 à R-12. |
