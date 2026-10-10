import copy,io,json,unittest
from pathlib import Path
from unittest.mock import patch
from smart_tkb.grade import *
from smart_tkb.grade_exchange import export_grade,import_grade
from smart_tkb.importer import read_pccm
from smart_tkb.validation import metrics
ROOT=Path(__file__).resolve().parent.parent

def fixture():
 cs=[dict(id='C'+str(g),name=str(g)+'A1',grade=g,shift='am') for g in [6,7,8,9]]
 ts=[dict(id='T'+str(i),name='Cùng nhãn',status='VERIFIED',full_name='GV '+str(i)) for i in [1,2,3]]
 def a(id,c,t,count=1,room=False):return dict(id=id,class_id=c,teacher=t,subject_id='M:NONE',subject='Môn',count=count,double_count=0,room_ids=['LAB'] if room else [])
 d=dict(classes=cs,teachers=ts,subjects=[dict(id='M:NONE',base='M',name='Môn')],assignments=[a('A8','C8','T1',2,True),a('B8','C8','T2'),a('A9','C9','T1',1,True),a('A6','C6','T3'),a('A7','C7','T3')],pending_special=[],issues=[])
 c=dict(target_grade=8,mode='both',days=2,active_days=[0,1],periods=3,session_periods={'am':3,'pm':2},max_class_session=3,max_teacher_session=3,rooms=[dict(id='LAB')],workers=1,time_limit=2,seed=17)
 rows=[]
 for aid,day,sh,per in [('A9',0,'am',0),('A6',0,'pm',0),('A7',1,'am',0)]:
  ass=next(a for a in d['assignments'] if a['id']==aid);rows.append(dict(assignment=aid,class_id=ass['class_id'],teacher=ass['teacher'],subject_id=ass['subject_id'],subject=ass['subject'],day=day,shift=sh,period=per,length=1,room='LAB' if aid=='A9' else None))
 bg=dict(lessons=rows,config={**c,'target_grade':9,'session_periods':{'am':3,'pm':3}},source_label='Synthetic complete fixture')
 return d,c,bg

class GradeTests(unittest.TestCase):
 def setUp(self):self.d,self.c,self.bg=fixture()
 def runok(self,previous=None,scope=None):
  r=solve_grade(self.d,self.c,self.bg,previous,scope=scope)
  self.assertIn(r['status'],['FEASIBLE','OPTIMAL']);self.assertEqual(r['placed'],3);self.assertEqual(r['grade_scheduling'],'PASS');self.assertEqual(r['cross_grade_conflict'],'PASS');self.assertTrue(r['verification']['valid']);self.assertEqual(r['locked_hash_before'],r['locked_hash_after']);return r
 def test_defaults_and_source_grade_filter(self):
  c=grade_config();self.assertEqual((c['target_grade'],c['mode'],c['session_periods'],c['active_days']),(8,'both',{'am':5,'pm':4},list(range(6))))
  d=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');before=json.dumps(d,sort_keys=True);bg=json.loads((ROOT/'data/LOCKED_BACKGROUND_SOURCE.json').read_text());p=prepare_grade(d,None,bg)
  self.assertEqual((len(p['target_data']['classes']),p['target_data']['required_periods'],p['special']['pending'],len(p['unverified_teacher_ids']),len(p['background_context']['cross_grade_teachers'])),(9,234,27,26,17));self.assertEqual(len(p['locked']),738);self.assertFalse(p['background_context']['complete']);self.assertEqual(json.dumps(d,sort_keys=True),before)
 def test_only_grade_decision_variables_exact_ids(self):
  r=self.runok();self.assertEqual(r['model_scope']['class_ids'],['C8']);self.assertEqual(r['model_scope']['assignment_ids'],['A8','B8']);self.assertEqual(r['model_scope']['locked_lesson_decision_variables'],0);self.assertTrue(all(x['class_id']=='C8' for x in r['lessons']))
 def test_frozen_cross_teacher_and_room(self):
  r=self.runok();self.assertFalse(any(x['day']==0 and x['shift']=='am' and x['period']==0 and (x['teacher']=='T1' or x['room']=='LAB') for x in r['lessons']));self.assertEqual(r['locked_lessons'],self.bg['lessons'])
 def test_missing_background_blocks_without_cp(self):
  with patch('smart_tkb.grade._solve_core',side_effect=AssertionError('must not build CP')):r=solve_grade(self.d,self.c,None)
  self.assertEqual(r['status'],'BLOCKED');self.assertIsNone(r['school_conflicts']);self.assertEqual(r['cross_grade_conflict'],'BLOCKED')
 def test_explicit_missing_simulation_stays_unknown(self):
  self.c.update(allow_incomplete_background=True,background_assumption='All missing background slots remain unknown')
  r=solve_grade(self.d,self.c,None);self.assertIn(r['status'],['FEASIBLE','OPTIMAL']);self.assertTrue(r['simulation']);self.assertIsNone(r['cross_grade_conflicts']);self.assertIsNone(r['school_conflicts']);self.assertEqual(r['cross_grade_conflict'],'BLOCKED')
 def test_simulation_requires_label(self):
  self.c['allow_incomplete_background']=True
  with self.assertRaises(ValueError):prepare_grade(self.d,self.c,self.bg)
 def test_corrupt_background_is_rejected_no_cp(self):
  self.bg['lessons'].append(copy.deepcopy(self.bg['lessons'][0]))
  with patch('smart_tkb.grade._solve_core',side_effect=AssertionError('must not build CP')):
   with self.assertRaisesRegex(ValueError,'Lịch nền'):solve_grade(self.d,self.c,self.bg)
 def test_locked_infeasible_no_unlock(self):
  self.c['fixed']=[dict(assignment='A8',day=0,shift='am',period=0)]
  before=schedule_hash(self.bg['lessons']);r=solve_grade(self.d,self.c,self.bg)
  self.assertEqual(r['status'],'INFEASIBLE');self.assertEqual(r['lessons'],[]);self.assertEqual(schedule_hash(self.bg['lessons']),before);self.assertTrue(any('khóa' in x for x in r['diagnostics']))
 def test_shared_room_alone_blocks_other_teacher(self):
  self.d['assignments'][2]['teacher']='T2';self.bg['lessons'][0]['teacher']='T2';self.c['fixed']=[dict(assignment='A8',day=0,shift='am',period=0)]
  self.assertEqual(solve_grade(self.d,self.c,self.bg)['status'],'INFEASIBLE')
 def test_max_teacher_load_includes_locked(self):
  self.c['max_teacher_session']=2;self.c['fixed']=[dict(assignment='A8',day=0,shift='am',period=1),dict(assignment='A8',day=0,shift='am',period=2)]
  self.assertEqual(solve_grade(self.d,self.c,self.bg)['status'],'INFEASIBLE')
 def test_new_global_holiday_rejects_frozen_data(self):
  self.c['unavailable']=[dict(kind='teacher',id='T1',day=0,shift='am',period=0)]
  with self.assertRaisesRegex(ValueError,'lịch nghỉ'):solve_grade(self.d,self.c,self.bg)
 def test_immutable_every_field_hash_critical(self):
  r=self.runok();p=prepare_grade(self.d,self.c,self.bg)
  for key,value in [('teacher','T2'),('room',None),('annotation','edited')]:
   after=copy.deepcopy(p['locked']);after[0][key]=value;v=verify_grade(p,r['lessons'],after);self.assertFalse(v['valid']);self.assertTrue(any('CRITICAL' in e for e in v['errors']))
 def test_independent_verifier_detects_cross_overlap(self):
  r=self.runok();p=prepare_grade(self.d,self.c,self.bg);bad=copy.deepcopy(r['lessons']);a=next(x for x in bad if x['assignment']=='A8');a.update(day=0,shift='am',period=0)
  self.assertFalse(verify_grade(p,bad)['valid'])
 def test_warm_incumbent_and_local_scope(self):
  r=self.runok();self.c.update(time_limit=.001,priorities=['changes','gaps','visits','distribution','preferences','concentration']);q=self.runok(r['lessons'],dict(classes=['C8']))
  self.assertTrue(q['performance']['warm_incumbent_valid']);self.assertEqual(q['metrics']['changes'],0);self.assertEqual(q['lessons'],r['lessons']);self.assertFalse(q['global_optimal_proven']);self.assertFalse(q['grade_optimal_proven']);self.assertEqual(q['optimality_scope'],'local_grade_with_frozen_background')
 def test_local_scope_cannot_unlock_other_grade(self):
  r=self.runok()
  with self.assertRaises(ValueError):solve_grade(self.d,self.c,self.bg,r['lessons'],scope=dict(classes=['C9']))
 def test_three_modes_and_noncontiguous_days(self):
  self.c['active_days']=[1]
  for mode in ['morning','both','mixed']:
   self.c['mode']=mode;r=self.runok();self.assertTrue(all(x['day']==1 for x in r['lessons']))
   if mode!='both':self.assertTrue(all(x['shift']=='am' for x in r['lessons']))
 def test_asymmetric_periods_and_double_room(self):
  self.d['assignments'][0]['double_count']=1;self.c['fixed']=[dict(assignment='A8',day=1,shift='pm',period=0,length=2)]
  r=self.runok();self.assertTrue(all(x['period']+x['length']<=self.c['session_periods'][x['shift']] for x in r['lessons']));self.assertTrue(any(x['length']==2 and x['room']=='LAB' for x in r['lessons']))
 def test_background_calendar_wider_than_target(self):
  self.c.update(days=1,active_days=[0],periods=2,session_periods={'am':2,'pm':2});self.bg['config'].update(days=6,active_days=list(range(6)),periods=5,session_periods={'am':5,'pm':5});self.bg['lessons'][2].update(day=5,period=4)
  r=self.runok();self.assertEqual(r['metrics']['baseline_visits'],3);self.assertTrue(all(x['day']==0 and x['period']<2 for x in r['lessons']))
 def test_combined_metric_added_visits_independent_sets(self):
  r=self.runok();b={(x['teacher'],x['day'],x['shift']) for x in self.bg['lessons']};t={(x['teacher'],x['day'],x['shift']) for x in r['lessons']};self.assertEqual(r['metrics']['visits'],len(b|t));self.assertEqual(r['metrics']['added_visits'],len(t-b))
  for phase in r['phases']:
   if phase['name'] in ['gaps','visits'] and phase['status']=='OPTIMAL':self.assertEqual(round(phase['objective']),r['metrics'][phase['name']])
 def test_exchange_roundtrip_and_no_inherited_proof(self):
  r=self.runok()
  for fmt in ['csv','xlsx']:
   raw=export_grade(self.d,self.c,self.bg,r['lessons'],fmt);restored=import_grade(self.d,self.c,self.bg,raw,fmt);self.assertEqual(restored['placed'],3);self.assertEqual(restored['locked_hash_after'],r['locked_hash_before']);self.assertFalse(restored['grade_optimal_proven']);self.assertEqual(restored['phases'],[])
 def test_same_display_name_does_not_merge_teacher(self):
  p=prepare_grade(self.d,self.c,self.bg);self.assertEqual([t['teacher_id'] for t in p['background_context']['cross_grade_teachers']],['T1']);self.d['teachers'][0]['status']='REVIEW';p=prepare_grade(self.d,self.c,self.bg);self.assertIn('T1',p['unverified_teacher_ids'])
 def test_special_scope_strict_and_scenario(self):
  self.d['subjects'].append(dict(id='HD02:NONE',base='HD02',name='Chào cờ / Sinh hoạt chủ nhiệm'))
  self.d['pending_special']=[dict(class_id='C8',subject_id='HD02:NONE',subject='Chào cờ / Sinh hoạt chủ nhiệm',count=1)]
  r=self.runok();self.assertEqual(r['unscheduled_special'],1);self.assertFalse(any(l.get('is_special') for l in r['lessons']))
  self.c.update(special_mode='SCENARIO',special_scenario=dict(enabled=True,activity_ids=['SP_C8_HD02'],teacher_required=False,scheduling_policy='independent',assumption_label='Technical fixture only'))
  r=solve_grade(self.d,self.c,self.bg);self.assertEqual(r['placed'],3);self.assertEqual(r['scenario_placed'],1);self.assertEqual(r['unscheduled_special'],1);self.assertTrue(r['simulation']);self.assertFalse(r['official_complete'])
 def test_collective_special_fixed_works_in_selected_grade(self):
  self.d['subjects'].append(dict(id='HD02:NONE',base='HD02',name='Chào cờ / Sinh hoạt chủ nhiệm'));self.d['pending_special']=[dict(class_id='C8',subject_id='HD02:NONE',subject='Chào cờ / Sinh hoạt chủ nhiệm',count=1)]
  self.c.update(special_overrides=[dict(activity_id='SP_C8_HD02',validation_status='VERIFIED',verification_note='Synthetic test rule',teacher_required=False,scheduling_policy='collective',shared_teacher_group='G')],fixed=[dict(assignment='SPECIAL:G',day=1,shift='pm',period=0)])
  r=solve_grade(self.d,self.c,self.bg);self.assertEqual(r['placed'],4);self.assertEqual(r['unscheduled_special'],0);self.assertTrue(any(l['assignment']=='SPECIAL:G' and l['period']==0 for l in r['lessons']))
 def test_unknown_rules_and_locked_fixed_not_ignored(self):
  self.c['special_overrides']=[dict(activity_id='UNKNOWN')]
  with self.assertRaises(ValueError):prepare_grade(self.d,self.c,self.bg)
  self.c['special_overrides']=[];self.c['fixed']=[dict(assignment='UNKNOWN',day=0,shift='am',period=0)]
  with self.assertRaises(ValueError):prepare_grade(self.d,self.c,self.bg)
  self.c['fixed']=[dict(assignment='A9',day=1,shift='am',period=0)]
  with self.assertRaisesRegex(ValueError,'lịch khóa'):prepare_grade(self.d,self.c,self.bg)
 def test_source_unknown_is_not_infeasible(self):
  d=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');bg=json.loads((ROOT/'data/LOCKED_BACKGROUND_SOURCE.json').read_text());r=solve_grade(d,dict(time_limit=.001,allow_incomplete_background=True,background_assumption='Technical timeout test'),bg,previous=[]);self.assertEqual(r['status'],'UNKNOWN');self.assertEqual(r['lessons'],[]);self.assertIsNone(r['conflicts'])
if __name__=='__main__':unittest.main()
