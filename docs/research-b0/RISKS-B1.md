# Risques, limites et N01-B1 proposé

Le laboratoire ne prouve aucune collecte Internet sécurisée ou admission CORE.
Les réponses DNS sont injectées, même si la connexion HTTPS/validation TLS est
réelle sur loopback. Les attaques DNS publiques, le routage Android, les proxies
imposés et l'authentification IPC restent non qualifiés. Aucun comportement
réseau de production ne doit réutiliser le permis de test comme une autorité.

Le magasin utilise POSIX flock/link et SQLite desktop. Il ne qualifie ni Android
SAF, ni stockage partagé hostile, ni panne physique d'alimentation. La barrière
Python n'est pas une sandbox native. La phase disque/SQLite synchrone bornée
appartient à un worker de test ; elle n'est pas un composant UI Android et son
arrêt ne garantit pas le rollback d'une publication déjà commise. Les horloges
murales et le stockage privé de l'hôte restent des hypothèses du banc, sans
attestation d'intégrité matérielle ni résistance à un propriétaire local hostile.

Les mesures CPU/RAM concernent la suite Python instrumentée sur Linux, incluent
fixtures et tests, et ne mesurent pas l'énergie ou la mémoire d'un APK. Les
processus OpenSSL ne sont pas inclus dans le CPU du seul runner. Aucun GPU.

Une première assertion de test confondait nettoyage du transfert refusé et fichier
temporaire légitime d'un autre transfert actif ; elle a été corrigée pour vérifier
le refus du second socket, le maintien du premier puis son nettoyage à l'arrêt.
Le premier résultat rouge est conservé dans les preuves de livraison.

**N01-B1 proposé : contrat d'admission et réception locale synthétique.**
Préparer un adaptateur expérimental versionné sous autorité hôte explicite,
en gardant les contrats v1 fermés et le transport loopback uniquement. Ajouter
rectification/suppression et provenance/licence de corpus synthétique, export
d'un manifeste borné vers un port NEXUS de test, tests de compatibilité réels et
reprise aux points de publication. Évaluer l'offload disque et des checkpoints
plus riches après mesures. Toute modification de contrat historique, migration,
réseau Internet réel ou raccordement sensible exige un accord distinct.

La revue B0 porte sur les sources et résultats liés aux SHA exacts ; elle ne
demande aucune fusion dans main, installation sur appareil ou dépense GPU.
