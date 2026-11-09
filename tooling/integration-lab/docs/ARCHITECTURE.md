# Architecture, réutilisations et couverture LAB-A à LAB-O

Le LAB vit exclusivement dans UNIFIED/tooling/integration-lab. Il ne fait partie d'aucun APK. ADR-001 est inchangée ; aucun troisième moteur, mandat, racine ou connexion productive. La CLI orchestre des tâches de développement explicitement autorisées, sur huit clones indépendants.

Réutilisations : liste des dépôts de tooling.integration.lock ; JSON strict et comparaison de manifestes de tooling.contracts ; schémas et validations sémantiques scripts.contracts ; suites historiques UNIFIED ; initialisation Gradle et collecteur APK M51 ; matrice d'incidents SystemUI M51-R1 ; helper C++ PERF03 sans modèle ; tests SQLite NEXUS et module JVM M53. Aucun garde historique n'est modifié.

| Lot | Réalisation | Limite conservée |
|---|---|---|
| A | modules.lock.json, empreinte du verrou, commits/trees et préimages, clones isolés | références indisponibles bloquées ; aucune mise à jour silencieuse |
| B | faits avec sources SHA256, matrice56liens de toolchain | UNKNOWN reste inconnu ; ne prouve pas le runtime |
| C | liste de commandes versionnée, processus bornés, refus des commandes arbitraires | pas de génération réelle ni de modèle |
| D | versions Gradle séparées, JDK adaptés, tests forcés, inventaires et logs | pas de composite build implicite |
| E | schémas historiques validés, comparaison des copies VOICE, matrice8relations | égalité de schémas n'est pas un adaptateur activé |
| F | préflight ADB/API/ABI/ressources/SystemUI, qualification M51 conditionnelle | aucun boot automatique ni appareil personnel |
| G | vrai build M51 baseline/candidat/testAPK et vérificateur historique réutilisé | APK non qualifiées avant réception Android |
| H | journal atomique, reçus exacts, logs/JUnit, SHA256 et ZIP vérifié | aucun fichier privé ou poids exporté |
| I | HTML autonome avec huit vues, données réelles, CSP sans scripts/réseau | page statique, aucun bouton build fictif |
| J | Actions tests du LAB + campagne SAFE, rapports même après FAIL | main sans workflow ; guide de relance Actions explicite |
| K | toutes les sous-commandes reliées et codes de sortie distincts | reprise sans rejouer une opération incertaine |
| L | chaque fichier suivi comparé aux blobs, préimages et modes ; baseline UNIFIED gelée | les filtres de checkout déclarés sont respectés |
| M | comparaison de reçus/module/états, recommandations conservatrices | pas de gain/performance sans campagnes comparables |
| N | structure et dossier d'adaptateurs, sondes de schémas en lecture | API sensibles et applications historiques inchangées |
| O | tests positifs/adversariaux et campagnes sur les vrais dépôts | tests du LAB distincts d'une qualification matérielle |

## Exécution et erreurs

Le verrou versionné contient huit identités exactes et runtime_enabled=false. Les commandes viennent uniquement de core/policy.py. Les branches servent à l'identification ; la récupération utilise le SHA complet. Les fichiers sont vérifiés contre le commit, indépendamment de l'index Git mutable, avant et après les commandes. Les fichiers générés restent dans les clones et les résultats ignorés .audit-cache ; aucun git clean/reset, migration ou restauration automatique.

Chaque sous-processus possède un groupe ; timeout, signal ou dépassement de log entraînent arrêt et conservation du résultat. Aucun retry automatique. Les échecs de dépendance et de test restent visibles, les modules indépendants continuent. Les secrets nommés dans l'environnement sont retirés avant les commandes de module, les paramètres sensibles ne sont jamais demandés.

Le rapport final ne remplace pas le statut de la campagne : une campagne peut produire son dashboard et son export tout en renvoyant FAIL. Les copies de preuves sont toujours liées au SHA du LAB, au verrou et aux SHA/trees des modules. Un développement local non commité conserve lab_dirty=true et les empreintes de ses fichiers ; seule une campagne au commit publié prouve cette version publiée.

## Android

Priorité à un émulateur déjà disponible, pas de relance des bancs M51-R1 en échec. Série emulator-NNNN plus qemu=1 obligatoires ; API29/35 x86_64 uniquement pour le cockpit actuel.13relevés SystemUI espacés de5s, budget mural120s, arrêt immédiat après incident. Les logs de démarrage ne sont pas effacés. Le banc original contrôle ensuite géométrie, mode avion, Wi-Fi, paquets testOnly,18baseline/24candidat, persistance et fenêtres de frames. Les observations hôte ne sont jamais présentées comme LLM physique ARM64.

Android Test Orchestrator n'est pas activé : il requiert une dépendance/test runner et un banc compatibles, non démontrés actuellement. Les cas M51 historiques et leurs assertions restent inchangés. Le cloisonnement des processus du banc existant est conservé ; un orchestrateur ne servirait pas à masquer un crash de production.

## Gates

JNI protégé, LAB_CLOUD, racine opérateur, mandats CORE/LLM, modèles, données personnelles, appareil privé, fusion et activation productive sont fermés. Un statut PASS du LAB n'ouvre aucune de ces gates. Les propositions sensibles existantes conservent leurs empreintes et leur avis NO_GO.
