"""python3 -m tooling.contracts.cli: offline, no remote mutations."""
import argparse
import json
from pathlib import Path
from .manifest import ContractSchemaLoader, strict_json, SchemaError
from .generator import DeterministicDtoGenerator
from .compatibility import ContractCompatibilityChecker


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate")
    generate.add_argument("--schemas", default="contracts/v1")
    generate.add_argument("--output", default="contracts/generated")
    compare = commands.add_parser("verify-contract")
    compare.add_argument("left")
    compare.add_argument("right")
    args = parser.parse_args(argv)
    try:
        if args.command == "generate":
            schemas = ContractSchemaLoader(args.schemas).load()
            DeterministicDtoGenerator().generate(schemas, args.output)
            print(json.dumps({"contracts": len(schemas), "output": args.output}))
            return 0
        result = ContractCompatibilityChecker.compare(*(strict_json(Path(p).read_text(encoding="utf-8")) for p in (args.left, args.right)))
        print(json.dumps(result))
        return {"COMPATIBLE": 0, "INCOMPATIBLE": 2, "UNKNOWN": 3}[result["status"]]
    except (SchemaError, OSError, ValueError) as exc:
        print(json.dumps({"status": "UNKNOWN", "reasons": [str(exc)]}))
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
