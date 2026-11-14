# CONVERSATION-01 — étude du modèle de langage (0.6B actuel vs 1.7B autorisé pour étude)

Date : 14/11/2026. Branche JARVIS-LLM `ccr-5cf17ed2-phgk00`.

> **Décision demandée au propriétaire, rien n'est appliqué.** Aucun remplacement du modèle, aucun
> téléchargement sur le téléphone, aucune intégration du 1.7B en production. Le 0.6B reste le modèle de l'application.

## Cadre de mesure

- **Où :** uniquement en CI Linux x86_64 (runner GitHub `ubuntu-24.04`). Ce **n'est pas** un téléphone : les
  latences absolues ne valent pas pour le POCO X8 Pro, seuls les écarts relatifs sont informatifs.
- **Poids :** depuis la source officielle, empreinte SHA-256 contrôlée avant tout chargement
  (manifestes `a02/models/qwen3-0.6b-q4km.json` et `a02/models/qwen3-1.7b-q4km.json`).
  - Qwen3-0.6B Q4_K_M : `ac2d9771…`.
  - Qwen3-1.7B Q4_K_M : `b139949c…`.
- **Moteur :** le moteur A02 protégé, inchangé : chargement scellé (memfd), plafond de sortie 128, 3 échanges
  d'historique au plus.
- **Banc :** 44 scénarios français publiés.
  - `fr-bench-30` (30 scénarios) : factuel, reformulation, raisonnement, multi-tours, ambigu, refus,
    documents absents.
  - `fr-conv-01` (14 scénarios) : référence implicite, correction, changement de sujet, information manquante,
    incertitude, longueur, initiative, chaleur, humour, identité.
  - Notation par mots-clés publiée (`bench_score.py`) : grossière, mais identique pour toutes les configurations.
- **Robustesse :** 20 sessions chargement/déchargement par configuration ; mémoire partagée après déchargement
  mesurée.

## Résultats (runs 43588723772 et 43590133529)

| Configuration | Instruction | Score /44 | 1er jeton p50 / p95 | Total p50 / p95 | RSS chargé | 20 sessions |
|---|---|---|---|---|---|---|
| 0.6B ctx768 1 thread | PRODUCTION (V1) | 23 (deux runs) | 2,1–3,0 / 3,4–4,8 s | 2,7–3,8 / 3,6–5,1 s | 567 Mio | OK, 0 Mio résiduel |
| 0.6B ctx768 1 thread | ATHENA complète | 25 (deux runs) | 6,2–7,3 / 8,6–10,1 s | 7,2–8,6 / 9,5–11,4 s | 567 Mio | OK (après correction du budget de temps) |
| 0.6B ctx768 1 thread | ATHENA_COMPACT v1 | **26** | 3,5 / 5,2 s | 4,9 / 6,7 s | 567 Mio | OK |
| 1.7B ctx768 1 thread | ATHENA complète | **37** | 7,6 / 11,0 s | 10,8 / 19,0 s | 1 884 Mio | OK |
| 1.7B ctx1536 2 threads | ATHENA complète | 36 | 2,9–4,0 / 4,0–5,3 s | 3,9–6,4 / 6,1–10,4 s | 1 968 Mio | OK |

**Variabilité :** les runners CI partagés varient. Par exemple, PRODUCTION mesure 2,1 s puis 3,0 s de premier
jeton sur deux runs. Ne comparer que des ordres de grandeur.

### Ce que montrent les réponses

- **0.6B, culture générale (PRODUCTION 2/10, COMPACT 4/10) :** faux fréquents.
  - « capitale de l'Italie : Londres » ;
  - « Les Misérables : Alfred Dreyfus » ;
  - « 17 est pair ».

  L'instruction ne corrige pas un manque de connaissances.
- **0.6B, contexte et mémoire :** prénom, correction du prénom, frère de 12 ans, rendez-vous corrigé et
  « 144 / 4 = 36 » sont **réussis**. Le rappel des faits par l'instruction fonctionne.
- **0.6B, instruction complète :** elle double le temps du premier jeton (texte plus long à traiter).
  Elle fait aussi commencer presque chaque réponse par « Bonjour ! Je suis JARVIS ». **Écartée pour le 0.6B.**
- **0.6B, ATHENA_COMPACT v1 :** meilleur score, mais **0/2 sur les refus**. Elle a répondu « Je l'ouvre,
  voici la lumière du salon » et a prétendu envoyer un e-mail. Régression de sécurité : une phrase explicite
  « aucune action » est ajoutée (3e2560e), mesure en cours.
- **1.7B :** factuel 8/10 et raisonnement 5/5. Erreurs restantes :
  - Les Misérables attribué à Dickens ;
  - planète la plus proche du Soleil : « la Terre » ;
  - Espagne : « le français » ;
  - un refus raté (« La lumière du salon est allumée »).

  Ton nettement plus naturel et tutoiement tenu.

## Analyse

| Critère | 0.6B (actuel) | 1.7B |
|---|---|---|
| Qualité conversationnelle mesurée | 23–26/44 | 36–37/44 (+ ~50 %) |
| Contexte / corrections / mémoire de conversation | bon avec les faits rappelés | bon |
| Culture générale | faible, erreurs affirmées | correcte, quelques erreurs |
| Mémoire vive | ~0,57 Gio | ~1,9 Gio (×3,3) |
| Latence sur runner, réglages du téléphone (1 thread) | 2–3 s au 1er jeton | 7–8 s au 1er jeton |
| Latence avec 2 threads et ctx 1536 | — | 3–4 s, mais **réglages hors politique A02 actuelle** (1 thread, ctx 768) |
| Fichier | ~0,4 Go | ~1,1 Go |

## Recommandation (à valider par le propriétaire)

1. **Maintenant, sans changer de modèle :** garder le 0.6B. Utiliser dans l'application la personnalité
   Athéna **compacte** et le rappel des faits de la conversation (intégrés dans INTERFACE `labs/v3`, branche
   `ccr-5cf17ed2-phgk00`). La version complète n'est gardée que comme option pour un modèle plus grand.
2. **Le 1.7B est la seule piste mesurée qui améliore nettement la conversation.** Avant toute intégration,
   trois choses sont nécessaires :
   - ton autorisation explicite ;
   - une mesure **sur le POCO X8 Pro** (latence, chaleur, mémoire disponible, autonomie) ;
   - une évolution **revue** de la politique A02 (threads/contexte), puisque la configuration rapide
     (2 threads, ctx 1536) sort des limites protégées actuelles.

   Le téléchargement sur ton téléphone n'aura lieu que si tu le décides.
3. **Pour les faits, quel que soit le modèle :** des réponses fiables passent par les connaissances locales
   (NEXUS, citations), pas par la mémoire du modèle. C'est l'étape suivante de l'intégration.

## Incident corrigé pendant l'étude

- **Symptôme :** deux jobs ont échoué sur le budget de temps fixe du harnais JNI (600 s, code 124). Le 0.6B
  ATHENA a échoué à la session 18/20 ; la JVM a signalé un SIGSEGV pendant son arrêt forcé. Le 1.7B a échoué
  après 34/44 scénarios.
- **Correction :** le budget devient réglable (`A02_JNI_TIMEOUT`). Seule l'étude le relève (2 400 s) ; le
  défaut reste 600 s pour tous les autres usages (ce499e2).
- **Vérification :** après correction, les cinq configurations passent leurs 20 sessions (run 43590133529).

## Commits JARVIS-LLM (branche `ccr-5cf17ed2-phgk00`)

| Commit | Contenu |
|---|---|
| 9eeff7b, b5bc7a0 | Banc `fr-conv-01`, instructions PRODUCTION / ATHENA, workflow `conv-01-study.yml` |
| ce499e2 | Budget de temps JNI réglable (étude seulement) |
| ce817b1 | ATHENA_COMPACT mesurée sur le 0.6B |
| 3e2560e | ATHENA_COMPACT : phrase « aucune action » (après le refus raté) |
