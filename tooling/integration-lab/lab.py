#!/usr/bin/env python3
"""JARVIS INTEGRATION LAB: development tooling only, no inference or runtime authority."""
import argparse,json,os,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE));sys.path.insert(0,str(HERE.parents[1]))
from core import campaign,repository,reporting,evidence,policy

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['run','status','verify','audit','contracts','test','build','android','report','dashboard','export','compare'])
    parser.add_argument('--profile',choices=['safe','android_lab'],default='safe')
    parser.add_argument('--output',default='.audit-cache/integration-lab/latest')
    parser.add_argument('--source-root');parser.add_argument('--offline',action='store_true')
    parser.add_argument('--resume',action='store_true')
    parser.add_argument('--archive');parser.add_argument('--receipt')
    parser.add_argument('--before');parser.add_argument('--after')
    parser.add_argument('--serial',default=os.environ.get('ANDROID_SERIAL',''))
    parser.add_argument('--api',type=int,choices=[29,35],default=29)
    args=parser.parse_args(argv)
    try:
        if args.command=='status':
            p=Path(args.output)/'campaign.json'
            value=json.loads(p.read_text()) if p.exists() else repository.read_lock(HERE/'config/modules.lock.json')
        elif args.command=='verify' and args.archive:value=evidence.verify_archive(args.archive)
        elif args.command in ['report','dashboard']:
            p=Path(args.receipt) if args.receipt else Path(args.output)/'campaign.json'
            value=reporting.render(json.loads(p.read_text()),args.output)
        elif args.command=='export':value=evidence.export(args.output)
        elif args.command=='compare':
            if not args.before or not args.after:raise ValueError('BEFORE_AND_AFTER_REQUIRED')
            value=reporting.compare(*(json.loads(Path(p).read_text()) for p in [args.before,args.after]));evidence.write(Path(args.output)/'comparison.json',value)
        else:
            if args.command=='android' and args.profile!='android_lab':raise ValueError('ANDROID_LAB_PROFILE_REQUIRED')
            value=campaign.run(args,'audit' if args.command=='verify' else args.command)
            print(json.dumps({'status':value['status'],'campaign':value['id'],'output':str(Path(args.output).resolve())}))
            return policy.EXIT[value['status']]
        print(json.dumps(value,ensure_ascii=False,indent=2));return 0
    except (ValueError,KeyError) as e:
        print(json.dumps({'status':'FAIL','reason':str(e)}));return 3
    except OSError as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)}));return 4
    except KeyboardInterrupt:return 5

if __name__=='__main__':raise SystemExit(main())
