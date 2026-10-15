# JARVIS-UNIFIED

Préparation d'une application Android JARVIS unique, modulaire et entièrement
hors ligne. **Mission 001 : audit et conception uniquement.** Ce dépôt ne contient
encore ni application fusionnée, ni moteur intégré, ni APK UNIFIED.

## Documents de référence

- [AUDIT.md](AUDIT.md) — branches et SHAs, fonctions présentes, preuves, limites et décisions de conservation.
- [ARCHITECTURE.md](ARCHITECTURE.md) — CORE / LLM / VOICE, contrats proposés, ressources, mémoire confirmée, sauvegarde et futur PC.
- [MIGRATION_PLAN.md](MIGRATION_PLAN.md) — missions courtes, critères de passage et retour arrière.
- [TEST_PLAN.md](TEST_PLAN.md) — contrôles réellement effectués et qualification à réaliser.

## Direction retenue pour préparation

CORE reprend orchestration, historique, mémoire, documents et Whisper de
[bubth720/JAVIS-Local-v2](https://github.com/bubth720/JAVIS-Local-v2).
LLM reprend le backend unique et les protections de
[bubth720/JARVIS-LLM](https://github.com/bubth720/JARVIS-LLM), branche 003B.
VOICE prépare la synthèse neuronale et les profils personnels de
[bubth720/JARVIS-VOICE](https://github.com/bubth720/JARVIS-VOICE), branche Android
005D/E/F/G. Aucun TTS Android générique ne remplace la voix personnalisée.

Références initiales : TABLET Redmi Pad SE / Qwen3 0,6B Q4_K_M ; MOBILE POCO X8 Pro /
Qwen3 1,7B Q4_K_M ; CENTRAL mini-PC et modèles à qualifier. Ces références restent
évolutives ; elles ne constituent pas une qualification matérielle.

Les profils vocaux FP32 ont une implémentation et des tests historiques, mais
la ressemblance personnelle et le naturel sur les appareils cibles restent à
valider. Aucun service cloud obligatoire, aucune fusion dans main, aucun dépôt
source modifié ou supprimé pendant cette mission.

## État et prochaine étape

Livrables préparés sur `audit/mission-001`. Accès Git, intégrité des clones,
provenance des branches, empreinte de la politique LLM, concordance des APK vocales
005F/G et fixture SQL vérifiés. Suites Android et inférences non rejouées ; leurs
résultats historiques sont explicitement séparés dans l'audit.

Mission recommandée : **002 — sécuriser la récupération et la restauration des
données et profils**, avec fixtures synthétiques et inventaire local des
installations, avant toute intégration. Les données personnelles, poids privés
et clés ne doivent pas être déposés dans ce dépôt.

Aucune commande de compilation UNIFIED n'existe à cette étape. Travailler dans
le checkout existant, sans worktree supplémentaire ; les tests futurs et leurs
prérequis sont décrits dans TEST_PLAN.md.
