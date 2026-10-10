"""Configurable pedagogy penalties. Empty rules add no school-specific policy."""
from collections import Counter,defaultdict
from .sessions import study_days,effective_periods

def active_days(c):return c.get('active_days',list(range(c['days'])))
def session_periods(c,shift):return c.get('session_periods',{}).get(shift,c['periods'])

def class_ids(a):return a.get('class_ids') or [a['class_id']]

def allowed_shifts(a,classes,c):
    def shifts(cl):return {'am'} if c['mode']=='morning' else {'am','pm'} if c['mode']=='both' else {classes[cl].get('shift','am')}
    common=set.intersection(*(shifts(cl) for cl in class_ids(a)))
    if a.get('activity_shift'):common &= {a['activity_shift']}
    return [s for s in ['am','pm'] if s in common]

def rule_for(cl,subject,data,c):
    grade=next(x.get('grade',0) for x in data['classes'] if x['id']==cl)
    matches=[r for r in c.get('subject_rules',[]) if r['subject']==subject and (not r.get('grades') or grade in r['grades'])]
    if len(matches)>1:raise ValueError('Nhiều subject_rules cùng khớp một lớp/môn')
    return {**dict(daily_soft_max=1,distribution_weight=1,concentration_weight=1,adjacent_weight=0,
                preferred_periods=[],period_weight=0),**(matches[0] if matches else {})}

def features(data,c,lessons):
    classes={cl['id']:cl for cl in data['classes']};assign={a['id']:a for a in data['assignments']};daily=Counter();pos=set();doubles=set();totals=Counter()
    for a in data['assignments']:
        if a.get('is_special') or a['subject_id'].startswith('HD'):continue
        for cl in class_ids(a):totals[(cl,a['subject_id'].split(':')[0])]+=a['count']
    for row in lessons:
        a=assign.get(row.get('assignment'))
        if not a:continue
        if a.get('is_special') or a['subject_id'].startswith('HD'):continue
        base=a['subject_id'].split(':')[0]
        for cl in class_ids(a):
            daily[(cl,base,row['day'])]+=row.get('length',1)
            for p in range(row['period'],row['period']+row.get('length',1)):pos.add((cl,base,row['day'],row['shift'],p))
            if row.get('length',1)==2:doubles.add((cl,base,row['day'],row['shift'],row['period']))
    weighted_dist=weighted_con=adjacency=period_pref=heavy=0;values={};dist_upper=con_upper=0
    for (cl,sub),total in totals.items():
        rule=rule_for(cl,sub,data,c);ns=[daily[(cl,sub,d)] for d in study_days(c,cl,classes)] or [0]
        weighted_dist+=rule['distribution_weight']*(max(ns)-min(ns));dist_upper+=rule['distribution_weight']*min(total,2*c['periods'])
        con_upper+=rule['concentration_weight']*max(0,total-rule['daily_soft_max'])
        for d in study_days(c,cl,classes):
            values[('daily',cl,sub,d)]=daily[(cl,sub,d)]
            ex=max(0,daily[(cl,sub,d)]-rule['daily_soft_max']);weighted_con+=rule['concentration_weight']*ex
            values[('excess',cl,sub,d)]=ex
            for sh in ['am','pm']:
                for p in range(effective_periods(c,classes[cl],d,sh)):
                    present=(cl,sub,d,sh,p) in pos;values[('subject_occ',cl,sub,d,sh,p)]=int(present)
                    if present and rule['preferred_periods'] and p not in rule['preferred_periods']:period_pref+=rule['period_weight']
                for p in range(max(0,effective_periods(c,classes[cl],d,sh)-1)):
                    pair=(cl,sub,d,sh,p) in pos and (cl,sub,d,sh,p+1) in pos
                    excess=pair and (cl,sub,d,sh,p) not in doubles
                    values[('adj_pair',cl,sub,d,sh,p)]=int(pair);values[('adj_penalty',cl,sub,d,sh,p)]=int(excess)
                    adjacency+=rule['adjacent_weight']*int(excess)
        values[('min',cl,sub)]=min(ns);values[('max',cl,sub)]=max(ns)
        # Conservative, documented upper bounds for a 0..100 scale; nonnegative
        # penalties cannot exceed these even under concentrated placement.
        con_upper+=rule['adjacent_weight']*total
    heavy_set=set(c.get('heavy_subjects',[]));limit=c.get('heavy_run_limit',2);weight=c.get('heavy_weight',0)
    if heavy_set and weight:
        for cl in [x['id'] for x in data['classes']]:
            for d in study_days(c,cl,classes):
                for sh in ['am','pm']:
                    flags=[any((cl,s,d,sh,p) in pos for s in heavy_set) for p in range(effective_periods(c,classes[cl],d,sh))]
                    for p,v in enumerate(flags):values[('heavy_occ',cl,d,sh,p)]=int(v)
                    for p in range(max(0,effective_periods(c,classes[cl],d,sh)-limit)):
                        v=int(all(flags[p:p+limit+1]));values[('heavy_window',cl,d,sh,p)]=v;heavy+=weight*v
        con_upper+=weight*len(data['classes'])*c['days']*2*max(0,c['periods']-limit)
    total_con=weighted_con+adjacency+heavy
    return dict(values=values,distribution_weighted=weighted_dist,concentration_weighted=total_con,
        daily_concentration=weighted_con,unnecessary_adjacency=adjacency,subject_period_preferences=period_pref,heavy_run_penalty=heavy,
        distribution_upper=dist_upper,concentration_upper=con_upper,
        distribution_penalty_100=round(100*weighted_dist/dist_upper,4) if dist_upper else 0,
        concentration_penalty_100=round(100*total_con/con_upper,4) if con_upper else 0,
        daily_matrix=[dict(class_id=cl,subject=sub,days=[daily[(cl,sub,d)] for d in range(c['days'])]) for cl,sub in sorted(totals)])

def add_quality_model(m,data,c,variables):
    cover=defaultdict(list);double=defaultdict(list);daily=defaultdict(list);subjects=set();hints=[];dist=[];con=[];prefs=[]
    classes={cl['id']:cl for cl in data['classes']};rules={}
    for v,row in variables:
        if row.get('is_special') or row['subject_id'].startswith('HD'):continue
        sub=row['subject_id'].split(':')[0]
        for cl in class_ids(row):
            subjects.add((cl,sub));daily[(cl,sub,row['day'])].append(v*row['length'])
            for p in range(row['period'],row['period']+row['length']):cover[(cl,sub,row['day'],row['shift'],p)].append(v)
            if row['length']==2:double[(cl,sub,row['day'],row['shift'],row['period'])].append(v)
            key=(cl,sub)
            if key not in rules:rules[key]=rule_for(cl,sub,data,c)
            rule=rules[key]
            if rule['preferred_periods'] and rule['period_weight']:
                hits=sum(p not in rule['preferred_periods'] for p in range(row['period'],row['period']+row['length']))
                prefs.append(v*hits*rule['period_weight'])
    position={}
    for cl,sub in sorted(subjects):
        rule=rules[(cl,sub)];loads=[]
        for d in study_days(c,cl,classes):
            z=m.new_int_var(0,2*c['periods'],'daily');m.add(z==sum(daily[(cl,sub,d)]));loads.append(z);hints.append((z,('daily',cl,sub,d)))
            ex=m.new_int_var(0,2*c['periods'],'excess');m.add_max_equality(ex,[z-rule['daily_soft_max'],0]);con.append(ex*rule['concentration_weight']);hints.append((ex,('excess',cl,sub,d)))
            if rule['adjacent_weight'] or (sub in c.get('heavy_subjects',[]) and c.get('heavy_weight',0)):
                for sh in ['am','pm']:
                    for p in range(effective_periods(c,classes[cl],d,sh)):
                        v=m.new_bool_var('subject_occ');m.add(v==sum(cover[(cl,sub,d,sh,p)]));position[(cl,sub,d,sh,p)]=v;hints.append((v,('subject_occ',cl,sub,d,sh,p)))
                    if rule['adjacent_weight']:
                        for p in range(max(0,effective_periods(c,classes[cl],d,sh)-1)):
                            a,b=position[(cl,sub,d,sh,p)],position[(cl,sub,d,sh,p+1)];pair=m.new_bool_var('adj_pair');pen=m.new_bool_var('adj_penalty')
                            m.add(pair<=a);m.add(pair<=b);m.add(pair>=a+b-1)
                            m.add(pen==pair-sum(double[(cl,sub,d,sh,p)]));con.append(pen*rule['adjacent_weight'])
                            hints.extend([(pair,('adj_pair',cl,sub,d,sh,p)),(pen,('adj_penalty',cl,sub,d,sh,p))])
        lo=m.new_int_var(0,2*c['periods'],'min');hi=m.new_int_var(0,2*c['periods'],'max');m.add_min_equality(lo,loads);m.add_max_equality(hi,loads)
        dist.append((hi-lo)*rule['distribution_weight']);hints.extend([(lo,('min',cl,sub)),(hi,('max',cl,sub))])
    heavy_set=set(c.get('heavy_subjects',[]));limit=c.get('heavy_run_limit',2);weight=c.get('heavy_weight',0)
    if heavy_set and weight:
        for cl in [x['id'] for x in data['classes']]:
            for d in study_days(c,cl,classes):
                for sh in ['am','pm']:
                    flags=[]
                    for p in range(effective_periods(c,classes[cl],d,sh)):
                        choices=[position[(cl,s,d,sh,p)] for s in heavy_set if (cl,s,d,sh,p) in position]
                        v=m.new_bool_var('heavy_occ');m.add(v==sum(choices));flags.append(v);hints.append((v,('heavy_occ',cl,d,sh,p)))
                    for p in range(max(0,effective_periods(c,classes[cl],d,sh)-limit)):
                        v=m.new_bool_var('heavy_window');m.add(v<=flags[p])
                        for flag in flags[p:p+limit+1]:m.add(v<=flag)
                        m.add(v>=sum(flags[p:p+limit+1])-limit);con.append(v*weight);hints.append((v,('heavy_window',cl,d,sh,p)))
    return dict(distribution=sum(dist),concentration=sum(con),subject_preferences=sum(prefs)),hints

def add_subject_hard_limits(m,data,c,variables):
    classes={cl['id']:cl for cl in data['classes']};grades={x['id']:x.get('grade',0) for x in data['classes']}
    for hard in c.get('subject_hard_limits',[]):
        for cl,grade in grades.items():
            if hard.get('grades') and grade not in hard['grades']:continue
            for d in study_days(c,cl,classes):
                terms=[v*r['length'] for v,r in variables if cl in class_ids(r) and r['day']==d and r['subject_id'].split(':')[0]==hard['subject']]
                m.add(sum(terms)<=hard['max_daily'])
