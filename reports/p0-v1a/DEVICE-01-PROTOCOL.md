# DEVICE-01 — Protocole de qualification physique V1-A sur POCO X8 Pro

**Statut : PRÊT, NON EXÉCUTÉ.** Aucune installation sur le téléphone sans l'accord explicite de son propriétaire, donné pour cette campagne précise. Le cloud ne peut pas mesurer le POCO : chaque valeur ci-dessous doit venir de l'appareil.

## 0. Prérequis (vérifiés avant de toucher au téléphone)

| Élément | Valeur attendue | Source |
|---|---|---|
| APK | `app-debug.apk` testOnly `fr.jarvis.v1a.lab`, SHA-256 publié par la CI V1-A au commit exact | artefact `JARVIS-V1A-LAB-APK-<sha>` + `apk-sha256.txt` |
| Modèle | `unsloth/Qwen3-0.6B-GGUF` @ `50968a4468ef4233ed78cd7c3de230dd1d61a56b`, `Qwen3-0.6B-Q4_K_M.gguf`, 396 705 472 o, SHA-256 `ac2d97712095a558e31573f62f466a3f9d93990898b0ec79d7c974c1780d524a` | `labs/v1a/model-authorization.json` |
| Outils PC | `adb` (platform-tools), câble USB, débogage USB activé temporairement | — |

## 1. Relevé initial (sans données personnelles)

```sh
adb shell getprop ro.product.model; adb shell getprop ro.build.version.release; adb shell getprop ro.build.version.sdk
adb shell cat /proc/meminfo | head -3          # MemTotal / MemAvailable
adb shell df -h /data | tail -1                  # stockage libre
adb shell dumpsys battery | grep -E 'level|temperature|status'
adb shell dumpsys thermalservice | grep -i 'status' | head -3
```

## 2. Installation (après accord uniquement)

```sh
sha256sum app-debug.apk                          # doit égaler apk-sha256.txt
adb install -r -t app-debug.apk                  # -t : APK testOnly
adb shell dumpsys package fr.jarvis.v1a.lab | grep -E 'versionName|requested permissions' -A2
```
Attendu : aucune permission demandée. Le modèle n'est **pas** dans l'APK.

## 3. Import du modèle

1. Vérifier sur le PC : `sha256sum Qwen3-0.6B-Q4_K_M.gguf` = SHA-256 attendu.
2. Copier le fichier dans `Téléchargements` du téléphone (ou `adb push … /sdcard/Download/`).
3. Dans l'app : coller le SHA-256 attendu, « Importer un modèle GGUF local », choisir le fichier.
4. Attendu : « Modèle vérifié et installé » ; un SHA erroné doit être refusé (tester une fois avec un caractère changé).

## 4. Mode avion puis conversation réelle

1. Activer le **mode avion** (Wi-Fi et données coupés) avant « Démarrer JARVIS ».
2. Chronométrer « Démarrer » → « Prêt » (= chargement A02).
3. Trois tours : « Bonjour, présente-toi en une phrase. » ; « Je m'appelle … » ; « Comment je m'appelle ? ». Pour chacun : délai jusqu'au **premier texte visible**, durée totale.
4. Pendant une longue réponse, appuyer sur **Stop** : la génération doit s'arrêter, aucune réponse ajoutée, nouvel envoi possible.

## 5. Mesures (pendant et après)

```sh
adb shell dumpsys meminfo fr.jarvis.v1a.lab | grep -E 'TOTAL PSS|TOTAL RSS'
adb shell dumpsys battery | grep -E 'level|temperature'
adb shell dumpsys thermalservice | grep -iE 'status|temperature' | head -5
```
Débit approximatif : caractères/s du tour 1 (chronométré) — ne pas convertir en jetons/s sans compteur natif.

## 6. Robustesse

Arrière-plan pendant génération puis retour ; rotation ; fermer la session (« Fermer la session et décharger ») puis redémarrer ; arrêter l'app (`adb shell am force-stop fr.jarvis.v1a.lab`) et relancer : le modèle importé reste, la session repart vide. Cas d'échec : supprimer le modèle importé → « Aucun modèle importé » ; stockage insuffisant (si reproductible sans risque).

## 7. Stabilité 20 minutes

Une question toutes les ~60 s pendant 20 min en mode avion ; relever température et batterie au début, à 10 min, à 20 min ; noter tout ralentissement, crash, ANR ou arrêt thermique.

## 8. Décision

| Décision | Condition |
|---|---|
| **GO** | Import vérifié, chargement A02, ≥ 3 tours réels, Stop fonctionnel, aucun crash/OOM, température et batterie dans les limites constructeur, mesures datées. |
| **GO-LAB-ONLY** | Fonctionne en CI/émulateur mais une mesure appareil manque ou est hors seuil non critique. |
| **NO-GO** | Crash, OOM, surchauffe, chargement hors A02, réponse non générée ou fausse. |

## 9. Retour arrière

`adb uninstall fr.jarvis.v1a.lab` supprime l'app, son modèle importé et sa session ; aucune autre donnée du téléphone n'est touchée. Désactiver le débogage USB.

## Formulaire de retour

```
Date/heure : …     Modèle/Android/SDK : …     RAM dispo / stockage libre : …
Batterie/température départ : …
APK SHA-256 vérifié : oui/non   Modèle SHA-256 vérifié : oui/non   Mode avion : oui/non
Chargement (s) : …   Tour 1 premier texte (s)/total (s) : …   Tour 2 : …   Tour 3 : …
Stop : OK/KO   PSS max (Mo) : …   Température max : …   Batterie après 20 min : …
Crash/ANR : …   Décision proposée : GO / GO-LAB-ONLY / NO-GO
```
