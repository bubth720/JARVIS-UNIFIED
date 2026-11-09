# LAB-02 — Diagnostic priorisé, en lecture seule

**Statut :** fonctionnalité candidate sur branche séparée. Ce document ne constitue ni qualification Android ni réception V1.

## But
Transformer le reçu d'une campagne LAB-01 en `TRIAGE.json` et `TRIAGE.md`, avec causes observées, priorité et prochaine action. Le programme ne compile, n'installe, ne corrige, ne relance et n'active rien.

## Commande depuis le dépôt UNIFIED
```bash
python3 tooling/integration-lab/triage.py \
  --receipt tooling/integration-lab/reports/CI-RECEIPT.json \
  --output /tmp/jarvis-lab02-triage
```

Pour vérifier les octets de logs réels déjà disponibles, ajouter `--evidence-root <répertoire de la campagne>`. Sans cette option, l'outil indique `NOT_CHECKED`, et jamais `VERIFIED`. Les empreintes de logs manquants restent `UNAVAILABLE`, un digest incorrect `MISMATCH`.

## Résultat attendu avec le reçu LAB-01 du 9 novembre
Le programme doit classer séparément les deux gardes LLM en échec, le test VOICE ignoré et le défaut de qualification Android. Il doit aussi rappeler qu'aucune connexion runtime intermodule n'est qualifiée.

**Ces résultats historiques ne sont pas de nouveaux tests.** L'exécution de la CLI prouve uniquement la génération et l'analyse du rapport depuis le reçu connu.

## Tests
```bash
python3 -m unittest discover -s tooling/integration-lab/tests -p 'test_*.py' -v
```
Les 12 nouveaux tests couvrent entrées invalides, doublons, tri, absence de fausse autorisation, déterminisme, création de fichiers, injection Markdown, liens symboliques, fuite de chemin, vérification SHA-256 et tampering.

## Règles
- Toujours préserver le statut original `FAIL/BLOCKED/NOT_RUN`; un rapport peut être généré sans que la campagne soit verte.
- Sorties dans un **nouveau** dossier vide ; ne jamais écraser les preuves.
- Les journaux sont des données non fiables, jamais des commandes exécutables.
- Pas de modification de CORE, LLM, VOICE, NEXUS, INTERFACE ou du registre de gates.
- Pas de fusion, déploiement, clé, modèle ou test physique sans accord.
- Les priorités sont des recommandations opérationnelles, **pas des assertions de cause prouvée**.

## Suite
Après réception CI de cette branche, compléter le catalogue de règles seulement à partir de nouvelles preuves et rattacher les rapports triés aux campagnes pertinentes. Une correction des gardes LLM ou une intégration NEXUS/SERVICES reste une mission séparée.
