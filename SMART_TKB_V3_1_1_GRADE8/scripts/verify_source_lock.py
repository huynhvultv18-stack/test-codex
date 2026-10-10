"""Check the exact Optimized ZIP baseline, SOURCE and unchanged Windows payload."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent.parent;lock=json.loads((R/'reports/GRADE8_SOURCE_LOCK.json').read_text());baseline=Path(lock['source'])
assert hashlib.sha256(baseline.read_bytes()).hexdigest()==lock['sha256']
checks=[];windows=0;tree=0
with zipfile.ZipFile(baseline) as z:
 assert z.testzip() is None;prefix='SMART_TKB_THCS_V3_1_OPTIMIZED_CANDIDATE/'
 for line in z.read(prefix+'SHA256SUMS.txt').decode().splitlines():
  sha,name=line.split('  ',1);assert hashlib.sha256(z.read(prefix+name)).hexdigest()==sha
  assert hashlib.sha256((baseline.parent/prefix[:-1]/name).read_bytes()).hexdigest()==sha,name;tree+=1
  if name.startswith(('SOURCE/','windows/runtime/','windows/wheels/')) or name in ['windows/requirements-lock.txt','windows/PYTHON_PROVENANCE.json']:
   assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha,name
   if name.startswith('SOURCE/'):checks.append(dict(file=name,sha256=sha,immutable=True))
   else:windows+=1
(R/'reports/GRADE8_SOURCE_IMMUTABILITY.json').write_text(json.dumps(dict(result='PASS',baseline_archive=lock['sha256'],baseline_tree_files=tree,source_checks=checks,windows_payload_files=windows,windows_runtime='UNTESTED'),ensure_ascii=False,indent=2));print('PASS immutable baseline',tree,'files, SOURCE and',windows,'Windows payload files; Windows UNTESTED')
