# Android M51 / M51-R1 / REUSE R1+ — diagnostic et réception

**État final : BLOCKED, aucune qualification Android acquise.** Les preuves et résultats M51 et M51-R1 ne sont ni supprimés ni réécrits. Les nouvelles preuves sont dans ce dossier et INTERFACE PR #21. Une compilation réussie ne qualifie pas Android.

## Reprise des anomalies antérieures

Les réceptions d'entrée M51 et le rapport INTERFACE `m51/r1/FINAL-REPORT.md` ont été relus. Au sujet M51 `9c8960a`, API29 avait 18 cas prévus, 12 commencés, 9 PASS / 3 FAIL puis crash et 6 non commencés ; API35 n'avait commencé aucun cas. Incidents non résolus : SnapshotStateObserver (ancien thread 260 / main), sélection DocumentsUI 20 s, navigation 15 s et sortie de processus API35. Sans pile/reproduction fiable, leurs causes restent UNKNOWN. Les sources Compose 1.8.0 déjà étudiées indiquent PixelCopy/callback main et runOnUiThread : déplacer aveuglément un appel bloquant sur main n'est pas une correction démontrée.

| Campagne antérieure | Source / CI | Résultat conservé et catégorie |
| --- | --- | --- |
| M51-R1 D1 Linux | 1fe0b9adc8554b0e144a9efe7f1075daeba6a192 / [42513995917](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42513995917) | API29 budget préflight dépassé, BLOCKED labo ; API35 assertion Wi-Fi immédiate sans valeur enregistrée, défaut de diagnostic/configuration, état réel UNKNOWN ; aucune application admise |
| M51-R1 Q1 Intel/HVF | d0e9219b205fbf89fd7dd346ab26aacd03a8f62d / [42515139639](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42515139639) | API29 crash SystemUI ConcurrentModificationException avant JARVIS, puis sdksetup timezone Unknown/Unknown ; causalité entre les deux non démontrée. API35 boot timeout, cause UNKNOWN ; application NOT_RUN |

C1 réutilise ces constats pour observer le Wi-Fi dans un délai borné et expliciter un fuseau valide. L'absence de l'ancien message Unknown/Unknown dans C1 ne suffit pas à conclure que les problèmes système sont résolus. Les anciens échecs restent consultables à leurs SHA et ne sont pas additionnés aux cas C1.

## Protocole reproductible et borné

1. Vérifier source et tree, run ID et première tentative, état propre, SHA des APK/test APK et certificats. Rejouer les anciens gardes sur leur source exacte ; figer les anciens tests et sources applicatives.
2. Contrôle hôte en lecture seule `emulator -version` / `-accel-check`, hash du binaire ; si pas d'accélération autorisée, BLOCKED. Aucun chmod de /dev/kvm, règle udev, root ou contournement de protection.
3. Par API : un seul boot, deux CPU, 2 048 MiB, 300 s maximum, timezone `Etc/UTC`, réseau/Wi-Fi coupé observé par lectures, pas présumé depuis une commande. Observation Wi-Fi 1→0 autorisée dans 10 s monotones ; inconnu, erreur ou zéro trop tardif refusé. Enregistrer chaque observation et capture système.
4. Préflight sans package JARVIS, budget 120 s : boot, SystemUI stable, home, événements, tombstones/crashes, dumpsys window et ANR antérieurs. Une preuve contradictoire invalide le préflight.
5. Seulement après préflight accepté : trois régressions individuelles (SAF, navigation, projet), puis suite baseline 18 / candidate 24, redémarrage et mesures. Budget instrumentation 900 s. Stop au premier problème, aucun retry automatique.
6. Archiver logs, captures, images système et hashes, source/run/tentative, état de chaque étape, incidents et cause inconnue. Ne pas attribuer au code applicatif un incident antérieur à son installation.

Campagne `REUSE-R1PLUS-C1`, source figée `7282fd769d4ab787467d08fd8059b2f1e18ca139`, tree `09091a0b2928fa976f47fb7035175c368c09aaa2`, [run 42524234101](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42524234101), tentative 1. Linux n'avait pas KVM disponible : sélection du runner standard macOS Intel, HVF disponible et vérifié sur chaque hôte. Binaire émulateur Darwin x86_64 SHA-256 `e88cef60654b095693b193a98cef7364d32ee13a43d1049fadd22c5734545db2`. Un boot/API, aucun rerun. Il s'agit d'émulation x86_64, pas de qualification ARM64 physique.

## API 35 : échec du laboratoire avant JARVIS

Le boot a terminé. Timezone `Etc/UTC`, Wi-Fi 0 observé à environ 0,340 s. Le préflight a refusé des événements `am_anr` : `com.android.phone` en échec de démarrage à 21:24:25.067, puis `com.android.systemui` à 21:24:36.948 (SystemUIService, attente 30 349 ms). Aucun package JARVIS créé, aucun test applicatif exécuté.

Catégorie **LABORATORY_FAILURE**, cause technique sous-jacente **UNKNOWN**, qualification **BLOCKED_ENVIRONMENT**. Ne pas convertir cela en crash JARVIS. Artifact `13635176855`, ZIP SHA-256 `e375ac3c53de0f4980edcb4e9da52e6e3e18aa81cc5e0d9196f23f384dbd9cc0`.

## API 29 : anomalie de préflight et assertion SAF

Le résultat brut du préflight disait PASS : 13 échantillons sur 96,769 s, SystemUI PID 2086, Wi-Fi 0 observé à environ 0,669 s, timezone exacte. **Ce PASS brut n'est pas accepté après revue.** Le fichier `environment/preflight-00-window.txt` contient déjà un `WINDOW MANAGER LAST ANR` daté de 21:24:47, splash sdksetup/FallbackHome, avant installation de JARVIS. Son SHA-256 intégral est `3a9ae56f7309d4c63c154600b43eb270c594187fb65032f591b3de95bd7b4601`.

L'ancien parseur ne détectait pas cette section datée. C'est un **défaut démontré de diagnostic de laboratoire**, corrigé dans l'option C1, sans modifier l'ancien comportement D1/Q1. Le replay du vrai extrait échoue avec l'ancien parseur et est refusé par le nouveau. `evidence/C1-api29-offline-review.json` ajoute cette revue sans modifier `C1-api29-RECEPTION.json`, preuve brute originale.

Après le préflight brut, seule la baseline et son test ont été installés. Une régression SAF a commencé, une a échoué : `Local Downloads fixture not selectable in system document picker`, ligne 62 du test généré DocumentPickerContractTest. Navigation, projet, suites 18/24, redémarrage et frames n'ont pas été exécutés ; le candidat n'a pas été testé.

Catégorie de l'assertion **UNKNOWN** : aucune preuve suffisante pour choisir entre environnement DocumentsUI, publication MediaStore/configuration ou code applicatif. La capture affiche Downloads vide, mais elle est prise après le nettoyage de la fixture par finally : **elle ne prouve pas l'absence du fichier pendant la sélection**. Le témoin `PickerWitness` existant peut enregistrer hash, IS_PENDING et fenêtre ; le collecteur Q1 réutilisé n'a pas récupéré son `picker.jsonl`. Cet état au moment exact de l'échec manque. Aucun correctif applicatif n'est justifié ; cette lacune de collecte est documentée pour la prochaine campagne, sans inventer de valeur ou changer le test pour le faire passer.

Artifact API 29 `13634613120`, ZIP SHA-256 `e096db9fc9852a9dcb8c60d9bf53a0ebfa401e9e773905aae6bc693e77f1ccc3`.

## Correctif réellement développé

Commit `d569ce816cf39191742769afef5b0711bc9a28cd`, sur la branche normale uniquement : détection d'un historique ANR daté et refus d'une section ANR non interprétable. Une section explicitement vide n'est pas faussement rejetée. Quatre tests de régression ajoutés, dont la capture réelle, **36 Python PASS** au total. Le Wi-Fi borné, l'identité source/run, les catégories d'échec et l'absence d'autorité font également l'objet de tests.

[CI après correctif 42526118449](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42526118449) : build, 36 JVM (6 historiques + 15 baseline + 15 candidate), 36 Python, lint et préservation PASS ; jobs device/probe SKIP. Le correctif est donc **vérifié en replay et sur hôte**, jamais présenté comme une réparation Android validée. La campagne C1 demeure close et sa branche demeure à 7282fd7.

## APK remis

- C1 artifact build `13634598111`, ZIP SHA-256 `bfe955d4f250ec54f63cb0bc202007d016c5e45cb625a8d1c57fafd24ae6986b`, quatre APK à source 7282fd7. Baseline : une assertion SAF FAIL ; candidat : NOT_RUN.
- Après correctif artifact `13635008299`, ZIP SHA-256 `1f4d943d66fb241b4af837f9263ffb4b8c2b8462b324b7b3f32e08263436657c`, quatre APK à source d569ce8. Android NOT_RUN, **NON QUALIFIÉS**.

APK testOnly, allowBackup false, minSdk 26/target 35, permissions limitées à la permission interne du package, UI locale uniquement. La présence d'une bibliothèque graphique arm64-v8a ne qualifie ni LLM ni protection native 16 KiB Android. Certificats debug différents selon le build : ne pas mélanger APK et APK de test entre builds. Voir les reçus exacts pour les hashes, ABI et certificats. Aucun appareil personnel touché.

## Historique préservé et prochaine expérience

M51 TCG et M51-R1 conservent leurs échecs/réceptions publiés. L'ancien récepteur UNIFIED accepte TCG/KVM et n'est pas élargi à HVF pour faire entrer un résultat C1 : ancien score/portes inchangés. Les nouveaux résultats restent séparés.

Prochaine mission Android : fournir un labo préprovisionné stable et traçable ; qualifier le système seul avant installation, examiner les ANR et la visibilité MediaStore/Downloads ; préparer une collecte en lecture seule du PickerWitness avec moment de création/nettoyage explicites. Lancer une nouvelle campagne numérotée et budgétée seulement après revue de ses prérequis. Ne pas effacer un historique ANR pour masquer l'instabilité ni relancer jusqu'à obtenir du vert.
