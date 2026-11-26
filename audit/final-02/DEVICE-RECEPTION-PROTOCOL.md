# FINAL-02 — Protocole de réception sur téléphone Android (à faire par toi)

Rien n'est installé à distance ; je ne signe rien. Durée : environ 1 h. Téléphone chargé, à température ambiante, **mode avion**.

## Préparation

1. Télécharge l'artefact `next01-apk-candidate-<SHA>` du run CI indiqué dans `TEST-REPORT.md`, puis vérifie le SHA-256 de `app-release-unsigned.apk`.
2. Signe-le **toi-même** avec ta clé (`apksigner sign --ks ta-cle.jks app-release-unsigned.apk`). Je ne signe jamais à ta place.
3. Prépare les fichiers de modèles et vérifie leur SHA-256 :
   - `Qwen3-0.6B-Q4_K_M.gguf` — ÉCO, par défaut. 396 705 472 octets, `ac2d9771…0d524a`.
   - `Qwen3-1.7B-Q4_K_M.gguf` — optionnel, étude. 1 107 409 472 octets, `b139949c…181897`.
   - Les modèles de voix (STT, TTS) indiqués dans `TEST-REPORT.md`.
4. Note le modèle du téléphone, sa RAM et la version d'Android.

## Partie A — mode ÉCO, 0.6B (référence qualifiée sur émulateur)

| # | Geste | Résultat attendu | OK / NON, mesure |
|---|---|---|---|
| A1 | Installer, ouvrir | Une seule permission demandée (micro) ; aucune connexion | |
| A2 | Importer le 0.6B et les modèles de voix | Empreintes vérifiées ; refus clair pour un fichier modifié | |
| A3 | « Bonjour, je m'appelle … », puis « Comment je m'appelle ? » | Le prénom est retrouvé | |
| A4 | Question écrite courte | Premier texte en moins de … s (note le temps) ; affichage progressif | |
| A5 | Parler : question courte | Écoute → réflexion → réponse audible ; note le temps jusqu'au premier son | |
| A6 | Toucher Stop pendant la réponse | Arrêt en moins d'une seconde ; JARVIS reste utilisable | |
| A7 | Importer un petit document, puis demander « Selon mes documents… » | Réponse citée, ou « je ne trouve pas » si l'information est absente | |
| A8 | « Souviens-toi que je préfère le thé » | Proposition affichée ; rien n'est retenu sans « Confirmer » | |
| A9 | Observer la sphère pendant l'écoute et la réflexion | Immobile ; elle ne s'anime que pendant la réponse | |
| A10 | Vingt échanges d'affilée | Pas de plantage ; note la batterie avant et après, et la chaleur au toucher | |
| A11 | Fermer, rouvrir | La conversation reprend | |

## Partie B — 1.7B (optionnelle, étude seulement ; à faire après la partie A réussie)

L'APK garde le 1.7B **désactivé par défaut**. La partie B n'est possible qu'avec un build d'étude explicitement autorisé par toi : je ne l'active pas moi-même.

| # | Geste | Résultat attendu |
|---|---|---|
| B1 | Importer `Qwen3-1.7B-Q4_K_M.gguf` | « vérifié (SHA-256) » ; refus si la mémoire libre est insuffisante |
| B2 | Mêmes questions que A3–A6 | Note le premier texte, le temps total et l'arrêt |
| B3 | Le panneau AI Core affiche le profil et le modèle chargés | Un seul modèle chargé ; retour automatique en ÉCO si la mémoire ou la température ne suffisent pas |
| B4 | Dix échanges | Chaleur, batterie, aucune réponse coupée par le délai de 90 s |

## À me renvoyer

- Le tableau OK / NON et les temps notés.
- Le modèle du téléphone.
- Une capture en cas de problème.
- Rien de personnel : ni audio, ni contenu de tes documents.

Tant que ce protocole n'est pas rempli, tous les résultats restent au niveau **émulateur** et non **appareil réel**.
