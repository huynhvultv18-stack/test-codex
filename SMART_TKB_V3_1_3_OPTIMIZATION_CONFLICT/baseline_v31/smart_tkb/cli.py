import argparse,json
from pathlib import Path
from .importer import read_pccm
from .solver import solve

def main():
    p=argparse.ArgumentParser(description='SMART TKB V3.1 Optimization Candidate CP-SAT')
    p.add_argument('excel',type=Path);p.add_argument('--mode',choices=['morning','both','mixed'],default='both')
    p.add_argument('--config',type=Path);p.add_argument('--previous',type=Path);p.add_argument('--scope',type=Path)
    p.add_argument('--seconds',type=float,default=30);p.add_argument('--out',type=Path,required=True)
    args=p.parse_args();data=read_pccm(args.excel);config=json.loads(args.config.read_text(encoding='utf-8')) if args.config else {}
    config.update(mode=args.mode,time_limit=args.seconds)
    if args.mode=='mixed':
        shifts=config.pop('class_shifts',{})
        if not shifts:raise ValueError('Chế độ phân ca cần class_shifts trong config; không tự quyết ca học thực tế.')
        for cls in data['classes']:cls['shift']=shifts[cls['id']]
    previous=json.loads(args.previous.read_text(encoding='utf-8')) if args.previous else None
    if isinstance(previous,dict):previous=previous['lessons']
    scope=json.loads(args.scope.read_text(encoding='utf-8')) if args.scope else None
    result=solve(data,config,previous,scope,lambda x:print(x,flush=True))
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(result['status'],result['placed'],'/',result['required'],'tiết')

if __name__=='__main__':main()
