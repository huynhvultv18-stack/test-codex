"""Recompute every A/B schedule, input hash and all independent metrics."""
import json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from smart_tkb.validation import verify_schedule,metrics,config_with_defaults
R=Path(__file__).resolve().parent.parent;checks=[]
for report,folder in [('AB_BENCHMARK.json','ab'),('AB_LNS_BENCHMARK.json','ab_lns')]:
 x=json.loads((R/'reports'/report).read_text())
 for run in x['runs']:
  path=R/run['file'];r=json.loads(path.read_text());inp=R/'reports'/folder/(run['mode']+'_'+run['profile']+'_input.json');a=json.loads(inp.read_text());assert hashlib.sha256(inp.read_bytes()).hexdigest()==run['input_sha256']
  if r['lessons']:
   v=verify_schedule(a['data'],a['config'],r['lessons']);assert v['valid'] and v['placed']==972 and v['conflicts']==0,v
   m=metrics(a['data'],config_with_defaults(a['config']),r['lessons'],a['previous']);assert m==r['metrics'],(m,r['metrics'])
   assert not r['global_optimal_proven']
   checks.append(dict(file=run['file'],status=r['status'],valid=True,placed=v['placed'],conflicts=v['conflicts'],metrics_match=True))
  else:
   assert r['status']=='INFEASIBLE' and r['placed']==0 and r['conflicts'] is None and r['metrics'] is None
   assert any('GV015' in line and '40' in line and '30' in line for line in r['diagnostics'])
   checks.append(dict(file=run['file'],status=r['status'],proof='GV015 40>30',no_schedule=True))
(R/'reports/AB_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(dict(result='PASS',checks=checks),ensure_ascii=False,indent=2));print('PASS',len(checks),'A/B results independently checked; counts, conflicts, metrics and input hashes')
