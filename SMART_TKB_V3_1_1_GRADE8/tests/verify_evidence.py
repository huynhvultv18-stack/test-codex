"""Verify every recorded fair schedule with the current independent checker."""
import json,hashlib,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from smart_tkb.validation import verify_schedule,metrics,config_with_defaults
ROOT=Path(__file__).resolve().parent.parent
report=json.loads((ROOT/'reports/FAIR_BENCHMARK.json').read_text());checks=[]
for run in report['runs']:
 result=json.loads((ROOT/run['file']).read_text());inputfile=ROOT/'reports/fair'/(run['mode']+'_'+run['profile']+'_input.json');inp=json.loads(inputfile.read_text())
 if not result['lessons']:
  assert result['status']=='INFEASIBLE' and result['placed']==0;checks.append(dict(file=run['file'],status='NO_SCHEDULE_CAPACITY_PROOF'));continue
 v=verify_schedule(inp['data'],inp['config'],result['lessons']);assert v['valid'],v
 m=metrics(inp['data'],config_with_defaults(inp['config']),result['lessons'],inp['previous']);assert m==result['metrics'],(m,result['metrics'])
 checks.append(dict(file=run['file'],valid=True,required=v['required'],placed=v['placed'],conflicts=v['conflicts'],metrics_match=True,sha256=hashlib.sha256((ROOT/run['file']).read_bytes()).hexdigest()))
(ROOT/'reports/INDEPENDENT_EVIDENCE_CHECK.json').write_text(json.dumps(dict(result='PASS',checks=checks),ensure_ascii=False,indent=2))
print('PASS',len(checks),'recorded fair results independently verified; all metrics recomputed')
