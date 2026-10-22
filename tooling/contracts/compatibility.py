"""Closed v1 schemas: no unnegotiated addition is compatible."""
from .manifest import verify_manifest, SchemaError


class ContractCompatibilityChecker:
    @staticmethod
    def compare(left, right):
        try:
            verify_manifest(left)
            verify_manifest(right)
        except (SchemaError, KeyError, TypeError) as exc:
            return {"status": "UNKNOWN", "reasons": [str(exc)]}
        changes = []
        for name in sorted(left["contracts"].keys() | right["contracts"].keys()):
            if left["contracts"].get(name) != right["contracts"].get(name):
                changes.append("Closed contract differs: " + name)
        return {"status": "INCOMPATIBLE" if changes else "COMPATIBLE", "reasons": changes}
