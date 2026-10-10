"""Independent time metrics and CP model extension share definitions, not solutions."""
from collections import defaultdict
from copy import deepcopy
from .resources import teachers_of
from .sessions import effective_periods
NAMES=['gaps','visits','days','waiting','fragmentation','distribution','preferences','fairness','concentration','changes']
DEFAULT=dict(enabled=False,mode='BALANCED',priorities=NAMES,waiting_enabled=False,fairness_enabled=True,seeds=[],period_times=[],lunch_break=None,phase_weights=dict(gaps=30,visits=25,days=25,waiting=10,fragmentation=3,distribution=3,preferences=2,fairness=1,concentration=1,changes=1))
def normalize(c):
 raw=c.get('teacher_time',{})
 if not isinstance(raw,dict) or set(raw)-set(DEFAULT):raise ValueError('teacher_time có trường/kiểu chưa hỗ trợ')
 t={**deepcopy(DEFAULT),**deepcopy(raw)}
 if any(type(t[k]) is not bool for k in ['enabled','waiting_enabled','fairness_enabled']):raise ValueError('Tiêu chí thời gian GV phải boolean')
 if t['mode'] not in ['FAST','BALANCED','PROVE_OPTIMAL']:raise ValueError('Chế độ tối ưu GV phải FAST/BALANCED/PROVE_OPTIMAL')
 if not isinstance(t['priorities'],list) or len(t['priorities'])!=len(NAMES) or any(not isinstance(x,str) for x in t['priorities']) or set(t['priorities'])!=set(NAMES):raise ValueError('Thứ tự GV cần đủ10mục tiêu duy nhất')
 if not isinstance(t['seeds'],list) or len(t['seeds'])>4 or any(type(x) is not int or not 0<=x<=2147483647 for x in t['seeds']) or len(set(t['seeds']))!=len(t['seeds']):raise ValueError('Multi-seed cần tối đa4seed nguyên duy nhất')
 weights=t['phase_weights']
 if not isinstance(weights,dict) or set(weights)!=set(NAMES) or any(type(v) is not int or not 0<=v<=100 for v in weights.values()) or sum(weights.values())<=0:raise ValueError('Ngân sách phase GV phải đủ10trọng số0..100')
 if not isinstance(t['period_times'],list):raise ValueError('period_times cần danh sách giờ thực tế')
 keys=set();group=defaultdict(list)
 for r in t['period_times']:
  if not isinstance(r,dict) or set(r)!={'day','shift','period','start','end'} or any(type(r[k]) is not int for k in ['day','period','start','end']) or not 0<=r['day']<7 or r['shift'] not in ['am','pm'] or not 0<=r['period']<8 or not 0<=r['start']<r['end']<=1440:raise ValueError('Giờ học: ngày0..6,tiết0..7,start/end phút nguyên trong ngày')
  key=(r['day'],r['shift'],r['period'])
  if key in keys:raise ValueError('Trùng ô giờ học thực tế')
  keys.add(key);group[(r['day'],r['shift'])].append(r)
 for (d,s),rows in group.items():
  ordered=sorted(rows,key=lambda r:r['period'])
  if any(a['end']>b['start'] for a,b in zip(ordered,ordered[1:])):raise ValueError('Giờ tiết thực tế chồng nhau hoặc không theo thứ tự')
 for d in range(7):
  if group[(d,'am')] and group[(d,'pm')] and max(r['end'] for r in group[(d,'am')])>min(r['start'] for r in group[(d,'pm')]):raise ValueError('Hai buổi có giờ thực tế chồng nhau; cần sửa giờ, không coi hai ca tách biệt')
 lunch=t['lunch_break']
 if lunch is not None and (not isinstance(lunch,dict) or set(lunch)!={'start','end'} or any(type(lunch[k]) is not int for k in ['start','end']) or not 0<=lunch['start']<lunch['end']<=1440):raise ValueError('lunch_break cần start/end phút nguyên, không tự suy ra nghỉ trưa')
 if lunch and any(r['start']<lunch['end'] and lunch['start']<r['end'] for r in t['period_times']):raise ValueError('Tiết học chồng giờ nghỉ trưa đã khai báo')
 c['teacher_time']=t

def settings(c):
 t=c['teacher_time']
 if not t['enabled']:return c['priorities'],c['objective_settings'],c['phase_fractions'],c['advance_on_incumbent']
 opts={k:dict(enabled=True,weight=1) for k in NAMES}
 for k in c['objective_settings']:opts[k]=c['objective_settings'][k]
 opts['waiting']['enabled']=t['waiting_enabled'];opts['fairness']['enabled']=t['fairness_enabled']
 return t['priorities'],opts,t['phase_weights'],t['mode']=='BALANCED' and c['advance_on_incumbent']

def clock(c,data,background):
 declared={(r['day'],r['shift'],r['period']):(r['start'],r['end']) for r in c['teacher_time']['period_times']}
 possible={(d,s,p) for cl in data['classes'] for d in range(c['days']) for s in ['am','pm'] for p in range(effective_periods(c,cl,d,s))}
 possible.update((r['day'],r['shift'],p) for r in background for p in range(r['period'],r['period']+r.get('length',1)))
 real=bool(declared) and possible<=set(declared) and c['teacher_time']['lunch_break'] is not None
 return dict(kind='REAL_MINUTES' if real else 'PROXY',unit='phút (đã trừ nghỉ trưa quy định)' if real else 'ô tiết đại diện; không phải phút',slots=declared,lunch=c['teacher_time']['lunch_break'],reason='' if real else 'Chưa đủ giờ thực tế cho miền xếp/lịch khóa hoặc chưa khai báo giờ nghỉ trưa; không tự suy ra thời gian')

def wait_cost(c,measurement,d,am_last,pm_first):
 if measurement['kind']=='PROXY':return c['periods']-1-am_last+pm_first
 start=measurement['slots'][(d,'am',am_last)][1];end=measurement['slots'][(d,'pm',pm_first)][0];lunch=measurement['lunch']
 excluded=max(0,min(end,lunch['end'])-max(start,lunch['start']))
 return max(0,end-start-excluded)

def _from_rows(data,c,rows,measurement):
 occ=defaultdict(set);loads=defaultdict(int)
 for r in rows:
  for tid in teachers_of(r):
   occ[(tid,r['day'],r['shift'])].update(range(r['period'],r['period']+r.get('length',1)));loads[tid]+=r.get('length',1)
 ids={t['id'] for t in data['teachers']}|{k[0] for k in occ};teachers=[];names={t['id']:t for t in data['teachers']}
 for tid in sorted(ids):
  sessions=[(d,s,ps) for (t,d,s),ps in occ.items() if t==tid and ps];gap=sum(max(ps)-min(ps)+1-len(ps) for d,s,ps in sessions);frag=sum(sum(p-1 not in ps for p in ps) for d,s,ps in sessions);days={d for d,s,ps in sessions};waiting=0
  for d in days:
   am=occ[(tid,d,'am')];pm=occ[(tid,d,'pm')]
   if am and pm:waiting+=wait_cost(c,measurement,d,max(am),min(pm))
  teachers.append(dict(teacher_id=tid,name=names.get(tid,{}).get('name',tid),periods=loads[tid],gaps=gap,visits=len(sessions),days=len(days),waiting=waiting,fragmentation=frag,day_list=sorted(days),sessions=[dict(day=d,shift=s,periods=sorted(ps),gaps=max(ps)-min(ps)+1-len(ps),fragmentation=sum(p-1 not in ps for p in ps)) for d,s,ps in sorted(sessions)]))
 totals={k:sum(t[k] for t in teachers) for k in ['gaps','visits','days','waiting','fragmentation']};totals['fairness']=max([t['gaps'] for t in teachers] or [0])
 return dict(totals=totals,teachers=teachers)

def evaluate(data,c,lessons,background=None):
 background=background or [];measurement=clock(c,data,background);combined=_from_rows(data,c,background+lessons,measurement);base=_from_rows(data,c,background,measurement)
 return {**combined,'locked_baseline':base['totals'],'change_from_locked':{k:combined['totals'][k]-base['totals'][k] for k in combined['totals']},'waiting_kind':measurement['kind'],'waiting_unit':measurement['unit'],'waiting_note':measurement['reason'],'fairness_definition':'Maximum weekly internal gaps of one teacher; equal names are separate IDs','all_rows_scope':'Selected grade + immutable known background; gaps/fragmentation may decrease by filling a locked hole'}

def add_model(m,data,c,occupied,visit_vars,background):
 """Time auxiliaries use actual occupancy; no guessed time or fake absence visits."""
 measurement=clock(c,data,background);days=[];fragments=[];waiting=[];teacher_gaps=defaultdict(list)
 for t in data['teachers']:
  tid=t['id']
  for d in range(c['days']):
   day=m.new_bool_var('teacher_day');m.add_max_equality(day,[visit_vars[(tid,d,s)] for s in ['am','pm']]);days.append(day)
   endpoints={}
   for s in ['am','pm']:
    cells=[occupied[(tid,d,s,p)] for p in range(c['periods'])]
    fragments.append(cells[0])
    for p in range(1,c['periods']):
     onset=m.new_bool_var('fragment_start');m.add(onset<=cells[p]);m.add(onset+cells[p-1]<=1);m.add(onset>=cells[p]-cells[p-1]);fragments.append(onset)
    for p in range(1,c['periods']-1):
     before=m.new_bool_var('fair_before');after=m.new_bool_var('fair_after');gap=m.new_bool_var('fair_gap');m.add_max_equality(before,cells[:p]);m.add_max_equality(after,cells[p+1:]);m.add(gap<=before);m.add(gap<=after);m.add(gap+cells[p]<=1);m.add(gap>=before+after-cells[p]-1);teacher_gaps[tid].append(gap)
    if c['teacher_time']['waiting_enabled']:
     endpoints[s]=[]
     for p in range(c['periods']):
      end=m.new_bool_var('last_am' if s=='am' else 'first_pm');other=cells[p+1:] if s=='am' else cells[:p];m.add(end<=cells[p])
      if other:
       any_other=m.new_bool_var('endpoint_other');m.add_max_equality(any_other,other);m.add(end+any_other<=1);m.add(end>=cells[p]-any_other)
      else:m.add(end==cells[p])
      endpoints[s].append(end)
   if c['teacher_time']['waiting_enabled']:
    for a,last in enumerate(endpoints['am']):
     for p,first in enumerate(endpoints['pm']):
      # Only actual-clock pairs with declared bell times can have occupancy.
      if measurement['kind']=='REAL_MINUTES' and ((d,'am',a) not in measurement['slots'] or (d,'pm',p) not in measurement['slots']):continue
      cost=wait_cost(c,measurement,d,a,p)
      if not cost:continue
      pair=m.new_bool_var('both_sessions_pair');m.add(pair<=last);m.add(pair<=first);m.add(pair>=last+first-1);waiting.append(pair*cost)
 maxgap=m.new_int_var(0,c['days']*2*max(0,c['periods']-2),'fair_max_gap');gapvars=[]
 for tid in teacher_gaps:
  g=m.new_int_var(0,c['days']*2*max(0,c['periods']-2),'teacher_week_gaps');m.add(g==sum(teacher_gaps[tid]));gapvars.append(g)
 if gapvars:m.add_max_equality(maxgap,gapvars)
 else:m.add(maxgap==0)
 return dict(days=sum(days),fragmentation=sum(fragments),waiting=sum(waiting),fairness=maxgap)
