# Plan CORE↔LLM — implémentation future soumise à autorisation

Ce plan n’autorise aucun changement de CORE/LLM. Bases : CORE226e2e8, LLM1756e29,
contrats proposés1.0.0 ; [ADR-001](DECISIONS/ADR-001-CORE-LLM-UNIFIED.md).

1. Stabiliser CORE seul : tests de référence commandes/PDF/RAG/SQLite/Whisper/voix,
   capture finalisée, cycle de vie, opérations concurrentes, données synthétiques
   puis sauvegarde réelle consentie. Garder original/installations/signature.
2. Qualifier LLM003B : premier plan, diagnostic passif puis chargement naturel
   admis, PSS/RSS/thermique/batterie et Arrêt/déchargement. Pas de stress forcé,
   budget diminué ou PLEINE PUISSANCE pour faire passer l’essai.
3. L’orientation ADR est approuvée avec précisions le15 octobre2026. Faire
   approuver séparément API supportées, transport, signatures et arbitrage avant
   toute mise en œuvre. Choisir explicitement
   un adaptateur intraprocessus ou IPC ; ne pas additionner arbitrairement deux
   APK. Client authentifié par UID/certificat/permission, service non exporté par
   défaut, toute exposition avec contrôle d’identité et quotas testés.
4. Implémenter la négociation de capacités et les enveloppes, sans génération
   d’abord. Adapter les bornes réelles de LanguageModel (messages/contexte/sortie),
   préparer budget tokenisé et références de contenu privées, jamais URI arbitraire.
5. Brancher un seul backend et l’arbitre pertinent : un lourd/résidence active,
   bail conservé après Stop jusqu’au retour natif puis destruction. Prévoir mort
   de client/service, reconnexion, réponse tardive, incompatibilité et refus.
6. Tester : absent, refusé, incompatible, timeout/expiration, annulation pendant
   load/generate, arrière-plan/rotation/redémarrage, cleanup_failed, double appel,
   perte de connexion et IDs périmés. Aucun replay automatique d’écriture/outil.
7. Comparer au CORE historique sur corpus textuel/PDF/commandes et données restaurées.
   Désactiver l’ancien moteur seulement après parité et validation utilisateur ;
   préserver le rollback vers ancienne installation et sa sauvegarde cohérente.
8. Qualification API29+ sur appareils ; API24–28 reste une porte explicite, pas une
   compatibilité présumée. Release/signature/stocks/données et mode avion testés.

Critère de sortie : code de liaison identifié, chemin d’exécution démontré, tests
au SHA exact et mesures physiques ; une branche/PR distincte, pas de merge
silencieux. Le format d’archive fictif UNIFIED ne suffit pas à récupérer les sandbox
Android. Références vocales et identité restent sélectionnées/confirmées par
l’utilisateur ; pas de TTS générique imposé ou conversion de profil universel.
