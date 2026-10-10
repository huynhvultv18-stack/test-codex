"""Independent schedule verification. Does not read CP-SAT variables."""
from collections import Counter, defaultdict
from copy import deepcopy
import math
from .sessions import normalize,effective_periods,study_days
from .special import PreparedData
from .quality import class_ids, features, rule_for, active_days, session_periods

DEFAULT_CONFIG = dict(mode='both', days=6, periods=5, max_class_session=5,
                      max_teacher_session=5, time_limit=30, workers=4, seed=17,
                      technical_only=True, rooms=[], unavailable=[], fixed=[],
                      preferences=[], priorities=['gaps','visits','distribution','concentration','preferences','changes'],
                      phase_fractions=dict(gaps=.25,visits=.50,distribution=.16,concentration=.06,preferences=.02,changes=.01),
                      advance_on_incumbent=True, search_mode='portfolio',
                      objective_settings={k:dict(enabled=True,weight=1) for k in ['gaps','visits','distribution','concentration','preferences','changes']},
                      subject_rules=[],subject_hard_limits=[],heavy_subjects=[],heavy_run_limit=2,heavy_weight=0,
                      special_mode='STRICT',special_overrides=[],special_scenario={})

def config_with_defaults(raw=None):
    if raw is not None and not isinstance(raw,dict):raise ValueError('Cấu hình phải là đối tượng JSON')
    c={**deepcopy(DEFAULT_CONFIG), **(raw or {})}
    if c['mode'] not in ('morning','both','mixed'): raise ValueError('Chế độ không hợp lệ')
    for name,low,high in [('days',1,7),('periods',1,8),('max_class_session',1,8),('max_teacher_session',1,8),('workers',1,16),('seed',0,2147483647)]:
        v=c[name]
        if isinstance(v,bool) or not isinstance(v,int) or not low<=v<=high: raise ValueError(f'{name} phải nằm trong {low}..{high}')
    normalize(c)
    if isinstance(c['time_limit'],bool) or not isinstance(c['time_limit'],(int,float)) or not 0<c['time_limit']<=600: raise ValueError('Giới hạn giải 0..600 giây')
    names={'gaps','visits','distribution','concentration','preferences','changes'}
    if not isinstance(c['technical_only'],bool):raise ValueError('technical_only phải là boolean')
    if not isinstance(c['priorities'],list) or any(not isinstance(n,str) for n in c['priorities']) or set(c['priorities']) != names or len(c['priorities']) != 6: raise ValueError('priorities phải chứa đủ 6 mục tiêu, mỗi mục một lần')
    for key in ('rooms','unavailable','fixed','preferences'):
        if not isinstance(c[key],list): raise ValueError(f'{key} phải là danh sách')
        if any(not isinstance(item,dict) for item in c[key]):raise ValueError(key+' cần từng mục là đối tượng JSON')
    if any(not isinstance(r.get('id'),str) or not r['id'] for r in c['rooms']):raise ValueError('Phòng cần mã chuỗi không rỗng')
    roomids=[r['id'] for r in c['rooms']]
    if len(set(roomids)) != len(roomids) or any(not isinstance(r,str) or not r for r in roomids): raise ValueError('Mã phòng trùng/rỗng')
    if c['search_mode'] not in ('portfolio','lns'):raise ValueError('search_mode phải là portfolio/lns')
    if not isinstance(c['advance_on_incumbent'],bool):raise ValueError('advance_on_incumbent phải là boolean')
    if c['special_mode'] not in ('STRICT','SCENARIO'):raise ValueError('special_mode phải là STRICT/SCENARIO')
    if not isinstance(c['special_overrides'],list) or not isinstance(c['special_scenario'],dict):raise ValueError('Cấu hình SpecialActivity không hợp lệ')
    if not isinstance(c['phase_fractions'],dict) or set(c['phase_fractions']) != names or any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<0 for v in c['phase_fractions'].values()) or sum(c['phase_fractions'].values())<=0:raise ValueError('phase_fractions cần đủ 6 mục tiêu và tỷ trọng không âm')
    if not isinstance(c['objective_settings'],dict):raise ValueError('objective_settings phải là đối tượng')
    settings={**deepcopy(DEFAULT_CONFIG['objective_settings']),**c['objective_settings']}
    if set(settings)!=names:raise ValueError('Mục tiêu không tồn tại')
    for value in settings.values():
        if not isinstance(value,dict) or not isinstance(value.get('enabled'),bool) or type(value.get('weight')) is not int or not 1<=value['weight']<=100:raise ValueError('Mục tiêu cần enabled boolean, weight nguyên 1..100')
    c['objective_settings']=settings
    for key in ('subject_rules','subject_hard_limits','heavy_subjects'):
        if not isinstance(c[key],list):raise ValueError(key+' phải là danh sách')
    if any(not isinstance(s,str) for s in c['heavy_subjects']):raise ValueError('Môn nặng cần mã chuỗi')
    if type(c['heavy_run_limit']) is not int or not 1<=c['heavy_run_limit']<=8 or type(c['heavy_weight']) is not int or not 0<=c['heavy_weight']<=100:raise ValueError('heavy_run_limit/heavy_weight không hợp lệ')
    for rule in c['subject_rules']:
        if not isinstance(rule,dict) or not isinstance(rule.get('grades',[]),list) or not isinstance(rule.get('preferred_periods',[]),list):raise ValueError('Quy tắc môn/khối phải đúng kiểu JSON')
        allowed={'subject','grades','daily_soft_max','distribution_weight','concentration_weight','adjacent_weight','preferred_periods','period_weight'}
        if set(rule)-allowed or not rule.get('subject'):raise ValueError('subject_rules có trường chưa hỗ trợ')
        for key in ('daily_soft_max','distribution_weight','concentration_weight','adjacent_weight','period_weight'):
            if key in rule and (type(rule[key]) is not int or not 0<=rule[key]<=100):raise ValueError('Trọng số/giới hạn soft phải nguyên 0..100')
        if any(type(p) is not int or not 0<=p<c['periods'] for p in rule.get('preferred_periods',[])):raise ValueError('Tiết ưu tiên môn nằm ngoài buổi')
        if any(g not in [6,7,8,9] for g in rule.get('grades',[])):raise ValueError('Khối phải là 6..9')
    for rule in c['subject_hard_limits']:
        if not isinstance(rule,dict) or not isinstance(rule.get('subject'),str) or not isinstance(rule.get('grades',[]),list) or any(type(g) is not int or g not in [6,7,8,9] for g in rule.get('grades',[])):raise ValueError('Khối HARD phải là 6..9')
        if set(rule)-{'subject','grades','max_daily'} or type(rule.get('max_daily')) is not int or not 0<=rule['max_daily']<=2*c['periods']:raise ValueError('Giới hạn HARD theo môn không hợp lệ')
    if 'session_periods' not in c:c['session_periods']={sh:c['periods'] for sh in ('am','pm')}
    if not isinstance(c['session_periods'],dict) or set(c['session_periods'])!={'am','pm'} or any(type(n) is not int or not 1<=n<=c['periods'] for n in c['session_periods'].values()):raise ValueError('Số tiết sáng/chiều phải nguyên1..periods')
    if 'active_days' not in c:c['active_days']=list(range(c['days']))
    if not isinstance(c['active_days'],list) or not c['active_days'] or any(type(d) is not int or not 0<=d<c['days'] for d in c['active_days']) or len(set(c['active_days']))!=len(c['active_days']):raise ValueError('Ngày học phải là danh sách ngày duy nhất trong tuần')
    return c

def class_shifts(cls,c):
    return ['am'] if c['mode']=='morning' else ['am','pm'] if c['mode']=='both' else [cls.get('shift','am')]

def validate_problem(data,config):
    errors=[]
    def err(msg): errors.append(msg)
    if not isinstance(data,dict):return ['Dữ liệu phải là đối tượng JSON']
    if not isinstance(data,PreparedData) and any(str(k).startswith('_') for k in data):err('JSON có dấu hiệu xử lý nội bộ không hợp lệ')
    for key in ('classes','teachers','subjects','assignments'):
        if not isinstance(data.get(key),list):return errors+[key+' phải là danh sách']
        if any(not isinstance(x,dict) or not isinstance(x.get('id'),str) or not x['id'] for x in data[key]):return errors+['Mã '+key+' phải là chuỗi không rỗng']
    for a in data['assignments']:
        if not all(k in a for k in ('teacher','class_id','subject_id','subject','count')):return errors+['Phân công thiếu trường bắt buộc']
        if 'class_ids' in a and (not isinstance(a['class_ids'],list) or not a['class_ids'] or any(not isinstance(cl,str) for cl in a['class_ids']) or len(set(a['class_ids']))!=len(a['class_ids'])):return errors+['Nhóm lớp phân công phải là danh sách mã duy nhất']
        if not isinstance(a.get('room_ids',[]),list):return errors+['Danh sách phòng không hợp lệ']
        if a.get('is_special') and not isinstance(data,PreparedData):err('Không được chèn phân công hoạt động nội bộ')
    tables={k:{x['id']:x for x in data[k]} for k in ('classes','teachers','subjects','assignments')}
    for k,t in tables.items():
        if len(t)!=len(data[k]): err('Mã trùng: '+k)
    if cals:=config.get('session_config'):
        if set(cals['class_weeks'])-set(tables['classes']):err('Cấu hình buổi tham chiếu lớp chưa có trong PCCM')
    subjects={s['id'] for s in data['subjects']};rooms={r['id'] for r in config['rooms']}
    original=[a for a in data['assignments'] if not a.get('is_special')]
    base_count=sum(a['count'] for a in original if type(a['count']) is int)
    pending=data.get('pending_special',[])
    if not isinstance(pending,list) or any(not isinstance(p,dict) or type(p.get('count')) is not int or p['count']<1 or not isinstance(p.get('class_id'),str) for p in pending):return errors+['Kiểm kê pending phải có lớp và số tiết nguyên dương']
    if 'required_periods' in data and data['required_periods']!=base_count:err('Tổng PCCM chuẩn hóa không khớp các phân công')
    if 'all_expected_periods' in data and data['all_expected_periods']!=base_count+sum(p['count'] for p in pending):err('Tổng nguồn không khớp PCCM và kiểm kê pending; không được bỏ hoạt động thiếu dữ liệu')
    for cls in data['classes']:
        if cls.get('shift','am') not in ('am','pm'): err('Ca lớp không hợp lệ: '+cls['id'])
        source_count=sum(a['count'] for a in original if a['class_id']==cls['id'] and type(a['count']) is int)+sum(p['count'] for p in pending if p['class_id']==cls['id'])
        if 'expected' in cls and cls['expected']!=source_count:err('Tổng nguồn của lớp không khớp: '+cls['id'])
    for a in data['assignments']:
        if not a.get('is_special') and class_ids(a)!=[a['class_id']]:err('PCCM thông thường phải thuộc đúng một lớp: '+a['id'])
        if (a['teacher'] not in tables['teachers'] and not (a.get('is_special') and a.get('teacher_required') is False and a['teacher'] is None)) or not set(class_ids(a))<=set(tables['classes']) or a['subject_id'] not in subjects: err('Phân công tham chiếu sai: '+a['id'])
        if not isinstance(a['count'],int) or isinstance(a['count'],bool) or a['count']<1: err('Số tiết không hợp lệ: '+a['id'])
        d=a.get('double_count',0)
        if not isinstance(d,int) or isinstance(d,bool) or d<0 or 2*d>a['count']: err('Số cặp tiết đôi không hợp lệ: '+a['id'])
        for room in a.get('room_ids',[]):
            if room not in rooms: err('Phòng chưa khai báo: '+room)
    for item in config['unavailable']+config['preferences']:
        if item.get('kind') not in ('teacher','class','room'): err('kind phải là teacher/class/room'); continue
        ids=tables['teachers'] if item['kind']=='teacher' else tables['classes'] if item['kind']=='class' else {r['id']:r for r in config['rooms']}
        if item.get('id') not in ids: err('Đối tượng lịch nghỉ/nguyện vọng không tồn tại')
        if type(item.get('day')) is not int or not 0<=item['day']<config['days']: err('day nằm ngoài lịch')
        if item.get('shift') not in ('am','pm'): err('shift không hợp lệ')
        if 'period' in item and (type(item['period']) is not int or not 0<=item['period']<config['periods']): err('period nằm ngoài lịch')
        if 'weight' in item and (type(item['weight']) is not int or not 0<=item['weight']<=1000): err('weight phải là số nguyên 0..1000')
    for f in config['fixed']:
        if f.get('assignment') not in tables['assignments']: err('Tiết cố định tham chiếu sai phân công'); continue
        if type(f.get('length',1)) is not int or f.get('length',1) not in (1,2): err('length của tiết cố định phải là 1 hoặc 2')
        if type(f.get('day')) is not int or not 0<=f['day']<config['days']: err('Ngày cố định ngoài lịch')
        if f.get('shift') not in ('am','pm'): err('Ca cố định không hợp lệ')
        if type(f.get('period')) is not int or not 0<=f['period']<=config['periods']-f.get('length',1): err('Tiết cố định ngoài buổi')
        if f.get('room') is not None and f['room'] not in rooms: err('Phòng cố định chưa khai báo')
    for item in data.get('issues',[]):
        if item['level']=='ERROR': err(item['message'])
    if not config['technical_only'] and (data.get('pending_special') or any(t.get('status')!='VERIFIED' or not t.get('full_name') for t in data['teachers']) or any(i['level']=='WARNING' for i in data.get('issues',[]))):
        err('PCCM chưa được nghiệm thu: chỉ được kiểm thử kỹ thuật có điều kiện')
    bases={s['id'].split(':')[0] for s in data['subjects']}
    for rule in config['subject_rules']+config['subject_hard_limits']:
        if rule['subject'] not in bases:err('Quy tắc có mã môn chưa tồn tại')
    if not set(config['heavy_subjects'])<=bases:err('Môn nặng chưa có trong danh mục')
    for cls in data['classes']:
        for sub in bases:
            try:rule_for(cls['id'],sub,data,config)
            except ValueError as e:err(str(e))
    return errors

def blocked(c,kind,identifier,d,sh,p):
    return any(x['kind']==kind and x['id']==identifier and x['day']==d and x['shift']==sh and ('period' not in x or x['period']==p) for x in c['unavailable'])

def signature(row):
    return (row['assignment'],row['day'],row['shift'],row['period'],row.get('length',1),row.get('room'))

def _verify_schedule(data,config,lessons,previous=None,scope=None,allow_partial=False):
    c=config_with_defaults(config);assign={a['id']:a for a in data['assignments']};classes={x['id']:x for x in data['classes']}
    errors=[]; count=Counter();used=Counter();c_load=Counter();t_load=Counter();doubles=Counter()
    if not isinstance(lessons,list):return dict(valid=False,conflicts=None,errors=['Lịch phải là danh sách'],required=sum(a['count']*len(class_ids(a)) for a in assign.values()),placed=0)
    accepted=[]
    for row in lessons:
        if not isinstance(row,dict):errors.append('Dòng lịch phải là đối tượng');continue
        if any(type(row.get(k,1 if k=='length' else None)) is not int for k in ('day','period','length')):errors.append('Ngày/tiết/độ dài phải là số nguyên');continue
        if 'class_ids' in row and (not isinstance(row['class_ids'],list) or not row['class_ids'] or any(not isinstance(cl,str) for cl in row['class_ids'])):errors.append('Nhóm lớp dòng lịch không hợp lệ');continue
        a=assign.get(row.get('assignment'))
        if not a: errors.append('Phân công không tồn tại'); continue
        if row.get('teacher')!=a['teacher'] or row.get('class_id')!=a['class_id'] or row.get('subject_id')!=a['subject_id']:
            errors.append('Sai giáo viên/lớp/môn phụ trách')
        d,sh,p,L=row['day'],row['shift'],row['period'],row.get('length',1)
        if L not in (1,2) or sh not in ('am','pm') or not 0<=d<c['days'] or not 0<=p<=min(effective_periods(c,classes[cl],d,sh) for cl in class_ids(a))-L:
            errors.append('Ngoài ca/ngày/buổi hoặc tiết đôi qua buổi');continue
        accepted.append(row)
        count[a['id']]+=L;doubles[a['id']]+=int(L==2)
        if len(class_ids(row))!=len(set(class_ids(row))) or set(class_ids(row))!=set(class_ids(a)):errors.append('Sai nhóm lớp của hoạt động')
        if bool(row.get('is_special'))!=bool(a.get('is_special')):errors.append('Sai cờ hoạt động đặc biệt')
        if a.get('is_special'):
            if any(a.get(k) is not None and val!=a[k] for k,val in [('fixed_day',d),('fixed_period',p),('activity_shift',sh)]):errors.append('Vi phạm khóa hoạt động đặc biệt')
            if row.get('activity_ids')!=a.get('activity_ids') or row.get('activity_status')!=a.get('activity_status'):errors.append('Sai định danh/trạng thái SpecialActivity')
            if row.get('activity_type')!=a.get('activity_type') or row.get('shared_teacher_group')!=a.get('shared_teacher_group'):errors.append('Sai loại/nhóm SpecialActivity')
        room=row.get('room')
        if a.get('room_ids') and room not in a['room_ids']:errors.append('Sai phòng chức năng')
        if not a.get('room_ids') and room is not None:errors.append('Gán phòng không thuộc phân công')
        for period in range(p,p+L):
            for kind,identity in ([('teacher',a['teacher'])] if a['teacher'] is not None else [])+ [('class',cl) for cl in class_ids(a)]+([('room',room)] if room else []):
                key=(kind,identity,d,sh,period);used[key]+=1
                if blocked(c,kind,identity,d,sh,period):errors.append('Vi phạm lịch nghỉ')
            for cl in class_ids(a):c_load[(cl,d,sh)]+=1
            if a['teacher'] is not None:t_load[(a['teacher'],d,sh)]+=1
    conflict_count=sum(max(0,n-1) for n in used.values())
    if conflict_count:errors.append(f'{conflict_count} xung đột giáo viên/lớp/phòng')
    for a in assign.values():
        if count[a['id']]>a['count'] or (not allow_partial and count[a['id']]!=a['count']):errors.append('Sai số tiết: '+a['id'])
        if doubles[a['id']]>a.get('double_count',0) or (not allow_partial and doubles[a['id']]!=a.get('double_count',0)):errors.append('Sai số cặp tiết đôi: '+a['id'])
    if any(n>c['max_class_session'] for n in c_load.values()):errors.append('Quá tiết tối đa/lớp/buổi')
    if any(n>c['max_teacher_session'] for n in t_load.values()):errors.append('Quá tiết tối đa/GV/buổi')
    for f in c['fixed']:
        if not any(row['assignment']==f['assignment'] and row['day']==f['day'] and row['shift']==f['shift'] and row['period']==f['period'] and row.get('length',1)==f.get('length',1) and ('room' not in f or row.get('room')==f['room']) for row in accepted):errors.append('Thiếu tiết cố định')
    if scope and previous:
        current=Counter(signature(r) for r in accepted)
        frozen=Counter(signature(x) for x in previous if not in_scope(x,scope))
        if frozen-current:errors.append('Thay đổi ngoài phạm vi xếp lại')
    quality=features(data,c,accepted)
    hard_daily=Counter()
    for row in accepted:
        a=assign.get(row.get('assignment'))
        if a:
            for cl in class_ids(a):hard_daily[(cl,a['subject_id'].split(':')[0],row['day'])]+=row.get('length',1)
    grades={cl['id']:cl.get('grade',0) for cl in data['classes']}
    for hard in c['subject_hard_limits']:
        for (cl,sub,d),n in hard_daily.items():
            if sub==hard['subject'] and (not hard.get('grades') or grades[cl] in hard['grades']) and n>hard['max_daily']:errors.append('Vi phạm HARD giới hạn môn/ngày')
    return dict(valid=not errors, conflicts=conflict_count, errors=errors,
                required=sum(a['count']*len(class_ids(a)) for a in assign.values()), placed=sum(r.get('length',1)*len(class_ids(r)) for r in accepted))

def verify_schedule(data,config,lessons,previous=None,scope=None):
    c=config_with_defaults(config)
    if not isinstance(data,PreparedData):
        from .special import prepare_special
        data,c,_=prepare_special(data,c)
    errors=validate_problem(data,c)
    if errors:return dict(valid=False,conflicts=None,errors=errors,required=0,placed=0)
    return _verify_schedule(data,c,lessons,previous,scope)

def in_scope(row,scope):
    return bool(set(class_ids(row)) & set(scope.get('classes',[]))) or row['teacher'] in scope.get('teachers',[])

def metrics(data,c,lessons,previous=None,background=None):
    occ=defaultdict(set);daily=Counter();pref=0
    assignments={a['id']:a for a in data['assignments']}
    for row in lessons:
        a=assignments[row['assignment']]
        for p in range(row['period'],row['period']+row.get('length',1)):
            if a['teacher'] is not None:occ[(a['teacher'],row['day'],row['shift'])].add(p)
            for cl in class_ids(a):
                if not a.get('is_special') and not a['subject_id'].startswith('HD'):daily[(cl,a['subject_id'].split(':')[0],row['day'])]+=1
            for q in c['preferences']:
                identities=[a['teacher']] if q['kind']=='teacher' else class_ids(a) if q['kind']=='class' else [row.get('room')]
                if q['id'] in identities and row['day']==q['day'] and row['shift']==q['shift'] and ('period' not in q or p==q['period']):pref+=q.get('weight',1)
    for row in background or []:
        if row.get('teacher') is not None:occ[(row['teacher'],row['day'],row['shift'])].update(range(row['period'],row['period']+row.get('length',1)))
    gaps=sum(max(ps)-min(ps)+1-len(ps) for ps in occ.values())
    subjects={(cl,a['subject_id'].split(':')[0]) for a in data['assignments'] if not a.get('is_special') and not a['subject_id'].startswith('HD') for cl in class_ids(a)}
    classes={cl['id']:cl for cl in data['classes']}
    distribution=sum(max([daily[(cl,s,d)] for d in study_days(c,cl,classes)] or [0])-min([daily[(cl,s,d)] for d in study_days(c,cl,classes)] or [0]) for cl,s in subjects)
    changes=0
    if previous:
        old=Counter(signature(r) for r in previous);cur=Counter(signature(r) for r in lessons)
        changes=sum((old-cur).values())
    pref+=features(data,c,lessons)['subject_period_preferences']
    return dict(gaps=gaps,visits=len(occ),distribution=distribution,
                concentration=sum(max(0,n-1) for n in daily.values()),preferences=pref,changes=changes)


def teacher_visits(data,lessons):
    seen=defaultdict(set);loads=Counter()
    for row in lessons:
        if row['teacher'] is not None:
            seen[row['teacher']].add((row['day'],row['shift']));loads[row['teacher']]+=row.get('length',1)
    return [dict(teacher_id=t['id'],name=t['name'],visits=len(seen[t['id']]),periods=loads[t['id']],sessions=sorted(seen[t['id']])) for t in data['teachers']]
