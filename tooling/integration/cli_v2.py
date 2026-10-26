"""Read-only FUSION-02 validation, comparison and release matrix."""
import argparse,json,sys
from .lock import ROOT,load
from .v2 import validate,verify,compare_to_v1,assess,report


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['validate','compare','assess','report'])
    p.add_argument('--lock',default=str(ROOT/'integration-lock-v2.json'))
    p.add_argument('--repositories')
    args=p.parse_args(argv)
    try:
        value=validate(load(args.lock))
        evidence=verify(value,load(args.repositories)) if args.repositories else {'mode':'structure_only','sources_verified_now':False}
        if args.command=='report':print(report(value),end='')
        else:
            result=compare_to_v1(value) if args.command=='compare' else assess(value) if args.command=='assess' else {'valid_candidate':True,**evidence}
            print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,KeyError,TypeError,RecursionError) as e:
        print('FUSION-02 rejected: '+type(e).__name__,file=sys.stderr);return 1


if __name__=='__main__':raise SystemExit(main())
