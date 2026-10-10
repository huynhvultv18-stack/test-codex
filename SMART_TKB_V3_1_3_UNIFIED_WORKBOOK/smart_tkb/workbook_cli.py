"""Offline workbook validation/export for administrators and Windows smoke tests."""
import argparse,json
from pathlib import Path
from .workbook import export_workbook,parse_workbook,export_errors

def main():
 p=argparse.ArgumentParser(description='SMART TKB — workbook tổng hợp 11 sheet')
 sub=p.add_subparsers(dest='command',required=True)
 t=sub.add_parser('template');t.add_argument('output',type=Path)
 v=sub.add_parser('validate');v.add_argument('input',type=Path);v.add_argument('--report',type=Path);v.add_argument('--json-report',type=Path)
 e=sub.add_parser('export');e.add_argument('backup',type=Path);e.add_argument('output',type=Path)
 a=p.parse_args()
 if a.command=='template':a.output.write_bytes(export_workbook());print(a.output);return 0
 if a.command=='export':
  state=json.loads(a.backup.read_text(encoding='utf-8'));a.output.write_bytes(export_workbook(state));print(a.output);return 0
 r=parse_workbook(a.input.read_bytes());public={k:v for k,v in r.items() if k!='state'}
 if a.report:a.report.write_bytes(export_errors(public))
 if a.json_report:a.json_report.write_text(json.dumps(public,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(public,ensure_ascii=False,indent=2));return 0 if r['valid'] else 1

if __name__=='__main__':raise SystemExit(main())
