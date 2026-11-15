# JARVIS V1 Android — rapport de livraison (12/11/2026)

**Statut : APK LIVRÉE, installable, qualifiée sur émulateurs. Voix réelle au micro et au haut-parleur : À VALIDER SUR APPAREIL.**

Toutes les mesures ci-dessous viennent d'émulateurs Android x86_64 (API 29 et API 35) en mode avion, dans la CI GitHub.
**Aucune ne vient d'un téléphone.** Rien n'a été installé sur un appareil personnel. Rien n'a été fusionné dans `main`.

## 1. Livrables

| Élément | Valeur |
|---|---|
| Dépôt / branche | `bubth720/JARVIS-INTERFACE` @ `ccr-5cf17ed2-phgk00` (base : `codex/jarvis-v1-delivery`) |
| Commits de cette mission | `98803a5` (APK installable, voix isolée, nouveaux tests), `9599d99` (écran petit format, test TTS→STT) |
| Exécution CI qualifiante | run **43313299256** — **succès** (verdict : API 29 et API 35 passent tous les tests requis) |
| APK | artefact `JARVIS-V1-APK-9599d99…` → https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/43313299256/artifacts/13986519641 |
| SHA-256 de `app-debug.apk` | `a1c97119f24310969ff1e93a01acfe38008b1c4285fd6e8f7ab9a59f02acfc38` |
| Ressources (GGUF, STT, voix) | artefact `JARVIS-V1-RESSOURCES-9599d99…` (≈ 557 Mo) → https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/43313299256/artifacts/13987063535 |
| Preuves (journaux, JSON, captures) | artefact `v1-evidence-9599d99…` → https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/43313299256/artifacts/13988856409 |
| Installation | `labs/v1/INSTALL.md` (dans l'artefact APK) |

Les artefacts demandent une connexion GitHub ; APK et ressources sont conservés 90 jours, les preuves 30 jours.

APK : `fr.jarvis.v1`, nom **JARVIS**, version 1.0.0, Android 10+ (API 29), bibliothèques natives `arm64-v8a` (POCO) et `x86_64` (émulateurs).
Le binaire testé sur émulateur est **le même** que celui publié : il est installé sans `-t` par la CI.

## 2. Composition (réutilisation, aucune réécriture des modules)

| Module | Origine (épinglée) | Rôle dans la V1 |
|---|---|---|
| CORE | JAVIS-Local-v2 @ `5da9838` (SessionCoordinator, via le transport V1-B) | orchestration de la conversation, historique de session |
| LLM | JARVIS-LLM @ `2e01177`, moteur A02 scellé + llama.cpp épinglé | génération locale ; empreinte revérifiée à chaque chargement |
| INTERFACE | cockpit M55-D (sphère 3D + avatar 2.5D), client CORE de l'INTERFACE | écran, avatar, états |
| VOICE | JARVIS-VOICE @ `92d0745`, `pocketRuntime` compilé sans modification, `PcmPlayer` | synthèse Pocket TTS, voix publique « alba » |
| STT | whisper.cpp v1.8.4 compilé depuis ses sources, `ggml-base-q5_1.bin` | reconnaissance vocale française |
| NEXUS, SERVICES | non intégrés | pas prêts pour une intégration Android sans retarder la V1 |
| EVOLUTION | **désactivé** (absent de l'APK) | fonctionnement autonome non qualifié |

Les 11 fichiers réutilisés sont vérifiés octet par octet (`check_reuse.py`). La garde de périmètre vérifie que
l'application historique et les labos M50, V1-A, V1-B et M55-D (391 fichiers) restent inchangés.

**Modèle GGUF conservé :** `unsloth/Qwen3-0.6B-GGUF` @ `50968a44…`, `Qwen3-0.6B-Q4_K_M.gguf`, 396 705 472 octets,
SHA-256 `ac2d9771…0d524a`, apache-2.0. Provenance vérifiée par la CI (révision exacte, taille et empreinte), puis dans l'application
(trace A02 : `copiedSha256 = sealedSha256 =` empreinte épinglée, 15 scellés, chargement via fd scellé en lecture seule).

## 3. Changements de cette mission

1. **APK installable par simple appui.** `testOnly` est retiré. La seule permission reste le micro, et il n'y a toujours pas d'Internet (`aapt` + test a).
2. **Voix isolée.** Seul le GGUF est obligatoire. Si la reconnaissance vocale ou la voix Pocket manque ou échoue, seule cette fonction est désactivée,
   avec un message clair ; la réponse réelle s'affiche alors en texte. Aucune réponse simulée.
3. **Écran utilisable sur petit écran.** La hauteur du cockpit est proportionnelle à l'écran, la dernière réponse est toujours visible sous le statut,
   et le clavier se ferme à l'envoi. Défaut constaté sur l'émulateur 320×640 (run 43308927350), puis corrigé.
4. **Nouveaux tests instrumentés**, chacun dans un nouveau processus (donc redémarrage à froid) : conversation texte de 3 messages avec contexte,
   écran réel piloté par entrées système, aller-retour TTS→STT, mode texte seul, réouverture après arrêt forcé, absence de crash.
5. **CI.** API 29 et API 35 sont toujours exécutées et jugées. APK et ressources sont publiées dès la fin du build.

## 4. Résultats (run 43313299256, mode avion, émulateurs)

| Test | API 29 | API 35 |
|---|---|---|
| a — 1 seule permission (micro), pas d'Internet, APK non testOnly | PASS | PASS |
| b — parcours vocal complet (WAV → STT → CORE → LLM → TTS), 2 échanges, interruption, libération | PASS* | PASS* |
| c — capture micro Android réelle (AudioRecord) | PASS (silence, RMS 8e-5) | PASS (silence, RMS 1,2e-4) |
| d — redémarrage à froid sans réimport + 3 messages avec contexte | PASS | PASS |
| f — écran réel : Démarrer → saisir → Envoyer → réponse générée affichée | PASS | PASS |
| h — Pocket synthétise une vraie parole, whisper la retranscrit | PASS | PASS |
| g — sans fichiers voix : démarrage et réponses écrites, micro refusé proprement | PASS | PASS |
| Réouverture après arrêt forcé / aucun crash | PASS / PASS | PASS / PASS |

\* La sortie haut-parleur de l'émulateur ne consomme jamais l'AudioTrack (message exact « Délai de lecture audio dépassé »,
avec et sans `-noaudio`). Ce seul cas est toléré et consigné ; toute autre erreur de STT, de LLM ou de TTS fait échouer le test.

### Réponses réellement générées (extraits des rapports JSON)

| Question (texte) | Réponse locale (API 29 et 35, identiques) |
|---|---|
| « Bonjour, je m'appelle Thomas. » | « Vous vous appelez Thomas. » |
| « Comment je m'appelle ? » (2e message) | « Vous vous appelez Thomas. » → **contexte conservé** |
| « Quelle est la capitale de la France ? » | « La capitale de la France est Paris. » |

### Mesures (émulateur, CPU x86_64 virtualisé ; non représentatif du POCO)

| Mesure | API 29 | API 35 |
|---|---|---|
| Chargement de la session (LLM + STT + TTS) | 3,6–7,9 s | 3,6–5,8 s |
| Réponse LLM complète (texte) | 13,7–18,1 s | 13,2–17,2 s |
| Pocket : 3,04 s d'audio, 1er PCM / total | 449 ms / 1,73 s | 696 ms / 1,86 s |
| Aller-retour TTS→STT | « Bonjour, je suis Jarvis, votre assistant local. » (exact) | idem |
| STT sur phrase espeak (voix robotique) | « Pouf, je m'appelte au ma... » (8,4–9,3 s) | idem (8,2–8,5 s) |
| Interruption pendant la parole → prêt | 254 ms | 504 ms |
| RSS chargé / pic (VmHWM) | 972 Mio / 1,47 Gio | 973 Mio / 1,46 Gio |
| Libération confirmée (LLM déchargé + détruit) | oui, 105 ms | oui, 152 ms |

## 5. Fonctionnalités : opérationnelles, non qualifiées, problèmes connus

**Opérationnelles (qualifiées sur émulateurs) :** ouverture, interface et avatar ; question écrite → réponse générée localement ;
contexte sur plusieurs messages ; fermeture/réouverture et redémarrage à froid sans réimport ; mode avion, sans Internet ni serveur ;
import vérifié des ressources (refus des fichiers non conformes) ; synthèse Pocket réelle ; reconnaissance whisper réelle ; interruption ; libération mémoire.

**À VALIDER SUR APPAREIL (POCO) :**
- micro réel avec une voix humaine (l'émulateur ne fournit que du silence) ;
- son réel au haut-parleur et aux écouteurs (l'émulateur ne consomme pas l'AudioTrack) ;
- latences et température sur le CPU ARM réel ; fluidité de la sphère sur GPU réel ;
- installation par appui sur MIUI/HyperOS et demande d'autorisation micro.

**Problèmes connus :**
1. **Qualité du 0.6B** : banc M55-B à 13/30. Les réponses simples sont correctes, mais le modèle reste limité (erreurs factuelles, refus excessifs).
   Les réponses sont plafonnées à 96 jetons par la politique protégée A02 : une réponse longue peut se terminer par « ... ».
   Le 1.7B (21/30) n'est pas qualifié sur Android.
2. **STT sur voix synthétique espeak** : transcription mauvaise, ce qui dégrade la réponse vocale dans le test b. La parole Pocket est
   retranscrite à l'identique, mais la qualité sur une voix humaine reste à mesurer au POCO.
3. **Latence** : 13–18 s par réponse sur émulateur. À mesurer sur le POCO (2 threads, CPU ARM natif).
4. **Signature de débogage CI**, différente à chaque build : pour une mise à jour, il faut désinstaller puis réimporter.
   L'APK est `debuggable` (accès `run-as` uniquement via un câble USB et le débogage USB activé).
5. **L'historique n'est pas conservé** après « Fermer » ou un redémarrage : le contexte vaut pour une session. Les ressources importées, elles, sont conservées.
6. Risques de sécurité A04 à A09 du rapport M55 (bail/broker, transitions terminales, chemins dans les erreurs, réservation mémoire globale) : **toujours ouverts**, sans régression introduite.
7. Profil vocal privé « B » non intégré : il reste en import local par le propriétaire. Seule la voix publique « alba » est livrée.

## 6. Historique CI de la branche V1

| Run | Commit | Résultat |
|---|---|---|
| 43294823223 → 43301708504 (×5) | `5c4d3ec`…`de59e2b` | échec : compilation puis lecture audio émulateur (session précédente) |
| 43308927350 | `98803a5` | APK publiée ; échec du verdict : écran API 29 (petit écran), haut-parleur émulateur |
| **43313299256** | **`9599d99`** | **succès** |

## 7. Prochaine étape

Essai physique DEVICE-01 sur le POCO (`DEVICE-01-V1-VOCAL.md`), puis retour des résultats pour corriger les défauts éventuels.
