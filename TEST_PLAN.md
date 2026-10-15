# Plan de vérification — JARVIS-UNIFIED

Ce document sépare ce qui a été vérifié en Mission 001 de la qualification future.
La présence d'un test ou d'un rapport historique ne signifie pas son exécution ici.
Les résultats source détaillés sont dans [AUDIT.md](AUDIT.md).

## Mission 001 : contrôles réellement réalisés

| Contrôle | Résultat | Ce que cela ne valide pas |
|---|---|---|
| Lecture Git HTTPS des trois dépôts | Réussie | Droits de push/API ou accès aux poids privés |
| Inventaire des 4/6/7 branches nommées CORE/LLM/VOICE, hors alias HEAD | Réussi | Branches supprimées ou PR non annoncées |
| `git fsck --full` sur les trois clones | Réussi | Fonctionnement de l'application |
| Ascendance des branches CORE vers main | Confirmée | Nécessité de fusionner ailleurs |
| Diff commits historiquement testés → bases retenues LLM/VOICE | Documents uniquement | Nouvelle exécution CI |
| SHA-256 de SafetyPolicy LLM | Conforme au rapport 003B | Adéquation physique des seuils |
| CRC, taille, SHA-256 des APK dans ZIP 005F/G | Conformes à delivery.json | Nouvelle vérification apksigner ou audibilité |
| Fixture SQL historique via Python sqlite3 en mémoire | Intégrité OK, 8 lignes dans quatre tables | Migration Android ou 33 tests Robolectric |
| Cinq livrables, liens locaux, blocs Markdown et `git diff --check` | Réussis | Compilation de pseudo-interfaces |
| Archives CORE/LLM/VOICE comparées aux blobs Git retenus | 39 + 77 + 204 fichiers identiques | Données privées hors Git |
| Branche UNIFIED et référence origin/main | Branche dédiée, origine inchangée | Publication ou fusion, non effectuées |

Les suites Gradle, CTest, builds, appareils, voix et inférences n'ont pas été
exécutés. Chaîne Android non préparée pour cette mission d'audit ; aucun modèle
personnel ou pack privé fourni. Pas de nouvelle défaillance applicative reproduite.
Les échecs historiques 005D et de parité FP32 restent ouverts et distincts.

## Rejouer les contrôles d'audit sans modifier les sources

Depuis un clone local séparé, les commandes `git ls-remote --heads`,
`git for-each-ref refs/remotes/origin/`, `git ls-tree -r <SHA>`,
`git merge-base --is-ancestor <branche> origin/main`, `git diff --name-only
<SHA-testé> <SHA-audité>` et `git fsck --full` sont des contrôles en lecture.
Réutiliser les SHAs immuables de l'audit. Ne pas confondre les sorties d'un nouveau
main avec les bases auditées. Pour les ZIP 005F/G : tester CRC, extraire en mémoire
l'APK et comparer sa taille et SHA-256 au manifeste de livraison au même commit.
La validation de signature est une commande apksigner distincte, non exécutée ici.

## Suites source à conserver dans les futures missions

Commandes historiques/documentées, **non exécutées ici**. À lancer dans des
copies de validation isolées aux SHAs de l'audit, avec sorties hors des sources
protégées et versions d'outils adaptées. Elles n'autorisent pas à changer une
source. Aucun poids, clé ou artefact personnel ne doit entrer dans les rapports.

| Source | Commandes / prérequis | Résultat historique de référence |
|---|---|---|
| CORE | Java17, Gradle8.10.2 sans wrapper, SDK35 ; `gradle :app:testDebugUnitTest :app:lintDebug :app:assembleDebug --no-daemon` | 33 cas SQLite + 7 heure ; 34 avertissements |
| LLM | JDK21, wrapper8.11.1, SDK36, NDK28.1.13356709, CMake3.22.1 ; `tools/prepare-native.sh`, `./gradlew :domain:test :app:testDebugUnitTest :app:lintDebug :app:assembleDebug`, `tools/test-native.sh`, `python3 tools/check-apk.py app/build/outputs/apk/debug/app-debug.apk` | 55 domaine, 16 Robolectric, 1 CTest ; 36 avertissements CI |
| VOICE 005G | JDK17, SDK35, wrapper source ; `./gradlew :pocketRuntime:test :voiceQuality:assembleDebug :voiceQuality:lintDebug --no-daemon --max-workers=2` | CI publique 33 réussis/13 ignorés sur 46 |
| VOICE 005F/G instrumentée | SDK/émulateur API35 x86_64 ; `./gradlew :voicePrototype:connectedDebugAndroidTest -PprototypeSidecar=true -PprototypeTestAbi=x86_64`, puis tâche analogue `:voiceQuality:connectedDebugAndroidTest` | Respectivement 10/10 et 14/14 synthétiques, pas génération personnelle |

Les commandes VOICE sans pack privé peuvent ignorer les tests d'inférence :
consigner les noms et motifs, ne pas transformer une suite partielle en validation
de bout en bout. Le CPU prototype est une piste CENTRAL distincte à rejouer selon
son `prototype/README.md`, pas une condition de l'APK Android locale.

## Matrice d'acceptation future

| Domaine | Scénarios requis | Critère observable |
|---|---|---|
| Contrats | Version inconnue, entrée trop longue, identifiant périmé, doublon, erreur et timeout | Refus typé, un terminal par requête, pas d'effet tardif sur autre session |
| CORE déterministe | Salutations, heure/fuseaux/API24–25 si maintenues, `/docs`, catalogue et ambiguïtés | Réponses/provenance correctes sans chargement LLM |
| Mémoire | Proposition automatique/`/remember`/voix/PDF malveillant, refus, modification après aperçu, expiration, double confirmation, redémarrage | Zéro souvenir durable sans confirmation du contenu exact ; écriture unique et traçable |
| SQLite | V1→V2, V2 existante, version inconnue, downgrade, insertion rejetée/-1, disque plein, échec passage 2 | Données et compteurs préservés ; transaction annulée en totalité |
| Catalogue | Import JSON versionné, conflits/révisions, répétition, corpus synthétique 1508 éléments | Pas de pertes/doublons silencieux ; clarification avant réponse ambiguë |
| Documents | PDF texte, scanné, chiffré, malformé, gros volume ; français/accent/chiffres ; injection de prompt | Bornes respectées, citations vérifiables, refus OCR absent, aucune action autorisée par le document |
| Prompt | Budget 512/768/2048 selon profil qualifié, longs historiques et sorties bornées | Taille tokenisée valide, contexte utile/citations conservés ; base originale intacte |
| GGUF | SHA faux, fichier tronqué, architecture/slot/quantification incompatibles, remplacement annulé | Refus avant activation, ancien modèle conservé, aucun second backend actif |
| LLM natif | Stop pendant load et generate, deadline, arrière-plan, rotation, unload en file, erreur de destruction | Arrêt effectivement observé ; bail conservé jusqu'à destruction, aucun rechargement concurrent |
| Ressources communes | STT/LLM/VOICE/import simultanés, résidence après génération, jeton périmé | Un travail lourd ; refus cohérent et libération idempotente ; pas de bypass d'admission |
| Matériel | Capteurs absents, batterie faible, thermique sévère, lowMemory, FULL_POWER | Refus sûrs ; aucune réduction de budget pour forcer l'essai |
| STT | Permission refusée, micro indisponible, arrêt/rotation, WAV incomplet, durée limite, transcription française | Fin de capture attestée avant Whisper ; nettoyage et retour au repos |
| VOICE import | Consentement absent, mauvais pack/JVFP1/PTVB1, ZIP traversal/doublons/bombe, hash/taille invalides, annulation | Aucune activation corrompue, ancien profil intact, bornes vérifiées |
| VOICE génération/lecture | Phrase courte/longue, PCM vide/non fini/silencieux, focus perdu, stop, dernière frame, cache corrompu | Génération/lecture/audibilité séparées ; aucun succès sur simple compteur de temps |
| Sauvegarde | Base active/WAL, espace insuffisant, annulation, archive altérée, mauvaise clé, version future, import répété | Snapshot cohérent ; refus sans écrasement ; activation atomique et retour arrière |
| Transfert PC | IDs/dates/compteurs, citations, catalogue, profils/pack incompatible, poids manquants | Équivalence des données ; profil préservé sans activation trompeuse |
| APK et distribution | Manifeste fusionné, bibliothèques natives, signature/mise à jour, release minifiée | Une app, un moteur LLM, ARM64 et alignement16K ; pas d'INTERNET ni backup/transfert automatique dans variante locale |
| Hors ligne | Installation avec packs locaux, mode avion, redémarrage à froid, PDF/STT/LLM/VOICE, absence du PC | Parcours complet sans authentification distante ni téléchargement à l'exécution |
| Hybride futur | Pair inconnu, version différente, coupure, réponse tardive, annulation distante | Refus authentifié ; aucune fuite/relecture d'action ni calcul local concurrent non autorisé |

## Campagne physique Redmi / POCO

Relever modèle exact, RAM accessible (sans compter extension constructeur), OS,
firmware, version APK/certificat, SHA GGUF et pack/profil, réglages contexte/threads,
conditions batterie/température et route audio. Ne pas inférer les ressources du
seul nom commercial. Commencer par diagnostic passif ; conserver un refus
naturel d'admission sans provoquer de pression mémoire ou contourner un garde.

Pour chaque configuration admise : au moins trois passages à froid puis un
passage chaud, phases import/chargement/génération/arrêt/déchargement/repos,
PSS/RSS/VmHWM séparés, latences, tokens/s ou RTF, batterie/thermique avec valeurs
absentes explicites. Fixer les critères de latence/qualité avant la campagne ;
aucun chiffre cloud ne vaut objectif matériel acquis. Arrêt immédiat sur garde
thermique/mémoire et aucune campagne FULL_POWER non qualifiée.

Voix : référence autorisée, aperçu/consentement, création et rechargement du profil,
phrases inédites françaises, graines et texte identiques pour A/B, ordre alterné,
même route/volume. Évaluer séparément : son audible, texte intelligible, naturel,
ressemblance au locuteur, artefacts et adéquation des réglages. Écoute par le
propriétaire avec notes explicites ; pas d'audio personnel envoyé au cloud.
ASR/WER et similarité numérique complètent l'écoute sans la remplacer.
Le clonage reste expérimental tant que ces portes ne passent pas.

## Format du rapport d'une campagne

Pour chaque cas : identifiant, version/commit source testé, plateforme, données
synthétiques/publiques/privées, commande, date, code retour, nombre de tests
réussis/échoués/ignorés, motif de chaque saut, rapport associé, résultat attendu
et observé. Zéro test exécuté n'est pas une réussite. Préserver les rapports
négatifs et les seuils ; distinguer régression, limite connue et blocage matériel.
