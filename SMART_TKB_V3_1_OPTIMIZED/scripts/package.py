"""Manifest and ZIP builder; validates all entries and safe extraction."""
from pathlib import Path
import hashlib,json,zipfile,shutil,sys
ROOT=Path(__file__).resolve().parent.parent
ARCHIVE=ROOT.parent/(ROOT.name+'.zip')
def include(p):return not any(s=='__pycache__' for s in p.parts) and p.suffix not in ('.pyc','.pyo') and '.git' not in p.parts
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and include(p))
manifest=ROOT/'SHA256SUMS.txt'
manifest.write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files if p!=manifest))
with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in files:z.write(p,ROOT.name+'/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(ARCHIVE) as z:
 assert z.testzip() is None
 assert all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in z.namelist())
 for required in ['smart_tkb/solver.py','smart_tkb/special.py','web/index.html','tests/test_v3_1.py','reports/AB_BENCHMARK.json','reports/AB_LNS_BENCHMARK.json','reports/FULL_AUDIT.md','reports/BUGFIX.md','reports/OPTIMIZATION.md','reports/AB_BENCHMARK.md','reports/ACCEPTANCE.json','reports/REGRESSION.md','windows/runtime/python.exe','windows/requirements-lock.txt','START_WINDOWS.bat','SHA256SUMS.txt']:
  assert ROOT.name+'/'+required in z.namelist(),required
 verify=ROOT.parent/'tkb-v3-1-package-verify'
 verify.mkdir(exist_ok=True);z.extractall(verify)
 payload=verify/ROOT.name
 for line in (payload/'SHA256SUMS.txt').read_text().splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256((payload/name).read_bytes()).hexdigest()==digest,name
sha=hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()
ARCHIVE.with_suffix('.zip.sha256').write_text(sha+'  '+ARCHIVE.name+'\n')
print(json.dumps(dict(zip=str(ARCHIVE),sha256=sha,bytes=ARCHIVE.stat().st_size,files=len(files),crc='PASS',safe_extract='PASS',manifest='PASS',extracted=str(payload)),indent=2))
