# JARVIS — N01-A2 / architecture et préparation N01-B

17 novembre 2026. Livraison de revue et de tests hors ligne, sans collecte réelle, migration ou dépense GPU.

## Résultat

La séparation réseau est validée : RESEARCH possède les accès autorisés ; NEXUS et les outils de transformation restent locaux. Les contrats existants sont conservés. Les champs et statuts proposés incompatibles sont refusés par les vrais validateurs, sans nouvelle autorité ni adaptateur actif.

Le refus NEXUS REUSE est reproduit et expliqué par un mauvais contexte de garde dans NEX-07. Le workflow REUSE dédié est qualifié sur sa branche A2, sans modification de protection historique. **L’application du correctif au routage NEX-07 gelé est suspendue à l’accord explicite demandé par l’utilisateur.**

## Branches et sources

| Module | Branche | Référence |
|---|---|---|
| NEXUS — reproduction et régressions | `codex/nexus-n01-a2-ci-review-20261117` | Commit [2dd4447a](https://github.com/bubth720/JARVIS-NEXUS/commit/2dd4447acb592e9e63123c0377b6310d4dae2bf1), base REUSE `b7d9d884` |
| UNIFIED — A2 et préparation B | `codex/nexus-n01-a2-preparation-20261117` | Base `6539b444`, ajouts seulement sous ce dossier, `tooling/nexus_n01_a2/` et workflow A2. Le SHA livré et sa CI sont liés dans le compte rendu de livraison |
| INTERFACE — V4 validée | `codex/interface-v4-nexus-command-20261117` | G02 `d2e737a9`, aucun changement V4 appliqué pendant A2 |

CORE, SERVICES, INTERFACE et les `main` des dépôts ne sont pas modifiés. Aucun merge, déploiement, installation sur téléphone, changement de modèle ou de permission de production.

## Documents

- [Orientations validées](ARCHITECTURE-VALIDEE.md), avec correction du placement ambigu du worker réseau dans N01-A.
- [Compatibilité des contrats](CONTRACT-COMPATIBILITY.md) : conservés/compatibles en syntaxe/rejetés et adaptations nécessaires.
- [Diagnostic et état CI NEXUS](NEXUS-CI-DIAGNOSIS.md).
- [Spécification N01-B](N01-B-SPEC.md) : liste blanche, permissions, DNS/IP/redirections, quotas, arrêt/reprise et fonctionnement hors ligne.
- [Proposition de delta non appliquée](patches/nex07-routing-proposal.patch) : le garde successeur reste un préalable à valider, ce patch n’est pas autonome.
- [Empreintes des cinq sources](evidence/five-repository-source-check.json), [CI NEXUS](evidence/nexus-ci-summary.json).

## Fichiers nouveaux / modifiés

NEXUS : `.github/workflows/reuse-r1plus.yml` (déclenchement A2 et régressions), `reuse-r1plus/n01-a2/README.md` et son test de contexte. Aucun ancien garde modifié.

UNIFIED : ce dossier documentaire et ses preuves, un oracle de revue sans client réseau, tests des schémas réellement existants et tests réseau négatifs sans socket, contrôles de préservation/source et workflow CI dédié. Aucun des 503 fichiers historiques n’est modifié ; contrats, registres et G03 restent identiques.

## Vérifications et limites

- NEXUS CI [44181266121](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44181266121) : SUCCESS, 108 JVM + 11 garde + 10 Python historiques ; 329 fichiers M53 préservés. [Artefact JUnit et provenance](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/44181266121/artifacts/14371627816).
- UNIFIED local : validateur, 117 tests existants et 54 nouveaux tests de revue. NEXUS local : 11 garde et 10 Python historiques. Rejouer via les commandes ci-dessous ; les logs de la livraison précisent plateforme, SHA, totaux et éventuels blocages.
- Un exemple négatif d’URL avec identifiants fictifs a d’abord été refusé par le scanner statique de secrets. La fixture est maintenant construite structurellement ; le validateur historique est inchangé et le cas de refus d’URL reste testé.
- JVM local bloqué avant exécution sur la résolution de `services.gradle.org` ; résultat CI JVM Java17 distinct. Aucun contournement de proxy/TLS.
- Les tests de revue réseau n’effectuent ni DNS ni HTTP et ne prouvent pas TLS/pair réel, révocation CORE ou HTTP de bout en bout. Le résultat de l’oracle n’autorise jamais de transport.
- Le contexte PRE-FUSION sur REUSE reste un refus attendu, pas un succès forcé. Android/LLM/énergie et moteur RESEARCH de production : non exécutés.

## Reproduction

```sh
python3 -m tooling.nexus_n01_a2.review --local-workspace /workspace
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tooling/nexus_n01_a2/tests -v
PYTHONDONTWRITEBYTECODE=1 python3 -m tooling.nexus_n01_a2.check_local --output /tmp/n01-a2-checks --workspace /workspace
```

Le contrôle des cinq sources exige les checkouts épinglés décrits dans le manifeste. La CI les reçoit en lecture seule. Les outils A2 n’ont que des dépendances standard Python ; `cryptography==50.0.0` est la dépendance historique des seuls tests backup.

## Accord restant et prochaine mission

Pour corriger le routage dans le fichier NEX-07 gelé, demander l’accord sur **ce seul delta et un garde successeur**, les autres fichiers M53, leurs modes et tous les gardes historiques restant inchangés. Les tests prouvent qu’une édition du workflow est actuellement refusée ; aucune exception n’est activée.

Après cet accord : finaliser et tester le garde successeur, appliquer le delta exact sur branche de développement et requalifier le contexte PR NEXUS. Le prototype N01-B de transport réel et ses serveurs de test contrôlés constituent ensuite un incrément distinct ; aucune collecte Internet n’est lancée par cette préparation.
