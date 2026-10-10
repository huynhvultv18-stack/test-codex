"""CP-SAT time-indexed assignment blocks with strict hard constraints.

No greedy fallback or partial schedule. Lexicographic objectives are locked only
after proof; budget exhaustion retains the best independently verified solution.
"""
from collections import defaultdict, Counter
import time
from ortools.sat.python import cp_model
from .validation import (config_with_defaults,validate_problem,class_shifts,blocked,
                         signature,in_scope,verify_schedule,metrics)

def solve(data, config=None, previous=None, scope=None, progress=None):
    start=time.monotonic();c=config_with_defaults(config);previous=previous or []
    errors=validate_problem(data,c)
    if errors: raise ValueError('\n'.join(errors))
    if scope is not None:
        if not isinstance(scope,dict) or set(scope)-{'classes','teachers'}:
            raise ValueError('Phạm vi xếp lại phải là JSON classes/teachers')
        if not all(isinstance(scope.get(k,[]),list) for k in ('classes','teachers')) or not (scope.get('classes') or scope.get('teachers')):
            raise ValueError('Phạm vi xếp lại không được rỗng')
    if scope:
        if not previous: raise ValueError('Xếp lại cục bộ cần lịch trước')
        if not set(scope.get('classes',[]))<=set(x['id'] for x in data['classes']) or not set(scope.get('teachers',[]))<=set(x['id'] for x in data['teachers']):raise ValueError('Phạm vi xếp lại có mã chưa tồn tại')
    diagnoses=[]
    required=sum(a['count'] for a in data['assignments'])
    classes={x['id']:x for x in data['classes']}
    for cls in data['classes']:
        need=sum(a['count'] for a in data['assignments'] if a['class_id']==cls['id'])
        capacity=sum(min(c['max_class_session'],sum(not blocked(c,'class',cls['id'],d,sh,p) for p in range(c['periods']))) for d in range(c['days']) for sh in class_shifts(cls,c))
        if need>capacity:diagnoses.append(f"Lớp {cls['name']}: cần {need}, sức chứa {capacity} tiết")
    for t in data['teachers']:
        related=[a for a in data['assignments'] if a['teacher']==t['id']]
        for shifts in [('am',),('pm',),('am','pm')]:
            need=sum(a['count'] for a in related if set(class_shifts(classes[a['class_id']],c))<=set(shifts))
            cap=sum(min(c['max_teacher_session'],sum(not blocked(c,'teacher',t['id'],d,sh,p) for p in range(c['periods']))) for d in range(c['days']) for sh in shifts)
            if need>cap:diagnoses.append(f"GV {t['id']} — {t['name']}: cần {need}, sức chứa {cap} tiết ({'/'.join(shifts)})")
    def empty(status,reason):
        return dict(status=status,lessons=[],required=required,placed=0,conflicts=0,
                    elapsed_seconds=round(time.monotonic()-start,3),diagnostics=reason,
                    metrics=None,phases=[],global_optimal_proven=False,
                    lexicographic_optimal_proven=False,optimality_scope='local_frozen' if scope else 'full_model',
                    technical_only=c['technical_only'],production_ready=False,
                    unscheduled_special=sum(x['count'] for x in data.get('pending_special',[])))
    if diagnoses:
        result=empty('INFEASIBLE',diagnoses);result['proof']='Necessary capacity bound';return result
    m=cp_model.CpModel();vars=[];by_assign=defaultdict(list);cover=defaultdict(list);daily=defaultdict(list)
    maxslots=c['days']*2*c['periods'];pref_terms=[];change_terms=[];assumptions={}
    old=Counter(signature(r) for r in previous)
    aid={a['id']:a for a in data['assignments']}
    for a in data['assignments']:
        doubles=a.get('double_count',0)
        for length,n in [(1,a['count']-2*doubles),(2,doubles)]:
            if not n:continue
            group=[]
            for d in range(c['days']):
                for sh in class_shifts(classes[a['class_id']],c):
                    for p in range(c['periods']-length+1):
                        for room in a.get('room_ids') or [None]:
                            resources=[('teacher',a['teacher']),('class',a['class_id'])]+([('room',room)] if room else [])
                            if any(blocked(c,k,i,d,sh,pp) for k,i in resources for pp in range(p,p+length)):continue
                            v=m.new_bool_var(f'x_{a["id"]}_{length}_{d}_{sh}_{p}_{room}')
                            row=dict(assignment=a['id'],teacher=a['teacher'],class_id=a['class_id'],subject_id=a['subject_id'],
                                     subject=a['subject'],day=d,shift=sh,period=p,length=length,room=room)
                            vars.append((v,row));group.append(v);by_assign[a['id']].append((v,row))
                            for pp in range(p,p+length):
                                for kind,identity in resources:cover[(kind,identity,d,sh,pp)].append(v)
                            daily[(a['class_id'],a['subject_id'].split(':')[0],d)].append((v,length))
                            for q in c['preferences']:
                                if (q['kind'],q['id']) in resources and q['day']==d and q['shift']==sh:
                                    hits=length if 'period' not in q else int(p<=q['period']<p+length)
                                    if hits:pref_terms.append(v*hits*q.get('weight',1))
                            if old[signature(row)]:change_terms.append(v)
            tag=m.new_bool_var('pccm_'+a['id']+'_'+str(length));m.add_assumption(tag)
            assumptions[tag.index]=f"PCCM {a['id']}: {n} bloc(s) × {length}, lớp {a['class_id']}, GV {a['teacher']}"
            m.add(sum(group)==n).only_enforce_if(tag)
    for key,vs in cover.items():m.add_at_most_one(vs)
    for kind,items,limit in [('teacher',data['teachers'],c['max_teacher_session']),('class',data['classes'],c['max_class_session'])]:
        for item in items:
            for d in range(c['days']):
                for sh in ['am','pm']:
                    m.add(sum(v for p in range(c['periods']) for v in cover[(kind,item['id'],d,sh,p)])<=limit)
    fixed=list(c['fixed'])
    if scope:fixed.extend(r for r in previous if not in_scope(r,scope))
    for n,f in enumerate(fixed):
        matches=[v for v,r in by_assign[f['assignment']] if r['day']==f['day'] and r['shift']==f['shift'] and r['period']==f['period'] and r['length']==f.get('length',1) and ('room' not in f or r['room']==f['room'])]
        tag=m.new_bool_var('fixed_'+str(n));m.add_assumption(tag)
        assumptions[tag.index]=f"Tiết khóa {f['assignment']} ngày {f['day']+2} {f['shift']} tiết {f['period']+1}"
        m.add(sum(matches)==1).only_enforce_if(tag)
    # The feasibility model contains only hard constraints. Soft auxiliaries
    # must not slow down the search for the first complete assignment.
    hard_model=m.clone()
    gaps=[];visits=[];hint_defs=[]
    for t in data['teachers']:
        for d in range(c['days']):
            for sh in ['am','pm']:
                occ=[]
                for p in range(c['periods']):
                    v=m.new_bool_var('occ');m.add(v==sum(cover[('teacher',t['id'],d,sh,p)]));occ.append(v)
                    hint_defs.append((v,'occ',(t['id'],d,sh,p)))
                visit=m.new_bool_var('visit');m.add_max_equality(visit,occ);visits.append(visit)
                hint_defs.append((visit,'visit',(t['id'],d,sh)))
                for p in range(1,c['periods']-1):
                    before=m.new_bool_var('before');after=m.new_bool_var('after');gap=m.new_bool_var('gap')
                    m.add_max_equality(before,occ[:p]);m.add_max_equality(after,occ[p+1:])
                    m.add(gap<=before);m.add(gap<=after);m.add(gap+occ[p]<=1);m.add(gap>=before+after-occ[p]-1);gaps.append(gap)
                    for v,kind in [(before,'before'),(after,'after'),(gap,'gap')]:hint_defs.append((v,kind,(t['id'],d,sh,p)))
    spread=[];concentration=[]
    for cl,sid in sorted({(a['class_id'],a['subject_id'].split(':')[0]) for a in data['assignments']}):
        loads=[]
        for d in range(c['days']):
            z=m.new_int_var(0,2*c['periods'],'daily');m.add(z==sum(v*L for v,L in daily[(cl,sid,d)]));loads.append(z)
            excess=m.new_int_var(0,2*c['periods'],'excess');m.add_max_equality(excess,[z-1,0]);concentration.append(excess)
            hint_defs.extend([(z,'daily',(cl,sid,d)),(excess,'excess',(cl,sid,d))])
        lo=m.new_int_var(0,2*c['periods'],'min');hi=m.new_int_var(0,2*c['periods'],'max')
        m.add_min_equality(lo,loads);m.add_max_equality(hi,loads);spread.append(hi-lo)
        hint_defs.extend([(lo,'min',(cl,sid)),(hi,'max',(cl,sid))])
    objectives=dict(gaps=sum(gaps),visits=sum(visits),distribution=sum(spread),concentration=sum(concentration),
                    preferences=sum(pref_terms),changes=sum(old.values())-sum(change_terms) if previous else 0)
    for v,row in vars:
        if previous:
            value=int(old[signature(row)]>0)
            m.add_hint(v,value);hard_model.add_hint(v,value)
    if previous:
        for index in assumptions:hard_model.add_hint(hard_model.get_bool_var_from_proto_index(index),1)
    model_error=m.validate()
    if model_error:raise ValueError('MODEL_INVALID: '+model_error)
    phases=[];best=None;proven=[];solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=c['workers'];solver.parameters.random_seed=c['seed']
    def run(name,budget,model=None):
        solver.parameters.max_time_in_seconds=max(.01,budget)
        if progress:progress(f'CP-SAT: {name}')
        before=time.monotonic();status=solver.solve(model or m)
        phase=dict(name=name,status=solver.status_name(status),seconds=round(time.monotonic()-before,3))
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            phase['objective']=solver.objective_value;phase['best_bound']=solver.best_objective_bound
        phases.append(phase);return status
    # Spend the available budget finding the first complete solution, then use
    # the remaining time for optimization. A short arbitrary feasibility slice
    # would report UNKNOWN even when presolve merely needs a little more time.
    solver.parameters.stop_after_first_solution=True
    solver.parameters.linearization_level=0
    st=run('feasibility',max(.01,c['time_limit']-(time.monotonic()-start)),hard_model)
    solver.parameters.stop_after_first_solution=False
    solver.parameters.linearization_level=1
    if st==cp_model.INFEASIBLE:
        core=[assumptions.get(abs(i),'Ràng buộc PCCM') for i in solver.sufficient_assumptions_for_infeasibility()]
        result=empty('INFEASIBLE',core or ['Mâu thuẫn ràng buộc cứng; thử giảm phạm vi tiết khóa/lịch nghỉ để chẩn đoán, không tự nới ràng buộc.']);result['phases']=phases;result['proof']='CP-SAT infeasibility / sufficient assumption core (not necessarily minimal)';return result
    if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        result=empty('UNKNOWN',['Hết thời gian trước khi tìm được nghiệm; UNKNOWN không có nghĩa INFEASIBLE.']);result['phases']=phases;return result
    best=[row for v,row in vars if solver.boolean_value(v)]
    initial_metrics=metrics(data,c,best,previous)
    # Once feasibility is established, keep every assumption enforced as a
    # hard equality and clear the assumption interface. CP-SAT's assumption
    # mode restricts its optimization portfolio; hard equalities preserve the
    # same feasible set while allowing parallel search/LNS for soft goals.
    for index in assumptions:m.add(m.get_bool_var_from_proto_index(index)==1)
    m.clear_assumptions()
    for name in c['priorities']:
        expr=objectives[name]
        if isinstance(expr,int):proven.append(name);continue
        remaining=c['time_limit']-(time.monotonic()-start)
        if remaining<=.02:break
        m.clear_hints()
        chosen=set(signature(r) for r in best)
        for v,row in vars:m.add_hint(v,int(signature(row) in chosen))
        for index in assumptions:m.add_hint(m.get_bool_var_from_proto_index(index),1)
        occupied=defaultdict(set);loads=Counter()
        for r in best:
            occupied[(r['teacher'],r['day'],r['shift'])].update(range(r['period'],r['period']+r['length']))
            loads[(r['class_id'],r['subject_id'].split(':')[0],r['day'])]+=r['length']
        for v,kind,key in hint_defs:
            if kind in ('occ','before','after','gap'):
                ps=occupied[key[:3]];p=key[3];before=any(q<p for q in ps);after=any(q>p for q in ps)
                value=p in ps if kind=='occ' else before if kind=='before' else after if kind=='after' else before and after and p not in ps
            elif kind=='visit':value=bool(occupied[key])
            elif kind=='daily':value=loads[key]
            elif kind=='excess':value=max(0,loads[key]-1)
            else:
                counts=[loads[(*key,d)] for d in range(c['days'])];value=min(counts) if kind=='min' else max(counts)
            m.add_hint(v,int(value))
        m.minimize(expr);st=run(name,remaining)
        if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):best=[row for v,row in vars if solver.boolean_value(v)]
        if st!=cp_model.OPTIMAL:break
        val=round(solver.objective_value);m.add(expr==val);proven.append(name)
    verification=verify_schedule(data,c,best,previous,scope)
    if not verification['valid']:raise RuntimeError('Independent verifier rejected solver output: '+str(verification['errors']))
    optimum=len(proven)==len(c['priorities'])
    return dict(status='OPTIMAL' if optimum else 'FEASIBLE',lessons=sorted(best,key=lambda r:(r['class_id'],r['day'],r['shift'],r['period'])),
                required=required,placed=verification['placed'],conflicts=verification['conflicts'],
                metrics=metrics(data,c,best,previous),verification=verification,
                initial_metrics=initial_metrics,
                elapsed_seconds=round(time.monotonic()-start,3),phases=phases,
                proven_priorities=proven,global_optimal_proven=optimum and not bool(scope),
                lexicographic_optimal_proven=optimum,optimality_scope='local_frozen' if scope else 'full_model',
                diagnostics=[],technical_only=c['technical_only'],production_ready=False,
                unscheduled_special=sum(x['count'] for x in data.get('pending_special',[])))
