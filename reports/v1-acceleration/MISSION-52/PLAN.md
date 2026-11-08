# M52 — chemin critique prêt à revue, exécution sensible OFF

Références LLM12/14/15 : runtime059cf9c3040d768e1074f62ec5d174c1a27a2590, fichier vérifié2500a123a69b059bf21ac6bec24be5a52b54a9c5, diff de revue69400fe26d61688262b94cc8a2d5efe20d1da4be. Patch8df826451e501a107305f8fcaee5ca3d5334e22de23246d32cc7fd5312da21e8 **non appliqué**. Le dossier M51.07 indépendant juge ses menaces ; aucune approbation ne découle de cette préparation.

## Étapes à ne jamais confondre

1. PATCH_APPLIED : SHA et préimages vérifiés, application seulement après G-A explicite sur branche isolée. Un diff corrigé nécessite une nouvelle empreinte et une nouvelle validation.
2. ROOT_PROVISIONED : empreinte publique approuvée par voie distincte G-ROOT ; clé privée hors dépôt/chat/CI publique. Une clé auto-générée sur runner ne prouve pas le consentement humain.
3. MODEL_ADMITTED : campagne d'acquisition autorisée séparément, octets exacts vérifiés, validations GGUF/template/quantification, vrai HEAVY puis MODEL, configuration/RAM et identité de résidence.
4. NATIVE_GENERATION_QUALIFIED : invocation JNI réelle, vrais fragments sampler, ordre/intégrité, annulation, backpressure et nettoyage observés ; pas un résultat de fixture/JVM.

Aucun de ces états n'implique le suivant. La récupération antérieure du Qwen de PR14 n'autorise pas son retéléchargement ici. Le modèle attendu demeure Qwen/Qwen3-0.6B-GGUF, révision8e42d41f70cb6c571f58c3f31bd9287b372d97cc, fichier Qwen3-0.6B-Q4_K_M.gguf,396704416octets, SHA256b0638f08417a2d3c8652760462eb5407c6e30173cf9608ad0820757a281eea0e. Aucun poids ne figure dans les artefacts de coordination.

## Contrat CORE–LLM à proposer séparément

CORE conserve admission/session/epoch/génération, demande logique, mandat authentique révocable et annulation. Le broker LLM atteste les objets de baux, owner/ID/révision/incarnation et fermeture, sans transfert de propriété. La préparation lie modèle réel, template/rendu/tokenisation/configuration aux octets exacts de la demande. Un identifiant textuel ou UUID n'est pas une attestation. La source LAB_CLOUD est incompatible avec le mandat CORE ; FIXTURE n'est jamais REAL_MODEL et ne devient pas une provenance autorisée par changement d'étiquette.

Port proposé, **documentaire seulement** : demande corrélée, états IDLE/ADMITTING/LOADING/PREFILLING/STREAMING/CANCELLING/TERMINAL/UNKNOWN/CLEANUP_FAILED ; ACK/TOKEN/COMPLETED/CANCELLED/ERROR bornés et ordonnés. Garder état métier et ressources distincts, callbacks fermés au vrai retour, aucun texte tardif après Stop/changement de session. Un timeout/file vide ne produit ni DRAINED ni UNLOADED. Un busy/cleanup inconnu ne crée jamais un second moteur.

La vue INTERFACE reçoit des événements versionnés, rend de vrais fragments par frame/batch borné sans reconstruire tout l'historique, conserve le texte partiel selon politique, refuse double Submit et événements périmés. Aucun routage runtime n'est ajouté par UNIFIED ; un changement partagé demande les PR/revues des deux propriétaires avant application.

## Protocole réel futur

Comparer ancien chemin complet et streaming sur **même** modèle/hash, bibliothèque/commit, template, prompt public, config/sampler/cap8 ou24, contexte et protections. Vérifier octets finaux sans trim ni réparation Unicode. Tester phases observées de chargement/prefill/decode/callback, annulation double et tardive, consommateur suspendu, reprise sans perte, mémoire insuffisante, exception callback et déchargement réel. Les limites candidates16événements/16Kio,4096octets/chunk,64Kio total ne deviennent pas des budgets Android validés.

Processus froid, modèle froid et résidence chaude attestée : cellules séparées, ordre alterné, repos normal, pas de résidence artificielle. Marqueurs UI submit, CORE admission, worker, JNI, préparation, sampler, premier UTF-8 utilisable non blanc, callback, frame et completion. Utiliser domaines monotones corrélés/calibrés ; jamais une soustraction host↔Android arbitraire. Au moins20échantillons comparables pour p95, conserver erreurs/refus/Stop, dénominateur complet. Mesures absentes=null/NOT_RUN ; hôte ne vaut ni Android ni p95 CORE→INTERFACE.

Tests C++/JNI, -Xcheck:jni, ASan/UBSan, ARM64/16Kio, ancien ABI, exceptions/handles/UAF/lifecycle restent à exécuter sur le code réellement approuvé. Les anciens tests model-free ne qualifient pas le sampling. API29/35 LLM ARM64 reste bloqué par l'infrastructure précédemment observée ; pas de nouvelle tentative identique. Les appareils personnels et le merge ont leurs accords propres.

Prochaine action prioritaire : recevoir l'avis indépendant M51.07 et demander la décision exacte de menace/diff, sans appliquer le patch ni provisionner une clé.
