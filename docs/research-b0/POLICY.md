# Liste blanche, protections et quotas

La politique ne s'importe jamais d'un document. L'hôte de test construit
`LabPolicy` avec une instance de serveur synthétique vivante qu'il possède.
L'hôte exact, le port réel et l'adresse `127.0.0.1` sont ensuite figés. Aucun
suffixe, sous-domaine, IP littérale, adresse interne arbitraire, proxy, tunnel,
service système ou autre port loopback n'est accepté depuis une URL.

Les URL doivent être ASCII, HTTPS, sans identifiants, fragments, paramètres,
contrôles, backslash ou nom encodé. Les chemins sont des routes simples finies
de fixture. Schémas file/data/ftp/http, IPv6, IP numériques alternatives et
Unicode sont refusés. Ce sous-ensemble strict est volontairement un laboratoire,
pas un normaliseur général d'URL Internet.

Les réponses de résolution sont injectées, contrôlées deux fois et doivent être
intégralement l'adresse possédée. Le client ne résout plus le nom : la socket se
connecte à l'IP épinglée et vérifie le pair, tandis que SNI, Host et le certificat
portent le nom approuvé. Une CA inconnue, un mauvais SAN, un contexte TLS rendu
insecure ou une mutation de destination est refusé. Les tests A2 sans sockets
restent conservés comme un oracle distinct ; ils n'autorisent pas ce transport.

Le client ne lit pas les variables de proxy pour ses sockets locales et ne
dispose d'aucune API d'egress externe. La barrière Python refuse les connexions
hors sockets de fixture et toute résolution système ; elle n'est pas une sandbox
pour du code Python/natif arbitraire hostile. Le namespace CI est la protection
système complémentaire ; il est vérifié avant les tests.

| Limite | Profil Android de laboratoire | Profil mini-PC opt-in |
|---|---|---|
| Requêtes cumulées | 12 | 12 |
| Document | 256 Kio | 1 Mio |
| Octets corps cumulés / mission | 1 Mio | 4 Mio |
| Connexions simultanées | 1 | 2 |
| Durée tentative / mission | 2 s / 30 s | 2 s / 30 s |
| Profondeur déclarée du plan | 2 | 2 |
| Fichiers temporaires cumulés en vol | 512 Kio | 2 Mio |
| Redirections | 3 | 3 |
| En-têtes / bloc de lecture | 8 Kio / 4 Kio | 8 Kio / 4 Kio |
| Événements persistés | 128 | 128 |

Les limites sont configurables avec plafonds de laboratoire codés et types stricts.
Un quota nul/invalide ne signifie jamais illimité. Aucun profil n'est activé selon
le matériel détecté. La profondeur est un attribut borné du plan ; B0 ne contient
aucun crawler récursif. Les quotas octets portent sur le corps lu par l'application,
pas sur tous les octets TLS/IP ; en-têtes, requêtes et buffers sont bornés à part.
Les connexions concurrentes dépassant le quota sont refusées, sans queue infinie.
Les encodages compressés et chunked sont refusés, sans décompression implicite.
Une réponse sans Content-Length, avec doublons d'en-tête, tronquée ou excédentaire
ne peut pas devenir un document validé.
