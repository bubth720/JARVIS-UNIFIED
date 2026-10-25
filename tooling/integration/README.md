# FUSION-01 — outillage de composition candidate

Python standard, hors runtime. Réutilise le parseur strict et le validateur des
contrats UNI-01, et les lecteurs de preuve UNI-02 ; aucun moteur ou orchestrateur.

```sh
python3 -m tooling.integration.cli validate
python3 -m tooling.integration.cli validate --repositories /chemin/local/repositories.json
python3 -m tooling.integration.cli report
python3 -m tooling.integration.cli plan
python3 -m tooling.integration.cli compare --against /chemin/autre-candidat.json
python3 -m tooling.integration.cli proposals
python3 -m unittest discover -s tooling/integration/tests -v
```

Le fichier local de chemins est un objet JSON `nom GitHub exact -> chemin Git`,
avec les huit dépôts du verrou. Un checkout ou bare snapshot suffit ; ne pas
versionner les chemins privés de l'utilisateur. Tous les objets SHA et leurs
parents doivent déjà être disponibles. Le programme ne clone/fetch/checkoute pas
et interdit les transports et fetch paresseux Git. Il ne lance ni code, ni build,
ni tests des dépôts inspectés. Il ne pousse et ne fusionne rien.

Sans `--repositories`, `validate` ne vérifie que structure et cohérence :
`mode:structure_only`, **pas une revérification de sources**. Avec les huit chemins,
il relit les octets Git exacts des fichiers réguliers (jamais une substitution du
worktree), contrôle parents/SHA-256 et les cinq schémas gelés actuels. Le rapport
reprend des états déclarés datés ; un résultat de validation du verrou n'est pas
un GO runtime. `plan` affiche dépendances et blocages sans les lever, sans agent
et sans commande à exécuter. `compare` rend les changements de SHA/observations
CI ; il n'accepte ni ne migre une nouvelle composition.

Admission : JSON <=2 Mio, pas de clés dupliquées/NaN/Unicode invalide ; schéma fermé
`jarvis.integration-lock/1`, exactement huit propriétaires et une référence primaire
par module, SHA complets, cinq plateformes, F0-F8 sans cycle, chemins relatifs sûrs,
preuves <=2 Mio. Les CI connues doivent viser le SHA sélectionné et une URL Actions
du dépôt exact. Une CI d'un parent documentaire ne devient pas celle du HEAD.
Un conflit ou prérequis manquant interdit un état intégré VERIFIED ; F0 vérifie
l'inventaire, jamais une intégration. Les licences inconnues restent UNKNOWN.

Limites de confiance : un hash lie des octets, pas une identité distante ; Git
local et les observations CI datées ne sont pas une attestation matérielle. Le
verrou n'est pas signé et se révise par diff/PR humaine. La réussite logicielle,
le rendu audio, la fin JNI et l'autorisation d'exécution sont des preuves distinctes.
Le schéma technique F7 est **une proposition non approuvée**, contrôlée hors ligne,
non déployée, sans permission ni transport. Aucun schéma `contracts/v1` modifié.
