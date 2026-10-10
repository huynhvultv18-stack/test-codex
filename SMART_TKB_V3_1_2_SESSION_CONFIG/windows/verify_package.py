"""Verify release payload before starting. Ignore generated reports/cache."""
from pathlib import Path
import hashlib
import sys

root=Path(__file__).resolve().parent.parent
manifest=root/'SHA256SUMS.txt'
if not manifest.is_file():
    raise SystemExit('Missing SHA256SUMS.txt')
count=0
for line in manifest.read_text(encoding='utf-8').splitlines():
    digest,name=line.split('  ',1)
    # Tests may update evidence. Runtime, code, UI, SOURCE and wheels remain
    # immutable release inputs. Verify those without rejecting new reports.
    if name.startswith('reports/') or name.startswith('data/'):
        continue
    relative=Path(name)
    if relative.is_absolute() or '..' in relative.parts:
        raise SystemExit('Unsafe manifest path')
    file=root/relative
    if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest()!=digest:
        raise SystemExit('SHA-256 mismatch: '+name)
    count+=1
print('Verified',count,'release files.')
