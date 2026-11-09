# Exécutions et reproduction

Les sources ci-dessous sont les sources effectivement testées, pas des branches productives mises à jour automatiquement. JAVA/JVM, Python, émulation et matériel restent des couches distinctes.

| Source / environnement | Commandes ou suite réutilisée | Résultat observé |
| --- | --- | --- |
| CORE 5da9838, CI JDK17 | tests/m50_s1 ; integration-lab test run ; app testDebugUnitTest et testMvp2UnitTest ciblé Mvp/MemoryLabUiTest ; p2-client testDebugUnitTest | 20 Python PASS ; 641 exécutions JVM/Robolectric PASS, 0 erreur/saut |
| VOICE 642d9c1, CI JDK17 | Suites voiceFusion02, voiceFinalSdk/Runtime, voice04Runtime, voiceSdk, studio/expression/identity/pocketRuntime, bridgeContract/Harness, app et voiceBridgePilot | 260 exécutions JVM : 237 PASS, 23 SKIP, 0 erreur ; pas de voix réelle qualifiée |
| SERVICES 8d80d09, CI JDK21 | `./gradlew :desktop:test --rerun-tasks` | 134 PASS, 0 FAIL/ERROR/SKIP |
| EVOLUTION 84ebc2e, CI JDK17 | `./gradlew test :evolution-cli:installDist --rerun-tasks` et trois scripts check_demo/check_diagnostic_demo/check_proposal_policy_demo | 40 JVM PASS ; démos PASS ; runner NOT_RUN/sandbox NOT_QUALIFIED |
| LLM 08fbda5, local Java21 et jars épinglés | `python m51review/check.py` ; `python m51review/run_audit.py --jdk /usr/lib/jvm/java-21-openjdk-amd64 --cache /workspace/JARVIS-REUSE-R1plus/compiler-cache` | 247 hérités + 12 audit PASS ; NO_GO ; patch non appliqué ; Android/poids/JNI/génération NOT_RUN |
| Avatar M54 2397bf2, local Java21 | `python m54-avatar/run_review.py --jdk /usr/lib/jvm/java-21-openjdk-amd64 --cache /workspace/JARVIS-REUSE-R1plus/compiler-cache` sur clone détaché de cette source | 21 JVM + 20 Python PASS ; Android/audio NOT_RUN, aucun renderer activé |
| NEXUS b7d9d88, CI JVM et SQLite réel | `./gradlew -I reuse-r1plus/init.gradle :nexus-jvm-store:test :nexus-core:test` ; `python -m unittest discover -s tests/final -v` | 108 JVM + 10 Python PASS ; sources historiques figées, test-only, base temporaire CC0 |
| INTERFACE d569ce8, CI JVM/build | commande Gradle exacte dans `.github/workflows/reuse-r1plus.yml` ; `python -m unittest discover -s m51 -v` | 36 JVM + 36 Python PASS ; quatre APK et lint PASS ; devices SKIP |
| INTERFACE 7282fd7, campagne C1 | Préflight puis régressions, un boot par API | API29 : préflight brut contredit par ANR, 1 SAF FAIL ; suites/candidat NOT_RUN. API35 : ANR système avant JARVIS, app NOT_RUN. Android BLOCKED |
| M50-S1B b9a6c19, historique récupéré | Rapports/API29 et API35 du run 41839854603, APK re-hashé pendant cette mission | 6 instrumentés PASS/API dans le labo synthétique CORE/UI ; pas de nouveau test Android ni LLM |

## UNIFIED, validation locale du dossier et des acquis

Python 3.12.14, cryptography déjà disponible. `PYTHONDONTWRITEBYTECODE=1` pour toutes les commandes :

```sh
python scripts/validate_unified.py
python -m unittest discover -s tests -v
python -m unittest discover -s registry/tests -v
python -m unittest discover -s backup_prototype/tests -v
python -m unittest discover -s tooling/campaign/tests -v
python -m unittest discover -s tooling/integration/tests -v
python -m unittest discover -s tooling/v1/tests -v
python -m tooling.v1.validate
python -m tooling.v1.reception
python -m tooling.reuse_r1plus.verify
python -m unittest discover -s tooling/reuse_r1plus/tests -v
```

Suites historiques : 41 + 23 + 30 + 32 + 21 + 51 = **198 tests Python PASS**. Neuf nouveaux tests de réception documentaire refusent les promotions indues d'un build APK, des tests LLM NO_GO ou des SKIP VOICE, les mauvaises sources et l'acceptation du préflight contradictoire. Le contrôle de préservation fige les 397 fichiers historiques UNIFIED, octets et modes ; seules les nouvelles preuves/tooling/CI sont autorisées.

Une première validation des liens a signalé ce fichier TESTS.md encore absent pendant la préparation ; le lien a été concrétisé puis le validateur relancé, sans modifier le validateur historique. Les autres suites avaient passé. La CI documentaire rejoue les suites sans dépendance externe ; la suite sauvegarde/cryptography est qualifiée localement, sans installation de cette dépendance en CI. L'ancien `tooling.v1.check_scope` au périmètre V1 exact n'est pas assoupli ni exécuté comme si les ajouts de cette mission appartenaient à sa preuve ancienne. Les validateurs V1 gardent score 0 et autorité false.

## CI et anomalies conservées

- Baselines fraîches des quatre modules : [42524692747 SUCCESS](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42524692747), commit coordinateur 9365e80 et sources producteurs épinglées.
- NEXUS nouveau laboratoire : [42523712059 SUCCESS](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42523712059).
- NEXUS ancien NEX-07 : [42523863724 FAILURE](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/42523863724), deux jobs refusent les ajouts au garde de périmètre avant les tests. Ni échec du moteur SQLite ni succès caché ; log du refus conservé.
- INTERFACE après correctif : [42526118449 SUCCESS](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42526118449), build/tests hôte, devices SKIP. CI Android historique également SUCCESS au même commit.
- Campagne Android C1 : [42524234101 FAILURE](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42524234101), preuves brutes et revue séparées ; jamais relancée.

Les logs locaux, XML réels, manifests d'artefacts, captures et bundles sont conservés dans la livraison récupérable. Les limites du corpus, de l'émulation et du microbenchmark figurent dans les rapports liés ; aucune métrique théorique n'est présentée comme mesurée.

La première CI documentaire [42569947051](https://github.com/bubth720/JARVIS-UNIFIED/actions/runs/42569947051) a passé les 168 tests historiques sans dépendance puis refusé son propre fichier build/reuse-r1plus-coordination/results.log comme ajout non déclaré. Correction du workflow : sorties dans runner.temp, sans élargir le garde ni modifier un source historique. La vérification finale utilise le nouveau commit et conserve ce premier échec.
