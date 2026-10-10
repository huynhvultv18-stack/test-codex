"""Explicit technical simulation; this does not verify missing school rules."""
import json,copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from smart_tkb.importer import read_pccm
from smart_tkb.special import inventory
from smart_tkb.solver import solve
from smart_tkb.validation import verify_schedule,signature
ROOT=Path(__file__).resolve().parent.parent
def main():
 data=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');cases=[]
 for i,c in enumerate(data['classes']):c['shift']='am' if i%2==0 else 'pm'
 ids=[a['activity_id'] for a in inventory(data)]
 for mode in ['morning','both','mixed']:
  c=dict(mode=mode,time_limit=30,workers=4,seed=17,special_mode='SCENARIO',special_scenario=dict(enabled=True,activity_ids=ids,teacher_required=False,teacher_id=None,scheduling_policy='independent',assumption_label='FIXTURE KỸ THUẬT: người viết test chọn 111 hoạt động độc lập không cần GV; không phải quy tắc nhà trường đã xác minh.'))
  r=solve(data,c,progress=lambda s:print('scenario',mode,s,flush=True))
  if r['lessons']:assert verify_schedule(data,c,r['lessons'])['valid']
  assert not r['official_complete'] and not r['data_accepted'];assert r['special_report']['verified']==0 and r['special_report']['pending']==111
  (ROOT/'reports'/f'SCENARIO_{mode}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));cases.append(dict(mode=mode,config=c,result={k:v for k,v in r.items() if k not in ['lessons','quality_scores','initial_quality_scores','teacher_visits','teacher_visit_lower_bounds']}))
  print(mode,r['status'],r['placed'],r['scenario_placed'],r['metrics'],flush=True)
 # 37-class local reoptimization keeps every row outside C06A01 frozen.
 prev=json.loads((ROOT/'reports/both.json').read_text())['lessons'];c=dict(mode='both',time_limit=10,workers=4,seed=17,priorities=['changes','gaps','visits','distribution','concentration','preferences'])
 r=solve(data,c,prev,dict(classes=['C06A01']));v=verify_schedule(data,c,r['lessons'],prev,dict(classes=['C06A01']));assert v['valid'];assert r['metrics']['changes']==0 and not r['global_optimal_proven']
 (ROOT/'reports/local_37.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));cases.append(dict(mode='both_local_37',config=c,result={k:v for k,v in r.items() if k not in ['lessons','quality_scores','initial_quality_scores','teacher_visits','teacher_visit_lower_bounds']}))
 (ROOT/'reports/EXTENDED_BENCHMARK.json').write_text(json.dumps(dict(cases=cases,official_eligible_special=0,simulation_is_not_acceptance=True),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
