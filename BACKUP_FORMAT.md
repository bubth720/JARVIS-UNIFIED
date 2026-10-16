# Format de sauvegarde portable — Mission 002

Statut : **v1 démonstrateur fictif**, implémenté dans
[backup_prototype/backup.py](backup_prototype/backup.py). Aucune donnée réelle,
aucun moteur, aucun poids, aucun profil personnel n'est traité par cette mission.
Le format est documenté pour une future implémentation Android/mini-PC ; les
adaptateurs Android ne sont pas développés. Compatibilités : [COMPATIBILITY.md](COMPATIBILITY.md).

## Inventaire des données sources

Inventaire par lecture des révisions immuables de [AUDIT.md](AUDIT.md), complété
par les chemins de stockage dans le code. Ce sont des emplacements relatifs au
sandbox de chaque application, pas des fichiers personnels découverts sur appareil.
Aucune taille réelle, clé ou installation utilisateur n'a été inspectée.

| Origine et emplacement | Contenu / version | Politique de conservation et extraction future |
|---|---|---|
| CORE `databases/jarvis_local_v2.db` | user_version 2, tables messages, memories, documents, chunks ; index idx_chunks_doc ; IDs, dates, sqlite_sequence | Snapshot cohérent, données originales intouchées ; souvenirs sans autorisation hors export actif |
| CORE `shared_prefs/jarvis_settings_v2.xml` | prompt, ctx, max, topk, speak | Export logique versionné, pas copie aveugle de SharedPreferences ; prompt potentiellement personnel |
| CORE `files/models/jarvis.gguf`, `whisper.bin` | LLM et reconnaissance locale ; imports depuis assets | Références/hashes/configuration ; poids optionnels selon droits et format futur ; aucun téléchargement |
| CORE documents/passages dans SQLite | Noms/MIME/date et texte découpé avec pages ; recherche lexicale recalculée | Conserver passages/citations ; PDF originaux non copiés par PdfImporter, ne pas prétendre les récupérer |
| CORE `cache/jarvis_input.wav` | Enregistrement STT temporaire 16 kHz | Exclu par défaut ; aucun audio personnel dans le prototype |
| LLM conversation/état ViewModel | Messages de session et profil de calcul en RAM | Pas de conversation SQLite persistante à récupérer ; état volatil non promis après arrêt |
| LLM `databases/catalogue.db` v1 | answers, variants, phrases, revisions, catalogue_meta et FTS4 phrase_search | Garder réponses/révisions/tombstones ; exporter logiquement et reconstruire FTS selon normalizer_version ; JSON actuel à contrôler pour équivalence complète des révisions |
| LLM `files/models/qwen3-0.6b.gguf`, `qwen3-1.7b.gguf` | Slots SMALL/MAIN, limites et SHA-256 attendus | Poids liés à architecture/quantification/backend ; ne pas convertir un hash absent en validation |
| LLM `shared_prefs/model_hashes.xml` | Digests attendus SMALL/MAIN | Export des références non secrètes et vérification au réimport ; pas de chargement automatique |
| LLM captures diagnostic / JSON exportés par l'utilisateur | PSS/RSS, profils, configuration, provenance APK ; pas de contenu conversationnel attendu | Facultatif, séparation des diagnostics et données métier ; aucun chemin externe supposé accessible |
| VOICE E/F/G `no_backup/models/fp32/` | Graphes, tokenizer, bundle, identité du pack, manifeste/hashes intégrés | Pack privé versionné, pas publié ni téléchargé ; vérifier licence avant transfert |
| VOICE E/F/G `no_backup/profiles/active.json`, `<uuid>/state.bin`, `metadata.json` | JVFP1 et 18 états, packId, SHA-256, consentConfirmed | Profil sensible : consentement d'export et confirmation d'activation ; préserver les octets, aucun réencodage implicite |
| VOICE E/F/G `no_backup/reference.wav` | Référence locale privée | Exclue par défaut ; inclusion future distincte avec consentement ; provenance et droits requis |
| VOICE E/F/G `no_backup/last-pcm/`, diagnostics | Dernière synthèse, pointeur/manifeste/hash ; diagnostics numériques | Cache facultatif exclu par défaut ; ne pas confondre avec profil |
| VOICE G `no_backup/ab-comparison/`, `human-ratings.json`, métriques | PCM A/B, paramètres, notes humaines bornées | Facultatif sensible, exclu du prototype ; pas de résultat perceptif inventé |
| VOICE probe INT8 | Pack de démonstration et preset PTVB1 | À préserver séparément ; preset ≠ clone et incompatible avec JVFP1 |
| VOICE CPU branche prototype | Profils safetensors, caches modèle, références et réglages du prototype Python | Format/identité spécifiques au moteur CPU, pas un profil Android universel |
| Tous projets | Temporaires `.part`, `.pending`, fichiers de travail et handles natifs | Ne pas les exporter comme données valides ; garder les sources en cas de diagnostic |

Preuves de chemins : CORE `LocalDatabase.kt`, `SettingsStore.kt`, `ModelManager.kt`,
`MainActivity.kt`, `PdfImporter.kt` ; LLM `ModelStore.kt`, `CatalogueStore.kt`,
`ChatViewModel.kt` ; VOICE `PersonalVoiceProfile.kt`, `PrivatePcmStore.kt`,
`QualityABStore.kt` et MainActivity des modules `voicePrototype`/`voiceQuality`.
Les règles de backup système empêchent d'utiliser Android Backup comme export
global. Le prototype ne contourne pas les sandbox. Un ajout d'export dans une
source exigerait une mission distincte ; aucune source n'est modifiée ici.

## Enveloppe binaire `.jvb`, version 1

| Position en octets | Longueur | Définition |
|---|---:|---|
| 0–5 | 6 | Magic exact `4a 56 42 4b 00 01` (`JVBK`, zéro, version1) |
| 6–21 | 16 | Sel cryptographique aléatoire |
| 22–33 | 12 | Nonce AES-GCM aléatoire |
| 34–fin | variable | Texte chiffré suivi du tag GCM 16 octets |

AES-256-GCM via `cryptography`, clé 32 octets dérivée avec **scrypt N=32768, r=8,
p=1**, sel de 16 octets. L'en-tête complet de 34 octets est authentifié en AAD.
Ces paramètres sont fixes pour cette version, ne proviennent pas de l'archive :
un attaquant ne peut pas demander un coût KDF arbitraire. Scrypt demande environ
32 Mio de mémoire pour son cœur de calcul, à mesurer sur Android avant adoption.
Toute nouvelle configuration cryptographique exige une version d'enveloppe.

Mot de passe de 12 à 1024 caractères Unicode, UTF-8 sans normalisation implicite.
Choisir une phrase aléatoire longue ou un secret généré, pas un mot courant de
12 caractères. Sel et nonce renouvelés à chaque sauvegarde ; la clé n'est jamais
stockée dans l'archive. Le prototype interactif demande le mot de passe avec
`getpass` et confirmation à l'export, sans argument CLI ni variable d'environnement.
Les tests et la démo utilisent des secrets aléatoires éphémères en RAM, sans
valeur versionnée. Aucune fonction de récupération sans mot de passe : conserver
celui-ci séparément dans un gestionnaire local ou un support privé approprié.

L'intégrité SHA-256 ne remplace pas GCM. GCM authentifie l'enveloppe et le manifeste,
mais ne prouve pas l'identité du propriétaire : quiconque connaît le mot de passe
peut fabriquer une nouvelle archive. Une autorisation utilisateur ne se déduit
pas d'un booléen dans une archive reçue. Pas de signature d'identité fictive.

## Charge utile et manifeste

JSON UTF-8 canonique produit par le prototype, sans compression ni ZIP. Objets
binaires encodés en Base64 strict. Deux clés racines seulement : `manifest` et
`objects`. Les clés JSON dupliquées, valeurs non finies, chemins inconnus et
versions incompatibles sont refusés. Le lecteur n'extrait jamais un chemin libre.

Le manifeste chiffré contient :

- `format: jarvis-backup`, `version: 1`, `purpose: synthetic-demo-only` ;
- `archive_id` UUID et `created_utc` ISO8601 ;
- `source_revisions` CORE/LLM/VOICE aux trois SHA audités, provenance du schéma,
  pas prétention d'export d'une installation réelle ;
- `required_engines` : identité exacte du faux moteur, pack SHA-256 et `usable:false` ;
- `compatibility` : lecteur `mission002-python-v1`, adaptateur Android et inférence
  PC à false ;
- `files` : chemin, catégorie, `schema_version`, taille en octets et SHA-256 de
  chaque fichier décodé. Inventaire et objets doivent correspondre exactement.

Chemins v1 implémentés, tous obligatoires :

```text
core/core.sqlite                    # schéma CORE v2, snapshot filtré fictif
core/memory-authorizations.json      # preuves fictives liées au texte exact
core/preferences.json                # schéma démonstrateur v1
llm/catalogue.json                   # catalogue FICTIF v1, pas dump natif LLM
resources/resources.json             # références seulement, aucun poids
voices/demo/profile.json             # JARVIS-DEMO-VOICE-1, non utilisable en TTS
```

Le générateur montre le manifeste réel via `pack()` et les tests le valident.
Pas d'archive chiffrée ou mot de passe d'exemple dans Git. La description du profil
fictif ne contient ni audio humain, ni tenseurs neuronaux, ni donnée clonée.

## Bornes et portée

Maximum par objet 4 Mio, total décodé 16 Mio, enveloppe 24 Mio ; lecture/déchiffrement
en RAM et validation avant écriture destination. Ni chemin absolu, ni traversée,
ni lien symbolique, ni entrée supplémentaire, ni pack/moteur inconnu. Ces bornes
sont adaptées aux fixtures ; les vrais GGUF et packs sont hors de cette v1.

Une future archive de production devra définir une nouvelle version/profil avec
objets volumineux authentifiés par blocs, quotas, capacité de reprise et schémas
natifs/logiques des trois applications. Les adaptateurs devront conserver IDs,
dates, relations, révisions et compatibilités sans faire télécharger de modèle.
La portabilité du conteneur vers un mini-PC ne signifie pas la portabilité de
l'inférence ou d'un profil vocal vers un autre moteur.

## Cohérence et confirmations

Le snapshot SQLite utilise la Backup API à partir d'une connexion **lecture seule**,
ce qui inclut les pages WAL déjà commitées et exclut les transactions en cours.
Les quatre tables et compteurs sont conservés, sauf exclusion volontaire des
souvenirs non autorisés dans la COPIE. Un VACUUM sur cette copie élimine les textes
exclus des pages libres ; les tests vérifient aussi leur absence en octets.

La fixture contient trois souvenirs : confirmé, en attente et refusé. Seul le
premier est exporté, avec empreinte du texte et preuve synthétique. Une preuve
absente, non correspondante ou un souvenir legacy ne doit pas autoriser l'export
actif. Dans une future migration legacy, conserver les originaux et demander la
confirmation avant copie autorisée, sans inventer de consentement rétroactif.
Les messages/documents restent des catégories distinctes, jamais promus en souvenirs.

Après restauration, le souvenir autorisé reste `pending-local-confirmation` dans
`memory-review.json`. L'option explicite `--confirm-memory ID:SHA256` représente
une confirmation locale exacte dans le démonstrateur et donne
`confirmed-locally`. Elle ne représente pas une authentification Android prête
pour production. Aucun moteur de récupération mémoire n'est intégré ; tout futur
lecteur devra respecter ce registre, pas lire directement toutes les lignes SQL.

Les JSON annexes de la fixture sont immuables pendant l'export. La cohérence entre
plusieurs fichiers/bases d'une application réelle demandera un verrou de mutation
applicatif et un instantané commun ; la Backup API seule ne résout pas cela.
