# UNIFIED — IDENTITY ID-001B : contrat candidat livré pour revue

Issue3 lue intégralement : https://github.com/bubth720/JARVIS-UNIFIED/issues/3,
HTTP200, updatedAt2026-10-17T12:39:07Z. Mission documentaire et tests de schéma,
**aucun runtime IDENTITY activé**. Date17 octobre2026.
Branche : `design/identity-001b-contract-freeze`.
Base : **1748cb0706fa4b0cfac2df963d82a14195b9d25a**, branche d’approbation
descendante de db63719. Elle conserve la validation de constitution/cible B et
les missions précédentes ; aucune fusion depuis D4-02E ou main.
Le SHA final est remis à la livraison Git ; pas de hash auto-référent inventé.

## Ce qui est figé comme candidat, pas automatiquement accepté

Version **jarvis.identity/1**, révision **001B.1-candidate**. Huit schémas fermés,
enums/styles/bornes/reférences, algorithme canonique, exemples et six vecteurs.

**Digest réel du bundle candidat de14 fichiers normatifs :**
`431b5212f742bd9028477a6a603acf328c414801873efdd529f45b6ed5e619de`.

BUNDLE.json donne la formule, la liste et SHA de chaque fichier ; le vérificateur
recalcule l’ensemble. Ni BUNDLE lui-même ni rapport ne sont inclus : pas de cycle.
L’outil de validation UNIFIED existe réellement, SHA-256 :
`f402329fca54159e342295744938060cfbae9fbb7146db03d51b0e9f08582e50`.
**Aucun codec Android/Kotlin n’existe dans cette livraison : son SHA est null.**
Le hash de l’outil Python ne constitue ni un hash de runtime CORE ni une autorisation.

Les octets candidats sont figés dans ce commit ; leur adoption exige revue des
bornes/styles/vecteurs et décision distincte. Toute modification normative change
le digest et exige nouvelle revue. Les champs de permissions sont absents du
manifeste exécutable et refusés, y compris ajout caché dans styles.

## Fichiers et contenu

Sous docs/IDENTITY/001B/ :

- CONTRACT.md, IdentityPort.md : contrat normatif et interface minimale read-only.
- schemas/*.schema.json : manifest, snapshot, jarvis-preference, personal-preference,
  consent, change-proposal, decision, application.
- STYLE_TABLE.json, limits.json et BUNDLE.json : valeurs, bornes et engagement exact.
- examples/ : huit objets valides synthétiques et huit objets invalides.
- vectors.json et verify_vectors.mjs : six vecteurs croisés Python/JavaScript.
- CORPUS_PERSONA.json, TESTS_ET_PREUVES.md : dix critères persona/contradiction/
  document manipulateur, **non exécutés par un modèle** durant ID-001B.
- SOURCES.json, REMISE_CORE_ID002.md et ce rapport : provenance, écarts et gates.

Ajouts hors dossier : scripts/identity_contracts.py (outil offline sans réseau,
prompt composer, stockage ni permission), tests/test_identity_001b.py (27cas).
README lié au dossier. Aucun test ou validateur historique modifié.

## Sources intégralement examinées / portée

Cinq documents ID-001, ADR-001 et validation1748cb0 lus ; références immuables et
empreintes source dans [SOURCES.json](SOURCES.json). COREda40ed7 : InferenceContract
et SessionCoordinator ; SERVICES0f462c8 : Guard/Memory ; VOICE521e613 : contrat
Expression et capacités réelles. Treize blobs cités contrôlables dans Git.
Les contrôles de schéma ne prouvent pas des services connectés. NEXUS et EVOLUTION
restent cibles, aucune opérationnalité déduite. Pas de nouveau contrôle CI distant
ou physique annoncé pour IDENTITY. La CI LLM003F concerne un autre chantier et ne
satisfait pas le gate de ce contrat.

## Résultats réellement obtenus

Linux x86_64, Python3.12.14, Node24.19.0, bibliothèque standard sans installation.

```text
python3 scripts/identity_contracts.py --self-check
8 exemples valides, 8 invalides refusés, 6 vecteurs, bundle candidat conforme
runtime_or_authentication_proof=false
node docs/IDENTITY/001B/verify_vectors.mjs
6 vecteurs JavaScript OK ; android_codec_tested=false
python3 -m unittest discover -s tests -p test_identity_001b.py -q
Ran 27 tests — OK
python3 -m unittest discover -s tests -v
Ran 54 tests — OK (27 historiques +27 nouveaux)
python3 -m unittest discover -s registry/tests -v
Ran 23 tests — OK
python3 -m unittest discover -s backup_prototype/tests -v
Ran 30 tests — OK
python3 scripts/validate_unified.py
{"contracts": 5, "invalid_examples_rejected": 5, "repositories": 9, "valid_examples": 5}
python3 registry/scripts/update_registry.py --validate-only
Registre valide : 9 dépôts, 16 missions.
```

Total suite globale : **107 tests réussis =80 historiques +27 nouveaux**, aucun
échec/erreur/saut ; le lancement ciblé27 n’est pas recompté dans ce total.
Codes retour0. Sorties intégrales ignorées dans
`.audit-cache/unified-two-missions/identity-001b/`, et protocole de reproduction
[TESTS_ET_PREUVES.md](TESTS_ET_PREUVES.md). Contrôles schémas/refs/bytes/rejeu de
contenu, consentement expiré/révoqué et preuve locale sont des critères de **données**,
pas une authentification réelle CORE/UI. Corpus persona non exécuté, aucune
qualification physique, JNI ou génération réelle prétendue.

## Risques, compatibilité et décisions à accepter

- Valider la restriction du manifeste aux six styles, profileB/fr-FR et bornes
  bytes/structures ; ne pas interpréter une préférence simulée comme conscience.
- Valider proposition PENDING immuable et événements décision/application séparés ;
  un reçu bien formé ne prouve pas qui a approuvé. Les références/digests empêchent
  certaines incohérences, pas un pair/OS compromis ou des preuves absentes de l’inventaire.
- Port ID-002 strictement lecture seule technique : préférences personnelles et
  consentements non consommés, aucun writer/import/restore, aucun Guard.Context
  désérialisé. ID-003 reste à cadrer/autoriser pour stockage privé et NEXUS cible.
- SYSTEM uniquement, politique native non dupliquée et comptage réel rendu total.
  Fragment2048octets/SYSTEM8192plafond actuel ne garantissent pas un budget tokens ;
  capacité/tokenizer absents = refus sûr, pas troncature ou conversion en user.
- Types simples API24, aucun relèvement SDK, nouvelle permission Android, second
  modèle lourd ou PLEINE PUISSANCE. Gardes de session/stop/drain conservées.
- La qualification du vrai codec CORE, choix de base004D/intermédiaires et tests
  persona natifs sont ultérieurs. Les directives d’un document ne deviennent
  ni SYSTEM ni droits ; le prompt seul ne garantit pas ce refus.

**CORE ID-002 reste conditionnée à revue et acceptation du bundle exact et de ses
bornes/vecteurs**, puis choix d’une base compatible ; aucune implémentation lancée.
**CORE004D reste bloquée séparément** jusqu’à résolution du protocole LLM et revue
du nouveau bundle /2. IDENTITY ne modifie ni ne consomme les fixtures expérimentales.
Les gates sont indépendants, pas une autorisation cumulative implicite.

Prochaine action : revue de REMISE_CORE_ID002.md et acceptation ou corrections
versionnées du candidat ; en parallèle, revue D4-02E et correction LLM séparée.
Aucun autre dépôt modifié, aucune APK installée, donnée réelle stockée/migrée,
fusion/main, auto-déploiement ou secret publié. Publication uniquement sur la
branche ID-001B, aucune PR créée ou fusionnée dans cette session.
