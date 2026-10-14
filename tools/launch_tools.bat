@echo off
setlocal
cd /d "%~dp0.."
set PYTHONPATH=src

if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
) else (
    set PYTHON_BIN=python
)

:menu
cls
echo ========================================================================
echo                 LMFT-LAB DEVELOPER TOOLING SUITE
echo ========================================================================
echo.
echo   [1] Brain Observatory       - Interactive Visual Web Dashboard (HTML)
echo   [2] Talk to LMFT            - Interactive Living Pair-Interaction CLI
echo   [3] Mindprint Diagnostic    - Ephemeral Digital-Twin Psychometric Test
echo   [4] Intersubjective Chamber - Dual-LMFT Dialogue Symposium
echo   [5] Exit
echo.
echo ========================================================================
set /p choice="Select an option [1-5]: "

if "%choice%"=="1" (
    start "" "tools\observatory.html"
    goto menu
)
if "%choice%"=="2" (
    cls
    "%PYTHON_BIN%" tools\talk_to_lmft.py
    pause
    goto menu
)
if "%choice%"=="3" (
    cls
    "%PYTHON_BIN%" tools\mindprint_diagnostic.py
    echo.
    pause
    goto menu
)
if "%choice%"=="4" (
    cls
    "%PYTHON_BIN%" tools\symposium.py
    echo.
    pause
    goto menu
)
if "%choice%"=="5" (
    exit /b 0
)

echo Invalid choice. Please select 1 through 5.
timeout /t 2 >nul
goto menu
