# DEVICE-01 (version simple) — essai de JARVIS V3 sur ton POCO

À faire **par toi**, quand tu le décides. Rien n'est installé à distance. Durée : environ 45 minutes. Garde le téléphone en charge, à température ambiante.

## Avant de commencer

1. Utilise l'APK **release** construit à partir du SHA convenu (S04 aujourd'hui : `e6489bf…`). Vérifie son SHA-256 dans le rapport CI.
2. Signe-le **toi-même** avec ta clé. Je ne signe jamais à ta place.
3. Copie sur le téléphone les trois fichiers de modèles indiqués dans le rapport : LLM, reconnaissance vocale et voix, avec leurs SHA-256.
4. Active le **mode avion**.

## Étapes (note OK / NON et une remarque)

| # | Geste | Ce qu'on doit voir |
|---|---|---|
| 1 | Installer, ouvrir | Une seule permission demandée (micro) ; aucune connexion |
| 2 | Importer les modèles | Empreintes vérifiées ; refus clair si un fichier est faux |
| 3 | Écrire « Bonjour, je m'appelle … » puis « Comment je m'appelle ? » | Ton prénom est retrouvé |
| 4 | Appuyer sur Parler et dire une question courte | Écoute, puis réflexion, puis réponse **audible** ; noter le temps jusqu'au premier son |
| 5 | Interrompre pendant la réponse | Arrêt immédiat ; JARVIS reste utilisable |
| 6 | Importer un petit document texte, puis demander « Selon mes documents, … » | Réponse citée ; « je ne trouve pas » si l'information est absente |
| 7 | « Souviens-toi que je préfère le thé » | Proposition affichée ; rien n'est retenu sans ton « Confirmer » |
| 8 | Observer la sphère pendant l'écoute et la réflexion | Immobile ; elle ne s'anime que pendant la réponse |
| 9 | Activer TalkBack et parcourir l'écran | Boutons annoncés ; changements d'état lus |
| 10 | Dix échanges d'affilée, puis toucher l'arrière du téléphone | Pas de chaleur excessive ; noter le pourcentage de batterie avant et après |
| 11 | Fermer, rouvrir | Conversation reprise ; aucun plantage |

## À me renvoyer

- Le tableau OK / NON.
- Les temps notés.
- Une capture en cas de problème.
- Rien de personnel : aucun audio, ni le contenu de tes documents.
