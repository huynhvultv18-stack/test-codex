"""Grade-only benchmark. Never calls the full-school solver."""
import copy,json,time,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from smart_tkb.importer import read_pccm
from smart_tkb.grade import solve_grade,prepare_grade,verify_grade,grade_config,schedule_hash
from test_grade import fixture
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'reports/grade8';OUT.mkdir(exist_ok=True)
d=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');bg=json.loads((ROOT/'data/LOCKED_BACKGROUND_SOURCE.json').read_text());source_hash=schedule_hash(bg['lessons']);runs=[]
def record(name,data,c,bg,prev=None,scope=None):
 print('RUN',name,flush=True);r=solve_grade(data,c,bg,prev,scope=scope);p=prepare_grade(data,c,bg)
 if r['lessons']:
  assert verify_grade(p,r['lessons'],r['locked_lessons'])['valid'];assert r['locked_hash_before']==r['locked_hash_after']
  assert set(r['model_scope']['class_ids'])=={x['id'] for x in p['target_data']['classes']}
  assert all(x['class_id'] in r['model_scope']['class_ids'] for x in r['lessons'])
 filename=OUT/(name+'.json');filename.write_text(json.dumps(dict(config=p['config'],result=r),ensure_ascii=False,indent=2))
 summary={k:r.get(k) for k in ['status','target_grade','class_count','required','placed','scenario_placed','unscheduled_special','conflicts','known_cross_grade_conflicts','cross_grade_conflicts','school_conflicts','metrics','elapsed_seconds','phases','proven_priorities','conditional_optimal_priorities','grade_optimal_proven','global_optimal_proven','optimality_scope','simulation','grade_scheduling','cross_grade_conflict','locked_grades','locked_hash_before','locked_hash_after','model_scope']}
 summary.update(name=name,config=p['config'],file=str(filename.relative_to(ROOT)),background_complete=p['background_context']['complete']);runs.append(summary);print(name,r['status'],r['placed'],r.get('metrics'),flush=True);return r
base=dict(time_limit=30,workers=4,seed=17,allow_incomplete_background=True,background_assumption='Saved V3.1 technical academic background has 738 periods; 84 background special periods remain unknown; teacher IDs unverified')
record('default_strict_blocked',d,{},bg)
cold=record('both_cold_s17_t30',d,base,bg,[])
assert cold['placed']==234 and cold['grade_scheduling']=='PASS'
warm=record('both_warm_s17_t30',d,{**base,'search_mode':'lns'},bg,cold['lessons'])
assert tuple(warm['metrics'][k] for k in grade_config()['priorities'])<=tuple(cold['metrics'][k] for k in grade_config()['priorities'])
record('both_local_C08A01_t10',d,{**base,'time_limit':10,'search_mode':'lns'},bg,warm['lessons'],dict(classes=['C08A01']))
record('morning_cold_s17_t10',d,{**base,'mode':'morning','time_limit':10},bg,[])
record('mixed_am_cold_s17_t10',d,{**base,'mode':'mixed','time_limit':10},bg,[])
# Actual afternoon-only capacity is 24 versus 26 PCCM per class: keep INFEASIBLE.
mixed=copy.deepcopy(d)
for cl in mixed['classes']:
 if cl['grade']==8 and cl['id']=='C08A09':cl['shift']='pm'
record('mixed_pm_capacity_infeasible',mixed,{**base,'mode':'mixed','time_limit':2},bg,[])
fd,fc,fb=fixture();record('complete_background_synthetic_fixture',fd,fc,fb)
assert schedule_hash(bg['lessons'])==source_hash
(ROOT/'reports/GRADE8_BENCHMARK.json').write_text(json.dumps(dict(runs=runs,source_background_hash=source_hash,real_windows_test=False,production_ready=False,comparison_scope='Grade-only; no whole-school solve or cross-size A/B comparison'),ensure_ascii=False,indent=2))
