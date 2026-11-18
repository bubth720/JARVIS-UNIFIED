"""Run real local HTTPS tests behind a process fence; optionally require OS netns."""
import argparse
import json
from pathlib import Path
import platform
import resource
import socket
import sys
import time
import tracemalloc
import unittest
from .fence import install


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--require-isolation', action='store_true')
    args = parser.parse_args()
    interfaces = [name for _, name in socket.if_nameindex()]
    routes = Path('/proc/net/route').read_text().splitlines()[1:]
    isolated = set(interfaces) == {'lo'} and not routes
    if args.require_isolation and not isolated:
        raise SystemExit('A loopback-only OS network namespace is required')
    fence = install()
    before = resource.getrusage(resource.RUSAGE_SELF)
    started = time.monotonic()
    tracemalloc.start()
    suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent/'tests'))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    after = resource.getrusage(resource.RUSAGE_SELF)
    data = dict(format='jarvis.research-b0-test-results/1', platform=platform.platform(),
        python=sys.version, tests=result.testsRun, failures=len(result.failures), errors=len(result.errors),
        skipped=len(result.skipped), result='PASS' if result.wasSuccessful() else 'FAIL',
        wall_seconds=time.monotonic()-started, cpu_user_seconds=after.ru_utime-before.ru_utime,
        cpu_system_seconds=after.ru_stime-before.ru_stime, process_max_rss_kib=after.ru_maxrss,
        python_peak_allocated_bytes=peak, os_loopback_only_namespace=isolated,
        interfaces=interfaces, loopback_connect_events=fence.accepted,
        blocked_connect_attempts=fence.denied, blocked_dns_attempts=fence.dns_attempts,
        production_connected=False, external_collection=False, gpu_spend_eur=0)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data))
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    raise SystemExit(main())
