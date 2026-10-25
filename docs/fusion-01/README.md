# FUSION-01 — première tranche UNIFIED

- [Architecture, ownership et ordre](ARCHITECTURE.md)
- [BOM généré et gates](BOM.md), [verrou machine](../../integration-lock.json)
- [Contrats/limites et menaces](CONTRACTS_ET_MENACES.md)
- [Matrice d'intégration et scénarios F8](unified-integration-matrix.md)
- [Audit CORE/LLM](AUDIT-CORE-LLM.md)
- [Audit NEXUS/SERVICES et échecs CI](AUDIT-NEXUS-SERVICES.md)
- [Audit INTERFACE/VOICE/EVOLUTION](AUDIT-INTERFACE-VOICE-EVOLUTION.md)
- [Guide de l'outil](../../tooling/integration/README.md)

Les sources machine dans `evidence/` conservent SHA, graphes, toolchains,
sourceSets, licences inconnues, limites et observations CI. Aucun média/poids ni
contenu utilisateur recopié. `remote-heads.json` inventorie les branches distantes,
mais seules les références explicitement auditées sont qualifiées pour le BOM.
Les trois audits séparent tests historiques relus et tests frais UNIFIED.

Validation structurelle ne signifie pas validation runtime. FUSION-01 complète
reste PARTIAL/BLOCKED ; l'orientation ADR est conservée, aucune gate sensible levée.
Le rapport final de livraison complète ces documents avec commandes et résultats.
