# JARVIS-FINAL-02 — Compte rendu

- **Dépôt** : `bubth720/JARVIS-UNIFIED`, branche `feat/next-01-android-1p7b-20261126`, de `bc1c7c9` (départ) à `5db8f6b` + docs.
- **Mission** : #34.
- **Aucune fusion, aucune installation, aucune signature, aucune suppression, aucune dépense.**

Documents :

- `TEST-REPORT.md` : runs et résultats exacts.
- `MODEL-COMPARISON.md` : comparaison 0.6B / 1.7B.
- `FEATURE-INVENTORY.md` : inventaire des fonctions.
- `DEVICE-RECEPTION-PROTOCOL.md` : protocole de réception sur téléphone.

## Synthèse

| Phase | Statut |
|---|---|
| 1. Déblocage CI | ✅ Les garde-fous historiques tournent **sans modification sur INTERFACE `e6489bf`**, avec leurs ressources. Les nouveaux tests tournent séparément dans le monorepo. Aucun test touché, aucune archive réintroduite. |
| 2. Qualification de l'APK (émulateur) | ✅ Run 45908509940 : **API 29 : 11/11 + 27/27 ; API 35 : 11/11 + 27/27**. Release non débogable, non signée, une seule permission, hors ligne, sans poids embarqués. ⚠️ Deux tests instables observés au run précédent : h et h4. |
| 3. Préparation du 1.7B | ✅ Intégré : catalogue, import vérifié, profils, repli vers ÉCO, un seul LLM à la fois. **Non activé par défaut**, car la qualification n'est pas atteinte : 4/59 tours dépassent le délai de 90 s sur émulateur à 768/1, et il n'existe aucune mesure sur téléphone. |
| 4. Livraison | ✅ APK candidate `da766bec…` (reproductible), rapports, protocole téléphone, inventaire, blocages, PR brouillon. |

## Par module

| Module | Mission | Branche | Commit | Tests | Performances | Blocages | Prochaine action |
|---|---|---|---|---|---|---|---|
| **CORE** (mémoire, journal) | Intégré dans V3 via `core-memory`, vérifié blob pour blob | UNIFIED `feat/next-01-…` (import `modules/core` @ `5da9838`) | `a40db85` (import), inchangé depuis | Qualification f, h, s, t ; audits a4, a5, b3, f6, g6, o : ✅ API 29 / 35 | Écriture du journal sans perte ; stockage plein refusé proprement | Orchestrateur CORE pas encore unique (ADR F01-01) ; lecture seule de CORE | Migrer l'orchestration selon l'ADR F01-01, après ta décision |
| **LLM** (A02, llama.cpp) | Moteur scellé ; 0.6B par défaut ; 1.7B préparé | UNIFIED (import @ `2e01177`) ; étude JARVIS-LLM `ccr-e05fe51e-ycqubx` | `a40db85`, `29a7849` ; LLM `9eedb47` | Linux 4/4 (natif 37/37 chacun) ; émulateur 3/3 ; audits h4, m, i : ✅ | Voir le tableau ci-dessous | 1.7B trop lent à 768/1 sur émulateur ; pas de mesure ARM ; « Android prototype checks » du dépôt LLM non concluant (téléchargement Maven) | Protocole B sur téléphone ; relancer « Android prototype checks » |
| **VOICE** (STT whisper, TTS pocket) | Embarquée, sans poids | UNIFIED (import @ `92d0745`) | `a40db85`, inchangé | d2, d3, g1 : ✅ (émulateur, audio simulé) | Non mesurées sur un vrai micro ou haut-parleur | **Voix non testée sur téléphone** | Protocole A5 / A6 sur téléphone |
| **INTERFACE** (V3 Cockpit) | APK unifié, profils de modèle, étude | UNIFIED | `29a7849`, `cf8ab42` | 11/11 + 27/27 sur API 29 et 35 ; 72 tests unitaires ; Lint OK ; garde-fous historiques 15/15 @ `e6489bf` | Sphère : 0 dessin hors réponse ; rendu sur émulateur à GPU logiciel, non représentatif | Tests h et h4 instables (`StaleObjectException`, PSS bruité) | Rendre `tap` robuste et mesurer h4 sur une médiane, **avec ton accord** |
| **NEXUS** (connaissances locales) | Embarqué | UNIFIED (import @ `06ccf98`) | `a40db85`, inchangé | g, l, q, r, f2f3f4, a3, c8 : ✅ | — | Mise à niveau de l'épinglage NEXUS : NO-GO (F01) | F06 : test de contrat sur la candidate `5f10193` |
| **SERVICES** | Désactivé | Import `modules/services` @ `d16dd84` | `a40db85` | Non embarqué | — | ISOLATED_OFF, volontairement | F07, en laboratoire uniquement |
| **EVOLUTION** | Diagnostic uniquement | Import @ `009961a` | `a40db85` | 61/61 en lecture seule (F08), non embarqué | — | Sandbox non qualifiée | Rester en diagnostic |

### Performances mesurées (aucune sur téléphone)

| Mesure | 0.6B (ÉCO, défaut) | 1.7B 768/1 | 1.7B 1536/2 (PERFORMANCE) |
|---|---|---|---|
| Score /44 sur Linux (ATHENA / PRODUCTION) | 25 / 23 | 37 / 33 | — |
| Score /44 sur émulateur (application) | 28 | 32 | 35 |
| 1er jeton p50 sur émulateur | 17,2 s | 46,6 s | 30,5 s |
| Débit sur émulateur | 6,2 jetons/s | 2,4 | 3,8 |
| PSS chargé → après déchargement sur émulateur | 556 → 90 Mio | 1233 → 82 Mio | 1318 → 82 Mio |
| Annulation (Stop → retour) | 1 ms | 1 ms | 1–2 ms |
| Tours coupés (délai de 90 s) | 0/59 | 4/59 | 0/59 |

## Blocages restants pour un usage quotidien (par priorité)

1. **Aucun essai sur téléphone.** Le protocole `DEVICE-RECEPTION-PROTOCOL.md` est prêt. Il faut ta signature de l'APK et ton installation.
2. **Voix réelle non validée.** Ni le micro, ni le haut-parleur, ni la latence jusqu'au premier son n'ont été mesurés.
3. **Latence** : le 1er jeton du 0.6B dépasse 17 s sur émulateur, valeur probablement bien plus basse sur ARM, mais **inconnue**. Le 1.7B n'est utilisable qu'en PERFORMANCE et n'est pas qualifié.
4. **Tests instables** : h (`StaleObjectException`) et h4 (PSS bruité). Ils pourraient produire un faux NO-GO ou masquer une vraie fuite.
5. **Orchestrateur CORE unique** : il n'est pas encore en place (ADR F01-01).
6. **Épinglages LLM, VOICE et NEXUS** : les candidats restent NO-GO depuis F01.
7. **Répétitions** : 3 avis « réponse quasi identique » sur 24 tours (audit m), surtout au même rang de tour, ce qui oriente vers la qualité du 0.6B.

## Prochaines optimisations proposées (par priorité)

1. **Mesurer sur téléphone** les profils ÉCO puis PERFORMANCE : 1er jeton, jetons/s, chaleur, batterie.
2. **TTFT** :
   - préchauffage du modèle à l'ouverture ;
   - mise en cache du préfixe système (persona) entre les tours ;
   - réduction du prompt (déjà 225 à 301 jetons d'entrée).
3. **1.7B** : choix automatique de PERFORMANCE quand la mémoire le permet. Garder le repli vers ÉCO, sans jamais relever les limites.
4. **Robustesse des tests** :
   - `tap` avec nouvelle recherche de l'élément en cas d'objet obsolète ;
   - h4 calculé sur une médiane ou une tendance.
   Ces deux changements sont soumis à ton accord, car ils touchent des tests de qualification.
5. **Répétitions** : seuil anti-répétition ou pénalité de répétition, à évaluer sur le banc de 44 scénarios.
6. **Fluidité de l'interface** : sur émulateur, le rendu V3 est plus lent que V1. Il faut mesurer sur un GPU réel avant tout changement.

## Ce qui demande ta décision

- Fusion de la PR, installation ou signature : **aucune faite**.
- Faire du 1.7B le modèle par défaut : **non proposé** tant que le protocole B n'est pas concluant.
- Modifier les tests instables h et h4.
