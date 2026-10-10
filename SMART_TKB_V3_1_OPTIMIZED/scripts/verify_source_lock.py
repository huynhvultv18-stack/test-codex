"""Verify archive baseline, immutable source bytes and Windows payload."""
from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parent.parent;lock=json.loads((R/'reports/SOURCE_LOCK.json').read_text());baseline=Path(lock['source']);digest=hashlib.sha256(baseline.read_bytes()).hexdigest();assert digest==lock['sha256']
checks=[];windows=[]
with zipfile.ZipFile(baseline) as z:
 assert z.testzip() is None
 prefix='SMART_TKB_THCS_V3_1_OPTIMIZATION_CANDIDATE/'
 for line in z.read(prefix+'SHA256SUMS.txt').decode().splitlines():
  sha,name=line.split('  ',1);assert hashlib.sha256(z.read(prefix+name)).hexdigest()==sha
  original=baseline.parent/prefix[:-1]/name;assert hashlib.sha256(original.read_bytes()).hexdigest()==sha,name
  if name.startswith('SOURCE/') or name.startswith('windows/runtime/') or name.startswith('windows/wheels/') or name in ['windows/requirements-lock.txt','windows/PYTHON_PROVENANCE.json']:
   assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha,name
   if name.startswith('SOURCE/'):checks.append(dict(file=name,sha256=sha,immutable=True))
   else:windows.append(dict(file=name,sha256=sha))
(R/'reports/SOURCE_IMMUTABILITY.json').write_text(json.dumps(dict(result='PASS',baseline_archive=digest,baseline_tree_manifest='PASS',source_checks=checks),ensure_ascii=False,indent=2))
(R/'reports/WINDOWS_INTEGRITY.json').write_text(json.dumps(dict(result='PASS',runtime='UNTESTED',method='Byte comparison against locked delivered V3.1 ZIP; not execution',files_checked=len(windows),files=windows),ensure_ascii=False,indent=2));print('PASS immutable baseline archive/tree, SOURCE and',len(windows),'Windows payload files')
