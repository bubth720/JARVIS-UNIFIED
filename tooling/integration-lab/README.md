# JARVIS INTEGRATION LAB — LAB-01

Outil de développement exécutable : vérification de huit dépôts épinglés, commandes de tests autorisées, compilations indépendantes, contrôle des APK M51, rapports et dashboard HTML autonome. Aucun moteur supplémentaire, connexion productive ou autorité CORE/LLM.

Base UNIFIED : `a7625a31513be5c56fa36ed946fbdcd3c23c2a15`. Branche : `codex/lab-01-complete-integration`. Les sources, contrats et preuves historiques sont préservés. Les sources des modules sont récupérées dans des clones isolés, sans worktree ni modification des dépôts d'origine.

## Lancer depuis Android

Voir [GUIDE-ANDROID.md](docs/GUIDE-ANDROID.md). Depuis GitHub Actions, ouvrir **JARVIS INTEGRATION LAB**, un run de cette branche, puis **Re-run all jobs**. C'est une nouvelle exécution SAFE du même code verrouillé ; aucune installation sur le téléphone. Le résultat du diagnostic peut être rouge si un test historique échoue : le rapport et les artefacts sont tout de même produits.

Le workflow déclare aussi workflow_dispatch. Actuellement main ne contient aucun workflow : le bouton Run workflow ne doit pas être promis avant sa disponibilité réelle. La relance Actions permet d'utiliser le LAB sans fusion ni modification de la branche par défaut. Le dashboard exporté est une vue statique, pas un déclencheur de build.

## CLI

Python3.12, bibliothèque standard pour le LAB. Git et les toolchains propres aux modules sont nécessaires pour leurs commandes. La dépendance cryptography existante concerne seulement la régression backup UNIFIED. Aucun modèle n'est requis ni téléchargé.

```sh
python3 tooling/integration-lab/lab.py status
python3 tooling/integration-lab/lab.py run --profile safe --output .audit-cache/lab-safe-01
python3 tooling/integration-lab/lab.py verify --archive .audit-cache/lab-safe-01/evidence.zip
python3 tooling/integration-lab/lab.py report --receipt .audit-cache/lab-safe-01/campaign.json --output .audit-cache/lab-report-replay
```

Toutes les fonctions annoncées sont reliées : `verify`, `audit`, `contracts`, `test`, `build` exécutent leurs phases avec vérification préalable des huit références ; `run` les enchaîne. `android --profile android_lab` construit le laboratoire M51 puis contrôle uniquement un émulateur **déjà disponible** avant la qualification. `report` et `dashboard` régénèrent les vues à partir du reçu ; `export` crée l'archive ; `compare --before … --after …` compare deux reçus sans modifier les modules. `status` lit le verrou ou le dernier reçu.

Exemple conditionnel, sur un laboratoire cloud autorisé disposant déjà d'un émulateur stable :

```sh
python3 tooling/integration-lab/lab.py android --profile android_lab --serial emulator-5554 --api 29 --output .audit-cache/lab-android-01
```

Sans émulateur admissible, le résultat est BLOCKED. Aucun boot automatique, retry, droit KVM, installation personnelle ou achat. Les campagnes Android M51-R1 défaillantes ne sont pas relancées.

`--source-root` réutilise exclusivement des clones isolés marqués par le LAB. `--offline` interdit leur récupération réseau et impose un Gradle déjà configuré pour les builds (`LAB_GRADLE_8_10_2`, `LAB_GRADLE_8_13`), lancé avec --offline. Un cache incomplet reste un blocage/échec documenté. Les sources originales et dossiers de sortie non vides sont refusés. `--resume` récupère un reçu après interruption sans rejouer une commande : une opération incomplète reste UNKNOWN.

Les versions Gradle ne sont pas harmonisées : NEXUS8.10.2 et les cibles8.13 restent distincts. `LAB_JAVA_HOME_17` / `LAB_JAVA_HOME_21` sélectionnent les JDK. Les tests Gradle sont forcés avec --rerun-tasks pour éviter d'annoncer des résultats périmés comme exécutés.

## Résultats et codes de sortie

Le reçu conserve les types UNIT, INTEGRATION, NATIVE, EMULATOR, PHYSICAL, STATIC et SIMULATION. Un test helper natif ne prouve ni JNI complet ni génération réelle. Une compilation ne prouve pas Android. Les mêmes cas rejoués sur deux variantes ne sont pas additionnés comme cas uniques.

Pour une campagne :0=PASS ;2=FAIL ;3=configuration/compatibilité invalide ;4=BLOCKED ou NOT_RUN ;5=UNKNOWN/interruption ;6=PARTIAL. Les opérations de lecture/rendu/export ont leur propre code d'opération, sans transformer le statut enregistré de la campagne. Un échec n'est jamais converti automatiquement en succès. Les autres modules continuent, sauf ceux concernés par un arrêt critique ou une modification de source.

Sorties : campaign.json atomique, report.json, REPORT.md, dashboard.html, logs, JUnit XML, APK contrôlées, inventaires binaires et evidence.zip avec SHA256SUMS et empreinte externe. Les artefacts GitHub sont conservés90jours : les télécharger avant expiration. Les poids, clés, profils vocaux privés et fichiers personnels sont exclus.

## Vérifier le LAB

```sh
python3 tooling/integration-lab/scripts/check_scope.py
python3 -m unittest discover -s tooling/integration-lab/tests -v
```

Les tests du LAB utilisent des fixtures explicites ; la campagne SAFE utilise les vrais dépôts verrouillés. [Architecture et couverture A–O](docs/ARCHITECTURE.md), [licences et dépendances](docs/DEPENDENCIES-LICENSES.md), [rollback](docs/ROLLBACK.md), [limites des adaptateurs](adapters/README.md). Les preuves finales de CI sont ajoutées dans docs/DELIVERY.md après observation ; aucun PASS n'est anticipé ici.
