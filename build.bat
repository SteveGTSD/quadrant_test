@echo off
REM Build script for Quadrant.exe
REM Run this from the quadrant_project folder

echo ============================================
echo Building Quadrant.exe
echo ============================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

REM Install dependencies
echo.
echo Installing dependencies...
pip install pandas openpyxl plotly pyinstaller

REM Build single-file executable
echo.
echo Building executable...
pyinstaller --onefile --name Quadrant --clean quadrant.py

if exist dist\Quadrant.exe (
    echo.
    echo ============================================
    echo SUCCESS! Executable created at:
    echo   dist\Quadrant.exe
    echo.
    echo Copy Quadrant.exe to your Excel folder.
    echo ============================================
) else (
    echo.
    echo ERROR: Build failed. Check the output above.
)

pause
