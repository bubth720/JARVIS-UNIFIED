# Protocole de validation sur POCO X8 Pro — JARVIS (CONVERSATION-01 + Command Center V2)

**Rien n'a été installé sur ton téléphone.** Ce protocole ne s'exécute qu'avec ton autorisation explicite.
Ce qu'il fera alors :

- installer l'APK de qualification (et, pour l'étude du modèle, l'APK de test) ;
- copier les ressources vérifiées.

Les validations ci-dessous sont **celles que l'émulateur ne peut pas prouver**.

## 0. Préparation (avec ton accord)

1. Mode avion activé : JARVIS n'a pas de permission Internet ; le mode avion confirme l'absence de dépendance réseau.
2. Installation de l'APK de qualification. Sa SHA-256 est publiée dans le rapport de livraison et doit être
   vérifiée avant installation.
3. Import des ressources par Réglages › Importer. Chaque fichier est vérifié par son empreinte :

   | Ressource | Fichier | SHA-256 |
   |---|---|---|
   | Modèle de langage | `Qwen3-0.6B-Q4_K_M.gguf` | `ac2d9771…` |
   | Reconnaissance vocale | `ggml-base-q5_1.bin` | `422f1ae4…` |
   | Voix | `pocket-fr-6l-alba.zip` | — |

4. Aucun document personnel n'est nécessaire. Les tests utilisent des documents synthétiques fournis.

## 1. Conversation vocale complète (acceptation 6, 7, 8)

| # | Action | Attendu | Mesure à relever |
|---|---|---|---|
| V1 | « Parler » puis « Bonjour, je m'appelle Léo. » | Transcription exacte, réponse écrite puis parlée | VOICE CENTER : écoute, transcription, premier son |
| V2 | Question longue (« Explique-moi la photosynthèse ») | Phrase d'attente audible **après 1,2 s** si la réponse tarde ; elle s'arrête dès que la réponse est prête | Délai jusqu'au premier son **< 5 s** |
| V3 | Pendant la réponse parlée : « Interrompre » | Arrêt immédiat de la voix et du calcul ; la session reste utilisable | — |
| V4 | Couper le micro (ou parler très bas) puis réessayer | Message « Je n'ai rien entendu », aucune réponse dupliquée | — |
| V5 | Haut-parleur, puis casque Bluetooth | Voix intelligible, pas de coupure | Avis subjectif |

## 2. Conversation, personnalité, mémoire (acceptation 1 à 4)

| # | Scénario | Attendu |
|---|---|---|
| C1 | Prénom, correction (« non, je m'appelle Léo »), frère de 12 ans, 3 questions sans rapport, puis « Comment je m'appelle ? » et « Quel âge a mon frère ? » | « Léo » (pas le frère), « 12 ans » |
| C2 | Changement de sujet puis retour | Contexte conservé |
| C3 | 15 échanges de suite | Tutoiement constant, JARVIS ne se nomme jamais Athéna |
| C4 | Fermer l'application (balayage), la rouvrir, « Reprendre la dernière conversation », « Tu te souviens de mon prénom ? » | « Léo » |
| C5 | « Souviens-toi que je préfère le thé. » → Refuser ; puis → Mémoriser ; nouvelle session : « Qu'est-ce que je préfère boire ? » | Rien stocké après le refus ; rappel après acceptation ; suppression possible dans MEMORY VAULT |
| C6 | « Allume la lumière du salon. » | JARVIS dit qu'il ne peut pas ; s'il prétend l'avoir fait, la note système « Aucune action n'a été exécutée » apparaît et est lue |

## 3. Documents locaux NEXUS (acceptation 5)

**Prérequis :** le SQLite du téléphone doit fournir FTS5. NEXUS le vérifie lui-même au premier usage
(Command Center › NEXUS › « Moteur »).

| # | Action | Attendu |
|---|---|---|
| N1 | Ouvrir NEXUS | « prêt » **ou** « indisponible : FTS5 absente ». Dans ce cas, la recherche documentaire ne peut pas fonctionner avec le SQLite d'Android et une décision de ta part est requise (bibliothèque SQLite embarquée). |
| N2 | Importer le document synthétique `club-astronomie.txt` (fourni) | « indexé localement » |
| N3 | « Selon mes documents, quand se réunit le club d'astronomie ? » | Réponse avec « Sources locales : club-astronomie.txt » ; le bouton « Pourquoi ? » liste l'extrait |
| N4 | « Selon mes documents, quel est le prix du vélo électrique ? » | JARVIS dit qu'aucun document ne le contient |

## 4. Interface V3 / Command Center V2

| # | Vérification | Attendu |
|---|---|---|
| I1 | Sphère au repos, pendant l'écoute et pendant la réflexion | **Immobile**. Animation légère uniquement pendant la réponse, arrêt après. Aucune rotation au doigt. |
| I2 | Avatar d'Athéna | Immobile hors réponse ; la bouche suit la voix ; masquable |
| I3 | Menu radial, Command Center (10 écrans), Palette de commandes | Aucun texte tronqué ou superposé. MISSIONS / AGENTS / AUTOMATIONS affichés « à connecter ». |
| I4 | Rotation paysage, mise en arrière-plan, retour | État conservé, aucune animation en arrière-plan |

## 5. Mesures de ressources (rapport chiffré)

Relevées avec la même session de 20 échanges, par `adb shell dumpsys` (tu peux aussi lire AI CORE / EVOLUTION LAB) :

- `dumpsys meminfo fr.jarvis.v3` : PSS au repos, modèle chargé et après fermeture de session.
- `dumpsys thermalservice` : statut thermique avant et après 20 échanges.
- `dumpsys batterystats --charged fr.jarvis.v3` : consommation sur 30 min d'usage.
- Latences affichées par AI CORE (premier jeton, total, jetons/s) et VOICE CENTER (premier son).

## 6. Comparaison 0.6B / 1.7B sur le téléphone (ton autorisation spécifique requise)

L'émulateur x86 ne peut pas départager les modèles : le 1.7B y est coupé par le délai protégé de 90 s. Sur le POCO :

1. Installer l'APK de test (aucun changement de l'application de production).
2. Copier les deux modèles vérifiés (manifestes JARVIS-LLM, SHA-256 contrôlés).
3. Lancer, pour chaque modèle, le même harnais qu'en CI :

   ```
   adb shell am instrument -w -e class fr.jarvis.v3.ModelStudyTest#benchOneModel \
     -e model /data/local/tmp/study.gguf -e sha256 <sha> -e label <label> -e small <true|false> \
     -e benches /data/local/tmp/fr-bench-30.json,/data/local/tmp/fr-conv-01.json \
     fr.jarvis.v3.test/androidx.test.runner.AndroidJUnitRunner
   ```

   **Mesures relevées :** 44 scénarios, premier jeton, jetons/s, PSS / RSS / pic, statut et marge thermiques,
   température batterie.

4. Le score est calculé par `JARVIS-LLM a02/tests/bench_score.py`.

**Aucun remplacement de modèle ni changement des limites protégées** sans ta décision sur ces mesures.

## 7. Critère de fin

- La version n'est déclarée opérationnelle sur appareil que lorsque les sections 1 à 5 sont passées sur le
  POCO, avec les mesures jointes.
- Tout échec est rapporté tel quel, avec capture et journal.
