# Lot3 — livraisons propriétaires vérifiées

Observation : 28 octobre 2026 UTC. Tous les pushes ci-dessous ont une tête distante
égale au SHA local, sans force et sans fusion. Les arbres sont relevés par Git.
PR nouvelles non créées : API GraphQL refusée; les corps et comparaisons sont prêts.

## CORE — CORE-PF-02

Branche `codex/prefusion-lot3-core`, base
`af6fe97e2d3f1cded76a4c0e28754b2c21272692`, commit
`aed84860f2ca85713140a687ba7d86efc0203dc8`, arbre
`f6bb7d1756d2192963a6125acb1a03883cf64c99`.

Port metadata read-only de laboratoire, borné, corrélé et fail-closed. Il ne
raccorde pas les APK. **629 tests JVM réussis, zéro échec/erreur/saut** :
Debug510, MVP2 53, fixture36, integration-lab30. Dont602 historiques conservés et27
nouveaux. Builds Debug/MVP2/MVP3 et3Lint réussis;27/37/37 warnings historiques,
zéro Error/Fatal. JNI et admission inchangés. Min24 et APK sans INTERNET vérifiés.
CI exacte [40667196196](https://github.com/bubth720/JAVIS-Local-v2/actions/runs/40667196196)
IN_PROGRESS à09:49UTC; résultat non anticipé.
[Rapport et inventaires](https://github.com/bubth720/JAVIS-Local-v2/blob/codex/prefusion-lot3-core/docs/prefusion/lot3/REPORT.md).

## INTERFACE — UI-PF-02

Branche `codex/prefusion-lot3-interface`, base
`c14eebdbce8b2fda024043d6abd1e84bc719f113`.
Premier commit `a1d9db6cf31c41256f96508147606029286ca343`;
outillage de diagnostic complété jusqu'à
`cc5d860f91c0c84c3513419cf3c80ffa0354bfd4`.

Treize nouveaux androidTests compilés, aucune source historique de production
modifiée.217 JVM et builds debug/androidTest/Lint réussis; CI historique Android
SUCCESS au commit intermédiaire `0cbde77dc36f5537af0442c077b4f7d4acfd9eaa`
([40665765393](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40665765393)).
Neuf tests Python du diagnostic public réussis au dernier commit. Garde114 fichiers
historiques byte-identiques PASS. Capture, UID/certificat réels et appareil
personnel non qualifiés.

**Échec réel conservé** : campagne instrumentée
[40665765400](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40665765400)
au0cbde77, API26 et35 échouées (`/usr/bin/sh exit1`), détail des XML/logs protégé
par connexion GitHub. Le premier run40664650866 avait déjà API26 en échec.
Aucun test supprimé ou assertion relâchée; des annotations bornées exposent
maintenant compteurs et phase/exitcode synthétiques, sans données privées.
Dernière campagne [40667162403](https://github.com/bubth720/JARVIS-INTERFACE/actions/runs/40667162403)
aucc5d860 en cours lors de cette capture. La cause exacte reste à établir, pas de
qualification émulateur annoncée. Trois anciens tests à pack privé non autorisé
restent NOT_RUN dans cette sélection publique22/API puis2 après restart.
[Rapport](https://github.com/bubth720/JARVIS-INTERFACE/blob/codex/prefusion-lot3-interface/docs/prefusion/lot3/REPORT.md).

## SERVICES — SERV-PF-02

Branche `codex/prefusion-lot3-services`, base
`7c9b0efe10187edadbf8555fefe4c98702fa5e98`, commit
`cfb5f117edc72acd8d5967980d3dfc9dfbf2903f`, arbre
`779ecc5e4590e38fd2ce315262e89eff27eec149`.

Banc de14 nouveaux tests de protocoles simulés, zéro modification de production.
121 JVM et40 Robolectric réussis, zéro échec/erreur/saut. AAR, APK androidTest
adaptateur et diagnostic, Lint PASS;24sources compilées contre API24,2locks
vérifiés, banc absent de l'AAR. CI
[40665178466](https://github.com/bubth720/JARVIS-SERVICES/actions/runs/40665178466)
SUCCESS au SHA exact, durée9m21. Les sept jobs sont SUCCESS, dont les quatre matrices API24/25/26/35;
le validateur CI inchangé exige15cas/API. Les XML protégés n’ont pas été relus
indépendamment : [preuve sélectionnée](SERVICES-CI.json).
Les compteurs locaux sont distincts des campagnes distantes; aucune qualification physique ou durabilité réelle déduite.
ADR002 non adoptée, export production OFF.
[Rapport](https://github.com/bubth720/JARVIS-SERVICES/blob/codex/prefusion-lot3-services/docs/prefusion/lot3/REPORT.md).

## NEXUS — NEX-PF-02

Branche `codex/prefusion-lot3-nexus`, base
`b2b899c8cce73ee0763bf6896fb9ceffe62c2bc6`, commit
`b5f89c0db8fa5ad96ed43697b5ffdb4d33ca757a`, arbre
`3979cf5b8cdb2ee5e02ac5a8ffc00505114f156d`.

Matrice FTS synthétique exécutable et packages SAF de test séparés, opt-in
`withPrefusionLab`, jamais dépendances par défaut. Provider protégé par
MANAGE_DOCUMENTS, sans permission ajoutée au consommateur de production.
95 JVM et71 Robolectric réussis, zéro échec/erreur/saut. Autres :15tests Pythonlot3,
6préservation,10SQLhôte,18ZIM,7Node réussis; **1ZIM SKIP** (archive non fournie).
AAR, APKs de test/baseline et3Lint réussis (0erreur/4warnings documentés).
Compilation réelle contre stubs API24 PASS, distincte d'un émulateur.
Cinq tests Android compilés; exécution locale NOT_RUN sansKVM.

Le premier build a révélé un conflit de version du plugin Gradle, corrigé sans
modifier production. Le routage de l'ancien workflow a été adapté uniquement au
lot3 : garde actuelle stricte et garde historique sur SHA exact archivé, tests
historiques conservés. Aucun backend SQLite natif ni migration ajouté; RAG reste
UNSUPPORTED. CI [40666775515](https://github.com/bubth720/JARVIS-NEXUS/actions/runs/40666775515)
IN_PROGRESS au SHA exact lors de l'observation09:47UTC.
[Rapport](https://github.com/bubth720/JARVIS-NEXUS/blob/codex/prefusion-lot3-nexus/docs/prefusion/lot3/REPORT.md).

## Comparaisons pour créer les PR brouillon

Base de chacune : `mission/prefusion-lot3-20261027`, jamais main.

- [CORE](https://github.com/bubth720/JAVIS-Local-v2/compare/mission/prefusion-lot3-20261027...codex/prefusion-lot3-core?expand=1)
- [INTERFACE](https://github.com/bubth720/JARVIS-INTERFACE/compare/mission/prefusion-lot3-20261027...codex/prefusion-lot3-interface?expand=1)
- [SERVICES](https://github.com/bubth720/JARVIS-SERVICES/compare/mission/prefusion-lot3-20261027...codex/prefusion-lot3-services?expand=1)
- [NEXUS](https://github.com/bubth720/JARVIS-NEXUS/compare/mission/prefusion-lot3-20261027...codex/prefusion-lot3-nexus?expand=1)
- [UNIFIED](https://github.com/bubth720/JARVIS-UNIFIED/compare/mission/prefusion-lot3-20261027...codex/prefusion-lot3-unified?expand=1)
