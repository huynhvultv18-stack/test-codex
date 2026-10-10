"""Per-class/day session calendars. Zero periods never produce a time slot."""
from copy import deepcopy
from collections import defaultdict
import hashlib,json
SHIFTS=('am','pm')
DAY_NAMES=['Thứ Hai','Thứ Ba','Thứ Tư','Thứ Năm','Thứ Sáu','Thứ Bảy','Chủ nhật']
REFERENCE_WEEK=[{'am':5,'pm':4},{'am':5,'pm':0},{'am':5,'pm':4},{'am':5,'pm':0},{'am':5,'pm':4},{'am':4,'pm':0},{'am':0,'pm':0}]
def reference_config():return dict(schema_version=1,max_periods=5,include_sunday=False,week=deepcopy(REFERENCE_WEEK),class_weeks={})

def normalize(c):
 value=c.get('session_config')
 if value is None:c['session_config']=None;return
 if not isinstance(value,dict) or set(value)-{'schema_version','max_periods','include_sunday','week','class_weeks'}:raise ValueError('session_config có trường/kiểu chưa hỗ trợ')
 v=deepcopy(value);v.setdefault('schema_version',1);v.setdefault('max_periods',5);v.setdefault('class_weeks',{})
 if type(v['schema_version']) is not int or v['schema_version']!=1:raise ValueError('session_config.schema_version phải là1')
 if type(v['max_periods']) is not int or not 1<=v['max_periods']<=8:raise ValueError('max_periods phải là số nguyên1..8')
 def check_week(w):
  if not isinstance(w,list) or len(w)!=7:raise ValueError('Lịch buổi cần7ngày thứHai..Chủnhật; ngày nghỉ ghi0')
  for day in w:
   if not isinstance(day,dict) or set(day)!=set(SHIFTS) or any(type(day[s]) is not int or not 0<=day[s]<=v['max_periods'] for s in SHIFTS):raise ValueError('Số tiết từng buổi phải nguyên0..max_periods;0=NGHỈ')
 check_week(v.get('week'))
 if not isinstance(v['class_weeks'],dict) or any(not isinstance(cid,str) or not cid for cid in v['class_weeks']):raise ValueError('class_weeks phải là đối tượng mã lớp/lịch7ngày')
 for w in v['class_weeks'].values():check_week(w)
 sunday=any(w[6][s]>0 for w in [v['week'],*v['class_weeks'].values()] for s in SHIFTS)
 v.setdefault('include_sunday',sunday)
 if not isinstance(v['include_sunday'],bool) or (sunday and not v['include_sunday']):raise ValueError('Chủnhật có tiết: cần bật include_sunday, không tự bỏ số tiết')
 c['session_config']=v;c['days']=max(c['days'],7);c['periods']=max(c['periods'],v['max_periods'])

def configured_periods(c,cid,day,shift):
 v=c.get('session_config')
 if v:return v['class_weeks'].get(cid,v['week'])[day][shift] if 0<=day<7 else 0
 if day not in c.get('active_days',range(c['days'])):return 0
 return c.get('session_periods',{}).get(shift,c['periods'])

def effective_periods(c,cls,day,shift):
 if c['mode']=='morning' and shift!='am':return 0
 if c['mode']=='mixed' and shift!=cls.get('shift','am'):return 0
 return configured_periods(c,cls['id'],day,shift)

def study_days(c,cid,classes):return [d for d in range(c['days']) if any(effective_periods(c,classes[cid],d,s)>0 for s in SHIFTS)]

def assignment_periods(c,a,classes,d,shift):
 if a.get('activity_shift') and a['activity_shift']!=shift:return 0
 return min(effective_periods(c,classes[cid],d,shift) for cid in (a.get('class_ids') or [a['class_id']]))

def visible_days(c):
 v=c.get('session_config')
 return list(range(7 if v and v['include_sunday'] else 6)) if v else list(range(c['days']))

def plan_snapshot(data,c):return {cl['id']:[{s:effective_periods(c,cl,d,s) for s in SHIFTS} for d in range(7)] for cl in data['classes']}

def impact(data,c,previous):
 classes={cl['id']:cl for cl in data['classes']};affected=[]
 for r in previous or []:
  ids=r.get('class_ids') or [r.get('class_id')]
  if not set(ids)<=set(classes):continue
  if any(r['period']+r.get('length',1)>effective_periods(c,classes[cid],r['day'],r['shift']) for cid in ids):affected.append(deepcopy(r))
 payload=dict(target_grade=c.get('target_grade'),plan=plan_snapshot(data,c),previous=previous or [])
 fingerprint=hashlib.sha256(json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
 return dict(confirmation_required=bool(affected),affected_periods=sum(r.get('length',1)*len(r.get('class_ids') or [r['class_id']]) for r in affected),affected_lessons=affected,confirmation=fingerprint)

def calendar_rows(data,c):
 rows=[]
 for cl in data['classes']:
  for d in visible_days(c):
   for s in SHIFTS:
    n=effective_periods(c,cl,d,s)
    rows.append(dict(class_id=cl['id'],class_name=cl['name'],day=d,day_name=DAY_NAMES[d],shift=s,periods=n,state='NGHỈ' if n==0 else 'HỌC',configured_periods=configured_periods(c,cl['id'],d,s)))
 return rows

def analyze(data,c,background=None):
 """Necessary capacity diagnostics; shared resource availability is not a proof."""
 background=background or [];classes={x['id']:x for x in data['classes']};assign={a['id']:a for a in data['assignments']};busy=set();fixed=list(c['fixed']);rows=[];warnings=[];teacher_slots=defaultdict(set);room_slots=defaultdict(set);teacher_load=defaultdict(int)
 def blocked(kind,i,d,s,p):return any(x['kind']==kind and x['id']==i and x['day']==d and x['shift']==s and ('period' not in x or x['period']==p) for x in c['unavailable'])
 for r in background:
  if r.get('teacher') is not None:teacher_load[(r['teacher'],r['day'],r['shift'])]+=r.get('length',1)
  for p in range(r['period'],r['period']+r.get('length',1)):
   if r.get('teacher') is not None:busy.add(('teacher',r['teacher'],r['day'],r['shift'],p))
   if r.get('room'):busy.add(('room',r['room'],r['day'],r['shift'],p))
 for a in data['assignments']:
  if a.get('is_special') and a.get('fixed_day') is not None and a.get('fixed_period') is not None and a.get('activity_shift'):
   fixed.append(dict(assignment=a['id'],day=a['fixed_day'],shift=a['activity_shift'],period=a['fixed_period']))
 for cl in data['classes']:
  cid=cl['id'];open_slots=set();capacities={};raw=0;sessions=0;days=visible_days(c)
  for d in days:
   for s in SHIFTS:
    n=effective_periods(c,cl,d,s);raw+=n;sessions+=int(n>0)
    usable={p for p in range(n) if not blocked('class',cid,d,s,p)};open_slots.update((d,s,p) for p in usable);capacities[(d,s)]=min(len(usable),c['max_class_session'])
  need=sum(a['count'] for a in data['assignments'] if cid in (a.get('class_ids') or [a['class_id']]))
  used=set();bad=[]
  for f in fixed:
   a=assign.get(f['assignment'])
   if not a or cid not in (a.get('class_ids') or [a['class_id']]):continue
   fs={(f['day'],f['shift'],p) for p in range(f['period'],f['period']+f.get('length',1))}
   if not fs<=open_slots:bad.append(f['assignment']);warnings.append(f'{cid}: tiết cố định {f["assignment"]} rơi vào buổi nghỉ/ngoài số tiết/lịch nghỉ')
   else:used.update(fs)
   resources=([('teacher',a['teacher'])] if a['teacher'] is not None else [])+([('room',f['room'])] if f.get('room') else [])
   if any((k,i,d,s,p) in busy for k,i in resources for d,s,p in fs):warnings.append(f'{cid}: tiết cố định {f["assignment"]} xung đột giáo viên/phòng với lịch khối khóa')
  capacity=sum(capacities.values());reserved=sum(min(n,sum(1 for d,s,p in used if (d,s)==key)) for key,n in capacities.items())
  if need>capacity:warnings.append(f'{cid}: PCCM{need} vượt công suất khả dụng{capacity}; không tự tăng số tiết')
  rows.append(dict(class_id=cid,class_name=cl['name'],weekly_sessions=sessions,weekly_slots=raw,capacity=capacity,required=need,rest_sessions=len(days)*2-sessions,fixed_periods=reserved,capacity_after_fixed=max(0,capacity-reserved),fixed_calendar_conflicts=bad,over_capacity=need>capacity))
 for a in data['assignments']:
  for d in range(c['days']):
   for s in SHIFTS:
    n=assignment_periods(c,a,classes,d,s)
    for p in range(n):
     resources=[('class',cid) for cid in (a.get('class_ids') or [a['class_id']])]+([('teacher',a['teacher'])] if a['teacher'] is not None else [])
     if any(blocked(k,i,d,s,p) or (k,i,d,s,p) in busy for k,i in resources):continue
     rooms=[r for r in a.get('room_ids',[]) if not blocked('room',r,d,s,p) and ('room',r,d,s,p) not in busy]
     if a.get('room_ids') and not rooms:continue
     if a['teacher'] is not None:teacher_slots[a['teacher']].add((d,s,p))
     for room in rooms:room_slots[room].add((d,s,p))
 teacher_availability=[]
 for tid in sorted({a['teacher'] for a in data['assignments'] if a['teacher'] is not None}):
  slots=teacher_slots[tid]
  groups=defaultdict(int)
  for d,s,p in slots:groups[(d,s)]+=1
  available=sum(min(n,max(0,c['max_teacher_session']-teacher_load[(tid,d,s)])) for (d,s),n in groups.items())
  need=sum(a['count'] for a in data['assignments'] if a['teacher']==tid)
  teacher_availability.append(dict(teacher_id=tid,required=need,available_slots=len(slots),residual_session_capacity=available))
  if need>available:warnings.append(f'GV {tid}: cần {need}, công suất sau lịch khóa/lịch nghỉ {available}; không tự mở buổi nghỉ')
 return dict(classes=rows,weekly_slots=sum(r['weekly_slots'] for r in rows),capacity=sum(r['capacity'] for r in rows),required=sum(r['required'] for r in rows),weekly_sessions=sum(r['weekly_sessions'] for r in rows),rest_sessions=sum(r['rest_sessions'] for r in rows),fixed_periods=sum(r['fixed_periods'] for r in rows),capacity_after_fixed=sum(r['capacity_after_fixed'] for r in rows),warnings=warnings,teacher_availability=teacher_availability,room_availability=[dict(room_id=r,available_slots=len(ps)) for r,ps in sorted(room_slots.items())],calendar=calendar_rows(data,c),session_config=deepcopy(c.get('session_config')))
