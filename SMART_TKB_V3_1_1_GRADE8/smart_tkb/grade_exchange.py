"""Grade exchange always rechecks frozen resource occupancy before accepting rows."""
import io
from openpyxl import load_workbook
from .grade import prepare_grade,restore_grade
from .exchange import export_schedule,import_schedule

def export_grade(data,config,background,lessons,fmt):
 p=prepare_grade(data,config,background);r=restore_grade(data,config,background,lessons)
 raw=export_schedule(p['target_data'],p['config'],lessons,fmt)
 if fmt=='xlsx':
  wb=load_workbook(io.BytesIO(raw));ws=wb['KIEM_CHUNG']
  for k in ['target_grade','class_count','grade_scheduling','cross_grade_conflict','locked_grades','known_cross_grade_conflicts','cross_grade_conflicts','school_conflicts','simulation','locked_hash_before','locked_hash_after','optimality_scope']:ws.append([k,r.get(k)])
  for k,v in r['metrics'].items():ws.append(['metric:'+k,v])
  ws.append(['background_source',p['background_context']['source_label']]);ws.append(['background_assumption',p['config']['background_assumption']])
  lock=wb.create_sheet('LOCKED_HASH');lock.append(['grade','hash','locked_periods'])
  for g in p['background_context']['grades']:lock.append([g['grade'],g['hash'],g['locked_periods']])
  out=io.BytesIO();wb.save(out);raw=out.getvalue()
 return raw

def import_grade(data,config,background,raw,fmt):
 p=prepare_grade(data,config,background)
 # Existing parser preserves IDs, exact counts and SpecialActivity metadata.
 imported=import_schedule(p['target_data'],p['config'],raw,fmt)
 return restore_grade(data,config,background,imported['lessons'])
