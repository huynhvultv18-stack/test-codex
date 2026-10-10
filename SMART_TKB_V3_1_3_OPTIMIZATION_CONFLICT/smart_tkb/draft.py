"""Draft edits never inherit solver proofs or modify frozen records."""
from copy import deepcopy
from .grade import prepare_grade,restore_grade,schedule_hash
from .conflicts import check_prepared
from .validation import metrics
from .teacher_time import evaluate
from .quality import class_ids

def draft_result(data,config,background,lessons):
 p=prepare_grade(data,config,background);report=check_prepared(p,lessons)
 if report['independent_verification']['valid'] and (p['background_context']['complete'] or p['config']['allow_incomplete_background']):
  r=restore_grade(data,config,background,lessons)
 else:
  ctx=p['special'];r=dict(status='DRAFT',lessons=deepcopy(lessons),required=ctx['curricular_required']+ctx['verified'],placed=report['independent_verification'].get('placed') or 0,unscheduled_special=ctx['pending'],phases=[],proven_priorities=[],global_optimal_proven=False,lexicographic_optimal_proven=False,grade_optimal_proven=False,selected_scope_optimal_proven=False,proven_optimal=False,locked_lessons=deepcopy(p['locked']),locked_hash_before=schedule_hash(p['locked']),locked_hash_after=schedule_hash(p['locked']),grade_scheduling='FAIL' if report['status']=='FAIL' else 'PASS',cross_grade_conflict='BLOCKED',locked_grades='PASS',known_cross_grade_conflicts=report['counts']['cross_grade'],school_conflicts=report['school_conflicts'],conflicts=report['known_conflicts'],elapsed_seconds=None,metrics=None,quality_scores={},teacher_visits=[],diagnostics=['Bản nháp được hậu kiểm; chưa xác nhận hợp lệ.'],background=p['background_context'],simulation=report['status']!='PASS',data_accepted=False,windows_accepted=False,production_ready=False,optimality_scope='draft_no_solver_proof')
  try:r['metrics']=metrics(p['working'],p['config'],lessons,background=p['locked']);r['teacher_time']=evaluate(p['working'],p['config'],lessons,p['locked'])
  except (ValueError,KeyError,TypeError,IndexError):pass
 r.update(post_check=report,draft=True,confirmation=None)
 return r

def manual_edit(data,config,background,lessons,index,patch):
 if not isinstance(lessons,list) or type(index) is not int or not 0<=index<len(lessons):raise ValueError('Chỉ sửa dòng của khối đang chọn; chỉ số không hợp lệ')
 if not isinstance(patch,dict) or not patch or set(patch)-{'day','shift','period','room'}:raise ValueError('Chỉ được chuyển ngày/ca/tiết/phòng, giữ nguyên PCCM và độ dài')
 if any(type(patch[k]) is not int for k in ['day','period'] if k in patch) or ('shift' in patch and patch['shift'] not in ['am','pm']) or ('room' in patch and patch['room'] is not None and not isinstance(patch['room'],str)):raise ValueError('Vị trí/phòng chỉnh sửa có kiểu không hợp lệ')
 p=prepare_grade(data,config,background);current=lessons[index]
 if not isinstance(current,dict) or not set(class_ids(current))<={cl['id'] for cl in p['target_data']['classes']}:raise ValueError('Không được sửa lịch ngoài khối đang chọn')
 rows=deepcopy(lessons);rows[index].update(patch)
 return draft_result(data,config,background,rows)
