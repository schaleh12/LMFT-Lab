@echo off
setlocal
cd /d "%~dp0.."
set PYTHONPATH=src

if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
) else (
    set PYTHON_BIN=python
)

"%PYTHON_BIN%" tools\talk_to_lmft.py %*
if %ERRORLEVEL% neq 0 (
    echo.
    echo Process exited with code %ERRORLEVEL%.
    pause
)
