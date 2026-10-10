"""Independent schedule verification. Does not read CP-SAT variables."""
from collections import Counter, defaultdict

DEFAULT_CONFIG = dict(mode='both', days=6, periods=5, max_class_session=5,
                      max_teacher_session=5, time_limit=30, workers=4, seed=17,
                      technical_only=True, rooms=[], unavailable=[], fixed=[],
                      preferences=[], priorities=['gaps','visits','distribution','concentration','preferences','changes'])

def config_with_defaults(raw=None):
    c={**DEFAULT_CONFIG, **(raw or {})}
    if c['mode'] not in ('morning','both','mixed'): raise ValueError('Chế độ không hợp lệ')
    for name,low,high in [('days',1,6),('periods',1,8),('max_class_session',1,8),('max_teacher_session',1,8),('workers',1,16),('seed',0,2147483647)]:
        v=c[name]
        if isinstance(v,bool) or not isinstance(v,int) or not low<=v<=high: raise ValueError(f'{name} phải nằm trong {low}..{high}')
    if not isinstance(c['time_limit'],(int,float)) or not 0<c['time_limit']<=600: raise ValueError('Giới hạn giải 0..600 giây')
    names={'gaps','visits','distribution','concentration','preferences','changes'}
    if set(c['priorities']) != names or len(c['priorities']) != 6: raise ValueError('priorities phải chứa đủ 6 mục tiêu, mỗi mục một lần')
    for key in ('rooms','unavailable','fixed','preferences'):
        if not isinstance(c[key],list): raise ValueError(f'{key} phải là danh sách')
    roomids=[r['id'] for r in c['rooms']]
    if len(set(roomids)) != len(roomids) or any(not isinstance(r,str) or not r for r in roomids): raise ValueError('Mã phòng trùng/rỗng')
    return c

def class_shifts(cls,c):
    return ['am'] if c['mode']=='morning' else ['am','pm'] if c['mode']=='both' else [cls.get('shift','am')]

def validate_problem(data,config):
    errors=[]
    def err(msg): errors.append(msg)
    tables={k:{x['id']:x for x in data[k]} for k in ('classes','teachers','assignments')}
    for k,t in tables.items():
        if len(t)!=len(data[k]): err('Mã trùng: '+k)
    subjects={s['id'] for s in data['subjects']};rooms={r['id'] for r in config['rooms']}
    for cls in data['classes']:
        if cls.get('shift','am') not in ('am','pm'): err('Ca lớp không hợp lệ: '+cls['id'])
    for a in data['assignments']:
        if a['teacher'] not in tables['teachers'] or a['class_id'] not in tables['classes'] or a['subject_id'] not in subjects: err('Phân công tham chiếu sai: '+a['id'])
        if not isinstance(a['count'],int) or isinstance(a['count'],bool) or a['count']<1: err('Số tiết không hợp lệ: '+a['id'])
        d=a.get('double_count',0)
        if not isinstance(d,int) or isinstance(d,bool) or d<0 or 2*d>a['count']: err('Số cặp tiết đôi không hợp lệ: '+a['id'])
        for room in a.get('room_ids',[]):
            if room not in rooms: err('Phòng chưa khai báo: '+room)
    for item in config['unavailable']+config['preferences']:
        if item.get('kind') not in ('teacher','class','room'): err('kind phải là teacher/class/room'); continue
        ids=tables['teachers'] if item['kind']=='teacher' else tables['classes'] if item['kind']=='class' else {r['id']:r for r in config['rooms']}
        if item.get('id') not in ids: err('Đối tượng lịch nghỉ/nguyện vọng không tồn tại')
        if not isinstance(item.get('day'),int) or not 0<=item['day']<config['days']: err('day nằm ngoài lịch')
        if item.get('shift') not in ('am','pm'): err('shift không hợp lệ')
        if 'period' in item and (not isinstance(item['period'],int) or not 0<=item['period']<config['periods']): err('period nằm ngoài lịch')
        if 'weight' in item and (not isinstance(item['weight'],int) or not 0<=item['weight']<=1000): err('weight phải là số nguyên 0..1000')
    for f in config['fixed']:
        if f.get('assignment') not in tables['assignments']: err('Tiết cố định tham chiếu sai phân công'); continue
        if f.get('length',1) not in (1,2): err('length của tiết cố định phải là 1 hoặc 2')
        if not isinstance(f.get('day'),int) or not 0<=f['day']<config['days']: err('Ngày cố định ngoài lịch')
        if f.get('shift') not in ('am','pm'): err('Ca cố định không hợp lệ')
        if not isinstance(f.get('period'),int) or not 0<=f['period']<=config['periods']-f.get('length',1): err('Tiết cố định ngoài buổi')
        if f.get('room') is not None and f['room'] not in rooms: err('Phòng cố định chưa khai báo')
    for item in data.get('issues',[]):
        if item['level']=='ERROR': err(item['message'])
    if not config['technical_only'] and (data.get('pending_special') or any(t.get('status')!='VERIFIED' or not t.get('full_name') for t in data['teachers']) or any(i['level']=='WARNING' for i in data.get('issues',[]))):
        err('PCCM chưa được nghiệm thu: chỉ được kiểm thử kỹ thuật có điều kiện')
    return errors

def blocked(c,kind,identifier,d,sh,p):
    return any(x['kind']==kind and x['id']==identifier and x['day']==d and x['shift']==sh and ('period' not in x or x['period']==p) for x in c['unavailable'])

def signature(row):
    return (row['assignment'],row['day'],row['shift'],row['period'],row.get('length',1),row.get('room'))

def verify_schedule(data,config,lessons,previous=None,scope=None):
    c=config_with_defaults(config);assign={a['id']:a for a in data['assignments']};classes={x['id']:x for x in data['classes']}
    errors=[]; count=Counter();used=Counter();c_load=Counter();t_load=Counter();doubles=Counter()
    for row in lessons:
        a=assign.get(row.get('assignment'))
        if not a: errors.append('Phân công không tồn tại'); continue
        if row.get('teacher')!=a['teacher'] or row.get('class_id')!=a['class_id'] or row.get('subject_id')!=a['subject_id']:
            errors.append('Sai giáo viên/lớp/môn phụ trách')
        d,sh,p,L=row['day'],row['shift'],row['period'],row.get('length',1)
        if L not in (1,2) or not 0<=d<c['days'] or not 0<=p<=c['periods']-L or sh not in class_shifts(classes[a['class_id']],c):
            errors.append('Ngoài ca/ngày/buổi hoặc tiết đôi qua buổi');continue
        count[a['id']]+=L;doubles[a['id']]+=int(L==2)
        room=row.get('room')
        if a.get('room_ids') and room not in a['room_ids']:errors.append('Sai phòng chức năng')
        if not a.get('room_ids') and room is not None:errors.append('Gán phòng không thuộc phân công')
        for period in range(p,p+L):
            for kind,identity in [('teacher',a['teacher']),('class',a['class_id'])]+([('room',room)] if room else []):
                key=(kind,identity,d,sh,period);used[key]+=1
                if blocked(c,kind,identity,d,sh,period):errors.append('Vi phạm lịch nghỉ')
            c_load[(a['class_id'],d,sh)]+=1;t_load[(a['teacher'],d,sh)]+=1
    conflict_count=sum(max(0,n-1) for n in used.values())
    if conflict_count:errors.append(f'{conflict_count} xung đột giáo viên/lớp/phòng')
    for a in assign.values():
        if count[a['id']]!=a['count']:errors.append('Sai số tiết: '+a['id'])
        if doubles[a['id']]!=a.get('double_count',0):errors.append('Sai số cặp tiết đôi: '+a['id'])
    if any(n>c['max_class_session'] for n in c_load.values()):errors.append('Quá tiết tối đa/lớp/buổi')
    if any(n>c['max_teacher_session'] for n in t_load.values()):errors.append('Quá tiết tối đa/GV/buổi')
    for f in c['fixed']:
        if not any(row['assignment']==f['assignment'] and row['day']==f['day'] and row['shift']==f['shift'] and row['period']==f['period'] and row.get('length',1)==f.get('length',1) and ('room' not in f or row.get('room')==f['room']) for row in lessons):errors.append('Thiếu tiết cố định')
    if scope and previous:
        current=Counter(signature(r) for r in lessons)
        for r in previous:
            if not in_scope(r,scope) and current[signature(r)]<Counter(signature(x) for x in previous if not in_scope(x,scope))[signature(r)]:errors.append('Thay đổi ngoài phạm vi xếp lại')
    return dict(valid=not errors, conflicts=conflict_count, errors=errors,
                required=sum(a['count'] for a in assign.values()), placed=sum(r.get('length',1) for r in lessons))

def in_scope(row,scope):
    return row['class_id'] in scope.get('classes',[]) or row['teacher'] in scope.get('teachers',[])

def metrics(data,c,lessons,previous=None):
    occ=defaultdict(set);daily=Counter();pref=0
    for row in lessons:
        a=next(a for a in data['assignments'] if a['id']==row['assignment'])
        for p in range(row['period'],row['period']+row.get('length',1)):
            occ[(a['teacher'],row['day'],row['shift'])].add(p)
            daily[(a['class_id'],a['subject_id'].split(':')[0],row['day'])]+=1
            for q in c['preferences']:
                identity=a['teacher'] if q['kind']=='teacher' else a['class_id'] if q['kind']=='class' else row.get('room')
                if identity==q['id'] and row['day']==q['day'] and row['shift']==q['shift'] and ('period' not in q or p==q['period']):pref+=q.get('weight',1)
    gaps=sum(max(ps)-min(ps)+1-len(ps) for ps in occ.values())
    subjects={(a['class_id'],a['subject_id'].split(':')[0]) for a in data['assignments']}
    distribution=sum(max(daily[(cl,s,d)] for d in range(c['days']))-min(daily[(cl,s,d)] for d in range(c['days'])) for cl,s in subjects)
    changes=0
    if previous:
        old=Counter(signature(r) for r in previous);cur=Counter(signature(r) for r in lessons)
        changes=sum((old-cur).values())
    return dict(gaps=gaps,visits=len(occ),distribution=distribution,
                concentration=sum(max(0,n-1) for n in daily.values()),preferences=pref,changes=changes)
