# Campagne intensive JARVIS — bilan de développement

État vérifié le 23 octobre 2026. Référence de planification :
`ef1592e9598e14d2245539e2453bf26d7f26969d`, branche
`plan/intensive-2026-10-22`. Ce bilan complète le plan historique ; il ne réécrit
pas ses champs `code_executed: false` ni ses fiches initiales.

## Comment lire les résultats

Le [registre vérifié](VERIFIED_STATUS.md) présente l'état strict des 31 missions.
À cet instant, 18 missions sont livrées sur preuves logicielles ; 23 incréments
sont publiés en comptant les cinq livraisons partielles. Les
[liens GitHub par mission](DELIVERIES.md) et l'[index des sources et empreintes](../../registry/intensive-2026-10-22/deliveries.json)
permettent de retrouver les rapports sans rechercher les anciennes conversations.
`DELIVERED` signifie que les capacités logicielles déclarées ont un rapport, un
reçu, des empreintes et une filiation Git vérifiables. Cela ne signifie pas que
l'ensemble des applications communique, que le JNI Android est qualifié, ou que
la conversation Athéna fonctionne sur un téléphone.

Un incrément partiel reste `BLOCKED` dans ce registre, même si son code compile.
Les missions simplement préparées ne sont pas des livraisons. Les versions des
bibliothèques produites sur JVM ne deviennent pas compatibles Android par leur
seule existence. Les résultats de tests de missions successives se recouvrent :
ne pas les additionner pour annoncer un total de tests distincts.

## Capacités déjà programmées et publiées

| Domaine | Missions livrées sur preuves logicielles | Fonctionnement obtenu |
|---|---|---|
| CORE | CORE-01, CORE-02 | Routage d'intentions et tâches locales, capacités et autorisations hôte ; bus d'événements corrélés et projection d'état. Pas de nouveau transport inter-APK. |
| IDENTITY / MEMORY dans CORE | ID-01, MEM-01 | Profils versionnés, comparaison, aperçus et retour à une révision ; mémoire de laboratoire SQLite avec confirmation du contenu exact, révocation et projection en lecture seule. Athéna reste inactive. |
| LLM | LLM-01 | Catalogue GGUF, import local vérifié et sélection persistée. Cette sélection n'est pas encore celle du worker d'inférence. |
| VOICE | VOICE-01 | SDK réutilisant le coffre, le moteur et le renderer existants ; file PCM bornée, annulation et quarantaine. Aucun nouveau moteur TTS générique. |
| INTERFACE / AVATAR | AVA-01 | Chargement de packs PNG vérifiés, rendu multicouche, prévisualisation et respect du cycle de vie. |
| SERVICES | SERV-01, SERV-02, SERV-03 | Registre et permissions d'outils ; extraction PDF/CSV avec provenance, exports ; workflows SQLite, reprise et déduplication. Une démonstration BRIDGE fonctionne entre deux JVM locales par stdio, sans Binder ni réseau. |
| NEXUS | NEX-01, NEX-02, NEX-03, NEX-05 | Catalogue SQLite réel, import TXT/Markdown/PDF avec SERVICES, index FTS5, recherche et résolution des citations sous autorisation hôte ; export chiffré et restauration isolée vérifiée. Bibliothèque JVM, pas d'adaptateur Android API24 livré. |
| EVOLUTION | EVOL-01, EVOL-02 | Observation locale optionnelle, incidents SQLite et diagnostics déterministes traçables. Aucun auto-correctif. |
| UNIFIED | UNI-01, UNI-02 | Génération et validation de DTO Java/Kotlin ; registre exécutable de dépendances, ownership et preuves Git, utilisable hors ligne. UNIFIED n'orchestre pas les applications. |

## Incréments publiés dont les objectifs restent incomplets

| Mission | Code utile livré | Blocage conservé |
|---|---|---|
| LLM-02 | Planificateur de contexte et port de mesure exacte ; réautorisation avant réduction de l'historique. | Tokenizer exact renvoie `UNSUPPORTED` en l'absence d'implémentation native qualifiée. Aucun comptage approximatif substitué. |
| LLM-03 | Profils matériels et observation passive des ressources du processus. | Patch F3B non appliqué, preuve native et prérequis LLM-02 incomplets. `EMPTY_UNATTESTED` ne prouve pas une libération. |
| VOICE-02 | Styles contextuels, segmentation, pauses, timeline PCM et comparaison A/B locale dans Studio. | Pas de modulation native ou d'écoute physique qualifiée. Les offsets PCM ne sont ni des phonèmes ni une horloge de lecture AudioTrack attestée. |
| UI-01 | Écran de conversation Compose, pagination, corrélation et refus des réponses tardives ; fixture explicitement distincte d'une réponse IA. | CORE-02 ne fournit ni soumission externe ni contenu des réponses ; aucun transport n'est activé. État par défaut NON CONNECTÉ. |
| EVOL-03 | Vérification de propositions de patch inertes, origine signée, revue humaine et journal durable. | Isolation OS non qualifiée : `bwrap: setting up uid map: Read-only file system`. Aucun patch non fiable exécuté. EVOL-04 reste bloquée. |

## Vérifications et limites des preuves

| Livraison | Résultat rapporté et vérifié dans son commit | Limites |
|---|---|---|
| CORE-01 | 425 cas réexécutés, zéro échec/saut ; builds et Lint sans erreur. | 36 résultats de fixture réutilisés séparément ; aucune qualification JNI Android. |
| CORE-02 | 348 tests réexécutés, zéro échec/saut ; builds et Lint sans erreur. | Bus de métadonnées interne, pas une conversation distante. |
| ID-01 | 334 tests debug réexécutés, zéro échec/saut. | SQLite sous Robolectric API24/25/35 ; les paramètres d'éditeur ne modifient pas `jarvis.identity/1`. |
| MEM-01 | 426 tests réexécutés : 376 debug et 50 MVP2, zéro échec/saut. | Base privée isolée, pas de chiffrement applicatif ni migration historique. La restauration de fixture testée n'est pas encore un export produit. |
| LLM-01 / 02 / 03 | Respectivement 240, 249, 254 tests logiciels sans échec/saut ; builds et Lint sans erreur. | Le test CTest Linux sans GGUF ne prouve pas une génération Android. |
| VOICE-01 | 25 tests SDK ciblés réussis ; régression globale 104 réussites et 16 sauts historiques sur 120 cas. | Sauts dus aux packs absents, conservés et signalés. Aucun clonage vocal ni rendu expressif physique nouvellement validé. |
| VOICE-02 | 37 tests ciblés réussis sans saut ; régression élargie 116 réussites et 16 sauts historiques, avec résultats inchangés réutilisés explicitement. Build/Lint Studio sans erreur. | Démonstration des timelines sur ports synthétiques, aucune preuve de rendu neuronal expressif. |
| AVA-01 / UI-01 | Respectivement 84 et 94 tests JVM sans échec/saut ; APK et tests instrumentés compilés, Lint sans anomalie. | Les nouveaux tests instrumentés n'ont pas été exécutés ; pas d'émulateur ou appareil disponible. |
| SERV-01 / 02 / 03 | Respectivement 69, 84, 92 tests JVM sans échec/saut ; démonstrations réelles sur fichiers fictifs. | Android/Lint encore non exécutés au commit SERV-01 ; les builds ultérieurs ne changent pas cette preuve historique. SAF physique non qualifié. |
| NEX-01 / 02 / 03 | Respectivement 18, 34, 50 tests sans échec/saut ; SQLite/FTS5, PDF SERVICES et résolution de citations réels sur données synthétiques. | Aucun appareil Android, aucune preuve de budget exact de tokens. |
| NEX-05 | 69 tests réussis sans échec/saut ; démo réelle d'archive AES-GCM, vérification, restauration isolée, conflit et corruption refusée. | Clé fournie par l'hôte, parent privé de confiance ; pas de Keystore/SAF ni d'adoption automatique. |
| EVOL-01 / 02 / 03 | Respectivement 14, 25 et 13 nouveaux tests réexécutés ; 25 anciens résultats réutilisés pour EVOL-03. | Les diagnostics ne prouvent pas la causalité ; l'atelier reste inerte sans sandbox qualifiée. |
| UNIFIED | 126 tests Python distincts : 41 audit/contrats, 23 registre, 32 campagne, 30 sauvegarde ; zéro échec/saut. Génération compilée : 45 assertions Java et 5 allers-retours Kotlin. | Profil JVM strict explicite ; pas de qualification API24 automatique des DTO générés. |

Dans UNIFIED, commandes réellement exécutées :

```sh
python3 -m unittest discover -s tests -q
python3 -m unittest discover -s registry/tests -q
python3 -m unittest discover -s tooling/campaign/tests -q
python3 -m unittest discover -s backup_prototype/tests -q
python3 scripts/validate_unified.py
python3 -m tooling.contracts.verify_jvm
```

Le dernier programme utilise le JDK et le compilateur Kotlin disponibles, décrits
dans [le guide des contrats](../../tooling/contracts/README.md). Le validateur
UNIFIED accepte 5 exemples et refuse 5 exemples invalides pour 5 contrats et
9 dépôts. Le diff de campagne des schémas `contracts/v1`, de `scripts/contracts.py`
et du manifeste historique `MISSIONS.json` est vide.

Les anciennes gardes CORE/VOICE dont le périmètre gelait toute l'application ne
sont pas désactivées pour masquer une extension autorisée. Leurs écarts de
périmètre sont documentés dans les rapports ; des gardes ciblées contrôlent les
fichiers historiques, JNI, coffres, fixtures et protections effectivement gelés.
Les avertissements Lint existants sont conservés et quantifiés par dépôt.

## Reprises et corrections issues des revues

- Le registre refuse une livraison depuis une branche sœur qui ne contient pas
  son prérequis dans le même dépôt. Il vérifie le nouvel état avant mutation.
- Les reçus historiques normalisés restent liés aux octets des rapports et, si
  disponible, des reçus Git d'origine. Une transcription n'est pas une réexécution.
- MEM-01 interdit le rejeu d'une proposition d'une ancienne incarnation de
  session, même après révocation et recréation du même identifiant. La perte d'un
  ACK après commit est présentée comme une incertitude à vérifier dans la liste,
  jamais comme une annulation garantie de l'écriture.
- NEX-05 ancre la destination au parent canonique, vérifie le SHA des octets
  réellement déchiffrés avant parsing et borne l'énumération ZIP. Le nettoyage
  vérifie l'identité de son workspace. Ces corrections sont couvertes par tests ;
  elles ne constituent pas une protection absolue contre un parent hôte hostile.

## Suite autorisée et décisions sensibles

Les missions ID-02, UI-02 et NEX-04 se poursuivent sur leurs branches distinctes.
MEM-02 et CORE-03 suivent dans le même checkout CORE ; les portions isolées de
VOICE-03 restent limitées par les gates natifs et de transport ; AVA-02 dépend
des capacités temporelles réellement livrées par VOICE-02.
Un seul agent écrit à la fois dans un dépôt. Les [états du registre](VERIFIED_STATUS.md)
précisent les affectations et blocages courants ; cette liste n'autorise pas le
lancement d'une dépendance dont les fonctions manquent.

Les prochaines frontières nécessitant un accord distinct sont : modification JNI
ou de l'admission, activation de communications sensibles inter-APK, stratégie
de signatures/permissions, qualification physique et installation, migration de
données personnelles et application de correctifs par EVOLUTION. L'approbation
de l'orientation ADR-001 reste acquise ; elle ne vaut pas autorisation de ces
opérations. CORE004D reste bloquée par F3 et la revue du protocole `/2`.

Aucune fusion dans main, installation, migration, utilisation de données privées
ou téléchargement de modèle n'est effectué par cette campagne. Les publications
réussies concernent uniquement les branches de mission, sans force-push. Les
anciennes branches et leurs commits sont conservés.
