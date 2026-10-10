"""Reproducible 37-class technical benchmark, never real-school acceptance."""
import argparse
import copy
import json
import os
import platform
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from smart_tkb.importer import read_pccm
from smart_tkb.solver import solve

def main():
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=30);p.add_argument('--local',action='store_true');args=p.parse_args()
    root=Path(__file__).resolve().parent.parent;data=read_pccm(root/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');cases=[]
    for mode in ['morning','both','mixed']:
        working=copy.deepcopy(data)
        for i,c in enumerate(working['classes']):c['shift']='am' if i%2==0 else 'pm'
        config=dict(mode=mode,days=6,periods=5,max_class_session=5,max_teacher_session=5,time_limit=args.seconds,workers=4,seed=17,technical_only=True)
        result=solve(working,config,progress=lambda s:print(mode,s,flush=True))
        (root/'reports'/f'{mode}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        cases.append(dict(mode=mode,config=config,class_shifts={c['id']:c['shift'] for c in working['classes']},result={k:v for k,v in result.items() if k!='lessons'}))
        print(mode,result['status'],result['placed'],result['metrics'],flush=True)
    report=dict(python=platform.python_version(),platform=platform.platform(),cpu_count=os.cpu_count(),ortools=__import__('ortools').__version__,cases=cases)
    (root/'reports/benchmark.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    if args.local:
        previous=json.loads((root/'reports/both.json').read_text(encoding='utf-8'))
        if previous['lessons']:
            config=dict(mode='both',time_limit=12,workers=4,priorities=['changes','gaps','visits','distribution','concentration','preferences'])
            result=solve(data,config,previous['lessons'],dict(classes=['C06A01']),progress=lambda s:print('local',s,flush=True))
            (root/'reports/local_37.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
            print('local',result['status'],result['metrics'],flush=True)

if __name__=='__main__':main()
