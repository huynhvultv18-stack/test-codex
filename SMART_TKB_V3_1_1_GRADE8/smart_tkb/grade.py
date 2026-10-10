"""Grade-only orchestration. Frozen lessons are constants, never placements.

Missing background stays unknown; explicit technical simulation never certifies
school-wide conflicts. Source teacher IDs are never joined by display name.
"""
from copy import deepcopy
from collections import Counter,defaultdict
import hashlib,json
from .validation import config_with_defaults,validate_problem,_verify_schedule,verify_schedule,metrics,teacher_visits,blocked
from .quality import class_ids,features,session_periods,active_days
from .special import prepare_special,inventory,special_report
from .solver import _solve_core

DEFAULT_GRADE=dict(target_grade=8,mode='both',days=6,active_days=[0,1,2,3,4,5],periods=5,session_periods={'am':5,'pm':4},max_class_session=5,max_teacher_session=5,time_limit=60,workers=4,seed=17,priorities=['gaps','visits','distribution','preferences','concentration','changes'],allow_incomplete_background=False,background_assumption='')
def grade_config(raw=None):
 c=config_with_defaults({**deepcopy(DEFAULT_GRADE),**(raw or {})})
 if type(c['target_grade']) is not int or c['target_grade'] not in [6,7,8,9]:raise ValueError('Khối cần xếp phải là6..9')
 if not isinstance(c['allow_incomplete_background'],bool) or not isinstance(c['background_assumption'],str):raise ValueError('Cấu hình mô phỏng lịch nền không đúng kiểu')
 if c['allow_incomplete_background'] and not c['background_assumption'].strip():raise ValueError('Mô phỏng thiếu lịch nền cần ghi rõ giả định')
 return c

def schedule_hash(rows):return hashlib.sha256(json.dumps(rows,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def filter_data(data,ids):
 out=deepcopy(data);out['classes']=[cl for cl in out['classes'] if cl['id'] in ids];out['assignments']=[a for a in out['assignments'] if a['class_id'] in ids]
 out['pending_special']=[a for a in out.get('pending_special',[]) if a['class_id'] in ids]
 out['observations']=[a for a in out.get('observations',[]) if a['class_id'] in ids]
 if 'special_activities' in out:out['special_activities']=[a for a in out['special_activities'] if set(class_ids(a))<=ids]
 out['required_periods']=sum(a['count'] for a in out['assignments']);out['all_expected_periods']=out['required_periods']+sum(a['count'] for a in out['pending_special'])
 return out

def slice_config(data,c):
 out=deepcopy(c);cls={cl['id'] for cl in data['classes']};aids={a['id'] for a in data['assignments']};activity_ids={a['activity_id'] for a in inventory(data)}
 out['special_overrides']=[o for o in c['special_overrides'] if o['activity_id'] in activity_ids]
 out['special_scenario']=deepcopy(c['special_scenario'])
 if 'activity_ids' in out['special_scenario']:
  out['special_scenario']['activity_ids']=[i for i in out['special_scenario']['activity_ids'] if i in activity_ids]
  if not out['special_scenario']['activity_ids']:out['special_scenario']['enabled']=False
 for key in ['unavailable','preferences']:out[key]=[o for o in c[key] if o.get('kind')!='class' or o.get('id') in cls]
 special_ids={'SPECIAL:'+i for i in activity_ids}|{'SPECIAL:'+str(o['shared_teacher_group']) for o in c['special_overrides'] if o['activity_id'] in activity_ids and o.get('shared_teacher_group')}
 if c['special_scenario'].get('shared_teacher_group') and set(c['special_scenario'].get('activity_ids',[]))&activity_ids:special_ids.add('SPECIAL:'+str(c['special_scenario']['shared_teacher_group']))
 out['fixed']=[o for o in c['fixed'] if o.get('assignment') in aids|special_ids]
 return out

def unpack_background(value):
 if value is None:return [],config_with_defaults(),''
 if not isinstance(value,dict):raise ValueError('Lịch nền cần lessons/config/source_label')
 rows=value.get('lessons',value.get('result',{}).get('lessons',[]))
 if not isinstance(rows,list) or any(not isinstance(r,dict) for r in rows):raise ValueError('Lịch nền phải là danh sách dòng lịch')
 return rows,config_with_defaults(value.get('config')),str(value.get('source_label','Lịch nền do người dùng nhập'))

def prepare_grade(data,config=None,background=None):
 c=grade_config(config)
 source_activity_ids={a['activity_id'] for a in inventory(data)}
 overrides=c['special_overrides']
 if any(not isinstance(o,dict) or o.get('activity_id') not in source_activity_ids for o in overrides) or len({o['activity_id'] for o in overrides})!=len(overrides):raise ValueError('Override hoạt động trùng mã hoặc chưa có trong nguồn')
 if set(c['special_scenario'].get('activity_ids',[]))-source_activity_ids:raise ValueError('Scenario có hoạt động chưa có trong nguồn')
 all_aids={a['id'] for a in data['assignments']}
 if any(f.get('assignment') not in all_aids and not str(f.get('assignment','')).startswith('SPECIAL:') for f in c['fixed']):raise ValueError('Tiết cố định tham chiếu sai phân công')
 # Validate all authoritative PCCM, not just a filtered projection.
 base=config_with_defaults({**c,'session_periods':{sh:c['periods'] for sh in ['am','pm']},'active_days':list(range(c['days']))})
 # Special/fixed rules are validated against their own projection below.
 check=deepcopy(base);check['fixed']=[];check['special_overrides']=[];check['special_scenario']={};check['special_mode']='STRICT'
 errors=validate_problem(data,check)
 if errors:raise ValueError('PCCM không hợp lệ: '+'; '.join(errors))
 grades={cl['id']:cl.get('grade') for cl in data['classes']}
 if any(g not in [6,7,8,9] for g in grades.values()):raise ValueError('Cần khối6..9 rõ ràng trong danh mục lớp')
 selected={cid for cid,g in grades.items() if g==c['target_grade']};other=set(grades)-selected
 if not selected:raise ValueError('Không có lớp thuộc khối được chọn')
 if any(set(a.get('class_ids') or [a['class_id']])&selected and set(a.get('class_ids') or [a['class_id']])&other for a in inventory(data)):raise ValueError('Hoạt động tập thể liên khối vượt phạm vi; cần quy tắc khóa rõ ràng, không tự tách')
 raw,bg_config,label=unpack_background(background)
 # Keep the physical calendar wide enough to include all frozen occupancy.
 # Target placements still use active_days and session_periods exclusively.
 c['days']=max(c['days'],bg_config['days']);c['periods']=max(c['periods'],bg_config['periods'])
 target=filter_data(data,selected);tc=slice_config(target,c);working,tc,context=prepare_special(target,tc)
 errors=validate_problem(working,tc)
 if errors:raise ValueError('; '.join(errors))
 locked=[];warm=[]
 for row in raw:
  cls=class_ids(row)
  if any(cl not in grades for cl in cls):raise ValueError('Lịch nền tham chiếu lớp chưa có trong PCCM')
  if set(cls)<=selected:warm.append(deepcopy(row))
  elif set(cls)<=other:locked.append(deepcopy(row))
  else:raise ValueError('Hoạt động tập thể vượt phạm vi khối; không tự tách hoặc di chuyển lịch khóa')
 bg=filter_data(data,other);bg_config['rooms']=deepcopy(c['rooms']);bc=slice_config(bg,bg_config);bg_work,bc,bg_context=prepare_special(bg,bc)
 errors=validate_problem(bg_work,bc)
 if errors:raise ValueError('Cấu hình lịch nền không hợp lệ: '+'; '.join(errors))
 # Partial checker still enforces identity, overlap, max load, fixed, doubles,
 # unavailable, rooms and bounds. Only missing counts may be reported separately.
 bv=_verify_schedule(bg_work,bc,locked,allow_partial=True)
 if not bv['valid']:raise ValueError('Lịch nền có lỗi/xung đột; không được tự sửa: '+'; '.join(bv['errors']))
 all_prepared_ids={a['id'] for a in working['assignments']+bg_work['assignments']}
 for f in c['fixed']:
  if f['assignment'] not in all_prepared_ids:raise ValueError('Tiết cố định chưa có hoạt động đủ quy tắc')
  if f['assignment'] in {a['id'] for a in bg_work['assignments']} and not any(r['assignment']==f['assignment'] and all(r.get(k,1 if k=='length' else None)==f.get(k,1 if k=='length' else None) for k in ['day','shift','period','length']) and ('room' not in f or r.get('room')==f['room']) for r in locked):raise ValueError('Tiết cố định yêu cầu thay đổi lịch khóa; không tự mở khóa')
 # New shared-resource holidays and teacher limits may invalidate frozen data;
 # report this rather than silently moving an already locked lesson.
 load=Counter()
 for row in locked:
  if row.get('teacher') is not None:load[(row['teacher'],row['day'],row['shift'])]+=row.get('length',1)
  for pp in range(row['period'],row['period']+row.get('length',1)):
   for kind,identity in ([('teacher',row['teacher'])] if row.get('teacher') is not None else [])+([('room',row['room'])] if row.get('room') else [])+[('class',cl) for cl in class_ids(row)]:
    if blocked(c,kind,identity,row['day'],row['shift'],pp):raise ValueError('Lịch nền khóa vi phạm lịch nghỉ hiện tại; cần người quản lý điều chỉnh')
 if any(n>tc['max_teacher_session'] for n in load.values()):raise ValueError('Lịch nền khóa vượt giới hạn GV/buổi hiện tại')
 counts=Counter()
 for row in locked:counts[row['assignment']]+=row.get('length',1)
 missing=[dict(assignment=a['id'],class_ids=class_ids(a),periods=(a['count']-counts[a['id']])*len(class_ids(a))) for a in bg_work['assignments'] if counts[a['id']]<a['count']]
 unresolved=bg_context['pending'];complete=not missing and unresolved==0 and not any(r.get('activity_status')=='SCENARIO' for r in locked)
 pergrade=[]
 for g in sorted(set(grades.values())-{c['target_grade']}):
  rows=[r for r in locked if grades[r['class_id']]==g];classes={i for i,v in grades.items() if v==g};required=sum(a['count'] for a in bg['assignments'] if a['class_id'] in classes)
  n=sum(r.get('length',1)*len(class_ids(r)) for r in rows if r.get('activity_status')!='SCENARIO')
  pergrade.append(dict(grade=g,classes=len(classes),source_periods=required,locked_periods=n,hash=schedule_hash(rows),status='LOCKED' if rows else 'MISSING'))
 cross=[];teacher_map={t['id']:t for t in data['teachers']}
 affected={a['teacher'] for a in working['assignments'] if a['teacher'] is not None}
 for tid in sorted(affected):
  gs=sorted({grades[a['class_id']] for a in data['assignments'] if a['teacher']==tid})
  if len(gs)>1:
   rows=[r for r in locked if r['teacher']==tid];t=teacher_map[tid]
   cross.append(dict(teacher_id=tid,name=t['name'],grades=gs,locked_periods=sum(r.get('length',1) for r in rows),locked_visits=len({(r['day'],r['shift']) for r in rows}),identity_verified=t.get('status')=='VERIFIED' and bool(t.get('full_name'))))
 warnings=[]
 if not complete:warnings.append(f'Lịch nền chưa đầy đủ: thiếu{sum(x["periods"] for x in missing)} tiết đã có phân công và{unresolved} tiết đặc biệt chưa có quy tắc. Không xác minh0 xung đột toàn trường.')
 unverified=[t['id'] for t in data['teachers'] if t['id'] in affected and (t.get('status')!='VERIFIED' or not t.get('full_name'))]
 if unverified:warnings.append(f'{len(unverified)} mã GV của khối chưa xác minh; dùng nguyên mã, không gộp theo tên.')
 context_bg=dict(complete=complete,known_schedule_valid=True,source_label=label,missing_assignments=missing,missing_assigned_periods=sum(x['periods'] for x in missing),pending_special_periods=unresolved,locked_periods=sum(r.get('length',1)*len(class_ids(r)) for r in locked),hash=schedule_hash(locked),grades=pergrade,cross_grade_teachers=cross,warnings=warnings)
 return dict(config=tc,target_data=target,working=working,special=context,locked=locked,background_config=bc,background_data=bg_work,background_context=context_bg,warm=warm,unverified_teacher_ids=unverified)

def verify_grade(prepared,lessons,locked_after=None):
 p=prepared;c=p['config'];locked=p['locked'];after=locked if locked_after is None else locked_after
 v=verify_schedule(p['working'],c,lessons);errors=list(v['errors']);unchanged=schedule_hash(after)==p['background_context']['hash']
 if not unchanged:errors.append('CRITICAL: thay đổi lịch ngoài khối được chọn')
 # This checker independently intersects resource occupancy; it never reads
 # CP variables or relies on generated unavailable constraints.
 busy=Counter();load=Counter();cross=0
 for row in locked:
  for pp in range(row['period'],row['period']+row.get('length',1)):
   for k,i in ([('teacher',row['teacher'])] if row.get('teacher') is not None else [])+([('room',row['room'])] if row.get('room') else []):busy[(k,i,row['day'],row['shift'],pp)]+=1
  if row.get('teacher') is not None:load[(row['teacher'],row['day'],row['shift'])]+=row.get('length',1)
 if v['valid']:
  for row in lessons:
   for pp in range(row['period'],row['period']+row.get('length',1)):
    for k,i in ([('teacher',row['teacher'])] if row.get('teacher') is not None else [])+([('room',row['room'])] if row.get('room') else []):cross+=busy[(k,i,row['day'],row['shift'],pp)]
   if row.get('teacher') is not None:load[(row['teacher'],row['day'],row['shift'])]+=row.get('length',1)
 if cross:errors.append(f'{cross} xung đột với lịch giáo viên/phòng đã khóa')
 if any(n>c['max_teacher_session'] for n in load.values()):errors.append('Vượt giới hạn GV/buổi khi cộng cả lịch nền')
 complete=p['background_context']['complete']
 return dict(valid=not errors,errors=errors,within_grade_conflicts=v['conflicts'],known_cross_grade_conflicts=cross if v['valid'] else None,cross_grade_conflicts=cross if complete and v['valid'] else None,school_conflicts=None if not complete or not v['valid'] else (v['conflicts']+cross),cross_grade_fully_verified=complete and not errors,locked_unchanged=unchanged,locked_hash_before=p['background_context']['hash'],locked_hash_after=schedule_hash(after),required=v['required'],placed=v['placed'])

def grade_summary(p,r):
 lessons=r['lessons'];ctx=p['special'];report=special_report(ctx,lessons);known=p['locked'];c=p['config'];local_scope=r.get('local_scope')
 r.setdefault('grade_optimal_proven',False);r['selected_scope_optimal_proven']=r.get('lexicographic_optimal_proven',r.get('grade_optimal_proven',False))
 r['solver_status']=r['status'] if r['status'] in ['FEASIBLE','OPTIMAL','INFEASIBLE','UNKNOWN'] else 'NOT_RUN'
 if local_scope:r['grade_optimal_proven']=False
 r.update(target_grade=c['target_grade'],class_count=len(p['target_data']['classes']),scheduled_class_periods=r['placed'],model_required=r['required'],required=ctx['curricular_required']+ctx['verified'],placed=sum(row.get('length',1)*len(class_ids(row)) for row in lessons if row.get('activity_status')!='SCENARIO'),scenario_placed=report['scheduled_scenario'],unscheduled_special=report['pending'],special_report=report,background=p['background_context'],locked_lessons=deepcopy(known),locked_hash_before=p['background_context']['hash'],locked_hash_after=schedule_hash(known),data_accepted=False,windows_accepted=False,production_ready=False,official_complete=False,all_source_periods=ctx['curricular_required']+ctx['total'],global_optimal_proven=False,optimality_scope='local_grade_with_frozen_background' if local_scope else 'grade_with_frozen_background')
 r['simulation']=not p['background_context']['complete'] or report['simulation'];r['scenario_assumptions']=([c['background_assumption']] if not p['background_context']['complete'] else [])+report['assumptions']
 r['teacher_visits']=teacher_visits(p['working'],known+lessons)
 if lessons:
  v=verify_grade(p,lessons,r['locked_lessons']);r['verification']=v
  if not v['valid']:raise RuntimeError('Independent grade verifier rejected output: '+str(v['errors']))
  r['conflicts']=v['within_grade_conflicts'];r['known_cross_grade_conflicts']=v['known_cross_grade_conflicts'];r['cross_grade_conflicts']=v['cross_grade_conflicts'];r['school_conflicts']=v['school_conflicts']
  base_visits=metrics(p['working'],c,[],background=known)['visits'];full=metrics(p['working'],c,lessons,background=known)
  r['metrics']={**(r.get('metrics') or full),'baseline_visits':base_visits,'added_visits':full['visits']-base_visits,'grade_only_gaps':metrics(p['working'],c,lessons)['gaps'],'grade_only_visits':metrics(p['working'],c,lessons)['visits']}
 else:r.update(known_cross_grade_conflicts=None,cross_grade_conflicts=None,school_conflicts=None)
 r['grade_scheduling']='PASS' if lessons else 'BLOCKED' if r['status']=='BLOCKED' else 'FAIL';r['cross_grade_conflict']='PASS' if lessons and p['background_context']['complete'] else 'BLOCKED';r['locked_grades']='PASS'
 return r

def solve_grade(data,config=None,background=None,previous=None,progress=None,scope=None):
 p=prepare_grade(data,config,background);c=p['config'];ctx=p['special']
 if not p['background_context']['complete'] and not c['allow_incomplete_background']:
  return grade_summary(p,dict(status='BLOCKED',lessons=[],required=ctx['curricular_required']+ctx['verified']+ctx['eligible_scenario'],placed=0,conflicts=None,metrics=None,elapsed_seconds=0,diagnostics=p['background_context']['warnings']+['Nạp đủ lịch nền hoặc chọn mô phỏng kỹ thuật có nhãn giả định rõ ràng.'],phases=[],proven_priorities=[]))
 warm=previous if previous is not None else p['warm']
 if warm:
  # Invalid prior schedules are hints only; no retained unverified incumbent.
  if not verify_grade(p,warm)['valid']:warm=[]
 if scope is not None:
  if not isinstance(scope,dict) or not (scope.get('classes') or scope.get('teachers')):raise ValueError('Phạm vi tối ưu cục bộ rỗng')
  if set(scope.get('classes',[]))-{cl['id'] for cl in p['target_data']['classes']} or set(scope.get('teachers',[]))-{t['id'] for t in data['teachers']}:raise ValueError('Phạm vi cục bộ vượt khối đang xếp hoặc mã GV chưa có')
  if not warm:raise ValueError('Tối ưu cục bộ cần lịch khối hiện tại đã kiểm chứng')
 r=_solve_core(p['working'],c,warm,scope=scope,progress=progress,background=p['locked'])
 r['grade_optimal_proven']=r.get('lexicographic_optimal_proven',False)
 r['local_scope']=deepcopy(scope)
 r=grade_summary(p,r)
 if r['status']=='INFEASIBLE':r['diagnostics']+=['Giữ nguyên khối khóa. Có thể đề nghị người quản lý điều chỉnh lịch nền/phòng/giới hạn hoặc ngày học; phần mềm không tự mở khóa.']
 return r

def restore_grade(data,config,background,lessons):
 p=prepare_grade(data,config,background)
 if not p['background_context']['complete'] and not p['config']['allow_incomplete_background']:raise ValueError('Lịch nền chưa đủ; cần nhãn mô phỏng để nhập lịch kỹ thuật')
 v=verify_grade(p,lessons)
 if not v['valid']:raise ValueError('; '.join(v['errors']))
 q=features(p['working'],p['config'],lessons)
 r=dict(status='FEASIBLE',lessons=deepcopy(lessons),required=v['required'],placed=v['placed'],metrics=metrics(p['working'],p['config'],lessons,background=p['locked']),quality_scores={k:x for k,x in q.items() if k!='values'},elapsed_seconds=None,phases=[],proven_priorities=[],grade_optimal_proven=False,diagnostics=['Lịch nhập đã hậu kiểm; không kế thừa chứng minh tối ưu.'])
 return grade_summary(p,r)
