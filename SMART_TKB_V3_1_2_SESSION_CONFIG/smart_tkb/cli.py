"""Public CLI only solves the selected grade. No whole-school solve option."""
import argparse,json
from pathlib import Path
from .importer import read_pccm
from .grade import solve_grade,prepare_grade
from .sessions import impact

def main():
 p=argparse.ArgumentParser(description='SMART TKB V3.1.2 Session Candidate CP-SAT')
 p.add_argument('excel',type=Path);p.add_argument('--grade',type=int,choices=[6,7,8,9],default=8)
 p.add_argument('--mode',choices=['morning','both','mixed'],default='both')
 p.add_argument('--am',type=int,default=None);p.add_argument('--pm',type=int,default=None)
 p.add_argument('--active-days',default=None);p.add_argument('--background',type=Path)
 p.add_argument('--config',type=Path);p.add_argument('--previous',type=Path);p.add_argument('--scope',type=Path)
 p.add_argument('--session-config',type=Path);p.add_argument('--confirm-session-change',action='store_true')
 p.add_argument('--simulate-background',metavar='ASSUMPTION');p.add_argument('--seconds',type=float,default=60);p.add_argument('--out',type=Path,required=True)
 args=p.parse_args();data=read_pccm(args.excel);c=json.loads(args.config.read_text(encoding='utf-8')) if args.config else {}
 c.update(target_grade=args.grade,mode=args.mode,time_limit=args.seconds)
 if args.session_config:c['session_config']=json.loads(args.session_config.read_text(encoding='utf-8'))
 if args.am is not None or args.pm is not None or args.active_days is not None:
  if c.get('session_config'):raise ValueError('Dùng session-config hoặc lịch đồng nhất --am/--pm; không ghi đè lịch buổi')
  am=5 if args.am is None else args.am;pm=4 if args.pm is None else args.pm
  c.update(days=6,periods=max(1,am,pm),session_periods={'am':am,'pm':pm},active_days=[int(d) for d in (args.active_days or '0,1,2,3,4,5').split(',')])
 if args.simulate_background:c.update(allow_incomplete_background=True,background_assumption=args.simulate_background)
 if args.mode=='mixed':
  shifts=c.pop('class_shifts',{})
  if not shifts:raise ValueError('Phân ca cần class_shifts; không tự quyết ca học')
  for cl in data['classes']:
   if cl['grade']==args.grade:cl['shift']=shifts[cl['id']]
 bg=json.loads(args.background.read_text(encoding='utf-8')) if args.background else None
 prev=json.loads(args.previous.read_text(encoding='utf-8')) if args.previous else None
 if isinstance(prev,dict):prev=prev['lessons']
 scope=json.loads(args.scope.read_text(encoding='utf-8')) if args.scope else None
 confirmation=None
 if args.confirm_session_change:
  prepared=prepare_grade(data,c,bg);confirmation=impact(prepared['working'],prepared['config'],prev if prev is not None else prepared['warm'])['confirmation']
 r=solve_grade(data,c,bg,prev,lambda m:print(m,flush=True),scope=scope,session_confirmation=confirmation)
 args.out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(r['status'],r['placed'],'/',r['required'],'tiết; cross-grade:',r['cross_grade_conflict'])
if __name__=='__main__':main()
