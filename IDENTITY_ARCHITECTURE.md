# ID-001 — architecture proposée et état des modules

**Proposition V1, non implémentée.** La constitution définit le comportement ;
CORE conserve l’autorité. UNIFIED ne devient ni runtime ni base de données privée.
Base de travail : décision documentaire UNIFIED
`8ddac8fe8a1861a27d3abeca81eb4ab8f110c3a9`, descendante de D4-02D27e6740.
Cette base préserve l’accord expérimental V1–V5 sans l’étendre à IDENTITY.

## Répartition et réemploi

| Module | Rôle IDENTITY proposé | Réemploi et frontière |
|---|---|---|
| CORE | IdentityManifest, IdentitySnapshot, IdentityPolicy, IdentityComposer et IdentityPort ; décisions de session/confirmation, vérification des résultats | Prompt système séparé et budgets existants ; aucun second LLM. Historique, SQLite, Whisper et modes historiques conservés |
| LLM | Inférence et comptage réel du rendu autorisé ; modèle interchangeable, capacité séparée pour SYSTEM | Même moteur llama.cpp/backend et catalogue SQLite existants. Ni stockage de personnalité personnelle ni autorité d’outil/mémoire |
| SERVICES | Fournisseur initial **proposé** de stockage versionné ID-003 via port, réemploi qualifié de MEMORY/GUARD | Namespace d’identité isolé, aucun accès direct aux bases historiques. Guard renforce/refuse, ne crée pas un consentement CORE |
| NEXUS | Cible future du domaine documentaire et du stockage des souvenirs confirmés | Pas encore moteur ni stockage prouvé. Changement de propriétaire physique ultérieur séparé, réversible et sans double écriture |
| EVOLUTION candidat | Diagnostics et propositions isolées, diff/mesures/retour arrière | Pas de moteur existant présumé ; aucun droit d’auto-appliquer, modifier permissions ou se valider lui-même |
| VOICE | Expression du texte final autorisé avec identité/profil/pack exacts | VoicePersonaDescriptor n’est pas IdentityManifest ; CoreVoiceRequestV1 reste fermé. Métadonnée HUMOROUS ne prouve pas une modulation acoustique |
| INTERFACE | Vue des propositions/consentements et intentions visuelles bornées | AvatarSession est actuellement un contrat sans renderer ; renderer futur, visibilité et libération des ressources à qualifier |
| UNIFIED | Constitution, interfaces proposées, compatibilités, preuves et feuille de route | Aucune session réelle, clé, voix ou préférence personnelle dans Git ; aucune orchestration d’exécution |

## Parcours cible, non raccordé

Entrée utilisateur → CORE valide session/permissions et charge un snapshot approuvé
→ Composer produit le SYSTEM autorisé → LLM compte le prompt final avec le vrai
modèle/template et génère → CORE valide corrélation/état/annulation/provenance
→ texte final, puis VOICE/INTERFACE seulement si disponibles et autorisés.
Les réponses locales CORE et catalogue LLM restent utilisables, sans nouvelle base
de formulations et sans obligation de charger le modèle pour afficher une préférence.

Le manifeste technique peut être embarqué localement. L’état privé passe par
IdentityPort ; pas de dépendance réseau ni PC. NEXUS absent ne doit pas empêcher
une personnalité de base approuvée de fonctionner hors ligne. ID-002 peut fournir
une implémentation minimale **en lecture seule** du manifeste approuvé, avec
snapshot volatil et sans mémoire personnelle ; ID-003 ajoute l’état durable privé.
Pas de stockage provisoire concurrent de préférences dans CORE pour contourner
l’absence du port SERVICES. Aucun transport IPC n’est décidé pour ce port.

IdentityPolicy vérifie les contraintes déterministes ; le LLM n’accorde aucun droit.
IdentityComposer ne fusionne pas permissions et texte. Le SYSTEM brut inclut la
personnalité approuvée une fois, sans reproduire la politique fixe native LLM,
le template GGUF ou les tokens de rôle. Contexte/historique/docs gardent leur
provenance et leur classe de confiance ; aucun document ne devient SYSTEM.
Le comptage porte sur le rendu réel total, pas seulement le fragment persona.
Les limites/annulations/quarantaines existantes demeurent supérieures au style.

## SERVICES et NEXUS : éviter une seconde mémoire

Un propriétaire d’écriture par namespace et appareil. ID-003 proposerait un
namespace privé identity.* hébergé par SERVICES, sans déplacer CORE.memories,
les documents ou profils. NEXUS reste propriétaire cible du domaine mémoire après
qualification ; il pourra utiliser le même port/implémentation ou une transition
explicitement autorisée, jamais une réplication silencieuse vers une seconde base.
Les propositions non personnelles peuvent être durables ; une proposition contenant
un fait personnel reste volatile jusqu’à consentement de son **propre stockage**.

Guard actuel confirme le digest du contenu, opération, principal, délai60s et
usage unique en mémoire. Memory.save consomme cette confirmation puis écrit une
version ; il ne fournit pas le cycle PENDING/APPROVED/REJECTED ni une preuve de
consentement durable transactionnelle suffisante pour IDENTITY. Guard.Context est
une capacité créée par l’hôte de confiance, pas une identité IPC authentifiée.
L’audit Guard est borné à500 lignes : il n’est pas un registre d’approbations
complet ou inviolable. Réemploi des primitives **après adaptations/test**, pas
annonce d’un ID-003 déjà prêt. Recovery SERVICES est un paquet logique distinct,
non chiffré par ce code, pas le format de backup UNIFIED ni une archive VOICE.

## Compatibilité et conflits recensés

| Point | Risque / conflit potentiel | Traitement proposé et porte requise |
|---|---|---|
| Identité qui décide de ses permissions | Contradit CORE autorité de l’ADR | Persona ne donne que préférences de formulation ; refus de champs/capacités non autorisés |
| SERVICES MEMORY vs NEXUS vs CORE SQLite | Plusieurs maîtres et mémoire personnelle non consentie | Namespace distinct, pas de migration ; choix d’hébergement ID-003 à approuver et propriété cible documentée |
| « Préférences de JARVIS » auto-apprises | Auto-modification et persistance cachée | Valeurs techniques explicites, candidats sans effet, décision extérieure et application transactionnelle |
| Prompt plus long | Dépassement contexte, perte de question/sources ou déplacement en user | Refus/recomposition explicite d’un budget, comptage natif requis pour chemin P2 ; aucun contournement ni suppression silencieuse |
| Modèle différent | Variance de ton et limites de SYSTEM | Snapshot identique et adaptateur qualifié ; si incapable, refus du mode identité, historique conservé et signalé, pas d’équivalence déclarée |
| VOICE/INTERFACE | Copier identité vocale, inventer émotion ou renderer | Adaptateurs de style sans poids/profils ; capacités exactes, repli neutre explicite/texte seul si nécessaire |
| EVOLUTION | Auto-validation sensible ou nouveau moteur | Sandbox, moteur local existant uniquement si autorisé et sérialisé, approbation extérieure, ID-006 non bloquant pour Alpha |
| Restaurer une ancienne préférence | Résurrection de consentements/permissions révoqués | Intersection avec révocations et consentements actuels, prévisualisation et confirmation, aucun ancien grant restauré |
| IDENTITY dans fixture /2 | Corpus/contrat fermés et bootstrap fragile | Interdiction explicite ; projet et tests d’identité indépendants, aucun champ persona ajouté aux fixtures |

Aucun amendement ADR n’est appliqué. Les transports définitifs, signatures,
arbitre, migrations et nombre d’APK restent dans leurs portes existantes. La
validation expérimentale D4-02D n’est pas une autorisation de ces changements.

## Photographie Git vérifiée le17 octobre 2026

Les têtes ci-dessous ont été récupérées en lecture seule via copies bare ignorées.
Un commit ou rapport versionné ne constitue pas une CI observée ou un test matériel.

| Dépôt exact | Branche et SHA observés | Portée du constat |
|---|---|---|
| bubth720/JAVIS-Local-v2 | fixture/004c-p2-client — da40ed7155409b85860a22c1dbbfe35029cea29a | Contrats/PromptBuilder/SQLite lus ; 004D non observée dans les refs accessibles |
| bubth720/JARVIS-LLM | fixture/003f-bootstrap-attestation — ac678de9b8c04f913b117d2d6bda034108523756 | Candidat /2, blocages F1/F2/F3 et mapping commit déclarés, génération /2 non activée ; aucune consommation CORE004D autorisée par ID-001 |
| bubth720/JARVIS-SERVICES | mission-002a-android-qualification — 0f462c8ad5529ba974cefa17fe6562c8d8461d26 | GUARD/MEMORY/Recovery et architecture lus, intégration CORE non démontrée |
| bubth720/JARVIS-VOICE | feat/voice-core-bridge-005k — 521e613448083ffe6d575de2c9c369b48fb901f8 | Contrats005I réemployés, document005K ; pas de pont runtime validé déduit du nom |
| bubth720/JARVIS-INTERFACE | test/interface-device-006 — ebd6c5fc873054d3f04bb2388d53e407dc73b7b7 | AvatarSession sans renderer dans ce code ; qualification physique non déduite du nom de branche |
| bubth720/JARVIS-NEXUS | main — b27df0b84d8f0082d17ca6278549298aaaf97926 | README seul dans l’arbre, pas de stockage implémenté |
| bubth720/JARVIS-VOLUTION- | main — a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0 | README seul ; nom/rôle candidat, aucun moteur EVOLUTION prouvé |

La décision UNIFIED8ddac8f valide D4-02D pour le prototype ; ses textes D4-02D
restent inchangés. Le rapport LLM003F signale des ambiguïtés F1/F2, un port natif
post-recovery incomplet F3 et une formule de commit à revoir. **ID-001 les signale
sans les corriger ou les approuver.** Un chantier de raccordement bloqué ne justifie
ni l’insertion d’une persona dans /2 ni un second moteur pour IDENTITY.

## Sources immuables relues

- [JARVIS-SERVICES/shared-runtime/src/main/java/fr/jarvis/services/modules/guard/Guard.java](https://github.com/bubth720/JARVIS-SERVICES/blob/0f462c8ad5529ba974cefa17fe6562c8d8461d26/shared-runtime/src/main/java/fr/jarvis/services/modules/guard/Guard.java).
- [JARVIS-SERVICES/shared-runtime/src/main/java/fr/jarvis/services/modules/memory/Memory.java](https://github.com/bubth720/JARVIS-SERVICES/blob/0f462c8ad5529ba974cefa17fe6562c8d8461d26/shared-runtime/src/main/java/fr/jarvis/services/modules/memory/Memory.java).
- [JARVIS-SERVICES/shared-runtime/src/main/java/fr/jarvis/services/shared/api/Contracts.java](https://github.com/bubth720/JARVIS-SERVICES/blob/0f462c8ad5529ba974cefa17fe6562c8d8461d26/shared-runtime/src/main/java/fr/jarvis/services/shared/api/Contracts.java).
- [JARVIS-SERVICES/shared-runtime/src/main/java/fr/jarvis/services/shared/storage/Recovery.java](https://github.com/bubth720/JARVIS-SERVICES/blob/0f462c8ad5529ba974cefa17fe6562c8d8461d26/shared-runtime/src/main/java/fr/jarvis/services/shared/storage/Recovery.java).
- [JARVIS-SERVICES/docs/ARCHITECTURE.md](https://github.com/bubth720/JARVIS-SERVICES/blob/0f462c8ad5529ba974cefa17fe6562c8d8461d26/docs/ARCHITECTURE.md).
- [JARVIS-VOICE/expressionRuntime/src/main/kotlin/com/jarvis/voice/expression/ExpressionContract.kt](https://github.com/bubth720/JARVIS-VOICE/blob/521e613448083ffe6d575de2c9c369b48fb901f8/expressionRuntime/src/main/kotlin/com/jarvis/voice/expression/ExpressionContract.kt).
- [JARVIS-VOICE/docs/mission005i/EXPRESSION-CAPABILITIES.md](https://github.com/bubth720/JARVIS-VOICE/blob/521e613448083ffe6d575de2c9c369b48fb901f8/docs/mission005i/EXPRESSION-CAPABILITIES.md).
- [JARVIS-INTERFACE/app/src/main/java/com/jarvis/interfaceapp/avatar/AvatarContract.kt](https://github.com/bubth720/JARVIS-INTERFACE/blob/ebd6c5fc873054d3f04bb2388d53e407dc73b7b7/app/src/main/java/com/jarvis/interfaceapp/avatar/AvatarContract.kt).
- [JARVIS-LLM/docs/mission-003f/RAPPORT.md](https://github.com/bubth720/JARVIS-LLM/blob/ac678de9b8c04f913b117d2d6bda034108523756/docs/mission-003f/RAPPORT.md).
- [JARVIS-LLM/docs/mission-003f/PREUVES.md](https://github.com/bubth720/JARVIS-LLM/blob/ac678de9b8c04f913b117d2d6bda034108523756/docs/mission-003f/PREUVES.md).
- [JARVIS-LLM/fixtures/p2-contract/CONTRACT.txt](https://github.com/bubth720/JARVIS-LLM/blob/ac678de9b8c04f913b117d2d6bda034108523756/fixtures/p2-contract/CONTRACT.txt).
- [JARVIS-LLM/fixtures/p2-contract/src/main/java/fr/jarvis/fixture/p2/Wire.kt](https://github.com/bubth720/JARVIS-LLM/blob/ac678de9b8c04f913b117d2d6bda034108523756/fixtures/p2-contract/src/main/java/fr/jarvis/fixture/p2/Wire.kt).
- [JARVIS-LLM/domain/src/main/kotlin/fr/jarvis/domain/generation/P2Contract.kt](https://github.com/bubth720/JARVIS-LLM/blob/ac678de9b8c04f913b117d2d6bda034108523756/domain/src/main/kotlin/fr/jarvis/domain/generation/P2Contract.kt).
- [JARVIS-LLM/domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt](https://github.com/bubth720/JARVIS-LLM/blob/ac678de9b8c04f913b117d2d6bda034108523756/domain/src/main/kotlin/fr/jarvis/domain/Conversation.kt).
- [JAVIS-Local-v2/app/src/main/java/com/stark/jarvislocal/PromptBuilder.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/app/src/main/java/com/stark/jarvislocal/PromptBuilder.kt).
- [JAVIS-Local-v2/app/src/main/java/com/stark/jarvislocal/InferenceContract.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/app/src/main/java/com/stark/jarvislocal/InferenceContract.kt).
- [JAVIS-Local-v2/app/src/main/java/com/stark/jarvislocal/LocalDatabase.kt](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/app/src/main/java/com/stark/jarvislocal/LocalDatabase.kt).
- [JAVIS-Local-v2/docs/mission-004c/REPORT.md](https://github.com/bubth720/JAVIS-Local-v2/blob/da40ed7155409b85860a22c1dbbfe35029cea29a/docs/mission-004c/REPORT.md).
- [JARVIS-NEXUS/README.md](https://github.com/bubth720/JARVIS-NEXUS/blob/b27df0b84d8f0082d17ca6278549298aaaf97926/README.md).
- [JARVIS-VOLUTION-/README.md](https://github.com/bubth720/JARVIS-VOLUTION-/blob/a67d3b6d39aa7d30ad38e9b1c9230b4e07180eb0/README.md).

Empreintes des20 blobs source recalculées lors du contrôle documentaire ;
les sorties de cette mission sont dans [IDENTITY_MISSIONS.md](IDENTITY_MISSIONS.md).
