"""Isolated A/B worker: import only the chosen code tree; never mutate baseline."""
import argparse,json,sys,time
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--code-root',required=True);p.add_argument('--input',required=True);p.add_argument('--output',required=True);a=p.parse_args();sys.path.insert(0,a.code_root)
from smart_tkb.grade import solve_grade,prepare_grade
x=json.loads(Path(a.input).read_text());start=time.monotonic();r=solve_grade(x['data'],x['config'],x['background'],previous=x['previous']);wall=time.monotonic()-start
Path(a.output).write_text(json.dumps(dict(config=prepare_grade(x['data'],x['config'],x['background'])['config'],result=r,wall_seconds=round(wall,3)),ensure_ascii=False,indent=2));print(r['status'],r['placed'],r.get('metrics'),flush=True)
