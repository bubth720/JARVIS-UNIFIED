# RESEARCH N01-B0 — laboratoire synthétique isolé

Branche `codex/research-n01-b0-lab-20261118`, base UNIFIED `18344721`.
NEXUS reste intégralement à `5f101934` ; CORE, SERVICES et INTERFACE sont seulement
lus à leurs SHA d'audit. L'outil réside dans UNIFIED car il s'agit d'un banc de
test, pas d'un nouveau runtime ou d'un port réseau de production. Voir
[audit préalable et compatibilité](AUDIT.md), [architecture](ARCHITECTURE.md),
[politique et quotas](POLICY.md), [contrats expérimentaux](CONTRACTS.md) et
[risques / prochaine mission](RISKS-B1.md).

Python 3.12, bibliothèque standard, OpenSSL déjà installé pour les certificats
éphémères. Aucune dépendance Python nouvelle, aucun téléchargement au lancement.
La CA, les clés et les fichiers synthétiques sont générés en répertoires privés
temporaires. Aucun domaine ne fait l'objet d'une résolution DNS réelle.

```sh
python3 -m tooling.research_b0.demo
# DISABLED, network_started=false ; aucun socket ni certificat initialisé.
python3 -m tooling.research_b0.offline_runner --output /tmp/b0-results.json
python3 -m tooling.research_b0.demo --enable-lab --store /tmp/b0-private-new --profile android
python3 -m tooling.research_b0.check_preservation --run-v1-chain --output /tmp/b0-preservation.json --v1-log /tmp/b0-v1.log
```

Le runner impose une barrière d'audit de sockets/DNS dans son processus. La CI
exécute en plus les tests dans un namespace réseau Linux ne contenant que `lo`,
sans route extérieure, avec `--require-isolation`. La création de namespace est
interdite par `/proc/self/uid_map` sur l'environnement local de développement :
la preuve locale et la preuve CI sont distinctes, jamais substituées.

Les données sont fictives, y compris la date de provenance explicitement marquée
SIMULATED. Le seul hôte admissible est `lab.synthetic.test` associé, sans DNS, au
socket loopback possédé par la fixture et à son port éphémère exact. Même une
autre destination loopback est interdite. HTTPS conserve vérification de chaîne,
nom d'hôte/SNI et pair effectif. Aucun mode de transport Internet n'existe.

La mission couvre : scénarios HTTPS réels locaux, erreurs, transferts en flux,
redirections, liste blanche, quotas, arrêt/pause, reprise, cache et provenance.
Les imports NEXUS, transformations SERVICES et autorisations CORE restent des
frontières documentées ; aucun raccordement de production ne découle des tests.

Le nouveau workflow `research-b0.yml` teste B0, les 171 régressions UNIFIED,
la chaîne V1 complète et les régressions JVM REUSE sur le producteur épinglé.
Les CI NEXUS A3/NEX-07 sont vérifiées à ce même SHA inchangé ; leurs routes et
gardes ne sont pas étendus à une nouvelle branche NEXUS. La PR B0 UNIFIED est
maintenue en brouillon. Les résultats exacts seront fournis dans la livraison
datée avec liens de runs, logs, plateformes, SHA et limites de mesure.
