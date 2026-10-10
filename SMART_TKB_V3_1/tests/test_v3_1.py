import copy,unittest,json
from pathlib import Path
from test_solver import fixture
from smart_tkb.solver import solve
from smart_tkb.validation import config_with_defaults,verify_schedule,signature,metrics
from smart_tkb.special import inventory,prepare_special
from smart_tkb.quality import features
from smart_tkb.exchange import export_schedule,import_schedule,summarize_schedule
ROOT=Path(__file__).resolve().parent.parent

def with_special():
 d=fixture();d['classes'][0]['grade']=6;d['classes'][1]['grade']=7
 d['subjects'].append(dict(id='HD02:NONE',base='HD02',name='Chào cờ / Sinh hoạt chủ nhiệm'))
 d['pending_special']=[dict(class_id=c['id'],subject_id='HD02:NONE',subject='Chào cờ / Sinh hoạt chủ nhiệm',count=1,source_row=i+2) for i,c in enumerate(d['classes'])]
 return d
class V31Tests(unittest.TestCase):
 def setUp(self):self.d=with_special();self.c=dict(days=2,periods=3,max_class_session=3,max_teacher_session=3,time_limit=2,workers=1)
 def overrides(self,**kw):return [dict(activity_id=a['activity_id'],validation_status='VERIFIED',verification_note='Fixture rule supplied explicitly',teacher_required=False,scheduling_policy='independent',**kw) for a in inventory(self.d)]
 def test_inventory_all_111_literal_classification(self):
  from smart_tkb.importer import read_pccm
  d=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');a=inventory(d)
  self.assertEqual(len(a),74);self.assertEqual(sum(x['weekly_count'] for x in a),111)
  self.assertEqual(sum(x['weekly_count'] for x in a if x['activity_type']=='EXPERIENTIAL_CAREER'),74)
  self.assertEqual(sum(x['weekly_count'] for x in a if x['activity_type']=='CC_SHCN_COMBINED'),37)
  self.assertTrue(all(x['teacher_id'] is None and x['teacher_required'] is None and x['validation_status']=='PENDING' and x['source_row'] for x in a))
 def test_strict_missing_rules_pending_not_scheduled(self):
  r=solve(self.d,self.c);self.assertEqual(r['placed'],6);self.assertEqual(r['special_report']['pending'],2);self.assertEqual(r['special_report']['scheduled'],0);self.assertFalse(r['official_complete'])
 def test_required_teacher_missing_stays_pending(self):
  self.c['special_overrides']=self.overrides();self.c['special_overrides'][0].update(teacher_required=True,teacher_id='UNKNOWN')
  r=solve(self.d,self.c);self.assertEqual(r['special_report']['verified'],1);self.assertEqual(r['special_report']['pending'],1)
 def test_verified_rules_null_teacher_no_fake_id(self):
  before=copy.deepcopy(self.d);self.c['special_overrides']=self.overrides()
  r=solve(self.d,self.c);self.assertEqual(self.d,before);self.assertEqual(r['placed'],8);self.assertTrue(r['official_complete'])
  self.assertTrue(all(l['teacher'] is None for l in r['lessons'] if l.get('is_special')));self.assertEqual(r['metrics']['visits'],sum(t['visits'] for t in r['teacher_visits']))
 def test_special_counts_against_class_capacity(self):
  self.c.update(days=1,mode='morning',special_overrides=self.overrides());self.d['assignments']=[self.d['assignments'][0]];self.d['assignments'][0]['count']=3
  r=solve(self.d,self.c);self.assertEqual(r['status'],'INFEASIBLE');self.assertIsNone(r['conflicts']);self.assertTrue(any('Lớp' in x for x in r['diagnostics']))
 def test_collective_shared_teacher_one_event_multiple_classes(self):
  o=self.overrides()
  for x in o:x.update(scheduling_policy='collective',shared_teacher_group='ASSEMBLY',teacher_required=True,teacher_id='T1',fixed_day=0,fixed_period=0,shift='am')
  self.c['special_overrides']=o;r=solve(self.d,self.c);events=[x for x in r['lessons'] if x.get('is_special')]
  self.assertEqual(len(events),1);self.assertEqual(set(events[0]['class_ids']),{'C1','C2'});self.assertEqual(r['special_report']['scheduled_verified'],2)
  self.assertTrue(verify_schedule(self.d,self.c,r['lessons'])['valid']);self.assertEqual(next(t for t in r['teacher_visits'] if t['teacher_id']=='T1')['periods'],5)
  bad=copy.deepcopy(r['lessons']);bad.append(copy.deepcopy(events[0]));self.assertFalse(verify_schedule(self.d,self.c,bad)['valid'])
 def test_real_teacher_overlap_not_relaxed_for_independent_events(self):
  o=self.overrides()
  for x in o:x.update(teacher_required=True,teacher_id='T1',fixed_day=0,fixed_period=0,shift='am')
  self.c['special_overrides']=o;self.assertEqual(solve(self.d,self.c)['status'],'INFEASIBLE')
 def test_collective_opposite_class_shifts_infeasible(self):
  o=self.overrides()
  for x in o:x.update(scheduling_policy='collective',shared_teacher_group='G')
  self.c.update(mode='mixed',special_overrides=o);self.assertEqual(solve(self.d,self.c)['status'],'INFEASIBLE')
 def test_special_fixed_room_and_holiday(self):
  self.c.update(rooms=[dict(id='HALL')],special_overrides=self.overrides(fixed_day=0,fixed_period=1,shift='am',room_id='HALL'))
  # Independent simultaneous events require different rooms; single HALL cannot be shared implicitly.
  self.assertEqual(solve(self.d,self.c)['status'],'INFEASIBLE')
 def test_scenario_explicit_selection_not_official(self):
  ids=[inventory(self.d)[0]['activity_id']]
  self.c.update(special_mode='SCENARIO',special_scenario=dict(enabled=True,activity_ids=ids,teacher_required=False,scheduling_policy='independent',assumption_label='Test selected only'))
  r=solve(self.d,self.c);self.assertEqual((r['required'],r['placed'],r['scenario_placed']),(6,6,1));self.assertEqual(r['scheduled_class_periods'],7);self.assertEqual(r['special_report']['pending'],2);self.assertTrue(r['simulation']);self.assertFalse(r['official_complete'])
 def test_scenario_requires_label_and_selection(self):
  self.c.update(special_mode='SCENARIO',special_scenario=dict(enabled=True,teacher_required=False,assumption_label='test'))
  with self.assertRaises(ValueError):solve(self.d,self.c)
 def test_source_type_count_class_cannot_be_overridden(self):
  self.c['special_overrides']=[dict(activity_id=inventory(self.d)[0]['activity_id'],weekly_count=99)]
  with self.assertRaises(ValueError):solve(self.d,self.c)
 def test_distribution_enabled_improves_warm_incumbent(self):
  d=fixture();d['classes']=d['classes'][:1];d['assignments']=d['assignments'][:1];d['assignments'][0]['count']=4
  a=d['assignments'][0];previous=[dict(assignment=a['id'],teacher=a['teacher'],class_id=a['class_id'],subject_id=a['subject_id'],subject=a['subject'],day=day,shift='am',period=p,length=1,room=None) for day,ps in [(0,[0,1,2]),(1,[0])] for p in ps]
  c=config_with_defaults(self.c);self.assertTrue(verify_schedule(d,c,previous)['valid']);before=features(d,c,previous);r=solve(d,c,previous)
  self.assertEqual(before['distribution_weighted'],2);self.assertEqual(r['quality_scores']['distribution_weighted'],0);self.assertEqual((r['metrics']['gaps'],r['metrics']['visits']),(0,2));self.assertEqual(r['status'],'OPTIMAL')
 def test_disabled_goals_and_normalized_bounds(self):
  self.c['objective_settings']={'distribution':dict(enabled=False,weight=1),'concentration':dict(enabled=False,weight=1)}
  r=solve(self.d,self.c);self.assertTrue(any(p['name']=='distribution' and p['status']=='SKIPPED_DISABLED' for p in r['phases']))
  for k in ['distribution_penalty_100','concentration_penalty_100']:self.assertTrue(0<=r['quality_scores'][k]<=100)
 def test_configured_adjacency_double_exemption_and_preferred_heavy(self):
  d=fixture();d['assignments']=d['assignments'][:1];d['assignments'][0]['double_count']=1
  self.c.update(subject_rules=[dict(subject='M1',adjacent_weight=5,preferred_periods=[0,1],period_weight=2)],heavy_subjects=['M1'],heavy_run_limit=1,heavy_weight=3)
  r=solve(d,self.c);q=r['quality_scores'];self.assertEqual(q['unnecessary_adjacency'],0);self.assertEqual(q['subject_period_preferences'],0);self.assertEqual(q['heavy_run_penalty'],3)
  phase=next(p for p in r['phases'] if p['name']=='concentration');self.assertEqual(phase['objective'],q['concentration_weighted'])
 def test_opt_in_hard_daily_limit_independent_verifier(self):
  self.c['subject_hard_limits']=[dict(subject='M1',grades=[6],max_daily=0)]
  self.assertEqual(solve(self.d,self.c)['status'],'INFEASIBLE')
  r=solve(self.d,{**self.c,'subject_hard_limits':[]});self.assertFalse(verify_schedule(self.d,self.c,r['lessons'])['valid'])
 def test_subject_period_preference_is_soft_and_separate_from_concentration(self):
  d=fixture();d['assignments']=d['assignments'][:1];d['assignments'][0]['double_count']=1
  c={**self.c,'fixed':[dict(assignment='A1',day=0,shift='am',period=0,length=2)],'subject_rules':[dict(subject='M1',preferred_periods=[2],period_weight=4)]}
  r=solve(d,c);self.assertTrue(r['verification']['valid']);self.assertEqual(r['metrics']['preferences'],8)
  self.assertEqual(r['quality_scores']['concentration_weighted'],1)
  phase=next(p for p in r['phases'] if p['name']=='preferences');self.assertEqual(phase['objective'],8)
 def test_grade_rules_and_overlapping_rule_rejected(self):
  self.c['subject_rules']=[dict(subject='M1',grades=[6],distribution_weight=3),dict(subject='M1',grades=[7],distribution_weight=0)]
  r=solve(self.d,self.c);self.assertTrue(r['verification']['valid'])
  self.c['subject_rules'].append(dict(subject='M1',grades=[6]))
  with self.assertRaises(ValueError):solve(self.d,self.c)
 def test_export_import_csv_excel_and_json_recomputes_counts(self):
  self.c['special_overrides']=self.overrides();r=solve(self.d,self.c)
  for fmt in ['csv','xlsx']:
   raw=export_schedule(self.d,self.c,r['lessons'],fmt);restored=import_schedule(self.d,self.c,raw,fmt)
   self.assertEqual((restored['placed'],restored['conflicts']),(8,0));self.assertFalse(restored['global_optimal_proven']);self.assertEqual(set(map(signature,restored['lessons'])),set(map(signature,r['lessons'])))
  restored=summarize_schedule(self.d,self.c,json.loads(json.dumps(r['lessons'])));self.assertEqual(restored['metrics'],r['metrics'])
 def test_exchange_rejects_tampered_identity(self):
  r=solve(self.d,self.c);bad=copy.deepcopy(r['lessons']);bad[0]['teacher']='FAKE'
  with self.assertRaises(ValueError):export_schedule(self.d,self.c,bad,'xlsx')
 def test_verifier_rejects_duplicate_class_units_and_tampered_special_flags(self):
  self.c['special_overrides']=self.overrides();r=solve(self.d,self.c)
  for kind in ['classes','flag','type']:
   bad=copy.deepcopy(r['lessons']);row=next(x for x in bad if x.get('is_special'))
   if kind=='classes':row['class_ids']*=2
   if kind=='flag':row['is_special']=False
   if kind=='type':row['activity_type']='GUESSED'
   self.assertFalse(verify_schedule(self.d,self.c,bad)['valid'])
 def test_unknown_no_conflict_claim(self):
  from smart_tkb.importer import read_pccm
  r=solve(read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx'),dict(time_limit=.001))
  self.assertEqual(r['status'],'UNKNOWN');self.assertIsNone(r['conflicts']);self.assertIsNone(r['metrics'])
if __name__=='__main__':unittest.main()
