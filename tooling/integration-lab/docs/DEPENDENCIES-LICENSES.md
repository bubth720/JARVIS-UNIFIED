# Dépendances et licences

Le LAB utilise Python3.12 et sa bibliothèque standard. Il réutilise les validateurs Python déjà présents dans UNIFIED sans nouvelle dépendance runtime. Git est requis pour les identités et préimages. cryptography50.0.0 reste une dépendance historique du prototype de sauvegarde, installée depuis son requirements existant en CI ; le LAB ne l'ajoute pas à ses nouveaux modules.

Les compilations utilisent les toolchains existantes : NEXUS Gradle8.10.2/Kotlin2.0.21 ; INTERFACE, VOICE et EVOLUTION Gradle8.13/Kotlin2.1.20 ; SERVICES Gradle8.13/JDK21 selon sa CI existante. Android SDK35/build-tools35.0.0 pour M51, sans harmonisation globale. Les wrappers et leurs propriétés font partie des préimages verrouillées ; la validation TLS/signatures/empreintes reste active. Aucun poids IA acquis par le LAB.

core/dependencies.py produit les versions, permissions sources, dépendances natives déclarées et chemins LICENSE/NOTICE avec SHA256. Les versions absentes restent UNKNOWN. Ces données peuvent inclure plusieurs variantes historiques : elles ne valent pas inventaire résolu d'une seule APK. Le collecteur M51 inspecte séparément les manifestes et bibliothèques réellement assemblés.

La licence du dépôt de chaque module reste UNKNOWN tant qu'une preuve exacte n'est pas fournie. Une licence de dépendance ne licence pas le dépôt ; une notice ne permet pas d'inférer un droit sur un modèle ou un profil vocal. Les notices existantes ne sont ni retirées ni réécrites. Le résultat est un rapport de développement pour les sources autorisées de l'utilisateur, pas une nouvelle autorisation de redistribution de contenus privés.

Le test visuel local utilise le Playwright et Chromium déjà installés dans l'environnement cloud ; ils ne sont pas requis pour ouvrir le HTML exporté. Aucun CDN, service permanent ou abonnement. Toute limitation du navigateur local est rapportée sans modifier sa politique.
