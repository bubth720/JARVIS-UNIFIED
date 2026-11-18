"""Explicit synthetic demonstration. Default invocation starts no network."""
import argparse
import asyncio
import json
from pathlib import Path
from .contracts import Limits
from .fence import install
from .fixtures import SyntheticServer,TLSMaterial
from .policy import LabPolicy
from .store import Ledger
from .transport import LabResearch


async def run(args):
    install()
    material=TLSMaterial()
    try:
        async with SyntheticServer(material) as server:
            ledger=Ledger(args.store,Limits.profile(args.profile))
            try:
                research=LabResearch(LabPolicy(server),ledger)
                research.enable_lab()
                plan=server.plan('/redirect')
                document=await research.start(plan,research.approve(plan))
                print(json.dumps(dict(document=document,mission=ledger.snapshot(),
                    production_connected=False,external_collection=False),indent=2))
            finally:
                ledger.close()
    finally:
        material.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--enable-lab',action='store_true')
    parser.add_argument('--store',type=Path)
    parser.add_argument('--profile',choices=['android','mini-pc'],default='android')
    args=parser.parse_args()
    if not args.enable_lab:
        print(json.dumps(dict(state='DISABLED',network_started=False,production_connected=False)))
        return
    if args.store is None:parser.error('--store is required with --enable-lab')
    asyncio.run(run(args))


if __name__=='__main__':main()
