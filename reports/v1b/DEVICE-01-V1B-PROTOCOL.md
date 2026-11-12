# DEVICE-01 (V1-B) — protocole de qualification physique sur POCO X8 Pro

**Statut : PRÊT, NON EXÉCUTÉ.** Rien n'est installé sur le téléphone sans une nouvelle validation explicite de son propriétaire pour cette campagne. Le cloud ne mesure pas le POCO : chaque valeur doit venir de l'appareil. Ce protocole remplace, pour V1-B, celui de V1-A (`reports/p0-v1a/DEVICE-01-PROTOCOL.md`, conservé).

## 0. Éléments vérifiés avant de toucher au téléphone

| Élément | Valeur attendue | Vérification |
|---|---|---|
| APK | `app-debug.apk`, paquet `fr.jarvis.v1b.lab`, testOnly, aucune permission | SHA-256 indiqué dans `reports/v1b/REPORT.md` (artefact `JARVIS-V1B-LAB-APK-<commit>`) : `sha256sum app-debug.apk` doit lui être **identique** |
| Modèle | `unsloth/Qwen3-0.6B-GGUF` @ `50968a4468ef4233ed78cd7c3de230dd1d61a56b`, `Qwen3-0.6B-Q4_K_M.gguf`, 396 705 472 octets | `sha256sum` = `ac2d97712095a558e31573f62f466a3f9d93990898b0ec79d7c974c1780d524a`, taille exacte (`stat -c %s`) |
| Outils PC | `adb` (platform-tools), câble USB, débogage USB activé **temporairement** | `adb devices` liste un seul appareil |

## 1. Relevé initial (aucune donnée personnelle)

```sh
adb shell getprop ro.product.model; adb shell getprop ro.build.version.release; adb shell getprop ro.build.version.sdk
adb shell cat /proc/meminfo | head -3
adb shell df -h /data | tail -1
adb shell dumpsys battery | grep -E 'level|temperature|status'
adb shell dumpsys thermalservice | grep -iE 'status|temperature' | head -5
```

## 2. Installation explicite (après validation uniquement)

```sh
sha256sum app-debug.apk                                  # = SHA-256 du rapport V1-B
adb install -t app-debug.apk                             # -t obligatoire : APK testOnly
adb shell dumpsys package fr.jarvis.v1b.lab | grep -E 'versionName|requested permissions' -A2
```
Attendu : aucune permission. Le modèle n'est pas dans l'APK.

## 3. Import du modèle

1. Sur le PC : `sha256sum Qwen3-0.6B-Q4_K_M.gguf` = empreinte attendue.
2. `adb push Qwen3-0.6B-Q4_K_M.gguf /sdcard/Download/`.
3. Dans l'app : coller l'empreinte, « Importer un modèle GGUF local », choisir le fichier.
4. Contrôle négatif : une empreinte avec un caractère modifié doit être refusée (« Empreinte différente »).

## 4. Conversation en mode avion (plafond 128 par défaut)

1. Activer le **mode avion** avant « Démarrer JARVIS » ; chronométrer « Démarrer » → « Prêt ».
2. Scénarios (nouvelle session pour chacun : « Fermer la session », puis « Démarrer ») :
   - « Bonjour, présente-toi. » / « Je m'appelle Thomas. » / « Comment je m'appelle ? » → doit répondre **Thomas**, sans se présenter comme Thomas ;
   - « Je m'appelle Thomas. » / « En fait non, je m'appelle Julien. » / « Comment je m'appelle ? » → **Julien** ;
   - « Quelle est la capitale de la France ? » / « Et celle de l'Italie ? » / « Et celle de l'Espagne ? » ;
   - « Je m'appelle Thomas. » / « Donne-moi une idée de dessert simple. » / « Au fait, comment je m'appelle ? ».
3. Pour chaque tour, recopier la ligne de mesures affichée par l'app (« Dernier tour : jetons, 1er jeton, jetons/s, total, échanges de contexte »).
4. **Stop** pendant « Compte lentement de un à cinquante, en toutes lettres. » : arrêt, aucune réponse ajoutée, nouvel envoi possible.
5. Option expérimentale 256 : fermer la session, cocher « Expérimental : plafond 256 jetons », démarrer, poser « Explique en détail comment fonctionne la photosynthèse. », puis la même question en 128.

## 5. Mesures pendant et après

```sh
adb shell dumpsys meminfo fr.jarvis.v1b.lab | grep -E 'TOTAL PSS|TOTAL RSS'
adb shell dumpsys battery | grep -E 'level|temperature'
adb shell dumpsys thermalservice | grep -iE 'status|temperature' | head -5
```
Relever : chargement (s), 1er jeton (ms), jetons/s, total (ms), PSS max (Mo), température max (°C), batterie avant/après (%).

## 6. Robustesse et rechargement

Arrière-plan pendant une génération puis retour ; rotation ; « Fermer la session et décharger » puis « Démarrer » (rechargement) cinq fois en relevant le PSS après chaque fermeture ; `adb shell am force-stop fr.jarvis.v1b.lab` puis relance (le modèle importé reste, la session repart vide).

## 7. Stabilité 20 minutes

Une question toutes les 60 s environ pendant 20 min en mode avion ; température et batterie à 0, 10 et 20 min ; noter ralentissement, crash, ANR ou bridage thermique. Ne jamais contourner une protection thermique.

## 8. Désinstallation et nettoyage

```sh
adb uninstall fr.jarvis.v1b.lab                          # supprime l'app, le modèle importé et la session
adb shell rm -f /sdcard/Download/Qwen3-0.6B-Q4_K_M.gguf  # copie de transfert
adb shell pm list packages | grep fr.jarvis               # ne doit plus lister fr.jarvis.v1b.lab
```
Désactiver le débogage USB et le mode avion. Aucune autre donnée du téléphone n'est touchée.

## 9. Décision

| Décision | Condition |
|---|---|
| **GO** | Empreintes vérifiées, chargement A02, 4 scénarios cohérents (prénom correct, aucune confusion d'identité), Stop fonctionnel, 5 rechargements sans hausse durable du PSS, aucun crash/ANR/OOM, température et batterie dans les limites constructeur. |
| **GO-LAB-ONLY** | Fonctionne mais une mesure manque ou est hors seuil non critique. |
| **NO-GO** | Crash, OOM, surchauffe, chargement hors A02, réponse incohérente sur le prénom. |

## Formulaire de retour

```
Date/heure : …     Modèle/Android/SDK : …     RAM dispo / stockage libre : …
Batterie/température départ : …
APK SHA-256 vérifié : oui/non   Modèle SHA-256 vérifié : oui/non   Mode avion : oui/non
Chargement (s) : …
Scénario prénom : réponses … / mesures …
Scénario correction : …   Questions successives : …   Changement de sujet : …
Stop : OK/KO   128 vs 256 : jetons / 1er jeton / jetons/s / total : …
PSS max (Mo) : …   PSS après 5 rechargements : …   Température max : …   Batterie après 20 min : …
Crash/ANR : …   Désinstallation faite : oui/non   Décision proposée : GO / GO-LAB-ONLY / NO-GO
```
