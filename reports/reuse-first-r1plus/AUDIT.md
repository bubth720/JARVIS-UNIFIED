# Audit des acquis et de leur réutilisation

## Périmètre vérifié

Huit dépôts accessibles, 214 branches initiales, 593 commits récupérés, 101 têtes de PR disponibles localement et 1 250 métadonnées de runs Actions parcourues sur toutes les pages. `INVENTORY.json` contient les branches/SHA, parents et messages des commits, PR et CI ; ce recensement ne signifie pas lecture de chaque log ou téléchargement de chaque ancien livrable. Les logs déterminants M51/M51-R1, les sources/tests des missions prioritaires et les nouveaux résultats ont été examinés. Huit clones complets et huit bundles vérifiés préservent les acquis.

CORE est réellement `bubth720/JAVIS-Local-v2` ; EVOLUTION est `bubth720/JARVIS-VOLUTION-`. Ces noms ne sont pas corrigés ou fusionnés par convention. Le registre historique UNIFIED conserve ses neuf entrées, dont l'ancien emplacement INTERFACE ; le dépôt INTERFACE actif est `JARVIS-INTERFACE`. INTERFACE n'a pas de branche `main` : sa branche par défaut et toutes les références initiales sont protégées comme celles des sept autres dépôts.

## CORE — CONSERVER

Source M50 `5da98383ed12cb5a54e896fbe57560bacc432fb5`. Orchestration, admission, mémoire/UI de laboratoire et contrats déjà présents ; source inchangée. Les tests `integration-lab` réutilisent exactement NEXUS `777e6afa75ecb99b85e52d68837cb0fefcf161cd` et SERVICES `3decdc47d82f9b43713c48cab244762941770a81`, sans substituer les nouvelles branches. Une nouvelle CI indépendante confirme 641 exécutions JVM/Robolectric, 20 Python. L'ancien garde historique passe à sa source exacte. Deux fichiers pycache générés par notre commande initiale avaient perturbé le contrôle de propreté : seuls ces deux fichiers générés ont été retirés, puis le contrôle a passé avec `PYTHONDONTWRITEBYTECODE=1`. Ce n'était pas un défaut de JARVIS.

La disponibilité JVM ne vaut pas admission native, modèle ARM64, déchargement fiable ou expérience Android. Quarantaine d'un unload inconnu, one-heavy et autorité CORE restent intacts. Aucun adaptateur CORE/LLM actif ajouté.

**Acquis M50-S1B distinct, conservé et récupéré** : INTERFACE `b9a6c1997710c182dd481b23a47ff7120e3e98a0` compile sept blobs exacts du vrai SessionCoordinator CORE et du client INTERFACE. La réception historique du 4 novembre, [run 41839854603](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/41839854603), qualifie un APK unique testOnly : 6 scénarios instrumentés PASS sur chacune des API 29/35, mode avion et Wi-Fi coupé observés, rotation, Stop/drainage, UNKNOWN et force-stop/restart. APK et rapports téléchargés/re-hashés pendant cette mission, sans nouvelle exécution Android ; `evidence/M50-S1B-*` conserve leurs valeurs exactes. APK SHA-256 `681fd6e521290717ca2f80599e9267434fff1596809d3e50ba34e7d173ed9686`. Cet acquis est la base de réutilisation CORE/UI : réponses fixes LAB/SYNTHETIC, sans moteur/poids/base/transport nouveau, autres modules OFF, G2 PASS limité au laboratoire. Il ne qualifie pas M51 SAF, LLM ou la chaîne verticale, et n'est pas recopié comme une nouvelle intégration.

## UNIFIED — CONSERVER et documenter

Base `a7625a31513be5c56fa36ed946fbdcd3c23c2a15`, branche M51. Registres, contrats, snapshots, campagnes, proposition d'intégration et réception V1 restent la référence. Les ajouts de cette mission sont des preuves, gardes de préservation et CI indépendantes. Ils ne changent ni les anciens contrats, ni les critères, ni les scores/portes, ni l'architecture. Le validateur de réception de cette mission est documentaire : il ne donne aucune permission à un runtime.

## LLM — CONSERVER, BLOCKED / NO_GO

Source `08fbda527d187f324d94e0adafbca76fa955a343`, branche `codex/m51-lab-cloud-audit`, [PR #16 existante](https://github.com/bubth720/JARVIS-LLM/pull/16). Harness Kotlin/JUnit existant réexécuté réellement sur Java 21, dépendances épinglées et vérifiées, 247 tests hérités + 12 audit PASS. Les tests d'audit reproduisent des problèmes : une exception d'observateur empêche les notifications suivantes ; callbacks sous moniteur de fermeture ; surveillance susceptible de bloquer l'annulation sur l'exécuteur de contrôle ; chmod 0400 ne révoque pas un descripteur déjà ouvert ; identité inode/taille/mtime/mode insuffisante contre un écrivain même UID ; exception filesystem pouvant exposer un chemin ; LabExecution n'atteste pas le bootstrap ; terminal insuffisamment scellé. Verdict **NO_GO**, pas « sécurité PASS ».

Patch non appliqué, JNI non chargé, aucun poids acquis, aucune génération. G-A et G-ROOT fermées, G-B non validée. Les moteurs alternatifs restent des candidats de comparaison : aucune substitution productive autorisée ou justifiée par mesure Android.

## VOICE — CONSERVER les profils et configurations

Source M50 `642d9c19bcba35e5ffe686403d50c65aa9dc992a`. Branche par défaut distincte `feat/pocket-tts-cpu-prototype`, pas de changement de profil ni de commutation. La CI reprend les suites SDK/runtime/identity/expression/pocket/bridge/studio/pilot existantes : 260 exécutions, 237 PASS et **23 SKIP**, zéro échec. Cela qualifie les protocoles JVM couverts, pas une voix humaine entendue ni l'interruption audio Android. Aucun audio privé traité, aucune licence de modèle présumée depuis celle du code. Le profil réellement actif sur un appareil reste inconnu sans réception autorisée.

## INTERFACE — OPTIMISER le diagnostic ; M54 CONSERVER

Base M51-R1 `b9a9506785b8851f55789ed4329c9394a3937447`. 155 fichiers historiques figés ; seuls deux helpers de laboratoire sont adaptés avec activation explicite de la nouvelle campagne. Sources applicatives, ressources Compose, signatures et assertions historiques conservées. Détails des défauts et de la correction démontrée dans [ANDROID.md](ANDROID.md). API 29 et 35 non qualifiées malgré build et tests hôte réussis.

M54 est sur une autre branche, source exacte `2397bf29526ba48ac881e67c8e07dde3e01cf489`, contrôleur enveloppant `AvatarSession` existant. Réexécution sur cette source sans la copier dans M51 : 21 JVM + 20 Python PASS, empreintes inchangées. Renderer non implémenté, master artistique non fourni, ressources privées non traitées, audio/Android non exécutés, visèmes non supportés. Ni renderer, ni synchronisation, ni design recréé.

## NEXUS — CONNECTER et OPTIMISER dans les tests uniquement

Base M53 `eae61fb62a9ccd4073b96d71454f89e5a943eae9`. Contrat DocumentaryGateway/1, LocalRagService, SQLite FTS5 et CitationResolver réutilisés. Les 329 fichiers historiques et leurs modes restent identiques. Ajout de ReadOnlyConsultationAdapter : refus par défaut, callbacks d'autorisation fraîche/session/génération, corrélation, annulation et échéance avant/après consultation, citations et JSON non fiable conservés. Aucun cache d'autorité, mandat CORE, réseau, écriture ou migration. L'init explicite compile ce code dans **test seulement**, sans JAR productif/APK.

100 tests M53 + 8 nouveaux = 108 JVM PASS, 10 Python SQLite PASS sur données fictives CC0, hash/citations/injection/révocation/échéance/annulation testés ; invariants de non-mutation et intégrité SQLite vérifiés. Ce carrier n'est pas un contrat wire approuvé ni une preuve d'identité Binder. Le vieux workflow NEX-07 échoue réellement à son garde de périmètre historique, avant tests ; il n'est pas assoupli ou caché. La CI dédiée de la mission est verte. Android, SAF, vraie mémoire, Kiwix natif et connexion CORE restent BLOCKED.

## SERVICES — CONSERVER, actions fermées

Source `8d80d09d6aabf6eac00a7bc6bb4930862bd72812`. 134 tests desktop JVM PASS sur fixtures ; dispatcher, règles et protections disponibles au périmètre testé. Aucun appel à un service personnel ni activation d'automatisation Android. Les contrats préparatoires M53 ne donnent pas de nouvelle autorité. WorkManager/Binder sont des possibilités à qualifier, pas des substitutions déjà installées.

## EVOLUTION — CONSERVER, exécution fermée

Source `84ebc2e2b55d48306247fc9045a712294abaf457`. 40 JVM PASS et démos CLI de diagnostic/proposition/politique exécutées. Le runner reste NOT_RUN et le sandbox NOT_QUALIFIED ; aucune réparation automatique. Une première commande locale visant un dossier `tests` inexistant était une erreur de sélection de commande, pas un test valide ou un échec applicatif ; les résultats publiés sont ceux de la vraie suite Gradle fraîche.

## Limites transversales

Le cloud local ne dispose ni de SDK/adb/émulateur/KVM pour Android. Une unique campagne distante bornée a donc été lancée, avec contrôles de l'accélération en lecture seule ; aucun changement de permissions KVM, protection matérielle ou appareil personnel. Aucun LLM local réel, STT/TTS réel, parcours hors ligne global, performance énergétique ou rendu d'avatar n'est qualifié. Le parcours vertical reste une préparation isolée dépendant des portes existantes. Aucun travail dans les autres projets.
