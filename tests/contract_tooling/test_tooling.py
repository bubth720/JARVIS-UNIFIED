import copy
import tempfile
import unittest
from pathlib import Path

from tooling.contracts.manifest import ContractSchemaLoader, SchemaError, strict_json, canonical, make_manifest
from tooling.contracts.generator import DeterministicDtoGenerator
from tooling.contracts.compatibility import ContractCompatibilityChecker

ROOT = Path(__file__).resolve().parents[2]


class ContractToolingTest(unittest.TestCase):
    def setUp(self):
        self.schemas = ContractSchemaLoader(ROOT / "contracts/v1").load()

    def test_repeated_generation_has_identical_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a", Path(directory) / "b"
            generator = DeterministicDtoGenerator()
            generator.generate(self.schemas, a)
            generator.generate(self.schemas, b)
            snapshot = lambda p: {str(f.relative_to(p)): f.read_bytes() for f in p.rglob("*") if f.is_file()}
            self.assertEqual(snapshot(a), snapshot(b))
            self.assertEqual(len(snapshot(a)), 12)

    def test_checked_in_sources_are_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            DeterministicDtoGenerator().generate(self.schemas, directory)
            for path in Path(directory).rglob("*"):
                if path.is_file():
                    self.assertEqual(path.read_bytes(), (ROOT / "contracts/generated" / path.relative_to(directory)).read_bytes())

    def test_exact_manifests_compatible(self):
        manifest = make_manifest(self.schemas)
        self.assertEqual(ContractCompatibilityChecker.compare(manifest, manifest)["status"], "COMPATIBLE")

    def test_closed_schema_addition_is_incompatible(self):
        changed = copy.deepcopy(self.schemas)
        changed["health-status"]["properties"]["extra"] = {"type": "string"}
        result = ContractCompatibilityChecker.compare(make_manifest(self.schemas), make_manifest(changed))
        self.assertEqual(result["status"], "INCOMPATIBLE")
        self.assertIn("health-status", result["reasons"][0])

    def test_digest_tampering_unknown(self):
        left = make_manifest(self.schemas)
        right = copy.deepcopy(left)
        right["contracts"]["health-status"]["sha256"] = "0" * 64
        self.assertEqual(ContractCompatibilityChecker.compare(left, right)["status"], "UNKNOWN")

    def test_unknown_generator_version_unknown(self):
        left = make_manifest(self.schemas)
        right = copy.deepcopy(left)
        right["generator"] = "jarvis.dto/999"
        self.assertEqual(ContractCompatibilityChecker.compare(left, right)["status"], "UNKNOWN")

    def test_duplicate_fields_and_nonfinite_rejected(self):
        for text in ('{"a":1,"a":2}', '{"nested":{"a":1,"a":2}}', 'NaN', 'Infinity'):
            with self.assertRaises(SchemaError):
                strict_json(text)

    def test_invalid_unicode_rejected(self):
        with self.assertRaises(SchemaError):
            strict_json('"\\ud800"')
        self.assertEqual(strict_json('"\\ud83d\\ude00"'), "😀")

    def test_unknown_schema_keyword_type_and_format_rejected(self):
        for spec in ({"type": "byte"}, {"type": "string", "format": "url"}, {"$ref": "https://invalid"}):
            with self.assertRaises(ValueError):
                ContractSchemaLoader.check(spec)

    def test_unknown_required_field_rejected(self):
        with self.assertRaises(SchemaError):
            ContractSchemaLoader.check({"type": "object", "properties": {}, "required": ["missing"]})

    def test_canonical_unicode_and_numbers(self):
        self.assertEqual(canonical({"😀": 1, "z": "é", "\ue000": True}), '{"z":"é","\ue000":true,"😀":1}'.encode())


if __name__ == "__main__":
    unittest.main()
