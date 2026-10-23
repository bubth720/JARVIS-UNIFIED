# Registre exécutable de campagne

Python standard, hors ligne. Aucune invocation Codex, aucun fetch, changement de
checkout, lancement de tests/patch, push ou merge par cet outil.

```sh
python3 -m tooling.campaign.cli list-ready
python3 -m tooling.campaign.cli list-blocked
python3 -m tooling.campaign.cli explain-mission --mission CORE-03
python3 -m tooling.campaign.cli export-wave --wave 0
python3 -m tooling.campaign.cli report --markdown
python3 -m unittest discover -s tooling/campaign/tests -v
```

Sans preuves fournies, les31missions sont PREPARED : seule la vague des huit
fondations est prête. Le fichier central historique `MISSIONS.json` n'est jamais
modifié pour prétendre que le code a été exécuté. Les numéros de vague proposés
ne remplacent pas les dépendances réelles. UI-01 est P1 dans le manifeste mais P0
dans sa fiche : l'ordre du manifeste est retenu, la dépendance CORE-02 conservée.

`MissionStatusMachine` fournit les transitions PREPARED→ASSIGNED→IN_PROGRESS→
DELIVERED, ou BLOCKED puis réattribution explicite. L'appelant persiste les
`records` dans son fichier local choisi ; les blocages/décisions manuels sont
conservés. Affecter deux missions au même dépôt est refusé, même si leurs fichiers
annoncés sont différents ; cela protège CORE/IDENTITY/MEMORY et UI/AVATAR.
Un propriétaire ne peut être actif dans deux missions simultanément.

Pour vérifier des livraisons, fournir `--state fichier.json` (objet mission→
record) et `--repository-paths chemins.json` (nom GitHub exact→checkout local).
Ces chemins sont de la configuration locale, pas des secrets à versionner.
Exemple de record :

```json
{"UNI-01":{"status":"DELIVERED","evidence":{
  "commit":"<SHA complet du commit contenant rapport et reçu>",
  "report":"docs/intensive-2026-10-22/REPORT-UNI-01.md",
  "report_sha256":"<SHA256 des octets du rapport>",
  "receipt":"docs/intensive-2026-10-22/RECEIPT-UNI-01.json",
  "receipt_sha256":"<SHA256 des octets du reçu>"
}}}
```

Le reçu versionné comporte `format:jarvis.campaign-validation/1`, `mission`,
`base_commit` (vraie base complète, jamais une approximation), `capabilities`
(liste non vide), `qualification:software_tested` et `checks`. Chaque check porte
`command` (tableau de chaînes), `exit_code:0`, `passed` strictement positif,
`failed:0` et `skipped:0`. Les autres validations non exécutées/sautées et les
limites doivent rester explicites dans le rapport ; un sous-ensemble réussi
n'autorise pas à annoncer toute la mission qualifiée. Une fonctionnalité dont
une dépendance nécessaire manque reste BLOCKED.

La vérification lit les objets Git : SHA, contenu exact des rapports/reçus,
empreintes, filiation depuis la référence figée, commits dépendants du même dépôt
dans l'ascendance. Elle accepte le parent technique d'une branche de planning
uniquement si le diff vérifié ajoute exclusivement les fiches de campagne.
Les bases dérivées de missions précédentes doivent conserver cette ascendance.
Un dépôt inaccessible, une preuve absente/corrompue ou un résultat échoué/non
exécuté est bloquant ; aucun résultat n'est inventé depuis une conversation.

Limite de confiance : un reçu reste une déclaration de l'auteur adossée à du Git
vérifiable, pas une signature matérielle ou une reproduction des tests. Cet
outil ne qualifie ni l'authenticité du processus natif, ni Android physique, ni
la publication distante. Ces preuves se vérifient séparément. Les catégories
sensibles de `OwnershipPolicy` exigent toujours une autorisation distincte ;
leur présence dans un plan ne donne aucun droit d'exécution.

Pour réutiliser les rapports anciens sans réécrire leurs branches, une preuve peut
ajouter `receipt_origin` avec `repository:bubth720/JARVIS-UNIFIED` et un `commit`
complet. Le reçu normalisé, stocké dans ce commit central, doit lier exactement
`validated_repository`, `validated_commit` et `source_report_sha256` au module
et rapport d'origine ; ses propres octets sont également vérifiés par SHA-256.
L'ascendance du commit central est contrôlée. Aucun autre dépôt de reçus n'est
accepté. Les commandes/comptes sont transcrits des preuves Git historiques avec
leur provenance explicite, jamais annoncés comme des tests rejoués maintenant.
Une validation Android restée en attente dans le rapport demeure en attente.
