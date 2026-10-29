# JARVIS — MISSION DIRECTRICE M50 (CAP SUR LE PRODUIT INTÉGRÉ)

**STATUT : PLAN PUBLIÉ / EXÉCUTION CODEX NON DÉCLENCHÉE PAR CE FICHIER.**
Dépôt : `bubth720/JARVIS-UNIFIED`. Branche de mission : `mission/m50-integrated-beta-20261029`.
Base UNIFIED : `deccfb709944f72a45f6a524001b1144b6c3b8dc` (lot4, PR#15).
Complément parallèle à comparer sans intégration automatique : UNIFIED#16 commit `d2c1dafd51339c185a758141e353f93f72ecb9fc`.

**Lire d'abord** `docs/m50/ACCEPTANCE-AND-ROADMAP.md`, `docs/m50/CANDIDATE-SOURCES.json` et `docs/m50/M50-READINESS.md` (gates non satisfaits et diagnostics CI NEXUS/LLM). Le premier document définit les huit gates **M50-G1..G8**, obligatoires. Le second est une proposition de références, PAS un lock de livraison approuvé. Ne pas inventer de pourcentage d'avancement actuel.

## Missions déposées dans les propriétaires

Chaque cible utilise **exactement** la branche `mission/m50-integrated-beta-20261029`, fichier `missions/M50-INTEGRATION-2026-10-29.md`. Codex doit créer sa propre branche `codex/m50-*` par dépôt, depuis le HEAD de la branche de mission ; une PR brouillon retour vers cette branche. Ne pas toucher aux anciens PR ou les réécrire.

| Ordre | Module | Mission | Emplacement direct | Référence |
|---|---|---|---|---|
| A | CORE | **CORE-M50-01** | [ouvrir mission](https://github.com/bubth720/JAVIS-Local-v2/blob/mission/m50-integrated-beta-20261029/missions/M50-INTEGRATION-2026-10-29.md) | document d754a6c19e3c · PR CORE #25 |
| A | INTERFACE | **UI-M50-01** | [ouvrir mission](https://github.com/bubth720/JARVIS-INTERFACE/blob/mission/m50-integrated-beta-20261029/missions/M50-INTEGRATION-2026-10-29.md) | document 3a0841266fd6 · PR UI #12 |
| A | NEXUS | **NEX-M50-01** | [ouvrir mission](https://github.com/bubth720/JARVIS-NEXUS/blob/mission/m50-integrated-beta-20261029/missions/M50-INTEGRATION-2026-10-29.md) | document c02a00e8d682 · PR NEX #10 |
| A | SERVICES | **SERV-M50-01** | [ouvrir mission](https://github.com/bubth720/JARVIS-SERVICES/blob/mission/m50-integrated-beta-20261029/missions/M50-INTEGRATION-2026-10-29.md) | document 8d80d09d6aab · PR SERV #11 |
| A/B | LLM | **LLM-M50-01** | [ouvrir mission](https://github.com/bubth720/JARVIS-LLM/blob/mission/m50-integrated-beta-20261029/missions/M50-INTEGRATION-2026-10-29.md) | document 615a2f165d64 · PR LLM #6 |
| B | VOICE | **VOICE-M50-01** | [ouvrir mission](https://github.com/bubth720/JARVIS-VOICE/blob/mission/m50-integrated-beta-20261029/missions/M50-INTEGRATION-2026-10-29.md) | document 642d9c19bcba · PR VOICE #25 |
| B | EVOLUTION | **EVOL-M50-01** | [ouvrir mission](https://github.com/bubth720/JARVIS-VOLUTION-/blob/mission/m50-integrated-beta-20261029/missions/M50-INTEGRATION-2026-10-29.md) | document 84ebc2e2b55d · PR EVOL #5 |

La mission directrice UNIFIED est **UNI-M50-01**. Elle ne publie aucun runtime de communication.

## Exécution UNI-M50-01 — sous-lots courts

### U0 — Vérifier, ne rien fusionner
Relire les huit HEADs des branches mission; récupérer arbres SHA, PR, CI et décisions. Calculer les écarts d'ascendance entre UNIFIED lot4 #15 et complément lot3 #16. Établir le DAG, aucune reprise aveugle de code divergent. Vérifier que les huit dépôts conservent leurs `main`/branches par défaut et qu'aucun historique/schéma n'a été remplacé.

### U1 — Intégrateur fédéré reproductible (source uniquement)
Sur nouvelle branche UNIFIED, écrire **un plan exécutable de build temporaire** qui référence des SHAs complets et refuse versions/licences/ABI inattendus, mais ne change aucun module original. Réaliser revue des wrappers Gradle/JDK, Kotlin/AGP et manifestes. Si l'environnement n'autorise pas le checkout multi-repo, fournir le blocage et CI locale/remote au lieu de déclarer assemblage réalisé.

### U2 — Contrats de première tranche
Comparer interfaces existantes, écrire mapping par owner : CORE unique session/permissions ; UI simple client ; NEXUS documents et citations exactes ; SERVICES lecture/CSV ; LLM un moteur local ; VOICE et EVOLUTION facultatifs. Définir un adaptateur **in-process** pour une éventuelle APK-lab unique avant de créer du Binder externe. Un port in-process ne prouve pas l'authentification d'une autre APK. Ne pas activer de permission, signature ni write SAF.

### U3 — APK de laboratoire réellement intégrée (sous gate)
Après **revue de faisabilité et autorisation spécifique pour les changements sensibles**, adapter sous nouvelles sources/variants isolés une seule application de démonstration Android, un seul CORE, sources synthétiques et un seul vrai moteur natif. Ne pas renommer un APK historique ou changer son minSdk. Les modèles natifs, bibliothèques/documents et actions non qualifiés restent OFF. Si les changements nécessitent import de sources/ABI/permissions, STOP et solliciter accord avant exécution.

### U4 — Preuve bout-en-bout / sécurité
Démontrer *réellement*, sur émulateur autorisé : sélectionner TXT/PDF via vrai SAF → construire résultat/citation NEXUS vérifié → CORE répond avec UN seul LLM local si disponible → INTERFACE montre réponse + source, CSV local normalisé par SERVICES (sans écrire). Scénarios : réseau coupé, provider revocation, faux READY/replay, crash/restart/UNKNOWN, taille limite, prompt injection documentaire, annulation et mémoire. **Tout composant qui manque conduit à NOT_RUN/BLOCKED, non à un résultat mock annoncé fonctionnel**.

### U5 — Gates de réception
Pour chaque M50-G1..G8, renseigner owner, SHA + tree, tests JVM/Robolectric/Android/physiques, captures non personnelles, version API/ABI, nombre de PASS/FAIL/SKIP, mode avion, températures et mémoire si instrumentées. N'afficher « M50 atteint » qu'après tous PASS, demande de revue utilisateur incluse.

### U6 — Consolidation (sans merge)
Proposer stratégie fédération→monorepo modulaire, conservation historiques/licences/provenance, dépendances changées et per-module CI. Documenter plan de migration sur **copies synthétiques** puis revue utilisateur. Toute fusion dans main, y compris un PR unifié de coordination, demeure interdite sans validation explicite.

### U7 — Livrables et restitution
Publier `docs/m50/M50-READINESS.md`, `docs/m50/RELEASE-EVIDENCE.json` avec statut de chaque gate, plan de tests et commandes exactes, scripts de bootstrap/check optionnels et PR brouillon. Rapport : module, mission, branche, commit, suite test, risques, rollback, prochaine action. Un changement de contrat gelé ou licence nécessite une demande formelle avant toute réalisation.

## Ordre d'exécution recommandé et règle de STOP

- **Parallèle tout de suite :** CORE contrat passif, UI démonstrateur, NEXUS capacité de recherche réelle, SERVICES CSV read-only, LLM JNI/port et UNIFIED outil de provenance.
- **Après leurs preuves :** assemblage de la variante APK-lab, E2E et vérification sur émulateurs.
- **Optionnel hors chemin critique :** VOICE synthèse locale et EVOLUTION observation, sans activer collection/auto-réparation.
- **Après décisions explicites :** nouveau driver/migration NEXUS, modification JNI/ABI, transport signé inter-APK, installation appareil, et enfin éventuel import monorepo/merge main.

Aucune suppression de tests, faux certificat, simulation présentée comme réel, faux « 50 % », transfert personnel, activation d'écriture ou réseau obligatoire au runtime. Les échecs CI doivent être réparés sans désactiver les gardes historiques; se limiter aux exceptions documentaires strictes lorsqu'un garde n'autorise pas le nouveau chemin.

## Message court à coller dans Codex

« Dans bubth720/JARVIS-UNIFIED, branche mission/m50-integrated-beta-20261029, lis missions/M50-INTEGRATION-2026-10-29.md. Coordonne les 7 missions liées sur leurs branches, démarre les phases sûres et les tests en PR brouillon. Construis les preuves vers M50, ne réclame 50 % qu'après les 8 gates. Aucun merge main, transport ni migration sensible sans mon accord. »
