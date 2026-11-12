# Mission V1-B — dialogue, plafond de réponse et mesures Android (12/11/2026)

**Décision : NO-GO sur le critère final, GO-LAB-ONLY pour la mécanique.** Le dialogue multi-tour est réparé :
- JARVIS répond « Vous vous appelez Thomas. » ;
- il ne se présente plus comme Thomas ;
- il prend en compte une correction de prénom.

Mais la porte de qualité stricte passe **3 scénarios sur 4** sur API 29 et API 35. Une capitale reste fausse (« Italie : Lione / Lucca »), ce qui est une erreur de connaissance du modèle 0.6B. Tous les tests de sécurité, de flux, de Stop, de déchargement et de rechargement sont **PASS**. Le téléphone n'a pas été testé (**NOT_RUN**).

## Branches et commits (aucune fusion dans `main`, aucune installation sur un appareil)

Toutes les branches sont `codex/jarvis-v1b-conversation-performance`.

| Dépôt | Départ | Commit final | Contenu |
|---|---|---|---|
| bubth720/JARVIS-LLM | `c00035b` | `2e011776d9e0f675bcae49b739f12a3a6dbf4de4` | A02 : `generateStreamTurns`, `countTurnsTokens`, `setOutputCeiling` + `a02_output_policy.h` ; banc de dialogue, étude de consigne, `dialogue_gate.py` |
| bubth720/JARVIS-INTERFACE | `4ed3f99` | `d592505` (APK construite sur `340ce8ae451ea1f70f74fa1ab0e89a2813d30379`, puis correctif de CI seul) | labo indépendant `labs/v1b` + workflow `v1b-lab.yml` ; `labs/v1a` inchangé |
| bubth720/JARVIS-UNIFIED | `c913673` | ce rapport + `DEVICE-01-V1B-PROTOCOL.md` | rapports |

Ni VOICE, ni NEXUS, ni SERVICES, ni EVOLUTION, ni aucun autre projet n'a été modifié. Le modèle est inchangé : `unsloth/Qwen3-0.6B-GGUF` @ `50968a4…`, SHA-256 `ac2d9771…524a`.

## Sécurité conservée (PASS)

| Élément | Preuve |
|---|---|
| `bridge.cpp` et `native_configuration.h` protégés : **non modifiés** (`git diff c00035b` vide) ; gardes de préservation 003e, 003f, f3a, f3b | A02 run 43186877283 |
| Garde V1-B, qui exécute la garde V1-A sur `4ed3f99`, laquelle exécute la garde M50 sur `b9a6c19` : 347 fichiers figés | V1-B run 43186945601 |
| memfd scellé avec 4 sceaux (`seals: 15`), SHA-256 copié = scellé = attendu, ouvertures servies depuis le fd scellé (3), 1 projection privée en lecture seule, inode source jamais projeté, chargeur par chemin non exporté | les deux runs, API 29 et API 35 |
| Refus : SHA faux, taille fausse, budget mémoire, fd invalide, GGUF malformé, 100 cycles refusés sans fuite de fd | Linux + bac à sable Android |
| Nouveaux refus V1-B : plafond 0 ou 257, 129 jetons sous un plafond de 128, 128 jetons avant activation (le plafond protégé de 96 est rétabli à chaque chargement), assistant en premier, injection `<\|im_start\|>`, 9 entrées, contexte dépassé sans sortie | A02 run 43186877283 |
| APK : testOnly, aucune permission, aucun modèle embarqué, alignement 16 Kio, nouveaux symboles présents | `verify_apk.py` |
| Contexte 768 et thread unique : inchangés ; aucun thread ajouté | trace + configuration |

## Corrections du dialogue

1. **Format** : V1-A aplatissait l'historique dans **un seul** message `user` (`UTILISATEUR: … ASSISTANT: …`), si bien que les réponses précédentes ressemblaient à du texte utilisateur. V1-B envoie les vrais rôles ChatML `system`, `user` et `assistant` (`generateStreamTurns`, via le `generate()` protégé). Les fins de tour sont gérées par le gabarit officiel du GGUF et l'arrêt sur jeton de fin.
2. **Troncature** : la fenêtre est choisie par **comptage exact des jetons** (`countTurnsTokens`), en partant des échanges les plus récents, avec 3 échanges au plus (limite protégée de 8 entrées). Le budget CORE (`validateInference`) s'applique toujours, sans modification, à la requête courante. Une question trop longue donne un refus visible, n'est pas enregistrée, et la session reste utilisable (PASS sur API 29 et API 35).
3. **Consigne** : l'étude a porté sur 4 tours, 13 consignes et 4 scénarios, avec le modèle réel et une porte stricte.
   - Aucune consigne unique ne dépasse 2/4.
   - Un gabarit cité (« <prénom> ») est recopié tel quel par le modèle.
   - **Le routage par intention** (consigne « prénom » ou consigne générale) **et la mémoire de session** (le dernier prénom déclaré, transmis comme fait connu) atteignent 3/4.
   - Les réponses restent intégralement générées par le modèle.

## Dialogue réel, mode avion (API 29 = API 35, réponses identiques)

| Scénario | Réponses de JARVIS V1-B | Porte |
|---|---|---|
| « Bonjour, présente-toi. » / « Je m'appelle Thomas. » / « Comment je m'appelle ? » | « Bonjour ! Je suis JARVIS. Je suis un assistant local. Je ne peux pas exécuter aucune action. » / « Vous vous appelez Thomas. » / « **Vous vous appelez Thomas.** » | **PASS** |
| « Je m'appelle Thomas. » / « En fait non, je m'appelle Julien. » / « Comment je m'appelle ? » | « Vous vous appelez Thomas. » / « Vous vous appelez Julien. » / « **Vous vous appelez Julien.** » | **PASS** |
| Capitales : France / Italie / Espagne | « … Paris. » / « … l'Italie est **Lione**. » / « … Madrid. » | **FAIL** (connaissance) |
| « Je m'appelle Thomas. » / « Donne-moi une idée de dessert simple. » / « Au fait, comment je m'appelle ? » | « Vous vous appelez Thomas. » / « Un plat simple comme un cake ou un fruit. » / « **Vous vous appelez Thomas.** » | **PASS** |

Avant (V1-A, puis la consigne V1-B initiale) : 0/4, avec « Je suis Thomas », « Je m'appelle Julien » et « Je ne sais pas la capitale de la France ».

## Tableau 48 / 128 / 256 (même configuration : contexte 768, 1 thread)

Question : « Explique en détail comment fonctionne la photosynthèse. » ; prompt de 134 jetons.

| Plafond | Jetons générés | Fin naturelle | 1er jeton API 29 / 35 | Total API 29 / 35 | Jetons/s API 29 / 35 | VmHWM API 29 / 35 |
|---|---|---|---|---|---|---|
| 48 | 41 | oui | 11,8 / 11,5 s | 17,6 / 16,8 s | 7,0 / 7,5 | 650 / 676 Mio |
| 128 | 41 | oui | 11,6 / 11,5 s | 17,4 / 16,8 s | 7,0 / 7,6 | 650 / 676 Mio |
| 256 (expérimental, moteur rechargé) | 41 | oui | 11,9 / 11,4 s | 17,7 / 16,7 s | 6,9 / 7,6 | 768 / 677 Mio |

Le plafond n'est **jamais atteint** : le moteur protégé impose « réponds brièvement », et le modèle s'arrête seul vers 30 à 40 jetons. Le plafond n'impose donc aucune longueur artificielle. Le relèvement du VmHWM à 768 Mio sur API 29 coïncide avec le second chargement (pic transitoire de la copie scellée, page-cache inclus) ; ce n'est pas un effet de 256. Sur le banc Linux, les plafonds 48, 128 et 256 donnent eux aussi des résultats identiques (25 jetons).

## Mesures Android (émulateur x86_64, **pas un téléphone**)

| Mesure | API 29 | API 35 |
|---|---|---|
| Import + vérification SHA-256 | 2,7 s | 4,7 s |
| Chargement scellé A02 | 15,0 s | 10,0 s |
| 1er jeton (dialogue, prompt de 127 à 224 jetons) | 11,5 à 21,2 s | 11,1 à 20,4 s |
| Décodage | 5,3 à 7,1 jetons/s | 5,9 à 7,6 jetons/s |
| Réponse totale (dialogue) | 12,7 à 23,2 s | 12,3 à 21,2 s |
| RSS avant chargement / chargé / VmHWM final | 146 / 644 / 768 Mio | 176 / 673 / 677 Mio |
| Stop en pleine génération : drainage | 4 ms | 5 ms |
| Déchargement : shmem scellée | 373 Mio → 0,6 Mio | 387 Mio → 15,6 Mio (= niveau avant chargement) |
| 5 rechargements (charger, répondre, détruire) | 4,2 à 4,3 s chacun ; shmem 0,6 Mio ; 66 fd stables | 4,2 s ; 15,7 Mio ; 116 fd stables |

**Cause de la latence initiale** (mesurée, non contournée) : le 1er jeton croît d'environ 75 ms par jeton de prompt. Le pré-remplissage s'exécute sur **un seul thread** avec des micro-lots protégés de 8 jetons (`native_configuration.h`), et l'historique est re-pré-rempli à chaque tour (le `generate()` protégé vide le cache KV). Les leviers possibles, à savoir plus de threads, des lots plus grands ou la réutilisation du cache KV entre les tours, modifient tous la politique protégée et **exigent ton autorisation**. Aucune réponse en moins de 3 s n'est mesurée ni promise : le meilleur 1er jeton mesuré est de 10,6 s sur émulateur, et de 3,0 s sur l'hôte Linux.

## Régressions et limites

- **Latence** : la consigne routée et la mémoire allongent le prompt d'environ 20 à 50 jetons. Le 1er jeton maximal passe de 16,9 s à 21,2 s (API 29) par rapport à la consigne V1-B initiale.
- **Budget CORE en octets, inchangé** : une question générale est limitée à 299 octets avec 128 (171 avec 256). Un message sur le prénom est limité à environ 175 octets avec 128, et à environ 47 avec 256. Au-delà, le refus est visible.
- **Qualité** : capitales et connaissances fragiles (« Lione », « Lucca », « Londres ») ; refus fréquents sur les explications, comme pour la photosynthèse, car la consigne protégée demande d'« admettre ses incertitudes » ; tournures maladroites (« Vouvez-vous »). Ces défauts ne sont **pas corrigeables** sans changer de modèle ou toucher à la politique protégée (consigne fixe, échantillonnage glouton).
- **CI** : la porte de dialogue du run 43186945601 s'est arrêtée après API 29. API 35 a été jugé ensuite sur le rapport produit par la même CI, avec le même script : 3/4, identique à API 29. La boucle est corrigée (`d592505`).

## APK V1-B testOnly

- **Artefact** : `JARVIS-V1B-LAB-APK-340ce8ae451ea1f70f74fa1ab0e89a2813d30379` (ID 13929544036, expire le 12/12/2026) — https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/43186945601
- **SHA-256 de `app-debug.apk`** : `78a0ce7f8033c5ad62327a75d7bf0cdec1a568975624423bb58074e11d97eb51`
- `fr.jarvis.v1b.lab`, testOnly (`adb install -t`), minSdk 29, arm64-v8a + x86_64. Le modèle n'est pas embarqué : il s'importe avec son SHA-256.

## Ledger

| Test | API 29 | API 35 | Linux |
|---|---|---|---|
| Sécurité A02, bac à sable, refus | PASS | PASS | PASS |
| Chargement réel, flux, Stop, erreur visible, déchargement | PASS | PASS | PASS |
| 5 rechargements sans fuite | PASS | PASS | PASS (10 cycles) |
| 48 / 128 / 256, plafonds et refus | PASS | PASS | PASS |
| Dialogue « Thomas » (identité) | PASS | PASS | PASS |
| Dialogue : 4 scénarios stricts | **FAIL 3/4** | **FAIL 3/4** | **FAIL 3/4** |
| POCO (DEVICE-01) | NOT_RUN | — | — |

## Prochaine action recommandée

Une décision t'appartient, et une seule suffit pour avancer :
1. **Autoriser Qwen3-1.7B Q4_K_M**, que le moteur protégé admet déjà : contexte ≥ 768, 1 à 4 threads, sortie ≤ 256. C'est le levier le plus probable pour les connaissances et la cohérence, au prix d'environ 1,1 Gio de mémoire et d'une latence plus forte. Il faut ensuite le qualifier sur le même banc.
2. Ou **autoriser une évolution de la politique protégée pour le 0.6B** : réutilisation du cache KV entre les tours (latence), 2 threads ou des lots plus grands (pré-remplissage), et/ou une consigne fixe moins restrictive. Chaque changement serait testé de façon comparative.
3. Ensuite seulement, DEVICE-01 sur le POCO, selon `DEVICE-01-V1B-PROTOCOL.md`, après une nouvelle validation explicite.
