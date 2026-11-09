# JARVIS — REUSE FIRST R1+ — réception de laboratoire

Observation : 8–9 novembre 2026 UTC. **Les développements indépendants sont livrés ; Android et le parcours vertical restent BLOCKED.** Aucun moteur, profil vocal, contrat canonique, base personnelle, source métier historique ou architecture n'a été remplacé. Aucune fusion, autorité supplémentaire ni installation personnelle.

## Accès aux preuves

- [Audit des huit modules](AUDIT.md), [inventaire exhaustif des métadonnées récupérées](INVENTORY.json).
- [Matrice REUSE FIRST : 19 comparaisons](REUSE-MATRIX.md), [JSON](REUSE-MATRIX.json), [CSV](REUSE-MATRIX.csv), [sources amont épinglées](UPSTREAM-SOURCES.json).
- [Diagnostic Android et campagne C1 close](ANDROID.md).
- [Mesures et limites](PERFORMANCE.md), [commandes et résultats](TESTS.md).
- [Feuille de route et critères de passage](ROADMAP.md).
- [Réception vérifiable](RECEIPT.json), [empreintes des preuves](EVIDENCE-SHA256.json), [sauvegardes initiales](BACKUP-MANIFEST.json).

| Composant | Résultat réellement observé | Limite de qualification |
| --- | --- | --- |
| CORE M50 | PASS : 641 exécutions JVM/Robolectric, 20 Python | Android matériel, LLM réel et chaîne globale NON QUALIFIÉS |
| UNIFIED | Coordination documentaire et vérification, aucun runtime ajouté | Anciennes portes et ancien score inchangés |
| LLM M51 | PASS : 247 tests hérités + 12 audit ; verdict de sécurité **NO_GO** | G-A/G-ROOT fermées, G-B non validée, aucun poids/JNI/génération |
| VOICE | 237 PASS, 23 SKIP parmi 260 exécutions JVM | Synthèse réelle, audition, interruptions et qualité Android NON QUALIFIÉES |
| INTERFACE M51-R1+ | PASS : build, 36 JVM et 36 Python après correctif ; quatre APK expérimentaux | Android **BLOCKED** ; candidat C1 NOT_RUN ; aucun rendu M54 activé |
| SERVICES | PASS : 134 tests JVM desktop | Actions Android/productives BLOCKED |
| NEXUS M53+ | PASS : 108 JVM + 10 Python ; adaptateur test-only et SQLite réel | Autorité CORE, Android/SAF et raccordement productif BLOCKED |
| EVOLUTION | PASS : 40 JVM et démonstrations de politique | Exécution de réparation/sandbox NON QUALIFIÉE |
| Avatar M54, dans INTERFACE | PASS : contrôleur existant, 21 JVM + 20 Python | Renderer NOT_IMPLEMENTED, audio/Android NOT_RUN, visèmes UNSUPPORTED |

Les tests reproduisant un défaut ou un refus attendu peuvent passer alors que la capacité reste dangereuse ou indisponible. Les exécutions des variantes ne sont pas des fonctionnalités distinctes. Aucune somme globale n'est présentée comme taux d'avancement de JARVIS.

L'acquis Android **M50-S1B** reste PASS dans son périmètre antérieur : CORE/INTERFACE réels avec réponses synthétiques, six scénarios par API29/35. Son APK et ses rapports ont été récupérés et leurs empreintes vérifiées, sans nouvelle exécution. Il fournit la base CORE/UI à réutiliser ; il ne qualifie pas M51 ou un LLM. Voir [AUDIT.md](AUDIT.md).

## Développements publiés

Branche commune : `codex/reuse-first-r1plus-20261108`. Bases conservées, distinctes des branches principales :

- INTERFACE [PR brouillon #21](https://github.com/bubth720/JARVIS-INTERFACE/pull/21), base `codex/m51-r1-android-stability`, commits `7282fd769d4ab787467d08fd8059b2f1e18ca139` puis `d569ce816cf39191742769afef5b0711bc9a28cd`. Diagnostic borné et refus d'un ANR système réellement capturé ; aucune correction applicative prétendue.
- NEXUS [PR brouillon #14](https://github.com/bubth720/JARVIS-NEXUS/pull/14), base `codex/m53-readonly-preparation`, commit `b7d9d884ddd034e3580a2268fce69ca43030e8c5`. Adaptateur expérimental désactivé par défaut, compilé uniquement dans les tests ; consultations et citations réelles sur corpus M53 synthétique.
- UNIFIED : base `codex/m51-unified-gates`, commit initial `9365e80aab273e22d894a3fcbf055e73c8ff82da` pour les baselines épinglées. La PR de cette branche porte le présent dossier et ses vérifications ; ses commits et son URL sont ceux affichés par GitHub, sans SHA auto-référentiel inventé dans les preuves.

La branche séparée `codex/reuse-first-r1plus-c1-android` reste figée à `7282fd7`. Sa campagne [42524234101](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/42524234101) n'est ni relancée ni réinterprétée comme un succès après la correction documentaire et du parseur.

## Livrables et conservation

Les APK sont des APK de laboratoire `testOnly`, UI locale seulement, sans LLM, avec certificats de debug propres à chaque build. Les SHA-256 et ABI sont dans `evidence/interface-*-build.json`. Les archives Actions expirent normalement après 90 jours ; une copie locale récupérable est fournie séparément avec manifeste et contrôle CRC. Aucune recommandation d'installation sur un appareil personnel.

Huit bundles Git complets initiaux ont été vérifiés. Les bundles peuvent contenir l'historique de profils et de ressources déjà présents : ils restent dans la sauvegarde remise au propriétaire, jamais ajoutés à la PR publique. Les branches anciennes, les profils et les données sont conservés. Les très gros anciens assets CORE sont inventoriés par métadonnées, sans prétendre les avoir tous téléchargés ni réexécutés.

Prochaine priorité : **qualifier un laboratoire Android stable avant JARVIS**, puis documenter précisément la visibilité SAF et ses témoins manquants. En parallèle, examiner séparément le diff LLM sensible et ses portes, sans appliquer le patch ni acquérir de modèle.
