"""Generate immutable typed Java DTOs and Kotlin facades without changing v1."""
import json
import re
from pathlib import Path
from .manifest import canonical, make_manifest, SchemaError


def pascal(value):
    return "".join(part.title() for part in re.split(r"[_-]", value))


def base_schema(schema):
    if "oneOf" in schema and "type" not in schema:
        variants = [x for x in schema["oneOf"] if x.get("type") != "null"]
        if len(variants) != 1:
            raise SchemaError("No deterministic DTO type for union")
        return variants[0]
    if "type" not in schema and "const" in schema:
        value = schema["const"]
        kind = "string" if isinstance(value, str) else "boolean" if type(value) is bool else "integer" if type(value) is int else None
        if kind is None:
            raise SchemaError("Unsupported constant type")
        return {**schema, "type": kind}
    return schema


class DeterministicDtoGenerator:
    def generate(self, schemas, destination):
        destination = Path(destination)
        java = destination / "java" / "org" / "jarvis" / "contracts" / "v1"
        kotlin = destination / "kotlin" / "org" / "jarvis" / "contracts" / "v1"
        java.mkdir(parents=True, exist_ok=True)
        kotlin.mkdir(parents=True, exist_ok=True)
        runtime = Path(__file__).parent / "runtime" / "ContractSupport.java"
        (java / runtime.name).write_bytes(runtime.read_bytes())
        for name, schema in sorted(schemas.items()):
            class_name = pascal(name)
            nested = []

            def type_and_read(spec, path, expression):
                spec = base_schema(spec)
                if "enum" in spec:
                    enum_name = path + "Value"
                    values = spec["enum"]
                    if not all(isinstance(x, str) for x in values):
                        raise SchemaError("Unsupported enum")
                    entries = [re.sub("[^A-Za-z0-9_]", "_", x).upper() for x in values]
                    if len(set(entries)) != len(entries):
                        raise SchemaError("Ambiguous enum identifier")
                    declaration = ", ".join(e + "(" + json.dumps(v) + ")" for e, v in zip(entries, values))
                    nested.append("public enum " + enum_name + " { " + declaration + ";\n"
                                  "public final String wire; " + enum_name + "(String wire) { this.wire=wire; }\n"
                                  "static " + enum_name + " read(Object value) { if(value==null)return null; for(" + enum_name +
                                  " x:values())if(x.wire.equals(value))return x; throw new IllegalArgumentException(\"enum\"); } }")
                    return enum_name, enum_name + ".read(" + expression + ")"
                kind = spec.get("type")
                if kind == "object":
                    child = path + "Object"
                    nested.append(object_class(child, spec))
                    return child, expression + "==null?null:new " + child + "(ContractSupport.object(" + expression + "))"
                if kind == "array":
                    item_type, item_read = type_and_read(spec["items"], path + "Item", "item")
                    return "List<" + item_type + ">", "ContractSupport.mapList(" + expression + ", item -> " + item_read + ")"
                types = {"string": "String", "integer": "Long", "boolean": "Boolean"}
                if kind not in types:
                    raise SchemaError("Unsupported DTO field type")
                return types[kind], "(" + types[kind] + ")" + expression

            def object_class(class_id, spec, root=False):
                methods = []
                for field, child in sorted(spec["properties"].items()):
                    field_type, read = type_and_read(child, pascal(field) if root else class_id + pascal(field),
                                                     "values.get(" + json.dumps(field) + ")")
                    methods.append("public " + field_type + " get" + pascal(field) + "() { return " + read + "; }")
                head = "public final class " if root else "public static final class "
                return head + class_id + " {\nprivate final Map<String,Object> values;\n" + \
                    "private " + class_id + "(Map<String,Object> values) { this.values=ContractSupport.freezeObject(values); }\n" + \
                    "public Map<String,Object> toMap() { return values; }\npublic String toJson() { return ContractSupport.json(values); }\n" + \
                    "\n".join(methods) + ("\n}" if not root else "")

            source = object_class(class_name, schema, root=True)
            literal = json.dumps(canonical(schema).decode("utf-8"), ensure_ascii=True)
            source += "\nprivate static final Map<String,Object> SCHEMA=ContractSupport.object(ContractSupport.parse(" + literal + "));\n"
            source += "public static " + class_name + " fromMap(Map<String,Object> value) { Map<String,Object> copy=ContractSupport.freezeObject(value); ContractSupport.validate(" + json.dumps(name) + ", copy, SCHEMA); return new " + class_name + "(copy); }\n"
            source += "public static " + class_name + " parse(String json) { return fromMap(ContractSupport.object(ContractSupport.parse(json))); }\n"
            source += "public static " + class_name + " parseUtf8(byte[] json) { return fromMap(ContractSupport.object(ContractSupport.parseUtf8(json))); }\n"
            source += "\n".join(nested) + "\n}\n"
            (java / (class_name + ".java")).write_text("// Generated by jarvis.dto/1. Do not edit.\npackage org.jarvis.contracts.v1;\nimport java.util.*;\n" + source, encoding="utf-8")
            props = []
            # Java getters preserve typed nested DTOs/enums. Kotlin delegates immutable state.
            for field in sorted(schema["properties"]):
                props.append("    val " + field + " get() = delegate.get" + pascal(field) + "()")
            kt = "// Generated by jarvis.dto/1. Do not edit.\npackage org.jarvis.contracts.v1\n\n"
            kt += "class " + class_name + "Dto private constructor(private val delegate: " + class_name + ") {\n"
            kt += "\n".join(props) + "\n    fun toJson(): String = delegate.toJson()\n"
            kt += "    fun toMap(): Map<String, Any?> = delegate.toMap()\n    companion object {\n"
            kt += "        fun parse(json: String): " + class_name + "Dto = " + class_name + "Dto(" + class_name + ".parse(json))\n"
            kt += "        fun parseUtf8(json: ByteArray): " + class_name + "Dto = " + class_name + "Dto(" + class_name + ".parseUtf8(json))\n    }\n}\n"
            (kotlin / (class_name + "Dto.kt")).write_text(kt, encoding="utf-8")
        (destination / "manifest.json").write_bytes(canonical(make_manifest(schemas)) + b"\n")
