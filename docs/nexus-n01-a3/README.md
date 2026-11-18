# N01-A3 — exception NEX-07 autorisée et qualification PR

18 novembre 2026, UTC. Module NEXUS, coordination des preuves dans UNIFIED.
Accord utilisateur : « Oui j'autorise », en réponse à la demande A2 portant
exclusivement sur le routage du workflow historique et son garde successeur.

Le commit NEXUS `5f10193440972ba25b30645d2811537418eface5`, sur
`codex/nexus-n01-a3-routing-20261118`, remplace la sélection erronée du garde
PRE-FUSION dans le contexte REUSE examiné. La [PR brouillon #16](https://github.com/bubth720/JARVIS-NEXUS/pull/16)
cible `codex/m53-readonly-preparation` à `eae61fb62a9ccd4073b96d71454f89e5a943eae9`.
Aucune fusion n'est demandée. La PR historique #14 et ses résultats demeurent
inchangés.

Le delta A3 contient six fichiers : un seul fichier historique modifié,
`.github/workflows/nex-07.yml`, et cinq ajouts exacts. Le garde successeur
préserve les 336 autres fichiers/modes de la base A2 à 337 fichiers. Tous les
scripts de garde historiques et les contrats sont identiques. Les routes M50,
LOT3 et PRE-FUSION ainsi que les commandes de compilation/test restent conservées.

Le contrôle relit l'événement GitHub : dépôt identique, base/ref/SHA épinglés,
deux noms de tête exacts autorisés et checkout au SHA réel de la PR. Il refuse
un fork, un déplacement de base, un autre nom de branche ou un merge artificiel.
Ce contrôle de source n'est pas une autorité CORE ni une permission de collecte.

Le garde REUSE ancien continue de refuser la modification du workflow à la tête
A3 : résultat attendu, conservé explicitement. Ses onze tests passent au SHA A2
original dans un clone jetable. Ils ne sont pas présentés comme une validation
de la tête A3 par l'ancien garde.

Preuves : [matrice de qualification](QUALIFICATION.md),
[risques et suite N01-B](RISKS-NEXT.md), fichiers sous `evidence/`.
La préparation [N01-B A2](../nexus-n01-a2/N01-B-SPEC.md) reste une spécification :
aucun moteur réseau n'est implémenté par cette correction.

UNIFIED ajoute uniquement ce dossier de preuves sur
`codex/nexus-n01-a3-evidence-20261118`. Les 519 fichiers/modes de `cfaa8260` sont
préservés, y compris les gardes A2. Le garde A2 conserve sa portée propre ;
aucune extension de ses listes n'est faite pour accepter le dossier A3.

Aucun runtime Android, modèle, contrat, migration, collecte réelle ou GPU payant
n'est activé. Les 430 fichiers/modes V1 INTERFACE sont vérifiés en lecture seule.
La V4 Nexus modulaire reste une mission d'interface distincte.
