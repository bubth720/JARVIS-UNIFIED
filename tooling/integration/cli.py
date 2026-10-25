"""Read-only offline BOM validation, Git fingerprints, planning and Markdown reporting."""
import argparse
import json
import sys
from .lock import ROOT, load, validate, verify_sources, markdown, plan, compare
from .proposals import check as check_proposals


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'report', 'plan', 'compare', 'proposals'])
    parser.add_argument('--lock', default=str(ROOT / 'integration-lock.json'))
    parser.add_argument('--repositories', help='Local JSON map exact repository name -> Git directory')
    parser.add_argument('--against', help='Second candidate lock, required by compare')
    args = parser.parse_args(argv)
    try:
        lock = validate(load(args.lock))
        verified = verify_sources(lock, load(args.repositories)) if args.repositories else {
            'mode': 'structure_only', 'sources_verified_now': False, 'hardware_qualified': False}
        if args.command == 'proposals':
            print(json.dumps(check_proposals(), sort_keys=True))
        elif args.command == 'report':
            print(markdown(lock), end='')
        elif args.command == 'plan':
            print(json.dumps({'scope': 'documentary_dependencies_only', 'phases': plan(lock)}, ensure_ascii=False, indent=2))
        elif args.command == 'compare':
            if not args.against: raise ValueError('--against required')
            print(json.dumps(compare(lock, load(args.against)), indent=2))
        else:
            print(json.dumps({'valid_candidate': True, **verified}, sort_keys=True))
        return 0
    except (ValueError, OSError, TypeError, KeyError, RecursionError) as exc:
        # No subprocess stderr/source content/credential/absolute private path is echoed.
        print('Integration validation rejected: ' + type(exc).__name__, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
