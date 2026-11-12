# DEVICE-01 (V1 vocale) — essai sur POCO X8 Pro

**Statut : PRÊT, NON EXÉCUTÉ.** Rien n'est installé sans ta validation explicite. Cet essai est le seul qui prouve la **voix réelle au microphone** et le **son réel au haut-parleur**. Le cloud ne peut pas le faire : un émulateur de CI ne reçoit que du silence au micro.

## 0. Matériel et fichiers

- PC avec `adb`, câble USB, débogage USB activé temporairement.
- APK `fr.jarvis.v1` de l'artefact `JARVIS-V1-APK-<commit>` : vérifier `sha256sum app-debug.apk` contre le SHA-256 publié dans `reports/v1-delivery/RAPPORT.md`.
- Trois ressources, à vérifier avec `sha256sum` (voir `labs/v1/resources.json` / `INSTALL.md`) :
  - `Qwen3-0.6B-Q4_K_M.gguf`
  - `ggml-base-q5_1.bin`
  - `pocket-fr-6l-alba.zip`

## 1. Installation

```sh
adb install -t app-debug.apk
adb shell mkdir -p /sdcard/Android/data/fr.jarvis.v1/files/import
adb push Qwen3-0.6B-Q4_K_M.gguf ggml-base-q5_1.bin pocket-fr-6l-alba.zip /sdcard/Android/data/fr.jarvis.v1/files/import/
```

Dans l'application : « Rechercher » (les trois lignes passent à ✓), puis activer le **mode avion**, puis « Démarrer JARVIS ».

## 2. Parcours à vérifier (chronométrer et noter)

1. « 🎤 Parler », autoriser le micro, dire **« Bonjour, je m'appelle Thomas. »**. Attendu :
   - transcription correcte affichée ;
   - réponse générée ;
   - **réponse entendue au haut-parleur**.
2. « 🎤 Parler », dire **« Comment je m'appelle ? »**. Attendu : réponse entendue ; noter si elle contient « Thomas ».
3. Poser une question longue (« Raconte-moi une histoire de dragon »), puis toucher **« Interrompre »** pendant que JARVIS parle. Attendu : la voix s'arrête en moins de 0,5 s environ et une nouvelle question est possible.
4. Toucher « Parler » pendant que JARVIS parle (barge-in). Attendu : la voix s'arrête et l'écoute démarre.
5. Retirer puis remettre l'autorisation micro (Paramètres). Attendu : un message clair, et la saisie au clavier reste possible.
6. Écouteurs filaires ou Bluetooth : répéter l'étape 1.
7. Dix échanges de suite, puis « Fermer » : aucun crash, application fluide.

## 3. Mesures

```sh
adb shell dumpsys meminfo fr.jarvis.v1 | grep -E 'TOTAL PSS|TOTAL RSS'
adb shell dumpsys battery | grep -E 'level|temperature'
adb shell dumpsys thermalservice | grep -iE 'status|temperature' | head -5
```

L'application affiche, sous chaque échange, la durée de la reconnaissance (STT), celle du LLM (et du 1er texte) et la durée de la voix.

À noter :
- la latence ressentie entre la fin de la parole et le début de la réponse audible ;
- la température et la batterie au début et après 20 minutes.

## 4. Désinstallation

```sh
adb uninstall fr.jarvis.v1
adb shell rm -rf /sdcard/Android/data/fr.jarvis.v1
```

Désactiver le débogage USB.

## Formulaire de retour

```
Date : …  Android / modèle : …  APK SHA vérifié : oui/non  Ressources vérifiées (3/3) : oui/non  Mode avion : oui/non
Démarrage (s) : …
Échange 1 : transcription « … » / réponse entendue : oui/non / délai fin de parole → voix (s) : …
Échange 2 : transcription « … » / réponse « … » / entendue : oui/non
Interruption : OK/KO (délai …)   Barge-in : OK/KO   Micro refusé : message OK/KO   Écouteurs : OK/KO
10 échanges : crash oui/non   PSS max (Mo) : …   Température max : …   Batterie après 20 min : …
Décision proposée : GO / GO avec réserves / NO-GO
```
