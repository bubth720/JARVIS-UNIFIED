"""Self-contained end-to-end proof with disposable, synthetic data and key."""
import json
from pathlib import Path
import secrets
import tempfile
from . import backup as b


def tree(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def main():
    with tempfile.TemporaryDirectory(prefix="jarvis-mission002-demo-") as work:
        root = Path(work)
        source, archive, store = root / "synthetic", root / "demo.jvb", root / "store"
        password = secrets.token_urlsafe(48)  # In-memory, never printed or saved.
        b.create_demo(source)
        originals = tree(source)
        b.export_demo(source, archive, password)
        _, objects, _ = b.verify_archive(archive, password)
        first = b.restore(archive, store, password)
        generation = store / "generations" / first["generation"]
        previous = tree(generation)
        assert all((generation / "payload" / p).read_bytes() == v for p, v in objects.items())
        second = root / "second.jvb"
        b.export_demo(source, second, password)
        try:
            b.restore(second, store, password, replace=True, fail_at="after_activate")
        except b.SimulatedCrash:
            pass
        else:
            raise AssertionError("Fault injection did not run")
        assert json.loads((store / "state.json").read_text())["active"] != first["generation"]
        recovery = b.recover(store)
        assert json.loads((store / "state.json").read_text())["active"] == first["generation"]
        assert tree(generation) == previous
        assert tree(source) == originals
        b.restore(second, store, password, replace=True)
        assert tree(source) == originals
        print(json.dumps({"fixture": "synthetic-only", "create_encrypted_archive": "PASS",
                          "verify": "PASS", "restore_bytes": "PASS", "simulated_error_after_activation": "PASS",
                          "recovery": recovery["status"], "previous_generation_unchanged": "PASS",
                          "source_unchanged": "PASS", "retry": "PASS", "files": len(objects)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
