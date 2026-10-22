# Contrats : génération et vérification hors ligne

Depuis la racine, Python3.12 standard :

```sh
python3 -m tooling.contracts.cli generate
python3 -m tooling.contracts.cli verify-contract contracts/generated/manifest.json contracts/generated/manifest.json
python3 -m unittest discover -s tests/contract_tooling -v
```

Les cinq schémas `contracts/v1` restent inchangés et **proposés**. Les sorties
`contracts/generated` sont une référence JVM, pas une dépendance automatiquement
intégrée aux APK. Classes Java immuables, objets imbriqués et enums typés ; façades
Kotlin en lecture seule. Les parseurs refusent les clés dupliquées/inconnues,
UTF-8 invalide, nombres flottants, dépassements, JSON >65536octets/profondeur64.
Les règles sémantiques v1 (délais, voix, libération, état inconnu et corrélation)
complètent le sous-ensemble JSON Schema supporté. Tout autre mot-clé/type est refusé.

Les empreintes sont SHA-256 du JSON canonique UTF-8, clés ordonnées par points
Unicode, sans espaces ; tableaux conservés dans leur ordre, nombres entiers.
Pas de date de génération ou accès réseau. Reproduire les sources avant revue ;
ne jamais modifier les fichiers générés directement.

Comparaison : code0 COMPATIBLE seulement si tous les schémas sont identiques ;
code2 INCOMPATIBLE pour tout changement d'un contrat fermé ; code3 UNKNOWN pour
manifeste/version/digest invalide. Une compatibilité de types ne prouve pas un IPC,
une autorisation ou une qualification native. Ne distribuer que volontairement
après revue des modules consommateurs et de leurs SDK/versions.

Vérification réelle Java et Kotlin :

```sh
export JAVA_HOME=/chemin/jdk17
python3 -m tooling.contracts.verify_jvm
```

Configurer `kotlinc` dans PATH, ou `KOTLIN_COMPILER_CLASSPATH` (compilateur Kotlin
embeddable et dépendances locales) et `KOTLIN_STDLIB` (JAR standard). Le script ne
télécharge rien. Il compile dans un répertoire temporaire, exécute les cinq
exemples, leurs refus et les cas de sécurité, puis supprime uniquement ses propres
sorties temporaires. Sans toolchain, sortie non nulle et compilation non validée.
Les besoins de desugaring/packaging Android restent à qualifier séparément.
