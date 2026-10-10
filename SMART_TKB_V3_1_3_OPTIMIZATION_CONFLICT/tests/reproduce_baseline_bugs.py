"""Replay audit findings in fresh processes against the locked A and current B."""
import json,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parent.parent
CODE='''import json,copy,io
from smart_tkb.importer import read_pccm
from smart_tkb.special import inventory,prepare_special
from smart_tkb.validation import config_with_defaults,verify_schedule
from smart_tkb.exchange import export_schedule,import_schedule
from openpyxl import load_workbook
from pathlib import Path
r=Path(__import__('sys').argv[1]);d=json.loads((r/'data/pccm_normalized.json').read_text());c=config_with_defaults();lessons=json.loads((r/'baseline_v31/reference_both.json').read_text())['lessons'];out={}
def attempt(name,fn):
 try:out[name]=fn()
 except Exception as e:out[name]={'rejected':True,'exception':type(e).__name__,'message':str(e)[:180]}
bad=copy.deepcopy(lessons)
for row in bad:row['day']+=.5
attempt('fractional_day',lambda:verify_schedule(d,c,bad)['valid'])
forged=copy.deepcopy(d);forged['_special_prepared']=True;forged['_special_context']=dict(total=0,pending=0)
attempt('forged_projection',lambda:prepare_special(forged,c)[2])
omitted=copy.deepcopy(d);omitted['special_activities']=inventory(d)[:-1]
attempt('omitted_special_record',lambda:prepare_special(omitted,c)[2]['total'])
raw=export_schedule(d,c,lessons,'xlsx');w=load_workbook(io.BytesIO(raw));w['TKB']['E2']=float(w['TKB']['E2'].value)+.5;b=io.BytesIO();w.save(b)
attempt('fractional_excel_day',lambda:import_schedule(d,c,b.getvalue(),'xlsx')['status'])
c['phase_fractions']['gaps']=float('nan');attempt('nan_phase_fraction',lambda:bool(config_with_defaults(c)))
print(json.dumps(out,ensure_ascii=False))
'''
results={}
for label,cwd in [('A_BASELINE',R/'baseline_v31'),('B_OPTIMIZED',R)]:
 proc=subprocess.run([sys.executable,'-c',CODE,str(R)],cwd=cwd,text=True,capture_output=True,check=True);results[label]=json.loads(proc.stdout)
(R/'reports/BUG_REPRODUCTIONS.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
