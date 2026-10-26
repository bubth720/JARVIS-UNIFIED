# U5 — réception, reproduction et retour arrière

## Reproduction hors ligne UNIFIED

Avec Python3 et la dépendance de sauvegarde existante installée, exécuter :

```sh
python3 -m tooling.integration.ci --output /tmp/fusion02-checks
python3 -m tooling.integration.cli_v2 validate
python3 -m tooling.integration.cli_v2 compare
python3 -m tooling.integration.cli_v2 assess
python3 -m tooling.integration.check_v2_contracts
```

Pour revérifier les objets source, préparer séparément les huit snapshots Git
aux références épinglées et une map JSON locale `repository -> chemin Git` ; puis
ajouter `--repositories /chemin/map.json` à `cli_v2 validate`. Aucun fetch n'est
fait par le validateur. Il relit 26 références/238 fichiers et cinq schémas v1.
Les branches candidates/parents/preuves datées sont dans PROVENANCE et evidence.
Les journaux de tests ne contiennent que fixtures techniques synthétiques.

Comparer le rapport généré à RELEASE_MATRIX.md et le diff à COMPARISON.json.
Ces sorties sont déterministes pour les mêmes octets ; aucun `READY` n'est
écrit automatiquement. Une nouvelle preuve nécessite une revue du verrou et
un commit, pas une mutation des résultats historiques FUSION-01.

## Réception Android future — NOT_RUN dans UNIFIED

| Scénarios | Preuve requise par API24 et API25 |
|---|---|
| A/J | Mode avion ; LLM/VOICE absents, outils locaux utilisables sans réponse IA fictive |
| B/C | SAF choisi, vraie requête/citation/relecture/provenance et fermeture ; probe FTS5 réel, pas seulement compile_options |
| D | CSV décimal exact0.10+0.20=0.30, aperçu/confirmation/destination neuve et digest relecture |
| E/F | DOCX sans consentement aucun effet ; confirmé SAF ACK+readback ou UNKNOWN |
| G/H | Tests à barrières de révocation avant/après engagement, kill/ACK perdu et reçu durable sans retry |
| I | Rotation/reprise/API et ressources bornées, sans hausse de minSdk ni permissions |

Les modules producteurs doivent livrer leur instrumentation et SHA exacts ;
CORE doit ensuite produire les dix scénarios E2E sur chaque API. JVM_PASS ne vaut
pas ANDROID_EMULATOR_PASS ; API26 ne couvre pas24/25. ANDROID_DEVICE_PASS nécessite
un essai physique séparément autorisé. Le GO documentaire ne l'autorise pas.
La licence/provenance/ABI des actifs est à qualifier avant distribution.

## Rollback non destructif

Les anciens fichiers integration-lock.json, contrats/v1, rapports et branches
restent intacts. Revenir au SHA précédent pour l'outillage UNIFIED ne nécessite
aucune migration ou restauration utilisateur : aucun runtime/donnée n'a changé.
Ne pas faire reset/purge de journaux, écrasement de fichiers, downgrade de base
v4 ni installation remplaçant une application existante. Les futures migrations
seront testées sur copies synthétiques et précédées de sauvegardes/restaurations
vérifiées, sur autorisation distincte.

## Séquence après réception de cette tranche

1. NEXUS : sonde FTS5 instrumentée24/25 et choix backend ; bibliothèque native
   supplémentaire seulement après revue licence/ABI/budget et autorisation.
2. SERVICES : contrat fence CORE + worker, puis vrai SAF et tests concurrents ;
   laisser DOCX_UNQUALIFIED tant que non démontré, corriger sa CI dans son dépôt.
3. CORE C0/refus en parallèle, C1 composé seulement après réception N/S ;
   recompilation des consommateurs et validation au vrai SessionCoordinator.
4. CI/émulateurs/API26/35, rapport F8 ; installation personnelle/distribution/merge
   réclament un accord précis. Lanes L/V/I/E indépendantes conservées, désactivées.
