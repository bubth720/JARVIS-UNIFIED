# JARVIS UNI-08/U02 — Vers un projet unique, modulaire

**STATUT : PROPOSITION À VALIDER.** Aucun regroupement définitif, aucune migration ni activation technique.

## Architecture recommandée

Un seul **produit** JARVIS, mais des modules autonomes, compilables/testables
séparément. UNIFIED reste le registre technique et ne devient ni un runtime,
ni un second CORE/LLM. Il n'est pas nécessaire d'avoir un seul dépôt Git pour
livrer une seule application ; c'est une question de packaging, d'API et de
cycle de vie Android, pas uniquement de répertoire de sources.

```text
JARVIS (interface utilisateur)
  Interface/Avatar [UI, présentation et événements]
          | futur adaptateur signé / local
         CORE [une autorité sessions, permission, admission]
      /     |       |         \
     LLM   VOICE   NEXUS     SERVICES
     IA    TTS/STT docs/RAG outils/écritures
  EVOLUTION : diagnostic isolé et revue, aucun auto-déploiement
  UNIFIED : contrats, registre, lock, preuves, release gates (hors runtime)
```

Tous les traits désignent des **dépendances proposées et INACTIVES**. Aujourd'hui
aucun mécanisme inter-APK, ABI JNI ou qualité Android physique n'est validé
par cette représentation.

## Trois niveaux à ne pas confondre

1. **Workspace fédéré** (préparé ici) : manifest JSON épinglant huit HEAD Git,
   topologie proposée et tests de structure hors ligne ; aucun checkout implicite.
2. **Monorepo modulaire** (non autorisé pour l'instant) : déplacer réellement
   l'historique/source en conservant les noms, namespaces, licences, chemins
   privés et provenance ; choisir subtree/submodules ou import Git contrôlé.
   Cette opération change l'architecture et requiert un accord spécifique.
3. **Une application Android unique** (non qualifiée) : décider quelles
   fonctionnalités sont des bibliothèques internes et quelles applis demeurent
   autonomes, définir un orchestrateur et des limites de ressources communs ;
   qualifier minSdk/ABI, partage mémoire, installations et migrations. Un
   monorepo ne prouve pas l'existence d'un APK unifié.

## Compatibilité et économie de modifications futures

- Chaque module possède un contrat versionné, une API publique testée, une
  implémentation et des tests isolés. Les clients consomment une interface,
  non les classes internes des autres modules.
- Les pipelines **changed-module** ne relancent que les tests du module touché,
  puis les contrats de ses consommateurs. Une campagne de régression complète
  est obligatoire avant promotion d'une distribution. Cette optimisation ne
  supprime pas les tests de régression globaux aux jalons.
- CORE seul émet les décisions d'action et les jetons de confirmation ; les
  outils, documents, modèles et modules vocaux restent remplaçables.
- Au départ API24/25 pour CORE/NEXUS/SERVICES, API26 pour UI/VOICE,
  API29 pour le client LLM examiné. Une APK unique ciblant API24 et contenant
  ce runtime API29 ne serait pas qualifiée. Compatibilité par appareil /
  feature-flag strict, sans charger plusieurs gros moteurs.
- Mode hors ligne, import manuel et absence de téléchargement d'exécution
  restent les invariants. Ne jamais considérer GitHub nécessaire au fonctionnement
  de JARVIS sur Android.
- NEXUS : le FTS5 du SQLite système est indisponible sur émulateurs API24/25
  testés ; aucun RAG Android valide dans ce chemin sans backend qualifié.
- SERVICES : réception SAF API35 intermittente sur la branche courante ;
  aucune autorisation de lancement d'export de production.
- La proposition CORE/SERVICES ADR-002 reste à approuver avant toute mise
  en production d'un port de mutation.

## Parcours de décision requis pour la fusion réelle

A. Approuver l'architecture de workspace commune et la stratégie de provenance
   (monorepo multi-modules **ou** fédération de dépôts avec manifeste locké).
B. Requalifier les têtes SHA et licences, versions Gradle/Kotlin/Java et minSdk.
C. Construire un **assemblage en laboratoire**, uniquement sur branche,
   avec scripts reproductibles et un module de démonstration sans données privées.
D. Vérifier l'autonomie de chaque module et les contrats CORE↔NEXUS/SERVICES,
   CORE↔LLM/VOICE et INTERFACE↔CORE en OFF par défaut.
E. Tester migrations sur copies, hors ligne, annulation, permissions, FTS5,
   mémoire/thermique sur émulateur puis appareil accepté.
F. Obtenir une approbation distincte avant toute fusion main, installation,
   activation des écritures ou migration personnelle.

## Livrables de U02

- `workspace/modular-workspace.proposed.json` : photo datée de 8 références
  et liens proposés. Les SHA doivent être revalidés pour toute réception ultérieure.
- `workspace/check_plan.py` : garde de structure (pas un fetch GitHub).
- `workspace/tests/test_workspace.py` : refus des faux GO, des dépendances
  cycliques, de la promotion de main et des commits non complets.
- `.github/workflows/uni-08-u02.yml` : qualification CI du seul plan.

Exécuter `python3 workspace/check_plan.py workspace/modular-workspace.proposed.json`
puis `python3 -m unittest discover -s workspace/tests -v`.
Le verdict doit rester `REVIEW_ONLY`, jamais `READY`.

## Règle de retour arrière

Revenir à la branche parente U01, ou supprimer la branche brouillon U02.
Aucun fichier des huit dépôts d'origine, historique, dépendance, licence,
source privée, APK et données utilisateur n'a été copié, remplacé ou effacé.

### Décision demandée (non présumée)

**Valider ou refuser l'orientation : projet unique, modules indépendants,
puis monorepo modulaire progressif après qualifications.**

Cette décision ne vaut PAS permission de fusionner dans main.
