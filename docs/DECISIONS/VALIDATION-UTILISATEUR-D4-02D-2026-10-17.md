# D4-02D — Accord exceptionnel V1 à V5 (fixtures seulement)

**Date de décision :** 17 octobre 2026.  
**Statut :** VALIDÉ POUR LE PROTOTYPE EXPÉRIMENTAL, avec limites explicites.  
**Autorité :** instruction directe de l'utilisateur dans la conversation JARVIS-CENTRAL : « Oui vas-y, fais toutes les validations, tu as mon accord. Pour cette fois-ci. »

## Références figées

- UNIFIED D4-02D : `27e674057a348f8074a86851f4e2c11a933162e9`, documents `docs/D4-02D/`.
- LLM 003E : `030152a5f3d888017ad7a7fe8026f2e2c48e8fd5` (code `5751646acd4a7bb13caaea4b96a4ab3a68ec6adb`).
- CORE 004C : `da40ed7155409b85860a22c1dbbfe35029cea29a`.
- ADR-001 : orientation antérieure approuvée, sans nouvelle portée déduite de cette décision.

## Portée exacte des décisions

**V1 — Approuvé :** évolution **du seul contrat de fixture** `jarvis.fixture.p2/1` vers `jarvis.fixture.p2/2`, tables fermées, négociation et nouveau digest. Conserver /1 figé ; refus des versions/paires/digests incompatibles, sans downgrade silencieux. Le bundle concret /2 et son SHA seront générés par LLM 003F puis soumis à la revue technique avant consommation CORE.

**V2 — Approuvé :** attestation **logicielle bornée** de l'état réellement instrumenté, avec autorité unique par processus, barrière avant toute allocation, vérifications UID/package/certificat Binder, nonce frais et snapshots cohérents. Pas de prétention de preuve absolue de la mémoire Android, ni de preuve OS de mort de processus.

**V3 — Approuvé :** enrôlement explicite d'une **nouvelle paire de fixtures de laboratoire** avec `pilot_id`, certificats/builds épinglés, intention et marqueurs durables. Aucune création artificielle d'état sain à partir d'un journal absent ; pas de réenrôlement automatique en cas de perte, conflit, corruption ou rollback.

**V4 — Approuvé comme paramètre expérimental à qualifier :** défi/attestation, PREPARED, COMMIT durable, ACK exacts et reprise idempotente ; fenêtre de contrôle proposée **5 secondes**, susceptible d'être refusée ou resserrée après tests, jamais convertie en timeout prouvant une libération. `UNKNOWN` et `CLEANUP_FAILED` restent bloquants sans preuves positives ; cleanup retry explicite uniquement dans les cas qualifiés.

**V5 — Autorisation d'exécution séquencée :**
1. **LLM 003F autorisée maintenant** : implémenter /2, le chemin d'attestation et ses tests exclusivement dans `bubth720/JARVIS-LLM`, branche `fixture/003f-bootstrap-attestation`, base vérifiée 003E.
2. **Porte technique obligatoire** : comparer le contrat /2 produit (AIDL, champs/valeurs fermés, SHA, vecteurs, compatibilité /1, sécurité/récupération, tests, code) à D4-02D, documenter toutes divergences. Si divergence substantielle ou garantie manquante : **bloquer CORE 004D et demander une nouvelle décision**.
3. **CORE 004D autorisée conditionnellement** après succès de cette revue, uniquement dans `bubth720/JAVIS-Local-v2`, branche `fixture/004d-bootstrap-reconciliation`, en réutilisant le contrat /2 exact gelé. Aucune modification unilatérale de LLM depuis CORE.

## Contraintes non négociables

- **Aucune fusion dans `main`**, même avec CI verte ; aucune auto-merge.
- Pas d'installation sur POCO/Redmi ou d'autre appareil personnel, pas de déploiement ni d'essai physique sans consentement dédié.
- Aucune suppression/migration de données, aucune clé privée/keystore dans Git ou les logs, aucune re-signature des APK historiques.
- Aucun changement des schémas UNIFIED `contracts/v1` ; ne pas étendre l'ADR ou conclure qu'O3 est une décision de déploiement définitif.
- Pas d'affaiblissement des contrôles RAM, batterie, température, des budgets ou d'activation PLEINE PUISSANCE sur Android.
- Aucun contournement de `RECOVERY_REQUIRED`, `UNKNOWN` ou `CLEANUP_FAILED` ; ni PID, ni simple `hello`, ni mort Binder, ni nouveau processus vide ne prouvent le déchargement.
- Pas d'activation du bouton de génération dans la fixture pendant les deux missions bootstrap ; ne pas revendiquer Binder inter-APK ou E2E natif tant que réellement non exécutés.
- Les tests et validations documentaires ne valent jamais qualification Android physique.

## Livraison et contrôle des missions

Se référer aux objectifs, fichiers, critères B01–B18 et livrables de `docs/D4-02D/MISSIONS_003F_004D.md` et `TESTS_ET_PREUVES.md` du commit cité. Publier uniquement sur branches dédiées, exposer commits exacts et résultats exécutés, distingue tests simulés, Linux JNI et Android. Pour toute modification de périmètre sensible, demander un nouvel accord.

**État au jour de la décision :** orientations et autorisations validées par l'utilisateur ; **aucune réalisation de 003F/004D ni vérification matérielle n'est constatée par cette décision documentaire**.
