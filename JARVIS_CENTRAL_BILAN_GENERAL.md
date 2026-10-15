> **Rapport historique de clôture001F, conservé.** Depuis ce bilan, l’utilisateur
> a approuvé l’orientation ADR-001 avec précisions le15 octobre2026. Voir
> [ADR actuelle](docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md) et
> [validation officielle](docs/DECISIONS/VALIDATION-UTILISATEUR-ADR-001-2026-10-15.md).
> Les anciens statuts non approuvés ci-dessous décrivent la clôture001F ;
> aucun résultat de tests, inventaire GitHub ou raccordement n’est actualisé par
> cette seule décision architecturale.

# JARVIS-CENTRAL — bilan général Mission001F

**Terminée localement, publication bloquée. ADR proposée, non approuvée.**
Ce rapport clôt l’audit et la préparation de consolidation, sans raccordement
applicatif ni nouvelle mission de développement. Les huit composants logiques
occupent neuf dépôts : INTERFACE et INTERFACE- restent deux identités distinctes.
La branche de reprise est `mission-001f-closure`, issue de d74730a. Le commit exact
de livraison se lit par `git rev-parse mission-001f-closure` et dans le reçu final
hors Git ; ce document ne prétend pas contenir le SHA de son propre commit.

## 1. Publication et conservation

- Branche historique architecture inchangée :
  `d74730a4b5ed817de1cdd163a96c3bdf72a1e4d8`, parent
  `61b30fcfe9f7cac471c164521b5f6e7b80a82bb0`.
- Branche mission003 inchangée :
  `f7b7a5ad96527bc43bd5349b97b7834667da9f03`.
- Missions001/002 conservées à004b89d/55680bc, ancêtres vérifiés. 89 fichiers suivis
  au départ, arbre propre ; git fsck sans corruption (un blob orphelin préexistant,
  aucune suppression). Les cinq documents001 et livrables002/003 sont présents.
- Lecture Git origin réussie le15 octobre2026 ; seule main distante est annoncée,
  `e4435f4bd60c5fdc5595c411cc8cab9da7ef020b`, un README. Aucune main modifiée.
- Dry-run non destructif sur branche de reprise : refus128/HTTP403, message exact
  dans [access.json](reports/001f/access.json). Aucun push réel ni PR en001F,
  aucune branche distante de consolidation confirmée ; aucune URL fictive.
- API GitHub bloquée séparément par politique réseau : neuf proxy_forbidden,
  statut CI/PR courant inconnu. Installation/Contents:write et expiration non
  observables ; ne pas attribuer le403 à un manque précis non démontré.
- Bundle initial vérifié/restauré : `.audit-cache/001f/safety.bundle`, quatre branches,
  SHA256 `cae1bb45c87746f695d3db037ea1d2029bd2518737582b5f60319f94e43c4713`.
- Bundle final hors Git : `.audit-cache/001f/JARVIS-UNIFIED-001F.bundle`, plus
  `.sha256` et `.receipt.json` à côté ; contient la branche001F avec les précédentes.
  Son reçu donne SHA final, liste de refs, fichiers et restauration vérifiée.
  [Récupération/publication manuelle](docs/RUNBOOK.md).

Aucun secret ou fichier privé ajouté ; le validateur et la revue des différences
recherchent les jetons usuels, clés privées et formats sensibles. Cela ne constitue
pas une certification exhaustive de tout secret arbitraire dans l’historique.

## 2. Architecture soumise à décision

[ADR existante](docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md), toujours **PROPOSED / AWAITING USER APPROVAL**.
[Page de décision](docs/DECISIONS/REVUE-ADR-001F.md) : comparaison monolithe,
APK/IPC et hybride modulaire. Recommandation : hybride modulaire avec CORE
orchestrateur, adaptateurs interchangeables et une seule configuration pilote
qualifiée. Le nombre final d’APK et le transport ne sont pas tranchés.

CORE possède session/permissions/confirmation ; LLM infère ; VOICE synthétise
avec moteur/pack/profil exact ; INTERFACE affiche ; NEXUS cible documents et
stockage mémoire confirmé ; SERVICES fournit outils autorisés ; EVOLUTION propose
des correctifs isolés ; UNIFIED gouverne preuves/contrats et ne tourne pas dans
l’application. Le stockage SQLite reste aujourd’hui dans CORE. Pas de changement
silencieux de responsabilité physique ni de consentement implicite.

Objections ouvertes : coût RAM de plusieurs APK, SDK24/26/29, signatures, baux
sans broker interprocessus, mappings/enveloppes et compatibilités encore génériques.
Les cinq schémas et leur sémantique ont été relus, restent inchangés et proposés.
Le contrôle d’identité, délai/annulation, mort de processus et retour arrière devront
être implémentés/testés dans une mission séparée après accord.

## 3. Neuf dépôts — état vérifié par Git et sources

Observation fraîche : 2026-10-15T17:46:31+00:00. Les dates de commits, branche par
défaut, **toutes** les branches importantes, état main et fichiers tests sont dans
[repositories.json](registry/repositories.json). Acquisition HTTPS neuve en lecture
seule dans [acquisition.json](reports/001f/acquisition.json). PR et CI actuelles
inconnues pour les neuf dépôts : [audit API](reports/001f/online/SUMMARY.md).
Les SHA ci-dessous sont les **refs inspectées**, pas nécessairement le dernier
code modifié : LLM code testé e9d408e, VOICE532c658 ; les commits ultérieurs
mentionnés sont documentaires/CI, détails dans [preuves](docs/PROUVES.md).
Aucun essai physique ni test Android exécuté pendant001F.

| Composant / dépôt exact | Branche / SHA vérifié | Code réellement présent | Tests et provenance | Limites / suite |
|---|---|---|---|---|
| CORE historique — `bubth720/JAVIS-Local-v2` | `main`<br>[226e2e8cc3eebd479805b89d035eb5c1cbcad540](https://github.com/bubth720/JAVIS-Local-v2/tree/226e2e8cc3eebd479805b89d035eb5c1cbcad540) | Commandes, SQLite, PDF/RAG, wrapper LLM, Whisper/TTS/UI | Rapport ancien : 7 heure +33 cas SQLite ; non exécutés ici | Pas de liaison LLM externe ; consentement commun et cycle capture à qualifier |
| LLM — `bubth720/JARVIS-LLM` | `mission-003b-resources`<br>[1756e29557287550b5cfdffdd911cada2a302db6](https://github.com/bubth720/JARVIS-LLM/tree/1756e29557287550b5cfdffdd911cada2a302db6) | Backend JNI llama.cpp, GGUF/SHA, garde matériel, catalogue, baux locaux | Rapport 55 domaine +16 Robolectric +1 natif ; run38636152472 non relu via API | Hors main ; budgets et arrêt à qualifier Redmi/POCO ; aucun IPC |
| VOICE — `bubth720/JARVIS-VOICE` | `feat/voice-expression-005i`<br>[f917ef15ce74a045564ddabdc407ccde4b595ba6](https://github.com/bubth720/JARVIS-VOICE/tree/f917ef15ce74a045564ddabdc407ccde4b595ba6) | Synthèse/identités/archives, expression neutre et DTO005I | Rapport 31/31 coinstallation émulateur run38762084531 ; aucune nouvelle exécution ici | Code applicatif532c658 inchangé ; profil privé et Xiaomi non validés |
| INTERFACE — `bubth720/JARVIS-INTERFACE` | `development/mission-002`<br>[d1c0931c4507e9af8f1aa60951947c23f4394b56](https://github.com/bubth720/JARVIS-INTERFACE/tree/d1c0931c4507e9af8f1aa60951947c23f4394b56) | UI Compose/StateFlow, AvatarSession sans rendu | Rapport 3 JVM ; tests Android compilés non exécutés, CI inconnue | Autonome, aucun CORE/avatar2.5D rendu ; aucune main annoncée |
| INTERFACE- distinct — `bubth720/JARVIS-INTERFACE-` | `main`<br>[a857f5019354ea1c912e6f66bebdcc053c0cb700](https://github.com/bubth720/JARVIS-INTERFACE-/tree/a857f5019354ea1c912e6f66bebdcc053c0cb700) | README seul | Aucun test découvert | Relation avec INTERFACE inconnue, ne pas fusionner/supprimer |
| NEXUS — `bubth720/JARVIS-NEXUS` | `main`<br>[b27df0b84d8f0082d17ca6278549298aaaf97926](https://github.com/bubth720/JARVIS-NEXUS/tree/b27df0b84d8f0082d17ca6278549298aaaf97926) | README seul | Aucun test découvert | Documents/mémoire/Wikipedia-Kiwix cibles, pas implémentés |
| EVOLUTION candidat — `bubth720/JARVIS-VOLUTION-` | `main`<br>[a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0](https://github.com/bubth720/JARVIS-VOLUTION-/tree/a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0) | README seul | Aucun test découvert | Nom VOLUTION- réel, rôle EVOLUTION non confirmé |
| SERVICES — `bubth720/JARVIS-SERVICES` | `main`<br>[c9f94ad2fa219a5e09cda92fb451aca606ee1646](https://github.com/bubth720/JARVIS-SERVICES/tree/c9f94ad2fa219a5e09cda92fb451aca606ee1646) | README seul | Aucun test découvert | Outils optionnels cibles, pas implémentés |
| UNIFIED — `bubth720/JARVIS-UNIFIED` | `main`<br>[e4435f4bd60c5fdc5595c411cc8cab9da7ef020b](https://github.com/bubth720/JARVIS-UNIFIED/tree/e4435f4bd60c5fdc5595c411cc8cab9da7ef020b) | Remote main README ; consolidation et backup fictif locaux | 80 tests locaux réellement réussis en001F ; CI distante non exécutée | Publication refusée403, ADR proposée, aucun runtime Android |

CORE est confirmé comme fonction du projet historique JAVIS-Local-v2 ; cela
n’autorise pas un renommage ni l’équivalence avec tout dépôt JARVIS-CORE.
Sondes exactes JARVIS-CORE et JARVIS-EVOLUTION : « Repository not found » Git128,
HTTP non déterminé, inaccessible ou absent ; absence **non prouvée**.

### Merges, CI et appareil ne prouvent pas la même chose

CORE inclut par ascendance docs/heure/SQLite dans main226e2e8. LLM main917e335
n’a que deux documents ; branche003B non fusionnée. VOICE mainb80b172 n’a que
README, branches005H/I non fusionnées. INTERFACE n’annonce pas de main ;
development/mission-002 est sa branche par défaut. UNIFIED distant reste initial.
Pas de conclusion sur PR fusionnée à partir d’un simple titre de commit.

Différence fraîche : VOICE005I56ffebc→f917ef1, six fichiers workflow/docs modifiés ;
empreintes sources applicatives identiques. Le nouveau rapport cité au SHA frais
indique coinstallation H/I sur émulateur et sentinelle synthétique conservée :
[run38762084531](https://github.com/bubth720/JARVIS-VOICE/actions/runs/38762084531),
workflow1cf87c4, code532c658. Première vérification de coinstallation échouée après
nettoyage Gradle, puis réinstallation de005I sur émulateur avant contrôle corrigée.
Ces rapports sont **lus dans Git**, non vérifiés directement dans Actions ici.
La date du run non connue par API ne sera pas remplacée par date du commit.
Les huit autres refs sélectionnées et leurs arbres sont inchangés.

CI historique LLM : [run38636152472](https://github.com/bubth720/JARVIS-LLM/actions/runs/38636152472),
55/16/1 rapportés au code e9d408e ; source documentaire1756e29. VOICE005I rapporte
11 expression/18 identité/33 pocket réussis avec1/1/13 sauts, et31 instrumentés ;
l’échec005D AudioTrack4/5 reste visible. Les sauts ne sont pas des réussites.
Xiaomi005I, clonage personnel et expressivité ne sont pas validés par ces chiffres.
INTERFACE : 3 JVM rapportés ; instrumentation non exécutée ; état CI courant à
**diagnostiquer**, sans inventer qu’il est rouge. Les sources et URLs immuables
sont répertoriées dans [proofs.json](registry/proofs.json).

## 4. Matrice de communication effective

| Relation | Classe | Code trouvé / test runtime / appareil |
|---|---|---|
| CORE↔LLM | contrat seul | CORE utilise son LlamaLocalEngine ; aucun IPC LLM ; intégration non prouvée |
| CORE↔VOICE | contrat seul | DTO005I local ; aucun appel CORE transporté ; intégration non prouvée |
| CORE↔NEXUS | contrat seul générique | README NEXUS ; opération métier à spécifier ; aucun test |
| CORE↔SERVICES | contrat seul générique | README SERVICES ; aucun outil raccordé ni test |
| CORE↔INTERFACE | contrat seul générique | UI autonome, avatar contrat ; aucun test CORE/UI |
| Ressources entre processus | contrat seul | Bail v1 proposé ; coordinateur LLM process-local ; aucun broker ni test |

Toutes les colonnes « intégration testée » et « essai physique » restent non
exécutées. Les liens internes CORE et bibliothèques VOICE sont présents dans le
code, sans devenir des connexions entre APK. Coexistence d’APK, schéma validé et
merge Git ne sont pas des preuves E2E. [Matrice détaillée](docs/MATRICE_INTEGRATION.md).

## 5. Validation réellement exécutée

Commandes depuis le checkout UNIFIED, Python3.12.14/Linux :

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s registry/tests -v
python3 -m unittest discover -s backup_prototype/tests -v
python3 scripts/validate_unified.py
```

27 +23 +30 = **80 tests réussis**, aucun échec ni saut ; pas d’écart avec les80
annoncés auparavant. Réexécution001F distincte du rapport historique préservé.
Logs complets, temps, empreintes des fichiers de code/schémas effectivement testés
et plateforme : [validation.json](reports/001f/validation.json) et ses trois logs.
Cryptography existante utilisée pour la sauvegarde fictive ; aucun export réel.
Le validateur vérifie inventaire/contrats/exemples/liens/JSON et jetons usuels ;
la liste des contrôles documentaires finaux est dans reports/001f/checks.json.
Le contrôle whitespace complet signale uniquement trois sauts Markdown intentionnels
(deux espaces, lignes4–6) du cahier utilisateur conservé à l’identique ; hors ce
fichier il réussit. Cette exception documentaire ne concerne aucun test.

Audit API : sortie2, neuf refus documentés, **audit incomplet**. Pas un échec des80
tests ni une CI verte. Aucun gradle/adb/kotlinc dans PATH, aucun appareil attaché
utilisé ; builds/tests Android et matériel **non exécutés**. Aucun modèle installé
ou exécuté par cette mission. Le workflow UNIFIED est préparé mais non publié ni
exécuté sur GitHub. Sauvegarde/restauration isolée Git vérifiée séparément.

## 6. Roadmap et prochaines missions

[Feuille de route détaillée](docs/ROADMAP.md) : propriétaire, branche proposée,
dépendances, fichiers, critères testables, risques, accord humain et non-régression.

- **P0** : rétablir publication UNIFIED, obtenir décision ADR ; stabiliser CORE,
  qualifier LLM003B Redmi/POCO et VOICE005I Xiaomi ; diagnostiquer CI INTERFACE.
- **P1 après accord** : spécification/tests d’abord, puis missions distinctes CORE
  et LLM pour un parcours CORE→LLM→CORE réel, un seul modèle résident, annulation,
  identité, panne et mode local conservé. Installation/déploiement séparément autorisés.
- **P2** : VOICE, puis UI, NEXUS et SERVICES selon qualifications/dépendances ;
  conserver fonctions historiques jusqu’à parité prouvée/restauration.
- **P3** : EVOLUTION isolée après confirmation du dépôt ; mini-PC local qualifié,
  sauvegarde portable, Android autonome, aucun auto-déploiement de correctifs.

### Que faire dans chaque chat

| Chat | Prochaine responsabilité, à autoriser séparément |
|---|---|
| JARVIS-CENTRAL | Lire ce bilan, arbitrer ADR/nombre APK, ordonner missions et autorisations, garder décisions avec date/portée |
| CORE | Stabilisation tête actuelle, données/confirmations et orchestration ; préparer futur adaptateur après P0 |
| LLM | Moteur unique, mesures003B/protections/arrêt ; pas de seconde orchestration ni mémoire personnelle |
| VOICE | Synthèse/identité, essais005I locaux et archives privées ; ne pas envoyer audio ou profil au cloud |
| INTERFACE | Comprendre CI/UI autonome, préparer avatar2.5D sans prétendre qu’il est rendu ou relié |
| NEXUS | Spécifier Wikipedia/Kiwix, documents/index et stockage de mémoire confirmée sous décision CORE |
| EVOLUTION | Confirmer identité du dépôt ; sandbox et propositions de correctifs avec revue humaine |
| SERVICES | Définir outils optionnels, permissions et tests de refus avant connexion |

Les chats coordonnent le travail, ne constituent pas des preuves de code. À chaque
PR/fusion approuvée, actualiser SHA/date/portée, relire diff et préserver anciennes
preuves selon [runbook](docs/RUNBOOK.md). Pas de synchronisation automatique ChatGPT.

## 7. Risques et limites

Critiques : perte SQLite/profils, signatures et double modèle. Élevés : UID/certificat
IPC, réponse tardive, mort native, RAM/LMK, chauffe/batterie, anciennes API, mémoire
sans confirmation et régressions. Gouvernance : 403, CI inaccessible, preuves
périmées ou assimilées au matériel. [Gravité et portes](docs/RISQUES.md).
Aucune parade simplement documentaire n’est présentée comme implémentée.

## 8. Actions utilisateur nécessaires

1. GitHub Settings → Applications → Installed GitHub Apps → Configure l’intégration
   Codex/ChatGPT : autoriser JARVIS-UNIFIED ; vérifier permissions Contents et Pull
   requests en écriture. Si les droits de l’App ne sont pas modifiables, accepter
   sa mise à jour ou réautoriser l’intégration officielle ; ne pas inventer de case.
2. Réautoriser la connexion GitHub côté Codex/ChatGPT si nécessaire ; dans la
   configuration cloud ajouter api.github.com sans supprimer les domaines existants.
   Les deux problèmes (réseau API et droit Git) doivent être vérifiés séparément.
3. Garder/télécharger le bundle et son empreinte avant toute nouvelle session ;
   suivre les commandes de récupération/publication autorisée du runbook. Ni token
   dans le chat, ni SSH/proxy contourné, ni forçage.
4. Lire la page de décision et répondre explicitement pour l’ADR. Autoriser ensuite
   chaque mission proposée séparément ; aucune fusion ni installation n’est implicitement accordée.

## Fichiers et périmètre de clôture

Documents réutilisés : README, inventaire, preuves, matrice, roadmap, risques,
runbook, ADR. Nouveaux : ce bilan, note de décision, cahier001F exact et rapports
reports/001f. Registres source/modules/preuves actualisés ; mission001F ajoutée
sans écraser champs manuels préexistants ; captures antérieures archivées.
Aucun code applicatif, contrat, test, dépendance ou workflow UNIFIED modifié.
La synthèse précédente conserve sa date et ses limites historiques.
Liste exacte de cette clôture : reports/001f/changed-files.json. Branches001/002/003
et consolidation antérieure préservées ; aucune autre application modifiée.
