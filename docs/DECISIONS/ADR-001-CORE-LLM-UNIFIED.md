# ADR-001 — CORE, LLM et UNIFIED

**Statut : APPROUVÉE AVEC PRÉCISIONS — orientation architecturale uniquement.**
Date d’approbation : **15 octobre 2026**.
Autorité : validation explicite de l’utilisateur dans cette conversation.
Référence documentaire locale : **USER-ADR-001-2026-10-15**,
[décision officielle et périmètre autorisé](VALIDATION-UTILISATEUR-ADR-001-2026-10-15.md).

**Option3 approuvée : architecture modulaire hybride, JARVIS CORE orchestrateur,
adaptateurs interchangeables.** Cette approbation clôt le choix de l’orientation.
Elle n’autorise ni déploiement ni intégration technique. Les contrats v1 restent
proposés ; leur implémentation et toute évolution de schéma ne sont pas approuvées
par cette décision. Aucun raccordement, migration ou changement de signature ici.

## Contexte et continuité

Cette ADR succède aux propositions historiques d’assemblage Android dans UNIFIED,
conservées dans ARCHITECTURE.md. La [revue001F](REVUE-ADR-001F.md) conserve la
comparaison et les propositions antérieures, replacées dans leur contexte historique.
La consolidation est préservée sur mission-001f-closure au commit4f06ef4, et les
missions antérieures restent sur leurs branches d’origine. Aucun main fusionné.

Le code inspecté en001F reste le point de référence daté : CORE utilise son
LlamaLocalEngine interne ; LLM et VOICE sont autonomes ; aucun parcours
CORE↔LLM/VOICE inter-applications n’a été démontré. Approbation de l’architecture,
présence d’un DTO, merge Git et CI verte ne prouvent pas une intégration E2E.
La qualification physique est une preuve supplémentaire distincte.
Aucun nouvel audit GitHub ni résultat matériel n’est déduit de cette validation.

## Architectures comparées et choix

| Option | Bénéfices | Coût / risque / migration | Décision |
|---|---|---|---|
| 1. Monolithe Android | Appels directs, processus et arbitrage plus simples | Harmonisation SDK24/26/29 et outils natifs ; déploiement/signature communs ; risque de régression des fonctions historiques | Non imposé. Un APK unique reste une possibilité de déploiement à qualifier, sans décision actuelle |
| 2. Applications indépendantes reliées par IPC local | Isolation des données, livraisons indépendantes, conservation des prototypes | Coût RAM multi-processus, UID/certificats, versions, panne et migrations à sécuriser ; aucun IPC actif démontré | Les applications autonomes sont conservées initialement ; un transport IPC définitif n’est pas approuvé |
| 3. Hybride modulaire, CORE orchestrateur et adaptateurs interchangeables | Frontières explicites, transition progressive, moteurs remplaçables, portabilité mini-PC et préservation du CORE | Adaptateurs et arbitrage à spécifier/tester ; risque de variantes trop nombreuses ; coût à mesurer sur appareils | **Orientation approuvée avec les précisions ci-dessous** |

Recommandation retenue : option3, car elle permet une migration progressive et
réversible sans sacrifier les fonctions existantes ni l’autonomie hors ligne.
« Hybride » désigne la modularité et les adaptateurs ; aucun cloud obligatoire.
Le choix logique des modules n’impose pas le nombre de paquets Android.

## Architecture et responsabilités approuvées

| Composant | Responsabilité approuvée | Frontière et état d’implémentation |
|---|---|---|
| UNIFIED | Registre technique central, contrats, versions, compatibilités, preuves de tests et feuille de route | Aucun rôle d’orchestrateur à l’exécution ; ni troisième moteur ni runtime Android |
| CORE | Autorité centrale des sessions, décisions, permissions, confirmations et orchestration | Conserve les fonctions et données historiques jusqu’à remplacement démontré ; un moteur ne décide pas des droits |
| LLM | Inférence locale, moteurs et modèles interchangeables | Ne possède pas l’autorité métier ou la confirmation des souvenirs ; code autonome actuel non raccordé |
| VOICE | Synthèse vocale, identités vocales et fonctions associées | Compatibilité exacte moteur/pack/profil ; capture/STT reste dans CORE tant qu’une migration distincte n’est pas autorisée et testée |
| INTERFACE | Interface utilisateur et avatar | Interface commune objectif ultérieur ; aucun rendu ou raccordement nouvellement validé |
| NEXUS | Cible future pour documents, recherche et stockage des souvenirs confirmés | CORE conserve l’autorité de confirmation ; aucune migration physique du stockage SQLite réalisée ni autorisée |
| SERVICES | Fonctionnalités complémentaires soumises aux autorisations CORE | Pas d’appel implicite autorisé par une sortie LLM ou un document |
| EVOLUTION | Diagnostics et propositions de correctifs isolés | Jamais d’application automatique sans approbation ; identité du dépôt candidat à confirmer |

JARVIS-CENTRAL assure la coordination humaine. Sa conversation n’est ni une
synchronisation GitHub ni une preuve de code ; les références techniques et
résultats vérifiables restent dans UNIFIED.

## Précisions obligatoires approuvées

### A — Modularité et déploiement

Conserver initialement les applications autonomes existantes. Une interface
commune est un objectif ultérieur. Ne pas imposer huit APK distinctes ni un
monolithe unique. Le déploiement définitif sera décidé **après qualification**.
Aucun adaptateur ou backend n’est développé par cette approbation.

### B — Ressources et protections matérielles

Pour la configuration Android pilote, **privilégier un seul travail lourd à la fois**.
Maintenir les protections RAM, température, batterie et annulation.
Aucun second chargement non maîtrisé. Plusieurs modèles résidents ne pourront
être autorisés que sur une configuration matériellement qualifiée, avec arbitrage
vérifié ; cette possibilité future ne qualifie aucun matériel et ne donne aucune
autorisation immédiate de chargement supplémentaire.

Le mode **PLEINE PUISSANCE** est conservé pour un futur matériel adapté ; aucune
activation prématurée sur téléphone ou tablette. Aucun seuil d’admission abaissé.
Stop demandé, fin native et libération réelle demeurent trois états distincts.
Le coordinateur LLM actuel est limité à son processus ; aucun arbitre global
n’est implémenté ou situé par cette décision. Les modèles TABLET Qwen3 0.6B
Q4_K_M et MOBILE1.7B sont des références initiales, pas des limites définitives.

### C — Préservation et mémorisation

Aucune suppression des fonctions historiques CORE sans remplacement fonctionnel
démontré. Toute migration de données doit être réversible, précédée d’une
sauvegarde vérifiée et accompagnée de tests de restauration. Préserver SQLite,
documents, profils vocaux, signatures et données privées. Aucune migration réelle
n’est autorisée ici ; le prototype de sauvegarde UNIFIED reste fictif.
JVBK fictif et archive vocale JVIENC01 ne sont pas déclarés interopérables.

Toute **nouvelle mémorisation personnelle durable exige la confirmation explicite
du contenu exact**. Une génération, un import PDF ou un diagnostic ne vaut pas
confirmation. Session volatile, historique de conversation, catalogue éditorial,
souvenirs durables et contexte natif restent distincts. La télémétrie « memory »
du LLM n’est pas une mémoire personnelle. Le parcours commun de confirmation
n’est pas déclaré implémenté ; aucune donnée legacy n’est supprimée ou migrée.

### D — Portabilité et fonctionnement local

Préserver le fonctionnement **100 % local et hors ligne**, préparer Android →
mini-PC avec moteurs remplaçables. GitHub sert au développement et à la traçabilité,
jamais de dépendance obligatoire au runtime. Mini-PC et backends futurs restent
à qualifier ; Android doit conserver son fonctionnement autonome.

## Décisions expressément ouvertes — non approuvées

1. Le transport IPC définitif.
2. La stratégie de signature et d’authentification entre applications.
3. Le nombre définitif d’APK.
4. L’emplacement et l’implémentation de l’arbitre global de ressources.
5. Les migrations physiques de données.
6. Le renommage ou la suppression des dépôts candidats.
7. Les paramètres de performance non qualifiés sur appareils.

Ces sujets nécessitent des propositions techniques et, lorsqu’il y a un changement
sensible, une autorisation distincte. Le rôle NEXUS est approuvé comme cible future,
non comme autorisation de transférer des données. Les noms exacts INTERFACE-,
VOLUTION- et autres candidats sont conservés ; aucune équivalence imposée.
Les contraintes API24 CORE / API29 LLM / API26 VOICE et INTERFACE observées en001F
restent à qualifier, sans hausse de minSdk ou retrait de support par cette ADR.

## Contrats v1 : conservés, évolutions seulement proposées

Les cinq schémas, exemples et leur sémantique ne sont pas modifiés. Les messages
proposés définissent capacités, corrélation, références privées, délais,
annulation, réponses et baux ; aucun transport ni broker ne devient opérationnel.
L’approbation de l’orientation n’accepte pas automatiquement les détails de ces
contrats ou les propositions plus précises de la revue001F.

À proposer et faire valider séparément avant toute évolution de contrat :

- Définir la portée de coordination (processus, appareil ou futur PC), l’autorité
  d’admission et la preuve de qualification matérielle. Ne pas généraliser une
  éventuelle multi-résidence qualifiée au pilote Android ou aux anciens appareils.
- Évaluer si resource-lease et capability-manifest suffisent : association des
  baux, enveloppes et modèles, génération, décès de processus, expiration et
  preuve de fin/déchargement. Aucun nouveau champ ou schéma créé ici.
- Proposer identité/authentification, mapping DTO VOICE et opérations NEXUS/SERVICES,
  négociation de versions et sérialisation bornée. Ne pas confondre une référence
  d’autorisation textuelle avec une identité vérifiée. UID/certificats/permissions
  restent des pistes à évaluer, pas une stratégie approuvée.
- Maintenir une corrélation session/opération et le refus des réponses périmées,
  annulation idempotente et récupération après panne ; spécification et tests
  restent à autoriser. Les schémas fermés exigent une version négociée avant tout
  ajout incompatible ; aucune modification automatique.

L’ancienne proposition « un lourd et un modèle » reste une prudence du pilote à
spécifier. Elle ne constitue plus une interdiction universelle de toute future
multi-résidence qualifiée. Les contrats existants ne réalisent ni cette exception
ni un contrôle matériel : aucun changement runtime ne découle du présent texte.

## Portée autorisée et suites

La présente opération est exclusivement documentaire dans UNIFIED, sur une
branche préservant la consolidation. Aucun merge/main, déploiement, modification
de dépôt externe, adaptateur, raccordement CORE/LLM/VOICE, migration, suppression
de code ou contournement des droits GitHub n’est autorisé.

Prochaine action recommandée : rétablir la publication documentaire par la voie
autorisée, puis soumettre une mission distincte et limitée de proposition des
choix techniques ouverts. La qualification de CORE/LLM/VOICE reste une mission
séparée à autoriser ; aucun déploiement ou développement supplémentaire lancé.
L’approbation de l’orientation n’a plus à être redemandée.
