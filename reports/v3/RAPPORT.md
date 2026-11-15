# JARVIS INTERFACE V3 — Holographic Cockpit : rapport de qualification (14/11/2026)

**Statut : APK de démonstration qualifiée sur émulateurs (API 29 et 35). Prête pour une évaluation visuelle sur appareil, après autorisation du propriétaire.**

Les mesures viennent d'émulateurs x86_64 à rendu logiciel (swiftshader), au profil pixel_6 (1080×2400), en mode avion. **Aucune ne vient d'un téléphone.**

## Livrables

| Élément | Valeur |
|---|---|
| Dépôt / branche | `bubth720/JARVIS-INTERFACE` @ `ccr-5cf17ed2-phgk00` |
| Commit qualifié | `1f169ae` (captures versionnées par la CI : `bce7b30`) |
| Exécution CI | run **43522819722**, **succès** |
| APK `fr.jarvis.v3` (« JARVIS V3 », 3.0.0-demo, arm64-v8a + x86_64) | https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/43522819722/artifacts/14084597077 |
| SHA-256 de `app-debug.apk` | `b35c563c7d0b686ab27665c169b9156385ab42e6cc07596104ed8abbaf83ee5f` |
| Captures réduites et rapports JSON | `labs/v3/captures/run-43522819722/` (dans le dépôt) |
| Preuves complètes | https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/43522819722/artifacts/14087718923 |

Fichiers ajoutés (aucun autre module, aucun fichier V1 modifié ; la garde `labs/v3/tools/check_scope.py` vérifie 430 fichiers figés) :
- `.github/workflows/v3-cockpit.yml` ;
- `labs/v3/` : 26 fichiers, dont `VisualTheme`, `HologramSphere`, `ContextCardHost`, `RadialNavigation`, `ConversationDock`, `PerformanceGovernor`, `CockpitScene`, `CockpitActivity`, `StateGalleryActivity`, `model/*`, des tests JVM et instrumentés, et des outils.

## Résultats (run 43522819722)

| Test | API 29 | API 35 |
|---|---|---|
| a — une seule permission (micro), pas d'Internet, installable sans `-t` | PASS | PASS |
| b — premier lancement, puis import vérifié des ressources | PASS | PASS |
| c — états réels (repos, clavier, réflexion, diffusion, parole, erreur, réponse, écoute, transcription), fiches, menu radial, module indisponible, réglages, fiche système, geste sur la sphère, paysage, arrière-plan | PASS | PASS |
| d — mouvement réduit Android : sphère immobile (0 image en 2 s) et 1er texte | PASS | PASS |
| e — galerie des 7 états (prototype EXEMPLE) et banc avant/après | PASS | PASS |
| Réouverture après arrêt forcé / aucun crash | PASS / PASS | PASS / PASS |
| Tests JVM (géométrie, états, fiches, intentions, mots-clés, menu) | 8/8 | — |

Mesures relevées :
- Réponse réelle affichée : « La capitale de la France est Paris. ».
- Fiche système : « Batterie : 100 % (en charge). », issue d'une mesure Android, sans appel au LLM.
- Arrière-plan : 0 image dessinée (API 29 et 35), reprise au retour (21 à 22 images).
- Geste : 19 événements de glissement, rotation de −5,9 rad.

## Écarts et anomalies

1. **Coût de rendu** : la sphère V3 coûte plus cher que la sphère V1 dans la même zone. Médiane du temps d'image sur émulateur logiciel :

   | Profil | V1 (M55-D) | V3 |
   |---|---|---|
   | Équilibré | 124–141 ms | 163–190 ms |
   | Économie | 94–104 ms | 150–186 ms |

   Le gouverneur bascule de lui-même en Économie (≈ 11 FPS mesurés). Ce n'est pas représentatif d'un GPU de téléphone.
2. **Impact sur le LLM** : avec la sphère animée, le 1er texte arrive en **26–29 s**, contre **12,8 s** quand la sphère est immobile (mouvement réduit). Sur émulateur, l'animation concurrence le LLM pour le CPU. C'est à mesurer impérativement sur le POCO.
3. **Affichage en double** : après une erreur de sortie vocale, la question et la réponse précédentes réapparaissent dans la zone « en cours » pendant le tour suivant. En V1, `partial` est conservé si la fin est en erreur. Correctif V3 proposé, non appliqué : n'afficher `partial` qu'en phase THINKING, et effacer `pending` à chaque nouvel échange.
4. **Menu radial** : l'élément « Cockpit » chevauche le champ de saisie quand le menu est ouvert.
5. **Saisie de test** : la frappe système est trop lente sur l'émulateur saturé. Le test bascule alors sur la saisie par accessibilité (consignée `inputMethod`). C'est une limite de l'environnement de test, pas de l'application.
6. **Voix** : le haut-parleur de l'émulateur ne lit pas (« Délai de lecture audio dépassé », comme en V1). La reconnaissance sur une voix espeak est médiocre, ce qui donne de mauvais mots-clés (« Pouf », « Appelte »).

## Conformité au cahier des charges V3

| Exigence | État |
|---|---|
| A — sphère en couches, animations par état, gestes, mode économie, pause en arrière-plan, mouvement réduit | Fait (rendu et fluidité à valider sur GPU réel) |
| C — fiches avec provenance, compacte/agrandie, épingler, citer, explorer, états vides honnêtes, fiche système mesurée | Fait (sans image locale : illustration de substitution) |
| D — 5 destinations, arc, assombrissement, halo, retour Android, cibles de 48 dp, variante TalkBack | Fait (chevauchement « Cockpit » à corriger) |
| Portrait et paysage, états d'écran obligatoires avec captures | Fait (transitions vidéo : NOT_RUN) |
| Planche comparative avec les deux images de référence | Non publiée (images privées du propriétaire) ; comparaison qualitative seulement |
| Avatar B | Hors périmètre (reporté) |
| Notation artistique 0–5 | Appartient au propriétaire |
