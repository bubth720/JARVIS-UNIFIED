#!/usr/bin/env python3
"""Generates REGISTRE-ANOMALIES.md from registre.json (single source)."""
import json, pathlib
here = pathlib.Path(__file__).parent; d = json.loads((here / 'registre.json').read_text())
L = ["# Registre central des anomalies — JARVIS (AUDIT-GLOBAL-01)", "", f"Source : `registre.json` (ce fichier est généré par `render_registre.py`). Mise à jour : {d['updated']}.", "",
     "Natures : **DEFAUT_CONFIRME** (prouvé), **RISQUE_THEORIQUE** (non observé), **FONCTION_ABSENTE**, **LIMITATION_ENVIRONNEMENT**, **LIMITATION_MODELE**.", "",
     "| ID | Module | Nature | Gravité | Statut | Symptôme | Preuve | Correction proposée |", "|---|---|---|---|---|---|---|---|"]
L += [f"| {i['id']} | {i['module']} | {i['nature']} | {i['gravite']} | {i['statut']} | {i['symptome']} | {i['preuve']} | {i['correction']} |" for i in d['items']]
L += ["", "## Détail", ""]
for i in d['items']:
    L += [f"### {i['id']} — {i['module']}", ""] + [f"- **{lab}** : {i[k]}" for k, lab in [("files", "Fichiers"), ("ref", "Branche / commit"), ("reproduction", "Reproduction"), ("attendu", "Attendu"), ("obtenu", "Obtenu"), ("cause", "Cause"), ("dependances", "Dépendances")]] + [""]
(here / 'REGISTRE-ANOMALIES.md').write_text("\n".join(L) + "\n")
