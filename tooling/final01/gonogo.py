"""F01 — strict GO / NO-GO gate for FINAL-01 lots.

Inputs (JSON):
  requirements: {"lot": "F05", "required": [{"id": "S04-API29-qualification", "sha": "<40 hex>"}, ...]}
  evidence:     [{"id": "...", "sha": "<40 hex>", "result": "PASS", "source": "run 4463... / local replay"}, ...]

Rules (FINAL-01 §C, owner instruction 21/11 "un test non exécuté, inconnu, ignoré ou bloqué ne doit pas devenir
un résultat positif"):
  * Only the exact string "PASS" counts. FAIL, BLOCKED, BLOCKED_DEVICE, NOT_RUN, UNKNOWN, SKIPPED, empty, any other
    spelling or case → NO-GO.
  * Evidence must be at the EXACT required SHA (40 hex). A branch name, a short SHA or another commit → NO-GO.
  * A required test with no evidence → NO-GO. Contradictory evidence for one test (PASS and FAIL at the same SHA) → NO-GO.
  * Every evidence item must name its source. An empty requirement list → NO-GO (nothing proven is not GO).
  * The verdict GO only means "every required test passed at that SHA"; it never authorises a merge, an install or
    an activation (those stay owner decisions).
"""
import argparse, json, re, sys

SHA = re.compile(r'^[0-9a-f]{40}$')


def decide(requirements, evidence):
    reasons, checked = [], []
    required = requirements.get('required') or []
    if not required:
        return {'lot': requirements.get('lot'), 'verdict': 'NO-GO', 'reasons': ['no required test declared'], 'checked': []}
    by_key = {}
    for e in evidence:
        by_key.setdefault((e.get('id'), e.get('sha')), []).append(e)
    for r in required:
        rid, sha = r.get('id'), r.get('sha')
        if not isinstance(sha, str) or not SHA.match(sha):
            reasons.append(f'{rid}: required SHA is not a full 40-hex commit ({sha!r})'); checked.append((rid, 'INVALID_REQUIREMENT')); continue
        items = by_key.get((rid, sha), [])
        if not items:
            others = sorted({e.get('sha') for e in evidence if e.get('id') == rid})
            reasons.append(f'{rid}: no evidence at {sha}' + (f' (only at {others})' if others else '')); checked.append((rid, 'MISSING')); continue
        results = {str(e.get('result')) for e in items}
        if any(not e.get('source') for e in items):
            reasons.append(f'{rid}: evidence without source'); checked.append((rid, 'UNSOURCED')); continue
        if results != {'PASS'}:
            reasons.append(f'{rid}: {"/".join(sorted(results))} at {sha}'); checked.append((rid, '/'.join(sorted(results)))); continue
        checked.append((rid, 'PASS'))
    return {'lot': requirements.get('lot'), 'verdict': 'GO' if not reasons else 'NO-GO', 'reasons': reasons,
            'checked': [{'id': i, 'status': s} for i, s in checked],
            'note': 'GO = every required test PASS at the exact SHA; never an authorisation to merge, install or activate.'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('requirements'); ap.add_argument('evidence')
    a = ap.parse_args()
    out = decide(json.load(open(a.requirements)), json.load(open(a.evidence)))
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False); print()
    sys.exit(0 if out['verdict'] == 'GO' else 1)
