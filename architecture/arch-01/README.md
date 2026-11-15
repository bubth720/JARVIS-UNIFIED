# ARCH-01 — Architecture PC + Android et préparation des futurs moteurs IA

| Livrable | Fichier |
|---|---|
| Document d'architecture PC + Android | [ARCHITECTURE-PC-ANDROID.md](ARCHITECTURE-PC-ANDROID.md) |
| Contrat technique des futurs moteurs IA | [MODEL-BACKEND-CONTRACT.md](MODEL-BACKEND-CONTRACT.md) |
| Matrice de compatibilité des modules | [COMPATIBILITY-MATRIX.md](COMPATIBILITY-MATRIX.md) |
| Incompatibilités, risques, adaptations | [RISKS-AND-ADAPTATIONS.md](RISKS-AND-ADAPTATIONS.md) |
| Référence exécutable du contrat | `tooling/arch01/` (`backend.py`, `registry.py`, `router.py`, `legacy.py`, `link.py`, `memory_sync.py`) |
| Empreinte figée du contrat CORE | `tooling/arch01/core_contract_5da9838.json` (extraite par `git show`) |
| Tests de contrat (moteurs simulés) | `tooling/arch01/tests/` |

Exécution :

```sh
python3 -m unittest discover -s tooling/arch01/tests -v
ARCH01_CORE_REPO=/chemin/vers/JAVIS-Local-v2 python3 -m unittest discover -s tooling/arch01/tests -v   # + vérification des blobs CORE
```

Ce que démontrent les tests : la **logique** des contrats (routage, registre, liaison, mémoire, adaptateur du moteur actuel) avec des moteurs **simulés**. Ils ne démontrent ni un moteur PC réel, ni une liaison réseau, ni une performance.
