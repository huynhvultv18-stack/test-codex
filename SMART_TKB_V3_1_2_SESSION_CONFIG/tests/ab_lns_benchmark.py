"""A/B against immutable delivered V3.1; sequential, fresh processes, common warm start."""
import json,subprocess,sys,platform,os,hashlib,time
from pathlib import Path
R=Path(__file__).resolve().parent.parent
PROFILES=[dict(name='warm_lns_s17_w4_t30',seed=17,workers=4,time_limit=30,warm=True,search_mode='lns'),dict(name='warm_lns_s23_w4_t30',seed=23,workers=4,time_limit=30,warm=True,search_mode='lns')]
CODE='''import json,sys,time,resource
from ortools.sat.python import cp_model
from smart_tkb.solver import solve
from smart_tkb.validation import verify_schedule
calls=[];ready=[];begin=None
original_validate=cp_model.CpModel.validate
original_solve=cp_model.CpSolver.solve
def validate(model):
 value=original_validate(model)
 ready.append(dict(seconds=time.monotonic()-begin,variables=len(model.proto.variables),constraints=len(model.proto.constraints)))
 return value
def instrument(solver,model,*args,**kwargs):
 before=time.monotonic();status=original_solve(solver,model,*args,**kwargs)
 calls.append(dict(start_seconds=before-begin,seconds=time.monotonic()-before,status=solver.status_name(status),objective=solver.objective_value if status in (cp_model.OPTIMAL,cp_model.FEASIBLE) else None,best_bound=solver.best_objective_bound,variables=len(model.proto.variables),constraints=len(model.proto.constraints)))
 return status
cp_model.CpModel.validate=validate;cp_model.CpSolver.solve=instrument
x=json.load(open(sys.argv[1],encoding="utf-8"));begin=time.monotonic();result=solve(x['data'],x['config'],x['previous']);wall=time.monotonic()-begin
peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
result['independent_check']=verify_schedule(x['data'],x['config'],result['lessons']) if result['lessons'] else None
result['observed_performance']=dict(wall_seconds=wall,peak_rss_mb=peak,model_ready=ready,solver_calls=calls,first_cp_solution_seconds=next((z['start_seconds']+z['seconds'] for z in calls if z['status'] in ('OPTIMAL','FEASIBLE')),None))
json.dump(result,open(sys.argv[2],"w",encoding="utf-8"),ensure_ascii=False,indent=2)
'''
def main():
 baseline=R/'baseline_v31';assert (baseline/'smart_tkb/solver.py').exists()
 data=json.loads((R/'data/pccm_normalized.json').read_text())
 for i,c in enumerate(data['classes']):c['shift']='am' if i%2==0 else 'pm'
 f=dict(platform=platform.platform(),python=platform.python_version(),ortools=__import__('ortools').__version__,logical_cpu=os.cpu_count(),baseline_zip_sha256='a94c50bbe617c72210412ff5fa9b491d1bc2691fd6502fe7a35436ece04029e9',source_sha256=data['source_sha256'],profiles=PROFILES,runs=[],method='Fresh subprocess per run; sequential; identical inputs/config/seed/workers/time/warm incumbent. RSS kernel high water mark in MiB. Model-ready instrumented identically at validate(). Treatment is solver code only, no configuration advantage.')
 start=time.monotonic()
 for mode in ['both','mixed']:
  profiles=PROFILES[:1] if mode=='morning' else PROFILES
  for p in profiles:
   previous=json.loads((baseline/('reference_'+mode+'.json')).read_text())['lessons'] if p['warm'] else []
   c=dict(mode=mode,days=6,periods=5,max_class_session=5,max_teacher_session=5,technical_only=True,time_limit=p['time_limit'],workers=p['workers'],seed=p['seed'],search_mode=p['search_mode'])
   name=mode+'_'+p['name'];inp=R/'reports/ab_lns'/(name+'_input.json');inp.write_text(json.dumps(dict(data=data,config=c,previous=previous),ensure_ascii=False))
   for version,cwd in [('A_BASELINE',baseline),('B_OPTIMIZED',R)]:
    out=R/'reports/ab_lns'/(name+'_'+version+'.json');env=dict(os.environ);env.pop('PYTHONPATH',None)
    subprocess.run([sys.executable,'-c',CODE,str(inp),str(out)],cwd=cwd,env=env,check=True,timeout=p['time_limit']+90)
    r=json.loads(out.read_text());assert not r['lessons'] or r['independent_check']['valid'],r.get('independent_check')
    f['runs'].append(dict(version=version,mode=mode,profile=p['name'],config=c,warm=p['warm'],file=str(out.relative_to(R)),input_sha256=hashlib.sha256(inp.read_bytes()).hexdigest(),result={k:v for k,v in r.items() if k not in ['lessons','initial_quality_scores','quality_scores','teacher_visits','teacher_visit_lower_bounds']}))
    f['elapsed_seconds']=round(time.monotonic()-start,3);(R/'reports/AB_LNS_BENCHMARK.json').write_text(json.dumps(f,ensure_ascii=False,indent=2));print(version,name,r['status'],r['metrics'],r['observed_performance']['peak_rss_mb'],flush=True)
if __name__=='__main__':main()
