@echo off
REM Batch morphology + spectroscopy analysis launcher (Windows)
REM Expects a local conda/venv Python on PATH, or .conda\python.exe beside the repo.

cd /d "%~dp0\.."

set "PY="
if exist ".conda\python.exe" set "PY=.conda\python.exe"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
if "%PY%"=="" set "PY=python"

echo Starting Simplified Morphology + Spectroscopy Analysis...
echo.
echo Place Agilent project folders under inputs\ then press Enter when prompted,
echo or pass a custom path.
echo Results are written under outputs\ by default.
echo.

"%PY%" scripts\batch_morphology_analysis.py %*

echo.
echo Analysis complete! Press any key to exit.
pause >nul
