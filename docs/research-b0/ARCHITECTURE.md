# Architecture du laboratoire

Le superviseur de test `LabResearch` simule les décisions d'un hôte CORE : opt-in,
permis RAM liés au plan exact, expiration, génération, pause/annulation et nouvelle
admission à chaque tentative. Il ne prétend pas authentifier le vrai CORE.
`LabPermit` n'est pas accepté depuis JSON : une copie/instance forgée n'appartient
pas au registre du contrôleur. Rien n'est persisté comme permission.

La partie RESEARCH du banc suit : plan immuable → permis de test → politique
exacte → réponses de résolution injectées revérifiées → socket IP épinglée →
TLS validé → pair vérifié → en-têtes bornés → flux borné → SHA et type vérifiés
→ publication locale de laboratoire. Chaque redirection refait ces contrôles,
sans héritage de cookies, credentials ou connexion. Aucun contenu n'est interprété
comme commande ou comme nouvelle URL à ouvrir.

Le serveur `SyntheticServer` ne bind que `127.0.0.1:0`. Ses routes fournissent
document valide, 503, attente, connexion persistante, corps tronqué, interruption,
corruption, texte invalide, redirection relative/externe/privée/cyclique, taille
annoncée excessive, compression/chunked refusés, surplus et en-têtes excessifs.
Toutes les données sont créées dans le code de fixture.

`Ledger` ouvre exclusivement un dossier marqué B0 neuf ou déjà possédé, avec
verrou OS exclusif, SQLite transactionnel et permissions privées. Compteurs de
requêtes/octets et limites sont persistés avant poursuite. Les octets rejetés
restent facturés au budget ; la lecture de dépassement est bornée à un octet.
Une reprise ne remet pas les quotas à zéro et refuse un changement des limites.
L'âge de mission couvre les pauses ; un recul d'horloge détecté refuse.

La pause/annulation révoque les permis, annule les tâches, ferme les sockets,
attend leur fin observée et retire les `.part`. La reprise redémarre le document
depuis zéro, avec nouveau permis et quota restant ; aucun Range/ETag n'est
simulé comme sûr. Un autre processus ne récupère qu'après libération du verrou
du précédent. Les parties reconnues sont alors nettoyées ; ni original ni objet
validé n'est écrasé. Le test de crash interprocessus prépare un état de fichier
partiel puis quitte brutalement ; le test de pause utilise un vrai transfert TLS.

Les objets sont adressés par SHA, publiés sans écrasement, et les documents
identifiés par le digest du plan. Une reprise d'un document déjà commis relit
hash/métadonnées sans nouvelle requête. Deux sources partageant les mêmes octets
gardent des notices distinctes et un objet partagé. Les manifestes décrivent une
copie identité ; aucune normalisation ou indexation NEXUS n'est effectuée.

Les transferts sont asynchrones. Les écritures locales/transactions et la phase
finale sont synchrones, bornées, dans ce worker de test sans UI Android. La
publication n'a aucun point de suspension entre revalidation et commit. Une
demande d'arrêt arrivée après commit ne promet pas son rollback. Cette stratégie
ne qualifie pas le stockage Android ou une annulation de processus de production.

Quand le quota de journal est plein, une nouvelle admission est refusée. L'arrêt
reste toujours possible : le dernier état est durable dans la ligne de mission,
même si aucun événement supplémentaire ne tient dans le quota. Stop renvoie la
fin observée et le nombre de documents préservés ; un arrêt après commit conserve
COMPLETED, sans annoncer une annulation rétroactive.
