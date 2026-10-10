"""Measured selected-grade benchmarks, no whole-school optimization."""
import copy,json,time,sys,platform
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
from smart_tkb.importer import read_pccm
from smart_tkb.grade import solve_grade,prepare_grade,verify_grade,schedule_hash
from smart_tkb.sessions import reference_config
OUT=ROOT/'reports/sessions';OUT.mkdir(exist_ok=True)
d=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');bg=json.loads((ROOT/'data/LOCKED_BACKGROUND_SOURCE.json').read_text());hash_before=schedule_hash(bg['lessons']);runs=[]
base=dict(target_grade=8,mode='both',time_limit=30,workers=4,seed=17,session_config=reference_config(),allow_incomplete_background=True,background_assumption='Technical conditional PCCM: 26 grade8 teacher IDs unverified; 84 frozen-background special periods unknown; no official acceptance')
variants=[]
u=copy.deepcopy(base);u['session_config']['week']=[dict(am=5,pm=4) for _ in range(6)]+[dict(am=0,pm=0)];variants.append(('uniform5am4pm',u))
v=copy.deepcopy(base);v['session_config']['week']=[dict(am=5,pm=4),dict(am=4,pm=3),dict(am=5,pm=2),dict(am=3,pm=4),dict(am=5,pm=1),dict(am=4,pm=2),dict(am=0,pm=0)];variants.append(('variable_days',v))
variants.append(('reference_rest_sessions',copy.deepcopy(base)))
x=copy.deepcopy(base)
for i,cl in enumerate(c for c in d['classes'] if c['grade']==8):
 w=copy.deepcopy(reference_config()['week']);w[i%6]['am']=4 if w[i%6]['am']==5 else 3
 if i%2:w[(i+1)%5]['pm']=2
 x['session_config']['class_weeks'][cl['id']]=w
variants.append(('different_classes',x))
for mode in ['morning','mixed']:variants.append(('reference_'+mode,{**copy.deepcopy(base),'mode':mode,'time_limit':10}))
blocked={**copy.deepcopy(base),'allow_incomplete_background':False,'background_assumption':''};variants.append(('incomplete_background_default_blocked',blocked))
small=copy.deepcopy(base);small['session_config']['week']=[dict(am=1,pm=0) for _ in range(6)]+[dict(am=0,pm=0)];variants.append(('over_capacity_infeasible',small))
for name,c in variants:
 print('RUN',name,flush=True);started=time.monotonic();r=solve_grade(d,c,bg,previous=[]);wall=time.monotonic()-started;p=prepare_grade(d,c,bg)
 if r['lessons']:
  v=verify_grade(p,r['lessons'],r['locked_lessons']);assert v['valid'],v;assert r['locked_hash_before']==r['locked_hash_after'];assert set(r['model_scope']['class_ids'])=={cl['id'] for cl in p['target_data']['classes']};assert r['model_scope']['locked_lesson_decision_variables']==0
  # Direct calendar audit against raw user counts, independent of CP output flags.
  for row in r['lessons']:
   w=c['session_config']['class_weeks'].get(row['class_id'],c['session_config']['week']);assert w[row['day']][row['shift']]>0;assert row['period']+row.get('length',1)<=w[row['day']][row['shift']]
 payload=dict(config=p['config'],result=r);(OUT/(name+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2))
 runs.append(dict(name=name,config=p['config'],file='reports/sessions/'+name+'.json',status=r['status'],required=r['required'],placed=r['placed'],capacity=p['session_analysis']['capacity'],weekly_slots=p['session_analysis']['weekly_slots'],weekly_sessions=p['session_analysis']['weekly_sessions'],rest_sessions=p['session_analysis']['rest_sessions'],conflicts=r['conflicts'],known_cross_grade_conflicts=r.get('known_cross_grade_conflicts'),school_conflicts=r.get('school_conflicts'),gaps=(r['metrics'] or {}).get('gaps'),visits=(r['metrics'] or {}).get('visits'),elapsed_seconds=r['elapsed_seconds'],wall_seconds=round(wall,3),diagnostics=r['diagnostics'],locked_hash_before=r['locked_hash_before'],locked_hash_after=r['locked_hash_after'],zero_period_status=r['zero_period_status'],grade_optimal_proven=r['grade_optimal_proven'],global_optimal_proven=False))
 print(name,r['status'],r['placed'],r.get('metrics'),flush=True)
 if name=='reference_rest_sessions' and r['lessons']:
  (ROOT/'data/EXAMPLE_SESSION_TECHNICAL_BACKUP.json').write_text(json.dumps(dict(version='3.1.2-session',data=d,config=p['config'],background=bg,result=r),ensure_ascii=False,indent=2))
assert schedule_hash(bg['lessons'])==hash_before
(ROOT/'reports/SESSION_BENCHMARK.json').write_text(json.dumps(dict(platform=platform.platform(),python=platform.python_version(),source_background_hash=hash_before,scope='Grade8 only; frozen grades6/7/9; Linux measurement; Windows untested',runs=runs,production_ready=False),ensure_ascii=False,indent=2))
