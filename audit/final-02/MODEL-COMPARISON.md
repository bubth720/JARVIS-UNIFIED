# FINAL-02 — Qwen3 0.6B vs 1.7B (Q4_K_M), même moteur, mêmes paramètres

**Aucune mesure ci-dessous n'a été faite sur un téléphone.** Il y a deux plateformes :

- **Linux** : runner GitHub x86-64, moteur A02 natif.
- **Émulateur** : Android 35 x86_64 avec GPU logiciel, sous un runner sans accélération matérielle comparable à celle d'un téléphone ARM.

Les latences de l'émulateur sont donc nettement pessimistes par rapport à un téléphone récent. Seul un essai sur appareil (protocole `DEVICE-RECEPTION-PROTOCOL.md`) peut trancher.

## Protocole commun

- **Modèles**, vérifiés à chaque run :
  - unsloth/Qwen3-0.6B-GGUF @ `50968a44…`, 396 705 472 octets, sha256 `ac2d9771…0d524a` ;
  - unsloth/Qwen3-1.7B-GGUF @ `d7f544ee…`, 1 107 409 472 octets, sha256 `b139949c…181897`.
  - Contrôle au chargement : taille, SHA-256 et métadonnées LFS Hugging Face ; licence apache-2.0.
- **Chargement** : un seul LLM à la fois, déchargement confirmé avant la fin de chaque run, par le chargeur scellé A02.
- **Paramètres identiques** : contexte 768, 1 thread, plafond de sortie 96. 96 est le plafond natif du 0.6B ; le 1.7B est donc aligné dessus.
- **Banc** : 44 scénarios français (`fr-bench-30` + `fr-conv-01`, JARVIS-LLM `3e2560e`), avec le correcteur publié `bench_score.py`.
- **Limites** : le délai protégé de 90 s par tour et toutes les limites natives sont **inchangés**.

## 1. Hôte Linux — [run 45899288719](https://github.com/bubth720/JARVIS-LLM/actions/runs/45899288719) (JARVIS-LLM `9eedb47`)

| Instruction | Modèle | Score /44 | 1er jeton p50/p95 (ms) | Total p50/p95 (ms) | Jetons/s | RSS (Mio) | Chargement (ms) | Natif |
|---|---|---|---|---|---|---|---|---|
| ATHENA | 0.6B | **25** | 4063 / 5591 | 4783 / 6305 | 48,6 | 567 | 2761 | 37/37 |
| ATHENA | 1.7B | **37** | 8761 / 12617 | 10958 / 15847 | 15,4 | 1886 | 9419 | 37/37 |
| PRODUCTION | 0.6B | **23** | 3479 / 5633 | 4453 / 5971 | 28,2 | 567 | 3496 | 37/37 |
| PRODUCTION | 1.7B | **33** | 2897 / 4704 | 3766 / 6737 | 23,3 | 1884 | 7596 | 37/37 |

« Natif 37/37 » couvre :

- le refus d'un fichier altéré (SHA ou taille), du budget mémoire et d'un descripteur invalide ;
- l'annulation avant chargement ;
- 100 cycles refusés ;
- 20 sessions réelles, sans fuite de descripteur ; la mémoire partagée est libérée (delta 0 Ko).

La ligne PRODUCTION du 1.7B est plus rapide que celle du 0.6B. Les jobs tournent sur des runners différents : je traite cet écart de latence comme du bruit de machine, pas comme une propriété du modèle. Les **scores**, eux, sont déterministes à configuration égale.

## 2. Application Android sur émulateur API 35 — [run 45900016272](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/45900016272) (UNIFIED `6e3dca8`)

Conditions du run : l'APK de test du monorepo, l'instruction réelle de l'application (persona ATHENA compacte + mémoire de travail), le mode avion, et `ModelStudyTest.benchOneModel` avec trois essais d'annulation.

| Config | Score /44 | 1er jeton p50/p95 (ms) | Total p50/p95 (ms) | Jetons/s | PSS chargé → après déchargement (Mio) | Chargement (ms) | Annulation : Stop → retour | Tours en échec |
|---|---|---|---|---|---|---|---|---|
| 0.6B 768/1/96 | **28** | 17150 / 26139 | 21378 / 29479 | 6,2 | 556 → 90 | 6079 | 1 ms (3/3) | **0/59** |
| 1.7B 768/1/96 | **32** | 46596 / 68449 | 59250 / 85468 | 2,4 | 1233 → 82 | 10702 | 1 ms (3/3) | **4/59** (délai protégé 90 s) |
| 1.7B 1536/2/96 (PERFORMANCE, info) | **35** | 30470 / 50122 | 38162 / 58294 | 3,8 | 1318 → 82 | 12147 | 1–2 ms (3/3) | **0/59** |

- **Thermique** : état 0 pour toutes les configurations, sur un émulateur qui ne simule pas la chauffe.
- **Nettoyage mémoire** : déchargement `CONFIRMED` dans tous les cas. Le PSS revient à environ 85 Mio, l'application seule.
- **Stabilité** : aucun plantage, un seul LLM chargé par run.

## 3. Lecture

| Critère | 0.6B (ÉCO) | 1.7B |
|---|---|---|
| Qualité | Base de référence | **+12 / +10 scénarios sur Linux** et +4 / +7 sur émulateur. Gains en factuel, raisonnement et documents absents (pas d'invention), surtout. |
| Latence | Référence | 2 à 3 fois plus lent à paramètres égaux. Sur émulateur, le 1er jeton médian passe de 17 s à 47 s. |
| Mémoire | ≈ 570 Mio en RSS | ≈ 1,9 Gio en RSS sur Linux, ≈ 1,3 Gio en PSS sur Android |
| Robustesse à 768/1 | 0 tour coupé | **4 tours coupés par le délai de 90 s** sur émulateur |
| Annulation | Immédiate | Immédiate |

## 4. Décision proposée (non appliquée)

- **Le 1.7B ne devient PAS le modèle par défaut.** Le critère de la mission n'est pas atteint : 4/59 tours dépassent le délai protégé sur émulateur, aucune mesure n'existe sur téléphone, et les fonctions vocales n'ont pas été mesurées avec le 1.7B.
- L'application reste en **ÉCO 0.6B par défaut**. Le 1.7B reste **désactivé** (`allow1p7b = false`) et la politique ne fait que rétrograder vers ÉCO.
- Le profil **PERFORMANCE (1536 / 2 threads)** est le bon candidat pour le 1.7B : meilleur score (35/44), aucun tour coupé sur émulateur.
- Ce qui reste à faire pour qualifier le 1.7B :
  1. Protocole B sur ton téléphone, avec la latence du premier jeton, la chaleur, la batterie et aucun tour coupé.
  2. Campagne de qualification complète avec le 1.7B chargé.
  3. Ta décision explicite.
