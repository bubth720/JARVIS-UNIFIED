# Mesures réelles et portée

Une optimisation documentaire a été mesurée dans le laboratoire NEXUS ; aucune mesure Android/LLM/voix/batterie n'est disponible pour justifier un remplacement. Les choix CONSERVER de la matrice tiennent compte de cette absence.

Source NEXUS `b7d9d884ddd034e3580a2268fce69ca43030e8c5`, [run 42523712059](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42523712059), JVM sur runner Linux, 4 processeurs visibles. SQLite FTS5 et citations réelles, corpus M53 CC0 de trois documents fictifs, bases temporaires. Dix appels d'échauffement puis 60 échantillons alternés par variante. Charge utile identique exigée ; aucune assertion de seuil temporel utilisée pour forcer un gain.

Référence : consommateur **de test M53** qui résout une seconde fois les citations publiques déjà validées par DocumentaryGateway dans son snapshot SQLite. Ce n'est pas une baseline productive ni une optimisation appliquée à un runtime. Candidat : adaptateur test-only consommant le bundle validé ; toutes les vérifications internes du Gateway demeurent.

| Mesure | Référence | Candidat |
| --- | ---: | ---: |
| Latence médiane | 1 059 042 ns | 934 671 ns |
| Latence p95 | 1 198 021 ns | 1 078 007 ns |
| CPU médian du thread courant | 1 062 802 ns | 938 290 ns |

La réduction p95 est d'environ 10,0 % **dans cet essai unique**. Voir `evidence/nexus-benchmark.json` pour toutes les valeurs brutes, minima/maxima et environnement. Variance inter-runs et intervalles de confiance non étudiés : aucun gain garanti sur appareil ou corpus réel.

Heap utilisée avant/après l'ensemble du JVM de test : 107 146 528 → 145 943 840 octets. Ces valeurs englobent le JVM et ne mesurent pas les allocations ou la rétention propres à l'adaptateur. **Aucun gain mémoire n'en est déduit.** Pas de mesure batterie, RSS Android, chauffe, génération LLM, tokens/s, délai TTS, frames ou stabilité en usage long. Aucune réutilisation de session native/modèle/autorisation n'a été introduite pour gagner artificiellement du temps.

La prochaine baseline pertinente dépend des portes Android/LLM : modèle et profil autorisés inchangés, corpus fixe, source/poids/hardware identifiés, latences médiane/p95, CPU, RSS/PSS, allocations, interruptions/drain/unload et dégradation thermique consignés. Toute optimisation devra être réversible et comparée sur ces mêmes entrées ; pas de promotion si la stabilité régresse.

Les rapports **historiques M50-S1B du 4 novembre**, récupérés et re-hashés, donnent aussi : démarrage à froid 1 715 ms / PSS du processus en état UNKNOWN synthétique 36 129 KiB (API29), 2 298 ms / 40 377 KiB (API35). Ce sont des observations uniques du petit laboratoire synthétique CORE/UI, sans génération native ni comparaison avant/après. Elles ne sont pas une nouvelle baseline du produit M51 ou d'un appareil physique.
