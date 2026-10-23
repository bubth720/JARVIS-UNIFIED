"""Read-only local reporting; never invokes Codex, a patch, push or merge."""
import argparse
import json
from pathlib import Path
from tooling.contracts.manifest import strict_json
from .manifest import CampaignManifestReader, CampaignError
from .dag import MissionDAGResolver
from .ownership import OwnershipConflictDetector, OwnershipPolicy
from .status import EvidenceGateEvaluator, MissionStatusMachine


class AssignmentPlanRenderer:
    @staticmethod
    def markdown(data):
        if not isinstance(data, dict) or "states" not in data:
            return "# Campagne JARVIS\n\n```json\n" + json.dumps(data, ensure_ascii=False, indent=2) + "\n```"
        safe = lambda text: str(text).replace("|", "\\|").replace("\n", " ")
        lines = ["# Campagne JARVIS — état local vérifié", "", "Prêtes : " + (", ".join(data["ready"]) or "aucune"),
                 "", "Livrées avec preuves vérifiables : " + (", ".join(data["delivered"]) or "aucune"), "",
                 "| Mission | État | Blocage |", "|---|---|---|"]
        for mission, state in data["states"].items():
            lines.append("| " + mission + " | " + state + " | " + safe("; ".join(data["blocked"].get(mission, []))) + " |")
        lines += ["", "## Décisions manuelles conservées", ""]
        for mission, decisions in data["manual_decisions"].items():
            lines.append("- " + mission + " : " + safe("; ".join(decisions)))
        if not data["manual_decisions"]:
            lines.append("Aucune décision enregistrée dans cette entrée locale.")
        lines += ["", "Les vagues sont un plan ; elles ne prouvent aucune intégration native ou physique."]
        return "\n".join(lines)


def report(manifest, state, repository_paths):
    machine = MissionStatusMachine(manifest, EvidenceGateEvaluator(manifest, repository_paths), state)
    delivered = machine.delivered()
    assignments = [{"mission": key, "owner": value.get("owner"), "branch": value.get("branch")}
                   for key, value in state.items() if value.get("status") in {"ASSIGNED", "IN_PROGRESS"}]
    OwnershipConflictDetector.check(manifest, assignments)
    occupied = {manifest.nodes[x["mission"]].repository for x in assignments}
    ready = []
    blocked = {}
    for node in manifest.nodes.values():
        status = machine.status(node.id)
        missing = sorted(set(node.dependencies) - delivered)
        reasons = ["Dependency not delivered: " + dep for dep in missing]
        if status == "BLOCKED":
            reasons.extend(state[node.id].get("blockers", []))
        if node.repository in occupied and status not in {"ASSIGNED", "IN_PROGRESS", "DELIVERED"}:
            reasons.append("Repository already owned")
        if status == "PREPARED" and not reasons:
            ready.append(node.id)
        elif reasons and status != "DELIVERED":
            blocked[node.id] = reasons
    return {"campaign": manifest.value["campaign"], "ready": ready, "blocked": blocked,
            "delivered": sorted(delivered), "waves": MissionDAGResolver(manifest).waves(),
            "states": {k: machine.status(k) for k in manifest.nodes},
            "manual_decisions": {k: v.get("decisions", []) for k, v in state.items() if v.get("decisions")},
            "shared_files": OwnershipPolicy.SHARED}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list-ready", "list-blocked", "explain-mission", "export-wave", "report"])
    parser.add_argument("--manifest", default="docs/intensive-2026-10-22/MISSIONS.json")
    parser.add_argument("--state", type=Path)
    parser.add_argument("--repository-paths", type=Path, help="JSON repository→local checkout; never fetched")
    parser.add_argument("--mission")
    parser.add_argument("--wave", type=int, default=0)
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = CampaignManifestReader.read(args.manifest)
        state = strict_json(args.state.read_text(encoding="utf-8")) if args.state else {}
        paths = strict_json(args.repository_paths.read_text(encoding="utf-8")) if args.repository_paths else {}
        data = report(manifest, state, paths)
        if args.command == "list-ready":
            data = data["ready"]
        elif args.command == "list-blocked":
            data = data["blocked"]
        elif args.command == "export-wave":
            if not 0 <= args.wave < len(data["waves"]):
                raise CampaignError("Unknown topological wave")
            data = {"planned": data["waves"][args.wave], "ready": [x for x in data["waves"][args.wave] if x in data["ready"]]}
        elif args.command == "explain-mission":
            if args.mission not in manifest.nodes:
                raise CampaignError("Unknown mission")
            node = manifest.nodes[args.mission]
            data = {"mission": node.id, "repository": node.repository, "status": data["states"][node.id],
                    "dependencies": node.dependencies, "blockers": data["blocked"].get(node.id, []),
                    "decisions": state.get(node.id, {}).get("decisions", []), "next_action": "Deliver prerequisites, then assign a single repository owner"}
        if args.markdown:
            print(AssignmentPlanRenderer.markdown(data))
        else:
            print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (CampaignError, OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
