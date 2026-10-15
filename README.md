# JARVIS-UNIFIED — référence technique centrale

**UNIFIED coordonne les preuves, registres, contrats et plans. Ce dépôt n’est ni
un runtime Android, ni un troisième moteur LLM, ni une application doublon.**
L’orientation est formalisée dans [ADR-001](docs/DECISIONS/ADR-001-CORE-LLM-UNIFIED.md),
**proposée — en attente de validation utilisateur**. Aucun raccordement applicatif
n’est développé pendant cette consolidation.

## Clôture 001F

**Terminée localement, publication bloquée HTTP403.** Branche de reprise
`mission-001f-closure`, issue de d74730a ; anciennes branches inchangées.
[Bilan général CENTRAL](JARVIS_CENTRAL_BILAN_GENERAL.md),
[décision utilisateur non approuvée](docs/DECISIONS/REVUE-ADR-001F.md),
[preuves et tests frais](reports/001f/README.md),
[reprise publication et récupération](docs/RUNBOOK.md).
VOICE005I observée à f917ef1 ; code applicatif inchangé, nouveaux rapports CI
versionnés de coinstallation émulateur. Pas de qualification Xiaomi nouvelle.

## Qui fait quoi — actuel et cible

| Module / dépôt exact | Code actuel inspecté | Responsabilité cible proposée |
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

Prochaine action : faire valider l’ADR, puis stabiliser CORE et qualifier LLM003B
sur appareils avant **une mission distincte autorisée d’adaptateur local**.
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
**supplantée comme proposition cible par la nouvelle ADR**, sans effacer l’historique.
