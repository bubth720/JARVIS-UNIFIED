"""Strict JSON, schema admission and content-addressed manifests."""
import hashlib
import json
from pathlib import Path

from scripts.contracts import ContractError, KEYWORDS, validate_schema


class SchemaError(ContractError):
    pass


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise SchemaError("Duplicate JSON field: " + key)
        result[key] = value
    return result


def strict_json(text):
    try:
        value = json.loads(text, object_pairs_hook=_pairs,
                           parse_constant=lambda _: (_ for _ in ()).throw(SchemaError("Non-finite JSON")))
        canonical(value)  # reject invalid Unicode, including unpaired surrogates
        return value
    except (ValueError, UnicodeError) as exc:
        raise SchemaError(str(exc)) from exc


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


class ContractSchemaLoader:
    """Only the documented frozen subset is admitted; no remote references."""
    def __init__(self, directory):
        self.directory = Path(directory)

    def load(self):
        result = {}
        for path in sorted(self.directory.glob("*.schema.json")):
            schema = strict_json(path.read_text(encoding="utf-8"))
            self.check(schema)
            if schema.get("title") != path.name.removesuffix(".schema.json"):
                raise SchemaError("Schema name mismatch: " + path.name)
            result[schema["title"]] = schema
        if not result:
            raise SchemaError("No schemas")
        return result

    @classmethod
    def check(cls, schema):
        validate_schema(schema)
        if "type" in schema and schema["type"] not in {"object", "array", "string", "integer", "boolean", "null"}:
            raise SchemaError("Unsupported schema type")
        if "properties" in schema:
            properties = schema["properties"]
            if not isinstance(properties, dict) or not set(schema.get("required", [])) <= properties.keys():
                raise SchemaError("Invalid required fields")
            for key, child in properties.items():
                if not key.isascii() or not key.replace("_", "").isalnum() or not key[0].isalpha():
                    raise SchemaError("Unsafe generated identifier")
                cls.check(child)
        if "items" in schema:
            cls.check(schema["items"])
        for keyword in ("oneOf", "allOf"):
            for child in schema.get(keyword, []):
                cls.check(child)


FrozenContractReader = ContractSchemaLoader


def make_manifest(schemas):
    payload = {"format": "jarvis.contract-manifest/1", "generator": "jarvis.dto/1",
               "contracts": {name: {"schema": schema, "sha256": digest(schema)}
                             for name, schema in sorted(schemas.items())}}
    return {**payload, "sha256": digest(payload)}


def verify_manifest(value):
    if not isinstance(value, dict) or set(value) != {"format", "generator", "contracts", "sha256"}:
        raise SchemaError("Invalid manifest fields")
    if value["format"] != "jarvis.contract-manifest/1" or value["generator"] != "jarvis.dto/1":
        raise SchemaError("Unknown manifest version")
    if digest({k: v for k, v in value.items() if k != "sha256"}) != value["sha256"]:
        raise SchemaError("Manifest digest mismatch")
    if not isinstance(value["contracts"], dict) or not value["contracts"]:
        raise SchemaError("Empty contract manifest")
    for name, entry in value["contracts"].items():
        if set(entry) != {"schema", "sha256"} or digest(entry["schema"]) != entry["sha256"]:
            raise SchemaError("Schema digest mismatch")
        ContractSchemaLoader.check(entry["schema"])
        if entry["schema"].get("title") != name:
            raise SchemaError("Contract title mismatch")
    return value
