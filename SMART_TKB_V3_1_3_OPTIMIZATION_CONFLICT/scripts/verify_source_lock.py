"""Verify immutable V3.1.1 archive/tree and unchanged source/Windows binaries."""
from pathlib import Path
import hashlib,json,zipfile,argparse
R=Path(__file__).resolve().parent.parent
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path);a=p.parse_args()
lock=json.loads((R/'reports/SESSION_SOURCE_LOCK.json').read_text());baseline=a.baseline or Path(lock['source']);sha=hashlib.sha256(baseline.read_bytes()).hexdigest();assert sha==lock['sha256']
checks=[];windows=0;tree=0
with zipfile.ZipFile(baseline) as z:
 assert z.testzip() is None;prefix='SMART_TKB_THCS_V3_1_1_GRADE8_CANDIDATE/'
 for line in z.read(prefix+'SHA256SUMS.txt').decode().splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256(z.read(prefix+name)).hexdigest()==digest
  original=baseline.parent/prefix[:-1]/name
  assert hashlib.sha256(original.read_bytes()).hexdigest()==digest,name;tree+=1
  if name.startswith(('SOURCE/','windows/runtime/','windows/wheels/')) or name in ['windows/requirements-lock.txt','windows/PYTHON_PROVENANCE.json']:
   assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
   if name.startswith('SOURCE/'):checks.append(dict(file=name,sha256=digest,immutable=True))
   else:windows+=1
(R/'reports/SESSION_SOURCE_IMMUTABILITY.json').write_text(json.dumps(dict(status='PASS',baseline_archive=sha,baseline_tree_files=tree,source_checks=checks,windows_payload_files=windows,windows_runtime='UNTESTED'),indent=2));print('PASS baseline',tree,'files; immutable SOURCE and',windows,'Windows payload files; Windows UNTESTED')
