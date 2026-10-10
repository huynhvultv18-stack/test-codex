"""Recompute evidence independently; no CP-SAT solve, no 37-class model."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent));sys.path.insert(0,str(Path(__file__).resolve().parent))
from smart_tkb.grade import prepare_grade,verify_grade,schedule_hash
from smart_tkb.validation import metrics,signature
from smart_tkb.quality import features
from smart_tkb.importer import read_pccm
from test_grade import fixture
R=Path(__file__).resolve().parent.parent
book=read_pccm(R/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');background=json.loads((R/'data/LOCKED_BACKGROUND_SOURCE.json').read_text());benchmark=json.loads((R/'reports/GRADE8_BENCHMARK.json').read_text());count=0;details=[]
for run in benchmark['runs']:
 x=json.loads((R/run['file']).read_text());c=x['config'];r=x['result'];data,bg=(fixture()[0],fixture()[2]) if run['name']=='complete_background_synthetic_fixture' else (book,background)
 p=prepare_grade(data,c,bg)
 if not r['lessons']:
  assert r['conflicts'] is None and r['school_conflicts'] is None;details.append(dict(run=run['name'],status=r['status'],no_false_conflict_claim=True));continue
 assert verify_grade(p,r['lessons'],r['locked_lessons'])['valid'];assert r['locked_lessons']==p['locked'];assert schedule_hash(r['locked_lessons'])==r['locked_hash_before']==r['locked_hash_after']
 assert r['model_scope']['locked_lesson_decision_variables']==0 and set(r['model_scope']['class_ids'])=={cl['id'] for cl in p['target_data']['classes']}
 previous=[]
 if run['name']=='both_warm_s17_t30':previous=json.loads((R/'reports/grade8/both_cold_s17_t30.json').read_text())['result']['lessons']
 if run['name']=='both_local_C08A01_t10':
  previous=json.loads((R/'reports/grade8/both_warm_s17_t30.json').read_text())['result']['lessons'];assert {signature(l) for l in previous if l['class_id']!='C08A01'}=={signature(l) for l in r['lessons'] if l['class_id']!='C08A01'};assert r['optimality_scope']=='local_grade_with_frozen_background';assert not r['grade_optimal_proven']
 m=metrics(p['working'],p['config'],r['lessons'],previous,background=p['locked']);q=features(p['working'],p['config'],r['lessons'])
 assert all(m[k]==r['metrics'][k] for k in m),(run['name'],m,r['metrics']);baseline=metrics(p['working'],p['config'],[],background=p['locked'])['visits'];assert r['metrics']['added_visits']==m['visits']-baseline
 vals={**m,'distribution':q['distribution_weighted'],'concentration':q['concentration_weighted']}
 for phase in r['phases']:
  if phase['name'] in vals and phase['status'] in ['OPTIMAL','PROVEN_LOWER_BOUND']:
   assert round(phase['objective'])==vals[phase['name']]*p['config']['objective_settings'][phase['name']]['weight']
 assert not r['global_optimal_proven'] and not r['production_ready']
 if not p['background_context']['complete']:assert r['cross_grade_conflicts'] is None and r['school_conflicts'] is None and r['cross_grade_conflict']=='BLOCKED'
 count+=1;details.append(dict(run=run['name'],status=r['status'],placed=r['placed'],metrics='MATCH',frozen_hash='MATCH',within_grade_conflicts=0,known_cross_grade_conflicts=0,cross_grade_fully_verified=p['background_context']['complete']))
(R/'reports/GRADE8_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(dict(result='PASS',feasible_runs_verified=count,details=details),ensure_ascii=False,indent=2));print('PASS',count,'complete grade schedules independently verified; locked hashes,counts,resources,metrics,proof scopes checked')
