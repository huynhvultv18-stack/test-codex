"""Sequential paired V3/V3.1 runs: identical PCCM, seeds, workers and budgets."""
import json,copy,subprocess,sys,platform,os,hashlib,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PROFILES=[dict(name='cold_s17_w4_t30',seed=17,workers=4,time_limit=30,warm=False),dict(name='warm_s23_w4_t45',seed=23,workers=4,time_limit=45,warm=True),dict(name='warm_s29_w1_t30',seed=29,workers=1,time_limit=30,warm=True)]
CODE='''import json,sys
from smart_tkb.solver import solve
from smart_tkb.validation import verify_schedule
x=json.load(open(sys.argv[1],encoding="utf-8"))
r=solve(x["data"],x["config"],x["previous"])
r["independent_check"]=verify_schedule(x["data"],x["config"],r["lessons"]) if r["lessons"] else None
json.dump(r,open(sys.argv[2],"w",encoding="utf-8"),ensure_ascii=False,indent=2)
'''
def main():
 data=json.loads((ROOT/'data/pccm_normalized.json').read_text())
 for i,c in enumerate(data['classes']):c['shift']='am' if i%2==0 else 'pm'
 baseline=ROOT/'baseline_v3'
 report=dict(platform=platform.platform(),python=platform.python_version(),cpu_count=os.cpu_count(),ortools=__import__('ortools').__version__,source_sha256=data['source_sha256'],baseline_zip_sha256='7374bde2f3ac23b4fdd1735e606c808b0dc9efc778beee44b4e10038b39a543f',profiles=PROFILES,runs=[],design='Sequential paired runs, identical common warm incumbent, no competing solver jobs; runtime includes model build. V3.1 phase allocation and redundant cuts are the treatment.')
 start=time.time()
 for mode in ['morning','both','mixed']:
  profiles=PROFILES[:1] if mode=='morning' else PROFILES
  for profile in profiles:
   previous=json.loads((baseline/('reference_'+mode+'.json')).read_text())['lessons'] if profile['warm'] else []
   config=dict(mode=mode,days=6,periods=5,max_class_session=5,max_teacher_session=5,technical_only=True,seed=profile['seed'],workers=profile['workers'],time_limit=profile['time_limit'])
   label=mode+'_'+profile['name'];inputfile=ROOT/'reports/fair'/(label+'_input.json')
   inputfile.write_text(json.dumps(dict(data=data,config=config,previous=previous),ensure_ascii=False))
   for version,cwd in [('V3',ROOT/'baseline_v3'),('V3.1',ROOT)]:
    out=ROOT/'reports/fair'/(label+'_'+version+'.json')
    env=dict(os.environ);env.pop('PYTHONPATH',None)
    subprocess.run([sys.executable,'-c',CODE,str(inputfile),str(out)],cwd=cwd,env=env,check=True,timeout=profile['time_limit']+120)
    r=json.loads(out.read_text());report['runs'].append(dict(version=version,mode=mode,profile=profile['name'],config=config,warm=profile['warm'],warm_sha256=hashlib.sha256(json.dumps(previous,sort_keys=True).encode()).hexdigest(),result={k:v for k,v in r.items() if k not in ['lessons','teacher_visits','teacher_visit_lower_bounds','initial_quality_scores','quality_scores']},file=str(out.relative_to(ROOT))))
    if r['lessons']:assert r['independent_check']['valid'],r['independent_check']
    (ROOT/'reports/FAIR_BENCHMARK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(version,label,r['status'],r['placed'],r['metrics'],flush=True)
 report['total_seconds']=round(time.time()-start,3)
 (ROOT/'reports/FAIR_BENCHMARK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
