"""CP-SAT time-indexed assignment blocks with strict hard constraints.

No greedy fallback or partial schedule. Proven objective locks and optional
incumbent locks are reported separately; no higher-priority incumbent is worsened.
"""
from collections import defaultdict, Counter
from copy import deepcopy
import time
import math
from .quality import class_ids, allowed_shifts, add_quality_model, add_subject_hard_limits, features
from .special import prepare_special, special_report
from ortools.sat.python import cp_model
from .validation import (config_with_defaults,validate_problem,class_shifts,blocked,
                         signature,in_scope,verify_schedule,metrics,teacher_visits)

def _solve_core(data, config=None, previous=None, scope=None, progress=None):
    start=time.monotonic();c=config_with_defaults(config);previous=previous or []
    timings={};solver_start=None
    def stamp(name,before):timings[name]=round(time.monotonic()-before,6)
    def stats(model):return dict(variables=len(model.proto.variables),constraints=len(model.proto.constraints))
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
    if not isinstance(previous,list) or any(not isinstance(r,dict) or not all(k in r for k in ('assignment','day','shift','period','teacher','class_id','subject_id')) or any(type(r.get(k,1 if k=='length' else None)) is not int for k in ('day','period','length')) for r in previous):raise ValueError('Lịch trước phải có mã phân công/ngày/ca/tiết nguyên hợp lệ')
    before=time.monotonic();warm_valid=bool(previous) and verify_schedule(data,c,previous,previous,scope)['valid'];stamp('warm_validation_seconds',before)
    diagnoses=[]
    required=sum(a['count']*len(class_ids(a)) for a in data['assignments'])
    classes={x['id']:x for x in data['classes']}
    for cls in data['classes']:
        need=sum(a['count'] for a in data['assignments'] if cls['id'] in class_ids(a))
        capacity=sum(min(c['max_class_session'],sum(not blocked(c,'class',cls['id'],d,sh,p) for p in range(c['periods']))) for d in range(c['days']) for sh in class_shifts(cls,c))
        if need>capacity:diagnoses.append(f"Lớp {cls['name']}: cần {need}, sức chứa {capacity} tiết")
    for t in data['teachers']:
        related=[a for a in data['assignments'] if a['teacher']==t['id']]
        for shifts in [('am',),('pm',),('am','pm')]:
            need=sum(a['count'] for a in related if set(allowed_shifts(a,classes,c))<=set(shifts))
            cap=sum(min(c['max_teacher_session'],sum(not blocked(c,'teacher',t['id'],d,sh,p) for p in range(c['periods']))) for d in range(c['days']) for sh in shifts)
            if need>cap:diagnoses.append(f"GV {t['id']} — {t['name']}: cần {need}, sức chứa {cap} tiết ({'/'.join(shifts)})")
    def empty(status,reason):
        return dict(status=status,lessons=[],required=required,placed=0,conflicts=None,
                    elapsed_seconds=round(time.monotonic()-start,3),diagnostics=reason,
                    metrics=None,phases=[],global_optimal_proven=False,
                    lexicographic_optimal_proven=False,optimality_scope='local_frozen' if scope else 'full_model',
                    technical_only=c['technical_only'],production_ready=False,
                    performance=dict(timings=timings,model=timings.get('model',{}),warm_incumbent_valid=warm_valid),
                    unscheduled_special=sum(x['count'] for x in data.get('pending_special',[])))
    if diagnoses:
        result=empty('INFEASIBLE',diagnoses);result['proof']='Necessary capacity bound';return result
    model_started=time.monotonic()
    m=cp_model.CpModel();vars=[];by_assign=defaultdict(list);cover=defaultdict(list)
    pref_terms=[];change_terms=[];assumptions={}
    old=Counter(signature(r) for r in previous)
    unavailable={(q['kind'],q['id'],q['day'],q['shift'],q.get('period')) for q in c['unavailable']}
    def unavailable_at(k,i,d,sh,p):return (k,i,d,sh,p) in unavailable or (k,i,d,sh,None) in unavailable
    for a in data['assignments']:
        doubles=a.get('double_count',0)
        for length,n in [(1,a['count']-2*doubles),(2,doubles)]:
            if not n:continue
            group=[]
            shifts=allowed_shifts(a,classes,c)
            for d in range(c['days']):
                for sh in shifts:
                    for p in range(c['periods']-length+1):
                        if a.get('fixed_day') is not None and d!=a['fixed_day']:continue
                        if a.get('fixed_period') is not None and p!=a['fixed_period']:continue
                        for room in a.get('room_ids') or [None]:
                            resources=([('teacher',a['teacher'])] if a['teacher'] is not None else [])+[('class',cl) for cl in class_ids(a)]+([('room',room)] if room else [])
                            if any(unavailable_at(k,i,d,sh,pp) for k,i in resources for pp in range(p,p+length)):continue
                            v=m.new_bool_var(f'x_{a["id"]}_{length}_{d}_{sh}_{p}_{room}')
                            row=dict(assignment=a['id'],teacher=a['teacher'],class_id=a['class_id'],subject_id=a['subject_id'],
                                     subject=a['subject'],day=d,shift=sh,period=p,length=length,room=room,class_ids=class_ids(a))
                            if a.get('is_special'):
                                row.update({k:a.get(k) for k in ['is_special','activity_ids','activity_status','activity_type','shared_teacher_group']})
                            vars.append((v,row));group.append(v);by_assign[a['id']].append((v,row))
                            for pp in range(p,p+length):
                                for kind,identity in resources:cover[(kind,identity,d,sh,pp)].append(v)
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
    add_subject_hard_limits(m,data,c,vars)
    timings['hard_model']=stats(m)
    hard_model=m.clone() if not warm_valid else None
    gaps=[];visits=[];hint_defs=[];visit_by_teacher=defaultdict(list);visit_by_shift=defaultdict(list)
    for t in data['teachers']:
        for d in range(c['days']):
            for sh in ['am','pm']:
                occ=[]
                for p in range(c['periods']):
                    v=m.new_bool_var('occ');m.add(v==sum(cover[('teacher',t['id'],d,sh,p)]));occ.append(v)
                    hint_defs.append((v,'occ',(t['id'],d,sh,p)))
                visit=m.new_bool_var('visit');m.add_max_equality(visit,occ);visits.append(visit)
                hint_defs.append((visit,'visit',(t['id'],d,sh)))
                visit_by_teacher[t['id']].append(visit);visit_by_shift[(t['id'],sh)].append(visit)
                for p in range(1,c['periods']-1):
                    before=m.new_bool_var('before');after=m.new_bool_var('after');gap=m.new_bool_var('gap')
                    m.add_max_equality(before,occ[:p]);m.add_max_equality(after,occ[p+1:])
                    m.add(gap<=before);m.add(gap<=after);m.add(gap+occ[p]<=1);m.add(gap>=before+after-occ[p]-1);gaps.append(gap)
                    for v,kind in [(before,'before'),(after,'after'),(gap,'gap')]:hint_defs.append((v,kind,(t['id'],d,sh,p)))
    lower_bounds={};visit_lower=0;limit=min(c['periods'],c['max_teacher_session'])
    for t in data['teachers']:
        related=[a for a in data['assignments'] if a['teacher']==t['id']]
        total=sum(a['count'] for a in related)
        forced={sh:sum(a['count'] for a in related if set(allowed_shifts(a,classes,c))=={sh}) for sh in ['am','pm']}
        lb=max(math.ceil(total/limit),sum(math.ceil(n/limit) for n in forced.values()))
        lower_bounds[t['id']]=lb;visit_lower+=lb
        m.add(sum(visit_by_teacher[t['id']])>=lb)
        for sh,n in forced.items():m.add(sum(visit_by_shift[(t['id'],sh)])>=math.ceil(n/limit))
    m.add(sum(visits)>=visit_lower)
    quality_exprs,quality_hints=add_quality_model(m,data,c,vars)
    subject_preferences=quality_exprs.pop('subject_preferences')
    objectives=dict(gaps=sum(gaps),visits=sum(visits),**quality_exprs,
                    preferences=sum(pref_terms)+subject_preferences,changes=sum(old.values())-sum(change_terms) if previous else 0)
    for v,row in vars:
        if previous:
            value=int(old[signature(row)]>0)
            m.add_hint(v,value)
            if hard_model is not None:hard_model.add_hint(v,value)
    if previous and hard_model is not None:
        for index in assumptions:hard_model.add_hint(hard_model.get_bool_var_from_proto_index(index),1)
    model_error=m.validate()
    if model_error:raise ValueError('MODEL_INVALID: '+model_error)
    stamp('model_build_seconds',model_started);timings['model']=stats(m)
    phases=[];best=None;proven=[];solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=c['workers'];solver.parameters.random_seed=c['seed']
    solver.parameters.use_lns=True
    def run(name,budget,model=None):
        solver.parameters.max_time_in_seconds=max(.01,budget)
        if progress:progress(f'CP-SAT: {name}')
        before=time.monotonic();status=solver.solve(model or m)
        phase=dict(name=name,status=solver.status_name(status),seconds=round(time.monotonic()-before,3))
        if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            phase['objective']=solver.objective_value;phase['best_bound']=solver.best_objective_bound
            phase['relative_gap']=max(0,solver.objective_value-solver.best_objective_bound)/max(1,abs(solver.objective_value))
        else:phase['objective']=None;phase['best_bound']=solver.best_objective_bound if name!='feasibility' else None;phase['relative_gap']=None
        phases.append(phase);return status
    # Spend the available budget finding the first complete solution, then use
    # the remaining time for optimization. A short arbitrary feasibility slice
    # would report UNKNOWN even when presolve merely needs a little more time.
    if warm_valid:
        best=deepcopy(previous);timings['first_solution_seconds']=timings['warm_validation_seconds']
        phases.append(dict(name='feasibility',status='VERIFIED_INCUMBENT',solver_status=None,seconds=timings['warm_validation_seconds'],proof='Independent hard-constraint verifier; no CP-SAT feasibility call'))
    else:
        solver.parameters.stop_after_first_solution=True
        solver.parameters.linearization_level=0
        st=run('feasibility',max(.01,c['time_limit']-(time.monotonic()-start)),hard_model)
        if st==cp_model.INFEASIBLE:
            core=[assumptions.get(abs(i),'Ràng buộc PCCM') for i in solver.sufficient_assumptions_for_infeasibility()]
            result=empty('INFEASIBLE',core or ['Mâu thuẫn ràng buộc cứng; thử giảm phạm vi tiết khóa/lịch nghỉ để chẩn đoán, không tự nới ràng buộc.']);result['phases']=phases;result['proof']='CP-SAT infeasibility / sufficient assumption core (not necessarily minimal)';return result
        if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE):
            result=empty('UNKNOWN',['Hết thời gian trước khi tìm được nghiệm; UNKNOWN không có nghĩa INFEASIBLE.']);result['phases']=phases;return result
        best=[row for v,row in vars if solver.boolean_value(v)];stamp('first_solution_seconds',start)
    solver.parameters.stop_after_first_solution=False
    solver.parameters.linearization_level=2
    solver.parameters.use_lns_only=c['search_mode']=='lns' and c['workers']>1
    initial_metrics=metrics(data,c,best,previous)
    initial_quality=features(data,c,best)
    # Once feasibility is established, keep every assumption enforced as a
    # hard equality and clear the assumption interface. CP-SAT's assumption
    # mode restricts its optimization portfolio; hard equalities preserve the
    # same feasible set while allowing parallel search/LNS for soft goals.
    for index in assumptions:m.add(m.get_bool_var_from_proto_index(index)==1)
    m.clear_assumptions()
    unproven_locks=False;incumbent_locks={};conditional=[]
    for number,name in enumerate(c['priorities']):
        setting=c['objective_settings'][name]
        if not setting['enabled']:
            phases.append(dict(name=name,status='SKIPPED_DISABLED',seconds=0));continue
        expr=objectives[name]*setting['weight']
        if isinstance(expr,int):
            phases.append(dict(name=name,status='CONSTANT',seconds=0,objective=expr,best_bound=expr))
            if unproven_locks:conditional.append(name)
            else:proven.append(name)
            continue
        incumbent=metrics(data,c,best,previous);q=features(data,c,best)
        incumbent.update(distribution=q['distribution_weighted'],concentration=q['concentration_weighted'])
        lower=visit_lower*setting['weight'] if name=='visits' else 0
        value=incumbent[name]*setting['weight']
        if value==lower:
            m.add(expr==value)
            phases.append(dict(name=name,status='PROVEN_LOWER_BOUND',solver_status=None,seconds=0,objective=value,best_bound=lower,relative_gap=0,proof='Verified incumbent attains a universal lower bound',proof_scope='conditional_on_incumbent_locks' if unproven_locks else 'lexicographic_prefix'))
            if unproven_locks:conditional.append(name)
            else:proven.append(name)
            continue
        remaining=c['time_limit']-(time.monotonic()-start)
        if remaining<=.02:break
        m.clear_hints()
        chosen=set(signature(r) for r in best)
        for v,row in vars:m.add_hint(v,int(signature(row) in chosen))
        for index in assumptions:m.add_hint(m.get_bool_var_from_proto_index(index),1)
        occupied=defaultdict(set)
        for r in best:
            if r['teacher'] is not None:occupied[(r['teacher'],r['day'],r['shift'])].update(range(r['period'],r['period']+r['length']))
        for v,kind,key in hint_defs:
            if kind in ('occ','before','after','gap'):
                ps=occupied[key[:3]];p=key[3];before=any(q<p for q in ps);after=any(q>p for q in ps)
                value=p in ps if kind=='occ' else before if kind=='before' else after if kind=='after' else before and after and p not in ps
            elif kind=='visit':value=bool(occupied[key])
            m.add_hint(v,int(value))
        quality_values=features(data,c,best)['values']
        for v,key in quality_hints:m.add_hint(v,quality_values[key])
        fractions=c['phase_fractions'];weight=fractions[name];tail=sum(fractions[n] for n in c['priorities'][number:] if c['objective_settings'][n]['enabled'])
        budget=remaining*(weight/tail if tail>0 else 1)
        if budget<=.005:phases.append(dict(name=name,status='SKIPPED_BUDGET',seconds=0));continue
        incumbent=metrics(data,c,best,previous);quality=features(data,c,best)
        incumbent.update(distribution=quality['distribution_weighted'],concentration=quality['concentration_weighted'])
        # A verified incumbent is a valid upper bound. This dominance cut
        # preserves every possible better optimum and guards short phases.
        m.add(expr<=incumbent[name]*setting['weight'])
        m.minimize(expr);st=run(name,budget)
        phases[-1]['proof_scope']='conditional_on_incumbent_locks' if unproven_locks else 'lexicographic_prefix'
        if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):best=[row for v,row in vars if solver.boolean_value(v)]
        if st==cp_model.OPTIMAL:
            val=round(solver.objective_value);m.add(expr==val)
            if unproven_locks:conditional.append(name)
            else:proven.append(name)
        elif c['advance_on_incumbent']:
            values=metrics(data,c,best,previous);q=features(data,c,best)
            values.update(distribution=q['distribution_weighted'],concentration=q['concentration_weighted'])
            val=values[name]*setting['weight'];m.add(expr==val);incumbent_locks[name]=val;unproven_locks=True
        else:break
    verification_started=time.monotonic()
    verification=verify_schedule(data,c,best,previous,scope)
    stamp('verification_seconds',verification_started)
    timings['optimization_seconds']=round(sum(p['seconds'] for p in phases if p['name']!='feasibility'),6)
    if not verification['valid']:raise RuntimeError('Independent verifier rejected solver output: '+str(verification['errors']))
    optimum=all(n in proven for n in c['priorities'] if c['objective_settings'][n]['enabled']) and not unproven_locks
    return dict(status='OPTIMAL' if optimum else 'FEASIBLE',lessons=sorted(best,key=lambda r:(r['class_id'],r['day'],r['shift'],r['period'])),
                required=required,placed=verification['placed'],conflicts=verification['conflicts'],
                metrics=metrics(data,c,best,previous),verification=verification,
                initial_metrics=initial_metrics,initial_quality_scores={k:v for k,v in initial_quality.items() if k!='values'},
                quality_scores={k:v for k,v in features(data,c,best).items() if k!='values'},
                teacher_visits=teacher_visits(data,best),visit_lower_bound=visit_lower,teacher_visit_lower_bounds=lower_bounds,
                performance=dict(timings=timings,model=stats(m),warm_incumbent_valid=warm_valid,feasibility_model_cloned=hard_model is not None),
                incumbent_locks=incumbent_locks,conditional_optimal_priorities=conditional,
                elapsed_seconds=round(time.monotonic()-start,3),phases=phases,
                proven_priorities=proven,global_optimal_proven=optimum and not bool(scope),
                lexicographic_optimal_proven=optimum,optimality_scope='local_frozen' if scope else 'full_model',
                diagnostics=[],technical_only=c['technical_only'],production_ready=False,
                unscheduled_special=sum(x['count'] for x in data.get('pending_special',[])))


def solve(data, config=None, previous=None, scope=None, progress=None):
    c=config_with_defaults(config);working,c,context=prepare_special(data,c)
    result=_solve_core(working,c,previous,scope,progress)
    report=special_report(context,result['lessons']);result['special_report']=report
    result['simulation']=report['simulation'];result['scenario_assumptions']=report['assumptions']
    result['scheduled_class_periods']=result['placed'];result['model_required']=result['required']
    result['required']=context['curricular_required']+context['verified']
    result['placed']=sum(r['length']*len(class_ids(r)) for r in result['lessons'] if r.get('activity_status')!='SCENARIO')
    result['scenario_placed']=report['scheduled_scenario'];result['unscheduled_special']=report['pending']
    result['all_source_periods']=context['curricular_required']+context['total']
    result['official_complete']=bool(result['lessons']) and report['official_complete']
    result['data_accepted']=False;result['windows_accepted']=False;result['production_ready']=False
    return result
