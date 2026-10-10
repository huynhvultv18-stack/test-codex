"""Measured grade8 A/B: identical JSON input/budget/seed/workers, serial same host.
Baseline ignores teacher_time extension; candidate honors documented new priority policy.
Compare shared gaps/visits prefix and raw indicators; never compare scalar objectives.
"""
import argparse,copy,hashlib,json,os,platform,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
from smart_tkb.importer import read_pccm
from smart_tkb.grade import prepare_grade,solve_grade,schedule_hash
from smart_tkb.teacher_time import evaluate
from smart_tkb.conflicts import check
p=argparse.ArgumentParser();p.add_argument('--baseline',required=True);args=p.parse_args();base=Path(args.baseline).resolve();assert (base/'smart_tkb/solver.py').exists();assert base!=ROOT
OUT=ROOT/'reports/time_conflict';OUT.mkdir(exist_ok=True);d=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');bg=json.loads((ROOT/'data/LOCKED_BACKGROUND_SOURCE.json').read_text());runs=[]
old=ROOT/'reports/historical_v312/sessions';cases=[]
for seed in [17,23]:
 x=json.loads((old/'reference_rest_sessions.json').read_text());c=x['config'];c.update(time_limit=20,seed=seed,workers=4,teacher_time=dict(enabled=True,mode='BALANCED'))
 cases.append(('ab_reference_s'+str(seed),dict(data=d,config=c,background=bg,previous=x['result']['lessons']),True))
for mode in ['morning','mixed']:
 x=json.loads((old/('reference_'+mode+'.json')).read_text());c=x['config'];c.update(time_limit=10,seed=17,workers=4,teacher_time=dict(enabled=True,mode='BALANCED'));cases.append(('profile_'+mode,dict(data=d,config=c,background=bg,previous=x['result']['lessons']),False))
for profile in ['FAST','PROVE_OPTIMAL']:
 x=json.loads((old/'reference_rest_sessions.json').read_text());c=x['config'];c.update(time_limit=10,seed=17,workers=4,teacher_time=dict(enabled=True,mode=profile,waiting_enabled=True,seeds=[17,23]));cases.append(('profile_'+profile.lower(),dict(data=d,config=c,background=bg,previous=x['result']['lessons']),False))
for name,problem,ab in cases:
 inputfile=OUT/(name+'_input.json');inputfile.write_text(json.dumps(problem,ensure_ascii=False,indent=2));ih=hashlib.sha256(inputfile.read_bytes()).hexdigest()
 for label,code in ([('A_V312',base),('B_V313',ROOT)] if ab else [('B_V313',ROOT)]):
  print('RUN',name,label,flush=True);output=OUT/(name+'_'+label+'.json');env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
  subprocess.run([sys.executable,str(ROOT/'tests/time_conflict_worker.py'),'--code-root',str(code),'--input',str(inputfile),'--output',str(output)],check=True,env=env)
  payload=json.loads(output.read_text());r=payload['result'];pp=prepare_grade(d,payload['config'],bg);before=evaluate(pp['working'],pp['config'],problem['previous'],pp['locked']);after=evaluate(pp['working'],pp['config'],r['lessons'],pp['locked']);post=check(d,payload['config'],bg,r['lessons']);assert post['status']=='INCOMPLETE' and post['known_conflicts']==0;assert r['placed']==234;assert r['locked_lessons']==pp['locked'];assert r['locked_hash_before']==r['locked_hash_after'];assert set(r['model_scope']['class_ids'])=={cl['id'] for cl in d['classes'] if cl['grade']==8};assert r['model_scope']['locked_lesson_decision_variables']==0
  runs.append(dict(name=name,variant=label,input_sha256=ih,input_file=str(inputfile.relative_to(ROOT)),output_file=str(output.relative_to(ROOT)),budget_seconds=problem['config']['time_limit'],workers=4,seed=problem['config']['seed'],required=r['required'],placed=r['placed'],before=before['totals'],after=after['totals'],waiting_kind=after['waiting_kind'],known_conflicts=post['known_conflicts'],school_conflicts=post['school_conflicts'],post_check=post['status'],warnings=post['counts']['data_warnings'],solver_status=r['status'],phases=r['phases'],proven_prefix=r['proven_priorities'],conditional_priorities=r.get('conditional_optimal_priorities',[]),elapsed_seconds=r['elapsed_seconds'],wall_seconds=payload['wall_seconds'],proof_scope=r['optimality_scope'],selected_scope_optimal_proven=r.get('selected_scope_optimal_proven',False),global_optimal_proven=False,locked_unchanged=True))
  if name=='ab_reference_s17' and label=='B_V313':(ROOT/'data/EXAMPLE_TIME_CONFLICT_TECHNICAL_BACKUP.json').write_text(json.dumps(dict(version='3.1.3-time-conflict',data=d,config=pp['config'],background=bg,result=r,draft=True,production_ready=False),ensure_ascii=False,indent=2))
# Default block and hard capacity infeasibility stay explicit.
x=copy.deepcopy(cases[0][1]);x['config'].update(allow_incomplete_background=False,background_assumption='');r=solve_grade(d,x['config'],bg,previous=[]);assert r['status']=='BLOCKED'
y=copy.deepcopy(cases[0][1]);y['config']['session_config']['week']=[dict(am=1,pm=0)]*6+[dict(am=0,pm=0)];r2=solve_grade(d,y['config'],bg,previous=[]);assert r2['status']=='INFEASIBLE'
(OUT/'blocked_infeasible.json').write_text(json.dumps(dict(blocked=r,infeasible=r2),ensure_ascii=False,indent=2))
report=dict(platform=platform.platform(),python=platform.python_version(),ortools=__import__('ortools').__version__,machine=platform.machine(),logical_cpus=os.cpu_count(),source_classes=len(d['classes']),target_grade=8,target_classes=9,background_sha256=schedule_hash(prepare_grade(d,cases[0][1]['config'],bg)['locked']),runs=runs,negative_controls=dict(default='BLOCKED',over_capacity='INFEASIBLE'),comparison_policy='Identical input JSON, hardware and serial wall budget; new default has days/waiting/fragmentation/fairness beyond baseline6 goals. Compare common gaps/visits prefix and measured indicators, not whole lex vectors across policies. Independent small exhaustive oracle proves new full vector separately.',windows_accepted=False,data_accepted=False,production_ready=False)
(ROOT/'reports/TIME_CONFLICT_BENCHMARK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('PASS',len(runs),'serial measurements',flush=True)
