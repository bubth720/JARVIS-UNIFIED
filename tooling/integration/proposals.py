"""Offline review of the proposed technical-only observation; never a runtime grant."""
from pathlib import Path
from scripts.contracts import ContractError, validate, validate_schema
from .lock import ROOT, load


def check(root=ROOT):
    directory = Path(root) / 'docs/fusion-01/proposals'
    schema = load(directory / 'technical-health.schema.json')
    validate_schema(schema)
    validate(load(directory / 'technical-health.valid.json'), schema)
    try:
        validate(load(directory / 'technical-health.invalid.json'), schema)
    except ContractError:
        return {'proposal': 'jarvis.technical-health/1-draft', 'valid_examples': 1,
                'invalid_examples_rejected': 1, 'approved': False, 'runtime_connected': False}
    raise ContractError('Private-data example was accepted')
