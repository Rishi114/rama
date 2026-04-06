@echo off
REM RAMA AI - Launcher (Double-click to run!)
cd /d "%~dp0"

echo.
echo 🤖 Starting RAMA AI...
echo.

REM Try py launcher first (Windows built-in)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using py launcher
    py main.py --cli
    goto :end
)

REM Try python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using python
    python main.py --cli
    goto :end
)

REM Try python3
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Using python3
    python3 main.py --cli
    goto :end
)

echo.
echo ❌ Python not installed!
echo.
echo Download from: https://www.python.org/downloads/
echo IMPORTANT: Check "Add Python to PATH"
echo.
pause

:end