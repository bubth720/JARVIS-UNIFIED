# Incompatibilités, risques et adaptations futures

## Incompatibilités constatées

| # | Constat | Impact | Adaptation proposée (non appliquée) |
|---|---|---|---|
| I1 | Contrats UNIFIED v1 fermés ; `platform` ∈ {android, linux, unknown} | Un PC Windows n'est pas descriptible en v1 | Schéma v2 négocié (ajout windows/macos) ; v1 inchangé |
| I2 | `offline_required: const true` (v1) | Ambiguïté entre « sans Internet » et « sans aucun réseau » | Définir en v2 : sans Internet ni cloud ; LAN appairé permis **seulement** dans la variante hybride |
| I3 | La variante Android locale n'a aucune permission réseau (V1, V3) | La liaison PC est impossible dans l'APK actuelle, ce qui est voulu | Variante séparée « hybride » avec `INTERNET`, appairage et chiffrement, activée par l'utilisateur ; la variante locale reste sans réseau |
| I4 | CORE n'a qu'un moteur (`LocalLanguageModel`) et pas de routeur | Un moteur PC ne peut pas être appelé aujourd'hui | Mission d'implémentation CORE : registre et routeur, adaptateur 1:1 du moteur actuel |
| I5 | Le moteur historique ne diffuse pas en flux et `requestStop` peut être `UNSUPPORTED` | L'interruption fine n'est garantie que si le moteur la déclare | Capacités `streaming` et `cancellation` déclarées ; l'UI adapte ses états |
| I6 | Le document « JARVIS_Vision_Architecture_Cahier_des_Charges_2026 » est absent des dépôts | Écarts possibles avec la vision du propriétaire | À fournir, puis réconcilier ARCH-01 |
| I7 | Les horloges des deux machines ne sont pas comparables | Les deadlines absolues sont fausses entre machines | Délai restant borné (`remaining_ms`), appliqué localement (déjà dans v1 SEMANTICS) |

## Risques

| Risque | Gravité | Maîtrise prévue |
|---|---|---|
| Fuite de données personnelles vers le PC | Élevée | PC non autorisé par défaut ; classes de données par le propriétaire ; `sensitive` jamais envoyée ; liste blanche de champs ; documents par référence |
| PC compromis ou usurpé sur le LAN | Élevée | Appairage hors bande, authentification mutuelle, chiffrement, anti-rejeu par séquence, aucun rôle de pilotage pour le PC |
| Réponse partielle puis bascule silencieuse | Moyenne | Requête liée à son moteur ; perte ⇒ interruption signalée, jamais rejouée |
| Double moteur lourd en mémoire sur le téléphone | Moyenne | Libération `CONFIRMED` exigée avant un autre moteur ; sinon `DEGRADED` non routable |
| Classement trompeur par chiffres annoncés | Moyenne | Seules les mesures réelles (au moins 5 échantillons) classent |
| Souvenir créé par une sortie du modèle PC | Élevée | Le PC propose seulement ; confirmation sur le téléphone liée au contenu exact |
| Dérive du contrat CORE | Moyenne | Empreinte figée et test de couverture ; une rupture fait échouer les tests |
| Confusion entre validation architecturale et fonctionnement réel | Moyenne | Tous les tests sont simulés et étiquetés comme tels ; aucune qualification n'est revendiquée |

## Adaptations futures, dans l'ordre (chacune soumise à autorisation explicite)

1. Négocier et publier les schémas UNIFIED v2 (descripteur de moteur, messages de liaison), avec exemples valides et invalides.
2. CORE : `ModelBackend` Kotlin, `CapabilityRegistry`, `Router` ; adaptateur 1:1 du moteur actuel. Aucune bascule de comportement : avec le seul moteur local, le résultat est identique.
3. Mesures réelles du backend Android sur le POCO pour `Performance.measured`.
4. JARVIS CENTRAL : choix du matériel PC, puis du moteur et du modèle (taille, licence, SHA), qualification locale.
5. Variante Android hybride et transport LAN chiffré, avec appairage. Tests d'intrusion et de rejeu.
6. Synchronisation mémoire en mode proposition, avec l'UI de confirmation existante.
7. SERVICES : déclaration des outils et routage `required_tools` ; confirmation des actions sensibles sous CORE.
