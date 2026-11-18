# Rapport d'état, d'audit et de feuille de route — 18/11/2026

Ce rapport repart de l'état réel du projet au 18/11/2026. Aucune fusion n'a été faite dans `main`, rien n'a été installé sur le téléphone et aucun modèle n'a été remplacé.

Chaque élément porte l'une de ces mentions :

| Mention | Sens |
|---|---|
| **VÉRIFIÉ** | Exécuté pendant cette mission, avec résultat mesuré. |
| **CORRIGÉ** | Modification faite et testée. |
| **RECOMMANDÉ** | Reste à faire. |

## 1. État d'avancement réel

### 1.1 Branches de référence

- **INTERFACE `ccr-e05fe51e-ycqubx` @ `aa344f3`**. La branche contient l'intégralité de `codex/gpu-forge-g02-captures-20261116`. Avant l'ajout d'A-038, son arbre était identique, octet pour octet, à celui de cette branche Codex.
- **UNIFIED `ccr-e05fe51e-ycqubx`**. Elle avance rapidement sur `codex/research-n01-b0-lab-20261118`, qui contient G03, N01-A2, N01-A3 et RESEARCH-B0, puis ajoute A-037 et ce rapport.
- **NEXUS**. La tête la plus récente est `codex/nexus-n01-a3-routing-20261118` @ `5f10193`, avec la PR brouillon #16 (non fusionnée).
- **LLM et VOICE**. Têtes `ccr-5cf17ed2-phgk00` (14/11), sans changement depuis.
- **SERVICES et EVOLUTION**. Inchangés depuis le 29/10.

### 1.2 Fonctionnalités

| Domaine | État | Preuve |
|---|---|---|
| Conversation locale (Qwen3-0.6B, moteur A02 scellé, hors ligne) | Opérationnelle sur émulateur | Campagnes API 29/35 |
| Voix : micro, STT whisper.cpp, Pocket TTS, interruption | Opérationnelle sur émulateur ; audio réel non qualifié | A-013, appareil requis |
| Sphère et cockpit V3, avatar Athéna 2D procédural | Opérationnels ; sphère encore redessinée hors réponse | A-008, ouvert |
| Command Center V2 (10 onglets) | 4 opérationnels, 3 partiels, 3 « à connecter » | Captures du run 44034195561 |
| MEMORY VAULT (souvenirs avec consentement) | Partiel ; export chiffré absent | A-019 |
| NEXUS (bibliothèque locale, FTS5, citations) | Partiel ; PDF et Kiwix absents | A-020 |
| Réponses documentaires fiables (absence et contradiction dites, citations) | Développé et testé en JVM ; émulateur en cours | Points 4 et 5 du 15/11 |
| MISSIONS, AGENTS, AUTOMATIONS, SERVICES | Absents (« à connecter ») | A-018 |
| RESEARCH | Laboratoire synthétique isolé seulement (B0) ; aucune collecte réelle | docs/research-b0 |
| GPU-FORGE | Préparation G03 (corpus, budget) ; aucune dépense GPU | tooling/gpu_forge |
| LEARNING-L01 | Non démarré (PDF de référence absent) | A-021 |
| Validation sur appareil réel (POCO) | **Aucune** | — |

Par rapport aux spécifications initiales (ADR-001, feuille de route 001F) :

- Le pilote CORE → LLM → interface est réalisé au stade laboratoire (V1, V1-B, V3).
- Les intégrations SERVICES et EVOLUTION, ainsi que l'architecture PC centrale, restent au stade de la spécification.

### 1.3 Éléments obsolètes ou incohérents

| Élément | Constat | Traitement |
|---|---|---|
| `docs/ROADMAP.md` (15/10) | Missions P0 décrites comme « non commencées » | Laissé tel quel (fichier historique figé par les portes UNI-08) ; la section 7 le remplace. **RECOMMANDÉ** : bandeau « obsolète » avec accord. |
| Branche de développement INTERFACE | Divergeait de la branche Codex (correctif A-036 en double) | **CORRIGÉ** : revert de mon doublon et fusion, sans réécriture d'historique (`b1224ae`). |
| Run de captures 43709555526 (15/11) | Échoué (A-036), donc aucune capture produite | Captures produites et vérifiées par le run Codex 44034195561. Mon run en doublon du 18/11 (44389637512) a été annulé. |
| Campagne émulateur complète | Dernière exécution sur `8f77a8d` (15/11) ; les corrections des points 4 et 5 et les tests P à T n'avaient jamais tourné | **Lancée** sur `b1224ae` : run 44391288619. |

## 2. Tests réellement exécutés

| Test | Où | Résultat |
|---|---|---|
| Tests JVM des gardes V3 (documents, injections, journal, contexte…) | Local, kotlinc 2.1.20 | **37/37** |
| Banc du script émulateur (faux `adb`, deux modes) | Local | **19/19** |
| Tests Python de validation des captures | Local | **12/12** |
| UNIFIED : campaign, v1, reuse_r1plus, gpu_forge, integration, nexus_n01_a2, arch01, workspace | Local, Python 3.13 | **222 tests passés**, 1 ignoré |
| RESEARCH-B0 (runner hors ligne) | Local | Python 3.12 : 63/63. Python 3.13 : **36 échecs** (A-037), puis **63/63 après correction**. |
| RESEARCH-B0 en CI (namespace réseau isolé, préservation avec CORE) | Run 44391205905 sur `977e475` | **Vert** (3 jobs) |
| INTERFACE : compilation V3, tests unitaires, Lint, inspection de l'APK | Run 44391288619 sur `b1224ae` | **Vert** |
| Workflow Android (application historique) | Runs 44390535177 et 44391511126 | **Verts** |
| Captures réelles des écrans | Run Codex 44034195561 | 22 captures × 2 API, vérifiées |
| Campagne émulateur complète (qualification + audits T1–T5) | Run 44391288619 | **En cours** au moment de la rédaction |

Non exécutable dans cet environnement :

- Le contrôle de préservation de RESEARCH-B0 en local, car le dépôt CORE est hors périmètre ; il a en revanche été exécuté en CI.
- Toute mesure sur appareil réel.
- La compilation Gradle locale : pas de SDK Android ni de KVM ici.

## 3. Problèmes détectés pendant cette mission

| ID | Gravité | Problème | État |
|---|---|---|---|
| A-036 | Majeure | Le mode captures cassait l'étape Guards ; aucun APK n'était construit (défaut introduit par moi le 15/11). | **CORRIGÉ** par Codex, convergé et vérifié 19/19 ; captures validées sur émulateur. |
| A-037 | Majeure | Le laboratoire RESEARCH-B0 échoue sous Python 3.13 (certificats non conformes à la vérification X.509 stricte). | **CORRIGÉ** (`977e475`) : 63/63 sous 3.12 et 3.13, CI verte. La vérification TLS n'est pas affaiblie. |
| A-038 | Majeure | Android 12+ : conversations (en clair), souvenirs et bibliothèque transférables vers un nouvel appareil malgré `allowBackup=false`. | **CORRIGÉ** (`aa344f3`) : `dataExtractionRules` qui exclut tout, et contrôle `aapt` en CI ; vérification au prochain build. |
| A-039 | **Critique avant appareil** | L'APK publié est une version debug : via USB-debug, `run-as` lit les données privées. | **RECOMMANDÉ** : build release signé avant toute installation sur le POCO. |

Anomalies héritées encore ouvertes : A-008 (sphère), A-011 et A-034 (tests API 35), A-004 et A-023 (limites du modèle 0.6B), A-012 et A-013 (appareil requis), A-014, A-016, A-018 à A-021. Voir `REGISTRE-ANOMALIES.md`, où chaque anomalie porte ses quatre niveaux de validation.

## 4. Sécurité et fiabilité — vérifications faites

| Point | Résultat |
|---|---|
| Permissions de l'application V3 | **VÉRIFIÉ** : une seule (micro), pas d'Internet (contrôle `aapt` en CI), pas de trafic en clair, `allowBackup=false`, activité secondaire non exportée. |
| Secrets dans les 8 dépôts (tête la plus récente de chacun) | **VÉRIFIÉ** : aucun jeton GitHub, clé AWS ou Google, clé privée ou jeton Slack détecté. |
| Workflows | **VÉRIFIÉ** : aucun `pull_request_target` et aucune injection d'expressions non fiables. Droits d'écriture limités aux deux workflows INTERFACE qui committent les captures. |
| Workflows sans bloc `permissions:` | 7 workflows historiques (LLM, UNIFIED). **RECOMMANDÉ** : `contents: read` explicite, après accord, car ce sont des fichiers figés. |
| Action tierce épinglée par étiquette | `reactivecircus/android-emulator-runner@v2` dans 14 workflows LLM et VOICE (INTERFACE l'épingle par empreinte). **RECOMMANDÉ** : épinglage par SHA. |
| Données sensibles | Journal de conversation en clair dans l'espace privé (A-016). Transfert d'appareil fermé (A-038). Debug à fermer (A-039). |
| Sauvegarde, reprise, erreurs | Ligne de journal tronquée (A-032, JVM 3/3), stockage plein (A-035), perte d'émulateur (A-029, 19/19), session non bloquante (A-026, émulateur) : corrigés. Ceux qui étaient en attente d'émulateur sont dans la campagne en cours. |
| Injections documentaires | Deux couches. Pire cas simulé : 0/30 attaque inédite présentée comme parole de JARVIS (JVM). La couche 1 seule ne détecte que 9/30 attaques inédites : limite documentée. Test Q sur émulateur en cours. |

## 5. Optimisations recommandées, par priorité

**P0 — avant toute installation sur le POCO**

1. Build release (A-039), avec signature par le propriétaire.
2. Campagne complète verte sur API 29/35, y compris P, Q, R, S et T.
3. Chiffrement du journal via Keystore (A-016).

**P1 — fiabilité**

4. A-008 : dessins résiduels de la sphère (le test P sépare désormais pixels et coût).
5. A-034 : test e bloqué sur API 35.
6. A-011 : défilement des onglets sur API 35.
7. Épingler les actions tierces par SHA.
8. Ajouter `permissions: contents: read` aux workflows historiques (avec accord).

**P2 — ergonomie et performances**

9. Mesures sur appareil : premier son, débit en jetons/s avec et sans phrase d'attente (A-014), énergie et thermique.
10. TalkBack réel (A-033).
11. Décision sur le modèle 1.7B (A-004, A-012), à prendre après mesure sur le POCO.

**P3 — simplification**

12. Le dépôt UNIFIED compte 56 branches et INTERFACE 41. Archiver (sans supprimer) les branches de missions closes, après accord, pour réduire le risque d'erreur de base, comme celui qui a causé A-036.
13. Un seul runner de tests Python. Le nom de fichier `test_reception.py`, en double, empêche aujourd'hui une collecte `pytest` globale ; renommer avec accord, car ce sont des fichiers figés.

## 6. Corrections effectuées pendant cette mission

| Dépôt | Commit | Objet |
|---|---|---|
| INTERFACE | `a200d7a`, `b1224ae` | Convergence avec la branche Codex : revert du doublon et fusion, arbre identique. |
| INTERFACE | `aa344f3` | A-038 : règles d'extraction des données et contrôle CI. |
| UNIFIED | `977e475` | A-037 : certificats du laboratoire compatibles Python 3.13. |
| UNIFIED | `bad6d51` et ce commit | Registre (A-036 à A-039) et rapport. |

Chaque correction a son test de non-régression, exécuté avant le commit (section 2).

## 7. Feuille de route actualisée

| Étape | Contenu | Condition de sortie |
|---|---|---|
| **R0** (en cours) | Résultats de la campagne 44391288619 ; correction des échecs sans nouvelle fonctionnalité | API 29/35 verts, ou défauts enregistrés |
| **R1** | APK release signé (A-039), chiffrement du journal (A-016), CI sur `aa344f3` | `aapt` : non debuggable, `dataExtractionRules` présentes |
| **R2** | Validation POCO (protocole DEVICE-01 existant) : voix réelle, latence, mémoire, thermique, TalkBack | Mesures sur appareil, **avec ton autorisation d'installation** |
| **R3** | Décision modèle 0.6B ou 1.7B à partir des mesures R2 | Ton accord |
| **R4** | NEXUS : PDF et Kiwix ; MEMORY VAULT : export chiffré | Tests émulateur et appareil |
| **R5** | RESEARCH N01-B1 (admission synthétique, toujours en boucle locale) ; GPU-FORGE G03 | Accords distincts (réseau réel, dépense GPU) |
| **R6** | SERVICES, MISSIONS, AGENTS : actions encadrées par permission | Après R2 ; contrats CORE |
| — | LEARNING-L01 | Dès réception du PDF de référence |
