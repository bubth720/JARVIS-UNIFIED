# Dépendances, ownership et restrictions
## Propriétaires techniques
CORE possède les sessions, permissions et souvenirs confirmés, IDENTITY personnalise sans devenir autorité. LLM possède l'unique moteur local, VOICE les voix et le SDK audio, INTERFACE et AVATAR partagent leur dépôt mais gèrent UI/rendu distincts, SERVICES les outils/actions, NEXUS les archives/index, EVOLUTION le diagnostic et les correctifs en sandbox, UNIFIED les contrats et registres.

## Interfaces et risques
- **JNI LLM** : LLM-02/03 ne peut appliquer aucune modification native sensible sans approbation du diff, et F3B reste en revue.
- **IPC CORE/VOICE/LLM** : CORE-03 et VOICE-03 peuvent développer ports opt-in ; activation production distincte et refus fail-closed.
- **Sandbox EVOLUTION** : EVOL-03/04 n'exécute aucune commande non fiable hors OS sandbox adapté et autorisé ; aucune écriture dans une branche réelle.
- **Données personnelles** : MEM-01/02 et NEX-05 ne migrent/exportent pas les données privées sans accord ; stockage local uniquement.
- **ZIM encyclopédique** : NEX-04 doit vérifier disponibilité, licence et ABI du lecteur ; aucun téléchargement automatique.
- **MVP** : GGUF vérifié octet par octet. Pas de preuve Android ARM64 JNI ni de GO personnel : MVP-005, 006, 007 restent des portes indépendantes.
- **Git** : Toutes les nouvelles branches `plan/intensive-2026-10-22` sont documentaires, distinctes de main, et ne démarrent aucun agent.

## Contrôle par preuves
Une mission peut être déclarée DEVELOPED uniquement après code, build/démo/test et commit ; une mission dépendante attend la livraison de ses ports. Toujours signaler module, mission, branche, commit, tests, blocages, action suivante.
