"""Public CLI only solves the selected grade. No whole-school solve option."""
import argparse,json
from pathlib import Path
from .importer import read_pccm
from .grade import solve_grade

def main():
 p=argparse.ArgumentParser(description='SMART TKB V3.1.1 Grade Candidate CP-SAT')
 p.add_argument('excel',type=Path);p.add_argument('--grade',type=int,choices=[6,7,8,9],default=8)
 p.add_argument('--mode',choices=['morning','both','mixed'],default='both')
 p.add_argument('--am',type=int,default=5);p.add_argument('--pm',type=int,default=4)
 p.add_argument('--active-days',default='0,1,2,3,4,5');p.add_argument('--background',type=Path)
 p.add_argument('--config',type=Path);p.add_argument('--previous',type=Path);p.add_argument('--scope',type=Path)
 p.add_argument('--simulate-background',metavar='ASSUMPTION');p.add_argument('--seconds',type=float,default=60);p.add_argument('--out',type=Path,required=True)
 args=p.parse_args();data=read_pccm(args.excel);c=json.loads(args.config.read_text(encoding='utf-8')) if args.config else {}
 c.update(target_grade=args.grade,mode=args.mode,time_limit=args.seconds,days=6,periods=max(args.am,args.pm),session_periods={'am':args.am,'pm':args.pm},active_days=[int(d) for d in args.active_days.split(',')])
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
 r=solve_grade(data,c,bg,prev,lambda m:print(m,flush=True),scope=scope)
 args.out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(r['status'],r['placed'],'/',r['required'],'tiết; cross-grade:',r['cross_grade_conflict'])
if __name__=='__main__':main()
