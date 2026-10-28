"""Reject any lot3 changes outside the coordinator's explicit allowlist."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'e4c678faf630a0a98adfaecd7a87fc11dfd82486'
ALLOWED = ('docs/prefusion/lot3/', 'tooling/integration/prefusion_lot3_tests/')
FILES = {'docs/prefusion/LOT3-ASSESSMENT.md', 'tooling/integration/prefusion_lot3.py',
         'scripts/check_prefusion_lot3.py', '.github/workflows/prefusion-lot3.yml'}


def check():
    changed = subprocess.check_output(['git', 'diff', '--name-only', BASE], cwd=ROOT, text=True).splitlines()
    changed += subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, text=True).splitlines()
    rejected = sorted({p for p in changed if p not in FILES and not p.startswith(ALLOWED)})
    if rejected:
        raise SystemExit('OUT OF SCOPE: ' + ', '.join(rejected))
    print('PASS: lot3 scope; historical contracts, locks, snapshots and runtimes unchanged')


if __name__ == '__main__':
    check()
