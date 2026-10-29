"""Restrict this lot's diff to its additive lab, evidence and CI files."""
import argparse
import subprocess


def allowed(path):
    return (path.startswith('docs/prefusion/LOT3-')
            or path in ('tooling/integration/lot3_lab.py', 'tooling/integration/lot3_scope.py')
            or path.startswith('tooling/integration/lot3_tests/')
            or path == '.github/workflows/prefusion-lot3.yml')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', required=True)
    args = parser.parse_args()
    changed = subprocess.check_output(['git', 'diff', '--name-only', '-z', args.base], text=True)
    untracked = subprocess.check_output(['git', 'ls-files', '--others', '--exclude-standard', '-z'], text=True)
    paths = sorted(set((changed + untracked).strip('\0').split('\0')) - {''})
    forbidden = [path for path in paths if not allowed(path)]
    print({'files': paths, 'forbidden': forbidden, 'runtime_authorized': False})
    return bool(forbidden)


if __name__ == '__main__':
    raise SystemExit(main())
