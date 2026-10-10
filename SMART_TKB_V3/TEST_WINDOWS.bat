@echo off
setlocal
cd /d "%~dp0"
set PYTHONNOUSERSITE=1
set PYTHONDONTWRITEBYTECODE=1
set PYTHONPATH=
set PYTHONHOME=
"windows\runtime\python.exe" -m pip --isolated install --no-index --find-links=windows\wheels --require-hashes --only-binary=:all: -r windows\requirements-lock.txt --disable-pip-version-check
if errorlevel 1 exit /b 1
"windows\runtime\python.exe" -m unittest discover -s tests -v
set TKB_TEST_EXIT=%ERRORLEVEL%
pause
exit /b %TKB_TEST_EXIT%
