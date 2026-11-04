# M50-S1B — intégration Android CORE + INTERFACE

**Laboratoire qualifié sur émulateurs API29 et API35 au 4 novembre 2026,
13:47 UTC. M50 NON ATTEINT.**
Module application : INTERFACE. Mission : M50-S1B, laboratoire privé testOnly.
Coordination : UNIFIED, branche `codex/m50-s1b-coordination-20261104`,
issue de `34f2de4ef0bd74738ead9656c85bdf4d947f1e0d`.

## Sources et intégration

| Dépôt | Branche / référence | Commit |
|---|---|---|
| CORE `bubth720/JAVIS-Local-v2` | `codex/m50-s1-core-ci-20261029`, PR#27 conservée | `5da98383ed12cb5a54e896fbe57560bacc432fb5` |
| INTERFACE `bubth720/JARVIS-INTERFACE` | `codex/m50-s1b-android-20261104`, [PR brouillon #14](https://github.com/bubth720/JARVIS-INTERFACE/pull/14) | `b9a6c1997710c182dd481b23a47ff7120e3e98a0` |
| INTERFACE historique | PR#13, source du client réutilisé | `3a0841266fd691b74fae784004804429e6e2e219` |
| UNIFIED historique | PR#19, base de coordination | `34f2de4ef0bd74738ead9656c85bdf4d947f1e0d` |

Les références, arbres, branches par défaut et CI de départ ont été relus
directement sur GitHub : [BASELINE.json](BASELINE.json). CORE n'a reçu aucun
nouveau commit ni changement de source. Les trois historiques restent conservés.

Le projet autonome `labs/m50-s1` dans INTERFACE extrait **sept blobs Git exacts**
dans un dossier temporaire extérieur aux dépôts. Il compile le véritable
`SessionCoordinator`, ses événements et modèles CORE avec le véritable
`CoreConversationClientAdapter` et ses types INTERFACE. Les arbres et blobs
sont épinglés dans son `sources.json`. Le garde vérifie tous les fichiers et
modes historiques, y compris les fins de ligne de checkout déclarées par Git.

L'Application possède un seul coordinateur de laboratoire, un bus RAM et le
client INTERFACE. Aucun AppGraph historique, moteur, base de données ou nouveau
transport n'est instancié. L'ACK reprend session/request/génération du véritable
événement CORE UserInput. Les chunks sont fixes, marqués LAB/SYNTHETIC et ne
reflètent pas la question. La fin de contenu attend le drainage effectif de CORE :
une métadonnée Completed suivie de RESOURCE_UNCONFIRMED reste UNKNOWN.

Stop demande l'annulation logique et conserve le refus de chevauchement pendant
le drainage. Rotation conserve le propriétaire processus. Fermer efface la
projection RAM et bloque la réouverture du banc dans ce processus. UNKNOWN ne
peut être réinitialisé par l'Activity ; seul un véritable redémarrage de processus
crée un nouvel epoch initialement OFF. Aucun état natif réel n'est attesté.

## Compatibilité et vérification locale

Outillage du laboratoire : **JDK17, Gradle8.13, Kotlin2.1.20, AGP8.9.2,
coroutines1.10.2, compile/target35, min29**. Les versions et minSdk historiques
CORE/API24 et INTERFACE/API26 restent intacts. Les sources CORE Kotlin2.0.21
sont réellement compilées avec cet outillage, sans changer leurs octets.

[LOCAL-RESULTS.json](LOCAL-RESULTS.json) distingue les résultats hôtes et Android :

- 11 tests JVM PASS, 0 FAIL/ERROR/SKIP : ACK, contenu fixe, double-submit,
  Stop/drainage, clé périmée, erreur CORE, UNKNOWN après Completed, replay,
  ACK perdu, fermeture/callback tardif et texte invalide.
- 11 tests Python PASS, 0 FAIL/ERROR/SKIP : gel historique, suppression,
  permissions de fichier, symlink, workflow non revu, traversée de chemin,
  refus d'écrasement et fins de ligne Git.
- `:app:assembleDebug`, `:app:assembleDebugAndroidTest` et Lint PASS ;
  Lint : 0 erreur, 6 avertissements non masqués.
- APK réellement inspecté : `fr.jarvis.lab.m50s1`, testOnly, sauvegarde désactivée,
  aucune permission, aucun asset/modèle, aucune bibliothèque native,
  aucune classe AppGraph/LlamaLocalEngine/WhisperLocalEngine ; signature vérifiée.

Le sujet de la compilation locale est `358ede1d33742b3bb00c575d49d4d829a3fe1ec1`.
Le correctif suivant ne change que le pilote Python d'émulateur. L'APK local
a le SHA256 `9cf076f0339aea5d362362573f51ed51a95061bb9ce6d4f987660c2b8808d0fe` ;
il n'est pas présenté comme l'APK instrumenté en CI. Le certificat debug
éphémère peut différer entre machines. `/dev/kvm` est absent du terminal :
l'instrumentation locale est NOT_RUN.

Commandes reproductibles, depuis INTERFACE :

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s labs/m50-s1/tests -v
python3 labs/m50-s1/tools/check_scope.py --interface .
python3 labs/m50-s1/tools/prepare_sources.py --core ../CORE --interface . --output /tmp/m50-sources
gradle -p labs/m50-s1 -PlabSources=/tmp/m50-sources/kotlin :app:testDebugUnitTest :app:assembleDebug :app:assembleDebugAndroidTest :app:lintDebug --no-daemon --max-workers=2
```

La CI compile un APK, vérifie son manifeste et sa signature, puis teste **ce
même digest** sur émulateurs API29/35. Les six scénarios instrumentés couvrent
manifeste, UI tactile/ACK/réponse/Stop/fermeture/rotation, Stop après drainage,
clé périmée, ERROR, UNKNOWN et replay. Le pilote externe ajoute mode avion,
UNKNOWN conservé en rouvrant l'Activity et véritable force-stop/restart.
Les XML et captures sont séparés par API. Les métriques, si disponibles,
décrivent uniquement ce laboratoire synthétique : démarrage Android et PSS,
jamais une latence ou consommation de LLM réel.

## Incident vérifié et correction

Au premier sujet `358ede1`, la CI historique Android est SUCCESS
([41837256481](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/41837256481)).
Le laboratoire est FAILURE
([41837256523](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/41837256523)) :
le shell Android refuse l'envoi direct du broadcast protégé AIRPLANE_MODE.
L'échec précède l'instrumentation ; API29 n'est pas annoncée PASS et API35
reste NOT_RUN à cette tentative. Aucun APK qualifié n'a été publié.
[Métadonnées et annotation du refus](CI-ATTEMPT-1.json).

Le commit `b9a6c19` utilise l'API shell ConnectivityService prévue pour activer
réellement le mode avion, et conserve les assertions sur son état et le Wi-Fi.
Il ne contourne pas le refus de broadcast, n'ajoute aucune permission à l'APK
et ne réduit aucun test. Il évite aussi d'envoyer BACK quand aucun clavier
virtuel n'est affiché, et conserve les diagnostics des échecs instrumentés.

## Livraison qualifiée et réception M50

Au commit `b9a6c1997710c182dd481b23a47ff7120e3e98a0` :

- [CI complète du laboratoire 41839854603](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/41839854603) SUCCESS : instrumentation API29 et API35, mode avion, rotation, erreurs/UNKNOWN, force-stop/reprise externe et qualification finale SUCCESS.
- [CI historique Android 41839854697](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/41839854697) SUCCESS au même commit.
- [Télécharger l'APK qualifié et sa réception](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/41839854603/artifacts/13329266245), connexion GitHub requise.
- [Rapports XML, Lint, captures et provenance](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/41839854603/artifacts/13329226310).

SHA256 de **l'APK réellement testé sur les deux API** :
`681fd6e521290717ca2f80599e9267434fff1596809d3e50ba34e7d173ed9686`.
Le qualificateur calcule ce digest, le compare aux deux campagnes et le publie
comme sortie GitHub utilisée dans le nom de l'artefact qualifié. Il diffère du
digest de l'APK local signé séparément. Le digest d'archive ZIP GitHub est
`85b5380415365715411231c64b309b2bb81bbb8f853c2c1705c75884df4f3b45` :
il ne faut pas le confondre avec celui de l'APK.

Les métadonnées et étapes finales ont été relues : [CI-FINAL.json](CI-FINAL.json).
Les exécutions push annulées par la concurrence ne sont pas additionnées
aux runs de PR. Les XML, comptes exacts CI et mesures PSS/démarrage sont dans
les vrais fichiers `QUALIFICATION.json` et `RESULTS.json` des artefacts.
Le terminal n'autorise pas les hôtes de stockage blob/logs Actions : ces fichiers
n'ont pas été téléchargés ni re-hashés localement, et aucune copie reconstruite
de leurs valeurs n'est présentée comme leur contenu réel. Les statuts de jobs,
étapes, noms d'artefacts et digests de métadonnées sont directement observés.
Les assertions de réception imposent au moins 11 cas JVM et 6 cas instrumentés
distincts et sans échec/saut par API ; les six scénarios définis restent séparés
entre API29 et API35.
La rétention des artefacts est configurée à sept jours ; conserver les archives
téléchargées pour une réception au-delà de cette période.

[État machine courant des huit gates](GATES.json). L'instantané historique
`RELEASE-EVIDENCE.json` conserve ses valeurs datées et pointe vers ce nouvel état.

| Gate | État après réception S1B | Preuve encore nécessaire |
|---|---|---|
| G1 | PARTIAL | Licences/SBOM des huit modules et lock de produit approuvé |
| G2 | PASS | APK-lab unique CORE/INTERFACE qualifiée sur émulateurs API29/35 ; portée privée et synthétique |
| G3 | BLOCKED | Conversation avec un vrai LLM local et libération qualifiée |
| G4 | BLOCKED | SAF, recherche documentaire Android et citations réelles |
| G5 | PARTIAL | Consommation SERVICES réelle dans l'application intégrée |
| G6 | PARTIAL | Lifecycle CORE/UI instrumenté ; ressources natives et autorités des autres modules non qualifiées |
| G7 | PARTIAL | API29/35 synthétiques et régression historique réussies ; E2E documentaire/LLM réel absent |
| G8 | NOT_RUN | Aucun appareil personnel autorisé ou installé |

UNIFIED : validateur PASS, 41 tests audit/contrats, 23 registre, 30 sauvegarde
PASS, aucun échec/erreur/saut. Ces 94 cas Python ne sont pas additionnés aux
tests Android ou aux campagnes anciennes. Les résultats hôtes sont conservés
dans `/workspace/m50-s1b-*-tests.log`.

Les licences de projet ne sont pas établies ; l'autorisation porte sur la
compilation privée de laboratoire, sans relicenciement ni diffusion de produit.
Les injections de pannes sont synthétiques et les autres modules restent OFF.
**M50 NON ATTEINT** ; aucune qualification physique ou native n'est déduite.

Retour arrière : abandonner les nouvelles PR/branches et retirer uniquement
`fr.jarvis.lab.m50s1` de l'émulateur. Aucun main, historique, stockage, permission,
modèle, protection ou appareil personnel modifié.

Mission suivante proposée après réception S1B : **S2, parcours documentaire
NEXUS/SERVICES en lecture seule**, avec compatibilité Android et références
producteurs revérifiées. Tout nouveau pilote SQLite, migration, modèle natif,
transport sensible ou installation personnelle exige sa décision distincte.
