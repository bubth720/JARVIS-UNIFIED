# F00 — Matrice des capacités (21/11/2026)

Colonnes :

- **Spéc.** : spécifiée.
- **Code** : présente au SHA de référence.
- **JVM** : test JVM ou CPU vert.
- **Émul.** : instrumentation verte sur API 29 et 35.
- **Appareil** : vérifiée sur un téléphone réel.
- **Intégrée** : dans l'APK V3 S04.
- **Livrée** : installée chez le propriétaire.

Valeurs :

| Valeur | Sens |
|---|---|
| ✔ | Prouvé, avec la référence indiquée |
| ◐ | Partiel |
| ✘ | Absent |
| NOT_RUN | Jamais exécuté |
| BLOCKED | Exécution impossible pour une raison nommée |

Références :

- **[S04]** : INTERFACE `e6489bf`, run [44638538519](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/44638538519). Journaux : qualification 11/11 et audits « 30/30 criteria, 26 recorded cases » sur API 29 et 35.
- **[L]** : rejeu local du 21/11 (`local-replay-results.txt`).

| Capacité | Module(s) | Spéc. | Code | JVM | Émul. | Appareil | Intégrée | Livrée | Preuve / remarque |
|---|---|---|---|---|---|---|---|---|---|
| Conversation texte hors ligne, mode avion | CORE+LLM+INTERFACE | ✔ | ✔ | ✔ [L] 37/37 | ✔ [S04] f, i, m | NOT_RUN | ✔ | ✘ | Qwen3-0.6B, A02 scellé |
| Boucle vocale micro → STT → LLM → TTS | VOICE+INTERFACE | ✔ | ✔ | — | ◐ [S04] c, d2, d3 (WAV injecté) | BLOCKED_DEVICE | ✔ | ✘ | Micro et haut-parleur réels non qualifiés (A-013) |
| Annulation, retour au repos, cycle de session | CORE+INTERFACE | ✔ | ✔ | — | ✔ [S04] j, d3, h4 | NOT_RUN | ✔ | ✘ | A-026 |
| Refus si modèle absent ou altéré | CORE+LLM | ✔ | ✔ | — | ✔ [S04] b (import vérifié SHA-256) | NOT_RUN | ✔ | ✘ | Cas « modèle corrompu sur appareil » non testé |
| Identité Athéna, persona, tutoiement | CORE+INTERFACE | ✔ | ✔ | ✔ | ✔ [S04] f | NOT_RUN | ✔ | ✘ | A-023 : vouvoiement résiduel (limite du modèle) |
| Mémoire durable avec consentement | CORE mem-02 + INTERFACE | ✔ | ✔ | — | ✔ [S04] h, b3, a5, g6 | NOT_RUN | ✔ | ✘ | Export chiffré ✘ (A-019) |
| NEXUS : import, FTS5, citations | NEXUS+INTERFACE | ✔ | ✔ | NOT_RUN [L] (Google Maven refusé) | ✔ [S04] g, a3, a4, f6 | NOT_RUN | ◐ (pin `06ccf98`, en retard) | ✘ | PDF et Kiwix ✘ (A-020) |
| Documents jamais pris pour des consignes | INTERFACE | ✔ | ✔ | ✔ [L] | ✔ [S04] F4, L, Q | NOT_RUN | ✔ | ✘ | Couche 1 seule : 9/30 attaques inédites détectées |
| Valeur absente ou contradictoire dite, jamais inventée | INTERFACE | ✔ | ✔ | ✔ [L] | ✔ [S04] c8, F2, R | NOT_RUN | ✔ | ✘ | |
| Sphère immobile hors réponse, coût borné | INTERFACE | ✔ | ✔ | — | ✔ [S04] K, P | NOT_RUN | ✔ | ✘ | A-008 et A-040 corrigés dans S04 (à confirmer sur appareil) |
| Accessibilité (48 dp, live regions) | INTERFACE | ✔ | ✔ | — | ✔ [S04] E6 | BLOCKED_DEVICE (TalkBack réel) | ✔ | ✘ | |
| Robustesse : journal tronqué, stockage plein, micro refusé, thermique | INTERFACE | ✔ | ✔ | ✔ [L] | ✔ [S04] S, T, g1, g2 | NOT_RUN | ✔ | ✘ | |
| Pas d'Internet, sauvegarde et transfert bloqués | INTERFACE | ✔ | ✔ | — | ✔ [S04] audit `aapt` debug et release | NOT_RUN | ✔ | ✘ | A-038 |
| APK release non débogable | INTERFACE | ✔ | ✔ | — | ◐ release **non signée** auditée [S04] | ✘ | ✘ | ✘ | Signature : geste du propriétaire (A-039) |
| Avatar Athéna 2D procédural | INTERFACE | ✔ | ✔ | — | ✔ [S04] E7 et captures | NOT_RUN | ✔ | ✘ | 2.5D et 3D ✘ ; importeur PNG sur branche séparée |
| Command Center V2 (10 onglets) | INTERFACE | ✔ | ✔ | ✔ | ✔ captures run 44034195561 | NOT_RUN | ✔ | ✘ | MISSIONS, AGENTS, AUTOMATIONS « à connecter » |
| SERVICES : actions permissionnées | SERVICES+UNIFIED M56 | ✔ | ◐ (OFF) | NOT_RUN [L] (Google Maven refusé) | ✘ | ✘ | ✘ | ✘ | CI SERVICES verte le 29/10 ; M56 sans PR |
| RESEARCH Web | UNIFIED B0 | ✔ | ◐ (loopback synthétique) | ✔ [L] 63/63 à `f1f30dc` sous 3.12 | — | — | ✘ | ✘ | Aucun réseau réel |
| EVOLUTION : diagnostic, recommandations, rapport | EVOLUTION | ✔ | ✔ | ✔ [L] 51/51 à `c4abfb0` | — | — | ✘ | ✘ | Adaptateur CORE ✘ |
| EVOLUTION : essai de correctif en sandbox | EVOLUTION | ✔ | ◐ (verrous) | ✔ (refus testés) | — | — | ✘ | ✘ | **BLOCKED** : `SANDBOX_NOT_QUALIFIED` |
| Architecture PC + Android | UNIFIED ARCH-01 | ◐ | ✘ | ✔ arch01 24/24 (contrats) | — | BLOCKED (pas de mini-PC) | ✘ | ✘ | |
| LLM 1.7B | LLM | ✔ | ✔ (laboratoire) | — | ◐ (coupé par le délai de 90 s, A-012) | BLOCKED_DEVICE | ✘ | ✘ | Décision du propriétaire après mesure |
| LEARNING-L01 | — | ✘ (PDF absent) | ✘ | — | — | — | ✘ | ✘ | A-021 |
