# UNIFIED — D4-02C : bilan de convergence

Date : 16 octobre 2026. Dépôt : bubth720/JARVIS-UNIFIED.
Branche dédiée : `audit/d4-02c-core-llm-convergence`.
Base vérifiée : **52a44fb6cf01623a8c5d96edc5d2bbac76abd9a1**,
`design/d4-02-ownership-mapping`. Le SHA du commit de livraison est fourni dans
le compte rendu de livraison et consultable par `git rev-parse HEAD` sur cette
branche ; ce document ne prétend pas contenir sa propre empreinte Git.

## Conclusion et références retenues

CORE renforcé **29646448c80568d868a702192df761fc9d7a896d** contient
07cd282 : deux commits ajoutent/durcissent l’admission au processus et la
corrélation des libérations. Cette protection ne couvre pas un autre processus.

LLM natif **daa46432e847ed9613dc403045498e27281eff42** est recommandé pour
la future fixture. Il diverge de c4e7611 : base003C commune, quatre/sept commits
exclusifs, 27 chemins différents ; les quatre fichiers de domaine P2 sont
identiques. Pas de fusion automatique. Les SHA complets, manifestes de fichiers,
liens immuables et filiation figurent dans [REFERENCES.md](REFERENCES.md).

**Aucune intégration CORE↔LLM opérationnelle démontrée.** Le JNI P2 existe et a
une preuve native Linux ; les sessions CORE, l’identité IPC, les reçus et
l’admission entre applications ne sont pas raccordés. Aucun essai Android
physique exécuté ou déduit d’une compilation/CI.

## Écarts bloquants et proposition commune

- CORE expose contexte aplati et métadonnées de sources sans révision ; P2 exige
  historique structuré et références documentaires versionnées. Refuser une
  conversion avec perte ; aucune révision ou provenance inventée.
- Identifiants CORE ne couvrent pas toute la clé P2 (epoch, génération, opération,
  annulation, autorisation et bail). Mapping explicite et corrélé indispensable ;
  UUID d’autorisation ne constitue pas une permission Android.
- SYSTEM P2 reste un rôle SYSTEM configurable. Planificateur P2 et JNI composent
  différemment la politique fixe : leur composition directe la dupliquerait.
  Retenir un rendu canonique compté et généré par le même tokenizer/template.
- Budget CORE en octets conservateur ≠ comptage natif. Le compteur JNI exposé au
  harnais ne couvre pas encore le port Kotlin complet/history/docs. Faire respecter
  aussi le contexte demandé, pas seulement celui chargé ; aucune troncature cachée.
- Réponse texte, arrêt demandé, fin réelle et modèle déchargé sont distincts.
  Ne pas utiliser nativeDone=true par défaut comme preuve ; adapter reçus,
  erreurs, réponses tardives et unload ACK exact/idempotent au bail.
- P2Lifecycle et backend possèdent des acquisitions séparées : les empiler risque
  double réservation/refus BUSY. Observer les baux réels du backend, sans second
  propriétaire lourd ni libération fictive. Quarantaine et panne restent bloquantes.
- Admission CORE locale ≠ arbitre interprocessus ; identité, protocole de reprise,
  limites Binder et compatibilité CORE24/LLM29 restent à valider.

La [matrice](MATRICE_CONVERGENCE.md) couvre les dix familles demandées, avec
responsable et test attendu. [ECARTS_ET_CORRECTIONS.md](ECARTS_ET_CORRECTIONS.md)
décrit le mapping et le contrat **proposé**, sans modifier les schémas v1.
Le premier parcours recommandé est texte synthétique SYSTEM + question, sans
contexte réel. Un contexte non représentable est refusé, jamais effacé.
CORE garde orchestration/permissions, LLM l’inférence et le droit de refus matériel.
Un seul moteur lourd résident, mode historique/API24, protections et hors-ligne
sont préservés ; aucune donnée ni fonction historique supprimée.

## Vérifications réellement exécutées

Environnement local : Linux x86_64, Python3.12.14. Commandes exécutées sur cette
branche documentaire, avec les scripts/tests inchangés de la base :

```text
python3 -m unittest discover -s tests -v
Ran 27 tests — OK
python3 -m unittest discover -s registry/tests -v
Ran 23 tests — OK
python3 -m unittest discover -s backup_prototype/tests -v
Ran 30 tests — OK
```

Total : **80 réussis, 0 échec, 0 erreur, 0 ignoré**. La suite de sauvegarde utilise
ses fixtures ; aucune donnée utilisateur traitée. Ces tests valident UNIFIED,
pas les applications ni le futur IPC. Sorties intégrales conservées localement
dans `.audit-cache/d4-02c/{audit-contracts,registry,backup}.txt`, métadonnées tests.json.
Contrôles complémentaires exécutés avec succès :

```text
python3 scripts/validate_unified.py
{"contracts": 5, "invalid_examples_rejected": 5, "repositories": 9, "valid_examples": 5}
python3 registry/scripts/update_registry.py --validate-only
Registre valide : 9 dépôts, 16 missions.
git diff --check
code retour 0, aucune sortie
```

Vérification documentaire ciblée : six livrables présents, 38 liens vérifiés
(objets Git pour les liens source immuables, fichiers locaux pour les liens
relatifs, observations des pages Actions pour les runs), 18 empreintes SHA-256
de blobs source recalculées conformes. Diff des chemins protégés contre52a44fb
vide : contrats/v1, registre, tests, scripts, sauvegarde, workflows, AGENTS et ADR.
Résultats détaillés dans final-checks.json local ignoré. Ce contrôle garantit
l’existence des objets cités, sans prétendre avoir testé l’accès HTTP à chaque
page blob. L’état de publication et le SHA final sont donnés à la livraison.

### Preuves distantes distinctes

- Git : quatre commits demandés vérifiés contre les branches distantes et objets
  source ; filiation/diffs calculés. Liens de code vérifiés contre ces objets.
- CORE : 174 tests initiaux, 187 renforcés **rapportés dans les documents source**,
  JVM/Robolectric et API native simulée. Non réexécutés ici ; aucune conclusion
  GitHub Actions attachée au SHA renforcé vérifiée. Workflow build-apk existant
  n’est pas une preuve de suite de tests et n’a pas été déclenché.
- LLM : pages publiques Actions HTTP200 et champ Status Success observés pour
  [38928638903](https://github.com/bubth720/JARVIS-LLM/actions/runs/38928638903)
  et [38963365435](https://github.com/bubth720/JARVIS-LLM/actions/runs/38963365435).
  Elles portent sur 74093e37 et 0f13573e respectivement ; les différences vers les
  têtes c4e7611/daa46432 sont documentaires uniquement. Annotations : 83 domaine +
  21 app simulée +1 natif, puis 87 domaine +25 app simulée +1 natif ; zéro
  échec/erreur/saut indiqué. Le harnais JNI P2 Linux est décrit par source/rapport
  et workflow réussi ; ses logs détaillés/JUnit n’ont pas été téléchargés ici.
- API api.github.com : tunnel HTTP403 observé ; pas de contournement ou tentative
  de jeton. Pages web et Git accessibles séparément. Pas d’inférence d’absence
  de tests à partir du refus API. Aucun APK, modèle ou artefact CI téléchargé.

Les caches sont ignorés et ne sont pas des livrables publiés ; les références et
résultats utiles sont consignés dans ces documents, sans dépendance au cache.

## Décisions qui nécessitent votre accord

L’ADR-001 reste **approuvée avec précisions** pour l’orientation seulement.
O1/O2/O4 restent dans leur périmètre existant ; aucun changement implicite.
O3 demeure **PROPOSÉE, NON APPROUVÉE**. Voir
[DECISION_O3_PROPOSEE.md](DECISION_O3_PROPOSEE.md) :

1. T1 : Bound Service/Binder et interface typée/AIDL dans des fixtures isolées,
   ou alternative bibliothèque commune étudiée sans relever CORE minSdk.
2. T2 : identité UID/certificats et clé de test commune ou certificats appairés ;
   aucune modification des signatures/installations historiques.
3. T3 : emplacement et participants de l’arbitre ; recommandation processus
   fixture CORE, baux physiques LLM conservés, sans prétendre contrôler tout Android.
4. T4 : récupération après mort/ACK perdu, journal technique minimal et preuves
   de fin/libération ; UNKNOWN ne permet aucune nouvelle charge ni reset implicite.
5. T5 : contrat canonique proposé et pilote texte synthétique à contexte vide,
   puis autorisations de code distinctes par dépôt. Aucun v1 approuvé réécrit.

## Ordre recommandé et fichiers livrés

Après accord technique, transmettre **exactement deux missions** décrites dans
[MISSIONS_SUIVANTES.md](MISSIONS_SUIVANTES.md) :

1. LLM : fixture adaptateur/endpoint sécurisé, rendu/comptage natif cohérents,
   reçus et port de broker ; refus si arbitre absent, pas de preuve E2E à ce stade.
2. CORE : fixture client et broker retenu, session/réponse corrélées, mode historique
   intact ; vrai parcours à deux processus et JNI, ou E2E explicitement non exécuté
   si les moyens/autorisations manquent. Linux seul ne prouve pas Android inter-APK.

Livrables : les six Markdown de docs/D4-02C et un lien dans README. Aucun fichier
applicatif, schéma v1, registre historique ou dépôt extérieur modifié. Pas de merge,
IPC, service exporté, installation, migration ou changement des seuils matériels.
Publication autorisée exclusivement sur la branche dédiée, sans force-push ;
aucune PR ni fusion requise par cette mission. Prochaine étape : votre validation
des choix techniques, avant toute mission de raccordement.
