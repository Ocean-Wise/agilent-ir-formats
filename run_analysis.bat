@echo off
REM Simplified Morphology + Spectroscopy Analysis Launcher
REM This script runs the Python analysis tool

cd /d "%~dp0"
if not exist ".conda\python.exe" (
    echo Error: .conda\python.exe not found. Please ensure the conda environment is set up.
    pause
    exit /b 1
)

echo Starting Simplified Morphology + Spectroscopy Analysis...
echo.
echo This tool will:
echo 1. Ask for a directory path to search for .dmt files
echo 2. Show default path: C:\Users\Stephanie.Wang\Downloads (configurable in script)
echo 3. Find all .dmt files in that directory and subdirectories
echo 4. Process each file using threshold = mean + 2*std
echo 5. Perform PCA analysis on all particles
echo 6. Write results to CSV with dmt_file column
echo.

".conda\python.exe" batch_simplified_morphology_analysis.py

echo.
echo Analysis complete! Press any key to exit.
pause >nul