# Suivi vérifié de la campagne intensive

`verified-state.json` est un instantané de preuves, pas un démarrage automatique
de missions. Les SHA et empreintes désignent les commits effectivement examinés.
Les champs BLOCKED conservent les décisions manuelles et les incréments partiels
publiés ; ils ne doivent pas être remplacés par une réussite de compilation.

Les reçus anciens sont normalisés dans `normalized-receipts` à partir de leurs
rapports Git, en conservant le SHA d'origine. Les résultats ne sont pas présentés
comme rejoués lors de la normalisation. SERV-01 n'avait pas de reçu JSON : son
rapport exact constitue la source, avec ses limites Android initiales conservées.

Depuis un environnement ayant les checkouts et commits correspondants :

```sh
python3 -m tooling.campaign.cli report --state registry/intensive-2026-10-22/verified-state.json --repository-paths /tmp/jarvis-campaign-paths.json --markdown
```

Le dernier argument est un fichier local JSON associant, par exemple,
`bubth720/JARVIS-UNIFIED` au chemin réel de son checkout. Aucun chemin local ou
secret n'est nécessaire dans le registre publié. Sans les objets Git nécessaires,
le programme refuse de vérifier : il ne suppose pas que le dépôt est absent.
Un fetch manuel en lecture peut être nécessaire avant vérification.

Pour actualiser : lire les rapports/reçus du commit publié exact, calculer leurs
SHA-256 sur les octets obtenus par `git show`, conserver les décisions manuelles,
puis exécuter le rapport. Une preuve partielle ou un dépôt non vérifié ne devient
pas DELIVERED. La vérification ne modifie ni les dépôts ni GitHub et ne reproduit
pas les tests ; natif Linux, Android simulé et appareil physique restent distincts.

Le bilan humain versionné accompagne cet instantané dans
[VERIFIED_STATUS.md](../../docs/intensive-2026-10-22/VERIFIED_STATUS.md).
