#!/usr/bin/env python3
"""Stage a single-source JARVIS monorepo snapshot from LOCAL Git repositories.

No network, checkout mutation, Git push, branch deletion, build, merge or deployment.
The destination must not exist; snapshot output is deliberately not auto-committed.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile

from validate_sources import DEFAULT_MANIFEST, load_and_validate

SKIP_DIRS = {
    ".git", ".github", ".gradle", ".deps", ".tools", "node_modules",
    "build", "__pycache__", ".idea", "secrets",
}
SKIP_SUFFIXES = {
    ".gguf", ".safetensors", ".apk", ".aab", ".jks", ".keystore",
    ".pem", ".key", ".p12", ".onnx", ".tflite", ".pt", ".pth", ".ckpt",
    ".sqlite", ".db",
}
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_ARCHIVE_BYTES = 200 * 1024 * 1024


def git_read(repo, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, timeout=180, check=False,
    )
    if proc.returncode:
        raise ValueError("Local Git command failed in {}: {}".format(repo.name, proc.stderr.decode("utf-8", "replace")[:200]))
    return proc.stdout


def excluded(name, module_id):
    parts = PurePosixPath(name).parts
    # Generated historic archives/captures are preserved at their original SHA,
    # but must not be copied into the runtime-source monorepo.
    if module_id == "voice" and parts[:1] == ("deliveries",):
        return True
    if module_id == "interface" and parts[:3] == ("labs", "v3", "captures"):
        return True
    if any(part in SKIP_DIRS for part in parts):
        return True
    path = PurePosixPath(name)
    return path.suffix.lower() in SKIP_SUFFIXES or (
        path.suffix.lower() == ".bin" and ("models" in parts or "model" in parts)
    )


def safe_relative(name):
    if not name or name.startswith("/") or chr(92) in name:
        raise ValueError("Invalid archive pathname")
    p = PurePosixPath(name)
    if ".." in p.parts or "." in p.parts or not p.parts:
        raise ValueError("Archive traversal rejected")
    return p


def stage_module(source_dir, target_dir, module):
    sha = module["source_sha"]
    kind = git_read(source_dir, "cat-file", "-t", sha).strip()
    if kind != b"commit":
        raise ValueError("Source SHA is not a commit: " + module["id"])
    archive = git_read(source_dir, "archive", "--format=tar", sha)
    if len(archive) > MAX_ARCHIVE_BYTES:
        raise ValueError("Git archive exceeds 200 MiB: " + module["id"])
    count = 0
    size = 0
    skipped = 0
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as tar:
        for member in tar:
            relative = safe_relative(member.name)
            if member.isdir():
                continue
            if not member.isfile() or member.issym() or member.islnk():
                raise ValueError("Unsafe Git archive entry: " + module["id"])
            if excluded(member.name, module["id"]):
                skipped += 1
                continue
            if member.size > MAX_FILE_BYTES:
                raise ValueError("Large tracked file needs review: " + module["id"])
            output = target_dir.joinpath(*relative.parts)
            output.parent.mkdir(parents=True, exist_ok=True)
            data = tar.extractfile(member)
            if data is None:
                raise ValueError("Unreadable Git archive entry")
            with output.open("xb") as handle:
                copied = shutil.copyfileobj(data, handle, length=1024 * 1024)
            os.chmod(output, 0o755 if member.mode & 0o111 else 0o644)
            count += 1
            size += member.size
    if not count:
        raise ValueError("Empty source snapshot: " + module["id"])
    return {
        "module": module["id"],
        "repository": module["repository"],
        "source_sha": sha,
        "archive_sha256": hashlib.sha256(archive).hexdigest(),
        "files": count,
        "bytes": size,
        "excluded_generated_or_sensitive_files": skipped,
        "integration_status": "SOURCE_STAGED_NOT_VALIDATED",
    }


def assemble(manifest_file, sources_dir, destination):
    manifest = load_and_validate(manifest_file)
    sources_dir = Path(sources_dir).resolve()
    destination = Path(destination).absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError("Refusing to overwrite destination")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent must already exist")
    if not sources_dir.is_dir():
        raise ValueError("Missing local source directory")
    for module in manifest["modules"]:
        path = sources_dir / module["id"]
        if not path.is_dir() or path.is_symlink():
            raise ValueError("Missing or linked local source: " + module["id"])
    with tempfile.TemporaryDirectory(prefix=".jarvis-monorepo-", dir=destination.parent) as tempdir:
        staged = Path(tempdir) / "snapshot"
        staged.mkdir()
        reports = []
        for module in manifest["modules"]:
            target = staged.joinpath(*PurePosixPath(module["target"]).parts)
            target.mkdir(parents=True)
            reports.append(stage_module(sources_dir / module["id"], target, module))
        (staged / "SOURCE-SNAPSHOT-REPORT.json").write_text(
            json.dumps({"schema_version": 1, "source_only": True, "modules": reports}, indent=2) + "\n",
            encoding="utf-8",
        )
        os.replace(staged, destination)
    return reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--sources-dir", type=Path, required=True,
                        help="Directory holding seven LOCAL Git checkouts named by module id")
    parser.add_argument("--destination", type=Path, required=True,
                        help="NEW empty path to receive modules/{id}; must not already exist")
    args = parser.parse_args()
    try:
        results = assemble(args.manifest, args.sources_dir, args.destination)
    except (ValueError, OSError, subprocess.TimeoutExpired, tarfile.TarError) as exc:
        print("NO-GO: " + str(exc), file=sys.stderr)
        return 2
    print("SOURCE SNAPSHOT STAGED; not compiled, integrated, merged, installed or qualified.")
    for item in results:
        print("{}: {} files, {} bytes".format(item["module"], item["files"], item["bytes"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
