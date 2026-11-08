import copy,json,pathlib,tempfile,unittest
from tooling.v1 import validate as v

class V1Safety(unittest.TestCase):
 def setUp(self):
  self.lock=v.read(v.REPORTS/'BASELINE-LOCK.json');self.modules=v.check_lock(self.lock)
  self.caps=v.read(v.REPORTS/'CAPABILITY-EVIDENCE.json');self.gates=v.read(v.REPORTS/'GATES.json');self.score=v.read(v.REPORTS/'SCORE.json')
 def test_real_snapshot_is_valid(self):self.assertEqual('PASS',v.validate()['status'])
 def test_all_sensitive_actions_stay_closed(self):
  for action in v.SENSITIVE:self.assertFalse(v.permitted(action))
  self.assertFalse(v.permitted('unknown_future_action'));self.assertTrue(v.permitted('unit_tests'))
 def test_short_git_sha_refused(self):
  self.lock['modules'][0]['source_sha']='5da9838'
  with self.assertRaisesRegex(v.InvalidEvidence,'BAD_GIT'):v.check_lock(self.lock)
 def test_duplicate_module_refused(self):
  self.lock['modules'].append(self.lock['modules'][0])
  with self.assertRaisesRegex(v.InvalidEvidence,'MODULE_SET'):v.check_lock(self.lock)
 def test_default_branch_is_not_assumed_main(self):
  self.assertEqual('development/mission-002',self.modules['INTERFACE']['default_branch']);self.assertNotEqual('main',self.modules['VOICE']['default_branch'])
 def test_unknown_repository_licence_is_preserved(self):self.assertTrue(all(m['repository_license']=='UNKNOWN' for m in self.modules.values()))
 def test_truncated_tree_refused(self):
  self.lock['modules'][0]['reference_tree_truncated']=True
  with self.assertRaisesRegex(v.InvalidEvidence,'TRUNCATED'):v.check_lock(self.lock)
 def test_unpinned_source_link_refused(self):
  self.lock['modules'][0]['source_documents'][0]['url']='https://github.com/bubth720/repo/blob/main/x'
  with self.assertRaisesRegex(v.InvalidEvidence,'SOURCE_URL'):v.check_lock(self.lock)
 def test_ci_of_another_commit_refused(self):
  self.lock['modules'][0]['ci_observed'][0]['head_sha']='f'*40
  with self.assertRaisesRegex(v.InvalidEvidence,'CI_AT_WRONG_COMMIT'):v.check_lock(self.lock)
 def test_ci_failure_not_reclassified_as_success(self):
  self.assertTrue(any(r['conclusion']=='failure' for r in self.modules['LLM']['ci_observed']))
  self.assertTrue(any(r['conclusion']=='failure' for r in self.modules['VOICE']['ci_observed']))
 def test_ready_label_without_meaning_refused(self):
  self.caps['capabilities'][0]['availability']='READY'
  with self.assertRaisesRegex(v.InvalidEvidence,'CAPABILITY_STATE'):v.check_capabilities(self.caps,self.modules)
 def test_active_without_approved_runtime_refused(self):
  self.caps['capabilities'][0]['availability']='ACTIVE_VERIFIED'
  with self.assertRaisesRegex(v.InvalidEvidence,'NO_APPROVED'):v.check_capabilities(self.caps,self.modules)
 def test_boolean_claim_needs_evidence(self):
  self.caps['capabilities'][0]['dimensions']['tested']['value']=True
  with self.assertRaisesRegex(v.InvalidEvidence,'MISSING_EVIDENCE'):v.check_capabilities(self.caps,self.modules)
 def test_source_inspection_is_not_execution(self):
  c=self.caps['capabilities'][0];c['dimensions']['tested']={'value':True,'tested_commit':c['source_sha'],'evidence_ref':'source_CORE'}
  with self.assertRaisesRegex(v.InvalidEvidence,'WRONG_PROOF_LAYER'):v.check_capabilities(self.caps,self.modules)
 def test_missing_dimension_never_defaults_to_false(self):
  del self.caps['capabilities'][0]['dimensions']['experienced']
  with self.assertRaisesRegex(v.InvalidEvidence,'DIMENSION_SET'):v.check_capabilities(self.caps,self.modules)
 def test_score_platform_cannot_be_changed_to_weaker_layer(self):
  self.score['criteria'][2]['required_platform']='HOST_EXECUTED'
  with self.assertRaisesRegex(v.InvalidEvidence,'SCORE_CRITERIA_SPEC'):v.check_score(self.score,self.modules,self.caps['evidence'])
 def test_runtime_connected_boolean_cannot_open_gate(self):
  self.caps['capabilities'][0]['connected']=True
  with self.assertRaisesRegex(v.InvalidEvidence,'RUNTIME_PROOF'):v.check_capabilities(self.caps,self.modules)
 def test_physical_qualification_is_not_source_or_emulator(self):
  self.caps['capabilities'][0]['device_qualified']=True
  with self.assertRaisesRegex(v.InvalidEvidence,'RUNTIME_PROOF'):v.check_capabilities(self.caps,self.modules)
 def test_absent_latency_must_not_be_zero(self):
  self.caps['metrics']['ttft_p50_ms']=0
  with self.assertRaisesRegex(v.InvalidEvidence,'ABSENT_MEASURE'):v.check_capabilities(self.caps,self.modules)
 def test_p95_not_published_under_twenty_samples(self):
  self.caps['metrics'].update(comparable_trials=19,ttft_p95_ms=100)
  with self.assertRaisesRegex(v.InvalidEvidence,'P95_REQUIRES'):v.check_capabilities(self.caps,self.modules)
 def test_self_claimed_approval_is_not_authorization(self):
  self.gates['gates'][0].update(approved=True,approval_ref='PR_DRAFT_OPEN')
  with self.assertRaisesRegex(v.InvalidEvidence,'HUMAN_GATE'):v.check_gates(self.gates)
 def test_preparation_never_marks_gate_pass(self):
  self.gates['gates'][0]['status']='PASS'
  with self.assertRaisesRegex(v.InvalidEvidence,'GATE_CANNOT'):v.check_gates(self.gates)
 def test_root_does_not_open_from_workflow_success(self):
  self.gates['lab_patch']['root']='PROVISIONED'
  with self.assertRaisesRegex(v.InvalidEvidence,'LAB_SCOPE'):v.check_gates(self.gates)
 def test_score_weights_are_fixed_at_one_hundred(self):
  self.assertEqual(100,sum(self.score['domain_weights'].values()));self.assertEqual(0,v.check_score(self.score,self.modules,self.caps['evidence']))
 def test_documentation_does_not_earn_points(self):
  row=self.score['criteria'][0];row.update(state='PASS',evidence_ref='source_LLM',tested_commit=self.modules['LLM']['source_sha'])
  self.score['qualified_points']=row['weight'];self.score['unassessed_or_blocked_points']=100-row['weight']
  with self.assertRaisesRegex(v.InvalidEvidence,'WRONG_PROOF_LAYER'):v.check_score(self.score,self.modules,self.caps['evidence'])
 def test_score_claim_cannot_skip_platform(self):
  row=self.score['criteria'][2];mod=row['module_id'];sha=self.modules[mod]['source_sha'];self.caps['evidence']['fake']={'module_id':mod,'tested_commit':sha,'kind':'EXECUTION','status':'PASS','url':'https://github.com/bubth720/example','platform':'HOST_EXECUTED','operation_ids':[row['operation_id']],'artifact_sha256':'a'*64}
  row.update(state='PASS',evidence_ref='fake',tested_commit=sha)
  with self.assertRaisesRegex(v.InvalidEvidence,'SCORE_WRONG_PLATFORM'):v.check_score(self.score,self.modules,self.caps['evidence'])
 def test_false_prepared_points_refused(self):
  self.score['prepared_points_earned']=30
  with self.assertRaisesRegex(v.InvalidEvidence,'NO_POINTS'):v.check_score(self.score,self.modules,self.caps['evidence'])
 def test_criterion_weights_cannot_silently_change(self):
  self.score['criteria'][0]['weight']+=1
  with self.assertRaisesRegex(v.InvalidEvidence,'SCORE_CRITERIA_SPEC'):v.check_score(self.score,self.modules,self.caps['evidence'])
 def test_duplicate_json_keys_are_rejected(self):
  with self.assertRaisesRegex(v.InvalidEvidence,'DUPLICATE_JSON_KEY'):json.loads('{"state":"PASS","state":"FAIL"}',object_pairs_hook=v.no_duplicates)
 def test_model_artifact_and_path_escape_refused(self):
  for name in ('model.gguf','profile.onnx','../../private.zip','voice.wav'):
   with self.assertRaises(v.InvalidEvidence):v.check_artifact(name,'a'*64)
 def test_public_artifact_needs_exact_hash(self):
  v.check_artifact('lab.apk','a'*64)
  with self.assertRaises(v.InvalidEvidence):v.check_artifact('lab.apk','unknown')
 def test_svg_is_deterministic_and_labels_unassessed_scope(self):
  a=v.graph_svg(self.score);self.assertEqual(a,v.graph_svg(self.score));self.assertIn('non évalué/bloqué',a);self.assertIn('historique',a)

if __name__=='__main__':unittest.main()
