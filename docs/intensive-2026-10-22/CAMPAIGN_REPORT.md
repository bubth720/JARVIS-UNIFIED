# Campagne intensive JARVIS — bilan de développement

État vérifié le 23 octobre 2026. Référence de planification :
`ef1592e9598e14d2245539e2453bf26d7f26969d`, branche
`plan/intensive-2026-10-22`. Ce bilan complète le plan historique ; il ne réécrit
pas ses champs `code_executed: false` ni ses fiches initiales.

## Comment lire les résultats

Le [registre vérifié](VERIFIED_STATUS.md) présente l'état strict des 31 missions.
À cet instant, 20 missions sont livrées sur preuves logicielles ; 26 incréments
sont publiés en comptant les six livraisons partielles. Les
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
| IDENTITY / MEMORY dans CORE | ID-01, ID-02, MEM-01, MEM-02 | Profils versionnés, comparaison, aperçus et retour à une révision ; goûts simulés et règles de langage bornées ; mémoire de laboratoire SQLite avec confirmation exacte, rappel traçable et export volontaire vérifié. Athéna reste inactive. |
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
| CORE-03 | Client autonome JVM : recherche NEXUS, résolution de citations, outils SERVICES CSV/DOCX et confirmation de mutations dans une fixture contrôlée. | NEXUS/JDBC et SERVICES ne sont pas qualifiés pour CORE Android API24. Aucun raccordement AppGraph/SessionCoordinator/PromptBuilder ou inter-APK. |
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
| ID-02 | 400 tests initiaux conservés ; correctif d'aperçu puis 406 tests debug réexécutés, zéro échec/saut. | Goûts et règles dans le format d'éditeur local, aucun changement de contrat v1 ni activation d'Athéna. |
| MEM-01 | 426 tests réexécutés : 376 debug et 50 MVP2, zéro échec/saut. | Base privée isolée, pas de chiffrement applicatif ni migration historique. La restauration de fixture testée n'est pas encore un export produit. |
| MEM-02 | 501 tests réexécutés : 448 debug et 53 MVP2, zéro échec/saut ; trois builds API24/ARM64, Lint sans erreur. | Export privé réel et protocole de copie SAF testé avec doubles ; aucun fournisseur/appareil physique qualifié. Chiffrement indisponible sans port qualifié, aucune restauration automatique. |
| CORE-03 | 10 tests JVM sans échec/saut, vraie recherche SQLite/FTS5, CSV SERVICES et DOCX relu ; source modifiée refusée. | Android inchangé contre MEM-02 ; ses 501 résultats restent des preuves du parent, pas 501 réexécutions supplémentaires. |
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
- Le correctif ID-02 expose aussi les valeurs par défaut masquées et les retraits
  d'overrides dans la revue ; les 400 anciens tests et leur commit restent conservés.
- MEM-02 ne bloque pas la révocation sur un fournisseur de fichiers en attente.
  Une erreur de copie conserve la copie privée, consomme la confirmation et ne
  prétend ni effacer le document du fournisseur ni retirer les octets déjà copiés.

## Reprise ciblée CORE / MEMORY

| Incrément | Branche publiée | Commit exact | Résultat |
|---|---|---|---|
| Correctif ID-02 | `feat/id-02-intensive` | `283423cb8b9d567539f33cf7f2f1fafa602cf974` | Correctifs locaux interrompus repris ; 406 tests, dont les 400 initiaux, sans réécriture du commit `7a54f85`. |
| MEM-02 | `feat/mem-02-intensive` | `49ad428e94edd75c2a1d115c8c2504f26609eace` | Rappel lexical confirmé, budget propre, aperçu exact et export volontaire, import isolé sans écriture ; 501 tests. |
| CORE-03 | `feat/core-03-intensive` | `aea5ac859ac551d54fe16187c1883a487dbee9d6` | Bibliothèques clientes JVM réellement exécutées, 10 tests ; objectif Android encore PARTIAL. |

Les branches forment une filiation linéaire, sans fusion. Leurs SHA distants sont
vérifiés par `git ls-remote` ; CORE main reste
`226e2e8cc3eebd479805b89d035eb5c1cbcad540`. Rapports, reçus, contrôles APK et guide
du laboratoire se trouvent dans les commits [indexés par mission](DELIVERIES.md).
La reprise ciblée ne modifie aucun autre module applicatif.

Après cette reprise, les suites UNIFIED sont réellement réexécutées : 41 tests
audit/contrats, 23 registre, 32 campagne, 30 sauvegarde, soit 126 réussites sans
échec/erreur/saut. Le validateur passe et les 26 incréments de l'index ont leurs
rapports/reçus relus depuis Git et leurs SHA-256 vérifiés. Ces vérifications ne
transforment pas les six incréments PARTIAL en missions livrées.

Les travaux interrompus UI-02, VOICE-03 et NEX-04 restent dans leurs checkouts et
branches, **non commités/non publiés et non comptés comme livrés**. Des copies
locales ZIP des patchs index/worktree et fichiers non suivis ont été vérifiées,
originaux conservés, sous `/workspace/shared/jarvis-reprise-20261023T220439Z/`.
Le fichier `BACKUPS.json` y conserve leurs empreintes. Ce chemin est une sauvegarde
de l'environnement, pas un téléchargement GitHub ni une preuve de validation de
ces trois missions. Aucun agent concurrent n'est annoncé actif après interruption.

## Suite autorisée et décisions sensibles

La reprise ciblée ID-02/MEM-02/CORE-03 est publiée. CORE-03 doit ensuite qualifier
les bibliothèques pour Android API24 avant de brancher ses ports au vrai hôte.
UI-02, VOICE-03 et NEX-04 attendent reprise et publication de leurs travaux locaux ;
AVA-02 dépend des capacités temporelles réellement livrées par VOICE-02.
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
