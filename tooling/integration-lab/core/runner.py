"""Bounded process groups; preserve nonzero exits, interruptions, timeouts and truncation."""
import os, re, signal, subprocess, tempfile, time, xml.etree.ElementTree as ET
from pathlib import Path

def stop(process):
    if process.poll() is not None: return
    os.killpg(process.pid, signal.SIGTERM)
    try: process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL); process.wait(timeout=3)

def execute(argv, cwd, log, timeout, env=None, max_bytes=8*1024*1024):
    if not argv or not all(isinstance(a, str) for a in argv): raise ValueError('INVALID_ARGV')
    log = Path(log); log.parent.mkdir(parents=True, exist_ok=True); start = time.monotonic_ns()
    state = 'PASS'; reason = None; code = None
    process = None
    with log.open('wb') as sink:
        try:
            process = subprocess.Popen(argv, cwd=cwd, stdout=sink, stderr=subprocess.STDOUT,
                                       env=env, start_new_session=True, stdin=subprocess.DEVNULL)
            while process.poll() is None:
                if time.monotonic_ns()-start > timeout*1_000_000_000:
                    state, reason = 'FAIL', 'TIMEOUT'; stop(process); break
                if log.stat().st_size > max_bytes:
                    state, reason = 'FAIL', 'OUTPUT_TRUNCATED'; stop(process); break
                time.sleep(0.05)
            code = process.wait()
            if log.stat().st_size > max_bytes:
                state, reason = 'FAIL', 'OUTPUT_TRUNCATED'; sink.truncate(max_bytes)
            if code and state == 'PASS': state, reason = 'FAIL', 'PROCESS_SIGNAL' if code < 0 else 'NONZERO_EXIT'
        except OSError as e:
            state, reason = 'BLOCKED', 'EXECUTABLE_UNAVAILABLE:' + type(e).__name__
        except BaseException:
            if process: stop(process)
            raise
    text = log.read_text(errors='replace')
    match = re.search(r'(?m)^Ran (\d+) tests?\b', text)
    result = {'status': state, 'reason': reason, 'exit_code': code, 'duration_ns': time.monotonic_ns()-start,
              'clock': 'time.monotonic_ns', 'argv': argv, 'test_invocations': int(match[1]) if match else None,
              'unique_test_cases': None, 'truncated': reason == 'OUTPUT_TRUNCATED'}
    if match and (int(match[1]) == 0 or not re.search(r'(?m)^OK(?:\s|$)', text)) and state == 'PASS':
        result.update(status='FAIL', reason='TEST_SUCCESS_EVIDENCE_MISSING')
    return result

def junit(root):
    rows = []; identities = set(); failures = 0; skipped = 0
    for p in sorted(Path(root).glob('**/build/test-results/**/TEST-*.xml')):
        e = ET.parse(p).getroot()
        for c in e.iter('testcase'):
            identity = c.get('classname', '') + '#' + c.get('name', '')
            identities.add(identity); failures += int(c.find('failure') is not None or c.find('error') is not None)
            skipped += int(c.find('skipped') is not None); rows.append(identity)
    return {'test_invocations': len(rows), 'unique_test_cases': len(identities), 'failures': failures, 'skipped': skipped}
