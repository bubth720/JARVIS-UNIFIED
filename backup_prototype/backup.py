"""Bounded encrypted synthetic backups and recoverable generation activation.

Only generated demo datasets are supported. Not a production Android exporter.
"""
from __future__ import annotations

import argparse
import base64
from contextlib import closing, contextmanager
from datetime import datetime, timezone
import fcntl
import getpass
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import uuid

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

MAGIC = b"JVBK\x00\x01"
HEADER_SIZE = len(MAGIC) + 16 + 12
MAX_FILE = 4 * 1024 * 1024
MAX_TOTAL = 16 * 1024 * 1024
MAX_ENVELOPE = 24 * 1024 * 1024
PURPOSE = "synthetic-demo-only"
DEMO_ENGINE = "jarvis-demo-no-inference-v1"
DEMO_PACK = hashlib.sha256(b"SYNTHETIC-NOT-A-MODEL").hexdigest()
PATHS = {
    "core/core.sqlite": ("sqlite-core", 2),
    "core/memory-authorizations.json": ("memory-authorizations", 1),
    "core/preferences.json": ("preferences", 1),
    "llm/catalogue.json": ("catalogue-demo", 1),
    "resources/resources.json": ("resource-references", 1),
    "voices/demo/profile.json": ("voice-demo", 1),
}
SOURCES = {
    "CORE": "226e2e8cc3eebd479805b89d035eb5c1cbcad540",
    "LLM": "1756e29557287550b5cfdffdd911cada2a302db6",
    "VOICE": "9429a9ebf0f21909ac6c59a07491fa2bca027493",
}
SCHEMA = (
    "CREATE TABLE messages(id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT NOT NULL, text TEXT NOT NULL, source TEXT, created_at INTEGER NOT NULL)",
    "CREATE TABLE memories(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, created_at INTEGER NOT NULL)",
    "CREATE TABLE documents(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, mime TEXT, created_at INTEGER NOT NULL)",
    "CREATE TABLE chunks(id INTEGER PRIMARY KEY AUTOINCREMENT, document_id INTEGER NOT NULL, document_name TEXT NOT NULL, chunk_index INTEGER NOT NULL, text TEXT NOT NULL)",
    "CREATE INDEX idx_chunks_doc ON chunks(document_id)",
)


class BackupError(Exception):
    """Safe failure, without displaying payloads or secrets."""


class SimulatedCrash(BackupError):
    pass


def require(condition, message):
    if not condition:
        raise BackupError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key")
        result[key] = value
    return result


def decoded(data: bytes):
    try:
        return json.loads(data, object_pairs_hook=_pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(BackupError("Invalid JSON number")))
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise BackupError("Invalid JSON") from exc


def safe_path(path: Path):
    """Reject existing symlinks including ancestors; caller owns the parent tree."""
    path = Path(os.path.abspath(path))
    require(not any(p.is_symlink() for p in (path, *path.parents)), "Symlinks are forbidden")
    return path


def read_small(path: Path, limit=MAX_FILE) -> bytes:
    path = safe_path(path)
    require(path.is_file() and path.stat().st_size <= limit, "Missing, non-regular or oversized file")
    with path.open("rb") as stream:
        result = stream.read(limit + 1)
    require(len(result) <= limit, "Oversized file")
    return result


def sync_dir(path: Path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def private_write(path: Path, data: bytes):
    with path.open("xb") as stream:
        os.chmod(path, 0o600)
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def atomic_replace(path: Path, data: bytes):
    """Replace only prototype control files in a locked, private store."""
    temp = path.parent / (".pending-" + uuid.uuid4().hex)
    private_write(temp, data)
    os.replace(temp, path)
    sync_dir(path.parent)


def create_demo(root: Path):
    root = safe_path(root)
    require(not root.exists(), "Demo destination already exists")
    root.mkdir(mode=0o700, parents=True)
    with sqlite3.connect(root / "core.sqlite") as db:
        for statement in SCHEMA:
            db.execute(statement)
        db.execute("PRAGMA user_version=2")
        db.execute("INSERT INTO messages VALUES(11,'user','DEMO: bonjour',NULL,1000)")
        db.execute("INSERT INTO messages VALUES(12,'assistant','DEMO: réponse','demo.txt',1001)")
        db.executemany("INSERT INTO memories VALUES(?,?,?)", [
            (21, "DEMO: souvenir autorisé", 1002),
            (22, "DEMO: proposition en attente", 1003),
            (23, "DEMO: proposition refusée", 1004),
        ])
        db.execute("INSERT INTO documents VALUES(31,'demo.txt','text/plain',1005)")
        db.execute("INSERT INTO chunks VALUES(41,31,'demo.txt',0,'DEMO: passage fictif')")
    values = {
        "fixture.json": {"purpose": PURPOSE, "version": 1},
        "memory-authorizations.json": {"version": 1, "records": [
            {"id": 21, "text_sha256": sha("DEMO: souvenir autorisé".encode()), "status": "confirmed", "proof": "synthetic-user-confirmation-21"},
            {"id": 22, "text_sha256": sha("DEMO: proposition en attente".encode()), "status": "pending", "proof": None},
            {"id": 23, "text_sha256": sha("DEMO: proposition refusée".encode()), "status": "rejected", "proof": None},
        ]},
        "preferences.json": {"version": 1, "prompt": "DEMO uniquement", "ctx": 512, "max": 64, "topk": 4, "speak": False},
        "catalogue.json": {"version": 1, "records": [{"id": "demo.hello", "revision": 1, "text": "DEMO: bonjour"}]},
        "resources.json": {"version": 1, "models": [
            {"deployment": "TABLET", "reference": "Qwen3-0.6B-Q4_K_M", "status": "not-included", "sha256": None},
            {"deployment": "MOBILE", "reference": "Qwen3-1.7B-Q4_K_M", "status": "not-included", "sha256": None},
            {"deployment": "CENTRAL", "reference": None, "status": "unqualified", "sha256": None},
        ]},
        "voice-demo.json": {"version": 1, "format": "JARVIS-DEMO-VOICE-1", "engine_id": DEMO_ENGINE,
                            "pack_sha256": DEMO_PACK, "inference_usable": False,
                            "description": "Synthetic profile metadata; no audio or tensors"},
    }
    for name, value in values.items():
        private_write(root / name, encoded(value))
    os.chmod(root / "core.sqlite", 0o600)
    sync_dir(root)


def check_database(db):
    db.execute("PRAGMA trusted_schema=OFF")
    require(db.execute("PRAGMA integrity_check").fetchall() == [("ok",)], "SQLite integrity failure")
    require(db.execute("PRAGMA user_version").fetchone()[0] == 2, "Unsupported SQLite version")
    sql = {row[0] for row in db.execute("SELECT sql FROM sqlite_master WHERE name != 'sqlite_sequence'")}
    require(sql == set(SCHEMA), "Unexpected SQLite schema")
    require(not db.execute("SELECT 1 FROM chunks LEFT JOIN documents ON chunks.document_id=documents.id WHERE documents.id IS NULL").fetchone(), "Orphan document chunk")


def _database(data: bytes):
    require(data.startswith(b"SQLite format 3\x00"), "Invalid SQLite header")
    db = sqlite3.connect(":memory:")
    try:
        db.deserialize(data)
        check_database(db)
        return db
    except Exception:
        db.close()
        raise


def snapshot_demo(source: Path) -> dict[str, bytes]:
    source = safe_path(source)
    require(decoded(read_small(source / "fixture.json")) == {"purpose": PURPOSE, "version": 1}, "Only generated demo datasets are accepted")
    original = safe_path(source / "core.sqlite")
    require(original.is_file() and original.stat().st_size <= MAX_FILE, "Invalid database size")
    authorizations = decoded(read_small(source / "memory-authorizations.json"))
    require(authorizations.get("version") == 1, "Unsupported authorization version")
    # Read-only connection + SQLite Backup API includes committed WAL pages.
    with sqlite3.connect(original.as_uri() + "?mode=ro", uri=True) as src:
        with sqlite3.connect(":memory:") as dest:
            src.backup(dest)
            # Validate the live backup connection. Deserializing a WAL-mode
            # header before compaction would require unavailable WAL sidecars.
            check_database(dest)
            rows = dict(dest.execute("SELECT id,text FROM memories"))
            approved = []
            seen = set()
            for record in authorizations["records"]:
                require(record["id"] not in seen, "Duplicate memory authorization")
                seen.add(record["id"])
                require(record["id"] in rows and sha(rows[record["id"]].encode()) == record["text_sha256"], "Memory authorization does not match exact text")
                if record["status"] == "confirmed" and record["proof"]:
                    approved.append(record)
            ids = {record["id"] for record in approved}
            for memory_id in rows:
                if memory_id not in ids:
                    dest.execute("DELETE FROM memories WHERE id=?", (memory_id,))
            dest.commit()
            # Rebuild the COPY so deleted/unapproved rows do not remain in free pages.
            dest.execute("VACUUM")
            database = dest.serialize()
    objects = {
        "core/core.sqlite": database,
        "core/memory-authorizations.json": encoded({"version": 1, "records": approved}),
        "core/preferences.json": read_small(source / "preferences.json"),
        "llm/catalogue.json": read_small(source / "catalogue.json"),
        "resources/resources.json": read_small(source / "resources.json"),
        "voices/demo/profile.json": read_small(source / "voice-demo.json"),
    }
    validate_objects(objects)
    return objects


def validate_objects(objects):
    require(set(objects) == set(PATHS), "Unexpected or missing payload paths")
    require(all(len(data) <= MAX_FILE for data in objects.values()), "Object too large")
    require(sum(map(len, objects.values())) <= MAX_TOTAL, "Payload too large")
    with closing(_database(objects["core/core.sqlite"])) as db:
        memories = dict(db.execute("SELECT id,text FROM memories"))
    auth = decoded(objects["core/memory-authorizations.json"])
    require(isinstance(auth, dict) and type(auth.get("version")) is int and auth["version"] == 1 and isinstance(auth.get("records"), list), "Invalid authorization schema")
    records = auth["records"]
    require(all(isinstance(r, dict) and set(r) == {"id", "text_sha256", "status", "proof"}
                and type(r["id"]) is int and isinstance(r["proof"], str) for r in records), "Invalid authorization record")
    require(len(records) == len(memories) and {r["id"] for r in records} == set(memories), "Missing or duplicate authorizations")
    for record in records:
        require(record["status"] == "confirmed" and bool(record["proof"]), "Unconfirmed memory in archive")
        require(record["text_sha256"] == sha(memories[record["id"]].encode()), "Memory text changed")
    for path in PATHS:
        if path.endswith(".json"):
            value = decoded(objects[path])
            require(isinstance(value, dict) and type(value.get("version")) is int and value["version"] == 1, "Unsupported object schema")
    voice = decoded(objects["voices/demo/profile.json"])
    require(voice.get("format") == "JARVIS-DEMO-VOICE-1" and voice.get("engine_id") == DEMO_ENGINE
            and voice.get("pack_sha256") == DEMO_PACK and voice.get("inference_usable") is False, "Incompatible demo voice profile")


def pack(objects: dict[str, bytes]) -> bytes:
    validate_objects(objects)
    manifest = {
        "format": "jarvis-backup", "version": 1, "purpose": PURPOSE,
        "archive_id": str(uuid.uuid4()), "created_utc": datetime.now(timezone.utc).isoformat(),
        "source_revisions": SOURCES, "required_engines": [{"id": DEMO_ENGINE, "pack_sha256": DEMO_PACK, "usable": False}],
        "compatibility": {"reader": "mission002-python-v1", "android_adapter": False, "pc_inference": False},
        "files": [{"path": path, "kind": PATHS[path][0], "schema_version": PATHS[path][1],
                   "size": len(data), "sha256": sha(data)} for path, data in sorted(objects.items())],
    }
    return encoded({"manifest": manifest, "objects": {path: base64.b64encode(data).decode("ascii") for path, data in objects.items()}})


def unpack(plain: bytes):
    require(len(plain) <= MAX_ENVELOPE, "Payload too large")
    doc = decoded(plain)
    require(isinstance(doc, dict) and set(doc) == {"manifest", "objects"}, "Invalid archive structure")
    m = doc["manifest"]
    require(isinstance(m, dict) and isinstance(doc["objects"], dict), "Invalid manifest or objects")
    require(m.get("format") == "jarvis-backup" and type(m.get("version")) is int and m["version"] == 1 and m.get("purpose") == PURPOSE, "Unsupported archive version or purpose")
    require(set(m) == {"format", "version", "purpose", "archive_id", "created_utc", "source_revisions", "required_engines", "compatibility", "files"}, "Unknown manifest field")
    try:
        require(str(uuid.UUID(m["archive_id"])) == m["archive_id"], "Invalid archive UUID")
        require(datetime.fromisoformat(m["created_utc"]).utcoffset().total_seconds() == 0, "Timestamp must use UTC")
    except (ValueError, TypeError, AttributeError) as exc:
        raise BackupError("Invalid archive identity or timestamp") from exc
    require(m["source_revisions"] == SOURCES, "Unknown source schema baseline")
    require(m["required_engines"] == [{"id": DEMO_ENGINE, "pack_sha256": DEMO_PACK, "usable": False}], "Incompatible required engine")
    require(m["compatibility"] == {"reader": "mission002-python-v1", "android_adapter": False, "pc_inference": False}, "Unknown compatibility contract")
    require(isinstance(m["files"], list) and len(m["files"]) == len(PATHS), "Invalid manifest inventory")
    require(set(doc["objects"]) == set(PATHS), "Unexpected object paths")
    objects = {}
    for entry in m["files"]:
        require(isinstance(entry, dict) and set(entry) == {"path", "kind", "schema_version", "size", "sha256"}, "Invalid file metadata")
        path = entry["path"]
        require(isinstance(path, str) and path in PATHS and path not in objects, "Unsafe, duplicate or unknown path")
        require(type(entry["schema_version"]) is int and (entry["kind"], entry["schema_version"]) == PATHS[path] and type(entry["size"]) is int and 0 <= entry["size"] <= MAX_FILE, "Unsupported file metadata")
        try:
            data = base64.b64decode(doc["objects"][path], validate=True)
        except (ValueError, TypeError) as exc:
            raise BackupError("Invalid object encoding") from exc
        require(len(data) == entry["size"] and sha(data) == entry["sha256"], "Object integrity failure")
        objects[path] = data
    validate_objects(objects)
    return m, objects


def derive(password: str, salt: bytes):
    require(isinstance(password, str) and 12 <= len(password) <= 1024, "Password must contain 12 to 1024 characters")
    return Scrypt(salt=salt, length=32, n=32768, r=8, p=1).derive(password.encode("utf-8"))


def seal(plain: bytes, password: str) -> bytes:
    require(len(plain) <= MAX_ENVELOPE - HEADER_SIZE - 16, "Archive too large")
    salt, nonce = os.urandom(16), os.urandom(12)
    header = MAGIC + salt + nonce
    return header + AESGCM(derive(password, salt)).encrypt(nonce, plain, header)


def unseal(blob: bytes, password: str) -> bytes:
    require(HEADER_SIZE + 16 <= len(blob) <= MAX_ENVELOPE and blob.startswith(MAGIC), "Invalid/truncated envelope or unsupported version")
    header = blob[:HEADER_SIZE]
    salt = header[len(MAGIC):len(MAGIC) + 16]
    nonce = header[-12:]
    try:
        return AESGCM(derive(password, salt)).decrypt(nonce, blob[HEADER_SIZE:], header)
    except InvalidTag as exc:
        raise BackupError("Authentication failed: wrong password or damaged archive") from exc


def export_demo(source: Path, output: Path, password: str):
    output = safe_path(output)
    require(not output.exists(), "Archive already exists; choose a new name")
    source = safe_path(source)
    require(source != output and source not in output.parents, "Archive must be outside the source")
    blob = seal(pack(snapshot_demo(source)), password)
    unpack(unseal(blob, password))  # Verify before exposing a completed archive.
    output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".jvb-pending-", dir=output.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(blob); stream.flush(); os.fsync(stream.fileno())
        # Atomic no-clobber publication, same filesystem; completed output is never partial.
        os.link(temp, output)
        sync_dir(output.parent)
    finally:
        temp.unlink(missing_ok=True)
    return {"archive_sha256": sha(blob), "files": len(PATHS)}


def verify_archive(archive: Path, password: str):
    blob = read_small(archive, MAX_ENVELOPE)
    manifest, objects = unpack(unseal(blob, password))
    return manifest, objects, sha(blob)


def _generation_id(value):
    require(isinstance(value, str) and len(value) == 32 and all(c in "0123456789abcdef" for c in value), "Invalid generation ID")
    return value


def _state(root):
    file = root / "state.json"
    if not file.exists():
        return None
    result = decoded(read_small(file))
    require(set(result) == {"active", "previous"}, "Invalid state")
    _generation_id(result["active"])
    if result["previous"] is not None:
        _generation_id(result["previous"])
    return result


@contextmanager
def locked_store(root: Path):
    root = safe_path(root)
    require(not root.exists() or root.is_dir(), "Store must be a directory")
    root.mkdir(mode=0o700, parents=True, exist_ok=True)
    require(root.stat().st_mode & 0o077 == 0, "Store must be private (0700)")
    allowed = {".lock", "store.json", "generations", "state.json", "journal.json"}
    def allowed_control(path):
        # A process can die between fsync(temp) and rename(control). Keep such
        # orphan control files without trusting or deleting them during recovery.
        suffix = path.name.removeprefix(".pending-")
        pending = path.name.startswith(".pending-") and len(suffix) == 32 and all(c in "0123456789abcdef" for c in suffix)
        return (path.name in allowed or pending) and not path.is_symlink()
    require(all(allowed_control(p) for p in root.iterdir()), "Not a clean managed store")
    lock_path = safe_path(root / ".lock")
    with lock_path.open("a+b") as lock:
        os.chmod(lock_path, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
        marker = root / "store.json"
        if marker.exists():
            require(decoded(read_small(marker)) == {"format": "jarvis-demo-store", "version": 1}, "Unknown store")
        else:
            require(not any((root / name).exists() for name in ["generations", "state.json", "journal.json"]), "Unrecognized existing store")
            private_write(marker, encoded({"format": "jarvis-demo-store", "version": 1}))
        generations = safe_path(root / "generations")
        generations.mkdir(mode=0o700, exist_ok=True)
        sync_dir(root)
        yield root


def memory_review(objects, confirmations):
    records = decoded(objects["core/memory-authorizations.json"])["records"]
    eligible = {str(r["id"]) + ":" + r["text_sha256"] for r in records}
    confirmations = set(confirmations)
    require(confirmations <= eligible, "Local memory confirmation does not match exact content")
    return {"version": 1, "records": [
        {"id": r["id"], "text_sha256": r["text_sha256"],
         "activation": "confirmed-locally" if str(r["id"]) + ":" + r["text_sha256"] in confirmations else "pending-local-confirmation"}
        for r in records]}


def validate_generation(root, generation):
    directory = safe_path(root / "generations" / _generation_id(generation))
    m = decoded(read_small(directory / "manifest.json"))
    objects = {p: read_small(directory / "payload" / p) for p in PATHS}
    # Reuse complete manifest + payload validation, not just per-file hashes.
    unpack(encoded({"manifest": m, "objects": {p: base64.b64encode(v).decode() for p, v in objects.items()}}))
    review = decoded(read_small(directory / "memory-review.json"))
    receipt = decoded(read_small(directory / "receipt.json"))
    local = [str(r["id"]) + ":" + r["text_sha256"] for r in review["records"] if r["activation"] == "confirmed-locally"]
    require(review == memory_review(objects, local), "Invalid memory activation state")
    require(receipt.get("review_sha256") == sha(encoded(review)), "Memory policy integrity failure")
    return receipt, review


def restore(archive: Path, root: Path, password: str, *, replace=False, confirmations=(), fail_at=None):
    manifest, objects, archive_hash = verify_archive(archive, password)
    review = memory_review(objects, confirmations)
    # No destination write before full cryptographic and semantic verification.
    with locked_store(root) as root:
        require(not (root / "journal.json").exists(), "Interrupted transaction: recover first")
        old = _state(root)
        if old:
            receipt, previous_review = validate_generation(root, old["active"])
            if receipt["archive_sha256"] == archive_hash and previous_review == review:
                return {"status": "already-restored", "generation": old["active"]}
            require(replace, "Destination conflict: explicit replace required; previous generation retained")
        generation = uuid.uuid4().hex
        stage = root / "generations" / (generation + ".staging")
        stage.mkdir(mode=0o700)
        for path, data in objects.items():
            destination = stage / "payload" / path
            destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            private_write(destination, data)
        private_write(stage / "manifest.json", encoded(manifest))
        private_write(stage / "memory-review.json", encoded(review))
        private_write(stage / "receipt.json", encoded({"archive_sha256": archive_hash, "review_sha256": sha(encoded(review))}))
        for directory, _, _ in os.walk(stage, topdown=False):
            sync_dir(Path(directory))
        if fail_at == "after_stage":
            raise SimulatedCrash("Simulated interruption after staging")
        final = stage.with_name(generation)
        os.rename(stage, final)
        sync_dir(final.parent)
        validate_generation(root, generation)
        new = {"active": generation, "previous": old["active"] if old else None}
        atomic_replace(root / "journal.json", encoded({"version": 1, "old": old, "new": new}))
        if fail_at == "before_activate":
            raise SimulatedCrash("Simulated interruption before activation")
        atomic_replace(root / "state.json", encoded(new))
        if fail_at == "after_activate":
            raise SimulatedCrash("Simulated interruption after activation")
        (root / "journal.json").unlink()
        sync_dir(root)
        return {"status": "restored", "generation": generation}


def recover(root: Path):
    with locked_store(root) as root:
        journal = root / "journal.json"
        if not journal.exists():
            state = _state(root)
            if state:
                validate_generation(root, state["active"])
            return {"status": "no-transaction", "staging_retained": True}
        record = decoded(read_small(journal))
        require(set(record) == {"version", "old", "new"} and record["version"] == 1, "Unknown journal")
        current = _state(root)
        require(current in (record["old"], record["new"]), "Journal/state conflict; manual review required")
        if record["old"]:
            validate_generation(root, record["old"]["active"])
            atomic_replace(root / "state.json", encoded(record["old"]))
        else:
            (root / "state.json").unlink(missing_ok=True)
            sync_dir(root)
        journal.unlink()
        sync_dir(root)
        return {"status": "rolled-back", "generations_retained": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    fixture = commands.add_parser("demo-fixture")
    fixture.add_argument("directory", type=Path)
    export = commands.add_parser("export")
    export.add_argument("source", type=Path); export.add_argument("archive", type=Path)
    verify = commands.add_parser("verify")
    verify.add_argument("archive", type=Path)
    rest = commands.add_parser("restore")
    rest.add_argument("archive", type=Path); rest.add_argument("store", type=Path)
    rest.add_argument("--replace", action="store_true")
    rest.add_argument("--confirm-memory", action="append", default=[], metavar="ID:SHA256")
    rest.add_argument("--simulate-crash", choices=["after_stage", "before_activate", "after_activate"])
    recovery = commands.add_parser("recover")
    recovery.add_argument("store", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "demo-fixture":
            create_demo(args.directory); result = {"status": "synthetic-fixture-created"}
        elif args.command == "recover":
            result = recover(args.store)
        else:
            password = getpass.getpass("Mot de passe de sauvegarde (12 caractères minimum) : ")
            if args.command == "export":
                require(password == getpass.getpass("Confirmer le mot de passe : "), "Passwords differ")
                result = export_demo(args.source, args.archive, password)
            elif args.command == "verify":
                m, _, digest = verify_archive(args.archive, password)
                result = {"status": "verified", "files": len(m["files"]), "archive_sha256": digest}
            else:
                result = restore(args.archive, args.store, password, replace=args.replace,
                                 confirmations=args.confirm_memory, fail_at=args.simulate_crash)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (BackupError, OSError, sqlite3.Error, KeyError, TypeError, ValueError) as exc:
        # Never print attacker-controlled JSON values, paths or SQL contents.
        print("Échec sûr : " + (str(exc) if isinstance(exc, BackupError) else type(exc).__name__))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
