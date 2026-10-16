# DESIGN-004 — rapport de conception et limites

Module : UNIFIED ; dépôt exclusif : bubth720/JARVIS-UNIFIED.
Branche : **design-004-sync-expressions**.
Base vérifiée locale et origin : **41f53501fb18fe727d5fd453dd715f0811d2e897**,
mission-001g-maintenance, incluant ADR approuvée et correction du compteur16.
Le SHA documentaire final sera indiqué dans le compte rendu et se vérifie par
`git rev-parse design-004-sync-expressions` ; aucun SHA de son propre commit
inventé dans le présent fichier. main e4435f4 demeure inchangée par cette mission.

## Livrables

- [SYNC V1](SYNC_V1.md) : autonomie téléphone, montre légère, transport local
  proposé sous BRIDGE existant, consentements, deltas causaux, conflits,
  tombstones, interruptions/reprise, versions et séparation des mises à jour.
- [EXPRESSIONS V1](EXPRESSIONS_V1.md) : catalogue LLM003 existant, cible800
  formulations (plage600–1000), intentions et lots, sélection contextuelle future,
  cache dérivé privé facultatif dans VOICE avec invalidation et quotas.
- [Responsabilités et risques](RESPONSABILITES_ET_ADR.md) : frontières ADR et
  recouvrements réels SERVICES/NEXUS/CORE, catalogue et caches sans doublons.
- [Contrats proposés](CONTRATS_INTEGRATION_PROPOSES.md) : champs et sémantique de
  travail, erreurs, mapping des namespaces et tests futurs ; aucun schéma v1 changé.
- [Missions suivantes](MISSIONS_SUIVANTES.md) : autorisations bornées, propriétaires,
  dépendances, fichiers/livrables attendus, critères et non-régression.
- [Sources](SOURCES.md) : six dépôts GitHub acquis fraîchement, SHA exacts, vingt
  fichiers déterminants avec URL immuable et SHA256. README central lié aux livrables.

## Constats et réutilisation

Le catalogue SQLite003 est conservé dans LLM003B : huit DEMO et neuf variantes,
format JSON1 strict, FTS4, historique, tombstones et contrôles de révision. Il peut
accueillir des variantes de même sens ;600–1000 textes réels ne sont pas déjà créés.
Le contexte typé et le rendu de paramètres ne sont pas des fonctions existantes.

SERVICES contient maintenant du code Java partagé desktop/Android et les modules
DOCUMENTS/KNOWLEDGE/MEMORY/BRIDGE ; son Simulator echo et CoreAdapter en processus
ne constituent pas une connexion réelle. Son stockage mémoire n’a pas de journal
distribué/tombstones compatible SYNC. Réutiliser après adaptations, sans donner
l’autorité CORE à un deuxième orchestrateur ni déplacer la cible NEXUS implicitement.
VOICE005J contient Studio et primitives PCM/identité ;005K n’ajoute ici qu’un
cahier de mission. Aucun module bridge opérationnel déduit de son nom.
INTERFACE005 conserve son DataStore de layout local : pas de sync déjà implémentée.

L’ADR-001 reste **APPROUVÉE AVEC PRÉCISIONS** ; son texte et sa validation sont
inchangés. Les réserves sont signalées avant les propositions : transport,
identité/signatures, nombre d’APK, arbitre et migrations ne sont pas approuvés par
ce design. Aucun changement du choix architectural option3 proposé ou nécessaire
pour la conception dans ces limites. Déplacer réellement stockage/autorité ou
ouvrir le réseau nécessitera une décision technique et une autorisation distinctes.

## Vérifications réellement exécutées

Depuis UNIFIED, Python3.12.14 sous Linux :

| Commande | Résultat |
|---|---|
| python3 -m unittest discover -s tests -v | 27 réussis |
| python3 -m unittest discover -s registry/tests -v | 23 réussis |
| python3 -m unittest discover -s backup_prototype/tests -v | 30 réussis |
| python3 scripts/validate_unified.py | Réussi : neuf dépôts, cinq contrats/exemples ; liens/JSON/jetons usuels |
| python3 registry/scripts/update_registry.py --validate-only | Réussi : neuf dépôts et seize missions ; aucune entrée ni donnée changée |
| git diff --check et vérification indexée | Réussi pour les différences documentaires |

**80 tests existants exécutés,80 réussis, zéro échec et zéro saut.** Journaux complets,
commandes, durées et plateforme dans `.audit-cache/design-004/tests.json`,
audit-contracts.txt, registry.txt, backup.txt. Ces contrôles ne valident pas les
nouveaux protocoles ou performances : aucun runtime SYNC/EXPRESSIONS développé.
Les résultats finaux des contrôles documentaires et de périmètre sont conservés
dans `.audit-cache/design-004/final-checks.json`.

Aucun test/build Android des autres dépôts, aucune CI distante Actions observée,
aucun essai réel téléphone/PC/montre. Les rapports005J et déclarations005K ne sont
pas requalifiés en mesures physiques. Les bornes de transport/cache sont des
propositions à mesurer. Pas de chiffre de gain de latence ou d’autonomie inventé.

## Conservation et publication

Historique001/002/003/001F/ADR/001G conservé ; branche issue de la dernière livraison
vérifiée. Uniquement README et nouveaux Markdown sous docs/DESIGN-004 ; aucun code,
test, contrat v1, donnée ou profil modifié. Les snapshots sources antérieurs du
registre ne sont pas écrasés par cet audit ciblé. Aucun dépôt extérieur modifié.

La publication de cette branche documentaire, si effectuée, est vérifiée séparément
dans le reçu local `.audit-cache/design-004/delivery.json` et le compte rendu de
livraison. Le présent rapport ne vaut pas preuve de push/PR ou CI distante.
Aucune PR/fusion/main n’est nécessaire à cette conception ; aucune fusion effectuée.

## Blocages et décisions restantes

- Aucun transport réseau BRIDGE réel ou protocole SYNC qualifié ; plateforme montre
  et capacités exactes non fournies. Proposition de pairing/crypto à évaluer, pas clé
  ou permissions héritées des profils vocaux.
- Mapping de consentement inter-appareil, rétention/purge, causalité et journal
  transactionnel à spécifier/tester dans leurs propriétaires ; aucun effacement
  distant instantané ou reprise d’action sensible garanti offline.
- Conflit potentiel de propriété SERVICES/NEXUS/CORE et hébergement du catalogue :
  décision de réemploi avant toute extraction/migration, pas de nouvelle base.
- Schémas UNIFIED/LLM/SERVICES fermés et différents, aucune extension ajoutée ;
  quotas/performance/compatibilité SDK et budget montre non qualifiés.
- API GitHub absente de la politique réseau appliquée observée ; PR/Actions non
  vérifiées dans cette mission. Lecture des six dépôts Git réussie ; aucun obstacle
  pour livrer la documentation et ses références Git.

## Prochaine action

Autoriser séparément D4-01 (transport/identité/plateforme montre) et D4-02
(propriété/mapping de contrats), puis le petit pilote éditorial D4-03 dans LLM.
Coordonner tout futur travail VOICE avec005K pour éviter de refaire son pont.
Aucune de ces missions n’est lancée et l’orientation ADR n’est pas à revalider.
