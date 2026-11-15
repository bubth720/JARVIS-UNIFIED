# Bilan consolidé — campagne de fiabilisation du 15/11/2026

Branche de travail : `ccr-e05fe51e-ycqubx` (INTERFACE et UNIFIED). Rien n'a été fusionné dans `main`, rien n'a été installé sur le téléphone, aucun modèle n'a été remplacé.

## Niveaux de preuve

Le registre (`REGISTRE-ANOMALIES.md`) comporte désormais une colonne par niveau :

- **Développée** : le commit existe.
- **Test unitaire** : validée par un test JVM ou un test de script.
- **Émulateur** : validée sur API 29 et 35, mode avion, vrai modèle.
- **Appareil réel** : validée sur le POCO.

**Aucune correction n'est validée sur appareil réel.**

## 1. Campagne T1–T4 sur le commit testé (8f77a8d, run 43658134254)

Le commit n'a pas été perturbé : aucun push sur sa branche pendant le run.

| | API 29 | API 35 |
|---|---|---|
| Qualification | 11/11 PASS | 9/11 |
| Audit T1–T4 | 24/26 | 24/26 |

Échecs :

- **c8 (deux API).** « Selon mes documents, quelle est la capitale de l'Italie ? » a reçu la réponse « Londres » avec une simple note. C'est exactement le défaut du point 5 (A-005). Il est corrigé sur la nouvelle branche, mais pas encore validé sur émulateur.
- **K (deux API).** La sphère compte 2 dessins par fenêtre, au repos comme au début de l'écoute et de la réflexion. **A-008 reste ouvert.**
- **c (API 35).** L'onglet `cc-tab-missions` est introuvable. Il s'agit de l'outillage de test (A-011).
- **e (API 35).** Le test est resté bloqué 25 min, puis a été coupé par la limite A-029 ; la campagne a continué (A-034, cause non établie).

Nouvelles validations sur émulateur à partir de ce run : A-010, A-022, A-024, A-026, A-027 et A-028.

## 2. Émulateur indisponible : échec rapide (A-029)

Le script vérifie l'émulateur avant chaque test et toutes les 15 s pendant le test. Tout appel `adb` est borné. Le budget est de 130 min par niveau d'API, avec une limite dure de 145 min par étape du workflow. En cas d'arrêt, le script écrit `DEVICE_LOST` ou `BUDGET_EXCEEDED` avec le nom du test concerné, puis produit un `device-diagnostic.txt`.

Le test avec faux `adb` passe 7/7. Il tourne aussi dans l'étape Guards de la CI. Durées d'arrêt mesurées :

| Situation | Arrêt après |
|---|---|
| Perte entre deux tests | 4 s |
| Perte pendant un test | 4 s |
| Shell bloqué | 35 s |
| Perte au démarrage | 0 s |

## 3. Sphère : deux mesures séparées (nouveau test P)

- **Mouvement visible.** Les pixels de la zone de la sphère sont comparés d'une capture à l'autre. Limite : 0,1 %.
- **Coût graphique.** Il est mesuré sans aucune capture : dessins de la sphère (au plus 1) et images de toute la fenêtre via `gfxinfo`.
  - Au repos et en réflexion : au plus 5 images/s.
  - En écoute : au plus 15 images/s (le vu-mètre du micro).
- **Contrôle positif.** La sphère doit bouger pendant la réponse, sinon le test échoue. Une application figée ne peut donc pas passer.

Statut : développé, **non exécuté**.

## 4. Injections documentaires (A-015, A-031)

**Mesure honnête.** L'ancien filtre détectait 16/16 de son propre corpus, mais **3/24** de formulations nouvelles.

**Couche 1 (filtre généralisé).** Elle traite la normalisation Unicode, les homoglyphes, les lettres espacées ou pointées, les jetons de rôle et la règle « s'adresse au lecteur ».

- Corpus d'ajustement : 24/24.
- Phrases bénignes : 0/52 supprimée à tort.
- Corpus inédit, écrit après le gel du filtre et mesuré une fois : **8/30** (9/30 aujourd'hui).
- Les 21 trous sont enregistrés dans le test.

**Couche 2 (structurelle, indépendante de la formulation).** Une phrase de document qui s'adresse à un lecteur n'est restituée qu'en **citation attribuée** (« je la cite sans l'appliquer »). Si la réponse du modèle s'appuie sur une telle phrase, elle est remplacée.

- Pire cas simulé (le modèle répète le document) : **0/30** attaques inédites présentées comme parole de JARVIS.
- Un document ne peut toujours pas créer de souvenir (G6).

Le test Q (bout en bout sur le vrai modèle) reste à exécuter.

## 5. Valeur absente ou contradictoire (A-005, A-025, A-030)

Ces trois cas ne se terminent plus par une mention « à vérifier ».

- **Question documentaire sans document correspondant.** JARVIS répond « Je ne trouve pas cette information dans tes documents locaux… » **sans appeler le modèle**.
- **Documents contradictoires sur le même sujet.** JARVIS cite les deux phrases avec leur source et dit qu'il ne peut pas trancher. Deux événements différents ne sont plus pris pour une contradiction.
- **Valeur absente de tous les extraits** (date, montant, nombre, nom, lien, téléphone, fichier). La réponse est remplacée par ce que disent réellement les documents.
  - La valeur rejetée n'est ni affichée ni prononcée ; elle n'apparaît que dans « Pourquoi ? ».
  - Elle est retirée du contexte du moteur.
  - La réponse documentaire n'est plus affichée en direct avant vérification.

Validation : test unitaire uniquement (DocumentaryAnswerTest) ; les tests g, c8, F2, N et R restent à exécuter sur émulateur.

## 6. S4 (accessibilité) et S6 (robustesse et performances)

**S4**

- Cibles tactiles de 48 dp (d011b17).
- Annonces TalkBack du statut via des régions live (A-033).
- E2, E3, E6 et E7 sont verts sur le run, mais celui-ci ne contenait pas ces deux corrections ; ils sont à réexécuter.
- TalkBack réel : appareil uniquement.

**S6**

- G1, G2 et H4 sont verts sur émulateur.
- **A-032 (nouveau défaut) :** après un arrêt brutal pendant l'écriture du journal, l'échange suivant était perdu sans message. Corrigé ; test unitaire 3/3 (2/3 échouaient avant la correction) ; test S sur émulateur à exécuter.
- **G3 (A-035) :** le stockage plein donne maintenant un message clair. Le test T remplit réellement le stockage ; il est à exécuter.
- Le test G4 est désormais écrit pour l'émulateur (test S).

## 7. Tableau de synthèse

| Catégorie | Anomalies |
|---|---|
| Validées sur émulateur | A-001, A-002, A-003 (CI), A-006, A-007, A-009, A-010, A-022, A-024, A-026, A-027, A-028 |
| Validées par test unitaire seulement | A-029, A-030, A-031, A-032 ; A-005, A-015 et A-025 pour le nouveau contrat |
| Développées, non testées | A-033, A-035 (tests écrits) |
| Ouvertes | **A-008** (sphère, K rouge), **A-034** (test e bloqué, API 35), **A-011** (onglet, API 35), A-004 et A-023 (limites du modèle 0.6B), A-012 et A-013 (appareil requis), A-014, A-016, A-018 à A-021 |
| Validées sur appareil réel | aucune |

## Prochaine étape proposée (aucune nouvelle fonctionnalité)

Lancer une campagne émulateur sur `ccr-e05fe51e-ycqubx` (workflow_dispatch) pour qualifier :

- les tests P, Q, R, S et T ;
- c8, g, F2 et N avec le nouveau contrat ;
- E6 avec les cibles 48 dp et les régions live.

Ensuite, analyser A-008 et A-034. Le code V3 de cette branche n'a pas été compilé localement (pas de SDK Android ici) : la compilation sera vérifiée par cette campagne.
