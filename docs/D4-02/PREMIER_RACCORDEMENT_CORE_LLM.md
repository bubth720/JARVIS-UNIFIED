# D4-02 — premier raccordement réel CORE ↔ LLM, plan soumis à accord

**Aucun code d’adaptateur, service ou test E2E réalisé ici.** Ce plan raffine le
[plan préalable](../PLAN_INTEGRATION_CORE_LLM.md) ; il ne déploie rien. Bases de
travail à revérifier : CORE004A306a89b, LLM003C43503f5. Schémas et ADR inchangés.

## Périmètre minimal et définition de preuve

Parcours initial texte synthétique : UI CORE → session CORE → port autorisé →
**vrai backend LLM/JNI/GGUF** → réponse liée à la session → UI CORE. VOICE,
SERVICES, NEXUS, sync PC et montre sont hors chemin. Aucun modèle téléchargé,
profil copié, mémoire modifiée ou corpus personnel utilisé pour le pilote.
Une réponse catalogue ou un mock ne valide pas l’inférence native E2E.

Conserver les applications autonomes et données. Recommandation à décider pour
un premier essai Android inter-applications : Bound Service/Binder avec appel
explicite entre fixtures de test, API29+ pour LLM, sans réseau. Option bibliothèque
in-process à comparer mais non retenue implicitement : elle exige extraction et
harmonisation de build/SDK plus larges. Le nombre final d’APK reste ouvert.
Transport PC/montre D4-01 ne bloque pas cet inventaire ni les tests purs ; il ne
décide pas non plus le transport Android inter-APK.

Authentification : service fermé par défaut ; s’il doit être exporté pour le
pilote, export dédié et contrôle package/UID/certificat et droits exacts à valider.
Une permission signature seule ne fonctionne pas entre certificats différents.
Certificat LLM debug dans un rapport ≠ certificat CORE installé connu ; les deux
identités réelles doivent être vérifiées. Aucun re-signing de l’existant, nouvelle
clé distribuée ou mode trust-all. Tester d’abord avec certificats de fixtures ;
installation d’essai distincte uniquement après consentement.

## Portes avant toute mise en œuvre

G0 décision propriétaire/conservation [matrice](MATRICE_RESPONSABILITES.md),
G1 mapping de prompt/budgets et contrat de cycle de vie, G2 transport et identité,
G3 règle d’admission interprocessus, G4 plateforme/API et qualification matérielle,
G5 autorisations par dépôt et d’installation. Tests purs/fixtures avant matériel.
Le pilote ne s’active pas parce qu’une branche ou une CI est verte.

Recommandation de prudence : un seul moteur résident et un travail lourd pour
le pilote. Plusieurs modèles possibles seulement après qualification et arbitrage
vérifié conformément à l’ADR, sans activation ici. Autorité logique de parcours
CORE ; emplacement de l’implémentation d’arbitrage à décider. Un gate côté CORE
et un coordinateur process-local LLM ne suffisent pas seuls : tous les chemins
LLM (UI autonome/import/chargement) doivent participer et aucun warm-up CORE ou
Whisper/VOICE concurrent ne doit contourner le gate. Pas de prétention de contrôle
des autres applications Android ou de réservation physique de RAM.

## Ordre de réalisation proposé

1. **Référence sans changement de runtime** : relever sources, plateformes,
   signatures réelles et modèle déjà local/empreinte, exporter/prouver restauration
   sur fixtures. Garder APK et modes actuels. Étudier avertissements tiers avant
   toute surface IPC/réseau ; aucune désinstallation de données utilisateur.
2. **Tests de contrat d’abord** dans chaque dépôt : erreurs/cancel/deadline,
   versions, identité, source de contenu, système/prompt, réponses tardives et
   génération de bail. Séparer mocks et scénario réel. Résoudre le prompt fixe
   natif vs systemPrompt CORE, sans le supprimer ou le déclasser silencieusement.
3. **Cycle de vie CORE** : adapter le port LocalLanguageModel existant et sa
   factory sans supprimer moteur historique. Choisir mode avant AppGraph.prepare :
   aujourd’hui llm.warmUp charge toujours le moteur interne. L’ancien releaseInternal
   est privé ; NonCancellable conserve l’opération jusqu’au retour natif. Exposer
   une preuve sûre de fin/déchargement demande une mission dédiée et des tests,
   pas un isLoaded=false supposé. Si pas d’arrêt natif disponible, maintenir gate
   occupé jusqu’à fin réelle et annoncer limite ; ne pas afficher arrêt réussi.
4. **Endpoint LLM de fixture** : réutiliser LanguageModel/ProcessResources et
   l’admission complète (capteurs, SafetyPolicy, hash GGUF, foreground/lifecycle).
   Appeler LlamaBackend directement sans ces gardes contournerait des protections.
   Le pipeline de génération doit rester unique, partagé avec les entrées locales,
   sans pousser une demande de backend dans l’UI MainViewModel pour l’exécuter.
5. **Handshake sans chargement** : versions, identité, capacités, modèle reconnu,
   budget et mapping testés ; refuser app absente/API non compatible ou capteur
   inconnu sans charger un autre moteur. API24–28 garde le mode historique si
   supporté : aucune hausse minSdk CORE pour faciliter l’essai API29+.
6. **Sélection exclusive** : sur session neuve de fixture, mode LLM délégué sans
   warm-up legacy ; si moteur historique déjà actif, attendre retour natif puis
   déchargement attesté avant admission LLM. Ne pas tuer silencieusement une
   opération ou désinstaller l’application pour imposer un basculement.
7. **Une requête bornée** : autorisation CORE, bail/corrélation, validation de
   budgets par LLM, prepareOperation avant load/generate, résultat vérifié avant
   publication. Budget effectif minimum des limites demande/politique matérielle ;
   aucune baisse des seuils SMALL2Gio/MAIN4Gio ou activation PLEINE PUISSANCE.
8. **Annulation et libération** : requestStop atteint le natif ; attendre retour
   effectif puis unload, acquitter fin et libération, seulement ensuite autoriser
   opération suivante. Si IPC rompu ou erreur de nettoyage : état inconnu/bloquant,
   pas de nouveau moteur. Unbind n’est pas unload ; client mort ≠ service mort.
9. **Parité et repli** : commandes/heure/PDF/SQLite/historique/voix ancienne testés
   comme avant ; parité du mapping texte puis corpus synthétique RAG séparé.
   Repli historique uniquement choisi explicitement après absence de résidence
   LLM confirmée ; aucun retry automatique sur autre moteur après timeout.
10. **Qualification physique et recette** : appareils autorisés, mode avion,
    froid/chaud/repos, PSS/pics disponibles/thermique/batterie et arrêt effectif ;
    refus d’admission est un résultat légitime, pas un motif de stress/abaissement.
    Déploiement et fusion font ensuite l’objet d’accords distincts.

## Matrice de tests et critères de sortie

| Niveau | Cas minimum | Preuve exigée / échec bloquant |
|---|---|---|
| Contrats purs | système/contexte non représentable, UTF-8/taille/tokens, mauvais modèle, version, cancel répété et résultat périmé | Tests par port ; fixtures explicitement simulées, pas E2E |
| IPC isolé | mauvais UID/certificat, service absent, deadline, mort client/service, processus redémarré, sérialisation hostile | Deux processus réels de test ; logs minimisés sans texte ni clé, versions exactes |
| Ressources | legacy warm-up interdit en mode délégué ; second appel via UI LLM/import/Whisper refusé ; timeout garde bail ; cleanup_failed bloque | Observation des participants et native_done/unloaded, pas booléen de façade |
| Native E2E | Une demande CORE appelle le vrai LLM/GGUF puis réponse corrélée et désallouée | SHA des deux APK + modèle, protocole, traces d’états sans données privées ; aucun mock ou catalogue |
| Non-régression | heure/docs/PDF/sources/SQLite/reprise/rotation, Annuler et mode historique | Tests004A et003C conservés, aucune donnée supprimée et aucun profil migré |
| Appareil | froid/chaud/repos/refus/arrêt/mode avion | Essai humain réellement exécuté et reproductible ; émulateur ≠ tablette/téléphone |

Succès limité : parcours démontré pour une paire précise d’APK/contrats/modèle et
configuration autorisée. Pas « toutes les applis fusionnées ». Échec ou décès
inconnu interdit le basculement automatique ; restauration ne dépend pas de PC,
cloud, export fictif JVBK ou accès aux sandbox d’un autre APK.
