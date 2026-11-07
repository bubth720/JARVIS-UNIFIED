# Registre de décision M51

| Décision | État | Justification / prochaine action |
|---|---|---|
| Réutiliser UI-01C dans une applicationId testOnly distincte | Autorisé pour laboratoire cloud | Le parent choisit l'hôte INTERFACE, préserve les anciennes données et publie ses propres APK/tests |
| Mettre les modules non raccordés OFF/BLOCKED | Requis | Code présent, connexion, activation, readiness, autorisation et matériel sont indépendants |
| Appliquer LAB_CLOUD8df826… | **STOP G-A** | Ce cahier ne l'autorise pas ; revue indépendante LLM M51.07 en parallèle |
| Provisionner une racine opérateur | **STOP G-ROOT** | Clé privée hors dépôt/chat/CI publique, empreinte publique à valider par diff exact distinct |
| Acquérir de nouveau Qwen3 | **STOP** | L'acquisition antérieure de PR14 suivie de suppression n'est pas une autorisation de campagne générale |
| Raccorder un mandat CORE réel | **STOP sur contrat sensible** | Préparation documentaire permise, pas UUID/hash forgé ni grant LAB converti en CORE |
| Recherche NEXUS lecture seule / SERVICES | Préparation indépendante | Corpus synthétique, provenance et refus ; écritures/export sensibles OFF |
| AVATAR / références visuelles | Préparation indépendante | Pas d'asset officiel reçu ; schémas/contrôleurs et fixtures anonymes seulement, aucun upload privé public |
| Co-résidence VOICE+LLM | **NON QUALIFIÉE** | Ne pas additionner des budgets séparés ; aucune qualification physique transposée depuis Linux |
| API29/35 M51 UI sans JNI | Test cloud permis si hôte qualifié | Distinguer l'émulation UI x86 compatible de l'ancien blocage ARM64 LLM ; pas de répétition des macOS HV_UNSUPPORTED |
| Installation POCO/Redmi / migration réelle | **STOP séparé** | APK/signature/SHA/guide/sauvegarde d'abord ; aucun appareil personnel ciblé automatiquement |
| Merge/main ou modification de protection | **STOP G-MERGE** | CI verte et PR draft ne valent jamais accord utilisateur |

`GATES.json` garde les décisions sensibles fermées. Un statut BLOCKED ou NOT_RUN ne doit pas immobiliser les tests JVM, le cockpit, les schémas d'assets ou la coordination. Aucun champ de JSON ne confère une autorisation ; le validateur ne sait exécuter aucune opération sensible.
