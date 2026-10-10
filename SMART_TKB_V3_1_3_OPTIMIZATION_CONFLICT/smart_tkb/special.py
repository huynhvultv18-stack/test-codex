"""Source-grounded SpecialActivity inventory and explicit STRICT/SCENARIO rules.

CC/SHCN is deliberately kept as one unresolved combined label. No fake teacher,
homeroom assignment or collective policy is inferred from workbook totals/images.
"""
from collections import defaultdict
from copy import deepcopy

class PreparedData(dict):
    """Internal trusted projection; JSON cannot instantiate this class."""
    def __init__(self, data, context):
        super().__init__(data); self.special_context=context

def inventory(data):
    custom=data.get('special_activities')
    activities=[]
    for row in data.get('pending_special',[]):
        base=row['subject_id'].split(':')[0]
        # Classify only the literal labels present in this source, without
        # splitting the combined CC/SHCN into guessed lesson types/counts.
        label=row['subject']
        kind='EXPERIENTIAL_CAREER' if label=='Hoạt động trải nghiệm, hướng nghiệp' else 'CC_SHCN_COMBINED' if label=='Chào cờ / Sinh hoạt chủ nhiệm' else 'SOURCE_OTHER'
        activities.append(dict(activity_id=f"SP_{row['class_id']}_{base}",class_id=row['class_id'],class_ids=[row['class_id']],
            activity_type=kind,source_label=label,source_subject_id=base+':NONE',weekly_count=row['count'],
            teacher_id=None,teacher_required=None,shared_teacher_group=None,
            fixed_day=None,fixed_period=None,shift=None,room_id=None,
            scheduling_policy='UNRESOLVED',validation_status='PENDING',verification_note='',
            source_row=row.get('source_row'),source_sheet='05_SO_TIET_THEO_LOP',
            pending_reason='Chưa có PCCM giáo viên; chưa xác minh quy tắc cần GV, ca/khóa/phòng và loại CC/SHCN ghép.' if kind=='CC_SHCN_COMBINED' else 'Chưa có PCCM giáo viên; chưa xác minh quy tắc tổ chức/cần giáo viên.'))
    if custom is not None:
        if not isinstance(custom,list) or any(not isinstance(a,dict) for a in custom):raise ValueError('special_activities phải là danh sách')
        if data.get('pending_special'):
            original={a['activity_id']:a for a in activities}
            if len(custom)!=len(original) or {a.get('activity_id') for a in custom}!=set(original):raise ValueError('Không được thêm/bỏ hoạt động trong kiểm kê nguồn')
            fields=('class_id','class_ids','activity_type','source_label','source_subject_id','weekly_count')
            for a in custom:
                if any(a.get(k)!=original[a['activity_id']][k] for k in fields):raise ValueError('Không được sửa loại/lớp/định mức hoạt động nguồn')
        return deepcopy(custom)
    return activities

def activity_classes(activity):
    return activity.get('class_ids') or [activity['class_id']]

def prepare_special(data,config):
    """Build a transient scheduling projection; source/PCCM are never mutated."""
    if isinstance(data,PreparedData):return data,config,data.special_context
    if not isinstance(data,dict):raise ValueError('Dữ liệu phải là đối tượng JSON')
    for name in ('classes','teachers','subjects','assignments','pending_special'):
        if not isinstance(data.get(name,[]),list) or any(not isinstance(row,dict) for row in data.get(name,[])):raise ValueError(name+' phải là danh sách đối tượng JSON')
    if any(not all(k in p for k in ('subject_id','subject','class_id','count')) for p in data.get('pending_special',[])):raise ValueError('Kiểm kê nguồn thiếu lớp/môn/số tiết')
    if any(not isinstance(o,dict) or not isinstance(o.get('activity_id'),str) for o in config.get('special_overrides',[])):raise ValueError('Override cần mã hoạt động chuỗi')
    if any(str(k).startswith('_') for k in data):raise ValueError('JSON không được chứa dấu hiệu xử lý nội bộ')
    if any(a.get('is_special') for a in data.get('assignments',[])):raise ValueError('Hoạt động phải khai báo qua SpecialActivity, không chèn phân công nội bộ')
    working=dict(data);working['assignments']=list(data['assignments']);c=deepcopy(config);activities=inventory(data)
    overrides={o['activity_id']:o for o in c.get('special_overrides',[])}
    ids={a['activity_id'] for a in activities}
    if len(ids)!=len(activities):raise ValueError('Trùng activity_id')
    if len(overrides)!=len(c.get('special_overrides',[])) or not set(overrides)<=ids:raise ValueError('Override SpecialActivity trùng mã hoặc không tồn tại')
    allowed={'teacher_id','teacher_required','shared_teacher_group','fixed_day','fixed_period','shift','room_id','scheduling_policy','validation_status','verification_note'}
    for activity in activities:
        o=overrides.get(activity['activity_id'],{})
        if set(o)-allowed-{'activity_id'}:raise ValueError('Override không được thay đổi loại, lớp hoặc số tiết nguồn')
        activity.update({k:v for k,v in o.items() if k in allowed})
    mode=c.get('special_mode','STRICT')
    if mode not in ('STRICT','SCENARIO'):raise ValueError('special_mode phải là STRICT hoặc SCENARIO')
    scenario=c.get('special_scenario',{})
    if not isinstance(scenario.get('enabled',False),bool) or not isinstance(scenario.get('activity_ids',[]),list):raise ValueError('enabled phải boolean; activity_ids phải danh sách')
    if len(scenario.get('activity_ids',[]))!=len(set(scenario.get('activity_ids',[]))):raise ValueError('Trùng lựa chọn SCENARIO')
    scenario_selected=set(scenario.get('activity_ids',[]))
    if not scenario_selected<=ids:raise ValueError('Scenario có hoạt động không tồn tại')
    if mode=='SCENARIO' and scenario.get('enabled'):
        if not isinstance(scenario.get('assumption_label'),str) or not scenario['assumption_label'].strip():raise ValueError('SCENARIO cần nhãn giả định do người dùng chọn')
        if not isinstance(scenario.get('teacher_required'),bool):raise ValueError('SCENARIO cần chọn rõ teacher_required')
        if not scenario_selected:raise ValueError('SCENARIO cần chọn rõ activity_ids; không tự chọn 111 tiết')
    classes={cl['id'] for cl in data['classes']};teachers={t['id'] for t in data['teachers']};rooms={r['id'] for r in c['rooms']}
    ready=[];pending=[];verified_count=0;scenario_count=0;approved_count=0;status_counts=defaultdict(int)
    for a in activities:
        if not isinstance(a['weekly_count'],int) or isinstance(a['weekly_count'],bool) or a['weekly_count']<1:raise ValueError('weekly_count không hợp lệ')
        cls=activity_classes(a)
        if not cls or len(set(cls))!=len(cls) or not set(cls)<=classes:raise ValueError('SpecialActivity tham chiếu lớp sai')
        simulated=mode=='SCENARIO' and scenario.get('enabled') and a['activity_id'] in scenario_selected
        effective=deepcopy(a)
        if simulated:
            effective.update({k:v for k,v in scenario.items() if k in allowed})
            effective['validation_status']='SCENARIO'
            effective['assumption_label']=scenario['assumption_label']
        reasons=[]
        if effective['validation_status'] not in ('VERIFIED','APPROVED','SCENARIO'):reasons.append('Quy tắc chưa được xác minh')
        if effective['validation_status']=='SCENARIO' and not simulated:reasons.append('SCENARIO chỉ được chọn qua cấu hình mô phỏng rõ ràng')
        if effective['validation_status'] in ('VERIFIED','APPROVED') and (not isinstance(effective.get('verification_note'),str) or not effective['verification_note'].strip()):reasons.append('Thiếu ghi nhận xác minh quy tắc')
        if not isinstance(effective.get('teacher_required'),bool):reasons.append('Chưa rõ có cần giáo viên')
        if effective.get('teacher_required') is True and effective.get('teacher_id') not in teachers:reasons.append('Thiếu mã giáo viên thực đã có trong PCCM')
        if effective.get('teacher_required') is False and effective.get('teacher_id') is not None:reasons.append('Không cần GV nhưng vẫn gán GV; không tự bỏ hoặc tạo GV')
        if effective['scheduling_policy'] not in ('independent','collective'):reasons.append('Thiếu chính sách tổ chức hợp lệ')
        if effective['scheduling_policy']=='collective' and not effective.get('shared_teacher_group'):reasons.append('Tập thể cần mã nhóm được cấu hình rõ')
        for field,upper in [('fixed_day',c['days']),('fixed_period',c['periods'])]:
            val=effective.get(field)
            if val is not None and (isinstance(val,bool) or not isinstance(val,int) or not 0<=val<upper):reasons.append(field+' nằm ngoài lịch')
        if effective.get('shift') not in (None,'am','pm'):reasons.append('Ca không hợp lệ')
        if effective.get('room_id') is not None and effective['room_id'] not in rooms:reasons.append('Phòng chưa khai báo')
        units=a['weekly_count']*len(cls)
        contradictions=('Không cần GV nhưng vẫn gán GV','nằm ngoài lịch','Ca không hợp lệ','Phòng chưa khai báo')
        state='CONFLICT' if any(any(t in reason for t in contradictions) for reason in reasons) else 'MISSING' if reasons or simulated else effective['validation_status']
        a['audit_status']=state;status_counts[state]+=units
        if reasons:
            pending.append(dict(activity_id=a['activity_id'],class_ids=cls,count=units,reasons=reasons,source_label=a['source_label']));continue
        effective['class_ids']=cls;ready.append(effective)
        if simulated:scenario_count+=units
        else:
            verified_count+=units
            if effective['validation_status']=='APPROVED':approved_count+=units
    groups=defaultdict(list)
    for a in ready:
        key=('collective',a['shared_teacher_group']) if a['scheduling_policy']=='collective' else ('independent',a['activity_id'])
        groups[key].append(a)
    new_assignments=[]
    for key,group in groups.items():
        first=group[0]
        fields=['weekly_count','source_subject_id','activity_type','teacher_required','teacher_id','fixed_day','fixed_period','shift','room_id','validation_status']
        if any(any(a.get(k)!=first.get(k) for k in fields) for a in group):raise ValueError('Nhóm tập thể có quy tắc/định mức không đồng nhất')
        cls=[cl for a in group for cl in a['class_ids']]
        if len(set(cls))!=len(cls):raise ValueError('Nhóm tập thể có lớp trùng')
        aid='SPECIAL:'+str(key[1])
        if aid in {a['id'] for a in working['assignments']}:raise ValueError('Mã SpecialActivity đụng PCCM')
        new_assignments.append(dict(id=aid,teacher=first['teacher_id'],teacher_required=first['teacher_required'],class_id=cls[0],class_ids=cls,
            subject_id=first['source_subject_id'],subject=first['source_label'],sub='NONE',count=first['weekly_count'],double_count=0,
            room_ids=[first['room_id']] if first['room_id'] else [],is_special=True,
            activity_ids=[a['activity_id'] for a in group],activity_status=first['validation_status'],
            activity_type=first['activity_type'],shared_teacher_group=first.get('shared_teacher_group'),
            fixed_day=first['fixed_day'],fixed_period=first['fixed_period'],activity_shift=first['shift']))
    working['assignments'].extend(new_assignments)
    total=sum(a['weekly_count']*len(activity_classes(a)) for a in activities)
    context=dict(mode=mode,total=total,verified=verified_count,approved=approved_count,rule_verified=verified_count-approved_count,status_counts=dict(status_counts),eligible_scenario=scenario_count,
        pending=sum(a['count'] for a in pending)+(scenario_count if mode=='SCENARIO' else 0),
        unscheduled_pending=sum(a['count'] for a in pending),inventory=activities,pending_details=pending,
        assumptions=[scenario['assumption_label']] if scenario_count else [],
        curricular_required=sum(a['count'] for a in data['assignments']),
        selected_class_periods=verified_count+scenario_count)
    # Source activities remain PENDING even when a scenario places them. Record
    # their unresolved official state separately from simulated placements.
    if scenario_count:
        for a in ready:
            if a['validation_status']=='SCENARIO':context['pending_details'].append(dict(activity_id=a['activity_id'],class_ids=a['class_ids'],count=a['weekly_count']*len(a['class_ids']),reasons=['Chỉ có giả định SCENARIO, chưa xác minh để dùng chính thức'],source_label=a['source_label']))
    return PreparedData(working,context),c,context

def special_report(context,lessons):
    scheduled_verified=scheduled_scenario=scheduled_approved=0
    for r in lessons:
        if not r.get('is_special'):continue
        units=r.get('length',1)*len(r.get('class_ids') or [r['class_id']])
        if r.get('activity_status')=='SCENARIO':scheduled_scenario+=units
        elif r.get('activity_status')=='APPROVED':scheduled_approved+=units
        else:scheduled_verified+=units
    return dict(total=context['total'],verified=context.get('rule_verified',context['verified']),approved=context.get('approved',0),eligible_strict=context['verified'],status_counts=context.get('status_counts',{}),scheduled_verified=scheduled_verified,scheduled_approved=scheduled_approved,
        scheduled_scenario=scheduled_scenario,scheduled=scheduled_verified+scheduled_approved+scheduled_scenario,
        pending=context['pending'],unscheduled_pending=context['unscheduled_pending'],
        pending_details=context['pending_details'],mode=context['mode'],assumptions=context['assumptions'],
        official_complete=context['verified']==context['total'] and scheduled_verified+scheduled_approved==context['total'],
        simulation=scheduled_scenario>0)
