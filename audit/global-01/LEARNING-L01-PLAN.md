# LEARNING-L01 — plan préparatoire (non démarré)

**Statut :** plan rédigé à partir des exigences du message du propriétaire du 14/11/2026.

- Le cahier des charges de référence **`JARVIS_LEARNING_L01_Mission_Codex.pdf` n'est pas présent dans la
  session** : il n'a pas été transmis et n'existe dans aucun dépôt autorisé.
- La couverture de ses exigences sera vérifiée ligne à ligne dès réception.
- Aucune implémentation avant validation du plan de stabilisation.

## Boucle

1. Observation autorisée
2. Détection d'anomalie
3. Vérification indépendante
4. Hypothèse
5. Expérience isolée
6. Comparaison avec la référence
7. Rapport
8. **Proposition en attente d'approbation**

## Architecture proposée (première version, conforme à la clause d'isolation)

**Choix proposé :** une isolation exécutable sûre n'est pas démontrable sur Android avec le moteur actuel (un
seul moteur par processus, budget mémoire). La première version est donc **limitée aux évaluations de
données et aux variantes non exécutables d'instructions**, comme le prévoit la demande.

| Composant | Rôle | Emplacement envisagé |
|---|---|---|
| Collecteur consenti | Enregistre un événement (question, réponse, mesures, décision de l'utilisateur) **seulement si l'interrupteur LEARNING est activé** (désactivé par défaut). Purge et export. | INTERFACE `conv/learning` (stockage isolé, noBackup) |
| Expurgation | Retire prénoms, souvenirs, extraits de documents et nombres longs avant stockage ; tests dédiés | idem |
| Classifieur | `FACTUAL_ERROR`, `REASONING_CONSTRAINT`, `STYLE_PREFERENCE`, `SAFETY_REGRESSION`, `UNKNOWN` | idem (règles) |
| Vérificateurs déterministes (prioritaires) | Calcul (évaluation exacte), contradiction avec un fait ou document cité, action prétendue (ActionGuard), contrainte Android connue, longueur | idem |
| Juge LLM local (limité) | Uniquement si aucun vérificateur ne s'applique ; verdict marqué « avis du modèle, non probant » | idem |
| Laboratoire d'expériences | Rejoue un **jeu synthétique ou autorisé** avec l'instruction de référence et une variante d'instruction : même moteur, même graine, mêmes limites. Hors session de conversation, arrêt sous contrainte (thermique, mémoire, batterie). | Harnais Linux CI (JARVIS-LLM) et, sur Android, test instrumenté isolé |
| Comparateur | Améliorations et régressions par catégorie. **Toute régression `SAFETY_REGRESSION` rejette la variante.** | — |
| Propositions | Fiche explicable : anomalie, preuve, variante, gains, pertes, risques. État `EN_ATTENTE` → approbation ou refus par le propriétaire. **Jamais appliquée automatiquement.** | Command Center › onglet LEARNING |

## Interdits vérifiés par test

LEARNING-L01 ne modifie jamais automatiquement :
- le code actif ;
- les poids ;
- les permissions ;
- les secrets ;
- les directives de sécurité ;
- la personnalité durable ;
- la configuration de production.

**Vérification :** chaque test compare empreinte avant / après du dossier de configuration de production, des
préférences de personnalité et de l'APK.

## Tests LEARNING (exigés)

| # | Scénario | Vérificateur | Niveau |
|---|---|---|---|
| L1 | Calcul faux détecté ; calcul juste non pénalisé | Évaluation arithmétique exacte | J + L |
| L2 | Préférence de concision détectée sans dégrader les explications complexes | Longueur + catégorie de question | J + L |
| L3 | Contrainte Android contradictoire détectée | Règles connues (permission, mémoire, thermique) | J |
| L4 | Instructions malveillantes dans un document : ignorées, signalées | Détection d'injection + absence d'effet | E |
| L5 | Interruption vocale **non** interprétée comme insatisfaction | Classifieur → `UNKNOWN` | J |
| L6 | Variante plus « agréable » mais qui dégrade la sécurité : **rejetée** | Comparateur `SAFETY_REGRESSION` | L |
| L7 | Collecte refusée sans consentement | Interrupteur désactivé → 0 événement | J + E |
| L8 | Purge vérifiable sur disque | Fichiers absents après purge | E |
| L9 | Fonctionnement hors ligne | Mode avion | E |
| L10 | Arrêt propre sous contrainte de ressources | Thermique / mémoire simulés | E |
| L11 | Aucune modification de production | Empreintes avant / après | E |

## Interface

- Nouvel onglet **LEARNING** du Command Center : anomalies, expériences, résultats, risques, propositions en
  attente. Approuver ou refuser une proposition ne fait que **marquer la décision** : l'application d'une
  variante reste un changement de code revu.
- La sphère n'est pas concernée : elle reste immobile hors réponse et n'est pas manipulable.

## Ordre proposé

LEARNING-L01 démarre **après** STABILISATION-01, dans cet ordre :

1. Réception du PDF et vérification de couverture.
2. Validation de ce plan par le propriétaire.
