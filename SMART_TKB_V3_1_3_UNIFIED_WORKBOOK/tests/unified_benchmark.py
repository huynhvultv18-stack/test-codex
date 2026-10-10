"""Three modes from imported full PCCM; only selected grade gets CP variables."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
from smart_tkb.workbook import parse_workbook
from smart_tkb.grade import solve_grade,prepare_grade,verify_grade
from smart_tkb.sessions import impact

def main():
 report=parse_workbook((ROOT/'data/DU_LIEU_PCCM_37_LOP_THAM_KHAO.xlsx').read_bytes());assert report['valid'];p=report['state'];old=json.loads((ROOT/'data/EXAMPLE_SESSION_TECHNICAL_BACKUP.json').read_text());out=[]
 for mode in ('morning','both','mixed'):
  c={**p['config'],'mode':mode,'time_limit':15,'workers':4,'allow_incomplete_background':True,'background_assumption':'Kiểm thử workbook PCCM chưa xác minh, lịch nền thiếu tiết đặc biệt'};c['teacher_time']={**c['teacher_time'],'mode':'FAST'}
  prepared=prepare_grade(p['data'],c,p['background']);previous=old['result']['lessons'];change=impact(prepared['working'],prepared['config'],previous)
  r=solve_grade(p['data'],c,p['background'],previous,session_confirmation=change['confirmation'],confirmation_schedule=previous)
  if r['lessons']:assert verify_grade(prepared,r['lessons'])['valid']
  entry=dict(mode=mode,status=r['status'],required=r['required'],placed=r['placed'],known_conflicts=(r.get('verification') or {}).get('within_grade_conflicts'),known_cross_grade_conflicts=(r.get('verification') or {}).get('known_cross_grade_conflicts'),school_conflicts=r.get('school_conflicts'),gaps=(r.get('metrics') or {}).get('gaps'),visits=(r.get('metrics') or {}).get('visits'),elapsed_seconds=r.get('elapsed_seconds'),frozen_hash_before=r.get('locked_hash_before'),frozen_hash_after=r.get('locked_hash_after'),post_check=(r.get('post_check') or {}).get('status'),optimal_proven=r.get('grade_optimal_proven'),production_ready=False);out.append(entry)
  (ROOT/('reports/UNIFIED_SOLVE_'+mode.upper()+'.json')).write_text(json.dumps(dict(input=dict(data=p['data'],config=c,background=p['background']),result=r),ensure_ascii=False,indent=2));print(entry,flush=True)
 (ROOT/'reports/UNIFIED_BENCHMARK.json').write_text(json.dumps(dict(source_classes=37,scope='9 lớp khối 8; các khối khác khóa',technical_only=True,results=out),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
