# JARVIS M50-S1 — RECOVERY-01 : publication contrôlée du travail local

**Statut : procédure de reprise uniquement. Aucun des commits locaux listés n'est supposé publié.**
**Priorité : récupérer les travaux existants avant toute nouvelle implémentation.**

Contexte : M50-S1 déjà publiée dans UNIFIED PR#18, branche `mission/m50-s1-bootstrap-20261029`, SHA source du cahier `a67116b44d828b435a7a1a662d3cd0200993e1c1`. Cinq workflows GitHub SUCCESS au SHA source (document de mission seulement). Les patches, logs, SHA256 et modèles de PR ne sont pas dans cette PR et ne doivent pas être inventés.

## Inventaire des sorties locales à récupérer

| Lot | Dépôt de destination | Commit Git local déclaré | Tests locaux transmis |
| --- | --- | --- | --- |
| A1 NEXUS | bubth720/JARVIS-NEXUS | `be70faa41d202d77eb8cf0cc5c831e10cfb020b5` | 18 PASS |
| A2 LLM | bubth720/JARVIS-LLM | `b670181987d39d27e2d0d9574fa448397a38fe42` | 21 PASS |
| A3 CORE | bubth720/JAVIS-Local-v2 | `5da98383ed12cb5a54e896fbe57560bacc432fb5` | 20 PASS |
| U validation | bubth720/JARVIS-UNIFIED | `048fdfc8a693af9b9cdba6a0d145669ed58d630c` | 261 PASS |
| U bilan | bubth720/JARVIS-UNIFIED | `92198ec2cd5c43c866587c0a207fe1226d67e3eb` | validateur PASS |

Ces chiffres sont des résultats déclarés hors GitHub. L'absence du SHA sur GitHub ne prouve pas qu'il n'existe plus dans le clone local. Un patch réappliqué sur une autre base générera un **nouveau SHA**, sans contradiction avec le SHA historique.

## REC-1 — Récupération du bundle

1. Dans la session de développement d'origine, localiser le véritable ZIP/bundle et ses manifestes de fichiers/hash SHA256. Vérifier chacun des artefacts par taille/hash, sans divulguer clés, compte, documents personnels, modèle privé, voix ni traces d'authentification.
2. Contrôler pour chaque dépôt le commit Git local, `git status`, `git rev-parse HEAD`, arbre `git rev-parse HEAD^{tree}`, parents `git show -s --format=%P` et emplacement du patch. **Ne pas déduire un commit à partir du nom de fichier.**
3. Si le clone complet existe et que le commit local est accessible, préférer publier sa branche après validation des références amont. Sinon reconstituer à partir des patches vérifiés, dans un **nouveau clone complet**, sur la base exacte. Interdire `git push --force`, `git reset --hard` sur travail existant et toute réécriture de `main`.
4. Si le bundle n'est accessible ni dans la session de Codex ni ici, STOP et demander l'archive réelle; le résumé textuel ne permet pas de retrouver les diffs ni de publier ces commits.

## REC-2 — Applicabilité et sécurité du patch

Pour chaque dépôt séparément :
- `git fetch` le dépôt autorisé et vérifier SHA base/M50; créer `codex/m50-s1-recovery-<module>` à partir de sa branche `mission/m50-integrated-beta-20261029` (UNIFIED à partir du cahier M50-S1 si approprié).
- Lire `AGENTS.md` et les gardes propriétaires. Faire `git apply --check` avec le patch propre au dépôt, vérifier que le patch n'ajoute ni fichier secret ni changement non approuvé d'AndroidManifest, permissions, JNI, SDK, données ou autorisation de production.
- Comparer le diff avec le clone local d'origine; refuser tout conflit de préimage ou changement non compris, sans `-3`/résolution silencieuse. Ne pas modifier les gardes historiques pour masquer un échec : leur évaluation se fait à leurs SHA historiques et un nouveau contrôle M50 à la branche de récupération.
- Vérifier les tests unitaires et gardes de lot effectivement disponibles, `git diff --check`, tests négatifs (modification d'un fichier protégé, symlink, suppression), rollback simple. Aucun test Gradle/Android NON exécuté ne peut être marqué PASS.

## REC-3 — Publication et PR

- Publier chaque branche **uniquement** dans son dépôt d'origine; PR **brouillon** vers sa branche M50 (UNIFIED vers branche de mission S1 si le graphe le permet). L'ancien commit local peut être conservé s'il a exactement ses objets et parents ; sinon afficher explicitement `source SHA` et `published SHA`.
- Ne pas utiliser de contournement d'authentification GitHub. Si push/API refuse, garder patch et hashes inchangés, documenter l'erreur exacte (sans identifiant sensible), proposer un fichier de récupération à importer dans un environnement autorisé.
- Rapport PR obligatoire : module, branche, parent SHA, HEAD SHA, arbre, fichiers, hashes patches, commandes, tests PASS/FAIL/SKIP/NOT_RUN, statut des gardes, incompatibilités, rollback, prochaine étape. Conserver intégralement les fonctionnalités et preuves historiques.

## REC-4 — CI et débloquage produit

**NEXUS A1 :** résoudre le routage des gardes depuis lot3 vers M50 sans assouplissement général; vérifier JVM + Android-hôte au SHA publié, puis tests d'émulateur seulement s'ils sont réellement lancés.

**LLM A2 :** séparer ancien garde 003E conçu pour son SHA d'une nouvelle campagne M50 sur delta gelé, documenter l'échec préexistant `Protected baseline drift: app/src/main/AndroidManifest.xml`. Ne pas effacer cette preuve, modifier le manifest productif, choisir un modèle ou appliquer le patch natif JNI sans autorisation.

**CORE A3 :** exécuter la campagne réellement propriétaire au nouveau SHA et distinguer les anciens 629 hôtes et les nouveaux tests; aucun droit Android ni AppGraph productif.

**UNIFIED U :** relancer validations après récupération des SHAs propriétaires et maintenir G1/G5/G6 PARTIAL, G3/G4 BLOCKED, G2/G7/G8 NOT_RUN tant que preuves nouvelles indisponibles.

## REC-5 — Déclenchement de l'APK de laboratoire

La phase B de M50-S1 n'est **pas** autorisée par une simple publication des patches. Une fois A1/A2/A3 réellement publiées et CI satisfaisantes, examiner contrats, compatibilité Gradle et manifeste de la variante testOnly, puis construire sur émulateur API29/35 une coquille CORE–INTERFACE avec **simulateur explicitement marqué LAB**. Cette démonstration ne compte ni comme LLM réel ni comme vraie recherche documentaire. Si l'assemblage exige import massif, changement de signature/permission ou modification d'un composant de production, solliciter validation humaine avant.

## Interdictions

Aucune fusion `main`, aucun écrasement de branche/PR, migration, téléchargement de poids privé, installation utilisateur, changement d'autorité ADR-002, activation de transport inter-APK, SAF en écriture, auto-réparation EVOLUTION ou annonce M50 à 50 %. En l'absence du bundle véritable, cette RECOVERY-01 est un plan publié, **pas une récupération des commits**.
