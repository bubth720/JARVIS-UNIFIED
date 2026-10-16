# Compatibilités et ressources — Mission 002

## Identités et versions observées dans les sources

Métadonnées lues aux SHAs de [AUDIT.md](AUDIT.md), pas inventaire d'installations
sur un téléphone. Aucun certificat privé ou secret lu.

| Projet | Identité Android / stockage | Contraintes importantes |
|---|---|---|
| CORE | com.stark.jarvislocal, versionCode4 / 3.1.0 | minSdk24, SDK35, ARM64 ; SQLite v1/v2 de même schéma ; préférences jarvis_settings_v2 |
| LLM 003B | fr.jarvis.llm, versionCode5 / 0.3.1-mission003b | minSdk29, SDK36, ARM64 ; catalogue SQLite v1/normalizer v1 ; llama.cpp épinglé |
| VOICE E | com.jarvis.voice.voiceprototype005e | minSdk26, SDK35, ARM64 ; sandbox distinct ; ancienne signature CI incompatible avec livraison 005F |
| VOICE F | com.jarvis.voice.voiceprototype005f (build prototypeSidecar=true), versionCode3 | minSdk26, SDK35, ARM64 ; profil FP32 JVFP1 |
| VOICE G | com.jarvis.voice.voicequality005g, versionCode1 | minSdk26, SDK35, ARM64 ; profil JVFP1, essais A/B séparés |

Certificat public rapporté pour les livraisons F/G :
`aba9ee43361fd342e119a33ae5a628e63199b3b6ef4f14d3a3619f6d5678d89e`.
Cette information ne prouve pas la disponibilité de la clé privée, ni l'identité
de la version installée. Préserver les installations ; une désinstallation
supprimerait les sandbox. Aucune clé de signature ne fait partie de l'archive.

## Matrice des moteurs et profils

| Objet | Identité requise | Migration autorisée / refus |
|---|---|---|
| GGUF Qwen3 0,6B/1,7B Q4_K_M | Architecture/quantification/template/tokenizer compatibles avec backend épinglé + SHA attendu | Fichier portable, chargement seulement après vérifications et admission ; autre GGUF non automatiquement accepté |
| llama.cpp LLM | Révision 1b70350c92563449576bcbbf552994b1d1ed847d | Un seul moteur actif ; aucun wrapper CORE supplémentaire nécessaire au backup |
| Whisper CORE | whisper-android 1.0.0 et whisper.bin correspondant | Conserver référence et configuration française ; qualifier backend/poids PC séparément |
| VOICE Android FP32 | JVFP1, 18 états exacts, offsets/formes et packId attendus par ExperimentalModelPack | Copie byte-identique possible entre lecteurs réellement compatibles ; aucun réencodage automatique |
| Preset probe INT8 | PTVB1, pack INT8 correspondant | N'est pas du clonage ; incompatible par renommage avec JVFP1 |
| VOICE CPU prototype | Pocket TTS 3.3.0, checkpoint et profil safetensors spécifiques | Pas de conversion JVFP1/safetensors présumée ; adaptateur à qualifier |
| Démonstrateur Mission002 | JARVIS-DEMO-VOICE-1, jarvis-demo-no-inference-v1, SHA du faux pack | Métadonnées synthétiques uniquement ; refus de tout moteur/pack différent ; aucune synthèse possible |
| Archive Mission002 | Enveloppe JVBK v1, format jarvis-backup v1, purpose synthetic-demo-only | Lecteur Python v1 seulement ; pas d'import direct Android ni de vraie archive applicative |

Le SHA du pack de démonstration est dérivé de la chaîne publique
`SYNTHETIC-NOT-A-MODEL` : c'est un marqueur fictif, pas un hash de poids téléchargés.
Toute divergence réelle de pack peut invalider un profil même si les noms ou les
18 clés restent identiques. Les profils réels sont des données sensibles et ne
sont pas des ressources publiques à commiter dans VOICES.

## Arborescence préparée

```text
resources/
  README.md
  TABLET/resource.json      # Qwen3 0.6B Q4_K_M, référence initiale
  MOBILE/resource.json      # Qwen3 1.7B Q4_K_M, référence initiale
  CENTRAL/resource.json     # matériel/backend/modèles futurs non qualifiés
  VOICES/resource.json      # registre de formats, aucun profil personnel
```

Aucun `.gguf`, `.onnx`, `.safetensors`, audio, profil utilisateur ou poids n'est
inclus. Les hashes absents sont null et le statut indique non installé/non
qualifié : jamais traiter null comme une correspondance d'intégrité. Les fichiers
resource.json sont une préparation documentaire, pas un chargeur de modèles.
La fixture de backup contient sa propre liste synthétique de références, pas de
poids ni de liens déclenchant une récupération réseau.

TABLET : Redmi Pad SE, référence initiale Qwen3 0.6B Q4_K_M ; MOBILE : POCO X8 Pro,
référence initiale Qwen3 1.7B Q4_K_M ; CENTRAL : futur mini-PC à qualifier. Ces
modèles ne sont pas des plafonds définitifs. Tout ajout requiert version,
compatibilité backend, intégrité, licence et qualification matérielle.

## Android vers mini-PC

JSON UTF-8, octets SQLite et empreintes sont indépendants de l'ABI. AES-GCM/scrypt
ont des implémentations interopérables ; aucun secret Android Keystore non
exportable n'est nécessaire au déchiffrement de l'archive avec sa phrase secrète.
Le démonstrateur a été exécuté sur Linux/Python seulement : aucun test croisé
Kotlin/Android n'est revendiqué. Les primitives POSIX de store/publication devront
être adaptées à Android et aux supports USB/FAT/SAF.

Sur mini-PC : importer d'abord vers un espace séparé, conserver IDs/dates/compteurs,
versions de catalogue/normalisation, provenances et confirmations. Reconstruire
les index seulement depuis les données canoniques, sans détruire l'ancien corpus.
Ne jamais réactiver automatiquement un souvenir ni charger un profil vocal avec
un moteur différent. Les moteurs absents laissent les artefacts en quarantaine.
Aucun réseau, synchronisation, inférence ni qualification CENTRAL n'est ajouté.

## Conditions bloquant une récupération réelle

- Export applicatif CORE complet absent ; l'accès à son sandbox n'est pas établi.
- Disponibilité locale des packs privés, profils et clés non inspectée.
- Consentements historiques CORE sans preuve vérifiable à réexaminer localement.
- Compatibilité exacte de l'installation et signature à relever sur appareil.
- Format de production volumineux, restauration Android, cohérence multi-fichiers
  et chiffrement des données actives à qualifier.

Ces points limitent l'usage réel du prototype ; ils n'empêchent pas la validation
fictive demandée. Aucun changement de source ou démarrage d'une mission suivante
n'est effectué pour les contourner.
