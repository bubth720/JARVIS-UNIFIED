# D4-02 — matrice de responsabilités proposée

**Version de proposition1, référence consolidée D4-02 ; non approuvée techniquement.**
« Définitive » désigne la matrice proposée complète, pas une décision utilisateur
inventée. [ADR-001](../DECISIONS/ADR-001-CORE-LLM-UNIFIED.md) reste approuvée avec
précisions, inchangée. [Sources fraîches](RAPPORT_ET_SOURCES.md).

## Règles qui tranchent les recouvrements

1. CORE est l’autorité de session, routage, autorisation et confirmation. Le LLM
   produit des propositions, un texte ou une clarification ; jamais des droits.
2. Un objet possède un propriétaire de données et un chemin d’écriture unique
   par namespace et appareil. Les autres modules utilisent des ports autorisés,
   pas des copies ou accès directs à sa base. Aucun maître PC obligatoire.
3. L’hébergement physique actuel est conservé. Un rôle cible NEXUS n’autorise ni
   migration ni copie concurrente ; l’existant SERVICES n’est pas supprimé.
4. SERVICES fournit des implémentations réutilisables et outils, non un second
   CORE ou NEXUS autonome. Son Guard peut renforcer/refuser, pas inventer les
   confirmations de CORE. Un contexte synthétique de test n’est pas une identité IPC.
5. Le catalogue éditorial reste celui de LLM Mission003, unique. NEXUS documents/
   souvenirs et le catalogue éditorial ne sont pas la même connaissance.

## Autorité, propriété et réemploi — un responsable par fonction

| Fonction / donnée | Autorité de décision | Propriétaire actuel prouvé | Propriétaire cible proposé et réemploi | Interdit / transition |
|---|---|---|---|---|
| Session, corrélation, choix de parcours | CORE | CORE004A SessionCoordinator/JarvisCore | CORE ; conserver single-flight, drainage et refus d’opération simultanée | Pas de session centrale SERVICES ni dépendance PC |
| Permissions, confirmation exacte et reçu | CORE | CORE UI/mémoire ; SERVICES Guard confirme ses opérations internes | CORE autorité, Guard SERVICES défense en profondeur ; consentement VOICE supplémentaire pour voix | Un texte LLM, authorization_ref ou token interne n’authentifie pas un autre APK |
| Conversation persistante et état de session | CORE | SQLite CORE ; conversation LLM volatile distincte | CORE pour historique, état de session volatil distinct ; pas de transfert de l’historique décidé ici | Ne pas synchroniser ni mémoriser implicitement tout dialogue |
| Souvenir personnel durable | CORE décide ; confirmation exacte | CORE memories ; SERVICES MEMORY possède ses propres données de diagnostic autorisées | NEXUS cible de stockage via port ; réutiliser code SERVICES si qualifié ; CORE garde politique | Pas de copie miroir des souvenirs CORE dans SERVICES/NEXUS ; legacy conservé tant que migration non autorisée |
| Préférences | CORE pour décisions ; module pour contraintes locales | CORE SharedPreferences, paramètres locaux LLM/VOICE | Valeurs portables via propriétaire explicite ; limites matériel locales restent dans leur module | Pas de budget PC ou de clé vocale imposés au téléphone |
| Documents, provenance et citations | CORE autorise l’accès | CORE PdfImporter/RagEngine/SQLite ; SERVICES DOCUMENTS pour ses imports propres | NEXUS façade domaine future, pilotes/bibliothèques SERVICES et provenance CORE réemployés après qualification | Pas de double import/recherche contre deux corpus divergents |
| Recherche documentaire/index | CORE choisit les sources autorisées | CORE RAG ; SERVICES KNOWLEDGE lexical/concept-hash | NEXUS domaine/index, réemploi SERVICES ; index dérivé régénérable | Aucun modèle embedding supplémentaire automatique ; pas de Kiwix actif inféré d’une interface |
| Catalogue éditorial/intention/variantes | CORE autorise le parcours ; LLM choisit selon règles typées | LLM CatalogueStore/Json/IntentRouter | Même composant LLM, mêmes IDs/révisions/FTS ; adapter l’accès sans copier la base | Pas de catalogue concurrent dans CORE/NEXUS/SERVICES |
| Réponses déterministes commandes/heure | CORE | CORE fastLocalReply, commandes/documents | CORE conserve ; cession de salutations éditoriales seulement après parité d’un accès catalogue qualifié | Premier pilote d’inférence ne remplace pas ces chemins ni ne crée un second IntentRouter |
| Inférence et modèles GGUF | CORE demande ; LLM valide admission | CORE LlamaLocalEngine ; LLM LanguageModel/LlamaBackend séparés | LLM moteur privilégié après adaptateur et tests ; ancien moteur CORE conservé en mode historique exclusif | Aucun second moteur actif/résident non maîtrisé, pas de copie de llama.cpp dans SERVICES |
| Budget mémoire/thermique/batterie | CORE politique de parcours + protections locales obligatoires | Gates CORE004A et ProcessResources LLM process-local | Autorité/arbitre global et emplacement à décider ; conserver les protections locales | Aucun coordinateur local présenté comme arbitre inter-APK |
| Capture et Whisper/STT | CORE tant que migration distincte absente | CORE WavRecorder/WhisperLocalEngine | CORE initialement ; VOICE cible possible seulement après mission spécifique | Pas de nouveau STT ni migration pour simplifier le premier raccordement texte |
| Synthèse/profils/PCM/cache | CORE autorise texte final ; VOICE consentement/compatibilité | VOICE Studio005J/identity/pocket ; LocalTts historique CORE distinct | VOICE ; réemployer primitives et005K futur, données privées restent dans VOICE | Pas de PCM/coffre copié dans catalogue, ni TTS Android silencieusement substitué |
| Outils, calculs, workflows | CORE autorise action exacte | SERVICES ACTIONS/DATA/ANALYST et commandes historiques CORE | SERVICES fournisseurs spécialisés, CORE orchestration ; LlmPort futur adaptateur au LLM existant | Aucun outil lancé sur simple génération ou import de tâche |
| BRIDGE et sync | CORE autorise pairs et objets | SERVICES Bridge.Transport et echo Simulator | SERVICES transport fournisseur ; NEXUS/propriétaires pour données ; CORE consentement | Aucun nouvel APK/moteur SYNC et aucun pont matériel affirmé |
| Gouvernance, contrats et versions | Utilisateur/CENTRAL ; suivi UNIFIED | UNIFIED | UNIFIED | Aucun runtime ni accès aux données personnelles |

SERVICES MEMORY, DOCUMENTS et KNOWLEDGE restent utilisables dans leur sandbox
actuelle. « NEXUS propriétaire cible » est une façade métier unique proposée,
pas l’extraction imposée du code SERVICES. Ses bibliothèques peuvent devenir des
adaptateurs internes, après décision de dépendances/licences/versions ; aucun
copier-coller ou fork parallèle. Tant que NEXUS reste README, CORE conserve son
corpus et SERVICES ses fixtures/données propres ; ni base ni index partagés.

Pour un même corpus futur : objet = namespace/owner/ID/révision/provenance ;
les refs privées résolues par propriétaire empêchent les chemins arbitraires.
Pas de double écriture de transition. Migration future : sauvegarde cohérente,
restauration testée, mode lecture comparée sur fixtures, bascule par pointeur après
parité et accord ; ancienne version conservée, aucune remise à zéro destructive.
Les durées de rétention et purges exigent décision distincte, pas conservation infinie.

## Désaccords qui exigeraient une décision nouvelle

Donner à SERVICES l’autorité de session ou une mémoire personnelle concurrente
contredirait les frontières ADR ; déplacer le catalogue dans NEXUS sans besoin
serait une duplication/extraction injustifiée. Ces options ne sont pas recommandées.
Confier au NEXUS futur l’autorité de confirmation au lieu du stockage contredirait
également CORE. Aucun amendement ADR n’est proposé ici ; seuls propriétaires
physiques, adaptateurs et décisions techniques encore ouvertes sont précisés.
Les gates à soumettre sont dans [DECISIONS_ET_MISSIONS](DECISIONS_ET_MISSIONS.md).
