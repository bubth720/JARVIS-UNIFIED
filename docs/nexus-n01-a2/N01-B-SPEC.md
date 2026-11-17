# N01-B — spécification préparée du moteur RESEARCH

Statut : **préparation A2, aucun moteur RESEARCH ou collecte réelle lancé**.

## Frontière et activation

RESEARCH est le seul propriétaire des requêtes HTTP/DNS vers les sources autorisées. NEXUS, les transformations SERVICES, la mémoire CORE et l’UI restent locaux. L’APK principale conserve l’absence de permission Internet. Une dépendance, un service ou un canal IPC nouveau n’est pas ajouté par cette spécification.

L’état initial est hors ligne, sans source autorisée, sans grant ni job automatique. Aucune liste de domaines réels n’est approuvée dans cette livraison. Les domaines `.test` et adresses présents dans les tests sont des fixtures ; aucun paquet ne leur est envoyé.

Le composant RESEARCH pourra être placé dans un processus/paquet séparé sur Android et dans un worker isolé sur mini-PC. L’emplacement concret, l’authentification et le transport doivent être qualifiés avant raccordement. Le modèle LLM actuel ne change pas ; aucun autre réseau neuronal ou GPU n’est nécessaire à ce lot.

## Modèle de permissions proposé

| Objet | Contenu / contrôle |
|---|---|
| Politique de source | ID/révision, hôte canonique exact, sous-domaines explicitement admis ou non, schéma/port, endpoints autorisés, conditions d’usage, débit et licence attendue |
| Plan de mission | Finalité, politique exacte, objets attendus, limites cumulées, durée, rétention et destination locale ; digest affiché pour revue |
| Autorité | Référence émise/résolue par CORE, liée à la session, génération, plan, politique, expiration, état d’annulation et portée d’écriture. Jamais créée par le payload |
| Permission de lecture locale | Collections/sources précises ; aucune expansion vers une URL trouvée dans le contenu |
| Publication RAW | Admission distincte et vérifiée : destination locale opaque, taille/hash/licence, quota et absence d’annulation au point de publication |
| Export/suppression | Décision exacte séparée ; destination et contenu affichés. L’accès au réseau n’autorise ni export ni effacement |

Un changement du plan, de la politique, de la portée ou de la destination exige une nouvelle revue. Toute reprise vérifie de nouveau l’autorité ; un checkpoint ou un fichier ne la porte pas. Les preuves UID/certificat/capacité doivent provenir du canal de confiance choisi, pas de champs JSON auto-déclarés.

## Validation des URL et connexions

1. Parser sans interprétations divergentes. Le pilote proposé accepte HTTPS/443 uniquement, hôtes ASCII canoniques examinés, sans identifiants, fragment, contrôle, espace, backslash ou encodage dans le nom d’hôte. Les IDN doivent être soumis à une revue explicite de leur A-label ; pas de normalisation Unicode silencieuse. Pas d’IP littérale, schéma local, proxy ou tunnel implicite.
2. Comparer l’hôte exact, puis éventuellement le suffixe avec frontière `.` si la politique permet les sous-domaines. Pas de wildcard global, correspondance par sous-chaîne ou élargissement à un domaine parent/public suffix. La configuration invalide refuse avant résolution.
3. Résoudre avec délai/quantité bornés. Vérifier toutes les adresses candidates : seules des adresses publiques admissibles peuvent servir. Refuser loopback, privées, link-local, non spécifiées, multicast, réservées, CGNAT, endpoints de métadonnées, IPv4 encodées/mappées et routes de transition non qualifiées. Un ensemble mixte public/privé refuse la requête entière.
4. Lier la connexion à une adresse vérifiée sans laisser le client HTTP refaire une résolution incontrôlée. Vérifier le pair réel, Host/SNI et certificat TLS du nom approuvé. Aucun `verify=false`, proxy ambiant ou réutilisation de connexion hors politique. **Ce point n’est pas démontré par les tests A2 : il exige un transport réel qualifié.**
5. Désactiver les redirections automatiques. Pour chaque Location, résoudre relativement à l’URL courante, refaire les contrôles de politique, d’autorité, de DNS et de pair. Pas de transfert de cookies, credentials ou en-têtes sensibles à une nouvelle origine. Le downgrade HTTP et toute cible non autorisée refusent.
6. Borner les redirections et les cycles ; proposition de pilote : au plus trois hops. Stop, expiration ou révocation sont revérifiés avant chaque hop, lecture de bloc et publication.

Les téléchargements par API ou exports officiels sont prioritaires. Les quotas/conditions d’utilisation doivent être vérifiés avant chaque nouveau connecteur ; aucune politique ne permet de contourner authentification, CAPTCHA ou paywall. Une source non compatible reste indisponible.

## Budgets et erreurs

Valeurs de départ **proposées**, à figer avec le prototype : une requête par source en vol, au plus deux tentatives pour une lecture idempotente, redirections ≤3, délai total d’opération ≤30 s, corpus synthétique ≤10 Mio et chaque document compatible avec la limite d’import existante de 2 Mio. Aucun dump complet n’est traité par l’importeur Android courant.

Ajouter des limites obligatoires sur les octets reçus et décompressés, objets, taille d’en-têtes, durée de lecture sans progrès, espace temporaire, file d’attente, nombre total d’étapes et journaux. Les compteurs cumulés persistent avec la mission ; ils ne repartent pas à zéro à la reprise. Réserver le disque avant admission/publication. Refuser les quotas nuls/incohérents plutôt que les remplacer par des valeurs illimitées.

Les propositions de délais ne remplacent pas les budgets CORE ni les contrats v1. Respecter Retry-After et le débit approuvé ; pas de retry sur refus de politique, rétractation de permission, erreur d’intégrité ou effet UNKNOWN. Une réponse tronquée, un téléchargement trop gros ou un corps décompressé excessif est mis en échec/quarantaine bornée, pas indexé.

## Arrêt, reprise et hors ligne

États conceptuels proposés : DRAFT, WAITING_APPROVAL, QUEUED, RUNNING, PAUSE_REQUESTED, PAUSED, STOP_REQUESTED, STOPPED_OBSERVED, COMPLETED, FAILED, UNKNOWN. Ils ne sont pas des alias des états NEXUS/SERVICES existants et n’autorisent pas un nouveau reçu wire.

- Stop bloque immédiatement les nouvelles admissions et demande l’arrêt des sockets/lectures. Le résultat distingue demande reçue et fin effectivement observée. Une écriture déjà engagée ne peut pas être annoncée annulée sans preuve.
- Perte réseau : suspendre les accès, conserver les compteurs/checkpoints vérifiés et continuer la lecture locale des documents déjà admis. Afficher la date de vérification ; pas de statut « frais » fabriqué.
- Reprise : vérifier version de politique, autorité, hashes, disponibilité des objets, quotas restants et état de publication. Une opération ambiguë reste UNKNOWN et n’est pas rejouée automatiquement.
- Redémarrage : l’ancien temps monotone et le consentement en RAM ne sont pas transportables comme permissions durables. L’hôte doit réadmettre la suite. Aucune activation au boot prévue par A2.
- Android économe : une opération lourde à la fois, priorité au dialogue/VOICE, pause sous contraintes thermiques/batterie/stockage. L’ordonnanceur persistant sera traité au lot G ; aucune dépendance WorkManager ni nouveau service permanent n’est ajouté ici.
- Mini-PC : même politique et reçus, quotas matériels propres, concurrence seulement après mesure et arbitrage. Aucun GPU payant.

## RAW/CURATED et données personnelles

RAW conserve les octets autorisés et les occurrences de provenance/licence. CURATED est une nouvelle révision dérivée ; aucun nettoyage n’écrase un original. Une déduplication exacte ne supprime pas les occurrences ou droits distincts. Les journaux techniques contiennent IDs/états/dates/codes, sans prompt, corps documentaire, cookie, token ou URL contenant des secrets.

La licence, l’attribution, la finalité, l’accès et la rétention sont requis pour la promotion. La suppression autorisée doit traiter index, dérivés, miniatures et politique de sauvegarde sans promettre l’effacement physique d’un provider. Aucun fichier de personne privée, profil sensible ou mémoire personnelle n’est collecté par ce lot préparatoire.

## Matrice des tests préparés

| Domaine | A2 : preuve disponible | N01-B : preuve encore requise |
|---|---|---|
| Hôtes, sous-domaines, schémas, ports, URL malformées | Oracle hors ligne et vecteurs négatifs/contrôles positifs | Même interprétation par le client HTTP réel et la politique |
| IP privées/spéciales, ensembles DNS mixtes, rebinding | Réponses DNS injectées ; aucune résolution ou socket | Resolver réel, IP épinglée, pair effectif, réutilisation des connexions |
| Redirections | Chaque hop examiné dans les fixtures, cible externe et budget refusés | Serveurs de test contrôlés, URLs relatives, cookies/en-têtes, boucles et TLS |
| Hors ligne, absence d’autorité, expiration, stop | Fixtures de décision, transport toujours non autorisé | Port CORE authentifié, révocation concurrente et arrêt de lecture observé |
| Proxy et réseau indirect | Présence simulée refusée | Environnement réel du transport, proxies imposés et règles d’egress équivalentes |
| Intégrité, compression, disque, quotas et reprise | Spécifiés ; mécanismes historiques identifiés | Tests de transport/stockage synthétiques, crash/ACK perdu et saturation |

`network_review.py` est un **oracle de revue**, pas un moteur réseau, une API d’autorité ou un résolveur. Ses verdicts positifs restent `eligible_for_test_request=true` avec `transport_authorized=false`. Les tests interdisent les sockets. Ils ne doivent jamais être utilisés pour autoriser une collecte réelle.

## Critères avant le premier prototype N01-B

Architecture/versions documentées, mode test exclusivement synthétique, transport choisi et dépendances examinées, DNS/pair/TLS contrôlables, port d’autorité réel défini, limites et arrêt observables, tests négatifs ci-dessus préparés, source/licence du petit corpus autorisées. Toute modification de contrat existant ou de protection historique exige un accord préalable distinct.
