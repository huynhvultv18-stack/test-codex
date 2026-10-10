@echo off
setlocal
cd /d "%~dp0"
set PYTHONNOUSERSITE=1
set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=
set PYTHONHOME=
if not exist "windows\runtime\python.exe" (
 echo Khong tim thay Python runtime. Hay giai nen toan bo goi ZIP.
 pause
 exit /b 1
)
"windows\runtime\python.exe" -c "import sys; sys.exit(0 if sys.version_info[:2] == (3,12) and sys.maxsize > 2**32 else 1)"
if errorlevel 1 (
 echo Can Windows x64 va Python 3.12 di kem.
 pause
 exit /b 1
)
"windows\runtime\python.exe" windows\verify_package.py
if errorlevel 1 (
 echo Kiem tra SHA-256 that bai. Khong chay goi bi thay doi.
 pause
 exit /b 1
)
"windows\runtime\python.exe" -m pip --isolated install --no-index --find-links=windows\wheels --require-hashes --only-binary=:all: -r windows\requirements-lock.txt --disable-pip-version-check
if errorlevel 1 (
 echo Cai dat ngoai tuyen that bai. Xem thong bao o tren.
 pause
 exit /b 1
)
"windows\runtime\python.exe" -m smart_tkb.server --open
if errorlevel 1 (
 echo Khong khoi dong duoc. Cong 8768 co the dang duoc su dung.
 pause
 exit /b 1
)
