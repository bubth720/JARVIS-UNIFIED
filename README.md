# JARVIS-UNIFIED — référence technique centrale

## Campagne intensive du22octobre2026

Les outils exécutables sont disponibles dans [tooling/contracts](tooling/contracts/README.md)
et [tooling/campaign](tooling/campaign/README.md). Génération Java/Kotlin strictement
hors runtime, comparaison de compatibilité et registre de dépendances/preuves Git ;
aucun contrat v1 modifié ni lancement automatique d'agent.
[État vérifié de campagne](docs/intensive-2026-10-22/VERIFIED_STATUS.md) et
[guide du registre](registry/intensive-2026-10-22/README.md). Les livraisons logicielles
ne constituent pas une qualification JNI, vocale ou Android physique. Les
instantanés historiques ci-dessous restent datés et conservés.

**UNIFIED coordonne les preuves, registres, contrats et plans. Ce dépôt n’est ni
un runtime Android, ni un troisième moteur LLM, ni une application doublon.**
L’orientation est formalisée dans [ADR-001](docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md),
**APPROUVÉE AVEC PRÉCISIONS le 15 octobre 2026 — orientation uniquement**. Aucun raccordement applicatif
n’est développé pendant cette consolidation.

## D4-02 — responsabilités et premier raccordement proposé

[Matrice consolidée proposée](docs/D4-02/MATRICE_RESPONSABILITES.md),
[adaptations/contrats](docs/D4-02/ADAPTATIONS_ET_CONTRATS.md),
[plan CORE↔LLM](docs/D4-02/PREMIER_RACCORDEMENT_CORE_LLM.md),
[risques](docs/D4-02/RISQUES_ET_PROTECTIONS.md),
[décisions et missions ordonnées](docs/D4-02/DECISIONS_ET_MISSIONS.md),
[rapport et sources fraîches](docs/D4-02/RAPPORT_ET_SOURCES.md).
Conception documentaire seule ; CORE004A et LLM003C relus, pas encore raccordés.
Le mapping du prompt système, le cycle de vie et l’admission interprocessus exigent
des décisions techniques distinctes ; l’orientation ADR reste approuvée, inchangée.

## DESIGN-004 — conception multi-appareils et expressions

[Architecture SYNC V1](docs/DESIGN-004/SYNC_V1.md),
[EXPRESSIONS V1](docs/DESIGN-004/EXPRESSIONS_V1.md),
[responsabilités et réserves ADR](docs/DESIGN-004/RESPONSABILITES_ET_ADR.md),
[contrats proposés](docs/DESIGN-004/CONTRATS_INTEGRATION_PROPOSES.md),
[missions suivantes](docs/DESIGN-004/MISSIONS_SUIVANTES.md) et
[rapport sourcé](docs/DESIGN-004/RAPPORT_DESIGN_004.md).
Conception documentaire uniquement : pas de sync réelle ni de bibliothèque800
formulations déjà livrée. Les sources du16 octobre complètent la photographie001F :
SERVICES dispose maintenant de fondations et BRIDGE simulé, VOICE de Studio005J
et d’un cahier005K, INTERFACE d’un stockage local005. Les nouveaux rôles de stockage,
transports et contrats restent à proposer/autoriser séparément ; ADR inchangée.

## Décision officielle ADR-001

Option3 approuvée : CORE orchestrateur, architecture modulaire hybride et
adaptateurs interchangeables. Applications autonomes conservées initialement ;
aucun nombre d’APK imposé. Pour le pilote Android, privilégier un travail lourd ;
multi-résidence seulement sur matériel qualifié et arbitrage vérifié, sans second
chargement non maîtrisé. Contrats v1 inchangés et toujours proposés.
[Validation utilisateur et réserves](docs/DECISIONS/VALIDATION-UTILISATEUR-ADR-001-2026-10-15.md).
Aucun déploiement, raccordement ni migration autorisé par cette approbation.
[Vérifications de cette consignation](docs/DECISIONS/VERIFICATION-APPROBATION-ADR-001.md) :
rapport historique de l’approbation : 79/80. Le défaut du compteur a ensuite
été corrigé exclusivement en [Mission001G](MISSION_001G_REPORT.md) : **80/80
réussis, aucun saut**. Registre et ADR inchangés.

## Maintenance001G

Sept branches utiles publiées sans forçage, SHA distants vérifiés ; main inchangée.
PR brouillon non créée : API GitHub bloquée par le proxy.
[Rapport et opérations restantes](MISSION_001G_REPORT.md). La branche
mission-001g-maintenance rassemble consolidation, décision ADR et correctif testé.
Aucune connexion runtime ajoutée.

## Clôture 001F — photographie historique

**Terminée localement, publication bloquée HTTP403.** Branche de reprise
`mission-001f-closure`, issue de d74730a ; anciennes branches inchangées.
[Bilan général CENTRAL](JARVIS_CENTRAL_BILAN_GENERAL.md),
[revue préalable conservée](docs/DECISIONS/REVUE-ADR-001F.md),
[preuves et tests frais](reports/001f/README.md),
[reprise publication et récupération](docs/RUNBOOK.md).
VOICE005I observée à f917ef1 ; code applicatif inchangé, nouveaux rapports CI
versionnés de coinstallation émulateur. Pas de qualification Xiaomi nouvelle.

## Qui fait quoi — photographie001F et cible ADR

Le tableau ci-dessous conserve la lecture001F. Pour les développements plus récents
SERVICES/VOICE/INTERFACE, lire les [sources DESIGN-004](docs/DESIGN-004/SOURCES.md)
et la [matrice de responsabilités](docs/DESIGN-004/RESPONSABILITES_ET_ADR.md).

| Module / dépôt exact | Code actuel inspecté | Responsabilité cible approuvée — déploiement non autorisé |
|---|---|---|
| CORE — bubth720/JAVIS-Local-v2 | Monolithe : commandes/routage, SQLite, PDF/RAG, wrapper LLM, Whisper, TTS et UI | Orchestration, sessions, permissions et souvenirs confirmés ; conserver les fonctions jusqu’au remplacement testé |
| LLM — bubth720/JARVIS-LLM | Application autonome, backend llama.cpp/JNI, import GGUF vérifié, protections et catalogue | Un seul moteur d’inférence interchangeable ; pas la mémoire personnelle ni toute l’orchestration |
| VOICE — bubth720/JARVIS-VOICE | Prototypes neuronaux autonomes, profils/identités/archives, DTO expression005I | Capacités vocales démontrées, profil/pack exact et consentement ; capture/STT à migrer explicitement depuis CORE |
| INTERFACE — bubth720/JARVIS-INTERFACE | UI Compose autonome ; contrat avatar sans rendu | UI/événements et avatar à qualifier, pas un moteur ni CORE |
| bubth720/JARVIS-INTERFACE- | README seul, dépôt distinct | Rôle/relation avec INTERFACE inconnus, conservé |
| NEXUS — bubth720/JARVIS-NEXUS | README seul ; documents actuellement dans CORE | Documents, Wikipedia/Kiwix, index et stockage mémoire futurs ; CORE garde les décisions, aucune migration ici |
| EVOLUTION candidat — bubth720/JARVIS-VOLUTION- | README seul ; alias non confirmé | Diagnostic et correctifs isolés après revue ; aucun auto-déploiement |
| SERVICES — bubth720/JARVIS-SERVICES | README seul | Outils supplémentaires sous permissions |
| UNIFIED — bubth720/JARVIS-UNIFIED | Registre, backup fictif et consolidation locaux ; main distant README initial | Source de vérité technique sans dépendance runtime pour les applications |

JARVIS-CENTRAL dans ChatGPT est une coordination humaine ; une conversation commune
n’est ni une mémoire technique exhaustive ni une synchronisation GitHub.

## Ce qui est fusionné et ce qui communique

- **Merge Git :** les corrections heure/SQLite et documentation CORE sont dans
  son main226e2e8. LLM main917e335 est documentaire, ses branches développées non
  fusionnées ; VOICE mainb80b172 reste README, branches005D/H/I hors main.
  INTERFACE n’annonce pas de main, seulement development/mission-002.
- **Communications :** CORE appelle son propre LlamaLocalEngine, pas l’APK LLM.
  Aucun pont runtime inter-APK CORE↔LLM/VOICE/NEXUS/SERVICES/INTERFACE n’est démontré
  par les sources inspectées. DTO CORE→VOICE005I et AvatarSession sont des
  frontières locales, pas des connexions. Les bibliothèques VOICE internes sont
  bien réutilisées dans ses applications autonomes.
- **Tests :** les tests locaux UNIFIED sont réellement exécutés et détaillés dans
  la [synthèse centrale](docs/COMPTE_RENDU_CENTRAL.md). Les tests Android historiques
  sont séparés des résultats de cette mission. API GitHub/CI actuelle bloquées
  par tunnel proxy403 ; aucune nouvelle CI distante verte annoncée.
- **Appareils :** aucune qualification physique réalisée ici. Pas de promesse de
  clonage/naturel/émotion, d’avatar2.5D rendu ou de compatibilité API24→LLM29.

La [matrice](docs/MATRICE_INTEGRATION.md) donne séparément contrat, code, test,
appareil et main pour chaque lien. Aucun pourcentage d’avancement inventé.

## Consulter les preuves et contrats

- [Inventaire daté](docs/INVENTAIRE.md), [preuves GitHub immuables](docs/PROUVES.md),
  [registre de dépôts](registry/repositories.json), [modules](registry/modules.json)
  et [liens machine](registry/integrations.json).
- [Contrats v1 et sémantique](contracts/v1/SEMANTICS.md), schémas/exemples fermés,
  indépendants du transport ; aucun IPC interprocessus implémenté.
- [Plan CORE↔LLM soumis à autorisation](docs/PLAN_INTEGRATION_CORE_LLM.md),
  [roadmap](docs/ROADMAP.md), [risques](docs/RISQUES.md), [runbook](docs/RUNBOOK.md).
- [Compte rendu directement réutilisable dans CENTRAL](docs/COMPTE_RENDU_CENTRAL.md).

## Vérifier localement

Python3.12 ; nouveaux audit/contrats/registre en bibliothèque standard :

```sh
python3 scripts/validate_unified.py
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s registry/tests -v
python3 scripts/audit_repos.py --offline --output-dir reports/offline
```

La fixture offline est explicitement synthétique, pas un état GitHub réel.
La régression de sauvegarde Mission002 utilise sa dépendance existante
cryptography50.0.0 : `python3 -m unittest discover -s backup_prototype/tests -v`.
Le workflow [validate-unified](.github/workflows/validate-unified.yml) prépare les
mêmes contrôles en PR ; audit live uniquement manuel, lecture seule. Il n’a pas
été exécuté sur GitHub dans cette session. Aucun APK ou modèle construit ici.

Prochaine action : appliquer le réglage réseau API et ouvrir une PR brouillon,
puis soumettre séparément les propositions techniques ouvertes et les missions
de stabilisation/qualification. Aucun adaptateur n’est autorisé ici.
TABLET0.6B Q4_K_M et MOBILE1.7B sont des références initiales ; mini-PC à qualifier.
Ne pas supprimer une fonction, une donnée ou une ancienne installation pour
simplifier la transition. GitHub est utilisé pour le développement, jamais comme
service obligatoire à l’exécution hors ligne.

## Travaux antérieurs préservés

Base locale f7b7a5a sur mission-003-central-registry, précédée de004b89d et55680bc.
Le nouveau cahier est conservé [ici](docs/CAHIER_DES_CHARGES_CONSOLIDATION.md).
Le registre historique, ses champs manuels/snapshots et le backup fictif sont
réutilisés ; aucun de leurs résultats anciens n’est réécrit comme résultat actuel.
[AUDIT.md](AUDIT.md), [ARCHITECTURE.md](ARCHITECTURE.md),
[MIGRATION_PLAN.md](MIGRATION_PLAN.md), [TEST_PLAN.md](TEST_PLAN.md),
[BACKUP_FORMAT.md](BACKUP_FORMAT.md), [RESTORE_PLAN.md](RESTORE_PLAN.md),
[COMPATIBILITY.md](COMPATIBILITY.md) et rapports002/003 restent historiques.
L’architecture ancienne envisageant un assemblage Android dans UNIFIED est
**supplantée comme orientation par l’ADR approuvée avec précisions**, sans effacer l’historique.

## Audit de convergence D4-02C

[Rapport CORE004B ↔ LLM003D](docs/D4-02C/RAPPORT_FINAL.md) : références vérifiées,
matrice et corrections proposées, comparaison O3 et deux missions de fixtures.
Travail documentaire uniquement ; O3 reste à approuver, aucun raccordement réalisé.

## D4-02D — amorçage et réconciliation proposés

[Diagnostic et reprise](docs/D4-02D/BOOTSTRAP_RECOVERY.md),
[protocole expérimental à valider](docs/D4-02D/PROTOCOLE_PROPOSE.md),
[tests exécutés, critères et sources](docs/D4-02D/TESTS_ET_PREUVES.md),
[missions003F/004D proposées](docs/D4-02D/MISSIONS_003F_004D.md).
Le contrôle initial ne charge aucun modèle ; UNKNOWN reste bloquant sans preuve.
Aucune implémentation ni approbation automatique du contrat de fixture /2.
