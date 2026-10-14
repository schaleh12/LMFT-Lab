@echo off
setlocal
cd /d "%~dp0.."
set PYTHONPATH=src

if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
) else (
    set PYTHON_BIN=python
)

"%PYTHON_BIN%" tools\symposium.py %*
echo.
pause
