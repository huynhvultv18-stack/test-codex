"""Independent evidence audit: no solving, recompute calendars/occupancy/metrics."""
import json,sys,io,csv
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
from smart_tkb.importer import read_pccm
from smart_tkb.grade import prepare_grade,verify_grade,schedule_hash
from smart_tkb.grade_exchange import import_grade
from smart_tkb.validation import metrics
from smart_tkb.quality import features
from smart_tkb.sessions import analyze
D=read_pccm(ROOT/'SOURCE/PCCM_INPUT_CODEX_5_NHOM.xlsx');BG=json.loads((ROOT/'data/LOCKED_BACKGROUND_SOURCE.json').read_text());b=json.loads((ROOT/'reports/SESSION_BENCHMARK.json').read_text());audits=[]
for run in b['runs']:
 payload=json.loads((ROOT/run['file']).read_text());c=payload['config'];r=payload['result'];p=prepare_grade(D,c,BG);assert schedule_hash(p['locked'])==r['locked_hash_before']==r['locked_hash_after'];assert {cl['grade'] for cl in p['working']['classes']}=={8}
 a=analyze(p['working'],p['config'],p['locked']);assert a['capacity']==run['capacity'];assert a['rest_sessions']==run['rest_sessions']
 if r['lessons']:
  v=verify_grade(p,r['lessons'],r['locked_lessons']);assert v['valid'];counts=Counter();occupied=Counter();occ=defaultdict(set);closed_placed=0
  for row in r['locked_lessons']+r['lessons']:
   if row['teacher'] is not None:occ[(row['teacher'],row['day'],row['shift'])].update(range(row['period'],row['period']+row.get('length',1)))
   for pp in range(row['period'],row['period']+row.get('length',1)):
    for kind,identity in ([('teacher',row['teacher'])] if row['teacher'] is not None else [])+[('class',cl) for cl in row.get('class_ids',[row['class_id']])]+([('room',row['room'])] if row.get('room') else []):occupied[(kind,identity,row['day'],row['shift'],pp)]+=1
  assert max(occupied.values())==1
  for row in r['lessons']:
   counts[row['assignment']]+=row.get('length',1)
   for cid in row.get('class_ids',[row['class_id']]):
    cl=next(cl for cl in D['classes'] if cl['id']==cid);assert cl['grade']==8
    raw=c['session_config']['class_weeks'].get(cid,c['session_config']['week'])[row['day']][row['shift']]
    effective=raw if c['mode']=='both' or c['mode']=='morning' and row['shift']=='am' or c['mode']=='mixed' and row['shift']==cl['shift'] else 0
    closed_placed+=int(effective==0);assert effective>0;assert row['period']>=0 and row['period']+row.get('length',1)<=effective
  assert counts==Counter({a['id']:a['count'] for a in p['working']['assignments']})
  assert closed_placed==0
  direct_gaps=sum(max(ps)-min(ps)+1-len(ps) for ps in occ.values());assert r['metrics']['gaps']==direct_gaps;assert r['metrics']['visits']==len(occ)
  m=metrics(p['working'],p['config'],r['lessons'],background=p['locked']);q=features(p['working'],p['config'],r['lessons'])
  for k in ['gaps','visits','distribution','preferences','concentration']:assert m[k]==r['metrics'][k],(run['name'],k,m[k],r['metrics'][k])
  assert q['values']['distribution']==r['quality_scores']['values']['distribution'] if 'values' in r['quality_scores'] else q['distribution_penalty_100']==r['quality_scores']['distribution_penalty_100']
  assert r['school_conflicts'] is None;assert not r['global_optimal_proven'];assert r['status']=='FEASIBLE'
 else:assert r['conflicts'] is None and r['metrics'] is None and r['status'] in ['BLOCKED','INFEASIBLE','UNKNOWN']
 audits.append(dict(name=run['name'],status='PASS',solver_status=r['status'],placed=r['placed'],calendar_capacity=a['capacity'],locked_unchanged=True,closed_session_lessons=0 if r['lessons'] else None))
exports=[]
for stem in ['SESSION_UI_EXPORT','SESSION_ZERO_EXPORT']:
 backup=json.loads((ROOT/'reports/SESSION_UI_EXPORT.json').read_text()) if stem=='SESSION_UI_EXPORT' else json.loads((ROOT/'reports/SESSION_ZERO_BACKUP.json').read_text())
 for fmt in ['csv','xlsx']:
  r=import_grade(backup['data'],backup['config'],backup['background'],(ROOT/'reports'/f'{stem}.{fmt}').read_bytes(),fmt);assert r['verification']['valid'];exports.append(dict(file=stem+'.'+fmt,placed=r['placed'],valid=True))
real=json.loads((ROOT/'data/EXAMPLE_SESSION_TECHNICAL_BACKUP.json').read_text());r=import_grade(D,real['config'],BG,(ROOT/'reports/SESSION_REAL_UI_EXPORT.xlsx').read_bytes(),'xlsx');assert r['placed']==234;exports.append(dict(file='SESSION_REAL_UI_EXPORT.xlsx',placed=234,valid=True))
(ROOT/'reports/SESSION_INDEPENDENT_VERIFICATION.json').write_text(json.dumps(dict(status='PASS',runs=audits,exports=exports,known_resource_conflicts=0,source_background_hash=schedule_hash(BG['lessons']),zero_period='PASS',school_conflicts='UNKNOWN: incomplete background',data_accepted=False,windows_accepted=False,production_ready=False),indent=2));print('PASS',len(audits),'benchmarks;',len(exports),'UI exports independently verified')
