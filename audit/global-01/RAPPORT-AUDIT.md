# AUDIT-GLOBAL-01 — rapport consolidé et plan de stabilisation (point d'arrêt)

**Date :** 14/11/2026. Branche de développement `ccr-5cf17ed2-phgk00` (INTERFACE, LLM, UNIFIED).

**Ce document est le point d'arrêt demandé.** Aucune correction massive n'est engagée avant ta validation du
plan (§10). Les tests déjà lancés n'ont pas été interrompus.

**Livrables associés :**

| Fichier | Contenu |
|---|---|
| `registre.json` / `REGISTRE-ANOMALIES.md` | Registre unique, 21 entrées |
| `MATRICE-COUVERTURE.md` | Exigences → tests → niveau de preuve |
| `CAMPAGNE-TESTS.md` | Plan A à H |
| `DEPENDANCES.md` | Cartographie réelle |
| `LEARNING-L01-PLAN.md` | Plan LEARNING-L01 |

## État réel des dépôts autorisés

| Dépôt | Branche par défaut | Branche de dév. | Dernière CI pertinente | Rôle dans l'application |
|---|---|---|---|---|
| JAVIS-Local-v2 (CORE) | main 226e2e8 | — | M50-S1 verte @5da9838 (03/11) | Sources épinglées 5da9838 |
| JARVIS-LLM | main 917e335 | 3e2560e | Étude verte ; **A02 natif rouge (A-002)** | Moteur 2e01177 + étude |
| JARVIS-VOICE | feat/pocket-tts-cpu-prototype | — | Labo vert ; **gardes 005J et SDK rouges @92d0745 (A-003)** | Pocket TTS @92d0745 |
| JARVIS-INTERFACE | development/mission-002 | 3dd3649 | V3 : constat ci-dessous | **Application unifiée** (`labs/v3`) |
| JARVIS-NEXUS | main b27df0b | — | NEX-07 verte (12/11) ; m53 rouge (08/11) | Sources 06ccf98 |
| JARVIS-SERVICES | main c9f94ad | — | Verte (29/10) | **Non intégré** |
| JARVIS-UNIFIED | main e4435f4 | d07188d+ | **Portes UNI-08 et FUSION-02 rouges (A-001, runner)** | Rapports, contrats ARCH-01 |
| JARVIS-VOLUTION- | main a67d3b6 | — | Verte (29/10) | **Non intégré** (désactivé) |
| JARVIS-INTERFACE- | main a857f50 | — | Aucune CI | Non utilisé |

## 1. Ce qui fonctionne réellement (prouvé sur émulateur API 29 et 35, mode avion, vrai moteur)

| Fonction | Preuve |
|---|---|
| Installation, une seule permission (micro), aucune permission Internet | Test a |
| Import vérifié par empreinte des ressources | Test b |
| Conversation locale Qwen3-0.6B (CORE → A02) | Tests c et f |
| Contexte au-delà des 3 échanges relus ; corrections ; référence implicite ; retour de sujet | Test f, 8/8 sur les deux niveaux d'API (run 43616811194) |
| Personnalité Athéna compacte, tutoiement, JARVIS ne se nomme jamais Athéna ; bascule Neutre / vouvoiement au tour suivant | Test f |
| Refus d'une action réelle, avec note système si le modèle prétend l'avoir faite | Test f |
| Historique local, reprise (texte + contexte), suppression | Test f (dont reprise par l'interface) |
| Recherche documentaire NEXUS, SQLite embarqué 3.46.0, FTS5, réponse citée | Test g |
| Mémoire durable seulement avec consentement : refus → rien ; acceptation → rappel dans une nouvelle session ; suppression | Test h, API 29 (API 35 à retester) |
| Sphère immobile au repos et en réflexion, animée en parole puis arrêtée, aucun geste ; mouvement réduit | Tests c et d |
| Réouverture après arrêt forcé, aucun plantage | Tests reopen et no_crash |
| Empreinte mémoire mesurée : 0.6B 557 Mio PSS, 1.7B 1 234 Mio, libération confirmée | Étude Android |

## 2. Problèmes confirmés

Détail et preuves dans le registre.

| ID | Problème | Gravité | Statut |
|---|---|---|---|
| A-004 | Hallucinations factuelles du 0.6B | critique | ouvert (limite du modèle) |
| A-005 | Réponse documentaire inventée quand aucun document ne correspond | majeure | corrigé par note système, à retester |
| A-008 | Sphère redessinée pendant l'écoute | majeure | corrigé, à retester |
| A-010 | Rappel de souvenirs ambigus injectés sans confirmation (écart au contrat CORE) | majeure | ouvert |
| A-001 | Portes CI historiques UNIFIED rouges (image runner) | majeure | ouvert |
| A-002 | Porte A02 qui dépend du savoir du modèle | majeure | ouvert |
| A-003 | VOICE @92d0745 échoue à ses gardes | majeure | ouvert |
| A-011 | Tests d'interface instables (outillage) | mineure | à retester |
| A-017 | Commit non compilable (processus de l'agent) | mineure | corrigé |

**Corrigés et validés pendant les missions :**
- A-006 : fausse action ;
- A-007 : prénom du frère ;
- A-009 : FTS5 absente du SQLite plateforme.

## 3. Régressions

- **Aucune régression constatée** des fonctions V1 et V3 gelées : 430 fichiers gelés inchangés (garde de
  portée verte à chaque commit), tests a, b, d, e, reopen et no_crash verts.
- **Régression de comportement introduite puis corrigée :** l'instruction Athéna complète doublait le
  premier jeton du 0.6B → rendu compact par défaut.
- **Régressions d'infrastructure, hors code :** A-001 et A-002.

## 4. Incompatibilités architecturales

1. **Politique A02.** Contexte 768, 1 thread, 3 échanges relus et sortie 128 bornent la longueur des réponses
   et du contexte. Compensé par la mémoire de travail ; un vrai long contexte exige une décision moteur.
2. **Deux SQLite dans un même processus.** Plateforme pour CORE, embarqué pour NEXUS. Bases distinctes ;
   à surveiller.
3. **ARCH-01 non branché.** `ModelBackend` n'est pas encore le chemin réel ; prérequis d'un changement de modèle.
4. **Internet.** RESEARCH-01 exigerait un composant réseau séparé, pour ne pas perdre l'absence de permission
   Internet.
5. **VOICE.** Le commit utilisé échoue à ses gardes (A-003).

## 5. Fonctionnalités manquantes

- SERVICES, MISSIONS, AGENTS, AUTOMATIONS : affichés « à connecter ».
- Export chiffré des souvenirs.
- PDF et Kiwix dans NEXUS.
- Accessibilité vérifiée.
- Disposition tablette.
- Modes Focus / Full Cockpit, Compare, Mission Replay (PDF CC V2 §8).
- LEARNING-L01.
- RESEARCH-01 : non autorisée.

## 6. Limitations des modèles IA

- **0.6B** : 23–28/44 au banc. Factuel 2–6/10. Invente des faits et des réponses documentaires. Suit mal
  certaines consignes : les gardes déterministes sont indispensables.
- **1.7B** : 36–37/44 sur Linux, factuel 8–9/10. Environ 2,2 fois la mémoire. Trop lent sur émulateur x86 :
  coupé par le délai protégé de 90 s. **Mesure POCO indispensable avant toute décision.**

## 7. Problèmes spécifiques à Android

1. FTS5 absente du SQLite plateforme : résolu par le SQLite embarqué.
2. Lint MissingPermission : l'état réseau exigerait une permission ; remplacé par le réglage mode avion.
3. Recompositions Compose coûteuses : sphère, niveau micro.
4. Puits audio et micro silencieux de l'émulateur : la voix réelle n'est pas prouvable en CI.
5. Émulateur x86 avec 1 thread : les latences ne valent pas pour un téléphone.

## 8. Corrections prioritaires

Par ordre de la consigne :

1. Sécurité et intégrité des données : A-010 (rappel ambigu), F4 (injection documentaire, test à écrire),
   G6 (souvenir créé hors consentement, test à écrire).
2. Plantages et régressions : retester A-005, A-008, A-011 sur le run en cours.
3. Contrats et intégration : A-002 (séparer intégrité moteur et qualité), A-001 (épingler l'image runner des
   portes historiques), A-003 (décision VOICE).
4. Fiabilité des réponses : C3 (« je ne sais pas »), C8 (général vs documentaire), F2 (documents contradictoires).
5. Voix : D2 et D3 (erreurs et interruptions à chaque étape).
6. Performance : H4 (stabilité 50 tours, cycles charger / décharger).
7. Interface : E2, E3, E6 (textes longs, petites surfaces, accessibilité).

## 9. Tests encore impossibles en CI

Vrai micro, haut-parleur et Bluetooth ; latence perçue ; CPU, consommation et thermique réels ; vitesse et
qualité du 1.7B sans coupure ; GPU réel de la sphère ; SQLite du POCO.

→ Protocole POCO X8 Pro : `reports/conversation-01/PROTOCOLE-POCO-X8-PRO.md` (non exécuté, autorisation requise).

## 10. Plan de STABILISATION-01 recommandé

**À valider.** Chaque groupe = une branche de travail cohérente, un test reproduisant le défaut avant la
correction, un test de non-régression, puis entrée du registre mise à jour.

| Groupe | Contenu | Dépôts | Accord requis |
|---|---|---|---|
| **S1 — Sécurité et données** | A-010 (rappel READY uniquement, ambiguïté → choix de l'utilisateur) ; tests F4, G6, F6 | INTERFACE | non (dans le périmètre autorisé) |
| **S2 — Fiabilité des réponses** | Tests C3, C8, F2, F3 ; garde « je ne sais pas » si nécessaire ; note documentaire étendue | INTERFACE | non |
| **S3 — Voix** | Tests D2, D3, D4 (émulateur) ; corrections | INTERFACE | non |
| **S4 — Interface et accessibilité** | E2, E3, E6, E7 ; corrections de mise en page | INTERFACE | non |
| **S5 — CI et contrats** | A-002 (workflow successeur intégrité / qualité, sans toucher l'historique) ; A-001 (épinglage `ubuntu-24.04` dans les portes historiques UNIFIED) ; A-003 (VOICE) | LLM, UNIFIED, VOICE | **oui** pour A-001 (fichiers historiques) et A-003 (VOICE non modifié jusqu'ici) |
| **S6 — Robustesse et performance** | G1 à G4, H4 | INTERFACE | non |
| **Ensuite** | LEARNING-L01 (après réception du PDF), puis APK de qualification et validation POCO | — | — |

**Constat de méthode, en réponse à ta demande d'arrêter la découverte au fil de l'eau :** la campagne T1 + T2
(environ 25 tests nouveaux) est exécutée **avant** les corrections S1 à S6. Ses résultats alimentent le
registre en une seule fois, puis les corrections sont faites par groupe.
