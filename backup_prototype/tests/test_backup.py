"""Temporary synthetic datasets only; no real models, voices, data or secrets."""
import json
import errno
from unittest import mock
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import uuid
from backup_prototype import backup as b


class BackupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="jarvis-backup-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "synthetic"
        b.create_demo(self.source)
        self.archive = self.root / "demo.jvb"
        self.store = self.root / "restored"
        self.password = uuid.uuid4().hex + uuid.uuid4().hex
        self.before = self.tree(self.source)

    @staticmethod
    def tree(path):
        return {str(p.relative_to(path)): p.read_bytes() for p in path.rglob("*") if p.is_file()} if path.exists() else {}

    def export(self):
        return b.export_demo(self.source, self.archive, self.password)

    def active(self):
        return json.loads((self.store / "state.json").read_text())["active"]

    def generation(self):
        return self.store / "generations" / self.active()

    def edited_archive(self, edit):
        self.export()
        _, objects, _ = b.verify_archive(self.archive, self.password)
        doc = json.loads(b.pack(objects)); edit(doc)
        self.archive.write_bytes(b.seal(b.encoded(doc), self.password))

    def assert_rejected(self):
        with self.assertRaises((b.BackupError, sqlite3.Error, KeyError, TypeError, ValueError)):
            b.restore(self.archive, self.store, self.password)
        self.assertFalse(self.store.exists())
        self.assertEqual(self.before, self.tree(self.source))

    def test_encrypted_round_trip_source_unchanged(self):
        self.export()
        m, objects, _ = b.verify_archive(self.archive, self.password)
        for marker in [b"DEMO:", b"memories", b"jarvis-backup"]:
            self.assertNotIn(marker, self.archive.read_bytes())
        b.restore(self.archive, self.store, self.password)
        for path, data in objects.items():
            self.assertEqual(data, (self.generation() / "payload" / path).read_bytes())
        with sqlite3.connect(self.generation() / "payload/core/core.sqlite") as db:
            self.assertEqual(db.execute("SELECT id FROM messages ORDER BY id").fetchall(), [(11,), (12,)])
            self.assertEqual(db.execute("SELECT id FROM chunks").fetchall(), [(41,)])
            self.assertEqual(db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            self.assertEqual(db.execute("SELECT seq FROM sqlite_sequence WHERE name='memories'").fetchone()[0], 23)
        self.assertEqual(len(m["files"]), 6)
        self.assertEqual(self.before, self.tree(self.source))
        self.assertEqual(self.archive.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.store.stat().st_mode & 0o777, 0o700)

    def test_ciphertext_randomized(self):
        self.export(); second = self.root / "second.jvb"
        b.export_demo(self.source, second, self.password)
        self.assertNotEqual(self.archive.read_bytes(), second.read_bytes())

    def test_unconfirmed_memories_absent_including_free_pages(self):
        self.export(); _, objects, _ = b.verify_archive(self.archive, self.password)
        data = objects["core/core.sqlite"]
        self.assertNotIn("proposition en attente".encode(), data)
        self.assertNotIn("proposition refusée".encode(), data)
        with b._database(data) as db:
            self.assertEqual(db.execute("SELECT id FROM memories").fetchall(), [(21,)])
        self.assertEqual(self.before, self.tree(self.source))

    def test_memory_inactive_until_exact_local_confirmation(self):
        self.export(); b.restore(self.archive, self.store, self.password)
        review = json.loads((self.generation() / "memory-review.json").read_text())
        self.assertEqual(review["records"][0]["activation"], "pending-local-confirmation")
        digest = review["records"][0]["text_sha256"]
        b.restore(self.archive, self.store, self.password, replace=True, confirmations=["21:" + digest])
        review = json.loads((self.generation() / "memory-review.json").read_text())
        self.assertEqual(review["records"][0]["activation"], "confirmed-locally")

    def test_mismatched_confirmation_no_writes(self):
        self.export()
        with self.assertRaises(b.BackupError):
            b.restore(self.archive, self.store, self.password, confirmations=["21:" + "0" * 64])
        self.assertFalse(self.store.exists())

    def test_wrong_password_preserves_existing_store(self):
        self.export(); b.restore(self.archive, self.store, self.password)
        before = self.tree(self.store)
        with self.assertRaises(b.BackupError):
            b.restore(self.archive, self.store, uuid.uuid4().hex)
        self.assertEqual(before, self.tree(self.store))

    def test_tampered_header_and_ciphertext(self):
        self.export(); original = self.archive.read_bytes()
        for offset in [0, len(b.MAGIC), b.HEADER_SIZE - 1, b.HEADER_SIZE + 2, len(original) - 1]:
            with self.subTest(offset=offset):
                data = bytearray(original); data[offset] ^= 1
                self.archive.write_bytes(data); self.assert_rejected()

    def test_truncated_archive(self):
        self.export(); original = self.archive.read_bytes()
        for size in [0, 5, b.HEADER_SIZE, len(original) - 1]:
            with self.subTest(size=size):
                self.archive.write_bytes(original[:size]); self.assert_rejected()

    def test_bad_hash_with_valid_aead(self):
        self.edited_archive(lambda d: d["manifest"]["files"][0].update(sha256="0" * 64))
        self.assert_rejected()

    def test_future_format(self):
        self.edited_archive(lambda d: d["manifest"].update(version=2)); self.assert_rejected()

    def test_unknown_engine(self):
        self.edited_archive(lambda d: d["manifest"]["required_engines"][0].update(id="other")); self.assert_rejected()

    def test_incompatible_voice_pack(self):
        self.export(); _, objects, _ = b.verify_archive(self.archive, self.password)
        profile = json.loads(objects["voices/demo/profile.json"]); profile["pack_sha256"] = "0" * 64
        objects["voices/demo/profile.json"] = b.encoded(profile)
        with self.assertRaises(b.BackupError): b.pack(objects)

    def test_traversal_duplicate_unknown_paths(self):
        self.export(); original = self.archive.read_bytes()
        for path in ["../../escape", "/tmp/escape", "C:\\escape", "core/core.sqlite", "unknown.bin"]:
            with self.subTest(path=path):
                self.archive.write_bytes(original)
                _, objects, _ = b.verify_archive(self.archive, self.password)
                doc = json.loads(b.pack(objects)); doc["manifest"]["files"][-1]["path"] = path
                self.archive.write_bytes(b.seal(b.encoded(doc), self.password)); self.assert_rejected()

    def test_authenticated_malformed_metadata_refused(self):
        self.export(); original = self.archive.read_bytes()
        mutations = [lambda d: d.update(manifest=[]), lambda d: d.update(objects=[]),
                     lambda d: d["manifest"].update(archive_id="not-a-uuid"),
                     lambda d: d["manifest"].update(created_utc="yesterday"),
                     lambda d: d["manifest"]["files"][0].update(schema_version=True)]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                self.archive.write_bytes(original)
                _, objects, _ = b.verify_archive(self.archive, self.password)
                doc = json.loads(b.pack(objects)); mutate(doc)
                self.archive.write_bytes(b.seal(b.encoded(doc), self.password)); self.assert_rejected()

    def test_duplicate_json_keys(self):
        with self.assertRaises(b.BackupError): b.decoded(b'{"version":1,"version":2}')

    def test_oversized_object_and_envelope(self):
        self.edited_archive(lambda d: d["manifest"]["files"][0].update(size=b.MAX_FILE + 1)); self.assert_rejected()
        with self.assertRaises(b.BackupError): b.unseal(b"x" * (b.MAX_ENVELOPE + 1), self.password)

    def test_corrupt_and_future_sqlite(self):
        self.export(); _, objects, _ = b.verify_archive(self.archive, self.password)
        original = objects["core/core.sqlite"]; objects["core/core.sqlite"] = b"not a database"
        with self.assertRaises(b.BackupError): b.pack(objects)
        with b._database(original) as db:
            db.execute("PRAGMA user_version=3"); objects["core/core.sqlite"] = db.serialize()
        with self.assertRaises(b.BackupError): b.pack(objects)

    def test_existing_archive_never_overwritten(self):
        self.export(); original = self.archive.read_bytes()
        with self.assertRaises(b.BackupError): self.export()
        self.assertEqual(self.archive.read_bytes(), original)

    def test_idempotence_and_explicit_conflict(self):
        self.export(); first = b.restore(self.archive, self.store, self.password)
        second = b.restore(self.archive, self.store, self.password)
        self.assertEqual(first["generation"], second["generation"])
        self.assertEqual(second["status"], "already-restored")
        other = self.root / "other.jvb"; b.export_demo(self.source, other, self.password)
        before = self.tree(self.store)
        with self.assertRaises(b.BackupError): b.restore(other, self.store, self.password)
        self.assertEqual(before, self.tree(self.store))
        b.restore(other, self.store, self.password, replace=True)
        self.assertTrue((self.store / "generations" / first["generation"]).is_dir())

    def test_crashes_all_boundaries_and_recovery_in_fresh_interpreter(self):
        self.export()
        for phase in ["after_stage", "before_activate", "after_activate"]:
            with self.subTest(phase=phase):
                store = self.root / phase; first = b.restore(self.archive, store, self.password)
                old_directory = store / "generations" / first["generation"]; old = self.tree(old_directory)
                other = self.root / (phase + ".jvb"); b.export_demo(self.source, other, self.password)
                with self.assertRaises(b.SimulatedCrash):
                    b.restore(other, store, self.password, replace=True, fail_at=phase)
                if phase != "after_stage":
                    with self.assertRaises(b.BackupError): b.restore(other, store, self.password, replace=True)
                result = subprocess.run([sys.executable, "-m", "backup_prototype.backup", "recover", str(store)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual(json.loads((store / "state.json").read_text())["active"], first["generation"])
                self.assertEqual(old, self.tree(old_directory)); self.assertEqual(self.before, self.tree(self.source))
                b.restore(other, store, self.password, replace=True)
                self.assertNotEqual(json.loads((store / "state.json").read_text())["active"], first["generation"])

    def test_abrupt_process_exit_after_activation(self):
        self.export(); first = b.restore(self.archive, self.store, self.password)
        other = self.root / "other.jvb"; b.export_demo(self.source, other, self.password)
        code = '''import os,sys
from pathlib import Path
from backup_prototype import backup as b
try:
 b.restore(Path(sys.argv[1]),Path(sys.argv[2]),sys.stdin.read(),replace=True,fail_at="after_activate")
except b.SimulatedCrash:
 os._exit(73)
'''
        result = subprocess.run([sys.executable, "-c", code, str(other), str(self.store)], input=self.password, text=True)
        self.assertEqual(result.returncode, 73); self.assertNotEqual(self.active(), first["generation"])
        b.recover(self.store); self.assertEqual(self.active(), first["generation"])
        self.assertEqual(self.before, self.tree(self.source))

    def test_first_restore_crash_back_to_no_active(self):
        self.export()
        with self.assertRaises(b.SimulatedCrash): b.restore(self.archive, self.store, self.password, fail_at="after_activate")
        b.recover(self.store); self.assertFalse((self.store / "state.json").exists())
        self.assertTrue(any((self.store / "generations").iterdir()))
        b.restore(self.archive, self.store, self.password); b.validate_generation(self.store, self.active())

    def test_corrupt_active_generation_not_silently_replaced(self):
        self.export(); b.restore(self.archive, self.store, self.password)
        (self.generation() / "payload/core/preferences.json").write_bytes(b"corrupt")
        before = (self.store / "state.json").read_bytes()
        with self.assertRaises(b.BackupError): b.restore(self.archive, self.store, self.password, replace=True)
        self.assertEqual(before, (self.store / "state.json").read_bytes())

    def test_symlink_and_unmanaged_store_refused(self):
        self.export(); target = self.root / "external"; target.mkdir(); self.store.symlink_to(target)
        with self.assertRaises(b.BackupError): b.restore(self.archive, self.store, self.password)
        self.assertEqual(self.tree(target), {})
        self.store.unlink(); self.store.mkdir(mode=0o700)
        (self.store / "original.txt").write_text("SYNTHETIC ORIGINAL")
        with self.assertRaises(b.BackupError): b.restore(self.archive, self.store, self.password)
        self.assertEqual((self.store / "original.txt").read_text(), "SYNTHETIC ORIGINAL")

    def test_live_wal_snapshot_committed_not_uncommitted(self):
        connection = sqlite3.connect(self.source / "core.sqlite"); self.addCleanup(connection.close)
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("INSERT INTO messages VALUES(13,'user','DEMO: committed WAL',NULL,2000)"); connection.commit()
        connection.execute("INSERT INTO messages VALUES(14,'user','DEMO: uncommitted',NULL,2001)")
        self.export(); _, objects, _ = b.verify_archive(self.archive, self.password)
        with b._database(objects["core/core.sqlite"]) as db:
            self.assertEqual(db.execute("SELECT id FROM messages ORDER BY id").fetchall(), [(11,), (12,), (13,)])
        self.assertEqual(connection.execute("SELECT id FROM messages ORDER BY id").fetchall(), [(11,), (12,), (13,), (14,)])
        connection.rollback()

    def test_invalid_consent_does_not_export(self):
        p = self.source / "memory-authorizations.json"; data = json.loads(p.read_text())
        data["records"][0]["text_sha256"] = "0" * 64; p.write_bytes(b.encoded(data))
        with self.assertRaises(b.BackupError): self.export()
        self.assertFalse(self.archive.exists())

    def test_disk_full_after_staging_preserves_current_generation(self):
        self.export(); first = b.restore(self.archive, self.store, self.password)
        other = self.root / "other.jvb"; b.export_demo(self.source, other, self.password)
        old = self.tree(self.generation())
        real_write = b.private_write
        def fail_receipt(path, data):
            if path.name == "receipt.json":
                raise OSError(errno.ENOSPC, "Synthetic disk full")
            return real_write(path, data)
        with mock.patch.object(b, "private_write", side_effect=fail_receipt):
            with self.assertRaises(OSError): b.restore(other, self.store, self.password, replace=True)
        self.assertEqual(self.active(), first["generation"])
        self.assertEqual(old, self.tree(self.generation()))
        b.recover(self.store)
        b.restore(other, self.store, self.password, replace=True)
        self.assertEqual(self.before, self.tree(self.source))

    def test_failed_pointer_write_and_orphan_control_recovery(self):
        self.export(); first = b.restore(self.archive, self.store, self.password)
        other = self.root / "other.jvb"; b.export_demo(self.source, other, self.password)
        real_replace = b.atomic_replace
        def fail_pointer(path, data):
            if path.name == "state.json":
                b.private_write(path.parent / (".pending-" + uuid.uuid4().hex), data)
                raise OSError(errno.EIO, "Synthetic write error")
            return real_replace(path, data)
        with mock.patch.object(b, "atomic_replace", side_effect=fail_pointer):
            with self.assertRaises(OSError): b.restore(other, self.store, self.password, replace=True)
        b.recover(self.store)
        self.assertEqual(self.active(), first["generation"])
        self.assertTrue(any(self.store.glob(".pending-*")))
        b.restore(other, self.store, self.password, replace=True)

    def test_two_processes_restore_are_serialized(self):
        self.export()
        code = "from pathlib import Path; import sys,json; from backup_prototype import backup as b; print(json.dumps(b.restore(Path(sys.argv[1]),Path(sys.argv[2]),sys.stdin.read())))"
        processes = [subprocess.Popen([sys.executable, "-c", code, str(self.archive), str(self.store)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
        for process in processes:
            process.stdin.write(self.password); process.stdin.close(); process.stdin = None
        results = [process.communicate(timeout=20) for process in processes]
        self.assertEqual([p.returncode for p in processes], [0, 0], results)
        self.assertEqual({json.loads(out)["status"] for out, _ in results}, {"restored", "already-restored"})
        b.validate_generation(self.store, self.active())

    def test_short_password(self):
        with self.assertRaises(b.BackupError): b.export_demo(self.source, self.archive, "short")
        self.assertFalse(self.archive.exists())


if __name__ == "__main__": unittest.main()
