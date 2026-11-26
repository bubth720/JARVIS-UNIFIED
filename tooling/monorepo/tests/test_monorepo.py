#!/usr/bin/env python3
"""Offline tests: source lock invariants and safe assembly from synthetic Git repos."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage_local_sources import assemble, safe_relative
from validate_sources import DEFAULT_MANIFEST, load_and_validate


def git(cwd, *args):
    return subprocess.check_output(["git", "-C", str(cwd), *args], stderr=subprocess.DEVNULL).decode().strip()


class MonorepoTest(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.TemporaryDirectory()
        self.addCleanup(self.base.cleanup)
        self.root = Path(self.base.name)
        self.manifest = copy.deepcopy(load_and_validate(DEFAULT_MANIFEST))
        self.sources = self.root / "sources"
        self.sources.mkdir()
        for module in self.manifest["modules"]:
            path = self.sources / module["id"]
            path.mkdir()
            git(path, "init", "-q")
            git(path, "config", "user.email", "test@example.invalid")
            git(path, "config", "user.name", "JARVIS Test")
            (path / "src").mkdir()
            (path / "src" / "hello.txt").write_text("source:" + module["id"])
            (path / ".github" / "workflows").mkdir(parents=True)
            (path / ".github" / "workflows" / "old.yml").write_text("disabled")
            (path / "models").mkdir()
            (path / "models" / "weights.gguf").write_bytes(b"synthetic")
            if module["id"] == "voice":
                archive = path / "deliveries" / "mission005j"
                archive.mkdir(parents=True)
                (archive / "005j-experimental-apk.zip").write_bytes(b"historic fixture")
            if module["id"] == "interface":
                captures = path / "labs" / "v3" / "captures"
                captures.mkdir(parents=True)
                (captures / "old-demo.jpg").write_bytes(b"historic capture")
            git(path, "add", ".")
            git(path, "commit", "-qm", "test fixture")
            module["source_sha"] = git(path, "rev-parse", "HEAD")
        self.manifest_file = self.root / "fixture-lock.json"
        self.write_manifest()

    def write_manifest(self):
        self.manifest_file.write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_manifest_has_all_seven_modules(self):
        result = load_and_validate(self.manifest_file)
        self.assertEqual(len(result["modules"]), 7)

    def test_sha_mismatch_is_rejected(self):
        self.manifest["modules"][0]["source_sha"] = "wrong"
        self.write_manifest()
        with self.assertRaises(ValueError):
            load_and_validate(self.manifest_file)

    def test_safety_policy_cannot_be_disabled(self):
        self.manifest["policy"]["android_offline"] = False
        self.write_manifest()
        with self.assertRaises(ValueError):
            load_and_validate(self.manifest_file)

    def test_path_traversal_is_rejected(self):
        for value in ("../escape", "/absolute", "foo/../../escape", "foo" + chr(92) + "bar"):
            with self.assertRaises(ValueError):
                safe_relative(value)

    def test_stage_from_local_git_archives(self):
        destination = self.root / "snapshot"
        result = assemble(self.manifest_file, self.sources, destination)
        self.assertEqual(len(result), 7)
        for module in self.manifest["modules"]:
            target = destination / module["target"]
            self.assertTrue((target / "src" / "hello.txt").exists())
            self.assertFalse((target / ".git").exists())
            self.assertFalse((target / ".github").exists())
            self.assertFalse((target / "models" / "weights.gguf").exists())
            if module["id"] == "voice":
                self.assertFalse((target / "deliveries").exists())
            if module["id"] == "interface":
                self.assertFalse((target / "labs" / "v3" / "captures").exists())
        report = json.loads((destination / "SOURCE-SNAPSHOT-REPORT.json").read_text())
        self.assertTrue(report["source_only"])
        self.assertEqual(len(report["modules"]), 7)

    def test_no_overwrite_of_existing_directory(self):
        destination = self.root / "snapshot"
        destination.mkdir()
        sentinel = destination / "keep.txt"
        sentinel.write_text("untouched")
        with self.assertRaises(ValueError):
            assemble(self.manifest_file, self.sources, destination)
        self.assertEqual(sentinel.read_text(), "untouched")

    def test_missing_git_object_does_not_leave_output(self):
        self.manifest["modules"][2]["source_sha"] = "0" * 40
        self.write_manifest()
        destination = self.root / "snapshot"
        with self.assertRaises(ValueError):
            assemble(self.manifest_file, self.sources, destination)
        self.assertFalse(destination.exists())

    def test_symlink_in_archive_is_refused(self):
        source = self.sources / "core"
        (source / "bad-link").symlink_to("/tmp")
        git(source, "add", "bad-link")
        git(source, "commit", "-qm", "introduce symlink")
        self.manifest["modules"][0]["source_sha"] = git(source, "rev-parse", "HEAD")
        self.write_manifest()
        destination = self.root / "snapshot"
        with self.assertRaises(ValueError):
            assemble(self.manifest_file, self.sources, destination)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
