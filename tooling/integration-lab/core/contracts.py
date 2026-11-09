"""Reuse frozen UNIFIED validators; compare real schema bytes, never infer a runtime link."""
from pathlib import Path
from scripts.contracts import validate_contract
from tooling.contracts.manifest import strict_json
from tooling.contracts.compatibility import ContractCompatibilityChecker
from .integrity import sha

LINKS = [('CORE', 'LLM'), ('CORE', 'INTERFACE'), ('CORE', 'NEXUS'), ('CORE', 'SERVICES'),
         ('CORE', 'VOICE'), ('VOICE', 'INTERFACE'), ('EVOLUTION', 'UNIFIED'), ('NEXUS', 'SERVICES')]

def inspect(sources):
    rows = []; unified = sources.get('UNIFIED'); validations = []
    if unified:
        directory = Path(unified) / 'contracts/v1'
        for p in sorted(directory.glob('*.schema.json')):
            schema = strict_json(p.read_text()); name = p.name.removesuffix('.schema.json')
            good = strict_json((directory/'examples'/(name+'.valid.json')).read_text())
            bad = strict_json((directory/'examples'/(name+'.invalid.json')).read_text())
            validate_contract(name, good, schema)
            try: validate_contract(name, bad, schema)
            except ValueError: pass
            else: raise ValueError('INVALID_HISTORICAL_EXAMPLE_ACCEPTED')
            validations.append({'contract': name, 'version': 'v1', 'sha256': sha(p), 'valid_accepted': True,
                                'invalid_rejected': True, 'kind': 'SIMULATION', 'scope': 'HISTORICAL_SCHEMA_EXAMPLES_ONLY'})
    for a, b in LINKS:
        status = 'BLOCKED' if (a, b) == ('CORE', 'LLM') else 'UNKNOWN'
        row = {'from': a, 'to': b, 'status': status, 'runtime_connected': False,
               'version': 'UNKNOWN', 'max_message_bytes': None, 'session_binding': 'UNKNOWN',
               'cancellation': 'UNKNOWN', 'errors': 'UNKNOWN', 'permissions': 'UNKNOWN',
               'resource_ownership': 'UNKNOWN', 'timeout': 'UNKNOWN', 'cleanup': 'UNKNOWN',
               'backward_compatibility': 'UNKNOWN', 'schema_equality': 'NOT_RUN',
               'reason': 'Authority and exact preparation are not admitted' if status == 'BLOCKED' else 'No qualified bilateral adapter in this composition'}
        if (a, b) == ('CORE', 'VOICE') and unified and 'VOICE' in sources:
            voice = Path(sources['VOICE'])/'voiceBridgeContract/src/main/resources/unified-v1'
            pairs = [(p, voice/p.name) for p in (Path(unified)/'contracts/v1').glob('*.schema.json')]
            row['schema_equality'] = 'COMPATIBLE' if len(pairs) == 5 and all(q.is_file() and sha(p) == sha(q) for p,q in pairs) else 'INCOMPATIBLE'
            row['version'] = 'UNIFIED_v1_COPIED_SCHEMAS'
            row['reason'] = 'Schema equality is static only; CORE to VOICE runtime remains unqualified'
        rows.append(row)
    # Actual frozen generated-contract checker, no new schema or public API.
    generated = 'NOT_RUN'
    if unified:
        p = Path(unified)/'contracts/generated/manifest.json'
        if p.is_file(): generated = ContractCompatibilityChecker.compare(strict_json(p.read_text()), strict_json(p.read_text()))['status']
    return {'status': 'PASS' if len(validations) == 5 and generated == 'COMPATIBLE' else 'BLOCKED',
            'kind': 'STATIC', 'links': rows, 'schema_tests': validations, 'generated_self_consistency': generated,
            'runtime_integration_proven': False, 'scope': 'FORMAT_AND_EVIDENCE_ONLY'}
