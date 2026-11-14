# Limites du modèle Qwen3-0.6B (distinctes des défauts logiciels)

Ce document recense ce que **le modèle** fait mal, indépendamment du code de JARVIS. Les défauts logiciels
sont dans `REGISTRE-ANOMALIES.md`. Ici, une « garde » est une protection déterministe de l'application qui
limite la conséquence d'une erreur du modèle **sans la corriger**.

**Modèle :** Qwen3-0.6B Q4_K_M (SHA `ac2d9771…`).

**Conditions :** moteur A02 protégé (contexte 768, 1 thread, sortie 128) et instruction Athéna compacte.

**Sources des mesures :**
- Études Linux : 43588723772, 43590133529, 43592731686.
- Émulateur : 43592693625, 43616811194, 43620844372, 43627862972.

| # | Limite observée | Exemple réel | Fréquence mesurée | Garde dans l'application | Ce que la garde ne résout pas |
|---|---|---|---|---|---|
| M-01 | Faits faux affirmés avec assurance | « La capitale de l'Italie est Londres » ; « Les Misérables : Alfred Dreyfus » ; « 17 est pair » | Factuel 2 à 6 / 10 selon l'instruction | « Pourquoi ? » : « non vérifié, peut se tromper » | L'utilisateur peut croire la réponse |
| M-02 | Invente une réponse documentaire absente | « Le prix du vélo électrique est de 10 euros » | Systématique sur le cas testé | Note système « cette réponse ne vient pas de tes documents » | Le texte inventé reste affiché |
| M-03 | Prétend avoir exécuté une action | « La lumière du salon est allumée » | 1/2 refus avant garde (0.6B et 1.7B) | ActionGuard : consigne ciblée + note système | — |
| M-04 | Transforme une consigne de document en fait | « la note indique que la lumière est allumée » | Cas d'injection testé | Phrases d'ordre retirées des extraits + note | Formulations non reconnues (voir A-015) |
| M-05 | Cache une contradiction entre documents | Cite « jeudi », omet « mardi » | Cas testé | Note nommant chaque version | — |
| M-06 | Répète sa réponse précédente | « Quel sport j'aime ? » → réponse sur la télévision | Observé en session longue (API 29 et 35) | Détection de répétition (en cours, A-022) | Le bon contenu n'est pas produit |
| M-07 | Dérive du tutoiement vers le vouvoiement | 3 réponses sur 16 | Session longue | Aucune (consigne système protégée en vouvoiement implicite) | — |
| M-08 | Renvoie la question au lieu d'y répondre | « Je suis JARVIS… Combien font 6 plus 1 ? » | Ponctuel (audit G1, banc F02, F05) | Aucune | Réponse inutile |
| M-09 | Ignore un fait présent dans l'instruction | Sport « randonnée » non rappelé | Session longue | Faits rappelés à chaque tour (aide partielle) | — |
| M-10 | Contexte court | 3 échanges relus au plus (politique A02) | Structurel | Mémoire de travail : faits rappelés | Nuances des échanges anciens perdues |
| M-11 | Lenteur sur émulateur x86 | 17–46 s par réponse | Émulateur, **non représentatif** du POCO | Réaction d'attente vocale (règles VOICE) | Mesure réelle : POCO |

## Comparaison avec le 1.7B (mesures Linux)

Le 1.7B corrige une large part de M-01 : factuel 8 à 9 / 10, score global 36 à 37 / 44 contre 23 à 28 / 44.
Il conserve M-03 (« La lumière du salon est allumée »). Les gardes de l'application restent donc nécessaires
quel que soit le modèle.

**Coût :** environ 2,2 fois la mémoire. Vitesse et thermique à mesurer sur le POCO (protocole prêt).
**Aucun remplacement sans ton autorisation.**
