# JARVIS — M50 : convention de progression et critères de réception

## 0. Ce que le « 50 % » signifie

**M50 = jalon de pilotage de la V1, non mesure scientifique de l'avancement de toute la vision JARVIS.** Les PR et CI de pré-fusion montrent des fondations techniques, pas un pourcentage de produit intégré. Le nombre 50 % ne sera affiché qu'en tant que *jalon V1 M50 atteint* après la satisfaction **de tous les critères indispensables ci-dessous**. Tant que ces preuves manquent : **M50 NOT_ACHIEVED**, progression globale NON_QUANTIFIÉE. Ne jamais additionner les nombres de tests de campagnes répétées.

**Utilisateur cible :** assistant personnel local, hors ligne en exploitation. Première tranche intégrée utile : interface de conversation, CORE arbitre unique, un moteur de génération local réellement qualifié et consultation TXT/PDF/CSV avec citations démontrées. Les extensions VOICE/EVOLUTION/veille connectée peuvent être présentes sous capacité optionnelle/OFF sans empêcher cette tranche. Si le LLM natif ne peut pas fonctionner, il s'agit d'un **pilote documentaire**, pas d'une conversation IA réelle ni de M50.

## 1. Topologie de transition retenue pour les essais (proposition réversible)

```text
[Android launcher: JARVIS lab / testOnly, aucune installation personnelle]
        [INTERFACE: chat, sources, capacités, avatar idle]
                      |
        [CORE: session, prompts, admission, révocation]
              /            |             \
       [LLM native]      [NEXUS]       [SERVICES]
       1 backend        TXT/PDF/     recherche doc
       1 budget          citations     CSV lecture
            [VOICE: optionnel, seul PCM/état qualifié]
            [EVOLUTION: monitor-only, opt-in OFF]
    [UNIFIED: lock source + contrat + CI + release gate, pas runtime]
```

- **Étape 1 : fédération des dépôts de développement** avec SHAs immuables, copies temporaires en CI, licences et namespaces vérifiés, build documenté et rollback ; aucun réseau pendant l'utilisation Android.
- **Étape 2 : APK unique de laboratoire** testOnly, variante indépendante, construction déterministe. Chercher d'abord une liaison **in-process** UI→CORE au sein de cette APK : ne pas inventer un IPC Binder/signature si inutile dans ce parcours. Les anciennes APK interprocessus restent préservées et déconnectées tant qu'un transport signé n'a pas été approuvé.
- **Étape 3 : preuve end-to-end sur émulateur** et même matériel cible autorisé, sans code test déguisé en runtime. Les composants non disponibles répondent UNSUPPORTED; ils ne se chargent pas silencieusement.
- **Étape 4 : monorepo modulaire définitif** seulement si comparaison fédération/monorepo et stratégie de conservation des historiques approuvées séparément. Une application unique ne nécessite pas nécessairement un dépôt unique.
- Aucun import/renommage Gradle, nouveau JNI, signature APK, permission, migration ni déploiement sensible sans décision explicite.

## 2. Les huit gates de réception M50 (tous obligatoires)

| Gate | Condition de succès | Refus / limites initiales |
|---|---|---|
| **M50-G1 — provenance** | 8 SHA40 revérifiés, tree hash, licence/SBOM, branche/PR/CI source, lock approuvé pour le labo, diff sans collision, aucun code abandonné | CANDIDATE-SOURCES.json n'est pas un release lock |
| **M50-G2 — application unique** | Android APK-lab installable sur **émulateur** API cible choisie, appId distinct, build reproductible et manifest inspecté, une Activity JARVIS, CORE unique | Aucun build unifié démontré aujourd'hui |
| **M50-G3 — conversation réelle** | UI→CORE→un LLM local réellement chargé et générant texte, flux ACK/chunks/stop, annulation et sortie sans faux READY, borne mémoire | LLM API29 vs CORE API24, JNI/unload encore incertains |
| **M50-G4 — documents réels** | Sélection SAF réelle TXT/PDF par utilisateur, index/recherche disponible sur plateforme de test, résultat sourcé URI/grant/version/page/offset/hash sans invention, grant révocable | FTS5 API24/25 ne doit jamais devenir SUPPORTED par défaut |
| **M50-G5 — SERVICES utiles** | documents.search et data.csv.normalize sans écriture ni connexion Internet, CSV 0.10+0.20 exact, permissions minimales, contrats CORE vérifiés | `SAF_EXPORT_UNQUALIFIED` reste OFF ; export non requis pour M50 |
| **M50-G6 — sécurité/lifecycle** | provenance réelle du CORE ou frontière in-process démontrée, pas de consentement issu LLM/UI, refus replay/revoke/timeout/crash; pas de deuxième modèle, cas UNKNOWN persistants, données privées intactes | ADR-002 principes acceptés ≠ permission de mutation |
| **M50-G7 — CI/Android** | matrice tests modules et consommateurs, JVM/Robolectric et véritables instruments émulateurs (API de l'APK-labo documentée, au moins API29 et API35; API24/25 refus/fallback séparés), aucune régression, inspecter SDK/ABI et fonctionnement hors ligne | Build APK/états simulés ≠ E2E ni test physique |
| **M50-G8 — appareil, reprise** | sur **un appareil explicitement autorisé**, installation uniquement d'une variante isolée approuvée, test offline, RAM/thermique/latence mesurés, fermeture/reprise/backup/rollback synthétiques puis procédure non destructrice vérifiée | Aucun appareil physique autorisé/testé dans ce dossier |

Chaque gate a : owner, test positif+négatif, SHA, suite/runner, compte PASS/FAIL/SKIP/NOT_RUN, artefact et personne validant. Les cas non exécutés sont NOT_RUN, pas 0 FAIL suffisant. M50-G8 ne peut pas être remplacé par un test hôte.

## 3. Ordre de travail et parallélisation

**Vague A — indépendante et immédiatement autorisée** : inventaire de provenance/branches, alignement Gradle sous copies, produit testOnly sans données, port CORE/UI purement injecté in-process OFF par défaut, consommateur CSV en lecture seule, tests NEXUS/LLM backend réels *si environnement de laboratoire autorisé*, diagnostics/contrats. Le matériel personnel, transport externe et migrations restent exclus.

**Vague B — convergence** : intégrer uniquement les modules dont les gates producteur sont réellement PASS, tests consommatrices CORE/UI et E2E hors ligne ; une fonction absente est affichée « indisponible », pas simulée. Garder le mot `READY` réservé aux preuves qualifiées.

**Vague C — décisions bloquantes à solliciter séparément** :
1. Choix explicite d'assemblage technique sur branche de laboratoire, licences/appId/SDK/ABI, après revue des diffs.
2. Accord distinct sur nouveau backend SQLite/natif et tout schéma/migration de données (NEXUS).
3. Accord distinct sur transport Android authentifié entre APK **si** nécessaire, signatures/permissions et ACL.
4. Accord distinct sur runtime native LLM nécessitant modification ABI/JNI ou modèle téléchargé.
5. Accord distinct sur instrumentation et installation sur appareil personnel.
6. Accord distinct sur monorepo/import Git puis sur chaque merge main ; **ne pas déduire l'un de l'autre**.
7. Toute écriture SAF ou auto-réparation EVOLUTION est **hors périmètre M50**, à revoir plus tard.

## 4. Interfaces minimales à faire valider

- `CoreSessionKey` : epoch/session/request UUID exacts et génération, budget; jamais confiance sur chaînes déclaratives.
- `ConversationPort` : Submit/Ack/Chunk/Stop/Error/Unknown, seq borné et déduplication, adaptateur in-process ou transport signé approuvé. Aucune réouverture automatiquement après UNKNOWN.
- `DocumentQueryPort` : état de capacité FTS5/literal explicite, source persistante sous grant seulement, page et unité d'offset, UTF-8 digest, version, réouverture/revocation; absence de source = UNSUPPORTED.
- `ToolsReadPort` : catalogue de deux outils Android réellement qualifiés, quota, bornes de durée, aucune méthode d'écriture ; mémoire personnelle uniquement avec consentement explicite hors M50.
- `LocalGenerationPort` : un seul moteur/tokenizer et budget, provenance native, timeout/annulation/non-retry, réserve CORE; gardes thermiques Android.
- `VoiceEventPort` optionnel : IDLE/PLAYING_ESTIMATED/UNKNOWN, ne prétend pas attester la perception/audio humain.
- `TelemetryPort` optionnel : uniquement enums et métriques expurgées, OFF par défaut.

Les noms ci-dessus sont **des noms de contrat proposés**, non des classes existantes ou déployées. Codex doit comparer avec les API réelles et éviter tout nouveau DTO incompatible.

## 5. Compatibilité Android : décisions pragmatiques

- Pour première APK-laboratoire **unifiée CORE+UI+LLM**, viser une cible de test **API29+** sans relever les minSdk des **applications historiques** CORE API24, UI/VOICE API26, NEXUS/SERVICES API24. Les versions inférieures peuvent garder un mode dégradé explicite, à tester séparément. Cette option n'autorise pas une migration de manifeste productif.
- Conserver un LLM interchangeable et une variante future mini-PC plein régime. Pas de deuxième modèle lourd simultanément sur Android.
- Sur POCO et Redmi : admission mémoire/sécurité thermique avant fonctionnalités avancées. La voie locale doit rester utilisable après extinction du réseau.
- Les 23 skips VOICE et le cas ZIM absent NEXUS restent documentés et ne sont pas effacés par la qualification d'une APK-labo.

## 6. Livraison de M50 et rollback

Artéfacts obligatoires : `docs/m50/RELEASE-EVIDENCE.json`, `docs/m50/M50-READINESS.md`, lock source SHA+tree final, rapports Gradle / XML tests authentiques, manifs APK/lab, liens GitHub Actions, matrice de compatibilité, journal des décisions, manuel sauvegarde/restauration.

Ne jamais annoncer « JARVIS 50 % » tant que M50-G1..G8 ne sont pas PASS. Pour tout FAIL/BLOCKED/NOT_RUN, publier le rapport et ouvrir une mission dédiée à la cause; ne pas modifier les chiffres à la main pour franchir un seuil.

Rollback : suppression de la variante de labo sur émulateur et retour aux SHAs sources sur branches indépendantes; aucune DB personnelle et aucun dépôt legacy écrasés. Pour des données persistantes futures, restauration validée sur copie avant toute migration.

## 7. État de départ réellement observé (29 octobre)

- Huit branches M50 ont été créées sur SHAs précédemment qualifiés, sans merge main.
- UNIFIED #15, CORE #25, SERVICES #11 : gardes ADR-002 lot4 synthétiques réussis au SHA. Ce ne sont pas des preuves d'un protocole durable exécuté.
- UNIFIED #16 `d2c1daf...` est une branche parallèle, **pas** ancêtre automatique du #15 `deccfb...`. Évaluer son diff/provenance, ne pas cherry-pick sans revue.
- NEXUS #10, UI #12, LLM #6, VOICE #25, EVOL #5 restent branches indépendantes et leurs résultats historiques s'appliquent aux SHA exacts, non à un futur APK.
- **Aucune preuve d'APK unique fonctionnelle, aucune qualification physique, aucune décision de monorepo/import Git définitif.**
