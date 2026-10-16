# O3 — transport, identité et arbitre interprocessus

**PROPOSÉE — NON APPROUVÉE.** Aucune décision O3 enregistrée, aucun service créé,
manifest modifié ou IPC implémenté. ADR-001 approuve l’orientation, pas ce transport.
La comparaison vise un premier pilote Android local CORE↔LLM, pas PC/montre.

## Options de communication locale

| Option | Identité, surface et permissions | Versions/erreurs et coût mémoire | API24/29 / recommandation |
|---|---|---|---|
| Bound Service Binder explicite, AIDL si utile | UID obtenu par Binder à chaque appel, package/certificat vérifiés ; export dédié nécessaire entre APK. Service fermé par défaut ailleurs ; permission signature uniquement si confiance de signature compatible | DTO bornés, callbacks/status/annulation typés ; transactions Binder partagent une limite mémoire, pas transfert de corpus en gros Parcel. Deux processus + JNI LLM à mesurer ; bind/unbind≠load/unload | Binder disponible à24 ; service LLM requiert29. CORE garde24 et branche déléguée inactive à24–28. **Recommandé pour fixtures**, conserve APK/sandboxes sans extraction moteur |
| Bibliothèque in-process commune | Pas de frontière UID entre modules du même processus ; confiance héritée de l’application hôte, accès données à restreindre | Appels directs, un gate process-wide possible ; risques de dépendances JNI/toolchain/packaging, même crash domaine. Mémoire potentiellement moindre, aucune mesure ici | Intégrer LLM29 dans CORE24 ne garantit pas24 ; module ou API guards/extraction à qualifier. Alternative à plus long terme, pas imposée |
| Messenger sur Binder | Même exigences UID/certificats et service exporté borné ; pas de confiance dans replyTo/package déclaré | Moins d’IDL, mais corrélation/versions/tailles/erreurs davantage manuelles ; aucun avantage de sécurité automatique | Possible local, alternative si petite interface ; moins explicite pour reçus de fin/baux |
| Intent explicite / Broadcast / PendingIntent | Permissions, identité et receiver contrôlés ; Intent implicite/public exclu ; absence de protocole natif durable par défaut | Adapté à activation/consentement ponctuel ; confirmations natives/reprises très fragiles si traité comme commande/réponse | Ne pas retenir pour génération/annulation/baux ; ne prouve pas provenance d’un résultat |
| ContentProvider / refs fichiers privées | URI accordées au bon UID, lecture bornée et durée courte ; file:// arbitraire exclu | Utile **canal de contenu** en complément Binder ; pas autorité des sessions ou arbitre. PFD/refs nécessitent révocation et ownership | Option pour payloads dépassant contrôle, pas second transport de commande |
| Socket local / HTTP loopback | Un port local n’est pas une identité APK ; auth/crypto/permissions supplémentaires | Serveur/discovery/protocole/timeout à maintenir, surface et coût non justifiés pour ce pilote | Ne pas choisir par défaut ; ne pas ajouter réseau à CORE/LLM pour ce besoin Binder |

## Recommandation de transport et frontière de confiance

Bound Service **dans une application de fixture isolée côté LLM**, composant explicite,
interface typée fermée/AIDL si nécessaire. Aucun export ajouté à l’app historique.
L’app de fixture CORE appelle l’endpoint, pas le catalogue ni une Activity LLM.
Contrat contrôle versionné/digest partagé ; autorisations données distinctes du
protocole et du consentement à installer. Seuils matériels et hors-ligne conservés.

Deux stratégies de signature à faire trancher, sans re-signer les APK existantes :

- Fixtures signées par une **clé de test dédiée commune**, permission signature et
  contrôle UID/package/certificat en plus. Cette clé ne remplace jamais les clés
  installées de CORE/LLM/VOICE et ne va pas dans Git. Solution de fixture recommandée.
- Fixtures signées différemment : vérification stricte des certificats explicitement
  appairés/allowlist ; permission signature commune ne suffit pas et peut interdire
  le client légitime. La politique d’enrôlement/rotation doit être approuvée ;
  une permission normale seule n’est pas une barrière de confiance.

Le certificat debug éphémère d’un run LLM n’est pas un ancrage de production.
Les signatures réelles CORE et LLM installées restent inconnues ici. Capturer
Binder.getCallingUid dans la transaction d’entrée, avant dispatch asynchrone ;
les noms transmis par client ne prouvent rien. Résoudre les packages liés au UID,
refuser ambiguïtés/shared UID non explicitement autorisées, vérifier certificats
et rotation selon politique. API24–27 et28+ ont APIs de signature différentes :
les guards doivent rester compatibles, aucune confiance de rotation automatique.

Avant tout contenu/modèle : vérification identité/version/capacité, mandat CORE
lié à la clé/session/expiration/objet et bail. LLM garde son droit de refus matériel.
Un identifiant UUID, SYSTEM « autorisé » ou consentement de fixture ne donne pas
un droit Android. Aucun texte ou chemin arbitraire exécuté. Limites de contrôle,
quota et backpressure ; refs privées/PFD bornées pour contenu au lieu d’énormes
Parcel, aucune donnée privée dans logs/annotations. Un canal Binder ne règle pas
à lui seul prompt/tokenizer/provenance ou arrêt réel.

## Emplacement de l’arbitre : proposition distincte

| Emplacement | Bénéfice | Risque/limite | Avis pour pilote |
|---|---|---|---|
| Processus de fixture CORE | Aligné sur autorité de parcours CORE, pas d’APK supplémentaire ; connaît moteur historique/proxy | Décès CORE alors que LLM calcule ; doit conserver état de récupération et réconcilier avant réouverture ; tous chemins participants doivent le consulter | **Recommandation de départ**, à valider avec protocole de panne ci-dessous |
| Processus LLM | Baux natifs proches du worker | CORE historique pourrait charger hors broker ; service absent sur API24–28 ; autorité technique ne doit pas devenir politique de permissions LLM | Alternative si toutes entrées CORE sont effectivement gardées, pas donnée comme acquise |
| Processus dédié | Indépendance vis-à-vis des deux UIs | Processus/permissions/état supplémentaires et coût à mesurer ; ne doit pas imposer un nouveau module/8APK | Non nécessaire au premier pilote ; à reconsidérer seulement après mesures |

Arbitre global du pilote = **registre exclusif des participants**, pas réserve RAM
Android ni maîtrise des applications tierces. CORE garde décisions/confirmations,
LLM ses baux ProcessResources et son admission matérielle locale. Une seule
réservation interprocessus active et un seul modèle lourd résident pour ce pilote.
P2Lifecycle ne crée pas un deuxième broker interne concurrent du backend.

Tous points de chargement contrôlés (UI autonome LLM, client, import lourd,
warm-up CORE/historique, Whisper/VOICE participants) doivent être refusés/sérialisés
pendant la réservation. Premier pilote texte isolé : ne pas lancer VOICE/Whisper.
Ne pas affirmer qu’un gate du client seul empêche une autre entrée LLM. Le mode
pilote est opt-in cohérent pour la paire, pas désactivable unilatéralement tant
qu’une réservation existe. Hors pilote, les applications historiques restent
autonomes ; aucune sûreté globale entre APK non participants n’est revendiquée.

## Pannes, mort de processus et libérations inconnues

Le broker doit garder un journal technique minimal de réservation/epoch/génération,
phase, identité de participant et nécessité de réconciliation, sans texte ni profil.
Un mandat expiré ou la mort du client déclenche stop/drain/unload côté LLM, pas
une libération immédiate du broker. Le retour natif puis le nettoyage doivent être
confirmés avant d’admettre le moteur suivant. Un timeout ne remplace aucune étape.

Au redémarrage CORE/broker : état **récupération bloquée**, interrogation du LLM et
vérification du propriétaire historique avant warm-up. Nouveau process/epoch ne
réutilise pas un ancien bail ; ancien ACK sans effet sur nouvelle génération.
Au redémarrage LLM : pas de génération ou UI autonome lourde avant réconciliation
si le mode pilote était engagé. Les requêtes status/recovery restent sans allocation
modèle ; aucun replay de texte.generate après ACK perdu.

DeathRecipient/unbind/déconnexion d’un Binder ne prouve pas que tout le processus
est mort ou que le modèle est libéré. Seule preuve adéquate de fin/nettoyage ou
mort effective du processus propriétaire reconnue dans le protocole peut résoudre
la réservation ; si impossible à attester, maintenir UNKNOWN et demander diagnostic,
jamais forcer libération. PID seul peut être réutilisé ; identité/epoch/génération
et rattachement au processus doivent être liés, pas un test « PID absent » isolé.
Le protocole détaillé de preuve de mort est un point à valider, pas une garantie
implémentée. La quarantaine CORE actuelle reste stricte, sans reset automatique.

Repli historique : explicite, après fin/libération confirmées de la paire ; pas
un second moteur de secours lancé dès qu’une réponse tarde. API24–28 conserve
le mode historique sans prétendre installer/exécuter LLM29. Pas de changement
minSdk, politique mémoire ou activation PLEINE PUISSANCE.

## Décisions requises

T1 : Binder/AIDL en fixtures, pas bibliothèque intégrée par défaut.
T2 : confiance par clé de fixture commune ou certificats distincts appairés, avec
UID/permissions et politique de rotation. T3 : emplacement du broker et scope des
participants. T4 : protocole de récupération/journal/mort et maintien de quarantaine.
T5 : contrat canonique et limites de la fixture (texte seul sans contexte), puis
autorisations par dépôt. Aucune de ces recommandations n’est enregistrée approuvée.
Le choix d’orientation ADR-001 n’est pas à redemander.
