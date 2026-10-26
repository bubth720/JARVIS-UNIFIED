# FUSION-02 — livraison propriétaire UNIFIED

Mission : https://github.com/bubth720/JARVIS-UNIFIED/issues/5

- [Rapport de livraison](REPORT.md), [provenance](PROVENANCE.json), [validation](VALIDATION.json)
- [Verrou v2](../../integration-lock-v2.json), [matrice générée](RELEASE_MATRIX.md),
  [diff FUSION-01 → 02](COMPARISON.json), [gates](ASSESSMENT.json)
- [Contrats et fence proposés](CONTRACTS.md), [runbooks et rollback](RUNBOOK.md)
- Audits [CORE/LLM](AUDIT-CORE-LLM.md), [NEXUS/SERVICES](AUDIT-NEXUS-SERVICES.md),
  [INTERFACE/VOICE/EVOLUTION](AUDIT-INTERFACE-VOICE-EVOLUTION.md)
- [Diagnostic CI et remédiation](CI_DIAGNOSIS.md), [texte PR brouillon](PR_DRAFT.md)

Code : extensions de `tooling/integration`, pas un second registre/orchestrateur.
Les lecteurs FUSION-01 sont réutilisés pour l'admission SHA/parents/fichiers et les
contrats sont proposés dans ce dossier, **sans mutation de contracts/v1**.

```sh
python3 -m tooling.integration.cli_v2 validate
python3 -m tooling.integration.cli_v2 validate --repositories /chemin/local/map.json
python3 -m tooling.integration.cli_v2 compare
python3 -m tooling.integration.cli_v2 assess
python3 -m tooling.integration.cli_v2 report
python3 -m tooling.integration.check_v2_contracts
python3 -m tooling.integration.ci --output /tmp/fusion02-checks
```

Sans map locale des huit dépôts, la CLI annonce `structure_only` : elle ne prétend
pas relire GitHub ou les sources. Avec cette map, parents et octets Git sont
vérifiés, sans fetch/checkout ni exécution du code inspecté. Les répertoires bare
d'audit peuvent être utilisés ; aucun chemin privé ne doit être publié.
Le lanceur CI utilise des commandes fixes, aucun shell/commande arbitraire. Il
préserve stdout/stderr et compte les résultats unittest, refuse zéro test, échec,
saut ou suite historique amputée. Le workflow indépendant est du JSON valide YAML1.2,
analysable par Python standard, avec Python3.12.12, artefacts même après échec,
contenu en lecture seule, déclenchement push/PR/manual sur la branche de mission.
L'ancien workflow reste présent et sa syntaxe est corrigée ; aucun job retiré.

Le verdict porte seulement sur les preuves déclarées et liées aux octets Git,
pas sur l'authenticité physique ou l'autorisation de runtime. Un auteur malveillant
peut mentir dans un rapport : revue humaine/logs CI/appareil restent nécessaires.
Les transitions de reçus sont des vérifications de contrat hors ligne, **pas une
implémentation concurrente de Guard/ApprovalGate ni de authorizeAtCommit**.
