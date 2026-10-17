"""ID-001B offline candidate schema/security invariants, no CORE runtime or model."""
import copy
import json
from pathlib import Path
import unittest
import tempfile
from scripts import identity_contracts as ic

ROOT=Path(__file__).resolve().parents[1]/'docs/IDENTITY/001B'
def example(kind):return json.loads((ROOT/'examples'/(kind+'.valid.json')).read_text())
def graph():return [example(k) for k in ic.KINDS]

class IdentityCandidateTests(unittest.TestCase):
    def test_all_valid_examples_and_closed_invalid_examples(self):
        result=ic.self_check();self.assertEqual(result['valid_examples'],8);self.assertEqual(result['invalid_examples_rejected'],8)
    def test_candidate_bundle_and_real_validator_hash(self):
        self.assertEqual(len(ic.check_bundle()),64)
    def test_simulated_user_approval_must_match_its_own_target(self):
        p=example('jarvis-preference');p['provenance']='USER_APPROVED'
        with self.assertRaisesRegex(ic.IdentityError,'PREFERENCE_DECISION'):ic.validate_object(p)
        records=graph();p=next(r for r in records if r['kind']=='jarvis-preference');p['provenance']='USER_APPROVED'
        p['decision_ref']=ic.reference(next(r for r in records if r['kind']=='decision'))
        with self.assertRaisesRegex(ic.IdentityError,'DECISION_BINDING'):ic.validate_graph(records,2000)
    def test_graph_links_and_exact_result_digest(self):
        self.assertTrue(ic.validate_graph(graph(),2000))
    def test_manifest_cannot_add_permissions(self):
        for key in ['permissions','capabilities','system','model_path','tools']:
            m=example('manifest');m[key]=['execute']
            with self.subTest(key=key),self.assertRaises(ic.IdentityError):ic.validate_object(m)
    def test_duplicate_fields_rejected_before_schema(self):
        with self.assertRaisesRegex(ic.IdentityError,'DUPLICATE'):ic.decode(b'{"kind":"manifest","kind":"manifest"}')
    def test_unknown_nested_style_rejected(self):
        m=example('manifest');m['styles']['permission']='all'
        with self.assertRaises(ic.IdentityError):ic.validate_object(m)
    def test_incompatible_versions_and_fixtures(self):
        for version in ['jarvis.identity/1-draft','jarvis.identity/2','jarvis.fixture.p2/2']:
            m=example('manifest');m['version']=version
            with self.subTest(version=version),self.assertRaises(ic.IdentityError):ic.validate_object(m)
    def test_revision_not_boolean_float_negative_or_unsafe(self):
        for value in [True,1.0,-1,9007199254740992]:
            m=example('manifest');m['revision']=value
            with self.subTest(value=value),self.assertRaises(ic.IdentityError):ic.validate_object(m)
    def test_integer_boundary_is_portable(self):
        m=example('manifest');m['revision']=9007199254740991;self.assertTrue(ic.validate_object(m))
    def test_float_exponent_nonfinite_and_trailing_data(self):
        for raw in [b'{"n":1.0}',b'{"n":1e0}',b'{"n":NaN}',b'{}{}']:
            with self.subTest(raw=raw),self.assertRaises(ic.IdentityError):ic.decode(raw)
    def test_invalid_utf8_and_unpaired_surrogate(self):
        for raw in [b'\xff',b'{"a":"\\ud800"}']:
            with self.subTest(raw=raw),self.assertRaises(ic.IdentityError):ic.decode(raw)
    def test_wire_limit_before_json_parse(self):
        raw=ic.canonical(example('manifest'));padded=raw+b' '*(32768-len(raw))
        self.assertTrue(ic.validate_object(ic.decode(padded)))
        with self.assertRaisesRegex(ic.IdentityError,'WIRE_LIMIT'):ic.decode(padded+b' ')
    def test_cli_file_read_rejects_oversize_input(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'oversize.json';path.write_bytes(b' '*65536)
            with self.assertRaisesRegex(ic.IdentityError,'WIRE_LIMIT'):ic.read_document(path)
    def test_depth_list_and_multibyte_bounds(self):
        with self.assertRaises(ic.IdentityError):ic.decode(b'['*9+b'0'+b']'*9)
        self.assertTrue(ic.canonical({'a':'é'*4096}))
        with self.assertRaisesRegex(ic.IdentityError,'STRING_LIMIT'):ic.canonical({'a':'é'*4097})
        s=example('snapshot');s['consents']=[{'id':f'20000000-0000-4000-8000-{i:012d}','revision':1,'sha256':'a'*64} for i in range(16)]
        self.assertTrue(ic.validate_object(s));s['consents'].append({'id':'20000000-0000-4000-8000-000000000016','revision':1,'sha256':'a'*64})
        with self.assertRaises(ic.IdentityError):ic.validate_object(s)
    def test_unicode_and_field_order_vectors(self):
        self.assertEqual(ic.digest({'a':'é','b':'x'}),ic.digest({'b':'x','a':'é'}))
        self.assertNotEqual(ic.digest({'a':'é'}),ic.digest({'a':'e\u0301'}))
    def test_styles_are_typed_by_key(self):
        p=example('jarvis-preference');p['value']='TU'
        with self.assertRaisesRegex(ic.IdentityError,'STYLE_VALUE'):ic.validate_object(p)
    def test_personal_preference_cannot_be_durable(self):
        p=example('personal-preference');p['storage']='TECHNICAL_CONFIG'
        with self.assertRaises(ic.IdentityError):ic.validate_object(p)
    def test_pending_is_not_approval(self):
        p=example('change-proposal');p['decision_state']='APPROVED'
        with self.assertRaises(ic.IdentityError):ic.validate_object(p)
    def test_personal_proposal_cannot_persist_implicitly(self):
        p=example('change-proposal');p.update(target_kind='personal-preference',sensitivity='PERSONAL')
        with self.assertRaisesRegex(ic.IdentityError,'PERSONAL_PERSISTENCE'):ic.validate_object(p)
    def test_duplicate_patch_keys_and_noop_rejected(self):
        p=example('change-proposal');p['patch']*=2
        with self.assertRaises(ic.IdentityError):ic.validate_object(p)
        p=example('change-proposal');p['patch'][0]['new_value']=p['patch'][0]['old_value']
        with self.assertRaises(ic.IdentityError):ic.validate_object(p)
    def test_reference_and_snapshot_tampering(self):
        records=graph();s=next(r for r in records if r['kind']=='snapshot');s['manifest_ref']['sha256']='a'*64
        with self.assertRaisesRegex(ic.IdentityError,'REFERENCE'):ic.validate_graph(records,2000)
        records=graph();s=next(r for r in records if r['kind']=='snapshot');s['styles']['humour']='LIGHT'
        with self.assertRaisesRegex(ic.IdentityError,'SNAPSHOT'):ic.validate_graph(records,2000)
    def test_snapshot_expiration_and_read_only_scope(self):
        with self.assertRaisesRegex(ic.IdentityError,'EXPIRED'):ic.validate_graph(graph(),60000)
        records=graph();s=next(r for r in records if r['kind']=='snapshot');s['personal_preferences']=[ic.reference(example('personal-preference'))]
        with self.assertRaisesRegex(ic.IdentityError,'READ_ONLY'):ic.validate_graph(records,2000)
    def test_rejected_decision_cannot_apply_even_with_matching_digest(self):
        records=graph();d=next(r for r in records if r['kind']=='decision');d['decision']='REJECTED'
        next(r for r in records if r['kind']=='application')['decision_ref']=ic.reference(d)
        with self.assertRaisesRegex(ic.IdentityError,'DECISION_NOT_APPROVED'):ic.validate_graph(records,2000)
    def test_result_digest_must_match_exact_patch(self):
        records=graph();next(r for r in records if r['kind']=='application')['result_sha256']='f'*64
        with self.assertRaisesRegex(ic.IdentityError,'RESULT_DIGEST'):ic.validate_graph(records,2000)
    def test_revocation_expiry_and_ambiguous_consent(self):
        target=example('personal-preference');c=example('consent');subject=target['subject_ref']
        self.assertTrue(ic.consent_effective([c],target,subject,2000))
        self.assertFalse(ic.consent_effective([c],target,subject,60000))
        revoked=copy.deepcopy(c);revoked.update(id='10000000-0000-4000-8000-000000000099',decision='REVOKED',consent_revision=2)
        self.assertFalse(ic.consent_effective([c,revoked],target,subject,2000))
        duplicate=copy.deepcopy(c);duplicate['id']='10000000-0000-4000-8000-000000000098'
        self.assertFalse(ic.consent_effective([c,duplicate],target,subject,2000))
    def test_content_subject_and_target_expiry_bound_to_consent(self):
        target=example('personal-preference');c=example('consent')
        self.assertFalse(ic.consent_effective([c],target,'10000000-0000-4000-8000-000000000099',2000))
        target['value']='VOUS';self.assertFalse(ic.consent_effective([c],target,target['subject_ref'],2000))
        target=example('personal-preference');target['expires_ms']=1500;c['content_ref']=ic.reference(target)
        self.assertFalse(ic.consent_effective([c],target,target['subject_ref'],2000))
    def test_rollback_requires_reference_and_previous_digest(self):
        a=example('application');a['state']='ROLLED_BACK'
        with self.assertRaisesRegex(ic.IdentityError,'ROLLBACK'):ic.validate_object(a)

if __name__=='__main__':unittest.main()
