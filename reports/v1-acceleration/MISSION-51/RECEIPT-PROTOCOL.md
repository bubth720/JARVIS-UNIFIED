# Réception de composition distincte du verrou historique

Le verrou BASELINE-LOCK conserve les sources initialement auditées. Le registre CAPABILITY-EVIDENCE décrit ce niveau source et ne devient pas une table d'autorisation. Une APK candidate possède son propre commit/tree, certificat, SHA256 et reçu : remplacer implicitement la source initiale par le head courant rendrait les preuves ambiguës.

SCORE.json et SCORE.svg conservent la préinscription initiale. RECEPTION-SCORE.json reprend exactement les 31 critères, poids et plateformes ; RECEPTION-SCORE.svg représente uniquement les points reçus pour la nouvelle composition. Le digest de la spécification de critères reste celui du validateur initial. Aucun poids, seuil ou niveau de preuve n'est affaibli.

`python3 -m tooling.v1.reception` vérifie une chaîne explicite :

1. Reçu de build INTERFACE : source/tree complets, base UI-01C exacte, provenance CI, ZIP et APK hashés, paquet candidat distinct testOnly, backup désactivé, permission de signature AndroidX seulement, aucun autre module connecté.
2. Reçus Android : même source/tree/APK/testAPK/paquet/run que le build, API 29 et 35, x86_64 émulé, TCG ou KVM déclaré d'après observation, protections inchangées, artefacts et fichiers bruts identifiés par SHA256.
3. Lecture réelle et inspection de la preuve brute consignée par le responsable de réception. Une quantité de tests ou un champstatus ne remplace pas cet examen. Chaque opération attribuée doit être attestée sur les deux API.
4. Portée limitée à navigation, CRUD/persistance et fonctionnement hors-ligne de l'INTERFACE locale. Aucun point LLM/CORE, gain de performance, accessibilité complète, VOICE/AVATAR ou qualification physique ne peut être attribué par ce chemin.

Le PASS du validateur signifie **cohérence de ce dossier de preuves**. Il n'est ni une attestation cryptographique indépendante de GitHub ni une authentification humaine. Le validateur ne télécharge et n'exécute rien ; les archives ont été téléchargées séparément, leur digest comparé à GitHub et leur contenu inspecté avant la consignation. La revue des liens et sorties reste indispensable : un JSON auto-déclaré ne crée aucune autorité.

Les 19 nouveaux tests de réception, dont 17 cas négatifs, utilisent des fixtures entièrement synthétiques et ne qualifient aucun appareil. Ils couvrent les écartsSHA/tree/APK/run/provenance, fauxAndroid physique, simple compteur de tests, job échoué marqué PASS, API manquante, builds différents du même commit réunis à tort, opération non attestée, permission sensible, second module, artefact sans SHA, ID dupliqué et préservation de l'ancien validateur strict. Les 32 tests initiaux restent présents.

Le dernier rapport UNIFIED peut avoir un commit plus récent que l'APK reçue : les preuves restent attachées au SHA source réellement compilé/testé. La première campagne échouée est conservée et liée à son propre commit. Aucun retry automatique ne masque une erreur critique.

Les gates G-A/G-ROOT/G-B/G-C et G-MERGE restent séparés du score. Ce code n'émet ni mandat CORE, ni bail, ni clé, ni admission LAB, ni commande d'installation. La génération réelle, le TTFT physique, les migrations privées et les appareils personnels restent NOT_RUN ou BLOCKED selon leurs dossiers respectifs.
