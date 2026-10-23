# UNI-02 — registre exécutable de dépendances et de preuves

Module UNIFIED, dépôt `bubth720/JARVIS-UNIFIED`, branche `feat/uni-02-tooling`.
Base livrée UNI-01 `bd283dad3a57effa276f7f4441901839d2834d5c` (inclut le code initial
`d947dadf73f8dec91543a3f86a1aa2ffef0b0d2f` et sa revue), référence campagne
`ef1592e9598e14d2245539e2453bf26d7f26969d`. Le commit contenant ce rapport donne
le SHA final consultable par `git log -1` ; aucune fusion dans main.

Code créé : `tooling/campaign/{manifest,dag,ownership,status,cli}.py`, tests et
guide. Parsing strict des31missions, tri topologique, détection des cycles et
conflits de dépôt/branche, états avec preuves Git locales, conservation des
blocages/décisions manuels, rendu JSON/Markdown et commandes list-ready,
list-blocked, explain-mission, export-wave. Aucune génération de processus agent,
mutation Git, connexion réseau, exécution de patch ou orchestration applicative.

Vérifications Linux réellement exécutées le23octobre2026 : suite dédiée29tests
réussis, zéro échec/erreur/saut ; vrai dépôt Git synthétique temporaire vérifiant
les SHA, rapports, reçus et filiations, y compris base documentaire et base non
documentaire refusée. Tests de cycles, dépendances absentes, collision ownership,
branches dangereuses, refus sensible, livraison sans preuve, mauvais digest,
échecs/sauts, fausse qualification physique, absence d'accès, stabilité sans
mutation et cinq commandes CLI hors ligne.

Les cinq schémas v1 et le manifeste de planification historique sont inchangés.
La suite historique reste exécutée séparément. Les essais temporaires ne sont
jamais comptés comme livraisons CORE ou LLM. Les preuves des autres dépôts doivent
être reçues, versionnées et vérifiées avant que la CLI les annonce DELIVERED ;
un compte rendu libre ne suffit pas. Le reçu n'est pas une attestation matérielle.

Prochaine action : enregistrer progressivement les preuves réelles de campagne,
débloquer les seuls ports livrés et conserver les gates JNI/Binder/données.

La revue indépendante a reproduit puis fait corriger : affectation d'une mission
à un mauvais dépôt/ID remplacé, composant de branche Git invalide et transition
DELIVERED depuis une branche sœur sans le commit dépendant. La validation du
nouvel état intervient maintenant avant toute mutation ; un test vérifie son
absence d'effet après refus. Un reçu PARTIAL ne débloque aucune dépendance.

Non-régression :41 tests audit/contrats/outillage,23 registre,30 sauvegarde et
27 campagne initialement passés, puis29 campagne après ajout des reçus centraux.
Cela représente123 tests Python distincts, sans échec/erreur/saut. Le générateur
UNI-01 a en plus été compilé/exécuté sur45 vérifications Java et5 Kotlin. Le
validateur UNIFIED passe ; aucune modification des contrats v1, de leur ancien
validateur ou du manifeste de planification.

Les quatre fondations anciennes SERV-01/AVA-01/NEX-01/EVOL-01 sont normalisées
dans le registre central à partir de leurs rapports Git exacts : aucune branche
module réécrite, aucune commande ni compte inventé, aucune nouvelle exécution
attribuée à ces traductions. Le reçu central et le rapport d'origine sont liés
par dépôt/SHA/empreinte, avec vérification de filiation et refus d'un autre
émetteur. Deux tests couvrent ces liens et les falsifications. Les limites
Android/instrumentation initiales restent conservées.
