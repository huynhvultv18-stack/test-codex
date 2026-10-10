"""Create immutable candidate ZIP + per-file manifest; never touches baseline."""
import argparse,hashlib,json,zipfile
from pathlib import Path

NAME='SMART_TKB_THCS_V3_1_3_UNIFIED_WORKBOOK_CANDIDATE'
def build(root,output):
 if not (root/'windows/runtime/python.exe').is_file():raise ValueError('Cần runtime Windows đã xác minh từ ZIP Candidate; checkout mã nguồn không chứa runtime/wheels')
 files=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts and p.suffix!='.pyc' and p.name!='SHA256SUMS.txt')
 entries=[(hashlib.sha256(p.read_bytes()).hexdigest(),p.relative_to(root).as_posix()) for p in files]
 manifest=root/'SHA256SUMS.txt';manifest.write_text(''.join(f'{h}  {n}\n' for h,n in entries),encoding='utf-8')
 with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files+[manifest]:z.write(p,NAME+'/'+p.relative_to(root).as_posix())
 digest=hashlib.sha256(output.read_bytes()).hexdigest();Path(str(output)+'.sha256').write_text(f'{digest}  {output.name}\n')
 with zipfile.ZipFile(output) as z:
  assert z.testzip() is None
  for h,n in entries:assert hashlib.sha256(z.read(NAME+'/'+n)).hexdigest()==h
 report=dict(filename=output.name,sha256=digest,bytes=output.stat().st_size,zip_crc='PASS',file_sha256='PASS',manifest_files=len(entries),zip_entries=len(entries)+1,production_ready=False)
 output.with_name(output.stem+'_PACKAGE_VERIFICATION.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.root.resolve(),a.output.resolve())
